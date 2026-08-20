SELECT
  workspace_id,
  cluster_id,
  event_type,
  event_time,
  details
FROM system.compute.clusters
WHERE event_time >= current_timestamp() - INTERVAL 7 DAYS;

