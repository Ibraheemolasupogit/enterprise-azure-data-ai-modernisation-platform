-- Representative Unity Catalog objects. These are DDL assets only; pipelines are deferred.

CREATE TABLE IF NOT EXISTS contoso_freight_prod.bronze.shipment_events_raw (
    event_id STRING COMMENT 'Synthetic operational event identifier.',
    shipment_code STRING COMMENT 'Source shipment business key.',
    event_type STRING COMMENT 'Raw event type from source.',
    event_timestamp_utc TIMESTAMP COMMENT 'UTC timestamp supplied by source.',
    source_system STRING COMMENT 'Source system name.',
    payload_json STRING COMMENT 'Raw event payload retained for future parsing.',
    ingestion_batch_id STRING COMMENT 'Future ingestion batch identifier.',
    ingested_at_utc TIMESTAMP COMMENT 'Future ingestion timestamp.'
)
USING DELTA
TBLPROPERTIES (
    'delta.logRetentionDuration' = 'interval 90 days',
    'delta.deletedFileRetentionDuration' = 'interval 14 days',
    'contoso.domain' = 'shipment',
    'contoso.lifecycle' = 'bronze',
    'contoso.sensitivity' = 'internal'
)
COMMENT 'Raw shipment event records for future Bronze ingestion.';

CREATE TABLE IF NOT EXISTS contoso_freight_prod.silver.shipments (
    shipment_id BIGINT COMMENT 'Analytical shipment surrogate key.',
    shipment_code STRING COMMENT 'Shipment business key.',
    customer_code STRING COMMENT 'Customer business key.',
    route_code STRING COMMENT 'Route business key.',
    billing_region STRING COMMENT 'Billing or operating region used for row filtering.',
    shipment_status STRING COMMENT 'Current shipment status.',
    promised_delivery_at_utc TIMESTAMP COMMENT 'Promised delivery timestamp.',
    delivered_at_utc TIMESTAMP COMMENT 'Actual delivery timestamp when available.'
)
USING DELTA
TBLPROPERTIES (
    'delta.logRetentionDuration' = 'interval 180 days',
    'delta.deletedFileRetentionDuration' = 'interval 30 days',
    'contoso.domain' = 'shipment',
    'contoso.lifecycle' = 'silver',
    'contoso.sensitivity' = 'internal'
)
COMMENT 'Conformed shipment records for future analytical processing.';

CREATE TABLE IF NOT EXISTS contoso_freight_prod.silver.customer_accounts (
    customer_code STRING COMMENT 'Customer business key.',
    account_number STRING COMMENT 'Account reference.',
    legal_name STRING COMMENT 'Customer legal name.',
    service_tier STRING COMMENT 'Service tier.',
    billing_region STRING COMMENT 'Billing region.',
    contact_email STRING COMMENT 'Customer contact email; protected by masking policy.',
    is_active BOOLEAN COMMENT 'Active account indicator.'
)
USING DELTA
TBLPROPERTIES (
    'delta.logRetentionDuration' = 'interval 180 days',
    'delta.deletedFileRetentionDuration' = 'interval 30 days',
    'contoso.domain' = 'customer',
    'contoso.lifecycle' = 'silver',
    'contoso.pii' = 'email',
    'contoso.sensitivity' = 'confidential'
)
COMMENT 'Conformed customer account data with protected contact details.';

CREATE TABLE IF NOT EXISTS contoso_freight_prod.reference.depots_routes (
    depot_code STRING COMMENT 'Depot business key.',
    depot_name STRING COMMENT 'Depot display name.',
    route_code STRING COMMENT 'Route business key.',
    region STRING COMMENT 'Operating region.',
    planned_hours INT COMMENT 'Reference transit duration.'
)
USING DELTA
TBLPROPERTIES (
    'delta.logRetentionDuration' = 'interval 365 days',
    'delta.deletedFileRetentionDuration' = 'interval 30 days',
    'contoso.domain' = 'depot_route',
    'contoso.lifecycle' = 'reference',
    'contoso.sensitivity' = 'internal'
)
COMMENT 'Depot and route reference data.';

CREATE TABLE IF NOT EXISTS contoso_freight_prod.silver.billing_service_cases (
    case_id STRING COMMENT 'Service case identifier.',
    customer_code STRING COMMENT 'Customer business key.',
    shipment_code STRING COMMENT 'Related shipment when present.',
    case_status STRING COMMENT 'Current case status.',
    case_detail STRING COMMENT 'Restricted service-case narrative text.',
    opened_at_utc TIMESTAMP COMMENT 'Case opened timestamp.'
)
USING DELTA
TBLPROPERTIES (
    'delta.logRetentionDuration' = 'interval 180 days',
    'delta.deletedFileRetentionDuration' = 'interval 30 days',
    'contoso.domain' = 'billing_service',
    'contoso.lifecycle' = 'silver',
    'contoso.sensitivity' = 'restricted'
)
COMMENT 'Conformed billing and service case boundary for future analytics.';

CREATE VOLUME IF NOT EXISTS contoso_freight_prod.quarantine.invalid_records
COMMENT 'Managed volume for rejected records and triage payloads.';

CREATE TABLE IF NOT EXISTS contoso_freight_prod.audit.data_quality_events (
    event_id STRING COMMENT 'Quality event identifier.',
    source_object STRING COMMENT 'Object that produced the event.',
    rule_id STRING COMMENT 'Data quality rule identifier.',
    severity STRING COMMENT 'Rule severity.',
    event_payload STRING COMMENT 'Evidence payload.',
    created_at_utc TIMESTAMP COMMENT 'Event timestamp.'
)
USING DELTA
COMMENT 'Future data quality and pipeline audit events.';

CREATE VIEW IF NOT EXISTS contoso_freight_prod.gold.shipment_reliability
COMMENT 'Curated future operational analytics view over shipment reliability.'
AS
SELECT
    s.route_code,
    s.billing_region,
    s.shipment_status,
    COUNT(*) AS shipment_count,
    COUNT_IF(s.delivered_at_utc <= s.promised_delivery_at_utc) AS on_time_count
FROM contoso_freight_prod.silver.shipments AS s
GROUP BY s.route_code, s.billing_region, s.shipment_status;

