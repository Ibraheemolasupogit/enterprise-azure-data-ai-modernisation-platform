# 0014 - Unity Catalog Managed and External Assets

- Status: Accepted
- Date: 2026-08-20

## Context

Contoso Freight needs governed analytical data products while still accommodating landing zones, checkpoints, quarantine payloads, and exchange paths in ADLS Gen2.

## Decision

Prefer managed Unity Catalog tables for Silver and Gold data products. Use external locations for landing, checkpoints, quarantine payloads, and explicit exchange zones where ADLS lifecycle ownership remains outside the table lifecycle.

## Consequences

Unity Catalog remains the governance authority for Databricks data objects. External paths stay limited and purposeful, reducing duplicated governance between ADLS and Unity Catalog.

