# Databricks Repeated Task Failure

## Trigger

A task fails after configured retries or repeatedly fails across runs.

## Triage

Classify failure as transient, data-quality, schema, dependency, or code/logical failure.

## Evidence

Collect retry policy, task logs, dependency graph, recent code changes, and quality results.

## Remediation

Apply bounded retry for transient failures only. For deterministic failures, fix data, schema, or code.

## Replay/Rerun

Rerun the smallest safe task branch after remediation. Rerun full workflow only when dependencies require it.

## Validation

Confirm affected gates pass and downstream publication state is correct.

## Escalation

Escalate repeated logical/code failures to data engineering owner.

## Closure

Record root cause, fix, rerun id, and prevention action.

