from __future__ import annotations

# ruff: noqa: E501
import argparse
import csv
from dataclasses import asdict
from pathlib import Path
from typing import Any

from fabric_integration.catalog import CONTRACT_FIELDS, PATTERN_DECISIONS, PRODUCTS
from fabric_integration.validation import validate_outputs


def generate_outputs(outputs_dir: Path, reports_dir: Path, repo_root: Path | None = None) -> dict[str, Path]:
    outputs_dir.mkdir(parents=True, exist_ok=True)
    reports_dir.mkdir(parents=True, exist_ok=True)
    outputs = {
        "fabric_boundary_matrix.csv": _boundary_matrix(),
        "fabric_data_product_catalog.csv": [asdict(row) | {"evidence_classification": "configuration defined"} for row in PRODUCTS],
        "integration_pattern_decisions.csv": [asdict(row) | {"evidence_classification": "configuration defined"} for row in PATTERN_DECISIONS],
        "fabric_data_contracts.csv": _contracts(),
        "schema_compatibility_policy.csv": _schema_policy(),
        "publication_gate.csv": _publication_gate(),
        "freshness_handoff_matrix.csv": _freshness_handoff(),
        "identity_access_matrix.csv": _identity_access(),
        "sensitivity_handoff.csv": _sensitivity_handoff(),
        "lineage_handoff.csv": _lineage_handoff(),
        "quality_handoff_manifest.csv": _quality_manifest(),
        "failure_responsibility_matrix.csv": _failure_matrix(),
        "cost_duplication_controls.csv": _cost_controls(),
        "versioning_policy.csv": _versioning_policy(),
        "fabric_integration_readiness.csv": _readiness(),
    }
    written: dict[str, Path] = {}
    for filename, rows in outputs.items():
        path = outputs_dir / filename
        _write_csv(path, rows)
        written[filename] = path
    report = reports_dir / "fabric_integration_report.md"
    report.write_text(_report(), encoding="utf-8")
    written["fabric_integration_report.md"] = report
    failures = validate_outputs(outputs_dir, repo_root or Path.cwd())
    if failures:
        joined = "\n".join(f"- {failure}" for failure in failures)
        raise RuntimeError(f"Fabric integration validation failed:\n{joined}")
    return written


def _write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def _boundary_matrix() -> list[dict[str, str]]:
    rows = [
        ("operational database sources", "Azure Data & AI platform", "source of truth and operational change capture"),
        ("Azure SQL", "Azure Data & AI platform", "schema, operations, performance, CI/CD, AI SQL boundary"),
        ("Databricks Bronze/Silver/Gold engineering", "Azure Data & AI platform", "ingestion, transformations, data quality, and Gold products"),
        ("Gold contracts and publication readiness", "Azure Data & AI platform", "contract-first handoff and quality/freshness status"),
        ("API and AI services", "Azure Data & AI platform", "REST/GraphQL/MCP/API and SQL AI service boundary"),
        ("Fabric ingestion/shortcut/mirroring decisions", "Fabric platform", "downstream consumption pattern after handoff"),
        ("OneLake/Lakehouse/Warehouse", "Fabric platform", "Fabric-side data estate implementation"),
        ("semantic models and Power BI", "Fabric platform", "downstream modelling, RLS/OLS, reports, and adoption"),
        ("Fabric monitoring and CI/CD", "Fabric platform", "Fabric-side operations and release process"),
        ("data contracts", "Shared", "producer defines; consumer validates and negotiates changes"),
        ("identity groups and sensitivity metadata", "Shared", "Entra group alignment and label/control handoff"),
        ("SLA/freshness and incident coordination", "Shared", "producer and consumer responsibilities remain separate"),
    ]
    return [
        {
            "responsibility": responsibility,
            "owner": owner,
            "boundary": boundary,
            "evidence_classification": "configuration defined",
        }
        for responsibility, owner, boundary in rows
    ]


def _contracts() -> list[dict[str, str]]:
    product_by_name = {product.gold_product: product.product_id for product in PRODUCTS}
    return [
        asdict(field)
        | {
            "product_id": product_by_name[field.dataset],
            "evidence_classification": "locally validated",
        }
        for field in CONTRACT_FIELDS
    ]


def _schema_policy() -> list[dict[str, str]]:
    rows = [
        ("add nullable column", "backward compatible", "minor version increment; notify consumers in release notes"),
        ("add non-nullable column", "review required", "producer/consumer review and default/backfill strategy"),
        ("breaking rename", "breaking", "major version increment and migration period"),
        ("removed field", "breaking", "major version increment and deprecation notice"),
        ("changed data type", "breaking", "major version increment unless widening is proven compatible"),
        ("changed grain", "breaking", "new product version or new product id"),
        ("changed key semantics", "breaking", "new contract and consumer migration plan"),
    ]
    return [
        {
            "change_type": change,
            "classification": classification,
            "notification_versioning": action,
            "evidence_classification": "configuration defined",
        }
        for change, classification, action in rows
    ]


def _publication_gate() -> list[dict[str, str]]:
    return [
        {
            "product_id": product.product_id,
            "gold_product": product.gold_product,
            "required_conditions": "upstream pipeline succeeded; critical quality checks passed; schema contract valid; freshness within boundary; sensitivity metadata present; publication status ready",
            "uses_existing_evidence": "outputs/databricks_orchestration/quality_results.csv; outputs/databricks_orchestration/orchestration_readiness.csv",
            "publish_decision": "ready only when all critical gates pass",
            "evidence_classification": "configuration defined",
        }
        for product in PRODUCTS
    ]


def _freshness_handoff() -> list[dict[str, str]]:
    return [
        {
            "product_id": product.product_id,
            "gold_product": product.gold_product,
            "producer_completion_target": product.freshness,
            "handoff_freshness": "after producer Gold publication and manifest emission",
            "fabric_responsibility_boundary": "Fabric owns downstream shortcut/ingestion/model refresh after handoff",
            "breach_owner": "Azure producer until manifest handoff; Fabric consumer after downstream consumption starts",
            "evidence_classification": "configuration defined",
        }
        for product in PRODUCTS
    ]


def _identity_access() -> list[dict[str, str]]:
    rows = [
        ("platform publisher identity", "Azure managed identity or service principal", "write publication manifest and expose read path metadata", "Gold publication container/path only"),
        ("Fabric ingestion/shortcut identity", "Entra service principal or managed identity where supported", "read published Gold product paths", "read-only to product path; no Bronze/Silver"),
        ("analytics consumer groups", "Entra groups", "consume Fabric-side models and shortcuts", "Fabric-side RLS/OLS and workspace roles"),
        ("auditor/security group", "Entra group", "read contract, manifest, lineage, and audit metadata", "metadata-only by default"),
    ]
    return [
        {
            "identity": identity,
            "preferred_auth": auth,
            "allowed_access": allowed,
            "storage_boundary": boundary,
            "evidence_classification": "configuration defined",
        }
        for identity, auth, allowed, boundary in rows
    ]


def _sensitivity_handoff() -> list[dict[str, str]]:
    return [
        {
            "product_id": product.product_id,
            "gold_product": product.gold_product,
            "azure_sensitivity": product.sensitivity,
            "fabric_enforcement_expectation": "Fabric must enforce downstream workspace permissions, RLS/OLS where applicable, endorsement/labelling, and audit controls",
            "automatic_propagation_claim": "not claimed; metadata handoff requires Fabric validation",
            "evidence_classification": "configuration defined",
        }
        for product in PRODUCTS
    ]


def _lineage_handoff() -> list[dict[str, str]]:
    return [
        {
            "product_id": product.product_id,
            "source": product.source,
            "azure_lineage": f"{product.source} -> {product.gold_product}",
            "handoff_identifier": f"{product.product_id}:{product.schema_version}",
            "fabric_lineage_start": "Fabric shortcut/ingestion item created by Fabric platform",
            "cross_platform_lineage_claim": "handoff identifiers only; no fabricated end-to-end graph",
            "evidence_classification": "configuration defined",
        }
        for product in PRODUCTS
    ]


def _quality_manifest() -> list[dict[str, str]]:
    return [
        {
            "product_id": product.product_id,
            "publication_timestamp": "<runtime-publication-timestamp>",
            "schema_version": product.schema_version,
            "record_count": "<runtime-record-count>",
            "quality_status": product.quality_status,
            "freshness_status": "<runtime-freshness-status>",
            "critical_rule_failures": "0 required for publication",
            "source_processing_id": "<runtime-processing-id>",
            "evidence_classification": "configuration defined",
        }
        for product in PRODUCTS
    ]


def _failure_matrix() -> list[dict[str, str]]:
    rows = [
        ("Gold product unavailable", "Azure Data & AI platform", "stop publication; repair or rerun Gold job", "hold Fabric refresh/consumption", "Azure data platform incident"),
        ("freshness breach", "Shared", "publish breach status and expected recovery", "surface consumer SLA impact", "joint incident if downstream users affected"),
        ("schema incompatibility", "Shared", "block publish or publish new version", "validate consumer impact and migrate", "contract review board"),
        ("shortcut/storage access failure", "Fabric platform", "confirm Azure access boundary is healthy", "repair Fabric connection/shortcut identity", "Fabric platform operations"),
        ("Fabric consumer uses stale version", "Fabric platform", "keep deprecated version lifecycle metadata current", "migrate consumer to active version", "Fabric adoption/support"),
        ("Azure-side data quality failure", "Azure Data & AI platform", "block publication and remediate upstream", "consume last valid version if policy allows", "Azure data quality owner"),
        ("identity/RBAC failure", "Shared", "validate Azure RBAC/ACL and group membership", "validate Fabric workspace/connection permissions", "identity/security teams"),
        ("downstream Fabric processing failure", "Fabric platform", "no producer action unless contract defect found", "repair Fabric pipeline/model/report", "Fabric operations"),
    ]
    return [
        {
            "failure_scenario": scenario,
            "owner": owner,
            "producer_action": producer,
            "consumer_action": consumer,
            "escalation": escalation,
            "recovery_boundary": "producer/consumer boundary remains explicit",
            "evidence_classification": "configuration defined",
        }
        for scenario, owner, producer, consumer, escalation in rows
    ]


def _cost_controls() -> list[dict[str, str]]:
    rows = [
        ("prefer shortcut/no-copy", "minimize duplicate storage and avoid repeated transformations when supported"),
        ("copy only by exception", "use batch copy for finance snapshots or retention needs with lifecycle approval"),
        ("avoid Bronze/Silver exposure", "prevent duplicate transformation ownership and unnecessary data movement"),
        ("retain one authoritative Gold producer", "Fabric consumes; it does not recompute producer-owned Gold logic"),
        ("review egress and region alignment", "avoid avoidable cross-region/cross-cloud movement"),
        ("version lifecycle", "do not retain indefinite duplicate product versions without deprecation policy"),
    ]
    return [
        {
            "control": control,
            "purpose": purpose,
            "evidence_classification": "configuration defined",
        }
        for control, purpose in rows
    ]


def _versioning_policy() -> list[dict[str, str]]:
    rows = [
        ("active version", "backward compatible", "current semantic version receives compatible additive changes"),
        ("deprecated version", "review required", "time-bound support while consumers migrate"),
        ("breaking change", "breaking", "major version or new product id; migration period required"),
        ("removed version", "breaking", "only after lifecycle approval and consumer notification"),
    ]
    return [
        {
            "version_state": state,
            "classification": classification,
            "policy": policy,
            "evidence_classification": "configuration defined",
        }
        for state, classification, policy in rows
    ]


def _readiness() -> list[dict[str, str]]:
    return [
        {"capability": "Fabric-facing product catalog", "status": "locally validated", "evidence": "fabric_data_product_catalog.csv and tests"},
        {"capability": "contract-first handoff", "status": "locally validated", "evidence": "fabric_data_contracts.csv"},
        {"capability": "publication gate and quality manifest", "status": "configuration defined", "evidence": "publication_gate.csv; quality_handoff_manifest.csv"},
        {"capability": "identity/storage/sensitivity handoff", "status": "configuration defined", "evidence": "identity_access_matrix.csv; sensitivity_handoff.csv"},
        {"capability": "OneLake shortcut/interoperability pattern", "status": "requires Fabric runtime validation", "evidence": "integration_pattern_decisions.csv"},
        {"capability": "Fabric downstream implementation", "status": "deferred to Fabric repository", "evidence": "no Fabric resources implemented here"},
    ]


def _report() -> str:
    return "\n".join(
        [
            "# Microsoft Fabric Downstream Integration Boundary Report",
            "",
            "Milestone 15 defines only the downstream integration contract between this Azure Data & AI platform and Microsoft Fabric. It does not create Fabric workspaces, Lakehouses, Warehouses, semantic models, Power BI assets, Fabric pipelines, notebooks, Real-Time Intelligence assets, or Fabric deployment pipelines.",
            "",
            "The recommended boundary is Azure Databricks governed Gold Delta products published through an ADLS/Delta boundary, then consumed by Fabric through OneLake shortcuts or a supported interoperability pattern where runtime validation confirms suitability. Controlled batch copy is retained as an exception for finance snapshot or retention requirements.",
            "",
            "Azure owns operational sources, Azure SQL, Databricks ingestion and Gold production, data quality, lineage to Gold, contracts, and publication readiness. Fabric owns downstream ingestion/shortcut choices, OneLake/Lakehouse/Warehouse implementation, semantic models, Power BI, Fabric-side RLS/OLS, monitoring, governance, CI/CD, and adoption.",
            "",
        ]
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate Fabric integration boundary evidence.")
    parser.add_argument("--outputs-dir", type=Path, default=Path("outputs/fabric_integration"))
    parser.add_argument("--reports-dir", type=Path, default=Path("reports"))
    args = parser.parse_args()
    written = generate_outputs(args.outputs_dir, args.reports_dir, Path.cwd())
    for name in sorted(written):
        print(f"{name}: {written[name]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
