from __future__ import annotations

import hashlib
from pathlib import Path

from databricks_pipelines.catalog import (
    BRONZE_TABLES,
    GOLD_PRODUCTS,
    INGESTION,
    TRACEABILITY,
)
from databricks_pipelines.cli import generate_outputs
from databricks_pipelines.transformations import (
    billing_revenue_gold,
    bronze_rows,
    deduplicate_events,
    delivery_delay_gold,
    detect_carrier_schema_drift,
    read_csv_rows,
    read_json_array,
    read_jsonl,
    scd_type2_customer_dimension,
    shipment_operations_gold,
    transform_depots,
    transform_service_cases,
    transform_shipments,
)
from databricks_pipelines.validation import validate_outputs

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "data/samples/legacy_estate/tiny"


def _digest_tree(path: Path) -> str:
    digest = hashlib.sha256()
    for file_path in sorted(path.rglob("*")):
        if file_path.is_file():
            digest.update(str(file_path.relative_to(path)).encode("utf-8"))
            digest.update(file_path.read_bytes())
    return digest.hexdigest()


def test_ingestion_metadata_is_complete() -> None:
    sources = {item.source for item in INGESTION}
    assert {
        "legacy_tms",
        "billing_ops",
        "depot_reference_feed",
        "carrier_updates",
        "customer_service_export",
        "shipment_operational_events",
    } == sources
    bronze_tables = {item.table_name for item in BRONZE_TABLES}
    assert {item.bronze_target for item in INGESTION} <= bronze_tables
    assert all(item.checkpoint_requirement for item in INGESTION)


def test_bronze_rows_preserve_payload_and_metadata() -> None:
    customers = read_csv_rows(FIXTURES / "legacy_oltp/customers.csv")
    bronze = bronze_rows(customers[:2], "legacy_tms", "customers")
    assert bronze[0]["_source_system"] == "legacy_tms"
    assert bronze[0]["_raw_payload"]
    assert bronze[0]["_record_hash"] != bronze[1]["_record_hash"]
    assert bronze[0]["customer_id"] == customers[0]["customer_id"]


def test_silver_transformations_route_invalid_records_to_quarantine() -> None:
    shipments = read_csv_rows(FIXTURES / "legacy_oltp/shipments.csv")
    customers = read_csv_rows(FIXTURES / "legacy_oltp/customers.csv")
    routes = read_csv_rows(FIXTURES / "legacy_oltp/routes.csv")
    accepted_shipments, shipment_quarantine = transform_shipments(shipments, customers, routes)
    assert accepted_shipments
    assert shipment_quarantine == []

    depot_rows = read_csv_rows(FIXTURES / "file_feeds/depot_reference_feed.csv")
    accepted_depots, depot_quarantine = transform_depots(depot_rows)
    assert accepted_depots
    assert any("missing capacity_units" in item["errors"] for item in depot_quarantine)

    service_cases = read_csv_rows(FIXTURES / "secondary_billing/service_cases.csv")
    accepted_cases, case_quarantine = transform_service_cases(service_cases, shipments)
    assert accepted_cases
    assert any("invalid contact_email" in item["errors"] for item in case_quarantine)
    assert any("unknown shipment_id" in item["errors"] for item in case_quarantine)


def test_streaming_event_deduplication_and_late_event_handling() -> None:
    events = read_jsonl(FIXTURES / "events/shipment_operational_events.jsonl")
    accepted, quarantine = deduplicate_events(events)
    assert accepted
    assert any("duplicate event_id" in item["errors"] for item in quarantine)
    assert any("late or out-of-order event" in item["errors"] for item in quarantine)


def test_schema_drift_detection_for_carrier_updates() -> None:
    carrier_updates = read_json_array(FIXTURES / "file_feeds/carrier_updates.json")
    drift = detect_carrier_schema_drift(carrier_updates)
    assert any(item["drift_type"] == "additive field" for item in drift)
    assert any("partner_eta_text" in item["fields"] for item in drift)


def test_scd_type2_customer_dimension_changes_current_row() -> None:
    customers = read_csv_rows(FIXTURES / "legacy_oltp/customers.csv")
    first_version = scd_type2_customer_dimension([], customers[:1], "2026-01-01T00:00:00Z")
    changed = dict(customers[0])
    changed["service_tier"] = "critical"
    second_version = scd_type2_customer_dimension(
        first_version,
        [changed],
        "2026-02-01T00:00:00Z",
    )
    versions = [row for row in second_version if row["customer_id"] == changed["customer_id"]]
    assert len(versions) == 2
    assert sum(1 for row in versions if row["is_current"]) == 1
    assert any(row["effective_end_utc"] == "2026-02-01T00:00:00Z" for row in versions)


def test_gold_aggregations_have_defined_grain() -> None:
    shipments = read_csv_rows(FIXTURES / "legacy_oltp/shipments.csv")
    customers = read_csv_rows(FIXTURES / "legacy_oltp/customers.csv")
    routes = read_csv_rows(FIXTURES / "legacy_oltp/routes.csv")
    silver_shipments, _ = transform_shipments(shipments, customers, routes)
    invoices = read_csv_rows(FIXTURES / "secondary_billing/invoices.csv")
    assert shipment_operations_gold(silver_shipments)
    assert delivery_delay_gold(silver_shipments)
    assert billing_revenue_gold(invoices)
    assert all(product.grain for product in GOLD_PRODUCTS)


def test_traceability_has_no_orphan_sources() -> None:
    assert {item.source for item in TRACEABILITY} == {item.source for item in INGESTION}
    assert all(item.gold_product.startswith("gold.") for item in TRACEABILITY)


def test_outputs_generate_validate_and_are_deterministic(tmp_path: Path) -> None:
    first = tmp_path / "first"
    second = tmp_path / "second"
    generate_outputs(first / "outputs" / "databricks_pipelines", first / "reports", ROOT)
    generate_outputs(second / "outputs" / "databricks_pipelines", second / "reports", ROOT)
    assert _digest_tree(first) == _digest_tree(second)
    assert validate_outputs(first / "outputs" / "databricks_pipelines", ROOT) == []

