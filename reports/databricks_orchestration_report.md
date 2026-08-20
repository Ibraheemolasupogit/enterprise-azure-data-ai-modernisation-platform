# Databricks Data Quality and Lakeflow Jobs Orchestration Report

Milestone 11 operationalises the Databricks medallion pipelines with formal data-quality rules, deterministic quality evidence, quarantine and replay handling, Lakeflow Jobs workflow definitions, task dependencies, schedules, retries, failure handling, backfill controls, permissions, and runbooks.

No Databricks job, Lakeflow Declarative Pipeline, expectation, stream, cluster, SQL warehouse, or production schedule was executed locally.

## Evidence Boundary

- Locally validated: quality-rule completeness, fixture-derived quality counts, quarantine routing, gate logic, retry classification, evidence generation, and tests.
- Configuration defined: Lakeflow Jobs bundle resources, task dependencies, schedules, permissions, timeout/retry policy, and runbooks.
- Simulated: deterministic fixture-derived quality results and freshness status.
- Requires Databricks runtime validation: actual job runs, task values, expectations, cluster/serverless behavior, schedule triggers, permissions enforcement, and pipeline event logs.

## Publication Gate

Gold publication is blocked when critical Bronze, Silver, or Gold quality gates fail. Data-quality failures are not blindly retried; they route to quarantine, manual review, or task failure depending on severity.
