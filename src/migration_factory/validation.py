from __future__ import annotations

import csv
from pathlib import Path

REQUIRED_FILES = [
    "migration_manifest.csv",
    "compatibility_remediation.csv",
    "schema_conversion_report.csv",
    "data_reconciliation.csv",
    "validation_gates.csv",
    "migration_wave_execution.csv",
    "cutover_readiness.csv",
    "rollback_readiness.csv",
    "tool_integration_points.csv",
    "failure_scenarios.csv",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def validate_migration_outputs(outputs_dir: Path) -> list[str]:
    failures: list[str] = []
    for filename in REQUIRED_FILES:
        path = outputs_dir / filename
        if not path.is_file():
            failures.append(f"missing migration output: {filename}")
        elif not read_csv(path):
            failures.append(f"empty migration output: {filename}")
    if failures:
        return failures

    manifest = read_csv(outputs_dir / "migration_manifest.csv")
    remediations = read_csv(outputs_dir / "compatibility_remediation.csv")
    schema = read_csv(outputs_dir / "schema_conversion_report.csv")
    reconciliation = read_csv(outputs_dir / "data_reconciliation.csv")
    gates = read_csv(outputs_dir / "validation_gates.csv")
    waves = read_csv(outputs_dir / "migration_wave_execution.csv")
    cutover = read_csv(outputs_dir / "cutover_readiness.csv")
    rollback = read_csv(outputs_dir / "rollback_readiness.csv")
    tools = read_csv(outputs_dir / "tool_integration_points.csv")

    systems = {row["source_system"] for row in manifest}
    if not {"legacy_tms", "billing_ops"} <= systems:
        failures.append("migration manifest must include legacy_tms and billing_ops by default")

    valid_evidence = {
        "synthetic assumption",
        "locally validated",
        "derived from assessment",
        "requires live validation",
        "simulated evidence",
        "architecture/design evidence",
    }
    for row in manifest:
        if row["evidence_classification"] not in valid_evidence:
            failures.append(f"{row['migration_id']} has invalid evidence classification")
        if not row["rollback_trigger"] or not row["hypercare_period"]:
            failures.append(f"{row['migration_id']} missing rollback or hypercare metadata")

    remediation_statuses = {row["status"] for row in remediations}
    required_statuses = {
        "implemented locally",
        "accepted risk",
        "deferred",
        "requires live validation",
    }
    if not required_statuses <= remediation_statuses:
        failures.append("remediation register missing required status coverage")

    if not any(row["source_system"] == "legacy_tms" for row in schema):
        failures.append("schema conversion report missing legacy_tms")
    if not any(row["source_system"] == "billing_ops" for row in schema):
        failures.append("schema conversion report missing billing_ops")

    if not any(row["check_type"] == "referential_integrity" for row in reconciliation):
        failures.append("reconciliation missing referential integrity checks")
    if not any(row["check_type"] == "invoice_payment_total_sanity" for row in reconciliation):
        failures.append("reconciliation missing invoice/payment financial check")
    if not any(row["check_type"] == "shipment_event_chronology" for row in reconciliation):
        failures.append("reconciliation missing shipment/event chronology check")

    if any(row["status"] == "failed" for row in reconciliation):
        failures.append("default migration evidence has failed reconciliation rows")

    if not any(row["status"] == "required" for row in gates):
        failures.append("validation gates must retain cloud-only required checks")
    if not any(row["gate_stage"] == "PRE-CUTOVER" for row in gates):
        failures.append("validation gates missing PRE-CUTOVER")
    if not any(row["gate_stage"] == "POST-CUTOVER" for row in gates):
        failures.append("validation gates missing POST-CUTOVER")

    if [row["wave"] for row in waves] != ["Wave 0", "Wave 1", "Wave 2", "Wave 3"]:
        failures.append("migration wave execution must preserve Wave 0-3 ordering")

    if not all(row.get("rollback_trigger", True) for row in manifest):
        failures.append("manifest missing rollback trigger")
    if not cutover or not rollback:
        failures.append("cutover and rollback readiness outputs are required")
    if not any(row["tool_name"] == "Azure Database Migration Service" for row in tools):
        failures.append("tooling integration points must include Azure DMS boundary")
    if not any(row["tool_name"] == "pg_dump/pg_restore" for row in tools):
        failures.append(
            "tooling integration points must include PostgreSQL native tooling boundary"
        )

    return failures
