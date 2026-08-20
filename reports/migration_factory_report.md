# Migration Factory Report

Milestone 5 implements a local deterministic migration factory for operational database workloads only. It does not deploy Azure resources and does not claim Azure DMS, Azure Migrate, DMA, SqlPackage, pg_dump, or pg_restore execution.

Selected systems: billing_ops, legacy_tms.
Active failure scenario: none.

## Local Execution Evidence

- Source CSV fixtures were extracted from `data/samples/legacy_estate/tiny`.
- Target-shaped CSV datasets were written under `outputs/migration/local_targets`.
- Schema conversion, reconciliation, validation gates, cutover readiness, rollback readiness, and wave evidence were generated deterministically.

## Simulation Boundary

- Online/minimal-downtime migration is modelled as bulk copy, incremental capture, delta replay, quiesce, final sync, validation, and cutover.
- Cloud-only checks remain `required` and are not marked passed.
- No DNS, application connection, backup/restore, DMS, DMA, SqlPackage, or PostgreSQL native tooling action is performed locally.

## Results

- Reconciliation rows: 54.
- Failed reconciliation rows: 0.
- Failed gates: 0.
- Gates requiring live validation: 6.

## Hypercare Model

- First hour: connectivity smoke checks, row-count sanity, business-critical workflow checks.
- First day: reconciliation rerun, integration review, error monitoring, user support triage.
- First week: performance review, failed integration review, incident trends, migration closure decision.
