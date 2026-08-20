# SQL Performance Engineering Report

Milestone 7 defines a reproducible SQL performance-engineering capability for `legacy_tms` on Azure SQL Managed Instance. It does not execute SQL MI workloads, collect Azure telemetry, fabricate execution-plan XML, or implement SQL CI/CD.

## Evidence Boundary

- Locally executable: T-SQL diagnostic scripts and deterministic evidence generation.
- Static analysis: query-shape, index, statistics, blocking, and Query Store readiness models.
- Simulated: baseline metrics, blocking/deadlock scenarios, parameter-sensitive plan scenario.
- Requires Azure/SQL MI validation: real Query Store runtime stats, actual execution plans, waits, memory grants, spills, index usage, and alert correlation.

## Workloads

Six workloads are catalogued: customer lookup, shipment create/update, shipment status query, route/depot reporting, incident/case lookup, and analytical delay reporting.

## Index Engineering

The focused before/after scenario remains route/depot operational reporting. The target schema includes `IX_Shipment_Route_Status_CreatedAt`; additional indexes are candidates only when Query Store and index usage evidence justify them.

## Statistics

The strategy keeps automatic statistics enabled, detects stale statistics, uses targeted updates, and avoids blanket FULLSCAN or blanket index rebuilds.

## Blocking and Deadlocks

DMV scripts and simulated scenarios cover head blockers, blocking chains, sleeping open transactions, writer/writer contention, Extended Events deadlock capture, and application retry guidance for error 1205.

## Regression Workflow

Baseline -> change/deployment -> detect regression -> identify query -> compare plans -> apply safe mitigation -> validate -> document evidence -> remove temporary mitigation where appropriate.
