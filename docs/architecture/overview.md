# Architecture Overview

## Problem Statement

Contoso Freight operates a legacy data estate across depot operations, shipment booking, fleet maintenance, customer service, and disruption management. Core transactional systems are relational and SQL-heavy, but analytics depends on delayed exports, local spreadsheets, and duplicated reporting logic. Governance is inconsistent, operational data lineage is weak, and AI experimentation risks bypassing established access controls.

The target platform must modernise relational workloads without losing operational resilience, establish a governed analytical lakehouse, and provide AI-enabled data capabilities with clear boundaries between database-native intelligence and broader retrieval-augmented services.

## Target-State Architecture

The intended architecture has four primary planes:

- Operational data plane: Azure SQL Database and Azure SQL Managed Instance patterns for modernised relational workloads, with SQL Server on Azure VM reserved for compatibility cases that cannot reasonably move to platform services.
- Analytical data plane: ADLS Gen2, Delta Lake, Databricks, Unity Catalog, medallion processing, data modelling, and data-quality controls.
- AI data plane: Azure SQL native AI features for close-to-data scenarios, plus external embeddings, vector/hybrid search, and Azure OpenAI grounded RAG where cross-domain retrieval and orchestration are required.
- Control plane: Microsoft Entra ID, managed identities, Key Vault, RBAC, policy, Purview integration points, Azure Monitor, Log Analytics, CI/CD, and Infrastructure as Code.

Milestone 1 defines the repository foundation only. Later milestones will implement workloads incrementally inside this architecture.

## Core Principles

- Prefer managed Azure platform services where they reduce undifferentiated operations without hiding architectural trade-offs.
- Keep transactional systems, analytical processing, and AI orchestration responsibilities explicit.
- Use Microsoft Entra ID and managed identity by default; avoid secrets wherever workload identity is available.
- Treat data products as governed assets with ownership, lineage, quality expectations, and access policies.
- Build repeatable infrastructure and database changes through source-controlled deployment paths.
- Separate dev, test, and prod through environment parameters, RBAC boundaries, data classification, and promotion gates.
- Make observability, cost, reliability, and rollback considerations first-class implementation work.

## System and Context Boundaries

In scope for the full platform:

- SQL Server estate assessment and migration decision patterns.
- Azure SQL Database, Managed Instance, and relevant SQL Server on Azure VM reference designs.
- Databricks ingestion, transformation, workload optimisation, and governance.
- Synthetic transactional and analytical datasets based on Contoso Freight.
- AI search and RAG capabilities grounded in governed platform data.
- CI/CD, validation, security controls, observability, and operational runbooks.

Out of scope for Milestone 1:

- Provisioned Azure infrastructure.
- Deployed databases, Databricks workspaces, or cloud networking.
- Real customer, shipment, employee, or vehicle data.
- Production-grade RAG application code.
- Complete Purview, Monitor, or FinOps implementation.

## Major Data Flows

1. Operational systems produce shipment, depot, fleet, customer, and disruption transactions in SQL Server-compatible relational models.
2. Modernised operational workloads move to Azure SQL Database or Azure SQL Managed Instance according to compatibility, isolation, HA/DR, and operational requirements.
3. Batch, CDC, and streaming ingestion patterns land data into ADLS Gen2 bronze Delta tables.
4. Databricks pipelines validate, standardise, conform, and enrich data into silver models.
5. Gold data products support operational analytics, performance reporting, service reliability monitoring, and downstream AI retrieval.
6. Sensitive fields are classified, masked, encrypted, and protected through RBAC, row-level security, Unity Catalog, and policy controls.
7. AI capabilities consume approved operational or curated analytical data through explicit retrieval and serving contracts.

## Security and Governance Model

The platform uses a least-privilege, Entra-first model:

- Workload identities use managed identities where supported.
- Secrets that remain unavoidable are stored in Key Vault and never committed.
- RBAC is scoped by environment and workload responsibility.
- SQL access patterns include contained users, role-based grants, auditing, dynamic data masking where appropriate, and row-level security for tenant or region isolation scenarios.
- Databricks access uses Unity Catalog, workspace separation, service principals or managed identity integration, and cluster policies.
- Data classification, lineage, and audit events are designed for Purview and Log Analytics integration.

## Environments

| Environment | Purpose | Data posture | Controls |
| --- | --- | --- | --- |
| `dev` | Fast iteration and local validation | Synthetic data only | Relaxed scale, strict no-secrets policy |
| `test` | Integration validation and release rehearsal | Synthetic or masked representative data | CI/CD gates, policy validation, drift checks |
| `prod` | Production reference deployment target | Production-class data controls | Least privilege, HA/DR, monitoring, change approval |

Environment-specific values belong in parameter files and deployment variables, not hard-coded modules.

## Reliability, HA, and DR Principles

- Define workload RTO/RPO before choosing Azure SQL tiers, failover groups, backup retention, or Managed Instance configurations.
- Use zone redundancy and geo-replication where business criticality justifies cost.
- Treat Databricks jobs and pipelines as restartable and observable.
- Keep raw and bronze data immutable enough to support replay.
- Validate database deployment rollback and forward-fix paths.
- Monitor service health, job failures, data freshness, query performance, and cost anomalies.

## Key Decisions and Trade-Offs

Initial decisions are captured in [ADR records](../adr/). The most important early trade-offs are:

- Azure SQL Database vs Managed Instance vs SQL Server on Azure VM.
- Databricks as the lakehouse engineering platform rather than a generic compute sidecar.
- Database-native AI for close-to-data scenarios vs external AI/search for broader retrieval and orchestration.
- Managed identity and Entra-first authentication as the default security posture.
- Bicep as the primary Azure IaC language.

