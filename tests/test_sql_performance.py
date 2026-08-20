from __future__ import annotations

import csv
import hashlib
from pathlib import Path

from sql_performance.catalog import (
    BASELINE,
    BLOCKING_SCENARIOS,
    DEADLOCK_READINESS,
    INDEX_RECOMMENDATIONS,
    PARAMETER_SENSITIVITY,
    PERFORMANCE_ASSURANCE,
    QUERY_ANALYSIS,
    STATISTICS_STRATEGY,
    WORKLOADS,
)
from sql_performance.cli import generate_outputs
from sql_performance.validation import validate_outputs


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


def test_workload_catalog_completeness() -> None:
    workload_ids = {workload.workload_id for workload in WORKLOADS}
    assert {
        "customer_lookup",
        "shipment_create_update",
        "shipment_status_query",
        "route_depot_reporting",
        "incident_case_lookup",
        "analytical_delay_report",
    } <= workload_ids
    assert all(workload.candidate_tuning_technique for workload in WORKLOADS)


def test_baseline_is_deterministic_and_not_fake_azure_telemetry() -> None:
    assert len(BASELINE) == len(WORKLOADS)
    assert all(metric.execution_duration_ms > 0 for metric in BASELINE)
    assert not any(metric.metric_classification == "Azure measured" for metric in BASELINE)


def test_query_analysis_traceability_and_before_after_scenario() -> None:
    assert any(item.analysis_type == "before/after scenario" for item in QUERY_ANALYSIS)
    assert any(item.workload_id == "route_depot_reporting" for item in QUERY_ANALYSIS)
    assert all(item.recommendation for item in QUERY_ANALYSIS)


def test_index_recommendations_are_focused() -> None:
    assert any(
        "IX_Shipment_Route_Status_CreatedAt" in item.proposed_index
        for item in INDEX_RECOMMENDATIONS
    )
    assert len(INDEX_RECOMMENDATIONS) <= 8
    assert not any("every column" in item.rationale.lower() for item in INDEX_RECOMMENDATIONS)


def test_statistics_strategy_avoids_blanket_fullscan() -> None:
    assert any("Avoids blanket FULLSCAN" in item.rationale for item in STATISTICS_STRATEGY)
    assert any(item.area == "SQL Agent integration" for item in STATISTICS_STRATEGY)


def test_blocking_deadlock_and_parameter_sensitivity_coverage() -> None:
    assert len(BLOCKING_SCENARIOS) >= 3
    assert any("error 1205" in item.recommendation for item in DEADLOCK_READINESS)
    assert any("OPTION(RECOMPILE)" in item.recommendation for item in PARAMETER_SENSITIVITY)


def test_performance_assurance_covers_required_areas() -> None:
    areas = {item.area for item in PERFORMANCE_ASSURANCE}
    assert "workload coverage" in areas
    assert "Query Store readiness" in areas
    assert "regression detection" in areas
    assert "operational integration" in areas


def test_outputs_generate_validate_and_are_deterministic(tmp_path: Path) -> None:
    first = tmp_path / "first"
    second = tmp_path / "second"
    generate_outputs(first / "outputs" / "sql_performance", first / "reports")
    generate_outputs(second / "outputs" / "sql_performance", second / "reports")
    assert _digest_tree(first) == _digest_tree(second)
    assert validate_outputs(first / "outputs" / "sql_performance") == []
    assert _read_csv(first / "outputs" / "sql_performance" / "performance_assurance.csv")

