# SQL Database Development Lifecycle

Milestone 8 implements database-as-code for the `legacy_tms` Azure SQL Managed Instance target. The lifecycle is intentionally evidence-driven: local commands can build and validate project assets, while real deployment remains behind environment approvals and live Azure configuration.

## Project Structure

The SQL project lives in `src/azure_sql/database_project/legacy_tms/` and uses `Microsoft.Build.Sql`.

- `legacy_tms.sqlproj` defines the SDK-style SQL project.
- `Tables/`, `Views/`, and `StoredProcedures/` hold declarative database objects.
- `Security/` holds role, grant, masking, and classification patterns.
- `PreDeployment/` contains release guardrails.
- `PostDeployment/ReferenceData.sql` contains idempotent depot and route reference data.
- `Tests/` contains SQL assertions for later SQL Server-compatible execution.

## Local Workflow

```bash
make validate-sql-cicd
make test-sql-project
make build-sql-project
```

`make build-sql-project` runs a real `dotnet build`. If the .NET SDK is not installed, the command fails clearly and does not claim a dacpac was created.

## CI and Promotion

The CI workflow validates the repository, generates SQL release evidence, builds the SQL project on a runner with .NET, and uploads the dacpac artifact. The SQL release-preview workflow is dispatch-only and separates `dev`, `test`, and `prod` through GitHub environments. Live publishing is deliberately left as an environment-specific extension after drift reporting, backups, approvals, and identity are configured.

## Drift and Safety

Release gates cover destructive changes, schema drift, reference-data idempotency, least-privilege security, environment promotion, and rollback boundaries. The expected production path is:

1. Build dacpac.
2. Generate deploy report and script preview.
3. Compare target drift against the committed dacpac.
4. Review destructive changes and security changes.
5. Confirm backup or restore point.
6. Publish only through an approved environment.

## Rollback Boundary

The rollback unit is one dacpac release plus the associated database backup or restore point. Data migrations are not hidden inside the schema publish path; they remain separate reviewed scripts with their own rollback plan.

## Evidence

Generated evidence is written to `outputs/sql_cicd/` and summarised in `reports/sql_cicd_report.md`. The release manifest records tool availability and states that no Azure deployment was performed.

