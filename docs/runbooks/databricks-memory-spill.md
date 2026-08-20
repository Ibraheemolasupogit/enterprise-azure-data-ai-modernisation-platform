# Databricks Memory and Spill Issue

## Trigger

Executor memory pressure, high spill, GC pressure, or failed tasks due to memory.

## Triage

Review data volume, join strategy, aggregation width, cache/persist use, and worker sizing.

## Evidence

Collect Spark UI spill metrics, executor logs, query plan, task failures, and input size.

## Remediation

Reduce shuffle width, prune columns, avoid unnecessary cache, tune joins, or right-size workers after evidence.

## Validation

Confirm spill and failure rate reduce without excessive cost.

## Escalation

Escalate if source volume change requires model or schedule adjustment.

## Closure

Document performance and cost trade-off.

