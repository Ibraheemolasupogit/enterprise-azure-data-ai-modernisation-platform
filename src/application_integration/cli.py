from __future__ import annotations

# ruff: noqa: E501
import argparse
import csv
from dataclasses import asdict
from pathlib import Path
from typing import Any

from application_integration.catalog import API_OPERATIONS, DAB_ENTITIES, MCP_TOOLS, ROLES
from application_integration.validation import validate_outputs


def generate_outputs(outputs_dir: Path, reports_dir: Path, repo_root: Path | None = None) -> dict[str, Path]:
    outputs_dir.mkdir(parents=True, exist_ok=True)
    reports_dir.mkdir(parents=True, exist_ok=True)
    outputs = {
        "api_catalog.csv": [asdict(row) | {"evidence_classification": "configuration defined"} for row in API_OPERATIONS],
        "dab_entity_catalog.csv": [asdict(row) for row in DAB_ENTITIES],
        "api_authorization_matrix.csv": _authorization_matrix(),
        "sensitive_field_exposure.csv": _sensitive_field_exposure(),
        "ai_endpoint_contract.csv": _ai_endpoint_contract(),
        "mcp_tool_catalog.csv": [asdict(row) for row in MCP_TOOLS],
        "mcp_security_matrix.csv": _mcp_security_matrix(),
        "hosting_decision.csv": _hosting_decision(),
        "resilience_policy.csv": _resilience_policy(),
        "error_catalog.csv": _error_catalog(),
        "rate_limit_policy.csv": _rate_limit_policy(),
        "observability_catalog.csv": _observability_catalog(),
        "audit_traceability.csv": _audit_traceability(),
        "security_test_scenarios.csv": _security_test_scenarios(),
        "integration_readiness.csv": _integration_readiness(),
    }
    written: dict[str, Path] = {}
    for filename, rows in outputs.items():
        path = outputs_dir / filename
        _write_csv(path, rows)
        written[filename] = path
    report = reports_dir / "application_integration_report.md"
    report.write_text(_report(), encoding="utf-8")
    written["application_integration_report.md"] = report
    failures = validate_outputs(outputs_dir, repo_root or Path.cwd())
    if failures:
        joined = "\n".join(f"- {failure}" for failure in failures)
        raise RuntimeError(f"Application integration validation failed:\n{joined}")
    return written


def _write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def _authorization_matrix() -> list[dict[str, str]]:
    return [
        {
            "role": role,
            "allowed_access": allowed,
            "denied_access": denied,
            "entra_mapping": f"appRole:{role}",
            "database_role": role,
            "evidence_classification": "configuration defined",
        }
        for role, allowed, denied in ROLES
    ]


def _sensitive_field_exposure() -> list[dict[str, str]]:
    rows = [
        ("shipment status", "dbo.vw_ApiShipmentSummary.Status", "API-visible", "shipment_reader", "operational status is required for lookup"),
        ("customer contact information", "CustomerEmail, Phone", "masked", "customer_service_user", "mask in API views; do not return through DAB field list"),
        ("declared shipment value", "DeclaredValueAmount", "never exposed", "none", "excluded from application-facing views"),
        ("billing information", "Invoice and payment fields", "restricted", "none", "not part of Milestone 14 API allowlist"),
        ("service-case notes", "RawCaseNotes", "restricted", "customer_service_user", "sanitized summary only; raw notes remain hidden"),
        ("AI retrieval context", "ai.DocumentChunk.Content", "restricted", "ai_query_user", "returned only through grounded citation-bound procedure output"),
    ]
    return [
        {
            "data_category": category,
            "field_or_source": field,
            "exposure_decision": decision,
            "required_role": role,
            "control": control,
            "evidence_classification": "configuration defined",
        }
        for category, field, decision, role, control in rows
    ]


def _ai_endpoint_contract() -> list[dict[str, str]]:
    return [
        {
            "endpoint": "POST /api/ai/query",
            "input_contract": "question; optional shipmentId/accountId/routeCode scope; topK between 1 and 5; correlationId",
            "output_contract": "answer; sourceReferences[]; evidenceStatus; requestId; errorState",
            "backing_procedure": "ai.usp_ApiAskGroundedOperationsQuestion",
            "authorization_propagation": "required",
            "grounding_policy": "use retrieved authorized context only; insufficiency is valid output",
            "evidence_classification": "configuration defined",
        }
    ]


def _mcp_security_matrix() -> list[dict[str, str]]:
    controls = [
        ("allowlisted operations", "tools are fixed catalog entries and map to explicit API/procedure boundaries"),
        ("strict schemas", "JSON schemas reject unknown fields, oversize inputs, and invalid identifiers"),
        ("least privilege", "each tool requires one application role and database role"),
        ("no arbitrary SQL", "tool inputs cannot carry SQL fragments or object names"),
        ("no arbitrary URLs", "tools do not accept callback or fetch URLs"),
        ("no shell execution", "MCP boundary exposes no shell, file, or process tools"),
        ("auditable calls", "correlation ID, identity, role, tool name, backing endpoint, and status are logged"),
        ("identity propagation", "caller identity and selected role flow into API authorization where supported"),
    ]
    return [
        {"control": control, "implementation": implementation, "evidence_classification": "configuration defined"}
        for control, implementation in controls
    ]


def _hosting_decision() -> list[dict[str, str]]:
    return [
        {"hosting_option": "Azure Container Apps", "decision": "selected", "reason": "fits containerized DAB/API runtime, managed identity, ingress control, revisioning, scaling, and Log Analytics integration", "boundary": "Bicep is switch-gated; no deployment performed", "evidence_classification": "configuration defined"},
        {"hosting_option": "Azure App Service", "decision": "rejected for now", "reason": "valid option, but less aligned with containerized DAB plus sidecar/API deployment pattern used here", "boundary": "may be reconsidered for App Service Easy Auth standardization", "evidence_classification": "configuration defined"},
        {"hosting_option": "Azure Static Web Apps", "decision": "not selected", "reason": "front-end hosting only; Milestone 14 does not build a front end", "boundary": "future UI boundary only", "evidence_classification": "configuration defined"},
        {"hosting_option": "Azure API Management", "decision": "documented boundary", "reason": "appropriate for external consumers, central policy, developer portal, versioning, and enterprise rate limiting", "boundary": "not added by default to avoid unnecessary complexity", "evidence_classification": "configuration defined"},
    ]


def _resilience_policy() -> list[dict[str, str]]:
    rows = []
    for operation in API_OPERATIONS:
        timeout = "10s" if operation.rate_limit_class != "ai_query" else "30s"
        retry = "retry idempotent read transient failures only" if operation.read_write == "read" else "no automatic replay of generation action after body accepted"
        rows.append(
            {
                "api_id": operation.api_id,
                "timeout": timeout,
                "retry_policy": retry,
                "circuit_breaker_boundary": "API host dependency policy; requires runtime implementation",
                "pagination_or_size_limit": "page size <= 100; AI question <= 2000 chars; topK <= 5",
                "evidence_classification": "configuration defined",
            }
        )
    return rows


def _error_catalog() -> list[dict[str, str]]:
    rows = [
        ("authentication failure", "401", "Missing or invalid Entra token.", "Do not reveal identity provider internals."),
        ("authorization failure", "403", "Caller is not allowed to access this resource.", "Do not reveal row existence across customers."),
        ("not found", "404", "Requested resource was not found.", "Use same response for inaccessible scoped rows where appropriate."),
        ("invalid request", "400", "Request failed validation.", "Return field-level validation codes without SQL details."),
        ("dependency timeout", "504", "A dependency timed out.", "Hide SQL/OpenAI endpoint details."),
        ("database unavailable", "503", "Database dependency is unavailable.", "No schema or connection details."),
        ("AI unavailable", "503", "AI dependency is unavailable.", "No model endpoint internals."),
        ("insufficient grounding", "422", "Answer cannot be generated from authorized context.", "Expected safe outcome."),
        ("throttling", "429", "Rate limit exceeded.", "Return retry-after when implemented."),
    ]
    return [
        {
            "error_class": klass,
            "http_status": status,
            "client_message": message,
            "leakage_control": control,
            "evidence_classification": "configuration defined",
        }
        for klass, status, message, control in rows
    ]


def _rate_limit_policy() -> list[dict[str, str]]:
    rows = [
        ("operational_lookup", "standard", "shipment/depot/route reads", "idempotent read; bounded page size"),
        ("customer_service_lookup", "moderate", "case summaries", "confidential data; tighter per-user controls"),
        ("ai_query", "strict", "grounded AI question endpoint", "cost-aware; topK and request-size bounded"),
        ("audit_lookup", "restricted", "AI citation/audit source references", "auditor role only"),
        ("administrative_endpoint", "restricted", "health/readiness/admin diagnostics", "internal access only"),
    ]
    return [
        {
            "rate_limit_class": klass,
            "relative_limit": limit,
            "applies_to": applies,
            "rationale": rationale,
            "implementation_boundary": "gateway/API host policy; no unsupported gateway implementation claimed",
            "evidence_classification": "configuration defined",
        }
        for klass, limit, applies, rationale in rows
    ]


def _observability_catalog() -> list[dict[str, str]]:
    return [
        {
            "api_id": operation.api_id,
            "signals": "request count; duration; failures; dependency duration; auth failures; throttling; correlation ID",
            "log_sink": "Application Insights, Azure Monitor, Log Analytics",
            "sensitive_payload_policy": "log hashes, IDs, and status metadata only; do not log prompts/source payloads indiscriminately",
            "evidence_classification": "configuration defined",
        }
        for operation in API_OPERATIONS
    ]


def _audit_traceability() -> list[dict[str, str]]:
    return [
        {
            "consumer": "application user",
            "operation": operation.route_or_entity,
            "authorization_role": operation.required_role,
            "database_object": operation.backing_object,
            "data_sensitivity": operation.sensitivity,
            "audit_signal": f"correlationId -> {operation.api_id} -> SQL dependency -> response status",
            "evidence_classification": "configuration defined",
        }
        for operation in API_OPERATIONS
    ] + [
        {
            "consumer": "AI endpoint",
            "operation": "POST /api/ai/query",
            "authorization_role": "ai_query_user",
            "database_object": "ai.usp_ApiAskGroundedOperationsQuestion -> ai.usp_AssembleRagContext",
            "data_sensitivity": "confidential",
            "audit_signal": "API correlationId -> RetrievalAuditId -> GenerationAuditId -> citation chunk ids",
            "evidence_classification": "configuration defined",
        }
    ]


def _security_test_scenarios() -> list[dict[str, str]]:
    rows = [
        ("anonymous access attempt", "call protected DAB entity without token", "401/403 and no data"),
        ("unauthorized role", "call ServiceCaseSummary as shipment_reader", "403 and no row-count hints"),
        ("cross-customer retrieval attempt", "AI query with shipment outside authorized account", "insufficient context or 403"),
        ("restricted field request", "request CustomerEmail or DeclaredValueAmount", "field unavailable/rejected"),
        ("injection-like input", "question contains SQL/control instructions", "treated as data, no dynamic SQL"),
        ("oversized request", "AI question exceeds size limit or topK > 5", "400 validation error"),
        ("invalid MCP tool input", "unknown fields or malformed IDs", "schema validation failure"),
        ("non-allowlisted database object attempt", "try table/object name input", "400/403; no arbitrary SQL path"),
    ]
    return [
        {
            "scenario": scenario,
            "test_input": test_input,
            "expected_result": expected,
            "claim_boundary": "deterministic contract/security validation; not penetration testing",
            "evidence_classification": "locally validated",
        }
        for scenario, test_input, expected in rows
    ]


def _integration_readiness() -> list[dict[str, str]]:
    return [
        {"capability": "API catalog and allowlist", "status": "locally validated", "evidence": "api_catalog.csv and tests"},
        {"capability": "DAB production configuration", "status": "configuration defined", "evidence": "src/api/dab/dab-config.production.json"},
        {"capability": "REST and GraphQL contracts", "status": "configuration defined", "evidence": "src/api/contracts"},
        {"capability": "SQL API views/procedures/roles", "status": "requires Azure validation", "evidence": "src/azure_sql/api/*.sql"},
        {"capability": "Container Apps hosting/IaC", "status": "configuration defined", "evidence": "infra/modules/application-integration/container-apps.bicep"},
        {"capability": "MCP tool boundary", "status": "configuration defined", "evidence": "src/api/mcp"},
        {"capability": "Runtime DAB/API smoke test", "status": "requires application runtime validation", "evidence": "DAB runtime and Azure SQL not executed locally"},
    ]


def _report() -> str:
    return "\n".join(
        [
            "# Secure Application and API Integration Report",
            "",
            "Milestone 14 defines a secure application/API integration layer for selected Azure SQL, SQL AI, and governed application-facing data capabilities. It covers Data API Builder, REST, GraphQL, stored-procedure boundaries, Entra authentication, managed identity, Container Apps hosting, MCP-compatible tool consumption, observability, resilience, CI/CD validation, and deterministic evidence.",
            "",
            "## Scope",
            "",
            "The API surface is allowlisted and read-focused. It exposes shipment lookup, operational reference lookup, sanitized customer-service case retrieval, governed AI retrieval/RAG execution, and grounding source metadata. It does not expose arbitrary SQL, raw administrative tables, destructive tools, a chatbot UI, or autonomous operational actions.",
            "",
            "## Runtime Boundary",
            "",
            "Local validation checks configuration, catalogs, schemas, mappings, security scenarios, and evidence consistency. Azure SQL object execution, Data API Builder runtime behavior, Entra token validation, managed identity to SQL, Container Apps hosting, and Azure OpenAI integration require Azure or application runtime validation.",
            "",
        ]
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate application integration evidence.")
    parser.add_argument("--outputs-dir", type=Path, default=Path("outputs/application_integration"))
    parser.add_argument("--reports-dir", type=Path, default=Path("reports"))
    args = parser.parse_args()
    written = generate_outputs(args.outputs_dir, args.reports_dir, Path.cwd())
    for name in sorted(written):
        print(f"{name}: {written[name]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
