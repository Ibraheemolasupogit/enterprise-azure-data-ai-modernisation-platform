from __future__ import annotations

import csv
import json
from pathlib import Path

CLASSES = {
    "locally validated",
    "configuration defined",
    "simulated",
    "requires Azure validation",
    "requires Databricks validation",
    "requires Fabric validation",
    "blocked",
    "requires application runtime validation",
}

REQUIRED_FILES = [
    "capability_inventory.csv",
    "architecture_traceability.csv",
    "platform_ownership_matrix.csv",
    "security_assurance_matrix.csv",
    "identity_assurance.csv",
    "data_product_assurance.csv",
    "governance_traceability.csv",
    "resilience_assurance.csv",
    "failure_mode_matrix.csv",
    "observability_assurance.csv",
    "finops_assurance.csv",
    "ai_assurance.csv",
    "api_assurance.csv",
    "cicd_assurance.csv",
    "implementation_truth_matrix.csv",
    "production_gap_register.csv",
    "final_risk_register.csv",
    "runbook_catalog.csv",
    "release_readiness.csv",
    "release_manifest.json",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def validate_outputs(outputs_dir: Path, repo_root: Path) -> list[str]:
    failures: list[str] = []
    for filename in REQUIRED_FILES:
        path = outputs_dir / filename
        if not path.is_file():
            failures.append(f"missing final assurance output: {filename}")
        elif filename.endswith(".csv") and not read_csv(path):
            failures.append(f"empty final assurance output: {filename}")
    if failures:
        return failures

    for filename in REQUIRED_FILES:
        if not filename.endswith(".csv"):
            continue
        rows = read_csv(outputs_dir / filename)
        class_fields = [field for field in rows[0] if "class" in field or "status" in field]
        for field in class_fields:
            values = {row[field] for row in rows if row[field]}
            suspicious = {value for value in values if "validated" in value or "requires" in value}
            allowed_values = {
                "implemented locally",
                "configuration defined",
                "PASS",
                "CONDITIONAL",
                "BLOCKED",
            }
            unknown = suspicious - CLASSES - allowed_values
            if unknown:
                failures.append(
                    f"{filename}:{field} has unsupported classifications: {sorted(unknown)}"
                )

    capabilities = read_csv(outputs_dir / "capability_inventory.csv")
    domains = {row["domain"] for row in capabilities}
    for required in (
        "Azure SQL",
        "Databricks",
        "AI-enabled SQL",
        "API integration",
        "Fabric boundary",
    ):
        if required not in domains:
            failures.append(f"capability inventory missing {required}")

    ownership = read_csv(outputs_dir / "platform_ownership_matrix.csv")
    if any(row["owner"] == "ambiguous" for row in ownership):
        failures.append("ownership matrix must not contain ambiguous owners")

    data_products = read_csv(outputs_dir / "data_product_assurance.csv")
    if any(not row["gold_or_serving_product"] for row in data_products):
        failures.append("data products must have Gold or serving product mapping")
    if not any(row["product"] == "AI grounding corpus" for row in data_products):
        failures.append("data product assurance must include AI grounding corpus")

    runbooks = read_csv(outputs_dir / "runbook_catalog.csv")
    failure_modes = read_csv(outputs_dir / "failure_mode_matrix.csv")
    missing_runbooks = {
        row["runbook"]
        for row in failure_modes
        if row["runbook"] and not (repo_root / row["runbook"]).is_file()
    }
    catalog_paths = {row["runbook_path"] for row in runbooks}
    if missing_runbooks - catalog_paths:
        failures.append(
            f"failure modes reference missing runbooks: {sorted(missing_runbooks - catalog_paths)}"
        )

    readiness = read_csv(outputs_dir / "release_readiness.csv")
    if not {"PASS", "CONDITIONAL"}.issuperset({row["gate_status"] for row in readiness}):
        failures.append("release gates may only be PASS or CONDITIONAL locally")
    if not any(row["gate_status"] == "CONDITIONAL" for row in readiness):
        failures.append("release readiness must be conditional where cloud validation remains")

    truth = read_csv(outputs_dir / "implementation_truth_matrix.csv")
    required_truth = {
        "Implemented locally",
        "Configuration defined",
        "Simulated",
        "Requires Azure validation",
        "Requires Databricks validation",
        "Requires Fabric validation",
        "Deferred/blocked",
    }
    if required_truth - {row["truth_category"] for row in truth}:
        failures.append("truth matrix missing required categories")

    gaps = read_csv(outputs_dir / "production_gap_register.csv")
    if not any("Azure OpenAI" in row["gap"] for row in gaps):
        failures.append("gap register must include Azure OpenAI validation")
    if not any("Fabric shortcut" in row["gap"] for row in gaps):
        failures.append("gap register must include Fabric shortcut validation")

    manifest = json.loads((outputs_dir / "release_manifest.json").read_text(encoding="utf-8"))
    if manifest.get("repository") != "enterprise-azure-data-ai-modernisation-platform":
        failures.append("release manifest repository mismatch")
    if not manifest.get("production_validation_gaps"):
        failures.append("release manifest must include production validation gaps")

    required_assets = [
        "docs/portfolio-release.md",
        "reports/final_assurance_report.md",
        "scripts/check_no_secrets.py",
        "scripts/check_generated_outputs.py",
    ]
    missing_assets = [asset for asset in required_assets if not (repo_root / asset).is_file()]
    if missing_assets:
        failures.append(f"missing final assurance assets: {missing_assets}")

    return failures
