from __future__ import annotations

# ruff: noqa: E501
from fabric_integration.model import ContractField, FabricProduct, PatternDecision

EVIDENCE_CLASSES = {
    "locally validated",
    "configuration defined",
    "simulated",
    "requires Fabric runtime validation",
    "requires Azure validation",
}

PRODUCTS = [
    FabricProduct("fabric-prod-001", "gold.shipment_operations_performance", "Azure Data & AI platform", "daily by shipment status", "silver.shipments", "Azure Databricks Gold", "1.0.0", "daily after Gold publication", "operational", "critical checks passed", "eligible"),
    FabricProduct("fabric-prod-002", "gold.depot_route_performance", "Azure Data & AI platform", "daily by route and depot", "silver.shipments; silver.depots_routes", "Azure Databricks Gold", "1.0.0", "daily after route/depot Gold publication", "operational", "critical checks passed", "eligible"),
    FabricProduct("fabric-prod-003", "gold.delivery_delay_metrics", "Azure Data & AI platform", "delivery date", "silver.shipments; silver.shipment_events", "Azure Databricks Gold", "1.0.0", "daily after delivery metric publication", "operational", "critical checks passed", "eligible"),
    FabricProduct("fabric-prod-004", "gold.billing_revenue_summary", "Azure Data & AI platform", "invoice month and status", "silver.billing_invoices", "Azure Databricks Gold", "1.0.0", "daily after billing Gold publication", "financial confidential", "critical checks passed", "eligible with finance consumer restriction"),
    FabricProduct("fabric-prod-005", "gold.service_incident_summary", "Azure Data & AI platform", "daily by case reason/status", "silver.service_cases", "Azure Databricks Gold", "1.0.0", "daily after service Gold publication", "confidential service data", "critical checks passed", "eligible with service consumer restriction"),
]

PATTERN_DECISIONS = [
    PatternDecision("fabric-prod-001", "OneLake shortcut to ADLS Gen2/Delta publication boundary", "preferred", "operational analytics and BI serving", "no-copy", "depends on Gold completion and shortcut refresh behavior", "Azure owns source access; Fabric owns downstream permissions", "Azure produces; Fabric consumes", "minimizes duplicate storage and repeated transformation", "moderate setup; low ongoing copy operations", "requires supported Delta/shortcut configuration and Fabric runtime validation"),
    PatternDecision("fabric-prod-002", "OneLake shortcut to ADLS Gen2/Delta publication boundary", "preferred", "depot and route performance analytics", "no-copy", "daily producer freshness", "regional restrictions must be carried into Fabric-side RLS", "shared sensitivity/identity handoff", "avoids duplicate route aggregates", "moderate", "Fabric must enforce downstream regional access"),
    PatternDecision("fabric-prod-003", "OneLake shortcut to ADLS Gen2/Delta publication boundary", "preferred", "delay trend analytics", "no-copy", "daily producer freshness", "quality manifest travels with product", "Azure produces; Fabric models", "avoids duplicate delay calculations", "moderate", "Fabric semantic model ownership remains separate"),
    PatternDecision("fabric-prod-004", "controlled batch copy from published Gold boundary", "conditional", "finance reporting where retention snapshots are required", "copy likely", "daily or monthly close aligned", "finance sensitivity and retention controls required", "Azure publishes; Fabric snapshots if needed", "adds storage/retention duplication", "higher due reconciliation and lifecycle", "use only if finance snapshot/audit requirements justify copying"),
    PatternDecision("fabric-prod-005", "OneLake shortcut to sanitized Gold aggregate", "preferred", "service incident trend analytics", "no-copy", "daily producer freshness", "raw service case details are not included", "Azure owns sanitization; Fabric owns downstream model", "minimizes duplicate sensitive data", "moderate", "Fabric must not infer or request raw case notes by default"),
]

CONTRACT_FIELDS = [
    ContractField("gold.shipment_operations_performance", "1.0.0", "event_date", "date", "no", "primary", "Gold aggregation date", "operational", "analytics", "daily", "critical checks passed", "active"),
    ContractField("gold.shipment_operations_performance", "1.0.0", "shipment_status", "string", "no", "primary", "Normalized shipment status", "operational", "analytics", "daily", "valid status domain", "active"),
    ContractField("gold.shipment_operations_performance", "1.0.0", "shipment_count", "integer", "no", "measure", "Number of shipments", "operational", "analytics", "daily", "non-negative", "active"),
    ContractField("gold.depot_route_performance", "1.0.0", "event_date", "date", "no", "primary", "Aggregation date", "operational", "regional analytics", "daily", "critical checks passed", "active"),
    ContractField("gold.depot_route_performance", "1.0.0", "depot_code", "string", "no", "primary", "Depot natural key", "operational", "regional analytics", "daily", "known depot", "active"),
    ContractField("gold.depot_route_performance", "1.0.0", "route_id", "string", "no", "primary", "Route identifier", "operational", "regional analytics", "daily", "known route", "active"),
    ContractField("gold.delivery_delay_metrics", "1.0.0", "delivery_date", "date", "no", "primary", "Delivery date", "operational", "analytics", "daily", "critical checks passed", "active"),
    ContractField("gold.delivery_delay_metrics", "1.0.0", "late_rate", "decimal", "no", "measure", "Share of late deliveries", "operational", "analytics", "daily", "between 0 and 1", "active"),
    ContractField("gold.billing_revenue_summary", "1.0.0", "invoice_month", "string", "no", "primary", "Invoice month", "financial confidential", "finance analytics", "daily/monthly", "critical checks passed", "active"),
    ContractField("gold.billing_revenue_summary", "1.0.0", "net_revenue_gbp", "decimal", "no", "measure", "Net revenue in GBP", "financial confidential", "finance analytics", "daily/monthly", "non-negative unless adjustment flagged", "active"),
    ContractField("gold.service_incident_summary", "1.0.0", "case_date", "date", "no", "primary", "Service case opened date", "confidential service data", "service analytics", "daily", "critical checks passed", "active"),
    ContractField("gold.service_incident_summary", "1.0.0", "case_count", "integer", "no", "measure", "Number of service cases", "confidential service data", "service analytics", "daily", "non-negative", "active"),
]

