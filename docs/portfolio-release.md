# Portfolio Release

This repository demonstrates an end-to-end enterprise Azure Data & AI modernisation platform for a fictional logistics company. It is designed for technical review of architecture, implementation assets, deterministic evidence, and assurance controls. It is not a live deployment package and it does not claim production runtime validation.

## What It Demonstrates

- Estate assessment and migration planning.
- Azure SQL target design, operations, performance engineering, database-as-code, and CI/CD guardrails.
- Databricks platform foundation, Unity Catalog, medallion ingestion, Gold products, data quality, Lakeflow Jobs orchestration, monitoring, troubleshooting, and FinOps controls.
- AI-enabled SQL, vector/full-text/hybrid retrieval, SQL-native RAG, and grounded response boundaries.
- Secure API integration using Data API Builder, REST, GraphQL, MCP-compatible contracts, and Container Apps architecture.
- Microsoft Fabric downstream integration boundary without implementing Fabric resources.
- Final assurance over architecture, security, identity, governance, resilience, observability, FinOps, CI/CD, and release readiness.

## How To Review

Start with:

- `README.md` for the portfolio overview and navigation.
- `docs/roadmap.md` for milestone coverage.
- `reports/final_assurance_report.md` for final assurance summary.
- `outputs/final_assurance/release_manifest.json` for machine-readable release metadata.
- `outputs/final_assurance/capability_inventory.csv` for the capability inventory.
- `outputs/final_assurance/implementation_truth_matrix.csv` for implementation truthfulness.
- `outputs/final_assurance/production_gap_register.csv` for remaining runtime validation gaps.

Then inspect the relevant domain evidence under `outputs/` and reports under `reports/`.

## Architecture Decisions

The platform keeps Azure SQL responsible for operational relational workloads, Databricks responsible for governed analytical engineering, SQL AI close to operational data where appropriate, API integration explicitly allowlisted, and Fabric as a downstream consumer of governed Gold products rather than a duplicate transformation owner.

## Limitations

No Azure, Databricks, Fabric, Azure OpenAI, Container Apps, or Data API Builder runtime deployment is performed locally. Backup/restore drills, DR failover, performance under load, vector runtime, generation calls, API smoke tests, Fabric shortcuts, and production identity bindings require cloud validation.

## Optional Live Deployment Path

A live deployment would require approved Azure/Fabric subscriptions and tenants, environment-specific parameterization, managed identity and Entra group binding, private networking, secret storage in Key Vault or platform equivalents, Databricks workspace validation, SQL dacpac deployment, API/DAB smoke tests, Fabric shortcut validation, telemetry wiring, DR drills, and environment approvals.

