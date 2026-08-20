# Architecture Decision Records

ADRs capture decisions that shape the platform. Use the template in [template.md](template.md) for future records.

| ADR | Status | Decision |
| --- | --- | --- |
| [0001](0001-azure-sql-target-options.md) | Accepted | Use workload-specific SQL modernisation target selection |
| [0002](0002-databricks-lakehouse-role.md) | Accepted | Use Databricks for lakehouse engineering and governed analytical processing |
| [0003](0003-database-native-ai-vs-external-ai-search.md) | Accepted | Separate database-native AI from external AI/search orchestration |
| [0004](0004-managed-identity-entra-first.md) | Accepted | Prefer managed identity and Entra-first authentication |
| [0005](0005-bicep-infrastructure-as-code.md) | Accepted | Use Bicep as the default Azure IaC approach |
| [0006](0006-azure-sql-vs-postgresql-disposition.md) | Accepted | Keep Azure SQL and PostgreSQL dispositions source-specific |
| [0007](0007-relational-vs-cosmos-db-disposition.md) | Accepted | Do not select Cosmos DB without a proven document-serving workload |
| [0008](0008-retain-vs-migrate-and-migration-ordering.md) | Accepted | Use staged waves and deliberate temporary retention |
| [0009](0009-adls-delta-medallion-architecture.md) | Accepted | Use ADLS Gen2 and Delta medallion zones |
| [0010](0010-databricks-table-boundaries-and-ingestion-modes.md) | Accepted | Define Databricks table boundaries and ingestion modes |
| [0011](0011-private-networking-target-architecture.md) | Accepted | Use private networking as production target architecture |
| [0012](0012-ha-dr-and-environment-isolation.md) | Accepted | Use tiered HA/DR and isolated environments |
