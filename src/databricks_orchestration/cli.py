from __future__ import annotations

# ruff: noqa: E501
import argparse
import csv
from dataclasses import asdict
from pathlib import Path
from typing import Any

from databricks_orchestration.catalog import (
    BACKFILL,
    DEPENDENCIES,
    FAILURES,
    JOBS,
    PERMISSIONS,
    QUALITY_RULES,
    QUARANTINE,
    READINESS,
    RETRIES,
    SCHEDULES,
    SEVERITY,
    TRACEABILITY,
    quality_results,
)
from databricks_orchestration.validation import validate_outputs

OUTPUTS = {
    "data_quality_rules.csv": QUALITY_RULES,
    "quality_severity_matrix.csv": SEVERITY,
    "quality_results.csv": quality_results(),
    "quarantine_catalog.csv": QUARANTINE,
    "job_catalog.csv": JOBS,
    "task_dependency_matrix.csv": DEPENDENCIES,
    "schedule_matrix.csv": SCHEDULES,
    "retry_timeout_policy.csv": RETRIES,
    "failure_handling_matrix.csv": FAILURES,
    "backfill_strategy.csv": BACKFILL,
    "job_permission_matrix.csv": PERMISSIONS,
    "orchestration_traceability.csv": TRACEABILITY,
    "orchestration_readiness.csv": READINESS,
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
    report = reports_dir / "databricks_orchestration_report.md"
    report.write_text(_report(), encoding="utf-8")
    written["databricks_orchestration_report.md"] = report
    failures = validate_outputs(outputs_dir, repo_root or Path.cwd())
    if failures:
        joined = "\n".join(f"- {failure}" for failure in failures)
        raise RuntimeError(f"Databricks orchestration validation failed:\n{joined}")
    return written


def _write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def _report() -> str:
    return "\n".join(
        [
            "# Databricks Data Quality and Lakeflow Jobs Orchestration Report",
            "",
            "Milestone 11 operationalises the Databricks medallion pipelines with formal data-quality rules, deterministic quality evidence, quarantine and replay handling, Lakeflow Jobs workflow definitions, task dependencies, schedules, retries, failure handling, backfill controls, permissions, and runbooks.",
            "",
            "No Databricks job, Lakeflow Declarative Pipeline, expectation, stream, cluster, SQL warehouse, or production schedule was executed locally.",
            "",
            "## Evidence Boundary",
            "",
            "- Locally validated: quality-rule completeness, fixture-derived quality counts, quarantine routing, gate logic, retry classification, evidence generation, and tests.",
            "- Configuration defined: Lakeflow Jobs bundle resources, task dependencies, schedules, permissions, timeout/retry policy, and runbooks.",
            "- Simulated: deterministic fixture-derived quality results and freshness status.",
            "- Requires Databricks runtime validation: actual job runs, task values, expectations, cluster/serverless behavior, schedule triggers, permissions enforcement, and pipeline event logs.",
            "",
            "## Publication Gate",
            "",
            "Gold publication is blocked when critical Bronze, Silver, or Gold quality gates fail. Data-quality failures are not blindly retried; they route to quarantine, manual review, or task failure depending on severity.",
            "",
        ]
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate Databricks orchestration evidence.")
    parser.add_argument("--outputs-dir", type=Path, default=Path("outputs/databricks_orchestration"))
    parser.add_argument("--reports-dir", type=Path, default=Path("reports"))
    args = parser.parse_args()
    written = generate_outputs(args.outputs_dir, args.reports_dir, Path.cwd())
    for name in sorted(written):
        print(f"{name}: {written[name]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

