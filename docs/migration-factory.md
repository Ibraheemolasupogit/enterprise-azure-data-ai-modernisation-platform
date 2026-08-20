# Migration Factory

Milestone 5 implements a local deterministic migration factory for operational database workloads:

- `legacy_tms` from SQL Server-style source assets to an Azure SQL Managed Instance target design.
- `billing_ops` from PostgreSQL-like source assets to an Azure Database for PostgreSQL Flexible Server target design.

File/event workloads are intentionally excluded and remain Databricks ingestion work for later milestones.

## Local vs Azure Boundary

Local execution:

- Reads committed synthetic source CSV fixtures.
- Writes target-shaped CSV datasets under `outputs/migration/local_targets`.
- Generates schema conversion, reconciliation, validation gate, wave execution, cutover, rollback, and tooling-boundary evidence.

Not executed locally:

- Azure Database Migration Service.
- Azure Migrate.
- Data Migration Assistant.
- SqlPackage.
- SQL backup/restore.
- `pg_dump` / `pg_restore`.
- Azure CLI or PowerShell against real resources.

## Migration Modes

`legacy_tms` prefers an online/minimal-downtime design:

1. Initial bulk copy.
2. Capture incremental changes.
3. Replay delta.
4. Quiesce writes.
5. Final synchronization.
6. Validation.
7. Cutover.

`billing_ops` prefers offline migration because the workload has a wider downtime tolerance and lower migration complexity.

## Validation Strategy

Validation gates are grouped as:

- PRE-MIGRATION
- POST-LOAD
- PRE-CUTOVER
- POST-CUTOVER

Cloud-only checks are marked `required`, not passed.

## Evidence Model

Generated evidence lives under `outputs/migration/` and `reports/migration_factory_report.md`.

Evidence classifications include:

- locally validated
- simulated evidence
- architecture/design evidence
- derived from assessment
- requires live validation

## Failure Behaviour

Controlled failure scenarios stop unsafe progression and emit failed evidence:

- row-count mismatch
- missing dependency
- unresolved compatibility blocker
- duplicate key
- checksum mismatch
- stale delta
- failed validation gate

