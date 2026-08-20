# Enterprise Azure Data and AI Modernisation Platform

This repository is the foundation for an enterprise Azure Data and AI modernisation reference implementation that modernises a legacy operational data estate into a secure platform.

The scenario is a fictional international logistics company, Contoso Freight, moving from fragmented SQL Server workloads and spreadsheet-driven analytics toward a governed platform spanning Azure SQL, Azure Databricks, ADLS Gen2, Microsoft Entra ID, Key Vault, observability, CI/CD, and AI-enabled data products.

Milestone 1 establishes the repository structure, architectural intent, engineering standards, and decision records. Milestone 2 adds a deterministic synthetic legacy source estate for future assessment, migration, ingestion, governance, performance, and AI work. Milestone 3 adds estate assessment and modernisation decisioning. Milestone 4 adds target-state architecture and platform decisions. Milestone 5 adds a local migration factory for schema, data, validation, cutover, rollback, and evidence generation. Milestone 6 adds the Azure SQL operational administration model. Milestone 7 adds SQL performance engineering. Milestone 8 adds SQL database development lifecycle, database-as-code, dacpac build readiness, release evidence, drift controls, and CI/CD guardrails. Milestone 9 adds the Databricks platform and Unity Catalog foundation. Milestone 10 adds Databricks ingestion, data modelling, and medallion processing. Milestone 11 adds Databricks data quality, Lakeflow Jobs, and operational orchestration. Milestone 12 adds Databricks monitoring, troubleshooting, performance, and cost optimization. Milestone 13 adds AI-enabled SQL, vector search, hybrid retrieval, and database-native RAG design for a grounded shipment operations assistant. Milestone 14 adds secure application/API integration with Data API Builder, REST, GraphQL, stored-procedure boundaries, MCP tool contracts, Container Apps hosting architecture, and deterministic security evidence. Milestone 15 adds the Microsoft Fabric downstream integration boundary for governed Gold product handoff, contracts, ownership, identity, lineage, freshness, quality, and failure responsibility. The repository still does not deploy Azure resources, does not claim working AI workloads, run production Databricks pipelines, execute Azure SQL AI functions locally, invoke Azure OpenAI locally, run a production application API, or implement Fabric resources.

## Business Problem

Contoso Freight runs shipment booking, depot operations, fleet maintenance, customer service, and disruption management on a mixed estate of legacy SQL Server databases, file drops, and manual reporting. Teams need faster operational insight, governed analytical data, reliable migration paths for relational workloads, and controlled AI capabilities that can search and reason over enterprise data without bypassing security controls.

## Target Solution

The planned platform provides:

- Azure SQL modernisation patterns for operational databases, including Azure SQL Database, Azure SQL Managed Instance, and SQL Server on Azure VM trade-offs.
- Azure Databricks engineering for batch, CDC, and streaming ingestion into a medallion lakehouse on ADLS Gen2 and Delta Lake.
- Unity Catalog, Microsoft Purview integration points, lineage, data quality gates, and access controls.
- Azure SQL native AI capabilities where they belong close to operational data, plus external vector, hybrid search, and RAG components where broader retrieval or orchestration is required.
- Managed identity, Microsoft Entra-first authentication, Key Vault, least privilege RBAC, encryption, row-level security, masking, and auditing.
- Infrastructure as Code, CI/CD, validation, monitoring, FinOps, and operational runbooks.

## High-Level Architecture

```mermaid
flowchart LR
  Legacy["Legacy SQL Server and file estate"] --> Migration["Assessment and migration patterns"]
  Migration --> AzureSQL["Azure SQL Database / Managed Instance"]
  Legacy --> Ingestion["Batch, CDC, and streaming ingestion"]
  AzureSQL --> Ingestion
  Ingestion --> Bronze["ADLS Gen2 + Delta bronze"]
  Bronze --> Silver["Databricks silver transformations"]
  Silver --> Gold["Curated gold data products"]
  Gold --> Analytics["Operational analytics and serving"]
  AzureSQL --> SqlAI["Database-native AI features"]
  Gold --> Search["Vector and hybrid search"]
  Search --> Rag["Grounded RAG services"]
  SqlAI --> Rag
  Governance["Entra ID, Key Vault, Unity Catalog, Purview, Monitor"] --- AzureSQL
  Governance --- Ingestion
  Governance --- Rag
```

## Current Implementation

Milestone 1 includes:

- Professional repository structure for infrastructure, SQL, Databricks, data engineering, AI, governance, observability, CI/CD, tests, documentation, synthetic data planning, and runbooks.
- Architecture documentation, system boundaries, principles, data-flow model, environment strategy, and HA/DR guidance.
- ADR scaffolding and initial architecture decisions.
- Bicep-first infrastructure skeleton with environment parameter placeholders.
- Deterministic repository and documentation validation.
- GitHub Actions CI foundation for local-equivalent validation.

Milestone 2 includes:

- A coherent synthetic Contoso Freight legacy estate covering customer/account management, freight orders, depots/routes, vehicles, billing/payments, and customer-service cases.
- SQL Server-style OLTP source scripts with tables, constraints, indexes, views, stored procedures, seed reference data, teardown, and representative workload queries.
- A PostgreSQL-like secondary billing and customer-service source schema.
- Deterministic synthetic-data generation with `tiny`, `development`, and `performance` profiles.
- Committed tiny sample fixtures plus ignored local generation paths for larger datasets.
- CSV, JSON, and JSONL feed/event fixtures with intentional, documented data-quality defects.
- Machine-readable contracts for file feeds, operational events, and core identifiers.
- A deterministic workload simulator for OLTP, operational reporting, analytical candidates, and CDC/event-source candidates.

Milestone 3 includes:

- Machine-readable estate inventory with explicit evidence classifications.
- Dependency model across applications, databases, stored procedures, file feeds, billing/service systems, reporting, events, identity, and scheduling.
- Local static compatibility assessment for SQL Server-style assets.
- Workload classification from the deterministic simulator.
- Azure target-service decisions with selected targets, rejected alternatives, and modernisation disposition.
- Configurable migration complexity scoring, migration wave planning, risk register, generated CSV outputs, and assessment report.

Milestone 4 includes:

- Target architecture across operational data, analytical/data-engineering, future AI-enabled data, and control/security/operations planes.
- Formal workload-to-target matrix, component catalog, security-control matrix, recovery strategy matrix, environment matrix, assumption register, and architecture traceability.
- Design decisions for Azure SQL Managed Instance, PostgreSQL Flexible Server, Databricks, ADLS Gen2, Delta Lake, Unity Catalog, private networking, identity, data protection, HA/DR, and environment isolation.
- Architecture report and validation command for deterministic target-state outputs.

Milestone 5 includes:

- Migration manifests for `legacy_tms` and `billing_ops`.
- Target-ready Azure SQL Managed Instance and PostgreSQL Flexible Server schema assets.
- Compatibility remediation register mapped to assessment findings.
- Local deterministic migration execution from synthetic source fixtures to target-shaped CSV outputs.
- Reconciliation checks, validation gates, migration wave execution evidence, cutover readiness, rollback readiness, failure scenarios, tooling integration boundaries, and hypercare model.

Milestone 6 includes:

- Azure SQL Managed Instance operational configuration baseline for `legacy_tms`.
- Bicep module intent for SQL MI, managed identity, Key Vault, diagnostics, Log Analytics, and alerting.
- Entra-first T-SQL security roles, placeholder principals, grants, masking, classification, and RLS pattern.
- KQL investigation assets, alert catalog, SQL Agent job definitions, backup/restore readiness, HA/DR readiness, operational readiness evidence, and runbooks.

Milestone 7 includes:

- SQL performance workload catalog and deterministic baseline model.
- Query Store configuration/diagnostic scripts, DMV toolkit, execution-plan analysis model, index recommendations, statistics strategy, blocking/deadlock scenarios, parameter-sensitive query scenario, regression workflow, and performance assurance evidence.

Milestone 8 includes:

- SDK-style SQL Database Project for the `legacy_tms` Azure SQL Managed Instance target using `Microsoft.Build.Sql`.
- Declarative table, view, procedure, security, pre-deployment, post-deployment reference-data, and static test assets.
- Dacpac build command that uses real local tooling when available and fails clearly when `dotnet` is absent.
- Deterministic SQL release evidence for inventory, traceability, reference data, safety rules, drift scenarios, environment promotion, tests, performance gates, security gates, readiness, and release manifest.
- GitHub Actions CI/CD guardrails for validation, dacpac build, artifact upload, release preview, environment approval, and explicit no-secret/no-fake-publish boundaries.

Milestone 9 includes:

- Azure Databricks dev/test/prod workspace and environment architecture.
- Switch-gated Bicep foundation for workspace, ADLS Gen2, access connector, containers, diagnostics, and managed-identity boundaries.
- Compute strategy for interactive, jobs, serverless jobs, SQL warehouse, future pipeline, and exception-only classic compute.
- Unity Catalog namespace design with environment catalogs and bronze, silver, gold, reference, quarantine, and audit schemas.
- Target-ready Unity Catalog SQL assets for representative shipment, customer, depot/route, billing/service, operational event, quarantine, audit, view, function, and governance objects.
- Least-privilege access model, governed tags, row/column security patterns, retention strategy, lineage/audit readiness, Delta Sharing and federation boundaries, and Databricks Asset Bundle foundation.

Milestone 10 includes:

- Source ingestion patterns for `legacy_tms`, `billing_ops`, depot reference feeds, carrier updates, customer service exports, and shipment operational events.
- Bronze, Silver, and Gold medallion design with Databricks-ready Spark/PySpark/SQL assets and deterministic local transformation functions.
- Auto Loader, Structured Streaming, incremental/CDC, checkpoint, replay, idempotency, schema drift, and quarantine design.
- Analytical data model with dimensions, facts, physical layout strategy, and SCD Type 2 customer dimension logic.
- Data contracts and generated evidence for ingestion, Bronze/Silver/Gold catalogs, model, SCD, drift, checkpoints, quarantine, replay, layout, traceability, and readiness.

Milestone 11 includes:

- Formal data-quality rules by Bronze, Silver, and Gold layer with severity/action mappings.
- Deterministic quality evidence, quarantine catalog, replay/remediation model, freshness assumptions, and publication gate behavior.
- Lakeflow Jobs bundle resources for batch feeds, relational increments, event streaming, Gold publication, and controlled backfill/replay.
- Task dependencies, parameters, schedules, retry/timeout policy, failure handling, permissions, traceability, and operational runbooks.

Milestone 12 includes:

- Databricks monitoring architecture across Lakeflow Jobs, tasks, compute, serverless, SQL warehouses, Structured Streaming, Delta tables, Unity Catalog, quality gates, storage, audit/security, and cost.
- Databricks-ready system-table SQL query assets for jobs, compute, query history, audit, lineage, warehouse latency, and cost attribution.
- Spark troubleshooting, join optimization, Delta table health, retention/VACUUM safety, predictive optimization assessment, streaming health/recovery, compute policy, SQL warehouse operations, FinOps, alerts, SLO assumptions, and runbooks.

Milestone 13 includes:

- AI-ready SQL schema assets for `ai.Document`, `ai.DocumentChunk`, `ai.EmbeddingMetadata`, `ai.RetrievalAudit`, and `ai.GenerationAudit` integrated into the SQL database project.
- Target-ready SQL examples for `AI_GENERATE_CHUNKS`, `AI_GENERATE_EMBEDDINGS`, `CREATE EXTERNAL MODEL`, `VECTOR(1536)`, `VECTOR_DISTANCE`, `VECTOR_SEARCH`, full-text search, RRF hybrid ranking, JSON context assembly, and outbound Azure OpenAI invocation.
- Deterministic local evidence for chunking, source traceability, stale detection, metadata filters, retrieval fixtures, Precision@K, Recall@K, MRR, context contracts, security, audit, failure handling, and cost controls.
- SQL AI architecture documentation, environment placeholders with no secrets, runbooks, and CI/CD guardrails for external model, vector dimension/index, endpoint, AI role, and retrieval-security changes.

Milestone 14 includes:

- Allowlisted application/API use cases for shipment lookup, operational reference lookup, sanitized service-case retrieval, governed AI retrieval/RAG execution, and grounding source metadata.
- Production-style Data API Builder configuration with Entra authentication, explicit roles, REST routes, selected GraphQL read entities, field restrictions, and no anonymous production permissions.
- Target-ready SQL API views, stored-procedure boundaries, API roles/permissions, OpenAPI and GraphQL examples, MCP-compatible read-focused tool contracts, KQL observability queries, and Container Apps Bicep module.
- Deterministic evidence for API catalog, DAB entities, authorization, sensitive exposure, AI endpoint contract, MCP security, hosting, resilience, errors, rate limits, observability, audit traceability, security scenarios, and readiness.

Milestone 15 includes:

- Explicit Azure/Fabric/shared ownership boundary for producer and downstream consumer responsibilities.
- Fabric-facing Gold product catalog for shipment operations performance, depot/route performance, delivery delay metrics, billing/revenue summary, and service/incident summary.
- Integration pattern decisions favoring governed Delta/ADLS publication plus OneLake shortcut/interoperability where validated, with controlled copy only by exception.
- Contract-first schema, versioning, publication gate, freshness, identity/access, sensitivity, lineage, quality manifest, failure ownership, and cost/duplication evidence.

## Planned Roadmap

Future milestones will add final cross-platform assurance and portfolio release. The full milestone roadmap is maintained in [docs/roadmap.md](docs/roadmap.md).

## Architecture Decisions and Trade-Offs

This platform deliberately separates workload responsibilities:

- Azure SQL remains the system of record for operational relational workloads where transactional consistency, security, and SQL performance engineering matter most.
- Databricks owns scalable lakehouse engineering, data quality, transformation, and analytical processing.
- Database-native AI is used for close-to-data capabilities, while external AI/search services handle cross-domain retrieval, orchestration, and grounded assistant patterns.
- Managed identity and Entra-first authentication are preferred to reduce secret sprawl and support auditable least privilege.
- Bicep is the default IaC language for Azure-native resources because it keeps Azure resource modelling explicit and reviewable.

## Repository Map

| Path | Purpose |
| --- | --- |
| `infra/` | Bicep infrastructure modules, environment parameter placeholders, deployment scripts |
| `src/azure_sql/` | SQL schema, migration, operations, performance, database project, and release automation assets |
| `src/databricks/` | Databricks Unity Catalog foundation assets plus future jobs, Lakeflow, and notebooks |
| `src/data_engineering/` | Secondary source schemas plus future ingestion, CDC, streaming, modelling, and data-quality code |
| `src/ai/` | Future SQL AI, embeddings, search, and RAG components |
| `src/security_governance/` | Future RBAC, policies, lineage, masking, and audit automation |
| `src/observability/` | Future monitoring, SLO, logging, and FinOps assets |
| `docs/` | Architecture, roadmap, ADRs, runbooks, and operating model |
| `data/` | Synthetic data strategy, source contracts, sample fixtures, and ignored local generated data zones |
| `outputs/` | Generated estate-assessment CSV outputs |
| `reports/` | Generated assessment, architecture, migration, and operations reports |
| `tests/` | Deterministic validation for repository foundation and synthetic legacy estate |

## Local Validation

```bash
python3 -m pip install -e ".[dev]"
make validate
```

The validation checks required directories, key documentation, ADR metadata, and internal Markdown links.

Generate the default local development estate with:

```bash
make generate-estate
make generate-workload
```

Generated development outputs are written under `data/raw/legacy_estate/` and are intentionally ignored by git.

Generate the estate assessment outputs with:

```bash
make assess-estate
```

Generate and validate the target architecture outputs with:

```bash
make validate-architecture
```

Run the local migration factory with:

```bash
make migrate-local
make validate-migration
```

Generate and validate Azure SQL operations evidence with:

```bash
make validate-azure-sql-operations
```

Generate and validate SQL performance evidence with:

```bash
make validate-sql-performance
```

Generate and validate SQL AI, vector search, hybrid retrieval, and database-native RAG evidence with:

```bash
make validate-sql-ai
```

Generate and validate secure application/API integration evidence with:

```bash
make validate-application-integration
```

Generate and validate Fabric downstream integration boundary evidence with:

```bash
make validate-fabric-integration
```

Generate and validate SQL database lifecycle and CI/CD evidence with:

```bash
make validate-sql-cicd
make build-sql-project
```

`make build-sql-project` requires a local .NET SDK and Microsoft.Build.Sql restore capability. If that tooling is unavailable, the command reports the missing dependency instead of claiming a dacpac exists.

Generate and validate Databricks platform foundation evidence with:

```bash
make validate-databricks-foundation
```

Generate and validate Databricks ingestion and medallion evidence with:

```bash
make validate-databricks-pipelines
```

Generate and validate Databricks data-quality and orchestration evidence with:

```bash
make validate-databricks-orchestration
```

Generate and validate Databricks monitoring and optimization evidence with:

```bash
make validate-databricks-operations
```
