# Milestone Roadmap

This roadmap preserves the long-term scope while keeping each milestone honest about what is implemented.

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

## Milestone 2: Azure SQL Modernisation Baseline

Planned:

- Legacy SQL Server assessment model.
- Azure SQL Database and Managed Instance target patterns.
- Schema migration workflow.
- Security baseline, auditing, masking, and row-level security examples.
- Backup, HA/DR, and operational runbook foundations.

## Milestone 3: SQL CI/CD and Operational Automation

Planned:

- Database project or migration tooling.
- Schema drift checks.
- Data drift and reference-data validation.
- Query performance baselines.
- Automated deployment gates.

## Milestone 4: Databricks Lakehouse Foundation

Planned:

- ADLS Gen2 structure.
- Databricks workspace conventions.
- Unity Catalog model.
- Delta Lake bronze, silver, and gold conventions.
- Workload optimisation standards.

## Milestone 5: Ingestion and Medallion Processing

Planned:

- Batch ingestion.
- CDC ingestion.
- Streaming ingestion pattern.
- Data quality checks.
- Replay and late-arriving data behaviour.

## Milestone 6: Governance, Security, and Lineage

Planned:

- Purview integration points.
- Classification and ownership metadata.
- End-to-end lineage examples.
- RBAC and access review automation.
- Audit reporting.

## Milestone 7: Operational Analytics

Planned:

- Curated data products for shipment reliability, depot performance, fleet maintenance, and disruption analysis.
- Semantic models or serving views.
- Data freshness and quality SLOs.

## Milestone 8: SQL AI, Vector, and Hybrid Search

Planned:

- Azure SQL native AI patterns.
- Embedding generation boundaries.
- VECTOR storage where appropriate.
- Hybrid search index design.
- Security-trimmed retrieval.

## Milestone 9: Grounded RAG

Planned:

- Azure OpenAI integration.
- Retrieval orchestration.
- Prompt and response evaluation.
- Citation, grounding, and safety controls.
- Clear separation between operational SQL AI and broader AI-platform responsibilities.

## Milestone 10: Monitoring, FinOps, and Production Assurance

Planned:

- Azure Monitor and Log Analytics dashboards.
- Databricks workload observability.
- Cost allocation and anomaly detection.
- Reliability tests.
- RTO/RPO evidence.
- Production readiness review.

