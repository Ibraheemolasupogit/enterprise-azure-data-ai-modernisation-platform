# Azure SQL Operations Report

Milestone 6 defines the Azure SQL Managed Instance operational control layer for `legacy_tms`. It does not deploy Azure resources, execute backups, perform restore, trigger failover, or tune workload performance.

## Configuration Baseline

- Target service remains Azure SQL Managed Instance.
- Service tier, vCores, storage, collation, zone redundancy, and long-term retention require live validation.
- Production posture disables public endpoint, requires private connectivity, TLS 1.2+, Entra-first authentication, diagnostic settings, and auditing.

## Security Model

- Synthetic Entra group and managed identity placeholders are used.
- Permissions are role based: DBA, deployment, application executor, automation executor, analyst, auditor, and platform administrator.
- Sensitive controls map to actual target schema assets such as `CustomerAccount.ContactEmail`, `LegalName`, `DeclaredValueGbp`, and regional shipment visibility.

## Recovery and HA/DR

- Automated Azure backups, PITR, restore drill evidence, and LTR decisions are modelled but require Azure validation.
- SQL MI built-in HA and possible failover groups are represented as readiness controls.
- Planned failover, unplanned regional outage, application reconnection, data-loss window, and failback are documented as planned tests.

## Monitoring, Alerts, and Automation

- Monitoring catalog covers CPU, storage, sessions, failed logins, deadlocks, blocking, availability, backup/recovery, failover, and long-running queries.
- Alerts map to operational runbooks.
- SQL Agent jobs cover integrity checks, statistics maintenance, operational evidence, and retention cleanup without implementing blanket index rebuilds.

## Validation Boundary

- Locally validated: generated matrices, T-SQL/KQL/runbook presence, role/control/alert mappings.
- Configuration defined: Bicep, SQL security patterns, SQL Agent job definitions, monitoring catalog.
- Requires Azure validation: deployment, diagnostics flow, backups, restore, failover, zone redundancy, actual sizing, and alert firing.
