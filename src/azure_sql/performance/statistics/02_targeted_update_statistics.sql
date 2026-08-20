DECLARE @sql nvarchar(max) = N'';

SELECT @sql = STRING_AGG(
    N'UPDATE STATISTICS '
    + QUOTENAME(OBJECT_SCHEMA_NAME(s.object_id))
    + N'.'
    + QUOTENAME(OBJECT_NAME(s.object_id))
    + N' '
    + QUOTENAME(s.name)
    + N' WITH RESAMPLE;',
    CHAR(10)
)
FROM sys.stats s
CROSS APPLY sys.dm_db_stats_properties(s.object_id, s.stats_id) sp
WHERE OBJECTPROPERTY(s.object_id, 'IsUserTable') = 1
  AND sp.modification_counter > 1000;

IF @sql <> N''
BEGIN
    EXEC sys.sp_executesql @sql;
END;

