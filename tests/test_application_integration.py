from __future__ import annotations

import json
from pathlib import Path

from application_integration.catalog import API_OPERATIONS, DAB_ENTITIES, MCP_TOOLS

ROOT = Path(__file__).resolve().parents[1]


def test_api_catalog_is_allowlisted_and_authenticated() -> None:
    assert API_OPERATIONS
    assert all(operation.auth_required == "yes" for operation in API_OPERATIONS)
    assert all(operation.backing_object for operation in API_OPERATIONS)
    assert all(operation.required_role for operation in API_OPERATIONS)
    assert not any("arbitrary" in operation.backing_object.lower() for operation in API_OPERATIONS)
    assert {operation.use_case for operation in API_OPERATIONS} >= {
        "Shipment lookup",
        "Operational reference lookup",
        "Customer-service case retrieval",
        "AI retrieval",
        "AI grounding sources",
    }


def test_dab_configuration_has_no_anonymous_production_permissions() -> None:
    config = json.loads(
        (ROOT / "src/api/dab/dab-config.production.json").read_text(encoding="utf-8")
    )
    assert config["runtime"]["host"]["authentication"]["provider"] == "EntraID"
    assert config["runtime"]["graphql"]["allow-introspection"] is False
    for entity in config["entities"].values():
        permissions = entity["permissions"]
        assert permissions
        assert all(permission["role"].lower() != "anonymous" for permission in permissions)


def test_dab_entities_match_catalog_and_restrict_sensitive_fields() -> None:
    restricted = {entity.entity: entity.field_restrictions for entity in DAB_ENTITIES}
    assert "CustomerEmail" in restricted["ShipmentSummary"]
    assert "DeclaredValueAmount" in restricted["ShipmentSummary"]
    assert "raw notes" in restricted["ServiceCaseSummary"].lower()
    assert all(entity.production_anonymous == "none" for entity in DAB_ENTITIES)


def test_mcp_tools_are_schema_constrained_and_read_focused() -> None:
    schemas = json.loads((ROOT / "src/api/mcp/tool-schemas.json").read_text(encoding="utf-8"))
    for tool in MCP_TOOLS:
        assert tool.tool_name in schemas["tools"]
        assert tool.read_write in {"read", "controlled action"}
        input_schema = schemas["tools"][tool.tool_name]["input"]
        assert input_schema["additionalProperties"] is False
        assert tool.required_role
        assert tool.audit_required == "yes"


def test_ai_endpoint_propagates_authorization_and_bounded_inputs() -> None:
    openapi = (ROOT / "src/api/contracts/openapi.yaml").read_text(encoding="utf-8")
    assert "/api/ai/query" in openapi
    assert "ai_query_user" in openapi
    assert "maximum: 5" in openapi
    procedure = (ROOT / "src/azure_sql/api/02_api_procedures.sql").read_text(encoding="utf-8")
    assert "usp_ApiAskGroundedOperationsQuestion" in procedure
    assert "authorization must be enforced before retrieval" in procedure


def test_security_scenarios_cover_negative_cases() -> None:
    scenarios = {
        "anonymous access attempt",
        "cross-customer retrieval attempt",
        "restricted field request",
        "injection-like input",
        "invalid MCP tool input",
        "non-allowlisted database object attempt",
    }
    catalog = (ROOT / "src/application_integration/cli.py").read_text(encoding="utf-8")
    for scenario in scenarios:
        assert scenario in catalog

