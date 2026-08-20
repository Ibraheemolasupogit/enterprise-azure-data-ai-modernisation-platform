# Milestone Roadmap

This roadmap preserves the long-term scope while keeping each milestone honest about what is implemented.

Scope anchors retained across the programme: Azure SQL modernisation, SQL CI/CD, Databricks, ingestion, medallion architecture, data quality, operational analytics, vector and hybrid search, RAG, monitoring, FinOps, and production assurance.

## Milestone 1: Enterprise Platform Foundation

Implemented in this milestone:

- Repository structure and engineering standards.
- Architecture overview and security model.
- ADR scaffolding and initial decisions.
- Bicep-first infrastructure skeleton.
- Validation scripts, tests, and CI foundation.
- Synthetic enterprise scenario and data strategy.

Intentionally deferred:

- Azure resource deployment.
- SQL schemas, migrations, and performance automation.
- Databricks jobs, notebooks, and Lakeflow pipelines.
- AI search, embeddings, and RAG services.
- Production monitoring and FinOps dashboards.

## Milestone 2: Synthetic Legacy Source Estate

Implemented:

- SQL Server-style legacy OLTP source assets.
- PostgreSQL-like secondary billing source assets.
- Deterministic synthetic fixtures, contracts, workload simulation, and documented data-quality defects.

## Milestone 3: Estate Assessment and Modernisation Decisioning

Implemented:

- Estate inventory, compatibility assessment, dependency model, workload classification, target-service decisions, complexity scoring, wave planning, and risk register.

## Milestone 4: Target-State Architecture and Platform Decisions

Implemented:

- Workload-to-target matrix, component catalog, security controls, recovery strategy, environment model, architecture traceability, and architecture report.

## Milestone 5: Migration Factory

Implemented:

- Migration manifests, target-ready schemas, local deterministic migration execution, reconciliation checks, validation gates, cutover readiness, rollback readiness, and failure scenarios.

## Milestone 6: Azure SQL Operational Administration Model

Implemented:

- SQL MI operating baseline, Bicep module intent, Entra-first security assets, monitoring/KQL assets, alert catalog, SQL Agent jobs, backup/restore readiness, HA/DR readiness, and runbooks.

## Milestone 7: SQL Performance Engineering

Implemented:

- Workload catalog, deterministic baseline model, Query Store and DMV toolkit, index recommendations, statistics strategy, blocking/deadlock scenarios, parameter-sensitive query scenario, regression workflow, and performance assurance evidence.

## Milestone 8: SQL Database Development Lifecycle and CI/CD

Implemented:

- SDK-style SQL Database Project for `legacy_tms`.
- Declarative schema assets, reference-data deployment script, drift scenarios, safety rules, environment promotion matrix, regression gates, release manifest, GitHub Actions CI, and release-preview guardrails.

## Milestone 9: Databricks Platform Foundation and Unity Catalog

Implemented:

- Dev/test/prod Databricks workspace and environment architecture.
- Switch-gated Bicep foundation for workspace, ADLS Gen2, access connector, containers, diagnostics, and private-network assumptions.
- Compute decision framework for interactive, jobs, serverless jobs, SQL warehouse, future pipeline, and exception-only classic compute.
- Unity Catalog catalog/schema strategy, representative DDL, storage credential and external-location model, least-privilege grants, fine-grained governance patterns, governed tags, retention policy, lineage/audit readiness, Delta Sharing boundary, federation decisions, and Databricks Asset Bundle foundation.

## Milestone 10: Databricks Ingestion and Medallion Processing

Implemented:

- Batch, incremental/CDC-oriented, Auto Loader, and Structured Streaming ingestion patterns for current source domains.
- Bronze, Silver, and Gold medallion assets with local transformation functions and Databricks-ready Spark/SQL assets.
- Analytical dimensions/facts, SCD Type 2 customer history strategy, schema drift handling, quarantine routing, replay/idempotency, physical layout strategy, data contracts, and pipeline traceability.

## Milestone 11: Databricks Data Quality and Lakeflow Jobs Orchestration

Implemented:

- Formal data-quality rules and severity/action model across Bronze, Silver, and Gold.
- Deterministic quality evidence, quarantine/replay model, freshness assumptions, failure handling, backfill controls, job permissions, operational traceability, and runbooks.
- Lakeflow Jobs bundle resources for batch feeds, relational incremental loads, event streaming, Gold publication, and controlled backfill/replay.

## Milestone 12: Databricks Monitoring, Troubleshooting, Performance, and Cost Optimization

Implemented:

- Monitoring architecture, system-table query assets, job/pipeline observability, Spark troubleshooting, join optimization, Delta table health, streaming health/recovery, compute optimization, SQL warehouse operations, FinOps cost attribution, alert catalog, SLO assumptions, and runbooks.

## Milestone 13: AI-Enabled SQL, Vector Search, Hybrid Retrieval, and Database-Native RAG

Implemented:

- Customer Service / Shipment Operations Knowledge Assistant use case with explicit no-autonomous-decision boundary.
- AI SQL schema integrated into the SQL database project for documents, chunks, embedding metadata, retrieval audit, and generation audit.
- Target-ready SQL assets for `AI_GENERATE_CHUNKS`, `AI_GENERATE_EMBEDDINGS`, `CREATE EXTERNAL MODEL`, `VECTOR(1536)`, `VECTOR_DISTANCE`, `VECTOR_SEARCH`, full-text search, hybrid RRF ranking, JSON context assembly, and Azure OpenAI outbound invocation.
- Deterministic local evidence for chunking, source traceability, stale detection, ranking fixtures, retrieval metrics, metadata filters, context assembly, security, data exposure, audit, failure handling, cost controls, and readiness.
- Security roles, managed-identity-first configuration placeholders, prompt contract, grounding/citation audit model, and runbooks for embedding, stale vectors, dimension mismatch, quality regression, invocation failure, grounding failure, and data leakage.

Intentionally deferred:

- Live Azure SQL vector, AI function, external model, full-text, and outbound REST validation.
- Real Azure OpenAI embedding or generation calls.
- Production performance, latency, token, and relevance claims.

## Future Milestone: Secure Application and API Integration

Planned:

- Secure application/API façade for the shipment operations assistant.
- End-user authorization propagation into SQL retrieval.
- UX and operational support workflow integration.
- API-level rate limiting, abuse handling, and response review paths.

## Future Milestone: Fabric Downstream Integration Boundary

Planned:

- Explicit Microsoft Fabric consumption boundary where needed.
- Downstream semantic model and reporting integration decisions.
- Cross-platform lineage and governance alignment.

## Future Milestone: Monitoring, FinOps, and Production Assurance

Planned:

- Azure Monitor and Log Analytics dashboards.
- Databricks workload observability.
- Cost allocation and anomaly detection.
- Reliability tests.
- RTO/RPO evidence.
- Production readiness review.
