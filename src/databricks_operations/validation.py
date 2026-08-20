from __future__ import annotations

import csv
from pathlib import Path

REQUIRED_FILES = [
    "monitoring_catalog.csv",
    "job_health_rules.csv",
    "pipeline_observability.csv",
    "spark_troubleshooting_matrix.csv",
    "join_optimization_matrix.csv",
    "delta_table_health.csv",
    "streaming_health_rules.csv",
    "compute_optimization_matrix.csv",
    "cluster_policy_catalog.csv",
    "sql_warehouse_operations.csv",
    "cost_allocation_model.csv",
    "cost_optimization_controls.csv",
    "alert_catalog.csv",
    "operational_slo_matrix.csv",
    "operations_readiness.csv",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def validate_outputs(outputs_dir: Path, repo_root: Path | None = None) -> list[str]:
    failures: list[str] = []
    for filename in REQUIRED_FILES:
        path = outputs_dir / filename
        if not path.is_file():
            failures.append(f"missing Databricks operations output: {filename}")
        elif not read_csv(path):
            failures.append(f"empty Databricks operations output: {filename}")
    if failures:
        return failures

    monitoring = read_csv(outputs_dir / "monitoring_catalog.csv")
    job_health = read_csv(outputs_dir / "job_health_rules.csv")
    pipeline = read_csv(outputs_dir / "pipeline_observability.csv")
    spark = read_csv(outputs_dir / "spark_troubleshooting_matrix.csv")
    delta = read_csv(outputs_dir / "delta_table_health.csv")
    streaming = read_csv(outputs_dir / "streaming_health_rules.csv")
    compute = read_csv(outputs_dir / "compute_optimization_matrix.csv")
    policies = read_csv(outputs_dir / "cluster_policy_catalog.csv")
    warehouse = read_csv(outputs_dir / "sql_warehouse_operations.csv")
    cost = read_csv(outputs_dir / "cost_allocation_model.csv")
    controls = read_csv(outputs_dir / "cost_optimization_controls.csv")
    alerts = read_csv(outputs_dir / "alert_catalog.csv")
    slos = read_csv(outputs_dir / "operational_slo_matrix.csv")
    readiness = read_csv(outputs_dir / "operations_readiness.csv")

    monitored_workloads = {row["workload"] for row in monitoring}
    for required in ("batch feeds", "relational increments", "shipment events", "Gold publication"):
        if required not in monitored_workloads:
            failures.append(f"critical workload missing monitoring: {required}")
    if not all(row["runbook"] for row in alerts):
        failures.append("every alert must map to a runbook")
    if not any("Gold freshness" in row["signal"] for row in monitoring):
        failures.append("critical Gold products require freshness monitoring")
    if not streaming:
        failures.append("streaming workload requires health rules")
    if not {"jobs compute", "serverless jobs or jobs compute", "SQL warehouse"} <= {
        row["area"] for row in compute
    }:
        failures.append("each compute class requires optimization guidance")
    if not all(row["required_tag_or_source"] for row in cost):
        failures.append("production workloads require cost attribution")
    if any(
        row["evidence_classification"] == "locally validated"
        and row["monitoring_source"]
        in {
            "system.compute and Spark UI/runtime metrics",
            "system.billing usage and list prices",
        }
        for row in monitoring
    ):
        failures.append("runtime-only monitoring must not be locally validated")
    if any("£" in str(row) or "$" in str(row) for row in cost + controls):
        failures.append("cost model must not fabricate currency values")
    if not any("checkpoint" in row["condition"] for row in alerts):
        failures.append("checkpoint issue alert is required")
    if not any("VACUUM" in row["recommendation"] for row in delta):
        failures.append("Delta health must cover VACUUM/retention")
    if not any(row["control"] == "tags" for row in policies):
        failures.append("cluster policies must require tags")
    if not warehouse:
        failures.append("SQL warehouse operations are required")
    if not slos:
        failures.append("SLO matrix is required")
    if any(row["evidence_classification"] == "blocked" for row in readiness):
        failures.append("readiness should not be blocked")
    if not spark:
        failures.append("Spark troubleshooting matrix is required")
    if not pipeline:
        failures.append("pipeline observability mapping is required")
    if not job_health:
        failures.append("job health rules are required")

    if repo_root is not None:
        for required_path in (
            "src/databricks/operations/sql/system_table_monitoring.sql",
            "src/databricks/operations/policies/cluster_policy_examples.json",
            "docs/databricks-monitoring-optimization.md",
        ):
            if not (repo_root / required_path).is_file():
                failures.append(f"missing Databricks operations asset: {required_path}")

    return failures
