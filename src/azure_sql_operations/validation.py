from __future__ import annotations

import csv
from pathlib import Path

REQUIRED_FILES = [
    "configuration_baseline.csv",
    "security_role_matrix.csv",
    "sensitive_data_controls.csv",
    "monitoring_catalog.csv",
    "alert_catalog.csv",
    "automation_catalog.csv",
    "backup_restore_readiness.csv",
    "ha_dr_readiness.csv",
    "operational_readiness.csv",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def validate_outputs(outputs_dir: Path) -> list[str]:
    failures: list[str] = []
    for filename in REQUIRED_FILES:
        path = outputs_dir / filename
        if not path.is_file():
            failures.append(f"missing Azure SQL operations output: {filename}")
        elif not read_csv(path):
            failures.append(f"empty Azure SQL operations output: {filename}")
    if failures:
        return failures

    config = read_csv(outputs_dir / "configuration_baseline.csv")
    roles = read_csv(outputs_dir / "security_role_matrix.csv")
    sensitive = read_csv(outputs_dir / "sensitive_data_controls.csv")
    monitoring = read_csv(outputs_dir / "monitoring_catalog.csv")
    alerts = read_csv(outputs_dir / "alert_catalog.csv")
    automation = read_csv(outputs_dir / "automation_catalog.csv")
    backup = read_csv(outputs_dir / "backup_restore_readiness.csv")
    hadr = read_csv(outputs_dir / "ha_dr_readiness.csv")
    readiness = read_csv(outputs_dir / "operational_readiness.csv")

    config_settings = {row["setting"]: row for row in config}
    for required in ("target_service", "backup_retention", "public_endpoint", "minimum_tls"):
        if required not in config_settings:
            failures.append(f"configuration baseline missing {required}")
    if config_settings.get("target_service", {}).get("value") != "Azure SQL Managed Instance":
        failures.append("configuration target must preserve Azure SQL Managed Instance decision")

    if not any(row["principal_type"] == "Managed identity" for row in roles):
        failures.append("security role matrix must include managed identities")
    if any("password" in row["placeholder_principal"].lower() for row in roles):
        failures.append("security roles must not include secret-like principals")
    if not all(row["least_privilege_rationale"] for row in roles):
        failures.append("all roles require least-privilege rationale")

    if not all(row["controls"] for row in sensitive):
        failures.append("every sensitive asset must map to controls")
    if not any("Dynamic Data Masking" in row["controls"] for row in sensitive):
        failures.append("sensitive controls must include Dynamic Data Masking where justified")
    if not any("Row-Level Security" in row["controls"] for row in sensitive):
        failures.append("sensitive controls must include Row-Level Security where justified")

    signals = {row["signal"] for row in monitoring}
    for signal in ("cpu_percent", "storage_percent", "deadlock", "database_unavailable"):
        if signal not in signals:
            failures.append(f"monitoring missing {signal}")

    runbook_paths = [Path(row["runbook"]) for row in alerts]
    for runbook in runbook_paths:
        if not runbook.is_file():
            failures.append(f"alert references missing runbook: {runbook}")
    if not any(row["signal"] == "backup_restore_event" for row in alerts):
        failures.append("alerts must include backup/recovery issue")

    if not any(row["mechanism"] == "SQL Agent on Managed Instance" for row in automation):
        failures.append("automation catalog must include SQL Agent assets")
    if any("blanket index rebuild" in row["purpose"].lower() for row in automation):
        failures.append("automation must not implement blanket index rebuild")

    if not any(row["status"] == "requires Azure validation" for row in backup):
        failures.append("backup/restore readiness must retain Azure validation requirements")
    if not any(row["area"] == "DR" for row in hadr):
        failures.append("HA/DR readiness must include DR")
    if not any(row["requirement"].startswith("RTO 60") for row in hadr):
        failures.append("HA/DR readiness must trace RTO/RPO to architecture")
    if any(row["status"] == "implemented" for row in readiness):
        failures.append("operational readiness must not falsely mark Azure controls implemented")

    return failures

