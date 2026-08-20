from __future__ import annotations

import csv
import hashlib
from pathlib import Path

from migration_factory.catalog import MANIFESTS, REMEDIATIONS
from migration_factory.execution import run_migration_factory
from migration_factory.validation import validate_migration_outputs


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


def test_manifest_completeness() -> None:
    by_system = {manifest.source_system: manifest for manifest in MANIFESTS}
    assert {"legacy_tms", "billing_ops"} <= set(by_system)
    assert by_system["legacy_tms"].target_service == "Azure SQL Managed Instance"
    assert "PostgreSQL" in by_system["billing_ops"].target_service
    assert all(manifest.rollback_trigger for manifest in MANIFESTS)
    assert all(manifest.hypercare_period for manifest in MANIFESTS)


def test_remediation_traceability_covers_required_statuses() -> None:
    statuses = {remediation.status for remediation in REMEDIATIONS}
    assert "implemented locally" in statuses
    assert "accepted risk" in statuses
    assert "deferred" in statuses
    assert "requires live validation" in statuses
    assert any(remediation.compatibility_finding == "SQL-COMP-001" for remediation in REMEDIATIONS)


def test_migration_execution_is_deterministic(tmp_path: Path) -> None:
    first = tmp_path / "first"
    second = tmp_path / "second"
    run_migration_factory(first / "outputs" / "migration", first / "reports")
    run_migration_factory(second / "outputs" / "migration", second / "reports")
    assert _digest_tree(first) == _digest_tree(second)


def test_default_migration_outputs_validate(tmp_path: Path) -> None:
    outputs = tmp_path / "outputs" / "migration"
    reports = tmp_path / "reports"
    run_migration_factory(outputs, reports)
    assert validate_migration_outputs(outputs) == []
    assert (reports / "migration_factory_report.md").is_file()


def test_schema_conversion_mapping_and_evidence(tmp_path: Path) -> None:
    outputs = tmp_path / "outputs" / "migration"
    run_migration_factory(outputs, tmp_path / "reports")
    schema = _read_csv(outputs / "schema_conversion_report.csv")
    assert any(row["source_definition"] == "ntext" for row in schema)
    assert any("IX_Shipment_Route_Status_CreatedAt" in row["target_definition"] for row in schema)
    assert any(row["source_system"] == "billing_ops" for row in schema)


def test_reconciliation_contains_required_checks(tmp_path: Path) -> None:
    outputs = tmp_path / "outputs" / "migration"
    run_migration_factory(outputs, tmp_path / "reports")
    reconciliation = _read_csv(outputs / "data_reconciliation.csv")
    check_types = {row["check_type"] for row in reconciliation}
    assert "row_count" in check_types
    assert "business_key_count" in check_types
    assert "referential_integrity" in check_types
    assert "invoice_payment_total_sanity" in check_types
    assert "shipment_event_chronology" in check_types
    assert all(row["status"] == "passed" for row in reconciliation)


def test_validation_gate_behavior_keeps_cloud_checks_required(tmp_path: Path) -> None:
    outputs = tmp_path / "outputs" / "migration"
    run_migration_factory(outputs, tmp_path / "reports")
    gates = _read_csv(outputs / "validation_gates.csv")
    assert any(row["gate_stage"] == "PRE-MIGRATION" for row in gates)
    assert any(row["gate_stage"] == "PRE-CUTOVER" for row in gates)
    assert any(row["gate_stage"] == "POST-CUTOVER" for row in gates)
    assert any(row["status"] == "required" for row in gates)
    assert not any(row["status"] == "failed" for row in gates)


def test_wave_cutover_and_rollback_readiness(tmp_path: Path) -> None:
    outputs = tmp_path / "outputs" / "migration"
    run_migration_factory(outputs, tmp_path / "reports")
    waves = _read_csv(outputs / "migration_wave_execution.csv")
    cutover = _read_csv(outputs / "cutover_readiness.csv")
    rollback = _read_csv(outputs / "rollback_readiness.csv")
    assert [row["wave"] for row in waves] == ["Wave 0", "Wave 1", "Wave 2", "Wave 3"]
    assert any(row["cutover_check"] == "go/no-go decision" for row in cutover)
    assert any(row["rollback_item"] == "data divergence risk" for row in rollback)


def test_failure_scenarios_fail_safely(tmp_path: Path) -> None:
    outputs = tmp_path / "outputs" / "migration"
    run_migration_factory(outputs, tmp_path / "reports", failure_scenario="row_count_mismatch")
    reconciliation = _read_csv(outputs / "data_reconciliation.csv")
    gates = _read_csv(outputs / "validation_gates.csv")
    assert any(row["status"] == "failed" for row in reconciliation)
    assert any(row["status"] == "failed" for row in gates)


def test_scoped_execution_supports_single_system(tmp_path: Path) -> None:
    outputs = tmp_path / "outputs" / "migration"
    run_migration_factory(outputs, tmp_path / "reports", system="billing_ops")
    manifest = _read_csv(outputs / "migration_manifest.csv")
    assert {row["source_system"] for row in manifest} == {"billing_ops"}
    assert (outputs / "local_targets" / "billing_ops_postgresql" / "invoice.csv").is_file()

