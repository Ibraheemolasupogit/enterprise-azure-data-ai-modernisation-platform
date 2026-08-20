# Databricks Quarantined Record Remediation

## Trigger

Records accumulate in quarantine or a data owner requests replay.

## Triage

Group records by source dataset, rule id, failure reason, and replay eligibility.

## Evidence

Use quarantine catalog, raw payload policy, source metadata, and failed quality rule.

## Remediation

Correct source data, approve acceptable reference repair, or update transformation logic through pull request.

## Replay/Rerun

Revalidate remediated records and replay through the controlled replay workflow.

## Validation

Confirm records leave open quarantine status and downstream quality gates pass.

## Escalation

Escalate sensitive or repeated failures to governance and source owner.

## Closure

Close evidence with remediation status, replay run id, and validation result.

