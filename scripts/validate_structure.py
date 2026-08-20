from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_PATHS = [
    ".editorconfig",
    ".gitignore",
    ".github/workflows/ci.yml",
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
    "infra/modules/azure-sql/managed-instance.bicep",
    "src/azure_sql/operations/security/01_roles_and_permissions.sql",
    "src/azure_sql/operations/security/02_data_protection.sql",
    "src/azure_sql/operations/agent_jobs/01_integrity_check_job.sql",
    "src/azure_sql/operations/agent_jobs/02_statistics_maintenance_job.sql",
    "src/azure_sql/operations/kql/sqlmi_resource_health.kql",
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
    "docs/runbooks/README.md",
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
    "scripts/validate_assessment.py",
    "scripts/validate_architecture.py",
    "scripts/validate_migration.py",
    "scripts/validate_azure_sql_operations.py",
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
    "src/azure_sql/operations/security",
    "src/azure_sql/operations/agent_jobs",
    "src/azure_sql/operations/kql",
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
    "does not deploy Azure resources",
    "synthetic legacy source estate",
    "estate assessment and modernisation decisioning",
    "target-state architecture and platform decisions",
    "migration factory",
    "Azure SQL operational administration model",
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
