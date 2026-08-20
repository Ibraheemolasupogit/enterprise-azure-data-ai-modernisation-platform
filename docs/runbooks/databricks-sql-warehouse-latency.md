# Databricks SQL Warehouse Latency

## Trigger

Queued queries, long-running SQL, or user-facing Gold query latency breaches assumptions.

## Triage

Review query history, warehouse size, queue time, concurrency, cache behavior, and scanned bytes/rows.

## Evidence

Use `system.query.history`, warehouse events, query profile, and Gold freshness evidence.

## Remediation

Tune filters, joins, aggregation grain, table layout, warehouse size, and auto-stop/concurrency settings based on evidence.

## Validation

Confirm query latency and queue time improve without unjustified cost increase.

## Escalation

Escalate repeated latency to analytics platform owner.

## Closure

Record query ids, evidence, change, and cost/performance trade-off.

