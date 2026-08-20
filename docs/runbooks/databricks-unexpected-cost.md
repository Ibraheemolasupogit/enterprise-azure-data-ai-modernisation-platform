# Databricks Unexpected Cost Increase

## Trigger

Usage or cost attribution shows unusual workload, job, environment, or interactive compute growth.

## Triage

Identify workspace, job, compute type, user/service principal, tags, schedule changes, retries, and data volume changes.

## Evidence

Use billing/usage system tables, job history, compute events, schedules, and tag attribution.

## Remediation

Stop idle compute, right-size jobs, reduce excessive retries, review schedule frequency, compact small files only when justified, and remove unused workloads.

## Validation

Confirm usage trend returns within architecture assumption without breaking freshness.

## Escalation

Escalate unexplained production usage to FinOps owner and platform lead.

## Closure

Record usage driver, owner, control applied, and residual risk.

