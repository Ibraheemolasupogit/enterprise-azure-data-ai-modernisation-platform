from __future__ import annotations

import csv
from pathlib import Path

REQUIRED_FILES = [
    "workload_target_matrix.csv",
    "security_control_matrix.csv",
    "recovery_strategy_matrix.csv",
    "architecture_traceability.csv",
    "environment_matrix.csv",
    "assumption_register.csv",
    "target_component_catalog.csv",
]

VALID_STATUS = {"planned", "implemented"}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def validate_architecture_outputs(outputs_dir: Path) -> list[str]:
    failures: list[str] = []
    for filename in REQUIRED_FILES:
        path = outputs_dir / filename
        if not path.is_file():
            failures.append(f"missing architecture output: {filename}")
        elif not read_csv(path):
            failures.append(f"empty architecture output: {filename}")
    if failures:
        return failures

    components = read_csv(outputs_dir / "target_component_catalog.csv")
    workload_targets = read_csv(outputs_dir / "workload_target_matrix.csv")
    security = read_csv(outputs_dir / "security_control_matrix.csv")
    recovery = read_csv(outputs_dir / "recovery_strategy_matrix.csv")
    traceability = read_csv(outputs_dir / "architecture_traceability.csv")
    environments = read_csv(outputs_dir / "environment_matrix.csv")
    assumptions = read_csv(outputs_dir / "assumption_register.csv")

    component_ids = {row["component_id"] for row in components}
    component_refs = {row["selected_target_component"] for row in workload_targets}
    for row in traceability:
        component_refs.update(part.strip() for part in row["target_component"].split(";"))
    missing_components = component_refs - component_ids
    if missing_components:
        failures.append(f"architecture references missing components: {sorted(missing_components)}")

    for row in components:
        if not row["purpose"]:
            failures.append(f"{row['component_id']} has no documented purpose")
        if row["implementation_status"] != "planned":
            failures.append(f"{row['component_id']} is falsely marked implemented")

    required_workloads = {
        "legacy_tms",
        "billing_ops",
        "depot_partner_feeds",
        "shipment_event_stream",
        "operational_reporting",
        "customer_service_search",
    }
    workloads = {row["workload_id"] for row in workload_targets}
    if required_workloads - workloads:
        failures.append(f"workload target matrix missing: {sorted(required_workloads - workloads)}")

    critical_assets = {"SQL MI", "PostgreSQL", "ADLS", "Databricks", "Key Vault"}
    security_assets = " ".join(row["applies_to_assets"] for row in security)
    for asset in critical_assets:
        if asset not in security_assets:
            failures.append(f"security controls do not cover {asset}")

    if not all(row["assumed_rto_minutes"] and row["assumed_rpo_minutes"] for row in recovery):
        failures.append("all recovery rows must assign RTO/RPO values")
    if any(row["validation_status"] != "not tested" for row in recovery):
        failures.append("DR must not be marked tested in Milestone 4")

    if {row["environment"] for row in environments} != {"dev", "test", "prod"}:
        failures.append("environment matrix must include dev/test/prod")

    valid_assumption_classes = {
        "known synthetic evidence",
        "estimated design assumption",
        "requires live validation",
        "derived evidence",
    }
    for row in assumptions:
        if row["classification"] not in valid_assumption_classes:
            failures.append(f"{row['assumption_id']} has invalid assumption classification")

    if not traceability:
        failures.append("architecture traceability cannot be empty")
    if not all(row["future_implementation_milestone"] for row in traceability):
        failures.append("traceability rows must map to future implementation milestones")

    return failures

