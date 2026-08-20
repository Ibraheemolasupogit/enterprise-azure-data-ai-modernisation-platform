from __future__ import annotations

# ruff: noqa: E501
from azure_sql_operations.model import (
    AlertRule,
    AutomationItem,
    ConfigurationBaseline,
    MonitoringItem,
    ReadinessCheck,
    SecurityRole,
    SensitiveDataControl,
)

CONFIGURATION_BASELINE = [
    ConfigurationBaseline("target_service", "Azure SQL Managed Instance", "Preserves SQL Server compatibility for legacy_tms.", "derived from assessment", True),
    ConfigurationBaseline("service_tier", "General Purpose initially; Business Critical only if latency/IO/HA validation justifies it", "Avoids invented production sizing while documenting service-tier decision path.", "estimated design assumption", True),
    ConfigurationBaseline("compute", "vCore count requires workload telemetry", "CPU, waits, concurrency, and IO are not locally measurable.", "requires Azure validation", True),
    ConfigurationBaseline("storage", "Start from migration volume plus growth buffer; max storage reviewed quarterly", "Synthetic estate does not represent production size.", "estimated design assumption", True),
    ConfigurationBaseline("backup_retention", "35-day PITR assumption for prod; shorter dev/test retention", "Balances operational recovery with cost; exact policy requires owner approval.", "estimated design assumption", True),
    ConfigurationBaseline("long_term_retention", "Required decision, not enabled locally", "Regulatory retention is not proven by synthetic data.", "requires Azure validation", True),
    ConfigurationBaseline("maintenance_window", "Defined per environment; avoid depot handover windows", "Operational peak window identified in assessment.", "derived from assessment", True),
    ConfigurationBaseline("timezone", "UTC for database timestamps and operational evidence", "Avoids regional ambiguity.", "locally validated", False),
    ConfigurationBaseline("collation", "Requires live estate validation before deployment", "Milestone 3 identified unknown production collation.", "requires Azure validation", True),
    ConfigurationBaseline("public_endpoint", "Disabled for production target", "Private data-plane architecture decision.", "estimated design assumption", True),
    ConfigurationBaseline("private_connectivity", "VNet delegated subnet for MI, Private DNS, restricted admin path", "Milestone 4 private networking target.", "estimated design assumption", True),
    ConfigurationBaseline("minimum_tls", "TLS 1.2 or newer", "Baseline in-transit protection expectation.", "estimated design assumption", True),
    ConfigurationBaseline("entra_authentication", "Entra-first with contained database users/groups", "Reduces static credential use.", "derived from assessment", True),
    ConfigurationBaseline("diagnostic_settings", "Send SQLSecurityAuditEvents, errors, blocks, waits, and resource metrics to Log Analytics", "Supports operations and audit evidence.", "configuration defined", True),
    ConfigurationBaseline("auditing", "Enabled to Log Analytics/storage destination in real Azure", "Audit destination cannot be validated locally.", "configuration defined", True),
]


SECURITY_ROLES = [
    SecurityRole("Entra group", "grp-cf-platform-admins", "cf_platform_admin", "ALTER ANY USER; VIEW DEFINITION; no broad data export by default", "Platform administration without ownership of all data.", "configuration defined"),
    SecurityRole("Entra group", "grp-cf-db-admins", "cf_db_admin", "db_owner equivalent only for DBA break/fix role in controlled environments", "DBA role is separate from app and analyst roles.", "configuration defined"),
    SecurityRole("Managed identity", "mi-cf-transport-app", "cf_app_executor", "EXECUTE on operational procedures; SELECT/INSERT/UPDATE only where required", "Application uses procedure-led access and avoids broad DDL.", "configuration defined"),
    SecurityRole("Federated identity", "id-cf-sql-deploy", "cf_deployment", "DDL deployment permissions through CI/CD only", "Deployment identity is not a runtime identity.", "configuration defined"),
    SecurityRole("Entra group", "grp-cf-operational-analysts", "cf_operational_reader", "SELECT on reporting views only", "Analysts do not need base table write access.", "configuration defined"),
    SecurityRole("Entra group", "grp-cf-security-auditors", "cf_security_auditor", "VIEW DATABASE SECURITY AUDIT; SELECT on audit/evidence views", "Auditors can inspect evidence without operational writes.", "configuration defined"),
    SecurityRole("Managed identity", "mi-cf-ops-automation", "cf_automation_executor", "EXECUTE on maintenance/evidence procedures only", "Automation rights are scoped to operational tasks.", "configuration defined"),
]


SENSITIVE_CONTROLS = [
    SensitiveDataControl("dbo.CustomerAccount.ContactEmail", "confidential contact data", "Sensitive classification; Dynamic Data Masking for non-privileged readers; audit access", "configuration defined", "locally validated"),
    SensitiveDataControl("dbo.CustomerAccount.LegalName", "confidential customer account data", "Sensitive classification; role-based SELECT; audit access", "configuration defined", "locally validated"),
    SensitiveDataControl("dbo.Shipment.DeclaredValueGbp", "commercially sensitive shipment value", "Role-based SELECT; audit access; no blanket masking for operations", "configuration defined", "locally validated"),
    SensitiveDataControl("dbo.Shipment.LegacyOptionsJson", "operational attributes", "JSON contract validation later; role-based SELECT", "configuration defined", "derived from assessment"),
    SensitiveDataControl("billing_ops invoice/payment data", "financial data boundary", "PostgreSQL target owns financial protection; SQL MI references only migration evidence", "planned external control", "architecture/design evidence"),
    SensitiveDataControl("service case information", "customer-service sensitive notes", "Retain in billing/service target; future governed search requires security trimming", "planned external control", "architecture/design evidence"),
    SensitiveDataControl("regional shipment visibility", "operational segmentation", "Row-Level Security pattern for region/depot readers where business rules require", "configuration defined", "locally validated"),
]


MONITORING_CATALOG = [
    MonitoringItem("cpu_percent", "Azure Monitor metric", "kql/sqlmi_resource_health.kql", "Detect sustained CPU saturation.", "Deep query tuning deferred to Milestone 7."),
    MonitoringItem("storage_percent", "Azure Monitor metric", "kql/sqlmi_resource_health.kql", "Detect storage exhaustion risk.", "Capacity review only."),
    MonitoringItem("connection_failed", "SQL audit logs", "kql/sqlmi_security_audit.kql", "Investigate failed logins and identity issues.", "No real audit stream locally."),
    MonitoringItem("deadlock", "SQL diagnostics/audit", "kql/sqlmi_blocking_deadlocks.kql", "Triage concurrency incidents.", "Query tuning deferred."),
    MonitoringItem("blocking_session", "SQL diagnostics", "kql/sqlmi_blocking_deadlocks.kql", "Triage blocking chains.", "Query tuning deferred."),
    MonitoringItem("database_unavailable", "Azure Monitor availability", "kql/sqlmi_availability_recovery.kql", "Detect database availability impact.", "Requires Azure validation."),
    MonitoringItem("backup_restore_event", "Azure activity/diagnostic logs", "kql/sqlmi_availability_recovery.kql", "Track restore and recovery events.", "Requires Azure validation."),
    MonitoringItem("failover_group_state", "Azure resource health/activity", "kql/sqlmi_availability_recovery.kql", "Track failover/replication status.", "Requires Azure validation."),
    MonitoringItem("long_running_query", "SQL diagnostics", "kql/sqlmi_long_running_queries.kql", "Identify candidates for performance milestone.", "No tuning performed."),
    MonitoringItem("worker_session_pressure", "SQL metrics", "kql/sqlmi_resource_health.kql", "Detect worker/session pressure.", "Requires Azure validation."),
]


ALERT_CATALOG = [
    AlertRule("sqlmi-high-cpu", "cpu_percent", "Sev3", "Sustained high CPU over business-relevant window, not single spike.", "15 minutes", "Notify database operations", "docs/runbooks/sqlmi-resource-saturation.md"),
    AlertRule("sqlmi-storage-risk", "storage_percent", "Sev2", "Storage trend approaching capacity requires proactive review.", "30 minutes", "Notify database operations and platform owner", "docs/runbooks/sqlmi-storage-capacity.md"),
    AlertRule("sqlmi-repeated-failed-logins", "connection_failed", "Sev2", "Repeated failures may indicate identity issue or attack.", "10 minutes", "Notify security and DBA", "docs/runbooks/sqlmi-authentication-failure.md"),
    AlertRule("sqlmi-deadlocks", "deadlock", "Sev3", "Repeated deadlocks affect business workflow reliability.", "15 minutes", "Notify DBA", "docs/runbooks/sqlmi-blocking-deadlock.md"),
    AlertRule("sqlmi-unavailable", "database_unavailable", "Sev1", "Unavailable critical OLTP database breaches service objective.", "5 minutes", "Page incident commander and DBA", "docs/runbooks/sqlmi-database-unavailable.md"),
    AlertRule("sqlmi-failover-replication", "failover_group_state", "Sev1", "Replication/failover status affects RTO/RPO confidence.", "5 minutes", "Page DBA and platform administrator", "docs/runbooks/sqlmi-regional-dr-failover.md"),
    AlertRule("sqlmi-backup-restore-issue", "backup_restore_event", "Sev2", "Backup/restore events require evidence and recovery review.", "30 minutes", "Notify DBA", "docs/runbooks/sqlmi-restore-request.md"),
    AlertRule("sqlmi-agent-job-failed", "sql_agent_job_failed", "Sev3", "Operational maintenance evidence job failure needs triage.", "per job execution", "Notify DBA", "docs/runbooks/sqlmi-failed-agent-job.md"),
]


AUTOMATION_CATALOG = [
    AutomationItem("integrity-check-job", "SQL Agent on Managed Instance", "weekly or pre-change", "Run representative DBCC CHECKDB/integrity workflow and capture evidence.", "Do not run heavyweight checks blindly; schedule requires production validation.", "configuration defined"),
    AutomationItem("statistics-maintenance-job", "SQL Agent on Managed Instance", "daily low-activity window", "Update stale statistics based on modification thresholds.", "No blanket index rebuild or query tuning in Milestone 6.", "configuration defined"),
    AutomationItem("operational-evidence-job", "SQL Agent on Managed Instance", "daily", "Capture backup status, row-count sanity, security posture, and job health evidence.", "Evidence collection only.", "configuration defined"),
    AutomationItem("retention-cleanup-job", "SQL Agent on Managed Instance", "weekly", "Retain job/audit staging evidence according to policy.", "Does not delete regulated audit destinations.", "configuration defined"),
    AutomationItem("restore-drill-runbook", "Azure Automation / PowerShell boundary", "quarterly planned drill", "Model PITR/restore validation steps and evidence capture.", "No local Azure restore execution.", "requires Azure validation"),
    AutomationItem("diagnostic-settings-deploy", "Bicep / CI-CD", "per deployment", "Apply diagnostic settings and alert definitions.", "Deployment not executed locally.", "configuration defined"),
]


BACKUP_RESTORE_READINESS = [
    ReadinessCheck("br-001", "backup", "Automated backup retention policy defined.", "configuration defined", "35-day prod PITR assumption and LTR decision captured.", "docs/runbooks/sqlmi-restore-request.md"),
    ReadinessCheck("br-002", "backup", "Long-term retention decision captured.", "requires Azure validation", "Regulatory retention requires owner approval.", "docs/azure-sql-operations.md"),
    ReadinessCheck("br-003", "restore", "Restore drill prerequisites documented.", "simulated", "Runbook defines prerequisites, expected commands, validation criteria, evidence, pass/fail.", "docs/runbooks/sqlmi-restore-request.md"),
    ReadinessCheck("br-004", "restore", "Point-in-time restore validation.", "requires Azure validation", "No Azure restore executed locally.", "docs/runbooks/sqlmi-restore-request.md"),
    ReadinessCheck("br-005", "reconciliation", "Post-restore data validation criteria exist.", "configuration defined", "Migration reconciliation model reused as validation pattern.", "outputs/migration/data_reconciliation.csv"),
]


HA_DR_READINESS = [
    ReadinessCheck("hadr-001", "HA", "Built-in SQL MI HA considered.", "configuration defined", "Target service baseline captured.", "outputs/architecture/recovery_strategy_matrix.csv"),
    ReadinessCheck("hadr-002", "HA", "Zone redundancy assumption documented.", "requires Azure validation", "Region/tier support and cost require validation.", "docs/azure-sql-operations.md"),
    ReadinessCheck("hadr-003", "DR", "Failover group/secondary-region design captured.", "requires Azure validation", "No failover group deployed locally.", "docs/runbooks/sqlmi-regional-dr-failover.md"),
    ReadinessCheck("hadr-004", "DR", "Planned failover test defined.", "simulated", "Runbook defines planned failover validation steps.", "docs/runbooks/sqlmi-planned-failover.md"),
    ReadinessCheck("hadr-005", "DR", "Unplanned outage scenario defined.", "simulated", "Regional DR runbook defines escalation and failover criteria.", "docs/runbooks/sqlmi-regional-dr-failover.md"),
    ReadinessCheck("hadr-006", "RTO/RPO", "RTO 60 / RPO 15 traces to architecture.", "configuration defined", "Milestone 4 recovery strategy matrix.", "outputs/architecture/recovery_strategy_matrix.csv"),
    ReadinessCheck("hadr-007", "application", "Application retry and reconnection requirement captured.", "configuration defined", "Runbooks include connection validation and app retry expectation.", "docs/runbooks/sqlmi-database-unavailable.md"),
]


OPERATIONAL_READINESS = [
    ReadinessCheck("ops-001", "identity", "Entra groups and managed identity patterns defined.", "configuration defined", "Security role matrix generated.", "outputs/azure_sql_operations/security_role_matrix.csv"),
    ReadinessCheck("ops-002", "encryption", "Encryption/TDE/TLS expectations defined.", "configuration defined", "Configuration baseline and data controls generated.", "outputs/azure_sql_operations/configuration_baseline.csv"),
    ReadinessCheck("ops-003", "auditing", "Audit and diagnostic settings defined.", "configuration defined", "Monitoring catalog and Bicep diagnostics module.", "infra/modules/azure-sql/managed-instance.bicep"),
    ReadinessCheck("ops-004", "network", "Private endpoint posture defined.", "configuration defined", "Configuration baseline and Bicep module parameters.", "outputs/azure_sql_operations/configuration_baseline.csv"),
    ReadinessCheck("ops-005", "backup", "Backup retention and restore drill defined.", "configuration defined", "Backup/restore readiness output.", "outputs/azure_sql_operations/backup_restore_readiness.csv"),
    ReadinessCheck("ops-006", "restore", "Actual restore validation pending.", "requires Azure validation", "No Azure PITR executed locally.", "docs/runbooks/sqlmi-restore-request.md"),
    ReadinessCheck("ops-007", "HA", "Built-in HA design documented.", "configuration defined", "HA/DR readiness output.", "outputs/azure_sql_operations/ha_dr_readiness.csv"),
    ReadinessCheck("ops-008", "DR", "Actual failover tests pending.", "requires Azure validation", "No Azure failover executed locally.", "docs/runbooks/sqlmi-regional-dr-failover.md"),
    ReadinessCheck("ops-009", "monitoring", "Signals and KQL assets defined.", "configuration defined", "Monitoring catalog generated.", "outputs/azure_sql_operations/monitoring_catalog.csv"),
    ReadinessCheck("ops-010", "alerting", "Alerts map to runbooks.", "locally validated", "Alert catalog generated and validated.", "outputs/azure_sql_operations/alert_catalog.csv"),
    ReadinessCheck("ops-011", "automation", "SQL Agent and platform-native automation boundaries defined.", "configuration defined", "Automation catalog and job scripts generated.", "outputs/azure_sql_operations/automation_catalog.csv"),
    ReadinessCheck("ops-012", "documentation", "Operational runbooks exist.", "locally validated", "Runbook files present and linked.", "docs/runbooks/README.md"),
]

