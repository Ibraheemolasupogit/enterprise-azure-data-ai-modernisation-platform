# Databricks Platform Foundation and Unity Catalog Report

Milestone 9 defines an implementation-ready Azure Databricks platform foundation for Contoso Freight. It covers dev/test/prod workspace boundaries, compute selection, Unity Catalog namespace design, storage credentials and external locations, least-privilege access, fine-grained governance, retention, lineage/audit readiness, Delta Sharing, federation boundaries, and Databricks Asset Bundle foundations.

No Azure Databricks workspace, Unity Catalog object, storage credential, external location, job, pipeline, lineage graph, audit event, or share was deployed or fabricated by this milestone.

## Evidence Boundary

- Locally validated: deterministic CSV evidence, documentation, bundle file structure, static SQL/IaC assets, tests.
- Configuration defined: Bicep resources, Unity Catalog DDL, grant model, compute policy intent, retention model.
- Simulated: none required for this milestone.
- Requires Azure validation: workspace creation, metastore assignment, ABAC policy execution, lineage capture, audit logs, system tables, Delta Sharing, federation, and runtime/compute behaviour.

## Platform Shape

The model uses one workspace per environment and one catalog per environment: `contoso_freight_dev`, `contoso_freight_test`, and `contoso_freight_prod`. Schemas are consistent across environments: bronze, silver, gold, reference, quarantine, and audit.

## Compute

Interactive compute is restricted to development and exploration. Production ingestion and transformation should run through jobs or future pipeline compute under service principals and compute policies. SQL warehouses serve curated Gold objects, while classic compute is exception-only.

## Governance

Unity Catalog is the authority for Databricks data-object governance. Managed tables are preferred for Silver and Gold data products; external locations are used for landing, checkpoints, quarantine payloads, and controlled exchange zones. ABAC with governed tags is preferred for consistent row and column enforcement, with table-level filters/masks only as a fallback.
