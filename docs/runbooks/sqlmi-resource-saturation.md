# SQL MI Resource Saturation

## Trigger

High CPU, worker/session pressure, or sustained resource saturation alert.

## Triage

- Confirm duration, affected database, and workload window.
- Check current sessions, waits, blocking, and recent deployments.
- Review whether migration, maintenance, or reporting activity is active.

## Evidence

- Azure Monitor metric trend.
- KQL resource-health query output.
- Active workload summary.
- Recent change record.

## Action

- Mitigate immediate operational impact.
- Pause non-critical jobs if approved.
- Route query/index tuning candidates to the SQL performance milestone.
- Do not apply broad index rebuilds or unreviewed query changes.

## Escalation

Escalate if transport shipment workflows degrade or saturation persists past the evaluation window.

## Validation

- CPU/session/worker pressure returns to expected range.
- Critical workflows pass smoke checks.
- No related alerts remain active.

## Closure

Record cause, mitigation, and performance backlog item if needed.

