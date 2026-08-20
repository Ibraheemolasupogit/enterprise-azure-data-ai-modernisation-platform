from __future__ import annotations

# ruff: noqa: E501
from application_integration.model import ApiOperation, DabEntity, McpTool

EVIDENCE_CLASSES = {
    "locally validated",
    "configuration defined",
    "simulated",
    "requires Azure validation",
    "requires application runtime validation",
}

API_OPERATIONS = [
    ApiOperation("api-001", "Shipment lookup", "GET shipment summary", "REST", "/api/ShipmentSummary/{ShipmentId}", "dbo.vw_ApiShipmentSummary", "read", "internal", "shipment_reader", "yes", "operational_lookup", "yes", "requires application runtime validation"),
    ApiOperation("api-002", "Shipment lookup", "GET shipment events", "REST", "/api/ShipmentEvents?$filter=ShipmentId eq {id}", "dbo.vw_ApiShipmentEvent", "read", "internal", "shipment_reader", "yes", "operational_lookup", "yes", "requires application runtime validation"),
    ApiOperation("api-003", "Operational reference lookup", "GET depot/route context", "REST", "/api/RouteContext", "dbo.vw_ApiRouteContext", "read", "internal", "operations_reader", "yes", "operational_lookup", "yes", "requires application runtime validation"),
    ApiOperation("api-004", "Customer-service case retrieval", "GET case summary", "REST", "/api/ServiceCaseSummary", "dbo.vw_ApiServiceCaseSummary", "read", "confidential", "customer_service_user", "yes", "customer_service_lookup", "yes", "requires application runtime validation"),
    ApiOperation("api-005", "AI retrieval", "POST grounded operations question", "REST", "/api/ai/query", "ai.usp_ApiAskGroundedOperationsQuestion", "controlled action", "confidential", "ai_query_user", "yes", "ai_query", "yes", "requires Azure validation"),
    ApiOperation("api-006", "AI grounding sources", "GET answer source references", "REST", "/api/GroundingSourceReference", "ai.vw_ApiGroundingSourceReference", "read", "confidential", "ai_auditor", "yes", "audit_lookup", "yes", "requires application runtime validation"),
    ApiOperation("api-007", "Shipment lookup", "GraphQL shipment summary query", "GraphQL", "shipmentSummary", "dbo.vw_ApiShipmentSummary", "read", "internal", "shipment_reader", "yes", "operational_lookup", "yes", "requires application runtime validation"),
    ApiOperation("api-008", "Operational reference lookup", "GraphQL route context query", "GraphQL", "routeContext", "dbo.vw_ApiRouteContext", "read", "internal", "operations_reader", "yes", "operational_lookup", "yes", "requires application runtime validation"),
]

DAB_ENTITIES = [
    DabEntity("ShipmentSummary", "dbo.vw_ApiShipmentSummary", "view", "true", "true", "shipment_reader; customer_service_user", "read", "exclude: CustomerEmail, DeclaredValueAmount", "none", "configuration defined"),
    DabEntity("ShipmentEvents", "dbo.vw_ApiShipmentEvent", "view", "true", "false", "shipment_reader; customer_service_user", "read", "include operational status fields only", "none", "configuration defined"),
    DabEntity("RouteContext", "dbo.vw_ApiRouteContext", "view", "true", "true", "operations_reader; customer_service_user", "read", "include depot/route/carrier context only", "none", "configuration defined"),
    DabEntity("ServiceCaseSummary", "dbo.vw_ApiServiceCaseSummary", "view", "true", "false", "customer_service_user", "read", "exclude raw notes/contact/billing fields", "none", "configuration defined"),
    DabEntity("GroundingSourceReference", "ai.vw_ApiGroundingSourceReference", "view", "true", "false", "ai_auditor; ai_query_user", "read", "source/citation metadata only", "none", "configuration defined"),
    DabEntity("AskGroundedOperationsQuestion", "ai.usp_ApiAskGroundedOperationsQuestion", "stored-procedure", "true", "false", "ai_query_user", "execute", "bounded input/output contract", "none", "configuration defined"),
]

MCP_TOOLS = [
    McpTool("get_shipment_status", "Return allowlisted shipment status summary.", "src/api/mcp/tool-schemas.json#/tools/get_shipment_status/input", "src/api/mcp/tool-schemas.json#/tools/get_shipment_status/output", "shipment_reader", "GET /api/ShipmentSummary/{ShipmentId}", "read", "internal", "yes", "configuration defined"),
    McpTool("get_shipment_history", "Return shipment event history for an authorized shipment.", "src/api/mcp/tool-schemas.json#/tools/get_shipment_history/input", "src/api/mcp/tool-schemas.json#/tools/get_shipment_history/output", "shipment_reader", "GET /api/ShipmentEvents", "read", "internal", "yes", "configuration defined"),
    McpTool("get_route_context", "Return depot, route, and carrier context.", "src/api/mcp/tool-schemas.json#/tools/get_route_context/input", "src/api/mcp/tool-schemas.json#/tools/get_route_context/output", "operations_reader", "GET /api/RouteContext", "read", "internal", "yes", "configuration defined"),
    McpTool("search_operational_knowledge", "Run bounded metadata-filtered operational retrieval.", "src/api/mcp/tool-schemas.json#/tools/search_operational_knowledge/input", "src/api/mcp/tool-schemas.json#/tools/search_operational_knowledge/output", "ai_query_user", "ai.usp_ApiSearchOperationalKnowledge", "read", "confidential", "yes", "configuration defined"),
    McpTool("ask_grounded_operations_question", "Ask a grounded shipment operations question with citations.", "src/api/mcp/tool-schemas.json#/tools/ask_grounded_operations_question/input", "src/api/mcp/tool-schemas.json#/tools/ask_grounded_operations_question/output", "ai_query_user", "POST /api/ai/query", "controlled action", "confidential", "yes", "requires Azure validation"),
]

ROLES = [
    ("shipment_reader", "read shipment summary/status/history through allowlisted views", "no service-case notes, no AI generation, no arbitrary SQL"),
    ("operations_reader", "read depot/route/carrier reference context", "no customer case or AI payload access"),
    ("customer_service_user", "read authorized shipment and sanitized case summaries", "no raw notes, declared values, billing details, or cross-customer records"),
    ("ai_query_user", "execute governed retrieval/RAG API and read citation metadata", "no direct AI table ownership or unrestricted context access"),
    ("ai_auditor", "read AI retrieval/generation audit summaries and citation metadata", "no unrestricted sensitive payload reads"),
    ("api_runtime_identity", "managed identity used by API host/DAB to connect to Azure SQL", "no db_owner, no ad hoc write grants"),
    ("api_deployment_identity", "deploy app configuration and infrastructure through controlled pipeline", "no runtime data-plane access"),
]

