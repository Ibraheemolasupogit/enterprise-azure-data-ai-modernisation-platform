# Azure SQL Managed Instance Target Assets

These scripts are target-ready schema assets for the local migration factory. They are not deployed in Milestone 5.

The scripts preserve SQL Server compatibility for Azure SQL Managed Instance while applying migration-readiness remediations:

- `ntext` modernised to `nvarchar(max)`.
- Stored procedure signatures preserved for application compatibility testing.
- `rowversion` retained and documented.
- JSON payload columns retained as `nvarchar(max)` with later contract validation required.
- A focused reporting-support index is added for migration readiness only; the dedicated SQL performance milestone remains deferred.

