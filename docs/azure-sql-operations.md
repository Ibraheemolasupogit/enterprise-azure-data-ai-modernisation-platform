# Azure SQL Administration and Operational Resilience

Milestone 6 defines the operational-control layer for the `legacy_tms` Azure SQL Managed Instance target. It does not deploy Azure resources, run backups, restore databases, fail over regions, or perform query/index tuning.

## Operational Architecture

The model uses:

- Azure SQL Managed Instance for `legacy_tms`.
- Entra-first database access with contained users and role-based permissions.
- Managed identities for application and automation workloads.
- Key Vault boundary for unavoidable secrets and future customer-managed key decisions.
- Private connectivity in production.
- Azure Monitor, Log Analytics, diagnostic settings, alert rules, and runbooks.
- SQL Agent for MI-compatible operational tasks.
- Bicep modules for future deployment intent.

## Configuration Baseline

The generated baseline in `outputs/azure_sql_operations/configuration_baseline.csv` captures service tier, compute, storage, backup retention, maintenance, timezone, collation, public endpoint posture, private connectivity, TLS, Entra authentication, diagnostics, and auditing.

Sizing remains design-level. vCores, storage, IO, collation, zone redundancy, and long-term retention require live validation.

## Security

Security assets are in `src/azure_sql/operations/security/`:

- Entra placeholder groups and managed identities.
- Database roles for platform admins, DBAs, deployment, app execution, operational readers, auditors, and automation.
- Procedure-level permissions for application workloads.
- View-level read access for analysts.
- Sensitive classification, masking, and RLS pattern for regional access.

RLS is scripted OFF until business regional-access rules are validated.

## Recovery

Recovery model:

- Automated Azure backups and PITR are expected platform capabilities.
- Long-term retention is a required decision, not locally enabled.
- Restore drills are modelled through runbooks and readiness outputs.
- No restore has been executed locally.

## HA/DR

The target follows the Milestone 4 recovery tier for critical transport OLTP:

- RTO: 60 minutes.
- RPO: 15 minutes.
- Built-in SQL MI HA is expected.
- Zone redundancy and failover groups require Azure region, tier, cost, and application validation.
- Planned failover, unplanned outage, application reconnection, data-loss window, and failback tests are defined but not executed.

## Monitoring and Alerts

KQL assets are in `src/azure_sql/operations/kql/`.

Monitoring covers CPU, storage, worker/session pressure, deadlocks, blocking, failed logins, database availability, backup/recovery events, failover status, and long-running queries.

Alert definitions are generated in `outputs/azure_sql_operations/alert_catalog.csv` and map each alert to a runbook.

## Automation and Maintenance

SQL Agent assets are in `src/azure_sql/operations/agent_jobs/`:

- Integrity check job.
- Statistics maintenance job.
- Operational evidence collection job.
- Job history retention cleanup job.

Maintenance principles:

- DBCC CHECKDB strategy must be scheduled by environment and capacity.
- Statistics maintenance is threshold/time based.
- Index maintenance is a boundary only; deep performance engineering is deferred.
- Audit/log retention and job history retention must follow policy.
- Capacity and backup reviews are recurring operational controls.

## Local vs Azure Validation Boundary

Locally validated:

- Generated evidence matrices.
- Role/control/alert/runbook mappings.
- Presence of T-SQL, KQL, SQL Agent, Bicep, and runbook assets.

Configuration defined:

- Bicep module intent.
- Diagnostic settings intent.
- SQL security and automation scripts.

Requires Azure validation:

- Deployment.
- Diagnostic log flow.
- Backup and restore.
- Failover groups.
- Zone redundancy.
- Alert firing.
- Production sizing and collation.

