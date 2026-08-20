# Databricks Platform Foundation and Unity Catalog

Milestone 9 establishes the Azure Databricks and Unity Catalog foundation for Contoso Freight. It starts the data-engineering plane without implementing ingestion pipelines, transformations, AI/RAG, Fabric workloads, or production assurance.

## Workspace Architecture

The environment model uses one Azure Databricks workspace per environment: dev, test, and prod. This preserves isolation without unnecessary workspace proliferation.

Each workspace has:

- Its own Azure resource boundary.
- Its own ADLS Gen2 storage boundary.
- Its own Unity Catalog catalog binding.
- Its own deployment target in `databricks.yml`.
- Managed identity and Entra group/service-principal based access.

The assumed primary region is UK South, consistent with the existing environment strategy. Promotion flows from feature branches and pull requests into dev, then controlled test and protected prod targets.

## Infrastructure Foundation

`infra/modules/databricks/foundation.bicep` declares:

- Azure Databricks workspace.
- ADLS Gen2 storage account with shared keys disabled.
- Landing, checkpoint, quarantine, and exchange containers.
- Databricks access connector with managed identity.
- Log Analytics workspace and diagnostic settings.

The module is disabled by default through `deployDatabricksFoundation = false`. Local validation does not deploy Azure resources.

## Compute Strategy

Compute is selected by workload class:

- All-purpose compute: dev-only interactive engineering and exploration.
- Jobs compute: batch ingestion and future transformation workloads.
- Serverless jobs: event or elastic jobs where region and policy support it.
- SQL warehouses: curated Gold consumption and operational analytics.
- Pipeline compute: future Lakeflow or Delta Live Tables pipeline milestones.
- Classic compute: exception-only compatibility path.

Production workloads must run under service principals, compute policies, controlled library scopes, autoscaling, and auto-termination. No performance benchmarks are claimed until Databricks runtime evidence exists.

## Unity Catalog Namespace

The catalog model is environment-scoped:

- `contoso_freight_dev`
- `contoso_freight_test`
- `contoso_freight_prod`

Each catalog uses consistent schemas:

- `bronze`
- `silver`
- `gold`
- `reference`
- `quarantine`
- `audit`

The foundation includes representative DDL for shipment events, shipments, customer accounts, depot/route reference data, billing/service cases, data-quality events, a quarantine volume, reusable functions, and a Gold reliability view. It does not implement the pipelines that populate those objects.

## Managed and External Objects

Managed tables are preferred for Silver and Gold data products because Unity Catalog governs metadata and storage lifecycle together. External locations are used where another process owns the file lifecycle: landing zones, checkpoints, quarantine payloads, and explicit exchange zones.

Managed volumes are used for governed platform-owned files. External volumes are reserved for controlled exchange or landing cases where ADLS lifecycle ownership remains outside the table lifecycle.

## Storage Credentials and External Locations

Unity Catalog storage access is modeled through:

- Managed identity/access connector.
- Storage credentials.
- External locations.

No storage keys, SAS tokens, PATs, or connection strings are committed. Managed Silver and Gold tables remain governed primarily through Unity Catalog, while raw landing and checkpoint paths retain explicit ADLS lifecycle responsibilities.

## Access Control and Fine-Grained Governance

Access is group and service-principal based. Representative personas include platform administrators, data engineers, pipeline workload identity, data quality operators, operational analysts, security auditors, downstream consumers, and CI/CD identity.

Fine-grained access uses modern Unity Catalog row filters, column masks, and ABAC policy patterns:

- Customer email masking.
- Region-based shipment row filtering.
- Restricted service-case detail masking.
- Quarantine schema isolation.

Governed tags are intentionally small and meaningful: `pii`, `sensitivity`, `domain`, `lifecycle`, and `environment`.

## Discoverability

Tables, columns, schemas, and catalogs include comments and purpose statements. AI-generated descriptions may be evaluated later as an optional catalog productivity feature, but this milestone does not claim to have run AI-generated comments.

## Retention and Lifecycle

Retention balances recovery, time travel, storage cost, and compliance deletion. Bronze keeps shorter replay windows than Gold and audit. Audit data keeps the longest retention for investigation. VACUUM should not be shortened below deleted-file retention requirements, and compliance deletes must account for downstream aggregates and lineage.

Predictive optimization and ADLS lifecycle tiering are Azure validation topics; they are not executed locally.

## Lineage and Audit

Unity Catalog lineage is the target mechanism for table, column, job, notebook, and downstream impact analysis. The repository includes query templates for system tables, but it does not fabricate lineage graphs or audit events before pipelines and workspaces exist.

Audit design covers Unity Catalog events, workspace events, compute events, job/pipeline events, secret access, and administrative changes. Azure Log Analytics is the integration boundary for resource diagnostics.

## Delta Sharing

Delta Sharing is an exception-based external sharing boundary. Internal account consumers should normally use Unity Catalog grants. External sharing is limited to approved Gold/reference data products, excludes raw PII and restricted service-case content, and requires revocation and audit evidence.

## Federation Boundary

Foreign catalogs and query federation are transitional tools for discovery, profiling, reconciliation, and limited operational access. They are not the primary ingestion architecture. Analytical reporting should use replicated or ingested data in the lakehouse.

## AI/BI Genie Boundary

AI/BI Genie is a future governed-consumption capability over curated Gold objects. Any future exposure requires semantic instructions, certified objects, row/column security validation, and clear consumer boundaries.

## Bundle and Git Workflow

`databricks.yml` defines dev/test/prod targets without fake jobs or pipelines. Production requires a protected service principal. Source code remains authoritative in GitHub; Databricks workspace Git folders are a development convenience, not the production source of truth.

## Validation Boundary

Local validation covers deterministic evidence, static SQL, IaC and bundle structure, and tests. Real Azure Databricks validation is still required for workspace creation, metastore assignment, storage credential binding, ABAC policy execution, lineage capture, audit logs, Delta Sharing, federation, compute runtime behavior, and cost/performance tuning.

