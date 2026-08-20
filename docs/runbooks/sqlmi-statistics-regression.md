# SQL MI Statistics Regression

## Trigger

Regression suspected from stale statistics, poor cardinality estimates, or post-load data distribution change.

## Triage

- Check `STATS_DATE`, modification counters, and affected plan estimates.
- Identify whether regression is isolated to one statistic/table.
- Review recent bulk load or migration activity.

## Evidence

- Statistics metadata.
- Plan estimate vs actual row count comparison in real SQL MI.
- Query Store runtime stats.

## Action

- Use targeted `UPDATE STATISTICS`.
- Use FULLSCAN only for narrow evidence-backed cases.
- Avoid blanket fullscan on every table.

## Escalation

Escalate if critical workflows remain regressed after targeted stats update.

## Validation

- Plan quality and runtime return to baseline.
- No excessive maintenance overhead appears.

## Closure

Record statistics updated, rationale, and follow-up monitoring.

