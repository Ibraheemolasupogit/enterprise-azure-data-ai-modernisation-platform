# Target-State Architecture Report

Milestone 4 formalises the implementation-ready target architecture for Contoso Freight. It does not deploy Azure resources, implement migration, build Databricks pipelines, or implement AI search/RAG.

## Target Architecture Planes

- Operational data plane: Azure SQL Managed Instance for `legacy_tms` and Azure Database for PostgreSQL Flexible Server for `billing_ops`.
- Data engineering / analytical plane: Azure Databricks, ADLS Gen2, Delta Lake, Bronze/Silver/Gold, Unity Catalog, batch, CDC, and streaming design boundaries.
- AI-enabled data plane: future boundary for Azure SQL native AI/vector features, embeddings, hybrid search, Azure OpenAI, RAG, and secure API/MCP integration.
- Control / security / operations plane: Entra ID, managed identities, Key Vault, private networking, Azure Monitor, Log Analytics, CI/CD, IaC, audit, and governance controls.

## Azure Services

- ADLS Gen2
- Azure Database for PostgreSQL Flexible Server
- Azure Databricks
- Azure Key Vault
- Azure Monitor, Log Analytics, Application Insights
- Azure SQL AI capabilities; Azure AI Search; Azure OpenAI
- Azure SQL Managed Instance
- Azure VNet, Private Link, private endpoints, Private DNS
- Bicep and GitHub Actions
- Microsoft Entra ID and managed identities
- Unity Catalog

## Operational Database Decisions

- Azure SQL Managed Instance remains the initial target for `legacy_tms` because stored procedures, SQL Server compatibility risk, instance-level unknowns, networking constraints, and low downtime tolerance make Azure SQL Database a later optimisation rather than the first migration target.
- The decision would change toward Azure SQL Database if live discovery proves no instance-level dependencies, acceptable procedure compatibility, no cross-database assumptions, and lower operational complexity. It would change toward SQL Server on Azure VM only if hard unsupported dependencies require OS/instance control.
- Azure Database for PostgreSQL Flexible Server is the target for `billing_ops` because the source is PostgreSQL-like and engine conversion to Azure SQL is not currently justified.

## Databricks and Storage Design

- Databricks owns batch, CDC/incremental, streaming/event ingestion, data quality, medallion processing, and analytical offload.
- ADLS Gen2 stores landing/raw, bronze, silver, gold, checkpoints, schema metadata, quarantine, and audit/evidence zones.
- Unity Catalog governs lakehouse catalogs, schemas, grants, lineage, and the managed-vs-external table boundary.
- Job compute is preferred for production pipelines; interactive compute remains a development concern. Serverless/classic choices require region, policy, and workload validation.

## Networking and Identity

- Production target architecture prefers private data-plane connectivity using VNet segmentation, private endpoints, Private DNS, and restricted administrative paths.
- Portfolio/dev implementation may simplify access while preserving the production architecture decision in documentation and IaC structure.
- Identity is Entra-first with managed identities for workloads, federated CI/CD identity, database groups/users, Databricks service identities, and least-privilege storage/Key Vault access.

## HA/DR

- Critical transport OLTP assumes RTO 60 minutes and RPO 15 minutes.
- Billing/service assumes RTO 240 minutes and RPO 60 minutes.
- Analytical processing assumes restartable jobs, replayable sources, and RTO/RPO tiers aligned to data freshness requirements.
- DR is not tested in Milestone 4.

## Assumptions Requiring Live Validation

- SQL MI compute/storage sizing, collation, SQL Agent dependencies, and production workload telemetry.
- PostgreSQL connection profile, write pattern, month-end billing workload, storage growth, and HA requirements.
- Corporate DNS, firewall, routing, private endpoint, and administrative-access constraints.
- Databricks compute mode, Lakeflow fit, workload concurrency, and serverless availability.
- Regulatory need for customer-managed keys and exact audit/log retention.
