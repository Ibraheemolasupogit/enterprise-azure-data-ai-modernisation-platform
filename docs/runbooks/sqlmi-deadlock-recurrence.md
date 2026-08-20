# SQL MI Deadlock Recurrence

## Trigger

Repeated deadlock alert or recurring error 1205 from application logs.

## Triage

- Capture deadlock graph from Extended Events in a real environment.
- Identify resources, victim, lock order, and application workflow.
- Check recent deployment or query changes.

## Evidence

- Deadlock graph.
- Query text/procedure names.
- Transaction order.
- Retry behaviour.

## Action

- Apply consistent object access order where possible.
- Keep transactions short.
- Add targeted indexes only when evidence supports them.
- Ensure application retry uses jitter and idempotency.

## Escalation

Escalate if deadlocks affect shipment status updates or customer-facing workflows.

## Validation

- Deadlock recurrence stops or returns to accepted baseline.
- Retry success rate is acceptable.

## Closure

Document graph analysis, mitigation, and follow-up.

