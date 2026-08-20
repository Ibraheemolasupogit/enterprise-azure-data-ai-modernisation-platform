from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

from legacy_estate.contracts import validate_depot_feed_row, validate_operational_event
from legacy_estate.generator import generate_estate
from legacy_estate.workload import generate_workload


def _digest_tree(path: Path) -> str:
    digest = hashlib.sha256()
    for file_path in sorted(path.rglob("*")):
        if file_path.is_file():
            digest.update(str(file_path.relative_to(path)).encode("utf-8"))
            digest.update(file_path.read_bytes())
    return digest.hexdigest()


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def _read_jsonl(path: Path) -> list[dict[str, object]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def test_generation_is_deterministic(tmp_path: Path) -> None:
    first = tmp_path / "first"
    second = tmp_path / "second"
    manifest = generate_estate(first, profile_name="tiny", seed=1234)
    generate_estate(second, profile_name="tiny", seed=1234)

    assert manifest["row_counts"]["shipments"] == 18
    assert _digest_tree(first) == _digest_tree(second)


def test_core_legacy_oltp_referential_integrity(tmp_path: Path) -> None:
    generate_estate(tmp_path, profile_name="tiny", seed=20260820)
    root = tmp_path / "legacy_oltp"
    customers = {row["customer_id"] for row in _read_csv(root / "customers.csv")}
    routes = {row["route_id"] for row in _read_csv(root / "routes.csv")}
    vehicles = {row["vehicle_id"] for row in _read_csv(root / "vehicles.csv")}
    shipments = _read_csv(root / "shipments.csv")
    shipment_ids = {row["shipment_id"] for row in shipments}

    assert shipments
    assert all(row["customer_id"] in customers for row in shipments)
    assert all(row["route_id"] in routes for row in shipments)
    assert all(row["assigned_vehicle_id"] in vehicles for row in shipments)

    events = _read_csv(root / "shipment_events.csv")
    assert all(row["shipment_id"] in shipment_ids for row in events)


def test_contract_validation_for_file_and_event_sources(tmp_path: Path) -> None:
    generate_estate(tmp_path, profile_name="tiny", seed=20260820)
    depot_rows = _read_csv(tmp_path / "file_feeds" / "depot_reference_feed.csv")
    operational_events = _read_jsonl(tmp_path / "events" / "shipment_operational_events.jsonl")

    assert all(validate_depot_feed_row(row) == [] for row in depot_rows)
    assert all(validate_operational_event(row) == [] for row in operational_events)


def test_known_anomalies_are_injected_and_traceable(tmp_path: Path) -> None:
    generate_estate(tmp_path, profile_name="tiny", seed=20260820)
    issues = json.loads((tmp_path / "data_quality_issues.json").read_text(encoding="utf-8"))
    issue_codes = {issue["issue_code"] for issue in issues}

    assert "DUPLICATE_CUSTOMER_ACCOUNT" in issue_codes
    assert "CASE_REFERENTIAL_ANOMALY" in issue_codes
    assert "DUPLICATE_AND_OUT_OF_ORDER_EVENT" in issue_codes
    assert "SCHEMA_DRIFT" in issue_codes

    customers = _read_csv(tmp_path / "legacy_oltp" / "customers.csv")
    account_numbers = [row["account_number"] for row in customers]
    assert len(account_numbers) > len(set(account_numbers))

    service_cases = _read_csv(tmp_path / "secondary_billing" / "service_cases.csv")
    known_shipments = {
        row["shipment_id"] for row in _read_csv(tmp_path / "legacy_oltp" / "shipments.csv")
    }
    assert any(row["shipment_id"] not in known_shipments for row in service_cases)


def test_workload_generation_is_deterministic_and_covers_profiles(tmp_path: Path) -> None:
    first_path = tmp_path / "workload_1.jsonl"
    second_path = tmp_path / "workload_2.jsonl"
    first = generate_workload(first_path, operations=300, seed=42)
    second = generate_workload(second_path, operations=300, seed=42)

    assert first == second
    assert first_path.read_text(encoding="utf-8") == second_path.read_text(encoding="utf-8")

    classifications = {row["classification"] for row in first}
    workload_types = {row["workload_type"] for row in first}
    assert {"oltp", "operational_reporting", "candidate_analytical"} <= classifications
    assert "create_shipment" in workload_types
    assert "update_shipment_status" in workload_types
    assert any(row["candidate_cdc_source"] for row in first)


def test_synthetic_data_uses_public_safe_domains(tmp_path: Path) -> None:
    generate_estate(tmp_path, profile_name="tiny", seed=20260820)
    text = "\n".join(
        file_path.read_text(encoding="utf-8")
        for file_path in tmp_path.rglob("*")
        if file_path.is_file()
    )

    assert "@gmail.com" not in text
    assert "@outlook.com" not in text
    assert "@hotmail.com" not in text
    assert "@synthetic.contoso.example" in text
    assert "No real personal data" in text
