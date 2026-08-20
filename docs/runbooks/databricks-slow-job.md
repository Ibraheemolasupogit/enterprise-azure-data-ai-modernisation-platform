# Databricks Slow Job

## Trigger

A job exceeds expected runtime or start delay assumptions.

## Triage

Scope workflow, task, data range, recent code/config changes, and upstream dependency status.

## Evidence

Collect job run metadata, task duration, queue time, Spark UI stages, query plan, record counts, and quality/freshness status.

## Remediation

Filter early, reduce scanned columns, inspect joins, review partition/file layout, and right-size compute only after evidence.

## Validation

Rerun the affected task or workflow and confirm freshness and downstream gates.

## Escalation

Escalate repeated slowdowns to platform operator and data engineering owner.

## Closure

Record probable cause, evidence, remediation, and follow-up optimization.

