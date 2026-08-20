# SQL MI Index Regression

## Trigger

Performance regression after index creation, removal, or changed index usage.

## Triage

- Identify changed index and affected workload.
- Review Query Store before/after runtime stats.
- Check write overhead, blocking, and storage growth.

## Evidence

- Change record.
- Query Store comparison.
- Index usage DMV snapshot.
- Write overhead indicators.

## Action

- Revert index change if it causes unacceptable regression.
- Avoid adding compensating indexes without evidence.
- Route durable changes through future SQL CI/CD.

## Escalation

Escalate if regression affects critical OLTP writes.

## Validation

- Affected workload returns to baseline.
- No new write path impact is observed.

## Closure

Record decision, validation, and CI/CD follow-up.

