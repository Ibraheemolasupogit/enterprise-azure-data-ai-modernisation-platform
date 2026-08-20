from __future__ import annotations

import csv
from pathlib import Path

REQUIRED_FILES = [
    "workload_catalog.csv",
    "performance_baseline.csv",
    "query_analysis.csv",
    "index_recommendations.csv",
    "statistics_strategy.csv",
    "blocking_scenarios.csv",
    "deadlock_readiness.csv",
    "parameter_sensitivity.csv",
    "performance_regression_controls.csv",
    "performance_assurance.csv",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def validate_outputs(outputs_dir: Path) -> list[str]:
    failures: list[str] = []
    for filename in REQUIRED_FILES:
        path = outputs_dir / filename
        if not path.is_file():
            failures.append(f"missing SQL performance output: {filename}")
        elif not read_csv(path):
            failures.append(f"empty SQL performance output: {filename}")
    if failures:
        return failures

    workloads = read_csv(outputs_dir / "workload_catalog.csv")
    baseline = read_csv(outputs_dir / "performance_baseline.csv")
    analysis = read_csv(outputs_dir / "query_analysis.csv")
    indexes = read_csv(outputs_dir / "index_recommendations.csv")
    stats = read_csv(outputs_dir / "statistics_strategy.csv")
    blocking = read_csv(outputs_dir / "blocking_scenarios.csv")
    deadlock = read_csv(outputs_dir / "deadlock_readiness.csv")
    psp = read_csv(outputs_dir / "parameter_sensitivity.csv")
    regression = read_csv(outputs_dir / "performance_regression_controls.csv")
    assurance = read_csv(outputs_dir / "performance_assurance.csv")

    required_workloads = {
        "customer_lookup",
        "shipment_create_update",
        "shipment_status_query",
        "route_depot_reporting",
        "incident_case_lookup",
        "analytical_delay_report",
    }
    workload_ids = {row["workload_id"] for row in workloads}
    if required_workloads - workload_ids:
        failures.append(f"workload catalog missing {sorted(required_workloads - workload_ids)}")

    baseline_ids = {row["workload_id"] for row in baseline}
    if workload_ids - baseline_ids:
        failures.append("every workload requires a baseline row")
    if any(row["metric_classification"] == "Azure measured" for row in baseline):
        failures.append("baseline must not claim Azure measured telemetry")

    if not any(row["analysis_type"] == "before/after scenario" for row in analysis):
        failures.append("query analysis must include before/after scenario")
    if not all(row["recommendation"] for row in analysis):
        failures.append("query analysis rows require recommendations")

    if not any("IX_Shipment_Route_Status_CreatedAt" in row["proposed_index"] for row in indexes):
        failures.append("index recommendations missing route/depot reporting scenario")
    if len(indexes) > 8:
        failures.append("index recommendations appear speculative/proliferated")
    if any("every column" in row["rationale"].lower() for row in indexes):
        failures.append("index strategy must not index every column")

    if not any("Avoids blanket FULLSCAN" in row["rationale"] for row in stats):
        failures.append("statistics strategy must avoid blanket FULLSCAN")
    if len(blocking) < 3:
        failures.append("blocking scenarios must cover at least three cases")
    if not any("error 1205" in row["recommendation"] for row in deadlock):
        failures.append("deadlock readiness must include retry guidance for error 1205")
    if not any("OPTION(RECOMPILE)" in row["recommendation"] for row in psp):
        failures.append("parameter sensitivity must include OPTION(RECOMPILE) trade-off")
    if not any("baseline -> change" in row["recommendation"] for row in regression):
        failures.append("regression workflow is missing lifecycle")

    assurance_areas = {row["area"] for row in assurance}
    for area in (
        "workload coverage",
        "baseline availability",
        "Query Store readiness",
        "index strategy",
        "statistics strategy",
        "blocking diagnostics",
        "deadlock diagnostics",
        "parameter sensitivity",
        "regression detection",
        "operational integration",
    ):
        if area not in assurance_areas:
            failures.append(f"performance assurance missing {area}")

    return failures

