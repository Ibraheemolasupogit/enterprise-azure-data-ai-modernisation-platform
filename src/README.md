# Source Areas

This directory is split by platform responsibility so future milestones can add implementation without mixing operational SQL, lakehouse, AI, governance, and observability concerns.

| Area | Responsibility |
| --- | --- |
| `azure_sql/` | SQL schemas, migrations, performance tuning, security, automation, HA/DR |
| `databricks/` | Jobs, notebooks, Lakeflow, Unity Catalog, Delta optimisation |
| `data_engineering/` | Ingestion, CDC, streaming, medallion logic, data quality |
| `ai/` | SQL AI, embeddings, vector/hybrid search, RAG |
| `security_governance/` | RBAC, policy, lineage, classification, audit controls |
| `observability/` | Monitoring, SLOs, alerts, FinOps |

