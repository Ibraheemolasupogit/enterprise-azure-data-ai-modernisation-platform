# Databricks Data Quality and Lakeflow Jobs Orchestration

Milestone 11 operationalises the Milestone 10 medallion pipelines. It adds formal data-quality rules, quality evidence, quarantine and replay handling, Lakeflow Jobs workflow definitions, task dependencies, schedules, retries, timeout policy, backfill controls, permissions, and runbooks.

No Databricks job, stream, expectation, cluster, SQL warehouse, or schedule is executed locally.

## Data-Quality Framework

Rules are machine-readable and include dataset, layer, rule id, category, fields, expectation, severity, action on failure, owner role, and evidence classification.

Rule categories cover completeness, validity, uniqueness, referential integrity, consistency, timeliness, freshness, schema conformity, and business rules.

Severity behavior:

- `INFO`: log only.
- `WARNING`: log and quarantine where relevant.
- `ERROR`: reject record, quarantine, or fail the affected task.
- `CRITICAL`: fail the task and stop downstream dependencies.

Deterministic quality results are fixture-derived. They do not claim Databricks expectation execution.

## Expectations

`src/databricks/quality/expectations.py` maps important controls to Databricks-ready expectation patterns equivalent to warn, drop, and fail behavior. These are configuration-defined assets until validated in a Databricks runtime.

## Quarantine and Replay

Quarantine records retain target table, source dataset, rule id, rejected key, source metadata, failure reason, detected timestamp, raw payload policy, remediation status, and replay eligibility.

Replay flow:

1. Quarantine captures the failed record and evidence.
2. Owner corrects or approves remediation.
3. Record is revalidated.
4. Record is reprocessed through the relevant Bronze/Silver/Gold path.
5. Evidence is closed without deleting the original quarantine trail.

Invalid records must not be silently discarded.

## Lakeflow Jobs Architecture

The bundle defines separate workflows for:

- Batch feeds.
- Relational incremental ingestion.
- Event streaming.
- Gold publication.
- Controlled backfill and replay.

Gold publication depends on validated Silver and Gold quality gates. Critical quality failures block publication.

## Parameters

Jobs are parameterized by environment, catalog, source system, processing date, load type, checkpoint path, schema, and replay mode. Production-specific identifiers remain environment configuration, not committed credentials.

## Schedules

Batch feeds run daily based on file arrival assumptions. Relational increments run during the operating window. Gold refresh runs after Silver gates or hourly. Event streaming is continuous and checkpoint-driven rather than batch scheduled. Backfill/replay is manual only.

## Retries and Timeouts

Transient platform/source failures have bounded retries. Deterministic data-quality failures do not get blind retries; they route to quarantine, fail the affected branch, or require manual review. Streaming failures restart from checkpoint with escalation for repeated failure.

## Backfill

Backfills require source range, target range, processing mode, validation gates, expected volume, isolation from current processing, reconciliation, and rollback. Streaming checkpoints must not be overwritten casually; replay uses isolated paths and reviewed merge.

## Permissions

Production runtime ownership is intended for a service principal. Operators can manage runs, data engineers can manage dev/test, governance can view evidence, and analysts remain viewers. Source code stays in Git.

## Local Boundary

Local validation covers rule completeness, deterministic quality evidence, quarantine routing, severity/action mapping, gate logic, dependency graph, retry classification, backfill controls, permissions, traceability, and evidence generation. Runtime validation remains required for Lakeflow Jobs execution, task values, permissions, expectations, cluster/serverless behavior, schedules, and operational logs.

