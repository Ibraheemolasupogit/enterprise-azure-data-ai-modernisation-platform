# ADR-0002: Databricks Lakehouse Role

- Status: Accepted
- Date: 2026-08-20

## Context

The platform needs scalable ingestion, medallion processing, Delta Lake optimisation, data quality, lineage, and governed analytical modelling. These concerns should not be forced into operational databases.

## Decision

Use Azure Databricks as the primary lakehouse engineering platform for batch, CDC, streaming, transformation, data quality, and curated analytical data products. Use Unity Catalog for Databricks data governance.

## Consequences

Databricks becomes a central implementation surface for analytical workloads. Operational SQL systems stay focused on transactional integrity and serving patterns. The platform must define clear interfaces between Azure SQL, ADLS Gen2, Databricks, and downstream analytics.

## Alternatives Considered

- Implement all analytical processing in Azure SQL: unsuitable for large-scale lakehouse processing and multi-format ingestion.
- Use only low-code data movement tools: useful for some ingestion but insufficient as the sole engineering foundation.
- Use general-purpose compute without Databricks: possible, but less aligned with Delta Lake, Unity Catalog, and enterprise lakehouse patterns.

