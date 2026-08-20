from __future__ import annotations

import csv
import json
from pathlib import Path

from application_integration.catalog import EVIDENCE_CLASSES

REQUIRED_FILES = [
    "api_catalog.csv",
    "dab_entity_catalog.csv",
    "api_authorization_matrix.csv",
    "sensitive_field_exposure.csv",
    "ai_endpoint_contract.csv",
    "mcp_tool_catalog.csv",
    "mcp_security_matrix.csv",
    "hosting_decision.csv",
    "resilience_policy.csv",
    "error_catalog.csv",
    "rate_limit_policy.csv",
    "observability_catalog.csv",
    "audit_traceability.csv",
    "security_test_scenarios.csv",
    "integration_readiness.csv",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def validate_outputs(outputs_dir: Path, repo_root: Path) -> list[str]:
    failures: list[str] = []
    for filename in REQUIRED_FILES:
        path = outputs_dir / filename
        if not path.is_file():
            failures.append(f"missing application integration output: {filename}")
        elif not read_csv(path):
            failures.append(f"empty application integration output: {filename}")
    if failures:
        return failures

    for filename in REQUIRED_FILES:
        rows = read_csv(outputs_dir / filename)
        if "evidence_classification" in rows[0]:
            unknown = {row["evidence_classification"] for row in rows} - EVIDENCE_CLASSES
            if unknown:
                failures.append(f"{filename} has unsupported classifications: {sorted(unknown)}")

    api_rows = read_csv(outputs_dir / "api_catalog.csv")
    for row in api_rows:
        if not row["backing_object"]:
            failures.append(f"{row['api_id']} has no backing object")
        if row["auth_required"] != "yes":
            failures.append(f"{row['api_id']} must require authentication")
        if not row["required_role"]:
            failures.append(f"{row['api_id']} has no required role")

    if any("anonymous" in row["required_role"].lower() for row in api_rows):
        failures.append("production API catalog must not use anonymous role")
    if any("arbitrary" in row["backing_object"].lower() for row in api_rows):
        failures.append("API catalog must not expose arbitrary SQL")

    sensitive = read_csv(outputs_dir / "sensitive_field_exposure.csv")
    if not {"API-visible", "masked", "restricted", "never exposed"}.issubset(
        {row["exposure_decision"] for row in sensitive}
    ):
        failures.append(
            "sensitive exposure matrix must cover visible/masked/restricted/never exposed"
        )

    ai_contract = read_csv(outputs_dir / "ai_endpoint_contract.csv")
    if not all(row["authorization_propagation"] == "required" for row in ai_contract):
        failures.append("AI endpoint must require authorization propagation")

    mcp_rows = read_csv(outputs_dir / "mcp_tool_catalog.csv")
    if any(row["read_write"] == "write" for row in mcp_rows):
        failures.append("MCP tools must avoid destructive write tools")
    if not all(row["input_schema_ref"] and row["output_schema_ref"] for row in mcp_rows):
        failures.append("MCP tools must have input and output schemas")

    observability = read_csv(outputs_dir / "observability_catalog.csv")
    observed_api_ids = {row["api_id"] for row in observability}
    missing_observability = {row["api_id"] for row in api_rows} - observed_api_ids
    if missing_observability:
        failures.append(f"endpoints missing observability mapping: {sorted(missing_observability)}")

    resilience = read_csv(outputs_dir / "resilience_policy.csv")
    resilience_api_ids = {row["api_id"] for row in resilience}
    critical = {
        row["api_id"]
        for row in api_rows
        if row["rate_limit_class"] in {"ai_query", "customer_service_lookup"}
    }
    if critical - resilience_api_ids:
        failures.append(
            f"critical endpoints missing resilience policy: {sorted(critical - resilience_api_ids)}"
        )

    security_tests = read_csv(outputs_dir / "security_test_scenarios.csv")
    for required in (
        "anonymous access attempt",
        "cross-customer retrieval attempt",
        "restricted field request",
        "injection-like input",
        "invalid MCP tool input",
        "non-allowlisted database object attempt",
    ):
        if not any(required in row["scenario"] for row in security_tests):
            failures.append(f"security scenarios missing {required}")

    required_assets = [
        "src/api/dab/dab-config.production.json",
        "src/api/contracts/openapi.yaml",
        "src/api/contracts/graphql-examples.graphql",
        "src/api/mcp/tool-catalog.md",
        "src/api/mcp/tool-schemas.json",
        "src/api/container/Dockerfile",
        "src/api/container/.env.example",
        "src/api/kql/application_api_observability.kql",
        "src/azure_sql/api/01_api_views.sql",
        "src/azure_sql/api/02_api_procedures.sql",
        "src/azure_sql/api/security/01_api_roles_permissions.sql",
        "infra/modules/application-integration/container-apps.bicep",
        "reports/application_integration_report.md",
        "docs/application-api-integration.md",
    ]
    missing_assets = [asset for asset in required_assets if not (repo_root / asset).is_file()]
    if missing_assets:
        failures.append(f"missing application integration assets: {missing_assets}")

    dab_config = json.loads(
        (repo_root / "src/api/dab/dab-config.production.json").read_text(encoding="utf-8")
    )
    if dab_config["runtime"]["host"]["authentication"]["provider"] not in {"EntraID", "AzureAD"}:
        failures.append("DAB production config must use Entra ID/Azure AD authentication")
    entities = dab_config.get("entities", {})
    for name, entity in entities.items():
        permissions = entity.get("permissions", [])
        if any(permission.get("role", "").lower() == "anonymous" for permission in permissions):
            failures.append(f"DAB entity {name} must not allow anonymous production access")
        if not permissions:
            failures.append(f"DAB entity {name} has no permissions")

    text_to_scan = "\n".join(
        (repo_root / path).read_text(encoding="utf-8")
        for path in required_assets
        if (repo_root / path).is_file()
    )
    forbidden = ("password=", "AccountKey=", "SharedAccessSignature=", "SECRET = '")
    if any(term in text_to_scan for term in forbidden):
        failures.append("application integration assets contain secret-like material")
    lower_text = text_to_scan.lower()
    arbitrary_sql_controls = (
        "no arbitrary sql",
        "does not expose arbitrary sql",
        "cannot submit arbitrary sql",
    )
    if "arbitrary sql" in lower_text and not any(
        control in lower_text for control in arbitrary_sql_controls
    ):
        failures.append("assets must not expose arbitrary SQL")

    return failures
