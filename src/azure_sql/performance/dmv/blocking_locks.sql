SELECT
    r.session_id,
    r.blocking_session_id,
    r.wait_type,
    r.wait_time,
    r.wait_resource,
    s.login_name,
    s.host_name,
    s.program_name,
    txt.text AS request_text
FROM sys.dm_exec_requests r
INNER JOIN sys.dm_exec_sessions s ON r.session_id = s.session_id
OUTER APPLY sys.dm_exec_sql_text(r.sql_handle) txt
WHERE r.blocking_session_id <> 0
   OR r.wait_type LIKE 'LCK%';

