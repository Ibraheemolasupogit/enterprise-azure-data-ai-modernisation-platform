# SQL MI Regional DR Failover

## Trigger

Regional outage, severe platform degradation, or disaster declaration.

## Triage

- Confirm incident scope.
- Validate primary region impact.
- Confirm secondary region readiness.
- Convene incident commander, DBA, platform, application, and business owner.

## Evidence

- Azure status and resource health.
- Replication/failover status.
- Last known recovery point.
- Business impact assessment.

## Action

- Execute DR failover only through approved emergency change.
- Communicate connection implications to application teams.
- Track RTO/RPO.

## Escalation

Escalate immediately for critical transport OLTP outage.

## Validation

- Application reconnects.
- Critical workflows pass.
- Data-loss window is understood and accepted.

## Closure

Record failover timeline, data-loss estimate, failback plan, and incident review.

