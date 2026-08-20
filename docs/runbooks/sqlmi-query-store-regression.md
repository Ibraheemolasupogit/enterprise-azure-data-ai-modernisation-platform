# SQL MI Query Store Regression

## Trigger

Query Store regressed-query signal or post-change performance regression.

## Triage

- Identify query_id, plan_id, runtime interval, and previous plan.
- Compare duration, CPU, reads, waits, and execution count.
- Confirm parameter distribution and statistics freshness.

## Evidence

- Query Store plan history.
- Runtime stats before and after regression.
- Plan comparison.
- Related deployment or data-change event.

## Action

- Consider Query Store plan forcing only with evidence.
- Consider Query Store hints or targeted recompilation only as reversible mitigation.
- Remove temporary forcing/hints after durable fix.

## Escalation

Escalate if regression affects critical transport workflows.

## Validation

- Runtime stats return to baseline.
- Error rates and blocking do not increase.

## Closure

Record query_id, plan_id, mitigation, validation, and removal plan.

