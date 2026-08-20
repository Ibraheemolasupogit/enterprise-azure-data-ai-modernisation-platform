# SQL MI Failed Agent Job

## Trigger

SQL Agent job failure alert.

## Triage

- Identify failed job, step, database, and error message.
- Confirm whether business operations are affected.
- Check recent deployments or configuration changes.

## Evidence

- Job history.
- Step output.
- SQL error.
- Related alerts.

## Action

- Rerun only if idempotent and approved.
- Fix configuration or permissions through controlled change.
- Escalate repeated failures to DBA owner.

## Escalation

Escalate integrity-check failures or evidence-job failures during cutover/hypercare.

## Validation

- Job completes successfully.
- Expected evidence is captured.

## Closure

Record failure cause, correction, and next scheduled run.

