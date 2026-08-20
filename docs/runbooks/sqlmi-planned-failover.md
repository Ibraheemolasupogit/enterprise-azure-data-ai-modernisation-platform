# SQL MI Planned Failover

## Trigger

Approved DR test or planned maintenance requiring failover validation.

## Triage

- Confirm failover group and secondary readiness in Azure.
- Confirm application retry and connection behaviour.
- Confirm rollback/failback plan.

## Evidence

- Approval record.
- Pre-test health checks.
- RTO/RPO target.
- Validation checklist.

## Action

- Execute planned failover in Azure through approved tooling.
- Milestone 6 does not execute failover locally.

## Escalation

Escalate if failover exceeds RTO or data-loss risk exceeds RPO.

## Validation

- Application reconnects.
- Critical smoke checks pass.
- Monitoring confirms target region health.

## Closure

Record timings, issues, failback decision, and lessons learned.

