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

## Future Milestone: Databricks Lakehouse Foundation

Planned:

- ADLS Gen2 structure.
- Databricks workspace conventions.
- Unity Catalog model.
- Delta Lake bronze, silver, and gold conventions.
- Workload optimisation standards.

## Future Milestone: Ingestion and Medallion Processing

Planned:

- Batch ingestion.
- CDC ingestion.
- Streaming ingestion pattern.
- Data quality checks.
- Replay and late-arriving data behaviour.

## Future Milestone: SQL AI, Vector, and Hybrid Search

Planned:

- Azure SQL native AI patterns.
- Embedding generation boundaries.
- VECTOR storage where appropriate.
- Hybrid search index design.
- Security-trimmed retrieval.

## Future Milestone: Grounded RAG

Planned:

- Azure OpenAI integration.
- Retrieval orchestration.
- Prompt and response evaluation.
- Citation, grounding, and safety controls.
- Clear separation between operational SQL AI and broader AI-platform responsibilities.

## Future Milestone: Monitoring, FinOps, and Production Assurance

Planned:

- Azure Monitor and Log Analytics dashboards.
- Databricks workload observability.
- Cost allocation and anomaly detection.
- Reliability tests.
- RTO/RPO evidence.
- Production readiness review.
