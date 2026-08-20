# SQL MI Blocking or Deadlock Incident

## Trigger

Deadlock alert, blocking alert, or application timeout pattern.

## Triage

- Identify database, session, login, query hash, and blocking chain.
- Check recent deployment or workload spike.
- Review deadlock graph where available.

## Evidence

- KQL result.
- Blocking session details.
- Query text or procedure name.
- Application impact.

## Action

- Resolve immediate blocker if approved.
- Capture evidence before killing sessions.
- Route tuning candidates to the SQL performance milestone backlog.

## Escalation

Escalate if shipment creation/status workflows are impaired.

## Validation

- Blocking clears.
- Error rate returns to expected level.
- No repeated deadlock pattern remains.

## Closure

Log incident and performance follow-up.

