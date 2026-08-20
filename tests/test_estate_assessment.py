from __future__ import annotations

import csv
import hashlib
from pathlib import Path

from estate_assessment.cli import generate_assessment
from estate_assessment.inventory import DEPENDENCIES, SYSTEMS
from estate_assessment.rules import (
    COMPLEXITY_WEIGHTS,
    compatibility_rows,
    migration_complexity,
    migration_wave_plan,
    target_service_decisions,
    workload_classifications,
)
from estate_assessment.validation import validate_assessment_outputs


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def _digest_tree(path: Path) -> str:
    digest = hashlib.sha256()
    for file_path in sorted(path.rglob("*")):
        if file_path.is_file():
            digest.update(str(file_path.relative_to(path)).encode("utf-8"))
            digest.update(file_path.read_bytes())
    return digest.hexdigest()


def test_inventory_covers_all_current_source_systems() -> None:
    system_ids = {system.system_id for system in SYSTEMS}
    assert {
        "legacy_tms",
        "billing_ops",
        "depot_partner_feeds",
        "shipment_event_stream",
    } <= system_ids
    assert all(system.business_criticality for system in SYSTEMS)
    assert all(system.technical_debt_indicators for system in SYSTEMS)


def test_dependency_model_covers_required_dependency_types() -> None:
    dependency_types = {dependency.dependency_type for dependency in DEPENDENCIES}
    assert "application_database" in dependency_types
    assert "stored_procedure_table" in dependency_types
    assert "cross_system_identifier" in dependency_types
    assert "file_feed_reference" in dependency_types
    assert "event_producer" in dependency_types
    assert "identity_transition" in dependency_types
    assert "operational_schedule" in dependency_types


def test_compatibility_rules_emit_meaningful_findings() -> None:
    findings = compatibility_rows()
    finding_ids = {row["finding_id"] for row in findings}
    assert "SQL-COMP-001" in finding_ids
    assert "SQL-COMP-005" in finding_ids
    assert "SQL-COMP-009" in finding_ids
    assert any(row["severity"] == "high" for row in findings)
    assert all(row["remediation"] and row["migration_impact"] for row in findings)


def test_target_decision_logic_selects_and_rejects_plausible_targets() -> None:
    decisions = {row["workload_or_system"]: row for row in target_service_decisions()}
    assert decisions["legacy_tms"]["selected_target"] == "Azure SQL Managed Instance"
    assert decisions["billing_ops"]["selected_target"] == "Azure Database for PostgreSQL"
    assert decisions["operational_reporting"]["selected_target"] == "Azure Databricks"
    assert decisions["customer_service_search"]["selected_target"] == "retain temporarily"
    assert "Cosmos DB" in decisions["operational_reporting"]["rejected_alternatives"]


def test_migration_complexity_scoring_is_deterministic_and_weighted() -> None:
    assert round(sum(COMPLEXITY_WEIGHTS.values()), 2) == 1.0
    first = migration_complexity()
    second = migration_complexity()
    assert first == second
    by_system = {row["system_id"]: row for row in first}
    assert by_system["legacy_tms"]["complexity_classification"] == "high"
    assert by_system["depot_partner_feeds"]["complexity_classification"] == "low"


def test_workload_classification_uses_simulator_evidence() -> None:
    workloads = {row["workload_id"]: row for row in workload_classifications()}
    assert workloads["create_shipment"]["category"] == "transactional OLTP"
    assert workloads["update_shipment_status"]["category"] == "event/streaming"
    assert workloads["analytical_delay_report"]["category"] == "analytical"
    assert all(int(row["operation_count_in_sample"]) >= 0 for row in workloads.values())


def test_migration_waves_are_ordered_and_dependency_aware() -> None:
    waves = migration_wave_plan()
    assert [row["wave"] for row in waves] == ["Wave 0", "Wave 1", "Wave 2", "Wave 3"]
    assert "legacy_tms" in waves[-1]["included_systems"]
    assert "operational_reporting" in waves[1]["included_systems"]
    assert all(row["rollback_considerations"] for row in waves)


def test_assessment_outputs_are_generated_and_validated(tmp_path: Path) -> None:
    outputs_dir = tmp_path / "outputs"
    reports_dir = tmp_path / "reports"
    generate_assessment(outputs_dir, reports_dir)

    assert validate_assessment_outputs(outputs_dir) == []
    assert (reports_dir / "estate_assessment_report.md").is_file()
    assert _read_csv(outputs_dir / "database_estate_inventory.csv")
    assert _read_csv(outputs_dir / "modernisation_risk_register.csv")


def test_assessment_generation_is_deterministic(tmp_path: Path) -> None:
    first = tmp_path / "first"
    second = tmp_path / "second"
    generate_assessment(first / "outputs", first / "reports")
    generate_assessment(second / "outputs", second / "reports")
    assert _digest_tree(first) == _digest_tree(second)
