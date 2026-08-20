USE msdb;
GO

IF EXISTS (SELECT 1 FROM dbo.sysjobs WHERE name = N'cf-job-history-retention')
BEGIN
    EXEC dbo.sp_delete_job @job_name = N'cf-job-history-retention';
END;
GO

EXEC dbo.sp_add_job
    @job_name = N'cf-job-history-retention',
    @description = N'Maintains SQL Agent job history retention. Does not delete regulated audit destinations.',
    @enabled = 1;

EXEC dbo.sp_add_jobstep
    @job_name = N'cf-job-history-retention',
    @step_name = N'Purge old job history',
    @subsystem = N'TSQL',
    @database_name = N'msdb',
    @command = N'EXEC dbo.sp_purge_jobhistory @oldest_date = DATEADD(day, -45, SYSUTCDATETIME());';

