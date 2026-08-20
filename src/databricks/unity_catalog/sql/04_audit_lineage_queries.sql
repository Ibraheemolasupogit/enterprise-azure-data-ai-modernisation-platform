-- Representative Databricks system-table queries.
-- These require a real Databricks account with system schemas enabled.

SELECT
    event_time,
    user_identity.email,
    action_name,
    request_params
FROM system.access.audit
WHERE service_name = 'unityCatalog'
  AND event_time >= current_timestamp() - INTERVAL 7 DAYS;

SELECT
    event_time,
    workspace_id,
    cluster_id,
    event_type,
    details
FROM system.compute.clusters
WHERE event_time >= current_timestamp() - INTERVAL 7 DAYS;

SELECT
    source_table_full_name,
    target_table_full_name,
    created_by,
    event_time
FROM system.access.table_lineage
WHERE target_table_full_name LIKE 'contoso_freight_prod.%';

SELECT
    source_table_full_name,
    target_table_full_name,
    source_column_name,
    target_column_name,
    event_time
FROM system.access.column_lineage
WHERE target_table_full_name LIKE 'contoso_freight_prod.%';

