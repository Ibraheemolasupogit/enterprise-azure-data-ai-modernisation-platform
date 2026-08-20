# Databricks Failed Optimization

## Trigger

An `OPTIMIZE`, clustering, predictive optimization review, or maintenance task fails or worsens runtime/cost.

## Triage

Identify table, maintenance operation, table size, file count, retention, workload impact, and concurrent readers/writers.

## Evidence

Use Delta history, table details, job logs, query history, and cost attribution.

## Remediation

Stop broad maintenance. Revert to previous table version where appropriate, or tune operation scope and schedule.

## Validation

Confirm reads, writes, and downstream freshness recover.

## Escalation

Escalate retention/recovery risk to governance and platform owners.

## Closure

Record table, operation, impact, decision, and validation.

