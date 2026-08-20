# Databricks Quality-Gate Failure

## Trigger

A Bronze, Silver, or Gold quality gate returns `ERROR` or `CRITICAL`.

## Triage

Identify failed rule id, severity, affected dataset, rejected keys, and downstream dependencies.

## Evidence

Use `outputs/databricks_orchestration/data_quality_rules.csv`, quality results, quarantine catalog, and task logs.

## Remediation

Quarantine invalid records, fix source data or transformation logic, and avoid blind retries for deterministic data failures.

## Replay/Rerun

Revalidate remediated records, replay the affected batch/range, and rerun dependent tasks only after the gate passes.

## Validation

Confirm critical failures are zero before Gold publication.

## Escalation

Escalate to dataset owner for repeated or business-rule failures.

## Closure

Close quarantine evidence and document the accepted disposition.

