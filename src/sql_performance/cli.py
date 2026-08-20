from __future__ import annotations

# ruff: noqa: E501
import argparse
import csv
from dataclasses import asdict
from pathlib import Path
from typing import Any

from sql_performance.catalog import (
    BASELINE,
    BLOCKING_SCENARIOS,
    DEADLOCK_READINESS,
    INDEX_RECOMMENDATIONS,
    PARAMETER_SENSITIVITY,
    PERFORMANCE_ASSURANCE,
    QUERY_ANALYSIS,
    REGRESSION_CONTROLS,
    STATISTICS_STRATEGY,
    WORKLOADS,
)
from sql_performance.validation import validate_outputs

OUTPUTS = {
    "workload_catalog.csv": WORKLOADS,
    "performance_baseline.csv": BASELINE,
    "query_analysis.csv": QUERY_ANALYSIS,
    "index_recommendations.csv": INDEX_RECOMMENDATIONS,
    "statistics_strategy.csv": STATISTICS_STRATEGY,
    "blocking_scenarios.csv": BLOCKING_SCENARIOS,
    "deadlock_readiness.csv": DEADLOCK_READINESS,
    "parameter_sensitivity.csv": PARAMETER_SENSITIVITY,
    "performance_regression_controls.csv": REGRESSION_CONTROLS,
    "performance_assurance.csv": PERFORMANCE_ASSURANCE,
}


def generate_outputs(outputs_dir: Path, reports_dir: Path) -> dict[str, Path]:
    outputs_dir.mkdir(parents=True, exist_ok=True)
    reports_dir.mkdir(parents=True, exist_ok=True)
    written: dict[str, Path] = {}
    for filename, rows in OUTPUTS.items():
        path = outputs_dir / filename
        _write_csv(path, [asdict(row) for row in rows])
        written[filename] = path
    report = reports_dir / "sql_performance_report.md"
    report.write_text(_report(), encoding="utf-8")
    written["sql_performance_report.md"] = report
    failures = validate_outputs(outputs_dir)
    if failures:
        joined = "\n".join(f"- {failure}" for failure in failures)
        raise RuntimeError(f"SQL performance validation failed:\n{joined}")
    return written


def _write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def _report() -> str:
    return "\n".join(
        [
            "# SQL Performance Engineering Report",
            "",
            "Milestone 7 defines a reproducible SQL performance-engineering capability for `legacy_tms` on Azure SQL Managed Instance. It does not execute SQL MI workloads, collect Azure telemetry, fabricate execution-plan XML, or implement SQL CI/CD.",
            "",
            "## Evidence Boundary",
            "",
            "- Locally executable: T-SQL diagnostic scripts and deterministic evidence generation.",
            "- Static analysis: query-shape, index, statistics, blocking, and Query Store readiness models.",
            "- Simulated: baseline metrics, blocking/deadlock scenarios, parameter-sensitive plan scenario.",
            "- Requires Azure/SQL MI validation: real Query Store runtime stats, actual execution plans, waits, memory grants, spills, index usage, and alert correlation.",
            "",
            "## Workloads",
            "",
            "Six workloads are catalogued: customer lookup, shipment create/update, shipment status query, route/depot reporting, incident/case lookup, and analytical delay reporting.",
            "",
            "## Index Engineering",
            "",
            "The focused before/after scenario remains route/depot operational reporting. The target schema includes `IX_Shipment_Route_Status_CreatedAt`; additional indexes are candidates only when Query Store and index usage evidence justify them.",
            "",
            "## Statistics",
            "",
            "The strategy keeps automatic statistics enabled, detects stale statistics, uses targeted updates, and avoids blanket FULLSCAN or blanket index rebuilds.",
            "",
            "## Blocking and Deadlocks",
            "",
            "DMV scripts and simulated scenarios cover head blockers, blocking chains, sleeping open transactions, writer/writer contention, Extended Events deadlock capture, and application retry guidance for error 1205.",
            "",
            "## Regression Workflow",
            "",
            "Baseline -> change/deployment -> detect regression -> identify query -> compare plans -> apply safe mitigation -> validate -> document evidence -> remove temporary mitigation where appropriate.",
            "",
        ]
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate SQL performance evidence.")
    parser.add_argument("--outputs-dir", type=Path, default=Path("outputs/sql_performance"))
    parser.add_argument("--reports-dir", type=Path, default=Path("reports"))
    args = parser.parse_args()
    written = generate_outputs(args.outputs_dir, args.reports_dir)
    for name in sorted(written):
        print(f"{name}: {written[name]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

