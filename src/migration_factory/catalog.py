from __future__ import annotations

# ruff: noqa: E501
from migration_factory.model import MigrationManifest, Remediation, ToolIntegration

MANIFESTS = [
    MigrationManifest(
        "mig-legacy-tms-sqlmi",
        "legacy_tms",
        "SQL Server 2016 compatibility profile",
        "Azure SQL Managed Instance",
        "SQL Managed Instance current platform version, requires live validation",
        "Wave 3",
        "replatform",
        "online/minimal-downtime",
        45,
        60,
        15,
        "CustomerAccount; Depot; Route; Vehicle; Shipment; ShipmentEventHistory; ShipmentIncident; views; stored procedures",
        "customers; depots; routes; vehicles; shipments; shipment events",
        "Wave 0 prerequisites; identity discovery; procedure regression; backup/recovery evidence; app readiness",
        "SQL-COMP-001; SQL-COMP-003; SQL-COMP-005; SQL-COMP-008; SQL-COMP-009",
        "local schema remediations implemented; cloud validation deferred",
        "row counts; key counts; null profile; timestamps; referential integrity; duplicates; checksums; chronology",
        "Database migration lead",
        "failed pre-cutover validation, unresolved compatibility blocker, stale delta, or business smoke-test failure",
        "first hour, first day, first week",
        "derived from assessment",
    ),
    MigrationManifest(
        "mig-billing-postgres",
        "billing_ops",
        "PostgreSQL 13 compatibility profile",
        "Azure Database for PostgreSQL Flexible Server",
        "PostgreSQL flexible-server target version requires live validation",
        "Wave 2",
        "replatform",
        "offline",
        180,
        240,
        60,
        "invoice; payment; service_case; case_note",
        "invoices; payments; service cases; case notes",
        "identifier mapping; invoice/payment reconciliation; service-process validation",
        "customer_ref mapping and case referential anomalies",
        "target schema implemented locally; live target validation deferred",
        "row counts; key counts; null profile; financial reconciliation; referential integrity; checksums",
        "Finance systems migration lead",
        "invoice/payment reconciliation failure, duplicate key, or case workflow smoke-test failure",
        "first hour, first day, first week",
        "derived from assessment",
    ),
]


REMEDIATIONS = [
    Remediation("SQL-COMP-001", "dbo.CustomerAccount.LegacyCustomerMemo", "Replace deprecated ntext with nvarchar(max).", "dbo.CustomerAccount.LegacyCustomerMemo", "implemented locally", "Target SQL uses nvarchar(max); local static schema comparison generated."),
    Remediation("SQL-COMP-002", "dbo.Shipment.DeclaredValueGbp", "Retain money for migration compatibility but flag decimal review for SQL performance milestone.", "dbo.Shipment.DeclaredValueGbp", "accepted risk", "Manifest documents accepted compatibility risk; no cloud validation claimed."),
    Remediation("SQL-COMP-003", "dbo.usp_CreateShipment; dbo.usp_UpdateShipmentStatus", "Preserve stored procedure signatures and create regression-test placeholders.", "target stored procedures", "implemented locally", "Target SQL assets include stored procedures; execution against Azure not performed."),
    Remediation("SQL-COMP-004", "LegacyOptionsJson; EventPayloadJson", "Retain JSON as nvarchar(max) and document contract validation requirement.", "target JSON columns", "implemented locally", "Target schema keeps JSON payload columns; downstream validation deferred."),
    Remediation("SQL-COMP-005", "vw_OpenShipmentsByDepot; operational reporting query", "Add migration-readiness nonclustered index for route/status/date reporting only.", "IX_Shipment_Route_Status_CreatedAt", "implemented locally", "Target index asset generated; performance milestone remains deferred."),
    Remediation("SQL-COMP-006", "dbo.ShipmentEventHistory", "Document history-table migration and replay strategy; do not implement partitioning yet.", "dbo.ShipmentEventHistory", "deferred", "Partitioning and archival design deferred to SQL operations/performance milestones."),
    Remediation("SQL-COMP-007", "dbo.Shipment.RowVersionBytes", "Preserve rowversion and document concurrency semantics.", "dbo.Shipment.RowVersionBytes", "implemented locally", "Target SQL preserves rowversion."),
    Remediation("SQL-COMP-008", "Legacy authentication model", "Remove hardcoded users from target schema; use Entra/managed identity later.", "security model", "requires live validation", "No users emitted in target schema; Entra mapping requires live environment."),
    Remediation("SQL-COMP-009", "Collation and instance settings", "Document live validation prerequisite.", "target MI settings", "requires live validation", "Cannot be validated locally; gate remains required."),
    Remediation("PG-COMP-001", "billing_ops customer_ref", "Keep source customer_ref but add migration evidence for identifier mapping risk.", "billing_ops.invoice.customer_ref", "accepted risk", "Reconciliation checks customer_ref counts; semantic mapping deferred."),
]


TOOL_INTEGRATIONS = [
    ToolIntegration("Azure Database Migration Service", "online migration", "Initial load, delta capture, final sync for supported database migrations.", "Local adapter models phases and evidence only.", "DMS project logs, cutover timestamps, validation summaries."),
    ToolIntegration("Data Migration Assistant / Azure SQL assessment tooling", "assessment and schema readiness", "SQL Server compatibility assessment before Azure SQL MI migration.", "Local static scanner and remediation register.", "DMA reports and resolved blocker evidence."),
    ToolIntegration("SqlPackage", "schema deployment", "Dacpac extract/publish or schema compare where project model is introduced.", "Target SQL scripts and schema-conversion report.", "Publish report, drift report, deployment logs."),
    ToolIntegration("Native SQL backup/restore", "bulk migration", "Backup/restore or log shipping approach where MI supports target scenario.", "Offline/online mode sequence model only.", "Backup chain validation and restore verification."),
    ToolIntegration("pg_dump/pg_restore", "PostgreSQL migration", "Logical dump/restore for billing_ops offline migration.", "CSV-based local movement and PostgreSQL target schema.", "Dump manifest, restore logs, row-count reconciliation."),
    ToolIntegration("Azure CLI / PowerShell", "orchestration", "Resource checks, identity, firewall/private endpoint, and migration command automation.", "Local command orchestrator with no Azure calls.", "Command transcripts and deployment evidence."),
]

