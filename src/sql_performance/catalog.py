from __future__ import annotations

# ruff: noqa: E501
from sql_performance.model import (
    BaselineMetric,
    IndexRecommendation,
    QueryAnalysis,
    StrategyItem,
    Workload,
)

WORKLOADS = [
    Workload("customer_lookup", "src/azure_sql/performance/workloads/customer_lookup.sql", "transactional OLTP", "read-heavy", "high", "medium", "high", "low", "single customer plus open shipments", "medium", "CustomerAccount.CustomerCode; Shipment.CustomerId/Status", "covering index validation and Query Store regression watch"),
    Workload("shipment_create_update", "src/azure_sql/performance/workloads/shipment_create_update.sql", "transactional OLTP", "write-heavy", "high", "high", "critical", "low", "single shipment transaction", "high", "PK/FK and procedure path", "procedure regression checks and blocking diagnostics"),
    Workload("shipment_status_query", "src/azure_sql/performance/workloads/shipment_status_query.sql", "transactional lookup", "read-heavy", "high", "high", "critical", "low", "single shipment event history", "medium", "ShipmentCode; ShipmentEventHistory Shipment/Sequence", "seek path and key lookup review"),
    Workload("route_depot_reporting", "src/azure_sql/performance/workloads/route_depot_reporting.sql", "operational reporting", "read-heavy aggregation", "medium", "medium", "high", "medium", "30-day shipment window", "high", "Shipment RouteId/Status/CreatedAt", "focused nonclustered covering index and analytical offload boundary"),
    Workload("incident_case_lookup", "src/azure_sql/performance/workloads/incident_case_lookup.sql", "customer-service lookup", "read-heavy", "medium", "medium", "medium", "low", "shipment incident/case references", "medium", "ShipmentIncident.ShipmentId/Status", "targeted lookup index if incident workload remains in MI"),
    Workload("analytical_delay_report", "src/azure_sql/performance/workloads/analytical_delay_report.sql", "candidate analytical", "read-heavy aggregation", "low", "low", "medium", "high", "large history/reporting window", "low", "Shipment dates/status plus event history", "offload to Databricks; do not over-index OLTP"),
]


BASELINE = [
    BaselineMetric("customer_lookup", 35, 180, 12, 12, 7, "medium", "transactional OLTP", "sub-100ms target after Azure validation", "simulated"),
    BaselineMetric("shipment_create_update", 55, 260, 22, 2, 5, "high", "transactional OLTP", "sub-250ms target after Azure validation", "simulated"),
    BaselineMetric("shipment_status_query", 28, 140, 10, 6, 4, "high", "transactional lookup", "sub-100ms target after Azure validation", "simulated"),
    BaselineMetric("route_depot_reporting", 920, 14500, 210, 180, 3, "medium", "operational reporting", "seconds-class operational report", "simulated"),
    BaselineMetric("incident_case_lookup", 45, 220, 16, 4, 6, "medium", "customer-service lookup", "sub-250ms target after Azure validation", "simulated"),
    BaselineMetric("analytical_delay_report", 1800, 42000, 480, 900, 3, "low", "candidate analytical", "offload target rather than OLTP SLA", "derived"),
]


QUERY_ANALYSIS = [
    QueryAnalysis("qa-001", "customer_lookup", "customer_lookup.sql", "static SQL shape", "Potential key lookup if customer/status include columns are incomplete.", "Joins CustomerAccount to Shipment filtered by CustomerCode/status.", "Use existing IX_Shipment_Customer_Status and validate include columns in Query Store.", "static analysis"),
    QueryAnalysis("qa-002", "shipment_create_update", "shipment_create_update.sql", "procedure path", "Writer/writer contention possible during status updates.", "usp_UpdateShipmentStatus updates Shipment and appends event history.", "Keep transaction short; monitor locks and deadlocks; do not add broad indexes to write path.", "static analysis"),
    QueryAnalysis("qa-003", "shipment_status_query", "shipment_status_query.sql", "static SQL shape", "Sort/key lookup risk on event history if sequence index absent.", "Query needs latest ordered event history per shipment.", "Use IX_ShipmentEventHistory_Shipment_Sequence; validate seeks vs scans.", "static analysis"),
    QueryAnalysis("qa-004", "route_depot_reporting", "route_depot_reporting.sql", "before/after scenario", "Original reporting query scans recent shipments and groups by depot/route/status.", "Milestone 3 identified OLTP reporting contention.", "Use IX_Shipment_Route_Status_CreatedAt for migration readiness and offload repeated analytics to Databricks later.", "static analysis"),
    QueryAnalysis("qa-005", "analytical_delay_report", "analytical_delay_report.sql", "static SQL shape", "Large aggregation and date filters risk high reads and memory grants.", "Delay report spans shipments and event history.", "Treat as analytical offload candidate; avoid indexing every analytical predicate in OLTP.", "derived"),
    QueryAnalysis("qa-006", "parameter_sensitive_customer_shipments", "parameter_sensitive_customer_shipments.sql", "parameter sensitivity", "Large/critical customers and small customers may need different join/access strategies.", "ServiceTier and customer distribution can skew shipment counts.", "Investigate Query Store runtime stats, PSP behaviour, Query Store hints, or OPTION(RECOMPILE) for targeted procedure only.", "simulated"),
]


INDEX_RECOMMENDATIONS = [
    IndexRecommendation("idx-001", "dbo.Shipment", "retain/validate", "IX_Shipment_Customer_Status INCLUDE (CreatedAtUtc, PromisedDeliveryAtUtc)", "Supports customer lookup and operational shipment summary.", "Lower logical reads for customer lookup.", "Adds write overhead on shipment writes; already targeted and narrow.", "configuration defined"),
    IndexRecommendation("idx-002", "dbo.ShipmentEventHistory", "retain/validate", "IX_ShipmentEventHistory_Shipment_Sequence (ShipmentId, EventSequence)", "Supports shipment event chronology lookup.", "Avoids sort/scan for event history lookup.", "Moderate write overhead on event inserts; justified by lookup path.", "configuration defined"),
    IndexRecommendation("idx-003", "dbo.Shipment", "implemented in target schema", "IX_Shipment_Route_Status_CreatedAt INCLUDE (PromisedDeliveryAtUtc, DeliveredAtUtc)", "Focused before/after scenario for route/depot reporting contention.", "Expected lower reads for recent route/status reporting.", "Adds write overhead; accepted as migration-readiness index only, deeper tuning deferred.", "configuration defined"),
    IndexRecommendation("idx-004", "dbo.ShipmentIncident", "candidate", "IX_ShipmentIncident_Shipment_Status (ShipmentId, IncidentStatus) INCLUDE (IncidentOpenedAtUtc)", "Only justified if incident lookup remains in MI after billing/service migration boundary.", "Could improve customer-service incident lookup.", "Do not implement until workload frequency is validated.", "requires Azure validation"),
    IndexRecommendation("idx-005", "all user tables", "review", "duplicate/redundant index DMV review", "Prevent index proliferation.", "Reduces write overhead and storage waste.", "Must be based on Query Store and index usage after representative workload.", "requires Azure validation"),
]


STATISTICS_STRATEGY = [
    StrategyItem("stat-001", "automatic statistics", "Keep auto create/update statistics enabled unless live evidence says otherwise.", "Azure SQL/SQL Server optimizer depends on current stats.", "configuration defined", "static analysis"),
    StrategyItem("stat-002", "stale detection", "Use modification counters and STATS_DATE to target stale statistics.", "Avoids blanket FULLSCAN across every table.", "configuration defined", "static analysis"),
    StrategyItem("stat-003", "sample strategy", "Use RESAMPLE/default for routine maintenance; FULLSCAN only for narrow critical stats with evidence.", "Balances accuracy, runtime, and IO.", "configuration defined", "derived"),
    StrategyItem("stat-004", "SQL Agent integration", "Integrate targeted stats job with Milestone 6 SQL Agent pattern.", "Keeps operations and performance model aligned.", "locally validated", "locally measured"),
]


BLOCKING_SCENARIOS = [
    StrategyItem("blk-001", "blocked reader/writer", "Session A updates Shipment and holds transaction; Session B reads customer shipment status.", "Demonstrates RCSI trade-off and reader blocking analysis.", "simulated", "simulated"),
    StrategyItem("blk-002", "writer/writer contention", "Two sessions update the same Shipment status through procedure path.", "Demonstrates lock waits, head blocker, and retry requirement.", "simulated", "simulated"),
    StrategyItem("blk-003", "sleeping open transaction", "Session opens transaction and goes idle after touching ShipmentEventHistory.", "Demonstrates open transaction detection and escalation.", "simulated", "simulated"),
]


DEADLOCK_READINESS = [
    StrategyItem("dl-001", "extended events", "Create database-scoped deadlock capture session for xml_deadlock_report where supported.", "Captures evidence without fabricating graphs.", "configuration defined", "static analysis"),
    StrategyItem("dl-002", "deadlock workflow", "Capture graph, identify resources/order, classify victim, apply retry/error 1205 guidance.", "Structured response to recurring deadlocks.", "configuration defined", "static analysis"),
    StrategyItem("dl-003", "repro scenario", "Two sessions update Shipment then ShipmentEventHistory in opposite order.", "Can be reproduced later in SQL Server-compatible environment.", "simulated", "simulated"),
]


PARAMETER_SENSITIVITY = [
    StrategyItem("psp-001", "representative query", "usp_GetCustomerShipmentSummaryByTier models skew between critical and standard customers.", "Different tiers can produce different optimal plans.", "simulated", "simulated"),
    StrategyItem("psp-002", "Query Store investigation", "Compare runtime stats by parameter/runtime distribution and plan_id.", "Avoids guessing from one execution.", "configuration defined", "static analysis"),
    StrategyItem("psp-003", "mitigation options", "Consider PSP optimization where available, Query Store hints, forced plans, or OPTION(RECOMPILE) only with evidence.", "Mitigations have trade-offs and should be reversible.", "configuration defined", "derived"),
]


REGRESSION_CONTROLS = [
    StrategyItem("reg-001", "workflow", "baseline -> change -> detect -> identify query -> compare plans -> mitigate -> validate -> document -> remove temporary mitigation", "Explicit lifecycle for safe tuning.", "configuration defined", "derived"),
    StrategyItem("reg-002", "Query Store", "Use regressed queries and plan history reports.", "Maps regression response to SQL MI/Azure SQL features.", "configuration defined", "static analysis"),
    StrategyItem("reg-003", "CI/CD boundary", "Future SQL CI/CD should run post-deployment baseline comparison.", "Documents Milestone 8 boundary without implementing it.", "planned", "derived"),
]


PERFORMANCE_ASSURANCE = [
    StrategyItem("pa-001", "workload coverage", "Six representative workloads are catalogued.", "Covers OLTP, reporting, customer-service, and analytical offload boundary.", "locally validated", "locally measured"),
    StrategyItem("pa-002", "baseline availability", "Deterministic simulated baseline exists for every workload.", "Enables regression workflow without fake Azure telemetry.", "simulated", "simulated"),
    StrategyItem("pa-003", "Query Store readiness", "Configuration and diagnostics scripts exist.", "Ready for SQL MI validation.", "configuration defined", "static analysis"),
    StrategyItem("pa-004", "index strategy", "Focused recommendations avoid index proliferation.", "Supports reporting scenario and write-overhead review.", "configuration defined", "static analysis"),
    StrategyItem("pa-005", "statistics strategy", "Targeted stale-statistics strategy exists.", "Avoids blanket FULLSCAN.", "configuration defined", "static analysis"),
    StrategyItem("pa-006", "blocking diagnostics", "Blocking scenarios and DMV scripts exist.", "Supports incident analysis.", "simulated", "simulated"),
    StrategyItem("pa-007", "deadlock diagnostics", "Extended Events and workflow assets exist.", "No deadlock graph fabricated.", "configuration defined", "static analysis"),
    StrategyItem("pa-008", "parameter sensitivity", "Representative skew scenario and mitigation options exist.", "Supports PSP/regression handling.", "simulated", "simulated"),
    StrategyItem("pa-009", "regression detection", "Regression workflow and Query Store mapping exist.", "Future CI/CD integration documented.", "configuration defined", "derived"),
    StrategyItem("pa-010", "operational integration", "Runbooks and Milestone 6 monitoring integration exist.", "Performance incidents fit operations model.", "locally validated", "locally measured"),
]

