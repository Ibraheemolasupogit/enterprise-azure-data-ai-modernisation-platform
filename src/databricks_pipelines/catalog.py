from __future__ import annotations

# ruff: noqa: E501
from databricks_pipelines.model import (
    DataModelItem,
    GoldProduct,
    SourceIngestion,
    StrategyItem,
    TableCatalog,
    TraceabilityItem,
    TransformationCatalog,
)

INGESTION = [
    SourceIngestion("legacy_tms", "incremental/CDC-oriented relational ingestion", "5-15 minutes after source validation", "abfss://landing@<env-storage>/legacy_tms/", "bronze.legacy_tms_changes", "data/contracts/databricks/bronze_legacy_tms_changes.schema.json", "required: abfss://checkpoints/<env>/legacy_tms/", "source change_version or updated_at high-water mark; deterministic local fixture models changes", "invalid change envelopes to quarantine; failed batch replay from checkpoint", "replay from landing version and high-water mark", "MERGE by source table and business key with change_version ordering", "configuration defined"),
    SourceIngestion("billing_ops", "batch/incremental relational ingestion", "hourly or daily depending on table", "abfss://landing@<env-storage>/billing_ops/", "bronze.billing_ops_invoices", "data/contracts/databricks/bronze_billing_ops_invoices.schema.json", "required for incremental loads", "invoice_date/updated_at watermark; delete feed modelled as tombstone flag", "amount/type defects to quarantine", "replay by batch_id and source extract timestamp", "MERGE by invoice_id and source extract timestamp", "configuration defined"),
    SourceIngestion("depot_reference_feed", "batch file ingestion using COPY INTO", "daily or on reference release", "abfss://landing@<env-storage>/partner/depot_reference/", "bronze.depot_reference_feed", "data/contracts/databricks/bronze_depot_reference_feed.schema.json", "optional batch manifest checkpoint", "feed_version and file modification time", "missing capacity accepted with quarantine warning", "reprocess file version from landing", "COPY INTO file tracking plus natural-key merge", "configuration defined"),
    SourceIngestion("carrier_updates", "Auto Loader JSON ingestion", "continuously arriving files", "abfss://landing@<env-storage>/partner/carrier_updates/", "bronze.carrier_updates", "data/contracts/databricks/bronze_carrier_updates.schema.json", "required: schemaLocation and checkpointLocation", "update_timestamp watermark; rescued data captures drift", "additive fields rescued/evolved after review; type changes quarantined", "checkpoint reset requires replay plan and schema snapshot", "cloudFiles exactly-once file discovery plus dedupe by carrier_update_id", "configuration defined"),
    SourceIngestion("customer_service_export", "batch CSV ingestion", "daily", "abfss://landing@<env-storage>/customer_service_export/", "bronze.customer_service_export", "data/contracts/databricks/bronze_customer_service_export.schema.json", "batch manifest checkpoint", "opened_at extract watermark", "malformed email/detail records to quarantine", "replay by extract date and file hash", "dedupe by case_id and opened_at", "configuration defined"),
    SourceIngestion("shipment_operational_events", "Structured Streaming event ingestion", "continuous", "abfss://landing@<env-storage>/events/shipment_operational_events/", "bronze.shipment_operational_events", "data/contracts/databricks/bronze_shipment_operational_events.schema.json", "required streaming checkpoint", "event-time watermark on occurred_at", "duplicate and late events to quarantine stream", "replay from event log with checkpoint reset approval", "dedupe by event_id and event-time watermark", "configuration defined"),
]

BRONZE_TABLES = [
    TableCatalog("bronze.legacy_tms_changes", "legacy_tms", "one source change record", "source_table,business_key,change_version", "_ingested_at_utc,_source_system,_source_file,_schema_version,_record_hash,_raw_payload", "Delta CDF enabled after Databricks validation", "mixed", "configuration defined"),
    TableCatalog("bronze.billing_ops_invoices", "billing_ops", "one invoice extract row", "invoice_id", "_ingested_at_utc,_source_system,_source_file,_schema_version,_record_hash", "Delta MERGE target; CDF candidate", "commercial", "configuration defined"),
    TableCatalog("bronze.depot_reference_feed", "depot_reference_feed", "one depot reference row per feed", "depot_code,feed_version", "_ingested_at_utc,_source_system,_source_file,_schema_version,_record_hash,_raw_payload", "COPY INTO file tracking", "internal", "configuration defined"),
    TableCatalog("bronze.carrier_updates", "carrier_updates", "one carrier update event", "carrier_update_id", "_ingested_at_utc,_source_system,_source_file,_schema_version,_record_hash,_rescued_data", "Auto Loader schema evolution and rescued data column", "internal", "configuration defined"),
    TableCatalog("bronze.customer_service_export", "customer_service_export", "one exported service case row", "case_id", "_ingested_at_utc,_source_system,_source_file,_schema_version,_record_hash", "COPY INTO/Auto Loader candidate", "restricted", "configuration defined"),
    TableCatalog("bronze.shipment_operational_events", "shipment_operational_events", "one operational event delivery", "event_id", "_ingested_at_utc,_source_system,_event_metadata,_schema_version,_record_hash,_raw_payload", "Structured Streaming append with checkpoint", "internal", "configuration defined"),
]

SILVER_TRANSFORMATIONS = [
    TransformationCatalog("silver.shipments", "bronze.legacy_tms_changes", "type normalization, status normalization, dedupe, referential checks", "required shipment/customer/route ids; valid timestamps; valid status; non-negative amount", "silver.shipments", "quarantine.invalid_shipments", "locally validated"),
    TransformationCatalog("silver.shipment_events", "bronze.shipment_operational_events", "streaming event normalization, watermark dedupe, late-event routing", "required event id; valid event time; duplicate id; out-of-order event", "silver.shipment_events", "quarantine.invalid_shipment_events", "locally validated"),
    TransformationCatalog("silver.customer_accounts", "bronze.legacy_tms_changes", "customer normalization and SCD2 preparation", "required customer id; valid email; duplicate account number flagged", "silver.customer_accounts", "quarantine.invalid_customers", "locally validated"),
    TransformationCatalog("silver.depots_routes", "bronze.depot_reference_feed; bronze.legacy_tms_changes", "reference normalization and route enrichment", "valid depot codes; capacity sanity; route depot references", "silver.depots_routes", "quarantine.invalid_depots_routes", "locally validated"),
    TransformationCatalog("silver.billing_invoices", "bronze.billing_ops_invoices", "amount typing and invoice status normalization", "positive amounts; valid dates; known invoice status", "silver.billing_invoices", "quarantine.invalid_billing", "locally validated"),
    TransformationCatalog("silver.service_cases", "bronze.customer_service_export; bronze.billing_ops_service_cases", "case normalization and shipment/customer reference validation", "valid case id; valid email; known shipment", "silver.service_cases", "quarantine.invalid_service_cases", "locally validated"),
]

GOLD_PRODUCTS = [
    GoldProduct("gold.shipment_operations_performance", "daily by shipment status", "silver.shipments", "shipment_count, open_count, delivered_count", "operational analytics and BI serving", "no direct PII", "locally validated"),
    GoldProduct("gold.depot_route_performance", "daily by route and depot", "silver.shipments; silver.depots_routes", "shipment_count, on_time_count, delayed_count", "depot and route performance", "regional row filters apply", "configuration defined"),
    GoldProduct("gold.delivery_delay_metrics", "delivery date", "silver.shipments; silver.shipment_events", "delivered_count, late_count, late_rate, rolling late rate", "SLA and delay analysis", "no direct PII", "locally validated"),
    GoldProduct("gold.billing_revenue_summary", "invoice month and status", "silver.billing_invoices", "invoice_count, net_revenue_gbp, paid_amount_gbp", "revenue operations summary", "commercial sensitivity tag", "locally validated"),
    GoldProduct("gold.service_incident_summary", "daily by case reason/status", "silver.service_cases", "case_count, open_count, resolved_count", "service and incident trend analysis", "case detail excluded", "configuration defined"),
]

DATA_MODEL = [
    DataModelItem("dim_customer", "dimension", "one row per customer version", "customer_id", "customer_sk", "legacy_tms; billing_ops", "SCD Type 2 with hash change detection", "late facts resolve to current or inferred customer row"),
    DataModelItem("dim_depot", "dimension", "one row per depot", "depot_code", "depot_sk", "legacy_tms; depot_reference_feed", "Type 1 for descriptive corrections; future Type 2 if operations require", "late facts use unknown depot member until reference arrives"),
    DataModelItem("dim_route", "dimension", "one row per route version", "route_code", "route_sk", "legacy_tms; depot_reference_feed", "Type 2 candidate for depot/path changes", "late facts use route effective date"),
    DataModelItem("dim_vehicle", "dimension", "one row per vehicle", "vehicle_id", "vehicle_sk", "legacy_tms", "Type 1 initially", "late facts use unknown vehicle member"),
    DataModelItem("dim_date", "dimension", "one row per calendar date", "date_key", "date_sk", "derived", "static", "not applicable"),
    DataModelItem("fact_shipments", "fact", "one row per shipment", "shipment_id", "shipment_sk", "legacy_tms", "facts can be updated by CDC MERGE", "late dimensions resolved by surrogate-key repair"),
    DataModelItem("fact_shipment_events", "fact", "one row per accepted event", "event_id", "event_sk", "shipment_operational_events", "append with dedupe", "late events accepted within watermark then quarantined/replayed by approval"),
    DataModelItem("fact_billing_invoices", "fact", "one row per invoice", "invoice_id", "invoice_sk", "billing_ops", "MERGE by invoice id and update timestamp", "late customer/shipment references resolved by inferred members"),
    DataModelItem("fact_service_cases", "fact", "one row per service case", "case_id", "case_sk", "billing_ops; customer_service_export", "MERGE by case id", "unknown shipment references quarantined"),
]

SCD = [
    StrategyItem("scd-001", "SCD Type 2", "dim_customer", "business key customer_id; surrogate key customer_sk; effective_start_utc; effective_end_utc; is_current; change_hash", "Customer tier, legal name, and billing region changes require analytical history.", "locally validated"),
    StrategyItem("scd-002", "MERGE pattern", "dim_customer", "close current row when hash differs, insert new current row, keep unchanged rows untouched", "Deterministic history tracking without operational temporal-table claims.", "locally validated"),
    StrategyItem("scd-003", "late-arriving dimension", "dim_customer", "use inferred member for late facts, then repair surrogate key when dimension arrives", "Preserves fact records without dropping late-arriving data.", "configuration defined"),
]

SCHEMA_DRIFT = [
    StrategyItem("drift-001", "additive field", "carrier_updates.partner_eta_text", "rescue in _rescued_data and evolve schema after contract review", "Schema version 2 fixture adds ETA text safely.", "locally validated"),
    StrategyItem("drift-002", "unexpected field", "carrier_updates.*", "rescue and alert; do not expose to Silver until reviewed", "Prevents silent business semantics changes.", "configuration defined"),
    StrategyItem("drift-003", "changed type", "carrier_updates.schema_version", "quarantine and fail contract validation", "Dangerous type changes should not be coerced silently.", "configuration defined"),
    StrategyItem("drift-004", "malformed JSON", "carrier_updates file", "route raw payload to quarantine with parser error", "Malformed payload remains auditable.", "configuration defined"),
]

CHECKPOINTS = [
    StrategyItem("chk-001", "checkpoint", "legacy_tms", "abfss://checkpoints/<env>/legacy_tms/", "incremental high-water mark and MERGE replay state", "configuration defined"),
    StrategyItem("chk-002", "checkpoint", "carrier_updates", "abfss://checkpoints/<env>/autoloader/carrier_updates/", "Auto Loader exactly-once file discovery and schema state", "configuration defined"),
    StrategyItem("chk-003", "checkpoint", "shipment_operational_events", "abfss://checkpoints/<env>/streaming/shipment_operational_events/", "Structured Streaming offset and watermark state", "configuration defined"),
    StrategyItem("chk-004", "schema location", "carrier_updates", "abfss://checkpoints/<env>/schemas/carrier_updates/", "Auto Loader schema inference and evolution state", "configuration defined"),
]

QUARANTINE = [
    StrategyItem("qr-001", "required identifiers", "shipments/events/cases", "missing business keys are rejected to quarantine", "No orphan facts in Silver.", "locally validated"),
    StrategyItem("qr-002", "referential validation", "service_cases", "unknown shipment ids are quarantined", "Preserves invalid records for triage.", "locally validated"),
    StrategyItem("qr-003", "schema drift", "carrier_updates", "changed types and malformed JSON are quarantined", "Avoids dangerous coercion.", "configuration defined"),
    StrategyItem("qr-004", "late events", "shipment_operational_events", "events outside watermark routed to quarantine or replay workflow", "Streaming semantics are explicit.", "locally validated"),
    StrategyItem("qr-005", "amount sanity", "billing_invoices", "negative or non-numeric amounts are quarantined", "Protects revenue aggregates.", "configuration defined"),
]

REPLAY = [
    StrategyItem("replay-001", "file replay", "depot_reference_feed; customer_service_export", "replay by source file hash/version through COPY INTO or manifest reset", "Effectively-once file processing with explicit reset.", "configuration defined"),
    StrategyItem("replay-002", "event replay", "shipment_operational_events", "replay event log after checkpoint reset approval; dedupe by event_id", "Duplicate delivery is expected and handled.", "locally validated"),
    StrategyItem("replay-003", "CDC replay", "legacy_tms", "replay from source change_version high-water mark and MERGE idempotently", "Does not fake SQL MI CDC runtime.", "configuration defined"),
    StrategyItem("replay-004", "partial batch failure", "all batch sources", "write Bronze append first, then idempotent Silver MERGE after validation", "Recovery can restart from Bronze without data loss.", "configuration defined"),
]

PHYSICAL_LAYOUT = [
    StrategyItem("layout-001", "physical layout", "bronze.shipment_operational_events", "liquid clustering by shipment_id,event_type after runtime validation; no small static partitioning", "Evolving event access patterns suit clustering better than brittle partitions.", "configuration defined"),
    StrategyItem("layout-002", "physical layout", "silver.shipments", "liquid clustering by shipment_id,route_code,billing_region", "Common filters are shipment, route, and region.", "configuration defined"),
    StrategyItem("layout-003", "physical layout", "gold.delivery_delay_metrics", "no partitioning initially; table is small aggregate", "Avoids small-file/partition overhead.", "configuration defined"),
    StrategyItem("layout-004", "physical layout", "fact_billing_invoices", "partition by invoice_month only when volume justifies", "Monthly revenue filters are common but current model remains modest.", "configuration defined"),
    StrategyItem("layout-005", "physical layout", "dimensions", "no partitioning for small dimensions", "Small dimensions should not be over-partitioned.", "configuration defined"),
]

TRACEABILITY = [
    TraceabilityItem("legacy_tms", "incremental/CDC-oriented relational ingestion", "bronze.legacy_tms_changes", "silver.shipments; silver.customer_accounts", "gold.shipment_operations_performance; gold.delivery_delay_metrics", "operational analytics; BI serving", "configuration defined"),
    TraceabilityItem("billing_ops", "batch/incremental relational ingestion", "bronze.billing_ops_invoices", "silver.billing_invoices", "gold.billing_revenue_summary", "revenue operations", "configuration defined"),
    TraceabilityItem("depot_reference_feed", "batch file ingestion using COPY INTO", "bronze.depot_reference_feed", "silver.depots_routes", "gold.depot_route_performance", "route/depot analytics", "configuration defined"),
    TraceabilityItem("carrier_updates", "Auto Loader JSON ingestion", "bronze.carrier_updates", "silver.shipment_events", "gold.delivery_delay_metrics", "delivery exception analytics", "configuration defined"),
    TraceabilityItem("customer_service_export", "batch CSV ingestion", "bronze.customer_service_export", "silver.service_cases", "gold.service_incident_summary", "service operations", "configuration defined"),
    TraceabilityItem("shipment_operational_events", "Structured Streaming event ingestion", "bronze.shipment_operational_events", "silver.shipment_events", "gold.shipment_operations_performance; gold.delivery_delay_metrics", "event-driven operational analytics", "configuration defined"),
]

READINESS = [
    StrategyItem("ready-001", "ingestion", "all current source domains", "source ingestion matrix covers mode, landing, Bronze, contract, checkpoint, watermark, replay, idempotency", "Ready for Databricks runtime validation.", "locally validated"),
    StrategyItem("ready-002", "Bronze", "all ingestion sources", "Bronze catalog preserves fidelity and metadata", "No premature business transformation.", "configuration defined"),
    StrategyItem("ready-003", "Silver", "core analytical entities", "Pure functions validate normalization, dedupe, quarantine, and referential handling", "Transformation logic is locally testable.", "locally validated"),
    StrategyItem("ready-004", "Gold", "five representative products", "Gold products have grain, measures, and use cases", "BI/Fabric assets are deferred.", "locally validated"),
    StrategyItem("ready-005", "Databricks runtime", "Spark, Auto Loader, Structured Streaming, Delta MERGE", "runtime behavior requires Databricks workspace execution", "No fake runtime evidence.", "requires Databricks runtime validation"),
]

