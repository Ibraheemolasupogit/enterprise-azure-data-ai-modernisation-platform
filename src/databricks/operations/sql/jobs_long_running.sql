SELECT
  job_id,
  run_id,
  task_key,
  unix_timestamp(end_time) - unix_timestamp(start_time) AS duration_seconds
FROM system.lakeflow.job_task_run_timeline
WHERE end_time IS NOT NULL
ORDER BY duration_seconds DESC;

