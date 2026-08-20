# ADR-0010: Databricks Table Boundaries and Ingestion Modes

- Status: Accepted
- Date: 2026-08-20

## Context

Future Databricks work must support batch feeds, CDC/incremental database ingestion, streaming events, managed governance, and replayable storage.

## Decision

Use Databricks for batch, CDC/incremental, and streaming ingestion boundaries. Prefer external Delta tables over ADLS-governed zones unless a managed table is specifically justified by lifecycle ownership. Use Unity Catalog for catalog/schema/table governance.

## Consequences

This keeps storage ownership explicit and supports environment portability. Later milestones must define Lakeflow pipelines/jobs, checkpoint locations, schema evolution, data-quality expectations, and managed table exceptions.

## Alternatives Considered

- Make every table managed: rejected because external ADLS zone ownership is important for replay and lifecycle controls.
- Use only batch ingestion: rejected because event fixtures and CDC requirements are explicit future needs.
- Implement streaming now: rejected because Milestone 4 is architecture only.

