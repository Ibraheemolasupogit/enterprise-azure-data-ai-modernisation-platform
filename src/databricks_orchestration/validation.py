from __future__ import annotations

import csv
from pathlib import Path

REQUIRED_FILES = [
    "data_quality_rules.csv",
    "quality_severity_matrix.csv",
    "quality_results.csv",
    "quarantine_catalog.csv",
    "job_catalog.csv",
    "task_dependency_matrix.csv",
    "schedule_matrix.csv",
    "retry_timeout_policy.csv",
    "failure_handling_matrix.csv",
    "backfill_strategy.csv",
    "job_permission_matrix.csv",
    "orchestration_traceability.csv",
    "orchestration_readiness.csv",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def validate_outputs(outputs_dir: Path, repo_root: Path | None = None) -> list[str]:
    failures: list[str] = []
    for filename in REQUIRED_FILES:
        path = outputs_dir / filename
        if not path.is_file():
            failures.append(f"missing Databricks orchestration output: {filename}")
        elif not read_csv(path):
            failures.append(f"empty Databricks orchestration output: {filename}")
    if failures:
        return failures

    rules = read_csv(outputs_dir / "data_quality_rules.csv")
    severity = read_csv(outputs_dir / "quality_severity_matrix.csv")
    results = read_csv(outputs_dir / "quality_results.csv")
    quarantine = read_csv(outputs_dir / "quarantine_catalog.csv")
    jobs = read_csv(outputs_dir / "job_catalog.csv")
    dependencies = read_csv(outputs_dir / "task_dependency_matrix.csv")
    schedules = read_csv(outputs_dir / "schedule_matrix.csv")
    retries = read_csv(outputs_dir / "retry_timeout_policy.csv")
    failures_matrix = read_csv(outputs_dir / "failure_handling_matrix.csv")
    backfill = read_csv(outputs_dir / "backfill_strategy.csv")
    permissions = read_csv(outputs_dir / "job_permission_matrix.csv")
    traceability = read_csv(outputs_dir / "orchestration_traceability.csv")
    readiness = read_csv(outputs_dir / "orchestration_readiness.csv")

    rule_categories = {row["rule_category"] for row in rules}
    for category in (
        "completeness",
        "validity",
        "uniqueness",
        "referential integrity",
        "consistency",
        "timeliness",
        "freshness",
        "schema conformity",
        "business rule",
    ):
        if category not in rule_categories:
            failures.append(f"missing quality rule category: {category}")
    if not all(row["severity"] and row["action_on_failure"] for row in rules):
        failures.append("every quality rule requires severity and action")
    if {"INFO", "WARNING", "ERROR", "CRITICAL"} - {row["severity"] for row in severity}:
        failures.append("severity matrix missing standard severities")
    if not any(int(row["quarantined_count"]) > 0 for row in results):
        failures.append("quality results must include fixture-derived quarantine counts")
    if not all(row["replay_eligibility"] for row in quarantine):
        failures.append("quarantine records require replay eligibility")
    if not all(row["purpose"] for row in jobs):
        failures.append("every job requires a purpose")
    if not any(row["downstream_publication_allowed"] == "no" for row in dependencies):
        failures.append("dependencies must block publication before gates")
    if not any(row["downstream_publication_allowed"] == "yes" for row in dependencies):
        failures.append("dependencies must allow publication after gates")
    if not all(row["rationale"] for row in schedules):
        failures.append("scheduled workflows require schedule rationale")
    if not retries:
        failures.append("retry policy is required")
    if not any("no blind retry" in row["action"].lower() for row in retries):
        failures.append("data-quality failures must not be blindly retried")
    if not failures_matrix:
        failures.append("failure handling matrix is required")
    if not backfill:
        failures.append("backfill strategy is required")
    if not any(row["role"] == "service principal" for row in permissions):
        failures.append("job permissions must include service principal")
    traced_jobs = {row["ingestion_task"].split(".")[0] for row in traceability}
    job_workflows = {row["workflow"].split("_workflow")[0] for row in jobs}
    if not traced_jobs & job_workflows:
        failures.append("traceability must map sources to job workflows")
    if any("executed" in row["response"].lower() for row in readiness):
        failures.append("readiness must not claim runtime execution")

    if repo_root is not None:
        for required_path in (
            "src/databricks/quality/expectations.py",
            "src/databricks/orchestration/job_entrypoints.py",
            "docs/databricks-data-quality-orchestration.md",
        ):
            if not (repo_root / required_path).is_file():
                failures.append(f"missing orchestration asset: {required_path}")

    return failures

