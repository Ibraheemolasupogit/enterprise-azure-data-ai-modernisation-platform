# legacy_tms SQL Database Project

This SDK-style SQL project models the `legacy_tms` Azure SQL Managed Instance database as code. It is intentionally local and reviewable: building the project can create a `.dacpac`, but publishing to Azure is deferred to approved release workflows.

## Structure

- `Schemas/` contains schema declarations.
- `Tables/` contains table and constraint definitions.
- `Indexes/` contains modelled secondary indexes that are separate build objects.
- `Views/` contains operational read models.
- `StoredProcedures/` contains controlled write paths.
- `Security/` contains role, grant, masking, and classification patterns.
- `PreDeployment/` contains deployment guardrails.
- `PostDeployment/` contains the post-deployment entrypoint and idempotent reference data.
- `Tests/` contains static assertions for database review and is excluded from dacpac schema compilation.

## Local Workflow

Run `make validate-sql-cicd` to generate deterministic release evidence and run static gates. Run `make build-sql-project` only when the local machine has the .NET SDK and can restore `Microsoft.Build.Sql`; otherwise the command fails clearly.
