-- Local evidence table shape; replace with production quality evidence table in Databricks.
SELECT
  dataset,
  critical_failures,
  quarantined_count,
  freshness_status
FROM contoso_freight_prod.audit.quality_results
WHERE critical_failures > 0
   OR freshness_status LIKE '%breach%';

