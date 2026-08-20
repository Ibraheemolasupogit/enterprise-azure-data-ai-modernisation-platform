# Databricks Ingestion and Medallion Processing

Milestone 10 implements the core Databricks data-engineering layer for Contoso Freight. It is built as testable Python and Databricks-ready Spark/SQL assets, with deterministic local evidence. It does not run Azure Databricks, Lakeflow orchestration, monitoring/optimization, AI/RAG, API integration, Fabric, or production assurance.

## Ingestion Patterns

Source ingestion is defined for:

- `legacy_tms`: incremental/CDC-oriented relational ingestion.
- `billing_ops`: batch/incremental relational ingestion.
- `depot_reference_feed`: batch file ingestion using SQL `COPY INTO`.
- `carrier_updates`: Auto Loader JSON ingestion with schema rescue/evolution.
- `customer_service_export`: batch CSV ingestion.
- `shipment_operational_events`: Structured Streaming event ingestion.

Each path has a Bronze target, landing path, data contract, checkpoint or manifest strategy, watermark/change-tracking approach, error handling, replay model, and idempotency strategy.

## Bronze

Bronze preserves source fidelity. Records retain source identifiers, ingestion timestamp, source ordinal or file/event metadata, schema version, record hash, and raw payload where useful. Bronze does not perform business cleanup.

## Silver

Silver transformations normalize types, timestamps, statuses, identifiers, and source-specific fields. They apply transformation-level checks for required identifiers, timestamps, statuses, depot/route references, duplicate keys, email shape, and amount sanity. Invalid records are routed to quarantine rather than dropped.

## Streaming and Auto Loader

Carrier updates use Auto Loader design with `cloudFiles`, `schemaLocation`, `checkpointLocation`, schema inference/evolution, and rescued data. Shipment operational events use Structured Streaming semantics with event time, watermarking, event-id dedupe, append mode, and explicit late-event handling.

These are configuration-defined assets. Exactly-once file discovery, streaming offsets, and watermark behavior require Databricks runtime validation.

## CDC and Replay

The CDC design uses source watermarks or change versions, high-water marks, insert/update/delete semantics, idempotent Delta `MERGE`, and replay from Bronze or landing. Local fixtures simulate change/event anomalies; they do not claim SQL MI CDC execution.

## Data Model

The analytical model includes customer, depot, route, vehicle, and date dimensions plus shipment, shipment event, billing invoice, and service case facts. Grains, keys, source systems, slowly changing behavior, and late-arriving handling are captured in generated evidence.

## SCD Type 2

`dim_customer` is modeled as SCD Type 2 with `customer_id`, `customer_sk`, `effective_start_utc`, `effective_end_utc`, `is_current`, and `change_hash`. The local Python implementation validates deterministic row closing and new-version insertion.

## Gold Products

Representative Gold products are:

- Shipment operations performance.
- Depot/route performance.
- Delivery delay metrics.
- Billing/revenue summary.
- Service/incident summary.

Gold assets define business grain and measures, and are intended for later BI, operational analytics, and governed downstream consumption.

## Schema Drift and Quarantine

Carrier update schema drift covers additive fields, unexpected fields, changed types, and malformed JSON behavior. Additive fields are rescued and reviewed before promotion. Dangerous type changes and malformed records are quarantined.

## Physical Layout

The strategy avoids partitioning small dimensions or small aggregate tables. Liquid clustering is preferred for evolving high-value analytical access patterns, subject to Databricks runtime validation. OPTIMIZE and VACUUM are not executed locally.

## Local Validation Boundary

Local validation covers deterministic metadata, transformation functions, dedupe, normalization, SCD2 behavior, late-arriving records, schema drift detection, quarantine routing, replay/idempotency evidence, Gold aggregates, and traceability. Databricks runtime validation remains required for Auto Loader, Structured Streaming, Delta MERGE/CDF, schema evolution, liquid clustering, and performance.

