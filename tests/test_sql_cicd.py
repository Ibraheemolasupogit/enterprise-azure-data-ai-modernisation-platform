from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

from sql_cicd.catalog import (
    DATABASE_TESTS,
    DRIFT_SCENARIOS,
    PERFORMANCE_GATES,
    PROJECT_OBJECTS,
    PROMOTION_MATRIX,
    REFERENCE_DATA,
    RELEASE_READINESS,
    SAFETY_RULES,
    SECURITY_GATES,
    TRACEABILITY,
)
from sql_cicd.cli import generate_outputs
from sql_cicd.validation import validate_outputs

ROOT = Path(__file__).resolve().parents[1]


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


def test_sql_project_inventory_covers_core_objects() -> None:
    object_names = {item.object_name for item in PROJECT_OBJECTS}
    assert "CustomerAccount" in object_names
    assert "Shipment" in object_names
    assert "ShipmentEventHistory" in object_names
    assert "usp_CreateShipment" in object_names
    assert "usp_UpdateShipmentStatus" in object_names
    assert "Depot and Route seed" in object_names
    assert all((ROOT / item.source_path).is_file() for item in PROJECT_OBJECTS)


def test_traceability_links_database_objects_to_release_gates() -> None:
    assert any(
        "IX_Shipment_Route_Status_CreatedAt" in item.database_object
        for item in TRACEABILITY
    )
    assert all(item.release_gate for item in TRACEABILITY)
    assert any(item.requirement_id == "req-005" for item in TRACEABILITY)


def test_reference_data_is_idempotent_and_natural_key_based() -> None:
    assert {item.target_table for item in REFERENCE_DATA} == {"dbo.Depot", "dbo.Route"}
    assert all(item.row_count > 0 for item in REFERENCE_DATA)
    assert all("MERGE" in item.deployment_method for item in REFERENCE_DATA)
    assert all(
        "natural" in item.idempotency_strategy or item.key_columns
        for item in REFERENCE_DATA
    )


def test_safety_drift_and_promotion_controls_are_explicit() -> None:
    assert any(rule.failure_action == "stop release" for rule in SAFETY_RULES)
    assert any(rule.area == "destructive changes" for rule in SAFETY_RULES)
    assert any(scenario.drift_type == "manual hotfix" for scenario in DRIFT_SCENARIOS)
    assert {environment.environment for environment in PROMOTION_MATRIX} == {
        "local",
        "dev",
        "test",
        "prod",
    }


def test_database_tests_and_regression_gates_cover_build_security_performance() -> None:
    assert any(test.required_for_release == "tooling dependent" for test in DATABASE_TESTS)
    assert any(gate.release_decision == "block promotion" for gate in PERFORMANCE_GATES)
    assert any(gate.area == "secret handling" for gate in SECURITY_GATES)
    assert any(item.status == "tooling dependent" for item in RELEASE_READINESS)


def test_outputs_generate_validate_and_are_deterministic(tmp_path: Path) -> None:
    first = tmp_path / "first"
    second = tmp_path / "second"
    generate_outputs(first / "outputs" / "sql_cicd", first / "reports", ROOT)
    generate_outputs(second / "outputs" / "sql_cicd", second / "reports", ROOT)
    assert _digest_tree(first) == _digest_tree(second)
    assert validate_outputs(first / "outputs" / "sql_cicd", ROOT) == []
    manifest = json.loads(
        (first / "outputs" / "sql_cicd" / "release_manifest.json").read_text(encoding="utf-8")
    )
    assert manifest["database"] == "legacy_tms"
    assert manifest["evidence_boundary"] == "local static evidence; no Azure deployment performed"
    assert _read_csv(first / "outputs" / "sql_cicd" / "release_readiness.csv")
