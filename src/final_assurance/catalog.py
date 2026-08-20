from __future__ import annotations

# ruff: noqa: E501

CAPABILITIES = [
    ("cap-001", "assessment", "Legacy estate assessment", "implemented locally", "outputs/database_estate_inventory.csv", "locally validated", "architecture and migration team", "none for local evidence", "live discovery would require customer estate access"),
    ("cap-002", "architecture", "Target-state architecture", "implemented locally", "outputs/architecture/architecture_traceability.csv", "locally validated", "architecture team", "cloud validation for deployment", "private networking and HA/DR require Azure validation"),
    ("cap-003", "migration", "Migration factory", "implemented locally", "outputs/migration/migration_manifest.csv", "locally validated", "migration team", "source/target connectivity", "production cutover requires live rehearsal"),
    ("cap-004", "Azure SQL", "SQL MI target, operations, performance and CI/CD", "configuration defined", "outputs/sql_cicd/release_readiness.csv", "requires Azure validation", "database platform team", "Azure SQL Managed Instance", "runtime build/deploy/performance validation remains required"),
    ("cap-005", "PostgreSQL target", "Secondary billing target schema", "configuration defined", "src/data_engineering/secondary_sources/postgres_billing/target_flexible_server_schema.sql", "requires Azure validation", "database platform team", "Azure Database for PostgreSQL", "sizing and live migration remain open"),
    ("cap-006", "Databricks", "Platform foundation and Unity Catalog", "configuration defined", "outputs/databricks_foundation/platform_readiness.csv", "requires Databricks validation", "data platform team", "Databricks workspace", "bundle and runtime validation remain required"),
    ("cap-007", "pipelines", "Medallion ingestion and Gold products", "implemented locally", "outputs/databricks_pipelines/pipeline_readiness.csv", "locally validated", "data engineering team", "Databricks runtime", "production job execution remains required"),
    ("cap-008", "data quality", "Quality gates and orchestration", "implemented locally", "outputs/databricks_orchestration/orchestration_readiness.csv", "locally validated", "data quality owner", "Databricks expectations/jobs", "runtime expectations remain required"),
    ("cap-009", "operations", "Databricks monitoring and FinOps", "configuration defined", "outputs/databricks_operations/operations_readiness.csv", "requires Databricks validation", "operations team", "Databricks system tables", "live telemetry remains required"),
    ("cap-010", "AI-enabled SQL", "Vector/full-text/hybrid retrieval and SQL-native RAG", "configuration defined", "outputs/sql_ai/sql_ai_readiness.csv", "requires Azure validation", "AI/data platform team", "Azure SQL AI and Azure OpenAI", "real embeddings/generation not executed locally"),
    ("cap-011", "API integration", "DAB, REST, GraphQL and MCP boundary", "configuration defined", "outputs/application_integration/integration_readiness.csv", "requires application runtime validation", "application integration team", "Container Apps/DAB runtime", "live API runtime validation remains required"),
    ("cap-012", "Fabric boundary", "Fabric downstream handoff contract", "configuration defined", "outputs/fabric_integration/fabric_integration_readiness.csv", "requires Fabric validation", "Azure producer and Fabric consumer teams", "Fabric runtime", "Fabric shortcuts/interoperability require validation"),
    ("cap-013", "IaC", "Bicep modules and switch-gated root template", "configuration defined", "infra/main.bicep", "configuration defined", "platform engineering", "Azure deployment tooling", "Bicep build optional based on local tooling"),
    ("cap-014", "CI/CD", "Repository validation and SQL release workflows", "implemented locally", ".github/workflows/ci.yml", "locally validated", "DevSecOps team", "GitHub Actions", "cloud deployment approval remains manual"),
    ("cap-015", "security", "Entra-first least privilege and data controls", "configuration defined", "outputs/final_assurance/security_assurance_matrix.csv", "configuration defined", "security team", "Azure/Databricks/Fabric runtime", "runtime permission validation remains required"),
    ("cap-016", "observability", "Monitoring, alert and runbook coverage", "configuration defined", "outputs/final_assurance/observability_assurance.csv", "configuration defined", "operations team", "live telemetry sources", "alerts require cloud telemetry"),
    ("cap-017", "resilience", "HA/DR and recovery posture", "configuration defined", "outputs/final_assurance/resilience_assurance.csv", "requires Azure validation", "operations team", "cloud failover/restore drills", "DR not tested locally"),
    ("cap-018", "FinOps", "Cost-driver and optimization controls", "configuration defined", "outputs/final_assurance/finops_assurance.csv", "configuration defined", "FinOps owner", "runtime billing/usage telemetry", "no currency values claimed"),
]

DATA_PRODUCTS = [
    ("shipment operations", "legacy_tms", "bronze.legacy_tms_changes", "silver.shipments", "gold.shipment_operations_performance", "outputs/databricks_orchestration/quality_results.csv", "Unity Catalog + regional controls", "operational analytics; Fabric boundary", "outputs/databricks_pipelines/pipeline_traceability.csv"),
    ("depot/route performance", "legacy_tms; depot_reference_feed", "bronze.depot_reference_feed", "silver.depots_routes", "gold.depot_route_performance", "outputs/databricks_orchestration/quality_results.csv", "regional row filters", "Fabric route analytics", "outputs/fabric_integration/lineage_handoff.csv"),
    ("delivery delays", "shipment_operational_events; carrier_updates", "bronze.shipment_operational_events", "silver.shipment_events", "gold.delivery_delay_metrics", "outputs/databricks_orchestration/quality_results.csv", "no direct PII", "SLA/delay analytics; Fabric", "outputs/fabric_integration/fabric_data_contracts.csv"),
    ("billing/revenue", "billing_ops", "bronze.billing_ops_invoices", "silver.billing_invoices", "gold.billing_revenue_summary", "outputs/databricks_pipelines/quarantine_rules.csv", "financial confidential", "finance analytics; controlled Fabric copy by exception", "outputs/fabric_integration/sensitivity_handoff.csv"),
    ("service/incident", "customer_service_export", "bronze.customer_service_export", "silver.service_cases", "gold.service_incident_summary", "outputs/databricks_orchestration/quality_results.csv", "case detail excluded", "service trend analytics", "outputs/fabric_integration/fabric_data_product_catalog.csv"),
    ("AI grounding corpus", "curated operational sources", "not exposed as Bronze", "AI-ready source projection", "ai.DocumentChunk", "outputs/sql_ai/retrieval_evaluation_results.csv", "retrieval authorization and sensitivity filters", "SQL-native RAG/API AI endpoint", "outputs/sql_ai/rag_context_contract.csv"),
]

SECURITY_CONTROLS = [
    ("Entra ID", "identity provider for users/workloads", "configuration defined", "runtime token validation required", "incorrect group mapping", "docs/application-api-integration.md"),
    ("managed identities", "API/SQL/embedding/runtime identities separated", "configuration defined", "Azure validation required", "over-broad identity grants", "outputs/application_integration/api_authorization_matrix.csv"),
    ("GitHub OIDC", "deployment identity pattern without stored cloud secrets", "configuration defined", "GitHub/Azure validation required", "environment approval misconfiguration", ".github/workflows/sql-cd.yml"),
    ("database roles", "least-privilege SQL roles", "configuration defined", "Azure SQL validation required", "permission drift", "src/azure_sql/database_project/legacy_tms/Security"),
    ("Unity Catalog permissions", "catalog/schema/table grants and governance", "configuration defined", "Databricks validation required", "workspace/group drift", "src/databricks/unity_catalog/sql/03_security_governance.sql"),
    ("API authorization", "allowlisted DAB/API roles", "locally validated", "application runtime validation required", "missing role claim mapping", "outputs/application_integration/api_authorization_matrix.csv"),
    ("RLS/masking/classification", "sensitive data controls", "configuration defined", "Azure/Databricks validation required", "incomplete policy binding", "outputs/azure_sql_operations/sensitive_data_controls.csv"),
    ("Key Vault boundary", "secret storage boundary, no committed secrets", "configuration defined", "Azure validation required", "mis-scoped secret access", "infra/modules/azure-sql/managed-instance.bicep"),
    ("private networking", "private SQL/storage/platform access", "configuration defined", "Azure validation required", "public exposure", "docs/architecture/security-governance.md"),
    ("retrieval authorization", "AI context filtered by caller authorization", "locally validated", "Azure/application validation required", "cross-customer context leakage", "outputs/sql_ai/ai_security_matrix.csv"),
    ("MCP allowlisting", "fixed tool catalog with schemas", "locally validated", "application runtime validation required", "tool overreach", "outputs/application_integration/mcp_security_matrix.csv"),
]

FAILURE_MODES = [
    ("Azure SQL outage", "operational apps and SQL AI unavailable", "Azure Monitor/SQL alerts", "failover/restore runbook", "backup/restore or failover", "database platform team", "docs/runbooks/sqlmi-database-unavailable.md"),
    ("PostgreSQL outage", "billing target unavailable", "database health alerts", "restore/failover per target design", "restore or reconnect", "database platform team", "docs/runbooks/billing-ops-cutover.md"),
    ("Databricks job failure", "pipeline delay", "job failure queries/alerts", "retry/remediate job", "controlled replay", "data platform team", "docs/runbooks/databricks-job-failure.md"),
    ("streaming lag", "event freshness breach", "streaming health rules", "scale/restart/replay", "checkpoint recovery", "data platform team", "docs/runbooks/databricks-streaming-lag.md"),
    ("schema drift", "contract break or quarantine", "schema drift validator", "classify and remediate", "schema evolution/replay", "data engineering team", "docs/runbooks/schema-drift-remediation.md"),
    ("data-quality failure", "publication blocked", "quality gate failures", "quarantine/remediate", "reprocess from valid source", "data quality owner", "docs/runbooks/data-quality-failure.md"),
    ("storage access failure", "pipeline or Fabric handoff blocked", "storage/dependency errors", "repair RBAC/ACL/network", "restore access", "platform team", "docs/runbooks/databricks-failed-ingestion-job.md"),
    ("Azure OpenAI unavailable", "AI answer generation unavailable", "AI dependency failure status", "return grounded unavailable response", "retry after provider recovery", "AI platform team", "docs/runbooks/sql-ai-azure-openai-invocation-failure.md"),
    ("API unavailable", "client integration failure", "Application Insights requests", "restart/rollback API revision", "previous container revision", "application integration team", "docs/application-api-integration.md"),
    ("authentication failure", "users/workloads blocked", "401/403 telemetry", "validate Entra/app role mapping", "restore identity config", "security team", "docs/runbooks/sqlmi-authentication-failure.md"),
    ("Fabric handoff failure", "downstream analytics stale", "quality/handoff manifest status", "coordinate producer/consumer fix", "last valid version or repaired shortcut", "shared Azure/Fabric owners", "docs/fabric-integration-boundary.md"),
    ("CI/CD failure", "release blocked", "GitHub Actions", "repair validation/dependency", "rerun after fix", "DevSecOps team", "docs/runbooks/deployment-rollback.md"),
    ("secret/configuration failure", "security/release block", "secret check/config validator", "rotate/remove and audit", "reissue credentials externally", "security team", "outputs/final_assurance/security_assurance_matrix.csv"),
]
