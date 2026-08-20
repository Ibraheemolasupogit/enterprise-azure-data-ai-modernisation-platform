SELECT
    r.session_id,
    r.status,
    r.command,
    r.cpu_time,
    r.logical_reads,
    r.reads,
    r.writes,
    r.granted_query_memory,
    r.wait_type,
    r.wait_time,
    txt.text AS request_text
FROM sys.dm_exec_requests r
OUTER APPLY sys.dm_exec_sql_text(r.sql_handle) txt
ORDER BY r.cpu_time DESC, r.logical_reads DESC;

