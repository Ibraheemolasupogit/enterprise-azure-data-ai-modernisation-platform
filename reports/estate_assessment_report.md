# Estate Assessment and Modernisation Decisioning

Milestone 3 produces a deterministic local assessment of the synthetic Contoso Freight estate. It does not run Microsoft cloud assessment tools, deploy Azure resources, or perform migration.

## Evidence Boundary

- Locally measured: derived from repository scripts, contracts, samples, or workload fixtures.
- Derived evidence: inferred from the synthetic estate design and deterministic workload model.
- Synthetic assumption: explicit planning assumption used to make the assessment realistic.
- Requires live estate validation: cannot be proven from local fixtures and must be checked in a real customer environment.

## Current-State Findings

- Source systems assessed: 4.
- Compatibility findings: 9 total, 1 high severity.
- High-complexity migrations: legacy_tms.
- The legacy transport management system is the most constrained workload because of stored procedure coupling, reporting contention, history growth, and unvalidated instance settings.
- Billing and service operations are relational but have cross-source identifier mismatch that must be remediated before integrated migration or analytics.
- File and event feeds are better treated as ingestion and data-quality candidates than as direct database migration units.

## Workload Segmentation

| Workload | Category | Evidence |
| --- | --- | --- |
| analytical_delay_report | analytical | locally measured |
| create_shipment | transactional OLTP | locally measured |
| customer_lookup | transactional OLTP | locally measured |
| incident_case_creation | customer-service/search | locally measured |
| invoice_lookup | transactional OLTP | locally measured |
| route_depot_reporting | operational reporting | locally measured |
| update_shipment_status | event/streaming | locally measured |

## Recommended Azure Targets

| Workload/System | Selected target | Disposition | Rationale |
| --- | --- | --- | --- |
| legacy_tms | Azure SQL Managed Instance | replatform | Best near-term fit for SQL Server-style OLTP with stored procedure coupling, history tables, compatibility risk, and limited downtime tolerance. |
| billing_ops | Azure Database for PostgreSQL | replatform | Preserves PostgreSQL-like relational semantics while reducing operational ownership. |
| depot_partner_feeds | Azure Databricks | refactor | File feeds with schema drift and data-quality defects are best landed and validated through lakehouse ingestion patterns before serving. |
| shipment_event_stream | Azure Databricks | refactor | Event-style JSONL fixtures map to future streaming ingestion, idempotency, ordering, and Delta bronze processing. |
| operational_reporting | Azure Databricks | refactor | Reporting queries aggregate operational shipment tables and should be isolated from OLTP. |
| customer_service_search | retain temporarily | retain | Search/RAG use cases are planned but should wait for governed data products and access controls. |

## Migration Strategy

- Complete Wave 0 discovery and remediation before moving production workloads.
- Offload low-risk feeds and operational reporting before moving the core OLTP system.
- Replatform PostgreSQL-like billing separately from SQL Server-style transport workloads.
- Move the business-critical transport OLTP workload only after compatibility, identity, HA/DR, and performance baselines are validated.

## Migration Waves

| Wave | Included systems | Approach |
| --- | --- | --- |
| Wave 0 - Prerequisites and remediation | all systems | no migration; assessment closure and remediation backlog |
| Wave 1 - Low-risk feeds and analytical offload foundations | depot_partner_feeds; operational_reporting | refactor ingestion/reporting to lakehouse in later milestone |
| Wave 2 - Secondary relational source | billing_ops | replatform to Azure Database for PostgreSQL after remediation |
| Wave 3 - Business-critical transport OLTP | legacy_tms | replatform to Azure SQL Managed Instance first |

## Major Risks

| Risk | Rating | Mitigation |
| --- | --- | --- |
| downtime risk | high | Require rehearsal, rollback plan, and business-approved outage window. |
| compatibility risk | critical | Complete static and live compatibility assessment before target lock. |
| data loss | high | Use reconciliation checks, backups, and parallel-run validation. |
| performance regression | high | Capture baseline workload and load-test target before cutover. |
| security misconfiguration | high | Use least-privilege review and deployment policy checks. |
| identity transition | high | Inventory principals and test Entra/managed identity paths. |
| schema drift | high | Implement contracts, quarantine, and schema evolution controls. |
| operational readiness | high | Complete runbooks, monitoring, and support handover. |

## Prerequisites

- Live estate validation for database size, growth, collation, SQL Agent dependencies, identity model, and production workload telemetry.
- Procedure-level regression tests for shipment create/update behaviour.
- Data classification and access model for customer, billing, case, and operational event data.
- Reconciliation framework for invoice, payment, shipment, and event counts.
- HA/DR and rollback design before business-critical workload movement.

## Unresolved Questions for a Real Environment

- What are the actual database sizes, growth rates, query baselines, wait statistics, and peak concurrency?
- Which SQL Agent jobs, linked servers, CLR objects, SSIS packages, or filesystem dependencies exist outside the local source scripts?
- What identities, groups, application credentials, and privileged access paths are currently used?
- What outage windows and contractual RTO/RPO commitments have business approval?
- Which reports are still required, and which can be retired or replaced by curated data products?
