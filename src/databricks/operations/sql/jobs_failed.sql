SELECT *
FROM system.lakeflow.job_task_run_timeline
WHERE result_state = 'FAILED'
  AND start_time >= current_timestamp() - INTERVAL 1 DAY;

