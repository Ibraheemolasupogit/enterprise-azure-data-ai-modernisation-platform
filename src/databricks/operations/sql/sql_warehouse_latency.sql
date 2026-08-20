SELECT
  warehouse_id,
  statement_id,
  total_duration_ms,
  waiting_at_capacity_duration_ms,
  execution_status
FROM system.query.history
WHERE start_time >= current_timestamp() - INTERVAL 7 DAYS
ORDER BY total_duration_ms DESC;

