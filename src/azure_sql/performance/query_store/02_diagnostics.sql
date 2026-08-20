-- Top resource consumers.
SELECT TOP (25)
    q.query_id,
    p.plan_id,
    qt.query_sql_text,
    rs.avg_duration,
    rs.avg_cpu_time,
    rs.avg_logical_io_reads,
    rs.count_executions,
    rsi.start_time,
    rsi.end_time
FROM sys.query_store_query q
INNER JOIN sys.query_store_query_text qt ON q.query_text_id = qt.query_text_id
INNER JOIN sys.query_store_plan p ON q.query_id = p.query_id
INNER JOIN sys.query_store_runtime_stats rs ON p.plan_id = rs.plan_id
INNER JOIN sys.query_store_runtime_stats_interval rsi ON rs.runtime_stats_interval_id = rsi.runtime_stats_interval_id
ORDER BY rs.avg_logical_io_reads DESC;

-- Regressed query candidates.
SELECT TOP (25)
    q.query_id,
    qt.query_sql_text,
    p.plan_id,
    rs.avg_duration,
    rs.count_executions,
    p.is_forced_plan
FROM sys.query_store_query q
INNER JOIN sys.query_store_query_text qt ON q.query_text_id = qt.query_text_id
INNER JOIN sys.query_store_plan p ON q.query_id = p.query_id
INNER JOIN sys.query_store_runtime_stats rs ON p.plan_id = rs.plan_id
WHERE rs.count_executions > 5
ORDER BY rs.avg_duration DESC;

