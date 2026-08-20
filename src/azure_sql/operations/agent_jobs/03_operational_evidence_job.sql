USE msdb;
GO

IF EXISTS (SELECT 1 FROM dbo.sysjobs WHERE name = N'cf-operational-evidence')
BEGIN
    EXEC dbo.sp_delete_job @job_name = N'cf-operational-evidence';
END;
GO

EXEC dbo.sp_add_job
    @job_name = N'cf-operational-evidence',
    @description = N'Captures lightweight operational evidence for backup, job, and database state review.',
    @enabled = 1;

EXEC dbo.sp_add_jobstep
    @job_name = N'cf-operational-evidence',
    @step_name = N'Capture evidence snapshot',
    @subsystem = N'TSQL',
    @database_name = N'legacy_tms',
    @command = N'
SELECT DB_NAME() AS database_name, SYSUTCDATETIME() AS evidence_utc;
SELECT name, state_desc, recovery_model_desc FROM sys.databases WHERE name = DB_NAME();
SELECT TOP (20) name, date_modified FROM sys.objects ORDER BY date_modified DESC;';

