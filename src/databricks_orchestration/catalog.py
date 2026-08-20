from __future__ import annotations

# ruff: noqa: E501
from pathlib import Path

from databricks_orchestration.model import (
    JobItem,
    MatrixItem,
    PermissionItem,
    QualityResult,
    QualityRule,
    QuarantineItem,
    RetryPolicy,
    ScheduleItem,
    SeverityAction,
    TaskDependency,
    TraceabilityItem,
)
from databricks_orchestration.quality import evaluate_fixture_quality

FIXTURE_ROOT = Path("data/samples/legacy_estate/tiny")

QUALITY_RULES = [
    QualityRule("bronze.shipment_operational_events", "Bronze", "br_evt_001", "schema conformity", "event_id,event_type,aggregate_id,occurred_at", "record conforms to event contract", "ERROR", "quarantine", "data engineering", "locally validated"),
    QualityRule("bronze.shipment_operational_events", "Bronze", "br_evt_002", "uniqueness", "event_id", "duplicate event deliveries are detected", "WARNING", "quarantine duplicate", "data engineering", "locally validated"),
    QualityRule("bronze.carrier_updates", "Bronze", "br_car_001", "schema conformity", "_rescued_data", "unexpected fields are rescued and reviewed", "WARNING", "quarantine if dangerous type change", "data engineering", "configuration defined"),
    QualityRule("bronze.depot_reference_feed", "Bronze", "br_dep_001", "completeness", "_ingested_at_utc,_source_system,_record_hash", "required ingestion metadata is present", "ERROR", "fail task", "data engineering", "configuration defined"),
    QualityRule("silver.shipments", "Silver", "sv_shp_001", "completeness", "shipment_id,customer_id,route_id", "required business keys are present", "CRITICAL", "fail task and stop downstream dependency", "data engineering", "locally validated"),
    QualityRule("silver.shipments", "Silver", "sv_shp_002", "validity", "shipment_status", "shipment status is in the normalized domain", "ERROR", "reject record", "data engineering", "locally validated"),
    QualityRule("silver.shipments", "Silver", "sv_shp_003", "referential integrity", "customer_id,route_id", "shipment references known customer and route", "CRITICAL", "quarantine and stop downstream dependency", "data engineering", "locally validated"),
    QualityRule("silver.billing_invoices", "Silver", "sv_inv_001", "business rule", "net_amount_gbp,tax_amount_gbp", "invoice amounts are non-negative unless explicitly credited", "ERROR", "reject record", "finance data owner", "configuration defined"),
    QualityRule("silver.service_cases", "Silver", "sv_case_001", "validity", "contact_email", "synthetic service email is well formed", "ERROR", "quarantine", "service data owner", "locally validated"),
    QualityRule("silver.service_cases", "Silver", "sv_case_002", "referential integrity", "shipment_id", "service case references known shipment", "ERROR", "quarantine", "service data owner", "locally validated"),
    QualityRule("silver.depots_routes", "Silver", "sv_dep_001", "completeness", "depot_code,capacity_units", "depot code exists; capacity warning when missing", "WARNING", "quarantine warning and manual review", "reference data owner", "locally validated"),
    QualityRule("silver.depots_routes", "Silver", "sv_dep_002", "consistency", "route_code,origin_depot,destination_depot", "route reference is internally consistent and not self-contradictory", "ERROR", "quarantine and manual review", "reference data owner", "configuration defined"),
    QualityRule("silver.shipment_events", "Silver", "sv_evt_001", "timeliness", "occurred_at_utc", "accepted event is within watermark or replay window", "WARNING", "quarantine late event for replay review", "data engineering", "locally validated"),
    QualityRule("gold.shipment_operations_performance", "Gold", "gd_ops_001", "grain uniqueness", "metric_date,shipment_status", "one KPI row per metric date/status", "CRITICAL", "fail task and block publication", "analytics owner", "configuration defined"),
    QualityRule("gold.delivery_delay_metrics", "Gold", "gd_delay_001", "aggregation consistency", "delivered_count,late_count,late_rate", "late count does not exceed delivered count and rate is between 0 and 1", "CRITICAL", "fail task and block publication", "analytics owner", "locally validated"),
    QualityRule("gold.billing_revenue_summary", "Gold", "gd_bill_001", "freshness", "invoice_month", "billing summary refreshes within daily threshold", "ERROR", "stop downstream publication", "finance data owner", "configuration defined"),
    QualityRule("gold.service_incident_summary", "Gold", "gd_case_001", "cross-product reconciliation", "case_count", "case aggregates reconcile to accepted Silver service cases", "ERROR", "fail task", "service data owner", "configuration defined"),
]

SEVERITY = [
    SeverityAction("INFO", "log only", "no retry required", "continue", "no"),
    SeverityAction("WARNING", "log and quarantine where relevant", "retry only for transient source issues", "continue unless threshold breached", "sometimes"),
    SeverityAction("ERROR", "reject record, quarantine, or fail task", "do not blindly retry deterministic data errors", "stop affected branch", "yes"),
    SeverityAction("CRITICAL", "fail task and stop downstream dependency", "no blind retry", "block Gold/publication", "yes"),
]


def quality_results() -> list[QualityResult]:
    return [
        QualityResult(dataset, **values, evidence_classification="locally validated")
        for dataset, values in evaluate_fixture_quality(FIXTURE_ROOT).items()
    ]


QUARANTINE = [
    QuarantineItem("quarantine.invalid_shipment_events", "bronze.shipment_operational_events", "br_evt_002", "event_id", "source_system,event_time,checkpoint,batch_id", "duplicate or late/out-of-order event", "2026-01-01T00:00:00Z", "retain original event payload", "open", "eligible after dedupe/replay review"),
    QuarantineItem("quarantine.invalid_service_cases", "silver.service_cases", "sv_case_001", "case_id", "source_file,row_number,extract_date", "invalid contact email", "2026-01-01T00:00:00Z", "retain restricted payload with UC controls", "open", "eligible after source correction"),
    QuarantineItem("quarantine.invalid_service_cases", "silver.service_cases", "sv_case_002", "case_id", "source_file,row_number,extract_date", "unknown shipment reference", "2026-01-01T00:00:00Z", "retain restricted payload with UC controls", "open", "eligible after reference repair"),
    QuarantineItem("quarantine.invalid_depots_routes", "silver.depots_routes", "sv_dep_001", "depot_code", "source_file,feed_version", "missing depot capacity warning", "2026-01-01T00:00:00Z", "retain source row", "review", "eligible after steward approval"),
]

JOBS = [
    JobItem("job-batch-feeds", "batch_feeds_workflow", "ingest and validate depot/customer-service/billing batch feeds", "python wheel/script and SQL tasks", "jobs compute", "environment,catalog,source_system,processing_date,load_type,replay_mode", 1, "configuration defined"),
    JobItem("job-relational-incremental", "relational_incremental_workflow", "incremental legacy_tms and billing_ops analytical loads", "python wheel/script task", "jobs compute", "environment,catalog,source_system,processing_date,checkpoint_path,load_type", 1, "configuration defined"),
    JobItem("job-events-streaming", "event_streaming_workflow", "run and quality-gate continuously arriving shipment events", "python wheel/script streaming task", "serverless jobs or jobs compute", "environment,catalog,checkpoint_path,replay_mode", 1, "configuration defined"),
    JobItem("job-gold-refresh", "gold_publication_workflow", "refresh Gold products only after validated Silver gates", "SQL task", "SQL warehouse", "environment,catalog,processing_date", 1, "configuration defined"),
    JobItem("job-backfill-replay", "controlled_backfill_replay_workflow", "controlled backfill and quarantine replay", "python wheel/script task", "jobs compute", "environment,catalog,source_range,target_range,replay_mode", 1, "configuration defined"),
]

DEPENDENCIES = [
    TaskDependency("batch_feeds_workflow", "landing_readiness", "", "landing files and manifests", "fail stops workflow", "no"),
    TaskDependency("batch_feeds_workflow", "bronze_ingestion", "landing_readiness", "source files", "retry transient source errors only", "no"),
    TaskDependency("batch_feeds_workflow", "bronze_quality_gate", "bronze_ingestion", "Bronze tables", "critical failure stops Silver", "no"),
    TaskDependency("batch_feeds_workflow", "silver_transformation", "bronze_quality_gate", "validated Bronze", "fail routes records to quarantine", "no"),
    TaskDependency("batch_feeds_workflow", "silver_quality_gate", "silver_transformation", "Silver tables", "critical failure blocks Gold", "no"),
    TaskDependency("gold_publication_workflow", "gold_transformation", "silver_quality_gate", "validated Silver", "run only after Silver gates pass", "no"),
    TaskDependency("gold_publication_workflow", "gold_quality_gate", "gold_transformation", "Gold products", "critical failure blocks publication", "no"),
    TaskDependency("gold_publication_workflow", "publish_readiness", "gold_quality_gate", "validated Gold", "publish only after gate pass", "yes"),
    TaskDependency("event_streaming_workflow", "streaming_ingestion", "", "event landing path/checkpoint", "stream restart for transient failure", "no"),
    TaskDependency("event_streaming_workflow", "streaming_quality_gate", "streaming_ingestion", "Bronze event stream", "schema/late-event failure quarantines or stops", "no"),
]

SCHEDULES = [
    ScheduleItem("batch_feeds_workflow", "daily 02:00 local time", "partner and service exports are daily files", "available by start of business", "6 hours late", "stale reference/service metrics", "data engineering on-call and source owner"),
    ScheduleItem("relational_incremental_workflow", "every 15 minutes during operating window", "legacy_tms operational analytics need frequent increments", "within 30 minutes", "45 minutes late", "stale shipment KPIs", "platform operator and operational data owner"),
    ScheduleItem("event_streaming_workflow", "continuous stream", "shipment events continuously arrive; scheduling is checkpoint-driven not batch-clock driven", "event visible within minutes after runtime validation", "30 minutes behind watermark", "delayed operational event visibility", "streaming operator"),
    ScheduleItem("gold_publication_workflow", "after successful Silver gates or hourly", "Gold should publish only from validated Silver", "hourly for operational products", "2 hours stale", "stale BI/analytics products", "analytics owner"),
    ScheduleItem("controlled_backfill_replay_workflow", "manual workflow_dispatch only", "backfills require isolation and approval", "case-specific", "case-specific", "incorrect historical correction risk", "data platform lead"),
]

RETRIES = [
    RetryPolicy("source unavailable", 3, 10, 60, "queued single concurrent run", "retry and escalate after attempts"),
    RetryPolicy("malformed source file", 0, 0, 30, "single run", "quarantine and manual review"),
    RetryPolicy("schema drift requiring manual intervention", 0, 0, 30, "single run", "stop downstream dependency and review contract"),
    RetryPolicy("bronze quality failure", 0, 0, 30, "single run", "quarantine/reject, no blind retry"),
    RetryPolicy("silver referential failure", 0, 0, 45, "single run", "quarantine and block Gold dependency"),
    RetryPolicy("transient platform failure", 2, 5, 90, "queued single concurrent run", "retry task"),
    RetryPolicy("streaming task failure", 5, 5, 0, "single active stream", "restart from checkpoint and escalate if repeated"),
    RetryPolicy("gold reconciliation failure", 0, 0, 30, "single run", "block publication and investigate"),
]

FAILURES = [
    MatrixItem("fail-001", "source unavailable", "landing_readiness", "source file or extract unavailable", "retry bounded attempts then escalate to source owner", "configuration defined"),
    MatrixItem("fail-002", "malformed source file", "bronze_ingestion", "CSV/JSON parse failure", "quarantine raw file and stop affected source branch", "configuration defined"),
    MatrixItem("fail-003", "schema drift", "carrier_updates", "unexpected dangerous type change", "rescue additive fields; quarantine/fail changed types", "configuration defined"),
    MatrixItem("fail-004", "Bronze quality failure", "bronze_quality_gate", "required metadata missing", "fail task and stop Silver dependency", "configuration defined"),
    MatrixItem("fail-005", "Silver referential integrity failure", "silver_quality_gate", "unknown customer/route/shipment reference", "quarantine and block Gold dependency when critical", "locally validated"),
    MatrixItem("fail-006", "stale checkpoint", "streaming_ingestion", "checkpoint prevents progress or is inconsistent", "pause stream, preserve checkpoint, clone for diagnosis, reset only by approval", "configuration defined"),
    MatrixItem("fail-007", "Gold reconciliation failure", "gold_quality_gate", "KPI grain or aggregate mismatch", "block publication and rerun from validated Silver after fix", "configuration defined"),
]

BACKFILL = [
    MatrixItem("bf-001", "backfill", "legacy_tms", "source range and target range provided", "isolate from current incremental processing; validate Bronze/Silver/Gold gates", "configuration defined"),
    MatrixItem("bf-002", "backfill", "shipment_operational_events", "event replay range", "do not overwrite streaming checkpoint; replay to isolated path then merge", "configuration defined"),
    MatrixItem("bf-003", "backfill", "quarantine replay", "remediated records", "revalidate, reprocess, close evidence, and preserve original quarantine record", "locally validated"),
    MatrixItem("bf-004", "rollback", "Gold backfill", "bad historical aggregate", "restore from previous Delta version or rerun Gold from validated Silver", "requires Databricks runtime validation"),
]

PERMISSIONS = [
    PermissionItem("spn-dbx-prod-pipelines", "service principal", "production jobs", "CAN_MANAGE_RUN", "runtime owner for approved prod jobs", "protected environment only"),
    PermissionItem("grp-data-engineers", "data engineer", "dev/test jobs", "CAN_MANAGE_RUN", "develop and validate workflows", "no direct prod owner rights"),
    PermissionItem("grp-platform-operators", "operator", "prod jobs", "CAN_MANAGE_RUN", "rerun, pause, and triage operational workflows", "no source-code bypass"),
    PermissionItem("grp-analytics-viewers", "viewer", "job run results", "CAN_VIEW", "observe readiness and publication state", "read-only"),
    PermissionItem("grp-data-governance", "quality owner", "quality evidence and quarantine", "CAN_VIEW plus table-level remediation grants", "review quality evidence", "no broad production write"),
]

TRACEABILITY = [
    TraceabilityItem("legacy_tms", "relational_incremental.bronze_ingestion", "bronze.legacy_tms_changes", "bronze_quality_gate", "silver.shipments", "silver_quality_gate", "gold.shipment_operations_performance", "gold_quality_gate", "publish_readiness"),
    TraceabilityItem("billing_ops", "batch_feeds.bronze_ingestion", "bronze.billing_ops_invoices", "bronze_quality_gate", "silver.billing_invoices", "silver_quality_gate", "gold.billing_revenue_summary", "gold_quality_gate", "publish_readiness"),
    TraceabilityItem("depot_reference_feed", "batch_feeds.bronze_ingestion", "bronze.depot_reference_feed", "bronze_quality_gate", "silver.depots_routes", "silver_quality_gate", "gold.depot_route_performance", "gold_quality_gate", "publish_readiness"),
    TraceabilityItem("carrier_updates", "event_streaming.streaming_ingestion", "bronze.carrier_updates", "streaming_quality_gate", "silver.shipment_events", "silver_quality_gate", "gold.delivery_delay_metrics", "gold_quality_gate", "publish_readiness"),
    TraceabilityItem("customer_service_export", "batch_feeds.bronze_ingestion", "bronze.customer_service_export", "bronze_quality_gate", "silver.service_cases", "silver_quality_gate", "gold.service_incident_summary", "gold_quality_gate", "publish_readiness"),
    TraceabilityItem("shipment_operational_events", "event_streaming.streaming_ingestion", "bronze.shipment_operational_events", "streaming_quality_gate", "silver.shipment_events", "silver_quality_gate", "gold.delivery_delay_metrics", "gold_quality_gate", "publish_readiness"),
]

READINESS = [
    MatrixItem("ready-001", "data quality", "all important datasets", "formal rules and deterministic quality evidence exist", "ready for Databricks expectation mapping", "locally validated"),
    MatrixItem("ready-002", "orchestration", "Lakeflow Jobs", "bundle job resources define workflows, tasks, dependencies and parameters", "ready for bundle validation in Databricks", "configuration defined"),
    MatrixItem("ready-003", "failure handling", "all workflow branches", "retry and stop/quarantine/escalate actions are explicit", "no blind retries for data-quality failures", "configuration defined"),
    MatrixItem("ready-004", "publication", "Gold products", "critical Silver/Gold failures block publication", "ready for runtime gate implementation", "configuration defined"),
    MatrixItem("ready-005", "runtime boundary", "Databricks workspace", "no job, expectation, stream, or pipeline was executed locally", "requires Databricks runtime validation", "requires Databricks runtime validation"),
]
