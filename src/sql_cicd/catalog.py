from __future__ import annotations

# ruff: noqa: E501
from sql_cicd.model import (
    DatabaseTest,
    DriftScenario,
    LifecycleRule,
    ProjectObject,
    PromotionEnvironment,
    ReferenceDataItem,
    RegressionGate,
    ReleaseReadinessItem,
    TraceabilityItem,
)

PROJECT_ROOT = "src/azure_sql/database_project/legacy_tms"

PROJECT_OBJECTS = [
    ProjectObject("obj-001", "schema", "dbo", "dbo", f"{PROJECT_ROOT}/Schemas/dbo.sql", "schema", "database engineering", "configuration defined"),
    ProjectObject("obj-002", "table", "dbo", "CustomerAccount", f"{PROJECT_ROOT}/Tables/dbo.CustomerAccount.sql", "schema", "database engineering", "configuration defined"),
    ProjectObject("obj-003", "table", "dbo", "CustomerAccountAudit", f"{PROJECT_ROOT}/Tables/dbo.CustomerAccountAudit.sql", "schema", "database engineering", "configuration defined"),
    ProjectObject("obj-004", "table", "dbo", "Depot", f"{PROJECT_ROOT}/Tables/dbo.Depot.sql", "schema", "database engineering", "configuration defined"),
    ProjectObject("obj-005", "table", "dbo", "Route", f"{PROJECT_ROOT}/Tables/dbo.Route.sql", "schema", "database engineering", "configuration defined"),
    ProjectObject("obj-006", "table", "dbo", "Vehicle", f"{PROJECT_ROOT}/Tables/dbo.Vehicle.sql", "schema", "database engineering", "configuration defined"),
    ProjectObject("obj-007", "table", "dbo", "Shipment", f"{PROJECT_ROOT}/Tables/dbo.Shipment.sql", "schema", "database engineering", "configuration defined"),
    ProjectObject("obj-008", "table", "dbo", "ShipmentEventHistory", f"{PROJECT_ROOT}/Tables/dbo.ShipmentEventHistory.sql", "schema", "database engineering", "configuration defined"),
    ProjectObject("obj-009", "view", "dbo", "vw_OpenShipmentsByDepot", f"{PROJECT_ROOT}/Views/dbo.vw_OpenShipmentsByDepot.sql", "schema", "database engineering", "configuration defined"),
    ProjectObject("obj-010", "view", "dbo", "vw_CustomerServiceSnapshot", f"{PROJECT_ROOT}/Views/dbo.vw_CustomerServiceSnapshot.sql", "schema", "database engineering", "configuration defined"),
    ProjectObject("obj-011", "stored procedure", "dbo", "usp_CreateShipment", f"{PROJECT_ROOT}/StoredProcedures/dbo.usp_CreateShipment.sql", "schema", "database engineering", "configuration defined"),
    ProjectObject("obj-012", "stored procedure", "dbo", "usp_UpdateShipmentStatus", f"{PROJECT_ROOT}/StoredProcedures/dbo.usp_UpdateShipmentStatus.sql", "schema", "database engineering", "configuration defined"),
    ProjectObject("obj-013", "security", "dbo", "roles and permissions", f"{PROJECT_ROOT}/Security/RolesAndPermissions.sql", "post-deployment", "platform security", "configuration defined"),
    ProjectObject("obj-014", "security", "dbo", "data protection", f"{PROJECT_ROOT}/Security/DataProtection.sql", "post-deployment", "platform security", "configuration defined"),
    ProjectObject("obj-015", "reference data", "dbo", "Depot and Route seed", f"{PROJECT_ROOT}/PostDeployment/ReferenceData.sql", "post-deployment", "database engineering", "deterministic local"),
    ProjectObject("obj-016", "test", "dbo", "static database assertions", f"{PROJECT_ROOT}/Tests/static_schema_tests.sql", "validation", "quality engineering", "static analysis"),
    ProjectObject("obj-017", "schema", "ai", "ai", f"{PROJECT_ROOT}/Schemas/ai.sql", "schema", "database engineering", "configuration defined"),
    ProjectObject("obj-018", "table", "ai", "Document", f"{PROJECT_ROOT}/Tables/ai.Document.sql", "schema", "database engineering", "configuration defined"),
    ProjectObject("obj-019", "table", "ai", "DocumentChunk", f"{PROJECT_ROOT}/Tables/ai.DocumentChunk.sql", "schema", "database engineering", "requires Azure SQL validation"),
    ProjectObject("obj-020", "table", "ai", "EmbeddingMetadata", f"{PROJECT_ROOT}/Tables/ai.EmbeddingMetadata.sql", "schema", "database engineering", "configuration defined"),
    ProjectObject("obj-021", "table", "ai", "RetrievalAudit", f"{PROJECT_ROOT}/Tables/ai.RetrievalAudit.sql", "schema", "database engineering", "configuration defined"),
    ProjectObject("obj-022", "table", "ai", "GenerationAudit", f"{PROJECT_ROOT}/Tables/ai.GenerationAudit.sql", "schema", "database engineering", "configuration defined"),
    ProjectObject("obj-023", "stored procedure", "ai", "usp_AssembleRagContext", f"{PROJECT_ROOT}/StoredProcedures/ai.usp_AssembleRagContext.sql", "schema", "database engineering", "configuration defined"),
    ProjectObject("obj-024", "security", "ai", "AI roles and permissions", f"{PROJECT_ROOT}/Security/AiRolesAndPermissions.sql", "post-deployment", "platform security", "configuration defined"),
    ProjectObject("obj-025", "post-deployment", "dbo", "post deployment orchestration", f"{PROJECT_ROOT}/PostDeployment/PostDeployment.sql", "post-deployment", "database engineering", "configuration defined"),
    ProjectObject("obj-026", "index", "ai", "IX_ai_Document_ShipmentAccount", f"{PROJECT_ROOT}/Indexes/ai.Document.IX_ai_Document_ShipmentAccount.sql", "schema", "database engineering", "configuration defined"),
    ProjectObject("obj-027", "index", "ai", "IX_ai_DocumentChunk_Metadata", f"{PROJECT_ROOT}/Indexes/ai.DocumentChunk.IX_ai_DocumentChunk_Metadata.sql", "schema", "database engineering", "configuration defined"),
    ProjectObject("obj-028", "index", "ai", "IX_ai_EmbeddingMetadata_WorkQueue", f"{PROJECT_ROOT}/Indexes/ai.EmbeddingMetadata.IX_ai_EmbeddingMetadata_WorkQueue.sql", "schema", "database engineering", "configuration defined"),
]

TRACEABILITY = [
    TraceabilityItem("req-001", "Primary OLTP target schema for legacy_tms", "dbo.CustomerAccount; dbo.Shipment; dbo.ShipmentEventHistory", "Tables/*.sql", "database_object_traceability.csv", "schema build required"),
    TraceabilityItem("req-002", "Performance scenario index preserved", "IX_Shipment_Route_Status_CreatedAt", "Tables/dbo.Shipment.sql", "performance_regression_gate.csv", "performance gate required"),
    TraceabilityItem("req-003", "Reference depot and route data is idempotent", "dbo.Depot; dbo.Route", "PostDeployment/ReferenceData.sql", "reference_data_manifest.csv", "reference data manifest required"),
    TraceabilityItem("req-004", "Entra-first least privilege access model", "db roles and grants", "Security/RolesAndPermissions.sql", "security_regression_gate.csv", "security gate required"),
    TraceabilityItem("req-005", "Deployment preview before publish", "dacpac deployment plan", ".github/workflows/sql-cd.yml", "deployment_safety_rules.csv", "preview blocks unsafe release"),
    TraceabilityItem("req-006", "Drift is detected before promotion", "target database model", "scripts/validate_sql_cicd.py", "schema_drift_scenarios.csv", "manual remediation before deployment"),
    TraceabilityItem("req-007", "AI-enabled SQL persistent objects are database-as-code assets", "ai.Document; ai.DocumentChunk; ai.EmbeddingMetadata; ai.RetrievalAudit; ai.GenerationAudit", "src/azure_sql/database_project/legacy_tms/*/ai.*.sql", "outputs/sql_ai/ai_schema_catalog.csv", "SQL AI review required"),
    TraceabilityItem("req-008", "AI metadata indexes remain database-as-code assets", "IX_ai_Document_ShipmentAccount; IX_ai_DocumentChunk_Metadata; IX_ai_EmbeddingMetadata_WorkQueue", "src/azure_sql/database_project/legacy_tms/Indexes/ai.*.sql", "sql_project_inventory.csv", "SQL AI review required"),
]

REFERENCE_DATA = [
    ReferenceDataItem("ref-001", "dbo.Depot", "DepotCode", 4, "post-deployment MERGE", "matched rows are updated, missing rows inserted, deletes are not automatic", f"{PROJECT_ROOT}/PostDeployment/ReferenceData.sql"),
    ReferenceDataItem("ref-002", "dbo.Route", "RouteCode", 5, "post-deployment MERGE", "routes resolve depots by natural keys and avoid identity assumptions", f"{PROJECT_ROOT}/PostDeployment/ReferenceData.sql"),
]

SAFETY_RULES = [
    LifecycleRule("safe-001", "destructive changes", "Block drop table, drop column, data loss, and unreviewed object removal in release preview.", "sqlpackage deploy report and script review", "stop release", "restore point or backup boundary only"),
    LifecycleRule("safe-002", "schema drift", "Compare deployed database to the committed dacpac before publish.", "drift report job", "stop release until drift is classified", "do not auto-overwrite manual hotfixes"),
    LifecycleRule("safe-003", "reference data", "Reference data deployments must be idempotent and natural-key based.", "static test and manifest check", "stop release", "manual data repair script if partial execution occurs"),
    LifecycleRule("safe-004", "permissions", "Security changes require explicit role/grant traceability.", "CODEOWNERS and security regression gate", "require security review", "revoke/grant script under change control"),
    LifecycleRule("safe-005", "environment promotion", "Production publish requires main branch, approved environment, release evidence, and no failed gates.", "GitHub Actions environment gate", "stop release", "previous dacpac plus database backup"),
    LifecycleRule("safe-006", "transaction boundary", "One dacpac release is the rollback unit; data migrations use separate reviewed scripts.", "release manifest", "split release", "roll forward preferred after schema publish"),
    LifecycleRule("safe-007", "AI external model", "External model, provider, endpoint, deployment, or model version changes require SQL AI review.", "SQL AI release evidence and CODEOWNERS review", "require AI/security review", "revert external model definition or disable invocation"),
    LifecycleRule("safe-008", "vector dimensions", "Vector column dimensions, embedding model dimensions, and vector index dimensions must match.", "SQL AI validation and schema review", "stop release", "re-embed chunks and rebuild vector index after approval"),
    LifecycleRule("safe-009", "AI role broadening", "AI roles must not gain broad ownership, unrestricted chunk access, or cross-account retrieval.", "security regression gate", "require security review", "revoke unsafe grants"),
    LifecycleRule("safe-010", "retrieval security", "Retrieval changes must preserve shipment/account/sensitivity/lifecycle authorization filters.", "SQL AI validation and static review", "stop release", "restore previous retrieval procedure"),
    LifecycleRule("safe-011", "AI endpoint changes", "Outbound endpoint URL and REST invocation changes require managed-identity and approved endpoint review.", "deployment safety rules and environment approval", "require AI/security review", "disable external invocation until remediated"),
]

DRIFT_SCENARIOS = [
    DriftScenario("drift-001", "manual hotfix", "Index added directly in production.", "sqlpackage drift/deploy report compared with committed dacpac", "capture, classify, and back-port to project or remove with approval", "not auto-remediated locally"),
    DriftScenario("drift-002", "permission drift", "Ad hoc user granted table access.", "security regression gate plus post-deployment permission query", "revoke or codify through role model", "requires live SQL validation"),
    DriftScenario("drift-003", "reference drift", "Depot name changed directly in target.", "reference data checksum/manifest review", "confirm authoritative source then update project seed or target", "no automatic delete"),
    DriftScenario("drift-004", "breaking column change", "Column length altered outside the project.", "dacpac model comparison", "block release and run compatibility review", "manual DBA review"),
]

PROMOTION_MATRIX = [
    PromotionEnvironment("local", "developer command", "none", "build and static validation only", "synthetic data only", "release_manifest.json"),
    PromotionEnvironment("dev", "feature branch or workflow_dispatch", "pull request review", "deploy report, script preview, optional publish", "non-production data", "dacpac, deploy report, test catalog"),
    PromotionEnvironment("test", "main branch workflow_dispatch", "database owner approval", "publish after drift review", "masked or synthetic test data", "signed release manifest and regression gates"),
    PromotionEnvironment("prod", "main branch workflow_dispatch", "protected environment approval", "manual approval then publish", "production controls required", "approved deploy report, backup/restore point, manifest"),
]

DATABASE_TESTS = [
    DatabaseTest("test-001", "static schema", "legacy_tms.sqlproj", "SQL project exists and uses Microsoft.Build.Sql SDK.", "local CI", "yes"),
    DatabaseTest("test-002", "static schema", "tables", "Required OLTP tables are declared as database-as-code assets.", "local CI", "yes"),
    DatabaseTest("test-003", "static schema", "stored procedures", "Procedure assets are represented in the project.", "local CI", "yes"),
    DatabaseTest("test-004", "reference data", "PostDeployment/ReferenceData.sql", "Reference MERGE statements are idempotent and natural-key based.", "local CI", "yes"),
    DatabaseTest("test-005", "deployment safety", "deployment_safety_rules.csv", "Unsafe release classes have explicit stop actions.", "local CI", "yes"),
    DatabaseTest("test-006", "drift", "schema_drift_scenarios.csv", "Manual and security drift scenarios are documented.", "local CI", "yes"),
    DatabaseTest("test-007", "integration", "dacpac build", "dotnet build creates a dacpac when SDK restore is available.", "developer or CI runner", "tooling dependent"),
    DatabaseTest("test-008", "AI guardrail", "outputs/sql_ai/sql_ai_readiness.csv", "SQL AI vector, model, role, endpoint, and retrieval-security changes have evidence classifications.", "local CI", "yes"),
]

PERFORMANCE_GATES = [
    RegressionGate("perf-001", "query duration", "Milestone 7 baseline by workload", "no critical OLTP workload worsens beyond 20 percent without waiver", "outputs/sql_performance/performance_baseline.csv", "block promotion"),
    RegressionGate("perf-002", "logical reads", "Query Store or deterministic baseline", "no high-criticality workload increases reads beyond 25 percent without mitigation", "Query Store after Azure validation", "block production"),
    RegressionGate("perf-003", "index drift", "target schema indexes", "required customer/status and route/status indexes remain present", "sql_project_inventory.csv", "block promotion"),
]

SECURITY_GATES = [
    RegressionGate("sec-001", "least privilege", "role/grant script", "application roles have execute/select access only through approved objects", "Security/RolesAndPermissions.sql", "block promotion"),
    RegressionGate("sec-002", "data protection", "table masking definition and classification script", "customer email and memo fields retain protection controls", "Tables/dbo.CustomerAccount.sql; Security/DataProtection.sql", "block promotion"),
    RegressionGate("sec-003", "secret handling", "workflow definitions", "no connection string or password is committed", ".github/workflows/*.yml", "block promotion"),
    RegressionGate("sec-004", "AI retrieval security", "SQL AI retrieval assets", "metadata filters and sensitivity/lifecycle controls remain present before ranking", "outputs/sql_ai/ai_security_matrix.csv", "block promotion"),
    RegressionGate("sec-005", "AI endpoint governance", "external model and REST endpoint definitions", "endpoint changes use managed identity placeholders and no committed secrets", "src/azure_sql/ai/embeddings/create_external_model_example.sql", "block promotion"),
]

RELEASE_READINESS = [
    ReleaseReadinessItem("ready-001", "schema", "SDK-style SQL project is present.", "ready", "legacy_tms.sqlproj", "Azure publish deferred"),
    ReleaseReadinessItem("ready-002", "build", "Dacpac can be built when dotnet restore is available.", "tooling dependent", "scripts/build_sql_project.py", "local environment may lack dotnet/sqlpackage"),
    ReleaseReadinessItem("ready-003", "reference data", "Reference data manifest and post-deployment script are deterministic.", "ready", "reference_data_manifest.csv", "no production data deployment"),
    ReleaseReadinessItem("ready-004", "drift", "Drift scenarios and release stop rules are defined.", "ready", "schema_drift_scenarios.csv", "live drift query requires Azure SQL MI"),
    ReleaseReadinessItem("ready-005", "security", "Security regression gates require least privilege and data-protection review.", "ready", "security_regression_gate.csv", "principal binding remains environment specific"),
    ReleaseReadinessItem("ready-006", "promotion", "Environment promotion matrix separates local, dev, test, and prod.", "ready", "environment_promotion_matrix.csv", "actual approvals configured in GitHub environments"),
    ReleaseReadinessItem("ready-007", "SQL AI", "External model, vector dimension, vector index, endpoint, AI role, and retrieval-security guardrails are defined.", "ready", "outputs/sql_ai/sql_ai_readiness.csv", "runtime validation remains Azure SQL and Azure OpenAI dependent"),
]
