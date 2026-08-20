from __future__ import annotations

import csv
from pathlib import Path

from fabric_integration.catalog import EVIDENCE_CLASSES

REQUIRED_FILES = [
    "fabric_boundary_matrix.csv",
    "fabric_data_product_catalog.csv",
    "integration_pattern_decisions.csv",
    "fabric_data_contracts.csv",
    "schema_compatibility_policy.csv",
    "publication_gate.csv",
    "freshness_handoff_matrix.csv",
    "identity_access_matrix.csv",
    "sensitivity_handoff.csv",
    "lineage_handoff.csv",
    "quality_handoff_manifest.csv",
    "failure_responsibility_matrix.csv",
    "cost_duplication_controls.csv",
    "versioning_policy.csv",
    "fabric_integration_readiness.csv",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def validate_outputs(outputs_dir: Path, repo_root: Path) -> list[str]:
    failures: list[str] = []
    for filename in REQUIRED_FILES:
        path = outputs_dir / filename
        if not path.is_file():
            failures.append(f"missing Fabric integration output: {filename}")
        elif not read_csv(path):
            failures.append(f"empty Fabric integration output: {filename}")
    if failures:
        return failures

    for filename in REQUIRED_FILES:
        rows = read_csv(outputs_dir / filename)
        if "evidence_classification" in rows[0]:
            unknown = {row["evidence_classification"] for row in rows} - EVIDENCE_CLASSES
            if unknown:
                failures.append(f"{filename} has unsupported classifications: {sorted(unknown)}")

    products = read_csv(outputs_dir / "fabric_data_product_catalog.csv")
    product_ids = {row["product_id"] for row in products}
    contracts = read_csv(outputs_dir / "fabric_data_contracts.csv")
    contracted = {row["product_id"] for row in contracts}
    if product_ids - contracted:
        failures.append(f"products missing contracts: {sorted(product_ids - contracted)}")

    for filename, field in (
        ("integration_pattern_decisions.csv", "product_id"),
        ("freshness_handoff_matrix.csv", "product_id"),
        ("publication_gate.csv", "product_id"),
        ("sensitivity_handoff.csv", "product_id"),
        ("lineage_handoff.csv", "product_id"),
        ("quality_handoff_manifest.csv", "product_id"),
    ):
        mapped = {row[field] for row in read_csv(outputs_dir / filename)}
        if product_ids - mapped:
            failures.append(f"{filename} missing products: {sorted(product_ids - mapped)}")

    exposes_lower_layers = any(
        "bronze." in row["gold_product"].lower()
        or "silver." in row["gold_product"].lower()
        for row in products
    )
    if exposes_lower_layers:
        failures.append("Fabric-facing product catalog must not expose Bronze/Silver by default")

    boundary = read_csv(outputs_dir / "fabric_boundary_matrix.csv")
    owners = {(row["responsibility"], row["owner"]) for row in boundary}
    if not any(owner == "Azure Data & AI platform" for _resp, owner in owners):
        failures.append("boundary matrix must include Azure owner")
    if not any(owner == "Fabric platform" for _resp, owner in owners):
        failures.append("boundary matrix must include Fabric owner")
    if any(row["owner"] == "ambiguous" for row in boundary):
        failures.append("boundary matrix must not include ambiguous ownership")

    identity = read_csv(outputs_dir / "identity_access_matrix.csv")
    key_or_sas = any(
        "SAS" in row["preferred_auth"]
        or "storage account key" in row["preferred_auth"].lower()
        for row in identity
    )
    if key_or_sas:
        failures.append("identity matrix must not prefer storage keys or SAS")

    versioning = read_csv(outputs_dir / "versioning_policy.csv")
    if not {"backward compatible", "review required", "breaking"}.issubset(
        {row["classification"] for row in versioning}
    ):
        failures.append("versioning policy must classify compatible, review, and breaking changes")

    readiness = read_csv(outputs_dir / "fabric_integration_readiness.csv")
    if not any(row["status"] == "requires Fabric runtime validation" for row in readiness):
        failures.append("readiness must preserve Fabric runtime validation boundary")

    required_assets = [
        "src/fabric_integration/cli.py",
        "src/fabric_integration/catalog.py",
        "src/fabric_integration/model.py",
        "docs/fabric-integration-boundary.md",
        "reports/fabric_integration_report.md",
    ]
    missing_assets = [asset for asset in required_assets if not (repo_root / asset).is_file()]
    if missing_assets:
        failures.append(f"missing Fabric boundary assets: {missing_assets}")

    text_to_scan = "\n".join(
        (repo_root / path).read_text(encoding="utf-8")
        for path in required_assets
        if (repo_root / path).is_file()
    )
    forbidden = ("password=", "AccountKey=", "SharedAccessSignature=", "SECRET = '")
    if any(term in text_to_scan for term in forbidden):
        failures.append("Fabric integration assets contain secret-like material")
    forbidden_fabric_impl = (
        "CREATE LAKEHOUSE",
        "CREATE WAREHOUSE",
        '"semanticModel"',
        ".pbix",
        "pipeline-content.json",
    )
    if any(term in text_to_scan for term in forbidden_fabric_impl):
        failures.append("Fabric implementation artifacts are out of scope")

    return failures
