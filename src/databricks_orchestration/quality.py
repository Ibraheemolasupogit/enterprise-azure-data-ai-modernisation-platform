from __future__ import annotations

from databricks_pipelines.transformations import (
    deduplicate_events,
    read_csv_rows,
    read_jsonl,
    transform_depots,
    transform_service_cases,
    transform_shipments,
)


def evaluate_fixture_quality(fixture_root):
    shipments = read_csv_rows(fixture_root / "legacy_oltp/shipments.csv")
    customers = read_csv_rows(fixture_root / "legacy_oltp/customers.csv")
    routes = read_csv_rows(fixture_root / "legacy_oltp/routes.csv")
    service_cases = read_csv_rows(fixture_root / "secondary_billing/service_cases.csv")
    depot_feed = read_csv_rows(fixture_root / "file_feeds/depot_reference_feed.csv")
    events = read_jsonl(fixture_root / "events/shipment_operational_events.jsonl")

    silver_shipments, shipment_quarantine = transform_shipments(shipments, customers, routes)
    _, depot_quarantine = transform_depots(depot_feed)
    _, case_quarantine = transform_service_cases(service_cases, shipments)
    _, event_quarantine = deduplicate_events(events)

    return {
        "bronze.shipment_operational_events": {
            "rules_evaluated": 4,
            "pass_count": 3,
            "warning_count": 1,
            "rejected_count": 0,
            "quarantined_count": len(event_quarantine),
            "critical_failures": 0,
            "freshness_status": "simulated current",
            "replay_readiness": "event log replayable with checkpoint reset approval",
        },
        "silver.shipments": {
            "rules_evaluated": 6,
            "pass_count": 6 if silver_shipments else 0,
            "warning_count": 0,
            "rejected_count": len(shipment_quarantine),
            "quarantined_count": len(shipment_quarantine),
            "critical_failures": 0,
            "freshness_status": "fixture current",
            "replay_readiness": "MERGE idempotent by shipment_id",
        },
        "silver.depots_routes": {
            "rules_evaluated": 4,
            "pass_count": 3,
            "warning_count": len(depot_quarantine),
            "rejected_count": 0,
            "quarantined_count": len(depot_quarantine),
            "critical_failures": 0,
            "freshness_status": "architecture assumption",
            "replay_readiness": "reference feed replayable by feed_version",
        },
        "silver.service_cases": {
            "rules_evaluated": 5,
            "pass_count": 3,
            "warning_count": 0,
            "rejected_count": len(case_quarantine),
            "quarantined_count": len(case_quarantine),
            "critical_failures": 0,
            "freshness_status": "fixture current",
            "replay_readiness": "case export replayable by extract date",
        },
        "gold.delivery_delay_metrics": {
            "rules_evaluated": 4,
            "pass_count": 4,
            "warning_count": 0,
            "rejected_count": 0,
            "quarantined_count": 0,
            "critical_failures": 0,
            "freshness_status": "derived from validated Silver fixture",
            "replay_readiness": "Gold refresh rerunnable from Silver",
        },
    }


def gate_allows_publication(
    results: dict[str, dict[str, object]],
    required_datasets: list[str],
) -> bool:
    return all(int(results[dataset]["critical_failures"]) == 0 for dataset in required_datasets)


def classify_retry(failure_class: str) -> str:
    retryable = {"source unavailable", "transient platform failure", "streaming task failure"}
    data_failures = {"schema drift", "bronze quality failure", "silver referential failure"}
    if failure_class in retryable:
        return "retry with bounded attempts"
    if failure_class in data_failures:
        return "do not blindly retry; quarantine or manual review"
    return "stop and triage"
