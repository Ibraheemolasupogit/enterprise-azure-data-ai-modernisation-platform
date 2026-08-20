from __future__ import annotations

# ruff: noqa: E501
import argparse
import csv
from dataclasses import asdict
from pathlib import Path
from typing import Any

from databricks_operations.catalog import (
    ALERTS,
    CLUSTER_POLICIES,
    COMPUTE_OPTIMIZATION,
    COST_ALLOCATION,
    COST_CONTROLS,
    DELTA_HEALTH,
    JOB_HEALTH,
    JOIN_OPTIMIZATION,
    MONITORING,
    PIPELINE_OBSERVABILITY,
    READINESS,
    SLOS,
    SPARK_TROUBLESHOOTING,
    SQL_WAREHOUSE,
    STREAMING_HEALTH,
)
from databricks_operations.validation import validate_outputs

OUTPUTS = {
    "monitoring_catalog.csv": MONITORING,
    "job_health_rules.csv": JOB_HEALTH,
    "pipeline_observability.csv": PIPELINE_OBSERVABILITY,
    "spark_troubleshooting_matrix.csv": SPARK_TROUBLESHOOTING,
    "join_optimization_matrix.csv": JOIN_OPTIMIZATION,
    "delta_table_health.csv": DELTA_HEALTH,
    "streaming_health_rules.csv": STREAMING_HEALTH,
    "compute_optimization_matrix.csv": COMPUTE_OPTIMIZATION,
    "cluster_policy_catalog.csv": CLUSTER_POLICIES,
    "sql_warehouse_operations.csv": SQL_WAREHOUSE,
    "cost_allocation_model.csv": COST_ALLOCATION,
    "cost_optimization_controls.csv": COST_CONTROLS,
    "alert_catalog.csv": ALERTS,
    "operational_slo_matrix.csv": SLOS,
    "operations_readiness.csv": READINESS,
}


def generate_outputs(
    outputs_dir: Path,
    reports_dir: Path,
    repo_root: Path | None = None,
) -> dict[str, Path]:
    outputs_dir.mkdir(parents=True, exist_ok=True)
    reports_dir.mkdir(parents=True, exist_ok=True)
    written: dict[str, Path] = {}
    for filename, rows in OUTPUTS.items():
        path = outputs_dir / filename
        _write_csv(path, [asdict(row) for row in rows])
        written[filename] = path
    report = reports_dir / "databricks_operations_report.md"
    report.write_text(_report(), encoding="utf-8")
    written["databricks_operations_report.md"] = report
    failures = validate_outputs(outputs_dir, repo_root or Path.cwd())
    if failures:
        joined = "\n".join(f"- {failure}" for failure in failures)
        raise RuntimeError(f"Databricks operations validation failed:\n{joined}")
    return written


def _write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def _report() -> str:
    return "\n".join(
        [
            "# Databricks Monitoring, Troubleshooting, Performance and Cost Optimization Report",
            "",
            "Milestone 12 defines the Databricks operational excellence layer for Contoso Freight. It covers monitoring architecture, system-table query assets, job and pipeline observability, Spark troubleshooting, Delta table health, streaming health, compute and SQL warehouse optimization, cost attribution, alerting, SLO assumptions, runbooks, and deterministic readiness evidence.",
            "",
            "No Databricks runtime telemetry, system-table results, Spark UI evidence, billing totals, OPTIMIZE, VACUUM, predictive optimization, SQL warehouse measurement, or stream progress output was executed or fabricated locally.",
            "",
            "## Boundary",
            "",
            "- Locally validated: catalog consistency, alert/runbook traceability, SLO/monitoring coverage, deterministic evidence and tests.",
            "- Configuration defined: query assets, runbooks, controls, policies, alerts and optimization guidance.",
            "- Simulated: architecture-assumption SLO/freshness thresholds where no customer SLA exists.",
            "- Requires Databricks validation: system tables, billing usage, Spark UI/runtime metrics, streaming progress, query history, warehouse events, and predictive optimization.",
            "",
        ]
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate Databricks operations evidence.")
    parser.add_argument("--outputs-dir", type=Path, default=Path("outputs/databricks_operations"))
    parser.add_argument("--reports-dir", type=Path, default=Path("reports"))
    args = parser.parse_args()
    written = generate_outputs(args.outputs_dir, args.reports_dir, Path.cwd())
    for name in sorted(written):
        print(f"{name}: {written[name]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

