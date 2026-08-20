# 0013 - Databricks Workspace and Catalog Isolation

- Status: Accepted
- Date: 2026-08-20

## Context

The platform needs Databricks development, release validation, and production consumption boundaries without creating unnecessary workspace or catalog sprawl.

## Decision

Use one Azure Databricks workspace per environment and one Unity Catalog catalog per environment: `contoso_freight_dev`, `contoso_freight_test`, and `contoso_freight_prod`. Use consistent bronze, silver, gold, reference, quarantine, and audit schemas in each catalog.

## Consequences

Environment isolation is easy to reason about, workspace-catalog bindings remain direct, and promotion can be modeled cleanly in Databricks Asset Bundles. Domain separation should happen through schemas, tags, ownership, and data products rather than one catalog per trivial domain.

