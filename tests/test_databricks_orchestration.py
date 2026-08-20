from __future__ import annotations

import hashlib
from pathlib import Path

from databricks_orchestration.catalog import (
    BACKFILL,
    DEPENDENCIES,
    JOBS,
    PERMISSIONS,
    QUALITY_RULES,
    RETRIES,
    SCHEDULES,
    SEVERITY,
    TRACEABILITY,
    quality_results,
)
from databricks_orchestration.cli import generate_outputs
from databricks_orchestration.quality import classify_retry, gate_allows_publication
from databricks_orchestration.validation import validate_outputs

ROOT = Path(__file__).resolve().parents[1]


def _digest_tree(path: Path) -> str:
    digest = hashlib.sha256()
    for file_path in sorted(path.rglob("*")):
        if file_path.is_file():
            digest.update(str(file_path.relative_to(path)).encode("utf-8"))
            digest.update(file_path.read_bytes())
    return digest.hexdigest()


def test_quality_rules_cover_required_categories_and_actions() -> None:
    categories = {rule.rule_category for rule in QUALITY_RULES}
    assert {
        "completeness",
        "validity",
        "uniqueness",
        "referential integrity",
        "consistency",
        "timeliness",
        "freshness",
        "schema conformity",
        "business rule",
    } <= categories
    assert all(rule.severity and rule.action_on_failure for rule in QUALITY_RULES)
    assert {"INFO", "WARNING", "ERROR", "CRITICAL"} == {row.severity for row in SEVERITY}


def test_quality_results_are_fixture_derived_and_route_quarantine() -> None:
    results = {row.dataset: row for row in quality_results()}
    assert results["bronze.shipment_operational_events"].quarantined_count > 0
    assert results["silver.service_cases"].quarantined_count > 0
    assert results["gold.delivery_delay_metrics"].critical_failures == 0


def test_publication_gate_blocks_critical_failures() -> None:
    assert gate_allows_publication({"gold": {"critical_failures": 0}}, ["gold"])
    assert not gate_allows_publication({"gold": {"critical_failures": 1}}, ["gold"])


def test_dependency_graph_blocks_then_allows_publication() -> None:
    assert any(dep.gate_behavior.startswith("critical failure blocks") for dep in DEPENDENCIES)
    assert any(dep.downstream_publication_allowed == "no" for dep in DEPENDENCIES)
    assert any(dep.downstream_publication_allowed == "yes" for dep in DEPENDENCIES)
    task_keys = {dep.task_key for dep in DEPENDENCIES}
    assert "gold_quality_gate" in task_keys
    assert "publish_readiness" in task_keys


def test_jobs_are_parameterized_and_scheduled_with_rationale() -> None:
    assert all(job.purpose for job in JOBS)
    assert all("environment" in job.parameters for job in JOBS)
    assert any("replay_mode" in job.parameters for job in JOBS)
    assert all(schedule.rationale for schedule in SCHEDULES)
    assert any(schedule.workflow == "event_streaming_workflow" for schedule in SCHEDULES)


def test_retry_classification_separates_transient_from_data_failures() -> None:
    assert classify_retry("source unavailable") == "retry with bounded attempts"
    assert classify_retry("schema drift") == "do not blindly retry; quarantine or manual review"
    assert any("no blind retry" in policy.action.lower() for policy in RETRIES)


def test_backfill_permissions_and_traceability_are_complete() -> None:
    assert any(
        item.area == "backfill" and item.target == "shipment_operational_events"
        for item in BACKFILL
    )
    assert any(permission.role == "service principal" for permission in PERMISSIONS)
    assert {row.source for row in TRACEABILITY} == {
        "legacy_tms",
        "billing_ops",
        "depot_reference_feed",
        "carrier_updates",
        "customer_service_export",
        "shipment_operational_events",
    }
    assert all(row.publication_readiness == "publish_readiness" for row in TRACEABILITY)


def test_outputs_generate_validate_and_are_deterministic(tmp_path: Path) -> None:
    first = tmp_path / "first"
    second = tmp_path / "second"
    generate_outputs(first / "outputs" / "databricks_orchestration", first / "reports", ROOT)
    generate_outputs(second / "outputs" / "databricks_orchestration", second / "reports", ROOT)
    assert _digest_tree(first) == _digest_tree(second)
    assert validate_outputs(first / "outputs" / "databricks_orchestration", ROOT) == []
