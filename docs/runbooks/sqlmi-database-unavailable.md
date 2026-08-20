# SQL MI Database Unavailable

## Trigger

Database availability alert or application connection failure.

## Triage

- Confirm alert scope and affected database.
- Check Azure Resource Health and SQL MI status.
- Review recent deployment, failover, maintenance, and network events.
- Confirm whether application retry logic is active.

## Evidence

- Alert payload.
- Azure Activity events.
- Connectivity test result.
- Recent deployment record.

## Action

- Engage DBA and platform administrator.
- Validate private DNS/private endpoint path.
- If regional issue is suspected, move to DR runbook.

## Escalation

Escalate as Sev1 for critical transport OLTP impact.

## Validation

- Application reconnects.
- Critical workflow smoke checks pass.
- Error rate returns to expected baseline.

## Closure

Capture timeline, root cause, mitigation, and follow-up actions.

