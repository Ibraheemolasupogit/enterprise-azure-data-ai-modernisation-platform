from __future__ import annotations

# ruff: noqa: E501
import csv
import json
import re
from pathlib import Path
from typing import Any

from estate_assessment.inventory import DEPENDENCIES, SYSTEMS
from estate_assessment.models import CompatibilityFinding, SourceSystem

ROOT = Path(__file__).resolve().parents[2]
SQL_ROOT = ROOT / "src/azure_sql/legacy_oltp/sqlserver"
SAMPLE_ROOT = ROOT / "data/samples/legacy_estate/tiny"

TARGET_OPTIONS = (
    "Azure SQL Database",
    "Azure SQL Managed Instance",
    "SQL Server on Azure VM",
    "Azure Database for PostgreSQL",
    "Azure Cosmos DB",
    "Azure Databricks",
    "retain temporarily",
    "retire",
)

COMPLEXITY_WEIGHTS = {
    "schema_complexity": 0.14,
    "feature_compatibility": 0.17,
    "application_coupling": 0.14,
    "data_volume": 0.10,
    "downtime_tolerance": 0.12,
    "integration_count": 0.11,
    "security_complexity": 0.08,
    "operational_criticality": 0.08,
    "performance_sensitivity": 0.06,
}


def compatibility_findings() -> list[CompatibilityFinding]:
    sql_text_by_file = {
        path.name: path.read_text(encoding="utf-8") for path in sorted(SQL_ROOT.glob("*.sql"))
    }
    all_sql = "\n".join(sql_text_by_file.values()).lower()
    findings: list[CompatibilityFinding] = []

    checks = [
        (
            "SQL-COMP-001",
            "dbo.CustomerAccount.LegacyCustomerMemo",
            "legacy_data_type",
            "medium",
            "Azure SQL Database; Azure SQL Managed Instance",
            "ntext" in all_sql,
            "Found ntext in table definition.",
            "Replace ntext with nvarchar(max) and regression-test application reads.",
            "Requires schema remediation before platform migration.",
        ),
        (
            "SQL-COMP-002",
            "dbo.Shipment.DeclaredValueGbp",
            "legacy_data_type",
            "low",
            "Azure SQL Database; Azure SQL Managed Instance; SQL Server on Azure VM",
            re.search(r"\bmoney\b", all_sql) is not None,
            "Found money data type in shipment financial attribute.",
            "Validate precision requirements and consider decimal(19,4).",
            "Low migration blocker, moderate testing requirement.",
        ),
        (
            "SQL-COMP-003",
            "dbo.usp_CreateShipment; dbo.usp_UpdateShipmentStatus",
            "stored_procedure_dependency",
            "medium",
            "Azure SQL Database; Azure SQL Managed Instance",
            "create procedure" in all_sql and "sysutcdatetime" in all_sql,
            "Stored procedures implement create/update business behaviour.",
            "Build procedure-level regression tests and identify application callers.",
            "Application coupling increases migration sequencing complexity.",
        ),
        (
            "SQL-COMP-004",
            "dbo.Shipment.LegacyOptionsJson; dbo.ShipmentEventHistory.EventPayloadJson",
            "denormalized_json_payload",
            "medium",
            "Azure SQL Database; Azure SQL Managed Instance; Azure Databricks",
            "nvarchar(max)" in all_sql and "json" in all_sql,
            "JSON payloads are stored in relational tables.",
            "Define JSON contract validation and indexing strategy before migration.",
            "Affects performance tuning and downstream ingestion contracts.",
        ),
        (
            "SQL-COMP-005",
            "dbo.vw_OpenShipmentsByDepot; operational reporting query",
            "performance_sensitive_reporting",
            "high",
            "Azure SQL Database; Azure SQL Managed Instance; Azure Databricks",
            "vw_openshipmentsbydepot" in all_sql and "count_big" in all_sql,
            "Operational reporting aggregates current shipment tables.",
            "Move repeated analytical/reporting workload to lakehouse or serving model.",
            "Risk of performance regression if migrated without workload isolation.",
        ),
        (
            "SQL-COMP-006",
            "dbo.ShipmentEventHistory",
            "large_history_table",
            "medium",
            "Azure SQL Database; Azure SQL Managed Instance; Azure Databricks",
            "shipmenteventhistory" in all_sql,
            "History table captures frequent shipment status events.",
            "Partition/archive strategy and CDC extraction design required.",
            "Impacts migration duration, replication, and future streaming ingestion.",
        ),
        (
            "SQL-COMP-007",
            "dbo.Shipment.RowVersionBytes",
            "transaction_semantics",
            "low",
            "Azure SQL Database; Azure SQL Managed Instance",
            "rowversion" in all_sql,
            "rowversion used for optimistic concurrency/change detection.",
            "Preserve concurrency semantics and assess CDC alternative.",
            "Requires application compatibility testing.",
        ),
        (
            "SQL-COMP-008",
            "Legacy authentication model",
            "authentication_difference",
            "medium",
            "Azure SQL Database; Azure SQL Managed Instance",
            True,
            "Inventory marks authentication as legacy SQL/application authentication assumption.",
            "Discover users, convert to Entra-first identities, and validate managed identity paths.",
            "Identity transition is a prerequisite for secure migration.",
        ),
        (
            "SQL-COMP-009",
            "Collation and instance settings",
            "requires_live_validation",
            "medium",
            "Azure SQL Database; Azure SQL Managed Instance; SQL Server on Azure VM",
            True,
            "Static local scripts do not expose production collation or instance settings.",
            "Run live estate discovery before choosing final compatibility level and collation.",
            "Unvalidated instance settings may affect target selection.",
        ),
    ]
    for check in checks:
        if check[5]:
            findings.append(
                CompatibilityFinding(
                    finding_id=check[0],
                    source_object=check[1],
                    category=check[2],
                    severity=check[3],
                    affected_targets=check[4],
                    evidence=check[6],
                    remediation=check[7],
                    migration_impact=check[8],
                )
            )
    return findings


def workload_classifications() -> list[dict[str, Any]]:
    workload_path = SAMPLE_ROOT / "workload.jsonl"
    rows = [json.loads(line) for line in workload_path.read_text(encoding="utf-8").splitlines()]
    grouped: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        grouped.setdefault(row["workload_type"], []).append(row)

    definitions = {
        "customer_lookup": ("transactional OLTP", "low", "medium", "high", "strong"),
        "create_shipment": ("transactional OLTP", "low", "high", "high", "strong"),
        "update_shipment_status": ("event/streaming", "low", "high", "high", "strong"),
        "invoice_lookup": ("transactional OLTP", "medium", "medium", "medium", "strong"),
        "route_depot_reporting": (
            "operational reporting",
            "medium",
            "medium",
            "medium",
            "eventual",
        ),
        "incident_case_creation": ("customer-service/search", "low", "medium", "medium", "strong"),
        "analytical_delay_report": ("analytical", "high", "medium", "low", "eventual"),
    }
    output = []
    for workload_type in sorted(definitions):
        category, latency, throughput, concurrency, consistency = definitions[workload_type]
        count = len(grouped.get(workload_type, []))
        read_write_ratio = (
            "read-heavy"
            if "lookup" in workload_type or "report" in workload_type
            else "write-heavy"
        )
        output.append(
            {
                "workload_id": workload_type,
                "category": category,
                "operation_count_in_sample": count,
                "latency_sensitivity": latency,
                "throughput": throughput,
                "concurrency": concurrency,
                "scale": "local sample; production volume requires live validation",
                "transactional_consistency": consistency,
                "read_write_ratio": read_write_ratio,
                "elasticity": "moderate" if category != "analytical" else "high",
                "integration_complexity": "high"
                if category in {"event/streaming", "analytical"}
                else "medium",
                "evidence_class": "locally measured",
                "evidence": "Derived from deterministic workload simulator sample.",
            }
        )
    return output


def target_service_decisions() -> list[dict[str, Any]]:
    return [
        {
            "workload_or_system": "legacy_tms",
            "selected_target": "Azure SQL Managed Instance",
            "modernisation_disposition": "replatform",
            "decision_confidence": "medium",
            "selection_rationale": (
                "Best near-term fit for SQL Server-style OLTP with stored procedure coupling, "
                "history tables, compatibility risk, and limited downtime tolerance."
            ),
            "rejected_alternatives": (
                "Azure SQL Database rejected for first wave due to procedure/application coupling and "
                "unvalidated instance settings; SQL Server on Azure VM rejected because it retains more "
                "operational burden; Databricks rejected for transactional serving."
            ),
            "evidence_class": "derived evidence",
            "key_prerequisites": "procedure regression tests; identity discovery; performance baseline",
        },
        {
            "workload_or_system": "billing_ops",
            "selected_target": "Azure Database for PostgreSQL",
            "modernisation_disposition": "replatform",
            "decision_confidence": "medium",
            "selection_rationale": (
                "Preserves PostgreSQL-like relational semantics while reducing operational ownership."
            ),
            "rejected_alternatives": (
                "Azure SQL rejected because source is PostgreSQL-like and does not need SQL Server "
                "compatibility; Cosmos DB rejected because transactional relational billing constraints "
                "matter; retain rejected after identifier remediation."
            ),
            "evidence_class": "derived evidence",
            "key_prerequisites": "customer identifier mapping; billing reconciliation tests",
        },
        {
            "workload_or_system": "depot_partner_feeds",
            "selected_target": "Azure Databricks",
            "modernisation_disposition": "refactor",
            "decision_confidence": "medium",
            "selection_rationale": (
                "File feeds with schema drift and data-quality defects are best landed and validated "
                "through lakehouse ingestion patterns before serving."
            ),
            "rejected_alternatives": (
                "Azure SQL rejected as the primary landing target for raw drifted files; Cosmos DB "
                "not justified because the feeds are integration inputs, not document-serving workloads."
            ),
            "evidence_class": "locally measured",
            "key_prerequisites": "feed contracts; quarantine rules; replay design",
        },
        {
            "workload_or_system": "shipment_event_stream",
            "selected_target": "Azure Databricks",
            "modernisation_disposition": "refactor",
            "decision_confidence": "medium",
            "selection_rationale": (
                "Event-style JSONL fixtures map to future streaming ingestion, idempotency, ordering, "
                "and Delta bronze processing."
            ),
            "rejected_alternatives": (
                "Azure SQL rejected for raw event-stream landing at scale; Cosmos DB retained as a "
                "possible future serving option only if low-latency document access is proven."
            ),
            "evidence_class": "locally measured",
            "key_prerequisites": "deduplication keys; ordering strategy; schema evolution rules",
        },
        {
            "workload_or_system": "operational_reporting",
            "selected_target": "Azure Databricks",
            "modernisation_disposition": "refactor",
            "decision_confidence": "high",
            "selection_rationale": (
                "Reporting queries aggregate operational shipment tables and should be isolated from OLTP."
            ),
            "rejected_alternatives": (
                "Retain on OLTP rejected due to performance contention; Cosmos DB rejected because "
                "workload is analytical aggregation, not document lookup."
            ),
            "evidence_class": "locally measured",
            "key_prerequisites": "bronze/silver/gold modelling; freshness SLOs",
        },
        {
            "workload_or_system": "customer_service_search",
            "selected_target": "retain temporarily",
            "modernisation_disposition": "retain",
            "decision_confidence": "medium",
            "selection_rationale": (
                "Search/RAG use cases are planned but should wait for governed data products and access "
                "controls."
            ),
            "rejected_alternatives": (
                "Immediate Cosmos DB or AI search implementation rejected because Milestone 3 is an "
                "assessment phase and governance prerequisites are not complete."
            ),
            "evidence_class": "derived evidence",
            "key_prerequisites": "classification; access model; curated case/shipment data products",
        },
    ]


def migration_complexity() -> list[dict[str, Any]]:
    scores_by_system = {
        "legacy_tms": {
            "schema_complexity": 4,
            "feature_compatibility": 4,
            "application_coupling": 5,
            "data_volume": 4,
            "downtime_tolerance": 5,
            "integration_count": 5,
            "security_complexity": 4,
            "operational_criticality": 5,
            "performance_sensitivity": 5,
        },
        "billing_ops": {
            "schema_complexity": 3,
            "feature_compatibility": 2,
            "application_coupling": 3,
            "data_volume": 3,
            "downtime_tolerance": 3,
            "integration_count": 4,
            "security_complexity": 3,
            "operational_criticality": 3,
            "performance_sensitivity": 3,
        },
        "depot_partner_feeds": {
            "schema_complexity": 2,
            "feature_compatibility": 3,
            "application_coupling": 2,
            "data_volume": 2,
            "downtime_tolerance": 2,
            "integration_count": 4,
            "security_complexity": 2,
            "operational_criticality": 3,
            "performance_sensitivity": 2,
        },
        "shipment_event_stream": {
            "schema_complexity": 3,
            "feature_compatibility": 3,
            "application_coupling": 3,
            "data_volume": 4,
            "downtime_tolerance": 4,
            "integration_count": 4,
            "security_complexity": 3,
            "operational_criticality": 4,
            "performance_sensitivity": 4,
        },
    }
    output = []
    for system_id, scores in scores_by_system.items():
        total = round(sum(scores[key] * COMPLEXITY_WEIGHTS[key] for key in COMPLEXITY_WEIGHTS), 2)
        classification = "high" if total >= 3.8 else "medium" if total >= 2.6 else "low"
        output.append(
            {
                "system_id": system_id,
                **scores,
                "weighted_total": total,
                "complexity_classification": classification,
                "weights_profile": json.dumps(COMPLEXITY_WEIGHTS, sort_keys=True),
                "rationale": _complexity_rationale(system_id, classification),
            }
        )
    return output


def _complexity_rationale(system_id: str, classification: str) -> str:
    rationales = {
        "legacy_tms": "High coupling, business criticality, compatibility findings, and downtime pressure.",
        "billing_ops": "Moderate relational complexity with identifier reconciliation dependency.",
        "depot_partner_feeds": "Lower platform complexity but schema drift and replay controls required.",
        "shipment_event_stream": "Event ordering, idempotency, and freshness make migration medium-high.",
    }
    return f"{classification}: {rationales[system_id]}"


def migration_wave_plan() -> list[dict[str, Any]]:
    return [
        {
            "wave": "Wave 0",
            "wave_name": "Prerequisites and remediation",
            "included_systems": "all systems",
            "prerequisites": "identity discovery; performance baseline; data classification; test harness",
            "blockers": "unknown production collation; unknown SQL Agent dependencies; identity inventory",
            "expected_migration_approach": "no migration; assessment closure and remediation backlog",
            "validation_needs": "compatibility review; stakeholder sign-off; source owner validation",
            "rollback_considerations": "not applicable; no production change",
            "dependency_rationale": "Reduces uncertainty before any workload movement.",
        },
        {
            "wave": "Wave 1",
            "wave_name": "Low-risk feeds and analytical offload foundations",
            "included_systems": "depot_partner_feeds; operational_reporting",
            "prerequisites": "feed contracts; quarantine rules; medallion landing design",
            "blockers": "schema-drift handling not implemented yet",
            "expected_migration_approach": "refactor ingestion/reporting to lakehouse in later milestone",
            "validation_needs": "row-count reconciliation; duplicate detection; freshness checks",
            "rollback_considerations": "retain existing file/reporting paths until parallel validation passes",
            "dependency_rationale": "Offloads reporting pressure without changing OLTP writes first.",
        },
        {
            "wave": "Wave 2",
            "wave_name": "Secondary relational source",
            "included_systems": "billing_ops",
            "prerequisites": "identifier mapping; reconciliation tests; support-process validation",
            "blockers": "customer_ref mismatch and case referential anomalies",
            "expected_migration_approach": "replatform to Azure Database for PostgreSQL after remediation",
            "validation_needs": "invoice/payment reconciliation; case workflow tests",
            "rollback_considerations": "dual-run billing extracts and preserve source cutback path",
            "dependency_rationale": "Moderate criticality and fewer SQL Server compatibility constraints.",
        },
        {
            "wave": "Wave 3",
            "wave_name": "Business-critical transport OLTP",
            "included_systems": "legacy_tms",
            "prerequisites": "stored procedure regression; HA/DR design; identity transition; performance tests",
            "blockers": "compatibility findings SQL-COMP-001 through SQL-COMP-009",
            "expected_migration_approach": "replatform to Azure SQL Managed Instance first",
            "validation_needs": "transactional cutover rehearsal; load test; rollback runbook",
            "rollback_considerations": "point-in-time restore, replication rollback, and application cutback",
            "dependency_rationale": "Highest criticality should move after dependencies and tests mature.",
        },
    ]


def risk_register() -> list[dict[str, Any]]:
    risks = [
        ("RISK-001", "downtime risk", "medium", "high", "high", "Database operations lead"),
        ("RISK-002", "compatibility risk", "high", "high", "critical", "Database architect"),
        ("RISK-003", "data loss", "low", "high", "high", "Data engineering lead"),
        ("RISK-004", "performance regression", "medium", "high", "high", "Performance engineer"),
        ("RISK-005", "security misconfiguration", "medium", "high", "high", "Security architect"),
        ("RISK-006", "identity transition", "high", "medium", "high", "Identity engineer"),
        ("RISK-007", "dependency failure", "medium", "medium", "medium", "Integration lead"),
        ("RISK-008", "schema drift", "high", "medium", "high", "Data quality lead"),
        ("RISK-009", "operational readiness", "medium", "high", "high", "Operations owner"),
        ("RISK-010", "cost uncertainty", "medium", "medium", "medium", "FinOps owner"),
        (
            "RISK-011",
            "skills/operational ownership",
            "medium",
            "medium",
            "medium",
            "Platform owner",
        ),
    ]
    mitigations = {
        "downtime risk": "Require rehearsal, rollback plan, and business-approved outage window.",
        "compatibility risk": "Complete static and live compatibility assessment before target lock.",
        "data loss": "Use reconciliation checks, backups, and parallel-run validation.",
        "performance regression": "Capture baseline workload and load-test target before cutover.",
        "security misconfiguration": "Use least-privilege review and deployment policy checks.",
        "identity transition": "Inventory principals and test Entra/managed identity paths.",
        "dependency failure": "Map and test file, event, billing, and application dependencies.",
        "schema drift": "Implement contracts, quarantine, and schema evolution controls.",
        "operational readiness": "Complete runbooks, monitoring, and support handover.",
        "cost uncertainty": "Model tiers, storage growth, HA/DR, and Databricks workload costs.",
        "skills/operational ownership": "Assign service owners and train support teams before migration.",
    }
    return [
        {
            "risk_id": risk_id,
            "risk_category": category,
            "likelihood": likelihood,
            "impact": impact,
            "risk_rating": rating,
            "mitigation": mitigations[category],
            "owner_role": owner,
            "trigger_escalation_condition": f"Escalate when {category} mitigation lacks owner or date.",
        }
        for risk_id, category, likelihood, impact, rating, owner in risks
    ]


def inventory_rows() -> list[dict[str, Any]]:
    return [_dataclass_row(system) for system in SYSTEMS]


def dependency_rows() -> list[dict[str, Any]]:
    return [_dataclass_row(dependency) for dependency in DEPENDENCIES]


def compatibility_rows() -> list[dict[str, Any]]:
    return [_dataclass_row(finding) for finding in compatibility_findings()]


def _dataclass_row(instance: SourceSystem | Any) -> dict[str, Any]:
    return dict(instance.__dict__)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
