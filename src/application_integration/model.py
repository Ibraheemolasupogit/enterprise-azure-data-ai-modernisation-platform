from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ApiOperation:
    api_id: str
    use_case: str
    operation: str
    protocol: str
    route_or_entity: str
    backing_object: str
    read_write: str
    sensitivity: str
    required_role: str
    auth_required: str
    rate_limit_class: str
    audit_required: str
    runtime_validation: str


@dataclass(frozen=True)
class DabEntity:
    entity: str
    source_object: str
    source_type: str
    rest_enabled: str
    graphql_enabled: str
    allowed_roles: str
    allowed_actions: str
    field_restrictions: str
    production_anonymous: str
    evidence_classification: str


@dataclass(frozen=True)
class McpTool:
    tool_name: str
    purpose: str
    input_schema_ref: str
    output_schema_ref: str
    required_role: str
    backing_api_or_procedure: str
    read_write: str
    data_sensitivity: str
    audit_required: str
    evidence_classification: str

