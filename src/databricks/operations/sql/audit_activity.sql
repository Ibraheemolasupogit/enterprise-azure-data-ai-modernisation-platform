SELECT
  event_time,
  service_name,
  action_name,
  user_identity.email,
  source_ip_address,
  request_params
FROM system.access.audit
WHERE event_time >= current_timestamp() - INTERVAL 7 DAYS
ORDER BY event_time DESC;

