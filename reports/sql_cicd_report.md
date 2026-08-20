# SQL Database Development Lifecycle and CI/CD Report

Milestone 8 implements database-as-code assets for the `legacy_tms` Azure SQL Managed Instance target. It defines an SDK-style SQL project, deterministic release evidence, reference-data deployment boundaries, drift scenarios, safety rules, regression gates, and GitHub Actions workflows. It does not publish to Azure, execute live sqlpackage deployment actions, or claim production validation.

## SQL Project

The SQL project is located at `src/azure_sql/database_project/legacy_tms/legacy_tms.sqlproj` and uses `Microsoft.Build.Sql`. Schema files are split by object so tables, views, procedures, security assets, pre-deployment checks, post-deployment reference data, and tests can be reviewed independently.

## Build and Dacpac

`make build-sql-project` runs a real `dotnet build` when the SDK restore toolchain is available. If `dotnet` is absent, the command fails clearly instead of reporting a fake dacpac.

## Reference Data

Reference depots and routes are deployed with deterministic natural-key `MERGE` statements. The post-deployment script updates/inserts known reference rows and does not automatically delete unexpected rows.

## Drift and Safety

Release controls require deploy preview, drift classification, destructive-change review, role/grant traceability, and environment approval before production promotion. Rollback is bounded to the previous dacpac and database backup/restore point; data migrations remain separate reviewed scripts.

## Testing and Regression Gates

Static tests validate project structure, traceability, manifest determinism, reference data, drift scenarios, and safety gates. Performance and security gates connect this milestone to the prior SQL operations and performance evidence without inventing live Azure measurements.
