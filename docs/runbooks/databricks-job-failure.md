# Databricks Job Failure

## Trigger

A Lakeflow Jobs task fails or retries repeatedly.

## Triage

Classify failure as transient platform, source, data-quality, schema, dependency, or code failure.

## Evidence

Collect task logs, job run metadata, dependency graph, quality results, source availability, and checkpoint status if relevant.

## Remediation

Retry transient failures within policy. Do not blindly retry deterministic data-quality failures.

## Validation

Confirm failed task and downstream gates pass after remediation.

## Escalation

Escalate repeated or production-impacting failures to platform lead.

## Closure

Record run id, failed task, cause, action, and validation.

