CREATE OR REPLACE VIEW ${catalog}.gold.shipment_operations_performance AS
SELECT
  DATE(created_at_utc) AS metric_date,
  shipment_status,
  COUNT(*) AS shipment_count,
  COUNT_IF(shipment_status <> 'delivered') AS open_count,
  COUNT_IF(shipment_status = 'delivered') AS delivered_count
FROM ${catalog}.silver.shipments
GROUP BY DATE(created_at_utc), shipment_status;

CREATE OR REPLACE VIEW ${catalog}.gold.depot_route_performance AS
SELECT
  DATE(s.created_at_utc) AS metric_date,
  r.depot_code,
  s.route_id,
  COUNT(*) AS shipment_count,
  COUNT_IF(s.delivered_at_utc <= s.promised_delivery_at_utc) AS on_time_count,
  COUNT_IF(s.shipment_status = 'delayed') AS delayed_count
FROM ${catalog}.silver.shipments AS s
LEFT JOIN ${catalog}.silver.depots_routes AS r
  ON s.route_id = r.route_id
GROUP BY DATE(s.created_at_utc), r.depot_code, s.route_id;

CREATE OR REPLACE VIEW ${catalog}.gold.delivery_delay_metrics AS
SELECT
  DATE(delivered_at_utc) AS metric_date,
  COUNT(*) AS delivered_count,
  COUNT_IF(delivered_at_utc > promised_delivery_at_utc) AS late_count,
  AVG(CASE WHEN delivered_at_utc > promised_delivery_at_utc THEN 1 ELSE 0 END) AS late_rate
FROM ${catalog}.silver.shipments
WHERE delivered_at_utc IS NOT NULL
GROUP BY DATE(delivered_at_utc);

CREATE OR REPLACE VIEW ${catalog}.gold.billing_revenue_summary AS
SELECT
  DATE_TRUNC('month', invoice_date) AS invoice_month,
  invoice_status,
  COUNT(*) AS invoice_count,
  SUM(CASE WHEN invoice_status <> 'void' THEN net_amount_gbp ELSE 0 END) AS net_revenue_gbp
FROM ${catalog}.silver.billing_invoices
GROUP BY DATE_TRUNC('month', invoice_date), invoice_status;

CREATE OR REPLACE VIEW ${catalog}.gold.service_incident_summary AS
SELECT
  DATE(opened_at_utc) AS metric_date,
  case_reason,
  case_status,
  COUNT(*) AS case_count
FROM ${catalog}.silver.service_cases
GROUP BY DATE(opened_at_utc), case_reason, case_status;

