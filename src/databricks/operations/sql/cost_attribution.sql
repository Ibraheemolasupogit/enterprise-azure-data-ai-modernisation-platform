SELECT
  usage_date,
  workspace_id,
  sku_name,
  custom_tags.environment,
  custom_tags.workload,
  custom_tags.domain,
  usage_metadata.job_id,
  SUM(usage_quantity) AS usage_quantity
FROM system.billing.usage
GROUP BY
  usage_date,
  workspace_id,
  sku_name,
  custom_tags.environment,
  custom_tags.workload,
  custom_tags.domain,
  usage_metadata.job_id;

