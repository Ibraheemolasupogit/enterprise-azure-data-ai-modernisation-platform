USE msdb;
GO

IF EXISTS (SELECT 1 FROM dbo.sysjobs WHERE name = N'cf-statistics-maintenance')
BEGIN
    EXEC dbo.sp_delete_job @job_name = N'cf-statistics-maintenance';
END;
GO

EXEC dbo.sp_add_job
    @job_name = N'cf-statistics-maintenance',
    @description = N'Updates stale statistics. Does not perform blanket index rebuilds.',
    @enabled = 1;

EXEC dbo.sp_add_jobstep
    @job_name = N'cf-statistics-maintenance',
    @step_name = N'Update changed statistics',
    @subsystem = N'TSQL',
    @database_name = N'legacy_tms',
    @command = N'
DECLARE @sql nvarchar(max) = N'''';
SELECT @sql = STRING_AGG(N''UPDATE STATISTICS '' + QUOTENAME(SCHEMA_NAME(o.schema_id)) + N''.'' + QUOTENAME(o.name) + N'' '' + QUOTENAME(s.name) + N'' WITH RESAMPLE;'', CHAR(10))
FROM sys.stats s
INNER JOIN sys.objects o ON s.object_id = o.object_id
WHERE o.type = ''U''
  AND STATS_DATE(s.object_id, s.stats_id) < DATEADD(day, -7, SYSUTCDATETIME());
IF @sql IS NOT NULL EXEC sys.sp_executesql @sql;';

