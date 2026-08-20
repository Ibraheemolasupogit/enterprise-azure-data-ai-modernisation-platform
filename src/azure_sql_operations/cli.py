from __future__ import annotations

# ruff: noqa: E501
import argparse
import csv
from dataclasses import asdict
from pathlib import Path
from typing import Any

from azure_sql_operations.catalog import (
    ALERT_CATALOG,
    AUTOMATION_CATALOG,
    BACKUP_RESTORE_READINESS,
    CONFIGURATION_BASELINE,
    HA_DR_READINESS,
    MONITORING_CATALOG,
    OPERATIONAL_READINESS,
    SECURITY_ROLES,
    SENSITIVE_CONTROLS,
)
from azure_sql_operations.validation import validate_outputs

OUTPUTS = {
    "configuration_baseline.csv": CONFIGURATION_BASELINE,
    "security_role_matrix.csv": SECURITY_ROLES,
    "sensitive_data_controls.csv": SENSITIVE_CONTROLS,
    "monitoring_catalog.csv": MONITORING_CATALOG,
    "alert_catalog.csv": ALERT_CATALOG,
    "automation_catalog.csv": AUTOMATION_CATALOG,
    "backup_restore_readiness.csv": BACKUP_RESTORE_READINESS,
    "ha_dr_readiness.csv": HA_DR_READINESS,
    "operational_readiness.csv": OPERATIONAL_READINESS,
}


def generate_outputs(outputs_dir: Path, reports_dir: Path) -> dict[str, Path]:
    outputs_dir.mkdir(parents=True, exist_ok=True)
    reports_dir.mkdir(parents=True, exist_ok=True)
    written: dict[str, Path] = {}
    for filename, rows in OUTPUTS.items():
        path = outputs_dir / filename
        _write_csv(path, [asdict(row) for row in rows])
        written[filename] = path
    report = reports_dir / "azure_sql_operations_report.md"
    report.write_text(_report(), encoding="utf-8")
    written["azure_sql_operations_report.md"] = report
    failures = validate_outputs(outputs_dir)
    if failures:
        joined = "\n".join(f"- {failure}" for failure in failures)
        raise RuntimeError(f"Azure SQL operations validation failed:\n{joined}")
    return written


def _write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def _report() -> str:
    return "\n".join(
        [
            "# Azure SQL Operations Report",
            "",
            "Milestone 6 defines the Azure SQL Managed Instance operational control layer for `legacy_tms`. It does not deploy Azure resources, execute backups, perform restore, trigger failover, or tune workload performance.",
            "",
            "## Configuration Baseline",
            "",
            "- Target service remains Azure SQL Managed Instance.",
            "- Service tier, vCores, storage, collation, zone redundancy, and long-term retention require live validation.",
            "- Production posture disables public endpoint, requires private connectivity, TLS 1.2+, Entra-first authentication, diagnostic settings, and auditing.",
            "",
            "## Security Model",
            "",
            "- Synthetic Entra group and managed identity placeholders are used.",
            "- Permissions are role based: DBA, deployment, application executor, automation executor, analyst, auditor, and platform administrator.",
            "- Sensitive controls map to actual target schema assets such as `CustomerAccount.ContactEmail`, `LegalName`, `DeclaredValueGbp`, and regional shipment visibility.",
            "",
            "## Recovery and HA/DR",
            "",
            "- Automated Azure backups, PITR, restore drill evidence, and LTR decisions are modelled but require Azure validation.",
            "- SQL MI built-in HA and possible failover groups are represented as readiness controls.",
            "- Planned failover, unplanned regional outage, application reconnection, data-loss window, and failback are documented as planned tests.",
            "",
            "## Monitoring, Alerts, and Automation",
            "",
            "- Monitoring catalog covers CPU, storage, sessions, failed logins, deadlocks, blocking, availability, backup/recovery, failover, and long-running queries.",
            "- Alerts map to operational runbooks.",
            "- SQL Agent jobs cover integrity checks, statistics maintenance, operational evidence, and retention cleanup without implementing blanket index rebuilds.",
            "",
            "## Validation Boundary",
            "",
            "- Locally validated: generated matrices, T-SQL/KQL/runbook presence, role/control/alert mappings.",
            "- Configuration defined: Bicep, SQL security patterns, SQL Agent job definitions, monitoring catalog.",
            "- Requires Azure validation: deployment, diagnostics flow, backups, restore, failover, zone redundancy, actual sizing, and alert firing.",
            "",
        ]
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate Azure SQL operations evidence.")
    parser.add_argument("--outputs-dir", type=Path, default=Path("outputs/azure_sql_operations"))
    parser.add_argument("--reports-dir", type=Path, default=Path("reports"))
    args = parser.parse_args()
    written = generate_outputs(args.outputs_dir, args.reports_dir)
    for name in sorted(written):
        print(f"{name}: {written[name]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

