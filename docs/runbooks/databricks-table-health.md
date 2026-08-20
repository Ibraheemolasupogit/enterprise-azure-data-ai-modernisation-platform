# Databricks Small File and Table Health

## Trigger

Delta table has excessive file counts, tiny average files, transaction-log growth, or stale clustering.

## Triage

Review table size, file count, average file size, write pattern, table history, CDF state, and retention.

## Evidence

Use Delta table details/history, system metadata, and workload query patterns.

## Remediation

Compact or `OPTIMIZE` only after evidence. Avoid partitioning small tables. Prefer liquid clustering for evolving analytical patterns where supported.

## Validation

Validate read performance, write impact, and cost after runtime optimization.

## Escalation

Escalate destructive retention or schema concerns to governance and platform owners.

## Closure

Record table, before/after evidence, and retention implications.

