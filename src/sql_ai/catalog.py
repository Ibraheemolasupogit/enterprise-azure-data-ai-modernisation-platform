from __future__ import annotations

# ruff: noqa: E501
from sql_ai.model import EmbeddingConfig, EvaluationQuery, SourceDocument

EMBEDDING_CONFIG = EmbeddingConfig(
    provider="Azure OpenAI via Azure SQL external model boundary",
    embedding_model="text-embedding-3-small",
    model_version="configured-per-environment",
    dimensions=1536,
    distance_metric="cosine",
    external_model_name="ai.shipment_ops_embedding_model",
    endpoint_placeholder="$(AZURE_OPENAI_ENDPOINT)",
    identity_mode="Microsoft Entra managed identity",
)

SOURCE_DOCUMENTS = [
    SourceDocument("doc-shp-1001-status", "legacy_tms_curated", "shipment_status", "Shipment SHP1001 delay summary", "Shipment SHP1001 for account ACC-100 is delayed after a missed line haul connection on route R-NE-17. Latest operational status is held at depot D-NYC with expected departure after vehicle replacement. Customer service should explain the delay and cite carrier and depot updates only.", "SHP1001", "ACC-100", "D-NYC", "R-NE-17", "internal", "active", "2026-08-19T09:00:00Z"),
    SourceDocument("doc-shp-1001-carrier", "carrier_update_feed", "carrier_update", "Carrier update for SHP1001", "Carrier Northwind Freight reported a mechanical fault on trailer TR-44 for shipment SHP1001. The recovery unit reached D-NYC at 11:20 and the carrier expects route R-NE-17 to depart on the next outbound slot. No compensation decision is included in this update.", "SHP1001", "ACC-100", "D-NYC", "R-NE-17", "internal", "active", "2026-08-19T11:25:00Z"),
    SourceDocument("doc-shp-1001-case", "customer_service_export", "case_note", "Customer case CS-778 for SHP1001", "Case CS-778 records that the customer asked whether shipment SHP1001 can be expedited. The agent noted account ACC-100 is authorized for proactive delay notifications but the note does not approve discounts, refunds, or rerouting. Use depot and carrier facts before answering.", "SHP1001", "ACC-100", "D-NYC", "R-NE-17", "confidential", "active", "2026-08-19T12:00:00Z"),
    SourceDocument("doc-shp-1001-route", "depot_reference_feed", "depot_route", "Depot and route context for R-NE-17", "Depot D-NYC handles north east overflow for route R-NE-17. Standard customer messaging says weather, trailer replacement, and missed line haul events must be grounded in operational events. Route context is not proof of current shipment status by itself.", "SHP1001", "ACC-100", "D-NYC", "R-NE-17", "internal", "active", "2026-08-18T17:30:00Z"),
    SourceDocument("doc-shp-2002-billing", "billing_ops_curated", "billing_case", "Billing note for SHP2002", "Shipment SHP2002 has a billing hold for account ACC-200 after an invoice reference mismatch. The note may mention contact details and billing values, so only sanitized billing status can enter AI context. It is unrelated to SHP1001.", "SHP2002", "ACC-200", "D-CHI", "R-MW-09", "confidential", "active", "2026-08-18T08:15:00Z"),
]

EVALUATION_QUERIES = [
    EvaluationQuery("eval-001", "Why is shipment SHP1001 delayed and what did the carrier say?", (), "SHP1001", "ACC-100", 3),
    EvaluationQuery("eval-002", "Did the case note approve a refund or reroute for SHP1001?", (), "SHP1001", "ACC-100", 3),
    EvaluationQuery("eval-003", "What depot and route context applies to SHP1001?", (), "SHP1001", "ACC-100", 3),
    EvaluationQuery("eval-004", "What should customer service say about current SHP1001 status?", (), "SHP1001", "ACC-100", 3),
    EvaluationQuery("eval-005", "What billing restriction exists for SHP2002?", (), "SHP2002", "ACC-200", 2),
    EvaluationQuery("eval-006", "Can route context alone prove the current delay cause for SHP1001?", (), "SHP1001", "ACC-100", 3),
]

