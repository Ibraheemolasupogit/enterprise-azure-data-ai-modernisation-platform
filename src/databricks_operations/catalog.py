from __future__ import annotations

# ruff: noqa: E501
from databricks_operations.model import (
    AlertItem,
    CostItem,
    JobHealthRule,
    MonitoringItem,
    OptimizationItem,
    PipelineStage,
    PolicyItem,
    SloItem,
    TraceabilityItem,
    TroubleshootingItem,
)

MONITORING = [
    MonitoringItem("mon-001", "batch feeds", "Lakeflow Jobs", "job run metadata and system tables", "task status, duration, retries, queue time", "detect failed or delayed batch ingestion", "data engineering", "configuration defined"),
    MonitoringItem("mon-002", "relational increments", "Lakeflow Jobs", "job run metadata", "duration, start delay, stale high-water mark", "detect stale incremental analytical loads", "data engineering", "configuration defined"),
    MonitoringItem("mon-003", "shipment events", "Structured Streaming", "streaming progress and checkpoint metadata", "input rate, processing rate, watermark, lag, checkpoint age", "detect stalled or lagging event stream", "streaming operator", "requires Databricks validation"),
    MonitoringItem("mon-004", "Gold publication", "Databricks SQL and Lakeflow Jobs", "query history and job metadata", "query latency, Gold freshness, Gold gate result", "detect stale publication and expensive SQL refresh", "analytics owner", "configuration defined"),
    MonitoringItem("mon-005", "jobs compute", "clusters/serverless", "system.compute and Spark UI/runtime metrics", "utilization, spill, shuffle, memory pressure", "troubleshoot Spark performance", "platform operator", "requires Databricks validation"),
    MonitoringItem("mon-006", "SQL warehouses", "Databricks SQL", "query history and warehouse events", "queue time, execution duration, cache hit behavior", "operate Gold consumption warehouses", "analytics platform owner", "requires Databricks validation"),
    MonitoringItem("mon-007", "Unity Catalog", "governance/audit", "system.access audit and lineage tables", "grant changes, object access, lineage updates", "security and lineage investigation", "security reviewer", "requires Databricks validation"),
    MonitoringItem("mon-008", "FinOps", "billing/usage", "system.billing usage and list prices", "DBU usage by workspace/job/tag", "attribute and optimize cost", "FinOps owner", "requires Databricks validation"),
    MonitoringItem("mon-009", "storage", "ADLS and Delta metadata", "table details/history and storage diagnostics", "file counts, table size, retention and stale files", "detect Delta table health issues", "data engineering", "configuration defined"),
    MonitoringItem("mon-010", "quality gates", "orchestration evidence", "quality_results and job task values", "critical failures, rejects, quarantines", "block unsafe publication", "data governance", "locally validated"),
]

JOB_HEALTH = [
    JobHealthRule("job-001", "batch_feeds_workflow", "failed task", "task result is failed", "batch source not refreshed", "data engineering", "docs/runbooks/databricks-job-failure.md", "configuration defined"),
    JobHealthRule("job-002", "relational_incremental_workflow", "delayed run", "start delay exceeds architecture assumption", "incremental Silver freshness at risk", "data engineering", "docs/runbooks/databricks-slow-job.md", "configuration defined"),
    JobHealthRule("job-003", "event_streaming_workflow", "repeated retry", "streaming task restarts repeatedly", "event freshness degraded", "streaming operator", "docs/runbooks/databricks-streaming-lag.md", "configuration defined"),
    JobHealthRule("job-004", "gold_publication_workflow", "stale publication", "Gold freshness breach threshold exceeded", "BI and operational analytics stale", "analytics owner", "docs/runbooks/databricks-stale-gold-product.md", "configuration defined"),
    JobHealthRule("job-005", "controlled_backfill_replay_workflow", "excessive duration", "backfill exceeds approved window", "current processing isolation at risk", "platform lead", "docs/runbooks/databricks-job-failure.md", "configuration defined"),
]

PIPELINE_OBSERVABILITY = [
    PipelineStage("source", "legacy_tms/billing_ops/file feeds/events", "source availability", "source manifest count", "source extract/event recency", "source arrival latency", "not applicable", "configuration defined"),
    PipelineStage("ingestion", "Lakeflow Jobs task", "task run status", "input/output record counts", "processing date high-water mark", "task duration", "checkpoint path for incremental/streaming", "configuration defined"),
    PipelineStage("Bronze", "bronze.*", "Bronze write success", "Bronze accepted/rejected counts", "ingested_at max", "landing-to-Bronze latency", "Auto Loader/stream checkpoint where relevant", "configuration defined"),
    PipelineStage("Bronze quality gate", "Bronze datasets", "gate pass/fail", "warning/rejected/quarantined counts", "freshness status", "gate duration", "not applicable", "locally validated"),
    PipelineStage("Silver", "silver.*", "Silver write success", "accepted/quarantined counts", "Silver max event/date", "Bronze-to-Silver latency", "not applicable", "configuration defined"),
    PipelineStage("Silver quality gate", "Silver datasets", "gate pass/fail", "critical failure count", "freshness status", "gate duration", "not applicable", "locally validated"),
    PipelineStage("Gold", "gold.*", "Gold refresh success", "KPI row counts", "Gold max metric date", "Silver-to-Gold latency", "not applicable", "configuration defined"),
    PipelineStage("publication", "Gold products", "publish_readiness", "published product count", "consumer freshness", "Gold gate-to-publish latency", "not applicable", "configuration defined"),
]

SPARK_TROUBLESHOOTING = [
    TroubleshootingItem("slow stages", "large shuffle, skew, or repeated scans", "Spark UI stages, SQL DAG, task duration distribution", "inspect joins/filtering; reduce scanned data; apply AQE and clustering", "requires Databricks validation"),
    TroubleshootingItem("skew", "hot customer/route/shipment key", "task time variance and shuffle read distribution", "salt only targeted keys, broadcast small dimensions, review join order", "configuration defined"),
    TroubleshootingItem("shuffle pressure", "wide aggregations or non-colocated joins", "shuffle bytes, spill, stage retries", "pre-filter, repartition by join key, reduce columns before join", "requires Databricks validation"),
    TroubleshootingItem("spill", "executor memory pressure", "spill metrics, GC time, executor logs", "right-size workers, reduce shuffle width, avoid unnecessary cache", "requires Databricks validation"),
    TroubleshootingItem("partition imbalance", "too few/many partitions or skewed input files", "input partition sizes, task counts", "coalesce small outputs, repartition before wide operations", "configuration defined"),
    TroubleshootingItem("driver bottleneck", "collect/toPandas or excessive metadata", "driver logs, command result size, job stall", "avoid driver collection and push work to Spark", "configuration defined"),
    TroubleshootingItem("Python UDF overhead", "row-by-row Python execution", "Python execution time and serialization metrics", "replace with Spark SQL functions or vectorized alternatives", "configuration defined"),
    TroubleshootingItem("inefficient joins", "missing filters, wrong build side, large shuffle", "query plan and join strategy", "broadcast small dimensions and filter facts before join", "configuration defined"),
]

JOIN_OPTIMIZATION = [
    OptimizationItem("shipments + routes", "join optimization", "fact shipments joins small route dimension", "broadcast route/depot dimension where small; preserve route_code filters", "reduces shuffle for Gold route metrics", "lower jobs compute runtime if dimension remains small", "configuration defined"),
    OptimizationItem("shipments + customers", "join optimization", "customer dimension may grow but remains smaller than fact", "let AQE choose broadcast; only hint after query-plan evidence", "avoids forcing bad broadcast when dimension grows", "prevents memory overhead from unsafe hinting", "configuration defined"),
    OptimizationItem("billing + customer", "join optimization", "billing invoices join customer/account dimension", "filter invoice date range before join and select required columns", "reduces scan and shuffle pressure", "reduces warehouse/job consumption", "configuration defined"),
    OptimizationItem("events + shipments", "join optimization", "event fact can outgrow shipment fact", "cluster by shipment_id and use event-time pruning", "supports event-to-shipment correlation", "avoids broad event scans", "configuration defined"),
]

DELTA_HEALTH = [
    OptimizationItem("bronze.shipment_operational_events", "Delta table health", "append-heavy event table", "monitor file count, average file size, transaction log growth, CDF state, checkpoint age", "detect small files and log growth before slow reads", "compaction may add cost; schedule after evidence", "configuration defined"),
    OptimizationItem("silver.shipments", "Delta table health", "MERGE/upsert fact-like table", "monitor table size, schema changes, CDF, clustering and stale data", "supports reliable incremental refresh", "avoid unnecessary optimize on tiny tables", "configuration defined"),
    OptimizationItem("gold.delivery_delay_metrics", "Delta table health", "small aggregate table", "avoid partitioning; monitor freshness and grain uniqueness", "small table should stay simple", "prevents over-optimization cost", "locally validated"),
    OptimizationItem("all Delta tables", "VACUUM and retention", "retention from Milestone 9", "VACUUM must not reduce below safe defaults; consider time travel, long readers, streaming checkpoints and compliance deletes", "protects recovery and readers", "retention storage trade-off explicit", "configuration defined"),
    OptimizationItem("managed Gold/Silver", "predictive optimization", "eligible UC managed tables after runtime validation", "assess enablement for managed tables with recurring queries", "can reduce manual maintenance", "may increase background optimization cost", "requires Databricks validation"),
]

STREAMING_HEALTH = [
    JobHealthRule("str-001", "event_streaming_workflow", "input faster than processing", "input rate consistently exceeds processing rate", "event freshness degraded", "streaming operator", "docs/runbooks/databricks-streaming-lag.md", "requires Databricks validation"),
    JobHealthRule("str-002", "event_streaming_workflow", "stale checkpoint", "checkpoint age exceeds breach threshold", "stream recovery at risk", "streaming operator", "docs/runbooks/databricks-checkpoint-failure.md", "configuration defined"),
    JobHealthRule("str-003", "event_streaming_workflow", "growing state", "state rows/memory grows without watermark progress", "streaming cost and latency risk", "streaming operator", "docs/runbooks/databricks-streaming-lag.md", "requires Databricks validation"),
    JobHealthRule("str-004", "event_streaming_workflow", "failed micro-batch", "micro-batch failure in progress/event log", "event processing paused", "streaming operator", "docs/runbooks/databricks-job-failure.md", "requires Databricks validation"),
    JobHealthRule("str-005", "event_streaming_workflow", "excessive late data", "late/quarantined event share breaches assumption", "Gold delay metrics may lag", "data governance", "docs/runbooks/databricks-streaming-lag.md", "locally validated"),
]

COMPUTE_OPTIMIZATION = [
    OptimizationItem("batch feeds", "jobs compute", "daily bounded file processing", "jobs compute with autoscaling, Photon where Delta-heavy, auto-termination", "handles variable files without interactive clusters", "limits idle compute", "configuration defined"),
    OptimizationItem("relational increments", "jobs compute", "frequent incremental MERGE", "small-to-medium job clusters with policy limits and LTS runtime", "keeps merge tasks isolated", "controls recurring job cost", "configuration defined"),
    OptimizationItem("event streaming", "serverless jobs or jobs compute", "continuous event ingestion", "serverless where available; otherwise isolated job compute and checkpoint health", "decouples stream from interactive users", "continuous workloads require cost review", "configuration defined"),
    OptimizationItem("Gold SQL refresh", "SQL warehouse", "SQL aggregation/serving", "right-sized serverless/pro warehouse with auto-stop and queue monitoring", "supports SQL refresh and BI queries", "prevents idle warehouse spend", "configuration defined"),
    OptimizationItem("backfill/replay", "jobs compute", "manual historical ranges", "isolated job cluster, max workers cap, no shared interactive compute", "protects current workloads", "backfill cost visible by tags", "configuration defined"),
]

CLUSTER_POLICIES = [
    PolicyItem("pol-001", "dev", "allowed runtimes", "current LTS plus one preview runtime by exception", "developer flexibility with bounded testing", "configuration defined"),
    PolicyItem("pol-002", "prod", "allowed runtimes", "current approved LTS only", "stable production runtime", "configuration defined"),
    PolicyItem("pol-003", "prod", "max workers", "cap by workload class; backfill requires approval", "avoid runaway scale", "configuration defined"),
    PolicyItem("pol-004", "prod", "auto-termination", "required for job clusters and warehouses where applicable", "reduce idle spend", "configuration defined"),
    PolicyItem("pol-005", "all", "tags", "environment,workload,domain,owner,cost_center", "mandatory FinOps attribution", "configuration defined"),
    PolicyItem("pol-006", "prod", "security mode", "Unity Catalog compatible access mode", "enforce governance boundary", "configuration defined"),
    PolicyItem("pol-007", "prod", "libraries", "bundle/source-controlled libraries only", "prevent unreviewed package drift", "configuration defined"),
]

SQL_WAREHOUSE = [
    OptimizationItem("Gold consumption warehouse", "SQL warehouse operations", "curated Gold BI and operational analytics", "monitor queued queries, p95 duration, cache use, auto-stop and concurrency", "right-size warehouse from query history", "avoid idle and oversized warehouse cost", "requires Databricks validation"),
    OptimizationItem("Gold refresh SQL task", "query performance", "Gold aggregation SQL", "review query history for large scans, poor filters, aggregation pressure and repeated expensive queries", "optimize Databricks SQL plans, not Azure SQL Server plans", "reduce warehouse DBU consumption", "requires Databricks validation"),
    OptimizationItem("warehouse sizing", "serverless/pro", "unknown initial concurrency", "start small under architecture assumption and scale by queue/latency evidence", "protects latency without guessing", "avoids fabricated benchmark sizing", "configuration defined"),
]

COST_ALLOCATION = [
    CostItem("environment", "environment tag", "split dev/test/prod usage", "FinOps owner", "configuration defined"),
    CostItem("workspace", "workspace_id system billing field", "workspace-level chargeback", "FinOps owner", "requires Databricks validation"),
    CostItem("workload", "workload tag", "batch/incremental/streaming/gold/backfill cost grouping", "platform operator", "configuration defined"),
    CostItem("job", "job_id/job_name system tables", "job-level cost attribution", "data engineering", "requires Databricks validation"),
    CostItem("compute type", "sku/compute_type", "serverless, jobs compute, SQL warehouse split", "platform operator", "requires Databricks validation"),
    CostItem("user/service principal", "run_as/user identity", "interactive vs service workload attribution", "security reviewer", "requires Databricks validation"),
    CostItem("domain", "domain tag", "shipment, billing, service, reference domain attribution", "data product owner", "configuration defined"),
]

COST_CONTROLS = [
    OptimizationItem("idle interactive compute", "preventive", "interactive clusters can idle", "auto-termination and dev policy limits", "minimal performance impact", "reduces idle spend", "configuration defined"),
    OptimizationItem("oversized clusters", "detective", "worker count exceeds workload need", "review utilization and right-size", "improves efficiency", "reduces DBU waste", "requires Databricks validation"),
    OptimizationItem("excessive retries", "corrective", "retry storm hides deterministic failures", "cap retries and stop data-quality failures", "reduces noisy reruns", "prevents repeated failed-run cost", "configuration defined"),
    OptimizationItem("over-frequent schedules", "detective", "schedule exceeds freshness need", "compare freshness target to run frequency", "keeps products fresh enough", "removes unnecessary runs", "configuration defined"),
    OptimizationItem("SQL warehouse idle time", "preventive", "warehouse left running", "auto-stop and queue monitoring", "keeps query serving available", "reduces idle warehouse cost", "configuration defined"),
    OptimizationItem("small-file overhead", "corrective", "many tiny files slow reads", "compact/OPTIMIZE after file-count evidence", "improves scan planning", "optimization cost must be justified", "requires Databricks validation"),
    OptimizationItem("excessive retention", "detective", "data kept beyond policy", "compare Delta/ADLS retention to policy", "protects recovery boundaries", "controls storage cost", "configuration defined"),
]

ALERTS = [
    AlertItem("alert-001", "job failed", "ERROR", "platform operator", "sql/jobs_failed.sql", "docs/runbooks/databricks-job-failure.md", "data engineering lead", "configuration defined"),
    AlertItem("alert-002", "repeated task failure", "ERROR", "platform operator", "sql/jobs_failed.sql", "docs/runbooks/databricks-job-failure.md", "platform lead", "configuration defined"),
    AlertItem("alert-003", "job duration regression", "WARNING", "data engineering", "sql/jobs_long_running.sql", "docs/runbooks/databricks-slow-job.md", "workflow owner", "configuration defined"),
    AlertItem("alert-004", "Gold freshness breach", "ERROR", "analytics owner", "sql/jobs_long_running.sql", "docs/runbooks/databricks-stale-gold-product.md", "business owner", "configuration defined"),
    AlertItem("alert-005", "streaming lag", "ERROR", "streaming operator", "sql/streaming_health.sql", "docs/runbooks/databricks-streaming-lag.md", "platform lead", "configuration defined"),
    AlertItem("alert-006", "stalled stream", "CRITICAL", "streaming operator", "sql/streaming_health.sql", "docs/runbooks/databricks-streaming-lag.md", "platform lead", "configuration defined"),
    AlertItem("alert-007", "checkpoint issue", "CRITICAL", "streaming operator", "sql/streaming_health.sql", "docs/runbooks/databricks-checkpoint-failure.md", "platform lead", "configuration defined"),
    AlertItem("alert-008", "critical quality failure", "CRITICAL", "data governance", "sql/quality_gate_failures.sql", "docs/runbooks/databricks-quality-gate-failure.md", "data owner", "locally validated"),
    AlertItem("alert-009", "compute saturation", "WARNING", "platform operator", "sql/compute_utilization.sql", "docs/runbooks/databricks-memory-spill.md", "platform lead", "requires Databricks validation"),
    AlertItem("alert-010", "warehouse queue/latency", "WARNING", "analytics platform owner", "sql/sql_warehouse_latency.sql", "docs/runbooks/databricks-sql-warehouse-latency.md", "analytics owner", "requires Databricks validation"),
    AlertItem("alert-011", "unusual usage/cost", "WARNING", "FinOps owner", "sql/cost_attribution.sql", "docs/runbooks/databricks-unexpected-cost.md", "platform owner", "requires Databricks validation"),
    AlertItem("alert-012", "security/audit anomaly", "CRITICAL", "security reviewer", "sql/audit_activity.sql", "docs/runbooks/databricks-audit-investigation.md", "security lead", "requires Databricks validation"),
]

SLOS = [
    SloItem("shipment event processing", "minutes-class architecture assumption", "processing keeps pace with input", "transient restart tolerated; repeated restart escalates", "recover from checkpoint after transient failure", "high", "configuration defined"),
    SloItem("operational shipment Gold", "hourly architecture assumption", "Gold refresh after validated Silver", "critical gate failure blocks publication", "rerun Gold from validated Silver", "high", "configuration defined"),
    SloItem("billing Gold", "daily architecture assumption", "daily revenue summary after billing increment", "single failed day requires owner review", "rerun from Silver billing invoices", "medium", "configuration defined"),
    SloItem("service/incident Gold", "daily architecture assumption", "daily service summary after case export", "malformed cases quarantined without silent loss", "replay corrected cases", "medium", "configuration defined"),
]

READINESS = [
    OptimizationItem("monitoring architecture", "readiness", "signals mapped to jobs, tables, warehouses, quality and cost", "ready for Databricks runtime wiring", "no runtime telemetry fabricated", "requires system tables/logs to execute", "configuration defined"),
    OptimizationItem("Spark troubleshooting", "readiness", "symptom-to-evidence-to-remediation matrix exists", "ready for Spark UI and query-plan use", "safe remediation patterns only", "requires runtime metrics", "configuration defined"),
    OptimizationItem("Delta optimization", "readiness", "table health and retention checks defined", "run OPTIMIZE/VACUUM only after evidence", "protects recovery/time travel", "avoids unjustified optimization cost", "configuration defined"),
    OptimizationItem("FinOps", "readiness", "mandatory tags and usage dimensions defined", "use system billing tables in production", "separates performance and cost controls", "no fake currency totals", "configuration defined"),
    OptimizationItem("runtime boundary", "readiness", "system table queries and alerts are authored", "execute only in Databricks workspace", "no local runtime pass claims", "requires Databricks validation", "requires Databricks validation"),
]

TRACEABILITY = [
    TraceabilityItem("batch feeds", "batch_feeds_workflow", "failed/delayed task; record counts", "alert-001", "docs/runbooks/databricks-job-failure.md", "data engineering", "workload=batch_feeds", "over-frequent schedules"),
    TraceabilityItem("relational increments", "relational_incremental_workflow", "duration, start delay, freshness", "alert-003", "docs/runbooks/databricks-slow-job.md", "data engineering", "workload=relational_incremental", "oversized clusters"),
    TraceabilityItem("shipment events", "event_streaming_workflow", "watermark, lag, checkpoint age", "alert-005", "docs/runbooks/databricks-streaming-lag.md", "streaming operator", "workload=event_streaming", "streaming compute right-sizing"),
    TraceabilityItem("Gold publication", "gold_publication_workflow", "Gold freshness and quality gate", "alert-004", "docs/runbooks/databricks-stale-gold-product.md", "analytics owner", "workload=gold_publication", "SQL warehouse idle time"),
    TraceabilityItem("SQL warehouse", "Gold SQL warehouse", "queue time and query latency", "alert-010", "docs/runbooks/databricks-sql-warehouse-latency.md", "analytics platform owner", "compute_type=sql_warehouse", "warehouse auto-stop/right-size"),
    TraceabilityItem("FinOps", "all workflows", "usage by tags/job/workspace", "alert-011", "docs/runbooks/databricks-unexpected-cost.md", "FinOps owner", "environment/workload/domain", "cost optimization controls"),
]
