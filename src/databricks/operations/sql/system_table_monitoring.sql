-- Databricks system-table monitoring query pack.
-- These queries require a Databricks workspace/account with system tables enabled.

-- failed jobs
SELECT
  workspace_id,
  job_id,
  run_id,
  task_key,
  result_state,
  termination_code,
  start_time,
  end_time
FROM system.lakeflow.job_task_run_timeline
WHERE result_state = 'FAILED'
  AND start_time >= current_timestamp() - INTERVAL 7 DAYS;

-- long-running jobs
SELECT
  workspace_id,
  job_id,
  run_id,
  task_key,
  start_time,
  end_time,
  unix_timestamp(end_time) - unix_timestamp(start_time) AS duration_seconds
FROM system.lakeflow.job_task_run_timeline
WHERE end_time IS NOT NULL
  AND unix_timestamp(end_time) - unix_timestamp(start_time) > 3600;

-- expensive workloads and cost attribution
SELECT
  workspace_id,
  usage_date,
  usage_metadata.job_id,
  usage_metadata.cluster_id,
  sku_name,
  custom_tags.environment,
  custom_tags.workload,
  custom_tags.domain,
  SUM(usage_quantity) AS usage_quantity
FROM system.billing.usage
GROUP BY
  workspace_id,
  usage_date,
  usage_metadata.job_id,
  usage_metadata.cluster_id,
  sku_name,
  custom_tags.environment,
  custom_tags.workload,
  custom_tags.domain;

-- SQL query latency and scan pressure
SELECT
  workspace_id,
  statement_id,
  executed_by,
  warehouse_id,
  execution_status,
  total_duration_ms,
  read_bytes,
  read_rows
FROM system.query.history
WHERE start_time >= current_timestamp() - INTERVAL 7 DAYS
ORDER BY total_duration_ms DESC;

-- user and service-principal activity
SELECT
  event_time,
  service_name,
  action_name,
  user_identity.email,
  request_params
FROM system.access.audit
WHERE event_time >= current_timestamp() - INTERVAL 7 DAYS;

-- lineage investigation
SELECT
  source_table_full_name,
  target_table_full_name,
  created_by,
  event_time
FROM system.access.table_lineage
WHERE target_table_full_name LIKE 'contoso_freight_%';

