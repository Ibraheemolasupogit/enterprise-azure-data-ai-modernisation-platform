from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_PATHS = [
    ".editorconfig",
    ".gitignore",
    ".github/workflows/ci.yml",
    ".github/workflows/sql-cd.yml",
    ".github/CODEOWNERS",
    ".pre-commit-config.yaml",
    "Makefile",
    "README.md",
    "pyproject.toml",
    "infra/main.bicep",
    "infra/parameters/dev.bicepparam",
    "infra/parameters/test.bicepparam",
    "infra/parameters/prod.bicepparam",
    "src/azure_sql/README.md",
    "src/databricks/README.md",
    "src/data_engineering/README.md",
    "src/ai/README.md",
    "src/security_governance/README.md",
    "src/observability/README.md",
    "src/legacy_estate/generator.py",
    "src/legacy_estate/workload.py",
    "src/legacy_estate/contracts.py",
    "src/estate_assessment/cli.py",
    "src/estate_assessment/rules.py",
    "src/estate_assessment/inventory.py",
    "src/estate_assessment/validation.py",
    "src/target_architecture/cli.py",
    "src/target_architecture/catalog.py",
    "src/target_architecture/model.py",
    "src/target_architecture/validation.py",
    "src/migration_factory/cli.py",
    "src/migration_factory/catalog.py",
    "src/migration_factory/execution.py",
    "src/migration_factory/model.py",
    "src/migration_factory/validation.py",
    "src/azure_sql_operations/cli.py",
    "src/azure_sql_operations/catalog.py",
    "src/azure_sql_operations/model.py",
    "src/azure_sql_operations/validation.py",
    "src/sql_performance/cli.py",
    "src/sql_performance/catalog.py",
    "src/sql_performance/model.py",
    "src/sql_performance/validation.py",
    "src/sql_cicd/cli.py",
    "src/sql_cicd/catalog.py",
    "src/sql_cicd/model.py",
    "src/sql_cicd/validation.py",
    "scripts/validate_sql_cicd.py",
    "scripts/build_sql_project.py",
    "scripts/test_sql_project.py",
    "src/azure_sql/database_project/legacy_tms/legacy_tms.sqlproj",
    "src/azure_sql/database_project/legacy_tms/README.md",
    "src/azure_sql/database_project/legacy_tms/Schemas/dbo.sql",
    "src/azure_sql/database_project/legacy_tms/Tables/dbo.CustomerAccount.sql",
    "src/azure_sql/database_project/legacy_tms/Tables/dbo.Shipment.sql",
    "src/azure_sql/database_project/legacy_tms/Tables/dbo.ShipmentEventHistory.sql",
    "src/azure_sql/database_project/legacy_tms/Views/dbo.vw_OpenShipmentsByDepot.sql",
    "src/azure_sql/database_project/legacy_tms/StoredProcedures/dbo.usp_CreateShipment.sql",
    "src/azure_sql/database_project/legacy_tms/StoredProcedures/dbo.usp_UpdateShipmentStatus.sql",
    "src/azure_sql/database_project/legacy_tms/Security/RolesAndPermissions.sql",
    "src/azure_sql/database_project/legacy_tms/Security/DataProtection.sql",
    "src/azure_sql/database_project/legacy_tms/PreDeployment/PreDeployment.sql",
    "src/azure_sql/database_project/legacy_tms/PostDeployment/ReferenceData.sql",
    "src/azure_sql/database_project/legacy_tms/Tests/static_schema_tests.sql",
    "infra/modules/azure-sql/managed-instance.bicep",
    "src/azure_sql/operations/security/01_roles_and_permissions.sql",
    "src/azure_sql/operations/security/02_data_protection.sql",
    "src/azure_sql/operations/agent_jobs/01_integrity_check_job.sql",
    "src/azure_sql/operations/agent_jobs/02_statistics_maintenance_job.sql",
    "src/azure_sql/operations/kql/sqlmi_resource_health.kql",
    "src/azure_sql/performance/query_store/01_configure_query_store.sql",
    "src/azure_sql/performance/query_store/02_diagnostics.sql",
    "src/azure_sql/performance/dmv/query_performance.sql",
    "src/azure_sql/performance/indexing/01_reporting_index_scenario.sql",
    "src/azure_sql/performance/statistics/02_targeted_update_statistics.sql",
    "src/azure_sql/performance/blocking/blocking_scenarios.sql",
    "src/azure_sql/performance/deadlock/deadlock_xevent.sql",
    "src/azure_sql/performance/parameter_sensitivity/customer_summary_by_tier.sql",
    "src/azure_sql/legacy_oltp/sqlserver/01_tables.sql",
    "src/azure_sql/legacy_oltp/sqlserver/02_constraints.sql",
    "src/azure_sql/legacy_oltp/sqlserver/03_indexes.sql",
    "src/azure_sql/legacy_oltp/sqlserver/04_views.sql",
    "src/azure_sql/legacy_oltp/sqlserver/05_stored_procedures.sql",
    "src/azure_sql/legacy_oltp/sqlserver/07_workload_queries.sql",
    "src/azure_sql/target_sqlmi/01_tables.sql",
    "src/azure_sql/target_sqlmi/02_constraints_indexes.sql",
    "src/azure_sql/target_sqlmi/03_stored_procedures.sql",
    "src/data_engineering/secondary_sources/postgres_billing/schema.sql",
    "src/data_engineering/secondary_sources/postgres_billing/target_flexible_server_schema.sql",
    "docs/architecture/overview.md",
    "docs/architecture/data-flows.md",
    "docs/architecture/security-governance.md",
    "docs/architecture/environments.md",
    "docs/roadmap.md",
    "docs/synthetic-data-strategy.md",
    "docs/legacy-estate.md",
    "docs/estate-assessment.md",
    "docs/target-state-architecture.md",
    "docs/migration-factory.md",
    "docs/azure-sql-operations.md",
    "docs/sql-performance-engineering.md",
    "docs/sql-database-lifecycle.md",
    "docs/runbooks/README.md",
    "docs/runbooks/sql-database-release-rollback.md",
    "docs/runbooks/schema-drift-remediation.md",
    "docs/adr/README.md",
    "docs/adr/template.md",
    "docs/adr/0006-azure-sql-vs-postgresql-disposition.md",
    "docs/adr/0007-relational-vs-cosmos-db-disposition.md",
    "docs/adr/0008-retain-vs-migrate-and-migration-ordering.md",
    "docs/adr/0009-adls-delta-medallion-architecture.md",
    "docs/adr/0010-databricks-table-boundaries-and-ingestion-modes.md",
    "docs/adr/0011-private-networking-target-architecture.md",
    "docs/adr/0012-ha-dr-and-environment-isolation.md",
    "tests/test_foundation.py",
    "tests/test_legacy_estate.py",
    "tests/test_estate_assessment.py",
    "tests/test_migration_factory.py",
    "tests/test_sql_performance.py",
    "scripts/validate_assessment.py",
    "scripts/validate_architecture.py",
    "scripts/validate_migration.py",
    "scripts/validate_azure_sql_operations.py",
    "scripts/validate_sql_performance.py",
    "data/README.md",
    "data/schemas/README.md",
    "data/contracts/shipment_operational_event.schema.json",
    "data/contracts/depot_reference_feed.schema.json",
    "data/contracts/carrier_update.schema.json",
    "data/samples/legacy_estate/tiny/manifest.json",
    "data/samples/legacy_estate/tiny/workload.jsonl",
    "outputs/database_estate_inventory.csv",
    "outputs/estate_dependencies.csv",
    "outputs/compatibility_assessment.csv",
    "outputs/workload_classification.csv",
    "outputs/target_service_decisions.csv",
    "outputs/migration_complexity.csv",
    "outputs/migration_wave_plan.csv",
    "outputs/modernisation_risk_register.csv",
    "reports/estate_assessment_report.md",
    "outputs/architecture/workload_target_matrix.csv",
    "outputs/architecture/security_control_matrix.csv",
    "outputs/architecture/recovery_strategy_matrix.csv",
    "outputs/architecture/architecture_traceability.csv",
    "outputs/architecture/environment_matrix.csv",
    "outputs/architecture/assumption_register.csv",
    "outputs/architecture/target_component_catalog.csv",
    "reports/target_architecture_report.md",
    "outputs/migration/migration_manifest.csv",
    "outputs/migration/compatibility_remediation.csv",
    "outputs/migration/schema_conversion_report.csv",
    "outputs/migration/data_reconciliation.csv",
    "outputs/migration/validation_gates.csv",
    "outputs/migration/migration_wave_execution.csv",
    "outputs/migration/cutover_readiness.csv",
    "outputs/migration/rollback_readiness.csv",
    "outputs/migration/tool_integration_points.csv",
    "outputs/migration/failure_scenarios.csv",
    "reports/migration_factory_report.md",
    "outputs/azure_sql_operations/configuration_baseline.csv",
    "outputs/azure_sql_operations/security_role_matrix.csv",
    "outputs/azure_sql_operations/sensitive_data_controls.csv",
    "outputs/azure_sql_operations/monitoring_catalog.csv",
    "outputs/azure_sql_operations/alert_catalog.csv",
    "outputs/azure_sql_operations/automation_catalog.csv",
    "outputs/azure_sql_operations/backup_restore_readiness.csv",
    "outputs/azure_sql_operations/ha_dr_readiness.csv",
    "outputs/azure_sql_operations/operational_readiness.csv",
    "reports/azure_sql_operations_report.md",
    "outputs/sql_performance/workload_catalog.csv",
    "outputs/sql_performance/performance_baseline.csv",
    "outputs/sql_performance/query_analysis.csv",
    "outputs/sql_performance/index_recommendations.csv",
    "outputs/sql_performance/statistics_strategy.csv",
    "outputs/sql_performance/blocking_scenarios.csv",
    "outputs/sql_performance/deadlock_readiness.csv",
    "outputs/sql_performance/parameter_sensitivity.csv",
    "outputs/sql_performance/performance_regression_controls.csv",
    "outputs/sql_performance/performance_assurance.csv",
    "reports/sql_performance_report.md",
    "outputs/sql_cicd/sql_project_inventory.csv",
    "outputs/sql_cicd/database_object_traceability.csv",
    "outputs/sql_cicd/reference_data_manifest.csv",
    "outputs/sql_cicd/deployment_safety_rules.csv",
    "outputs/sql_cicd/schema_drift_scenarios.csv",
    "outputs/sql_cicd/environment_promotion_matrix.csv",
    "outputs/sql_cicd/database_test_catalog.csv",
    "outputs/sql_cicd/performance_regression_gate.csv",
    "outputs/sql_cicd/security_regression_gate.csv",
    "outputs/sql_cicd/release_readiness.csv",
    "outputs/sql_cicd/release_manifest.json",
    "reports/sql_cicd_report.md",
]

REQUIRED_DIRECTORIES = [
    "infra/modules",
    "infra/scripts",
    "src/azure_sql",
    "src/databricks",
    "src/data_engineering",
    "src/ai",
    "src/security_governance",
    "src/observability",
    "src/legacy_estate",
    "src/estate_assessment",
    "src/target_architecture",
    "src/migration_factory",
    "src/azure_sql_operations",
    "src/sql_performance",
    "src/sql_cicd",
    "src/azure_sql/operations/security",
    "src/azure_sql/operations/agent_jobs",
    "src/azure_sql/operations/kql",
    "src/azure_sql/performance",
    "src/azure_sql/performance/query_store",
    "src/azure_sql/performance/dmv",
    "src/azure_sql/database_project",
    "src/azure_sql/database_project/legacy_tms",
    "src/azure_sql/database_project/legacy_tms/Tables",
    "src/azure_sql/database_project/legacy_tms/PostDeployment",
    "src/azure_sql/legacy_oltp/sqlserver",
    "src/azure_sql/target_sqlmi",
    "src/data_engineering/secondary_sources/postgres_billing",
    "docs/architecture",
    "docs/adr",
    "docs/runbooks",
    "data/raw",
    "data/interim",
    "data/processed",
    "data/schemas",
    "data/contracts",
    "data/samples/legacy_estate/tiny",
    "outputs",
    "outputs/architecture",
    "outputs/migration",
    "outputs/azure_sql_operations",
    "outputs/sql_performance",
    "outputs/sql_cicd",
    "reports",
    "tests",
]

REQUIRED_README_TERMS = [
    "enterprise Azure Data and AI modernisation",
    "Milestone 1",
    "Milestone 2",
    "Milestone 3",
    "Milestone 4",
    "Milestone 5",
    "Milestone 6",
    "Milestone 7",
    "Milestone 8",
    "does not deploy Azure resources",
    "synthetic legacy source estate",
    "estate assessment and modernisation decisioning",
    "target-state architecture and platform decisions",
    "migration factory",
    "Azure SQL operational administration model",
    "SQL performance engineering",
    "SQL database development lifecycle",
    "database-as-code",
    "Azure SQL",
    "Azure Databricks",
    "managed identity",
    "Bicep",
]


def validate_required_paths() -> list[str]:
    failures: list[str] = []
    for relative_path in REQUIRED_PATHS:
        if not (ROOT / relative_path).is_file():
            failures.append(f"Missing required file: {relative_path}")
    for relative_path in REQUIRED_DIRECTORIES:
        if not (ROOT / relative_path).is_dir():
            failures.append(f"Missing required directory: {relative_path}")
    return failures


def validate_readme_terms() -> list[str]:
    readme = (ROOT / "README.md").read_text(encoding="utf-8").lower()
    return [
        f"README.md missing required term: {term}"
        for term in REQUIRED_README_TERMS
        if term.lower() not in readme
    ]


def validate_adr_metadata() -> list[str]:
    failures: list[str] = []
    adr_files = sorted((ROOT / "docs/adr").glob("[0-9][0-9][0-9][0-9]-*.md"))
    if len(adr_files) < 5:
        failures.append("Expected at least five initial ADRs")
    for adr_file in adr_files:
        text = adr_file.read_text(encoding="utf-8")
        for required in ("- Status:", "- Date:", "## Context", "## Decision", "## Consequences"):
            if required not in text:
                failures.append(f"{adr_file.relative_to(ROOT)} missing {required}")
    return failures


def validate_roadmap_scope() -> list[str]:
    roadmap = (ROOT / "docs/roadmap.md").read_text(encoding="utf-8").lower()
    required_topics = [
        "azure sql modernisation",
        "sql ci/cd",
        "databricks",
        "ingestion",
        "medallion",
        "data quality",
        "operational analytics",
        "vector",
        "hybrid search",
        "rag",
        "monitoring",
        "finops",
        "production assurance",
    ]
    return [
        f"docs/roadmap.md missing topic: {topic}"
        for topic in required_topics
        if topic not in roadmap
    ]


def main() -> int:
    failures = (
        validate_required_paths()
        + validate_readme_terms()
        + validate_adr_metadata()
        + validate_roadmap_scope()
    )
    if failures:
        print("Repository structure validation failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("Repository structure validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
