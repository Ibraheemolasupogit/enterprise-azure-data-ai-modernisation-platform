# Databricks Monitoring, Troubleshooting, Performance and Cost Optimization

Milestone 12 defines the operational excellence layer for the Databricks plane. It does not execute Databricks workloads, query system tables, collect Spark UI evidence, produce billing totals, run `OPTIMIZE` or `VACUUM`, enable predictive optimization, or claim production SLOs.

## Monitoring Architecture

The monitoring model covers Lakeflow Jobs, tasks, jobs compute, serverless compute, SQL warehouses, Structured Streaming, Delta tables, Unity Catalog, quality gates, storage, audit/security events, and cost/utilization.

Intended production sources include Databricks system tables, job run metadata, pipeline event logs, Spark UI/runtime metrics, Structured Streaming progress, Unity Catalog metadata, query history, billing/usage tables, and Azure Monitor or Log Analytics integration where configured.

## System Tables

Query assets in `src/databricks/operations/sql/` cover failed jobs, long-running jobs, expensive workloads, compute events, SQL query latency, user/service-principal activity, cost attribution, lineage, and audit investigation. These are Databricks-ready assets only.

## Job and Pipeline Observability

Each pipeline stage exposes status, counts, rejected/quarantined counts, freshness, latency, previous-success time, and checkpoint state where relevant. Gold publication depends on quality and freshness signals from upstream Bronze/Silver/Gold gates.

## Spark Troubleshooting

The Spark troubleshooting matrix maps slow stages, skew, shuffle pressure, spill, partition imbalance, excessive tasks, driver bottlenecks, inefficient joins, repeated scans, unnecessary caching, and Python UDF overhead to evidence and safe remediation.

Remediation is evidence-led: inspect Spark UI, query plans, task distribution, spill metrics, and runtime logs before changing layout or compute.

## Delta Optimization

Delta health checks cover file count, average file size, table size, stale data, deleted-file retention, clustering, schema changes, CDF state, table properties, and transaction-log growth.

`OPTIMIZE`, liquid clustering, predictive optimization, and `VACUUM` are runtime activities. They should be used after evidence, not as blanket maintenance. Retention must respect time travel, long-running readers, streaming checkpoints, compliance deletion, and recovery requirements.

## Streaming Health

Shipment-event streaming health monitors input rate, processing rate, batch duration, watermark progress, state size, lag, checkpoint age, late records, duplicate handling, failed micro-batches, and stalled stream behavior.

Production checkpoint deletion is dangerous and is never the default recovery action. Preserve checkpoint evidence, replay into isolated paths where needed, and merge idempotently.

## Compute and SQL Warehouse Operations

Compute optimization separates performance and cost. Jobs compute, serverless jobs, SQL warehouses, and backfill job clusters have different scaling and cost profiles. Production avoids all-purpose interactive clusters for scheduled jobs.

SQL warehouse operations focus on sizing, serverless/pro choice, auto-stop, concurrency, queue time, query duration, cache behavior, Photon, and query history.

## FinOps

Cost attribution uses environment, workspace, workload, job, pipeline, compute type, SQL warehouse, user/service principal, domain, and tag dimensions. Billing and usage system tables are the intended production source. This milestone defines tags and controls but does not fabricate currency values or budgets.

## Root-Cause Workflow

Alert -> scope affected workload -> review dependency graph -> inspect run history -> inspect quality/freshness -> inspect Spark/SQL metrics -> identify probable cause -> apply safe remediation -> rerun/replay if appropriate -> validate downstream freshness -> close evidence.

## Local Boundary

Local validation checks catalog consistency, alert/runbook traceability, SLO/monitoring coverage, cost attribution, and readiness evidence. Runtime validation remains required for actual telemetry and operational behavior.

