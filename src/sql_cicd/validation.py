from __future__ import annotations

import csv
import json
from pathlib import Path

REQUIRED_FILES = [
    "sql_project_inventory.csv",
    "database_object_traceability.csv",
    "reference_data_manifest.csv",
    "deployment_safety_rules.csv",
    "schema_drift_scenarios.csv",
    "environment_promotion_matrix.csv",
    "database_test_catalog.csv",
    "performance_regression_gate.csv",
    "security_regression_gate.csv",
    "release_readiness.csv",
    "release_manifest.json",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def validate_outputs(outputs_dir: Path, project_root: Path | None = None) -> list[str]:
    failures: list[str] = []
    for filename in REQUIRED_FILES:
        path = outputs_dir / filename
        if not path.is_file():
            failures.append(f"missing SQL CI/CD output: {filename}")
        elif filename.endswith(".csv") and not read_csv(path):
            failures.append(f"empty SQL CI/CD output: {filename}")
    if failures:
        return failures

    inventory = read_csv(outputs_dir / "sql_project_inventory.csv")
    traceability = read_csv(outputs_dir / "database_object_traceability.csv")
    reference_data = read_csv(outputs_dir / "reference_data_manifest.csv")
    safety_rules = read_csv(outputs_dir / "deployment_safety_rules.csv")
    drift = read_csv(outputs_dir / "schema_drift_scenarios.csv")
    promotion = read_csv(outputs_dir / "environment_promotion_matrix.csv")
    tests = read_csv(outputs_dir / "database_test_catalog.csv")
    performance = read_csv(outputs_dir / "performance_regression_gate.csv")
    security = read_csv(outputs_dir / "security_regression_gate.csv")
    readiness = read_csv(outputs_dir / "release_readiness.csv")
    manifest = json.loads((outputs_dir / "release_manifest.json").read_text(encoding="utf-8"))

    object_names = {row["object_name"] for row in inventory}
    for required in (
        "CustomerAccount",
        "Shipment",
        "ShipmentEventHistory",
        "usp_CreateShipment",
        "usp_UpdateShipmentStatus",
        "Depot and Route seed",
    ):
        if required not in object_names:
            failures.append(f"SQL project inventory missing {required}")

    if not any(
        "IX_Shipment_Route_Status_CreatedAt" in row["database_object"]
        for row in traceability
    ):
        failures.append("traceability must include the performance-critical route/status index")
    if not all(int(row["row_count"]) > 0 for row in reference_data):
        failures.append("reference data manifest requires positive row counts")
    if not all("MERGE" in row["deployment_method"] for row in reference_data):
        failures.append("reference data must be deployed through idempotent MERGE")
    if not any(row["failure_action"] == "stop release" for row in safety_rules):
        failures.append("safety rules must include stop-release actions")
    if not any(row["drift_type"] == "manual hotfix" for row in drift):
        failures.append("drift scenarios must include manual hotfix drift")
    if "prod" not in {row["environment"] for row in promotion}:
        failures.append("promotion matrix must include prod")
    if not any(row["required_for_release"] == "tooling dependent" for row in tests):
        failures.append("test catalog must distinguish optional dacpac build tooling")
    if not any(row["release_decision"] == "block promotion" for row in performance):
        failures.append("performance gate must block unsafe promotion")
    if not any(row["area"] == "secret handling" for row in security):
        failures.append("security gate must include secret handling")
    if not any(row["status"] == "tooling dependent" for row in readiness):
        failures.append("release readiness must mark build tooling honestly")

    if manifest.get("database") != "legacy_tms":
        failures.append("release manifest database must be legacy_tms")
    if manifest.get("evidence_boundary") != "local static evidence; no Azure deployment performed":
        failures.append("release manifest must state no Azure deployment was performed")
    if sorted(manifest.get("outputs", [])) != sorted(REQUIRED_FILES[:-1]):
        failures.append("release manifest output inventory is incomplete")

    if project_root is not None:
        missing_assets = [
            row["source_path"]
            for row in inventory
            if not (project_root / row["source_path"]).is_file()
        ]
        if missing_assets:
            failures.append(f"inventory references missing project assets: {missing_assets}")

    return failures
