# SQL MI Slow Query Incident

## Trigger

User-reported slowness, long-running query alert, or Query Store regression signal.

## Triage

- Identify query text, plan, database, application workflow, and time window.
- Check whether the issue is isolated or platform-wide.
- Review recent deployments and data volume changes.

## Evidence

- Query Store runtime stats.
- DMV snapshot.
- Relevant execution plan in a real SQL MI environment.
- Baseline comparison.

## Action

- Prefer reversible mitigations.
- Avoid broad index changes without evidence.
- Route durable fixes through the performance backlog and later CI/CD controls.

## Escalation

Escalate if shipment creation/update or critical lookup workflows breach latency expectations.

## Validation

- Query returns to baseline or accepted threshold.
- No new regression appears.

## Closure

Document root cause, evidence, mitigation, and whether temporary hints/forcing must be removed.

