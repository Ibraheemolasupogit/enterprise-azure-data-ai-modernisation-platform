# ADR-0006: Azure SQL vs PostgreSQL Disposition

- Status: Accepted
- Date: 2026-08-20

## Context

Milestone 3 assesses two relational source patterns: a SQL Server-style transport management system and a PostgreSQL-like billing/service source. Forcing both into one relational target would hide source-specific compatibility and operational trade-offs.

## Decision

Recommend Azure SQL Managed Instance for the SQL Server-style transport workload and Azure Database for PostgreSQL for the PostgreSQL-like billing/service workload, subject to live validation before migration execution.

## Consequences

This preserves source semantics and avoids unnecessary application change. It also means future integration work must handle cross-source identifiers, reconciliation, security, monitoring, and coordinated cutover across more than one database platform.

## Alternatives Considered

- Move both sources to Azure SQL: rejected because the billing source is PostgreSQL-like and does not need SQL Server compatibility.
- Move both sources to PostgreSQL: rejected because the transport system contains SQL Server-style stored procedures and compatibility concerns.
- Keep both indefinitely: rejected as a target state, but temporary retention remains valid until prerequisites are complete.

