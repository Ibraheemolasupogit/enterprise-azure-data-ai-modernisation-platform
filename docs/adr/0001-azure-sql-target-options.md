# ADR-0001: Azure SQL Target Options

- Status: Accepted
- Date: 2026-08-20

## Context

The platform must demonstrate modernisation patterns for a legacy SQL Server estate without implying one universal target. Different operational workloads have different compatibility, isolation, manageability, cost, HA/DR, and performance requirements.

## Decision

Use workload-specific target selection across Azure SQL Database, Azure SQL Managed Instance, and SQL Server on Azure VM:

- Prefer Azure SQL Database for modernised application databases that can adopt platform-as-a-service boundaries and database-scoped features.
- Use Azure SQL Managed Instance when instance-level compatibility, SQL Agent compatibility, cross-database behaviour, or migration risk justifies it.
- Reserve SQL Server on Azure VM for workloads with hard compatibility constraints that cannot move to Azure SQL platform services within acceptable risk or cost.

Milestone 3 applies this decision by recommending Azure SQL Managed Instance as the initial target for the synthetic `legacy_tms` workload. Azure SQL Database remains a plausible later optimisation target after procedure coupling, identity, collation, and performance risks are validated. SQL Server on Azure VM is rejected for the current target state because no hard local evidence justifies retaining that level of infrastructure responsibility.

## Consequences

This keeps the architecture credible for enterprise estates with mixed constraints. It also means future documentation and automation must explain decision criteria instead of presenting one target as universally correct.

## Alternatives Considered

- Standardise only on Azure SQL Database: simpler but unrealistic for complex legacy estates.
- Standardise only on Managed Instance: easier migration path for some workloads but can overfit compatibility needs and increase cost.
- Lift all SQL Server workloads to Azure VM: maximises compatibility but preserves too much infrastructure responsibility.
