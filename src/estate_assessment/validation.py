from __future__ import annotations

import csv
from pathlib import Path

REQUIRED_FILES = [
    "database_estate_inventory.csv",
    "estate_dependencies.csv",
    "compatibility_assessment.csv",
    "workload_classification.csv",
    "target_service_decisions.csv",
    "migration_complexity.csv",
    "migration_wave_plan.csv",
    "modernisation_risk_register.csv",
]

VALID_EVIDENCE_CLASSES = {
    "synthetic assumption",
    "derived evidence",
    "locally measured",
    "requires live estate validation",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def validate_assessment_outputs(outputs_dir: Path) -> list[str]:
    failures: list[str] = []
    for filename in REQUIRED_FILES:
        path = outputs_dir / filename
        if not path.is_file():
            failures.append(f"missing output: {filename}")
        elif not read_csv(path):
            failures.append(f"empty output: {filename}")
    if failures:
        return failures

    inventory = read_csv(outputs_dir / "database_estate_inventory.csv")
    dependencies = read_csv(outputs_dir / "estate_dependencies.csv")
    compatibility = read_csv(outputs_dir / "compatibility_assessment.csv")
    targets = read_csv(outputs_dir / "target_service_decisions.csv")
    complexity = read_csv(outputs_dir / "migration_complexity.csv")
    waves = read_csv(outputs_dir / "migration_wave_plan.csv")
    risks = read_csv(outputs_dir / "modernisation_risk_register.csv")

    system_ids = {row["system_id"] for row in inventory}
    required_systems = {
        "legacy_tms",
        "billing_ops",
        "depot_partner_feeds",
        "shipment_event_stream",
    }
    if required_systems - system_ids:
        failures.append(f"inventory missing systems: {sorted(required_systems - system_ids)}")

    for row in inventory:
        for field in (
            "database_size_evidence",
            "growth_evidence",
            "transaction_volume_evidence",
        ):
            if row[field] not in VALID_EVIDENCE_CLASSES:
                failures.append(f"{row['system_id']} has invalid evidence class in {field}")

    if not any(row["evidence_class"] == "locally measured" for row in dependencies):
        failures.append("dependencies must include locally measured evidence")

    if not any(row["severity"] == "high" for row in compatibility):
        failures.append("compatibility assessment must include at least one high finding")

    if not all(row["remediation"] and row["migration_impact"] for row in compatibility):
        failures.append("compatibility findings require remediation and migration impact")

    target_names = {row["selected_target"] for row in targets}
    if "Azure SQL Managed Instance" not in target_names:
        failures.append("target decisions must include Azure SQL Managed Instance")
    if "Azure Database for PostgreSQL" not in target_names:
        failures.append("target decisions must include Azure Database for PostgreSQL")
    if "Azure Databricks" not in target_names:
        failures.append("target decisions must include Azure Databricks")
    if not all(row["rejected_alternatives"] for row in targets):
        failures.append("target decisions must explain rejected alternatives")

    for row in complexity:
        total = float(row["weighted_total"])
        if total < 1 or total > 5:
            failures.append(f"{row['system_id']} weighted_total outside 1-5 range")

    if [row["wave"] for row in waves] != ["Wave 0", "Wave 1", "Wave 2", "Wave 3"]:
        failures.append("migration waves must be Wave 0 through Wave 3 in order")

    required_risk_categories = {
        "downtime risk",
        "compatibility risk",
        "data loss",
        "performance regression",
        "security misconfiguration",
        "identity transition",
        "dependency failure",
        "schema drift",
        "operational readiness",
        "cost uncertainty",
        "skills/operational ownership",
    }
    risk_categories = {row["risk_category"] for row in risks}
    if required_risk_categories - risk_categories:
        failures.append(
            f"risk register missing: {sorted(required_risk_categories - risk_categories)}"
        )

    return failures
