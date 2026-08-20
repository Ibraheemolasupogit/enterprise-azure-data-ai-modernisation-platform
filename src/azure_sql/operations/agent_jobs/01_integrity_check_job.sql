USE msdb;
GO

IF EXISTS (SELECT 1 FROM dbo.sysjobs WHERE name = N'cf-integrity-check')
BEGIN
    EXEC dbo.sp_delete_job @job_name = N'cf-integrity-check';
END;
GO

EXEC dbo.sp_add_job
    @job_name = N'cf-integrity-check',
    @description = N'Runs targeted database integrity checks and captures evidence. Schedule requires production validation.',
    @enabled = 1;

EXEC dbo.sp_add_jobstep
    @job_name = N'cf-integrity-check',
    @step_name = N'DBCC CHECKDB physical only',
    @subsystem = N'TSQL',
    @database_name = N'legacy_tms',
    @command = N'DBCC CHECKDB (N''legacy_tms'') WITH PHYSICAL_ONLY, NO_INFOMSGS;';

