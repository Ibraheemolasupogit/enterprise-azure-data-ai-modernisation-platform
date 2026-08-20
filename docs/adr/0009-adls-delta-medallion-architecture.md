# ADR-0009: ADLS Gen2 and Delta Medallion Architecture

- Status: Accepted
- Date: 2026-08-20

## Context

The estate contains relational sources, file feeds, event fixtures, data-quality defects, and reporting workloads that should not continue to compete with OLTP systems.

## Decision

Use ADLS Gen2 with Delta Lake medallion zones: landing/raw, bronze, silver, gold, checkpoints, schemas, quarantine, and audit/evidence. Databricks will process and govern these zones through Unity Catalog.

## Consequences

This supports replay, CDC, streaming, data quality, lineage, and analytical offload. It also requires clear lifecycle, access, and environment-separation controls in later implementation milestones.

## Alternatives Considered

- Store analytical data only in operational databases: rejected because it preserves reporting contention and limits replay.
- Use ungoverned file folders only: rejected because enterprise lineage and access controls matter.
- Skip bronze/silver/gold: rejected because data-quality and traceability milestones need explicit processing stages.

