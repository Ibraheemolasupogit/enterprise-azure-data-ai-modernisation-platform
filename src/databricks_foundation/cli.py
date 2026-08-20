from __future__ import annotations

# ruff: noqa: E501
import argparse
import csv
from dataclasses import asdict
from pathlib import Path
from typing import Any

from databricks_foundation.catalog import (
    ACCESS,
    AUDIT,
    BUNDLE_TARGETS,
    COMPUTE,
    FEDERATION,
    FINE_GRAINED,
    LINEAGE,
    NAMESPACE,
    READINESS,
    RETENTION,
    SHARING,
    STORAGE,
    TAGS,
    WORKSPACES,
)
from databricks_foundation.validation import validate_outputs

OUTPUTS = {
    "workspace_strategy.csv": WORKSPACES,
    "compute_strategy.csv": COMPUTE,
    "unity_catalog_namespace.csv": NAMESPACE,
    "storage_boundary.csv": STORAGE,
    "access_control_matrix.csv": ACCESS,
    "fine_grained_security.csv": FINE_GRAINED,
    "governed_tag_catalog.csv": TAGS,
    "retention_policy.csv": RETENTION,
    "lineage_readiness.csv": LINEAGE,
    "audit_catalog.csv": AUDIT,
    "delta_sharing_matrix.csv": SHARING,
    "federation_decisions.csv": FEDERATION,
    "bundle_target_matrix.csv": BUNDLE_TARGETS,
    "platform_readiness.csv": READINESS,
}


def generate_outputs(
    outputs_dir: Path,
    reports_dir: Path,
    repo_root: Path | None = None,
) -> dict[str, Path]:
    outputs_dir.mkdir(parents=True, exist_ok=True)
    reports_dir.mkdir(parents=True, exist_ok=True)
    written: dict[str, Path] = {}
    for filename, rows in OUTPUTS.items():
        path = outputs_dir / filename
        _write_csv(path, [asdict(row) for row in rows])
        written[filename] = path
    report = reports_dir / "databricks_foundation_report.md"
    report.write_text(_report(), encoding="utf-8")
    written["databricks_foundation_report.md"] = report
    failures = validate_outputs(outputs_dir, repo_root or Path.cwd())
    if failures:
        joined = "\n".join(f"- {failure}" for failure in failures)
        raise RuntimeError(f"Databricks foundation validation failed:\n{joined}")
    return written


def _write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def _report() -> str:
    return "\n".join(
        [
            "# Databricks Platform Foundation and Unity Catalog Report",
            "",
            "Milestone 9 defines an implementation-ready Azure Databricks platform foundation for Contoso Freight. It covers dev/test/prod workspace boundaries, compute selection, Unity Catalog namespace design, storage credentials and external locations, least-privilege access, fine-grained governance, retention, lineage/audit readiness, Delta Sharing, federation boundaries, and Databricks Asset Bundle foundations.",
            "",
            "No Azure Databricks workspace, Unity Catalog object, storage credential, external location, job, pipeline, lineage graph, audit event, or share was deployed or fabricated by this milestone.",
            "",
            "## Evidence Boundary",
            "",
            "- Locally validated: deterministic CSV evidence, documentation, bundle file structure, static SQL/IaC assets, tests.",
            "- Configuration defined: Bicep resources, Unity Catalog DDL, grant model, compute policy intent, retention model.",
            "- Simulated: none required for this milestone.",
            "- Requires Azure validation: workspace creation, metastore assignment, ABAC policy execution, lineage capture, audit logs, system tables, Delta Sharing, federation, and runtime/compute behaviour.",
            "",
            "## Platform Shape",
            "",
            "The model uses one workspace per environment and one catalog per environment: `contoso_freight_dev`, `contoso_freight_test`, and `contoso_freight_prod`. Schemas are consistent across environments: bronze, silver, gold, reference, quarantine, and audit.",
            "",
            "## Compute",
            "",
            "Interactive compute is restricted to development and exploration. Production ingestion and transformation should run through jobs or future pipeline compute under service principals and compute policies. SQL warehouses serve curated Gold objects, while classic compute is exception-only.",
            "",
            "## Governance",
            "",
            "Unity Catalog is the authority for Databricks data-object governance. Managed tables are preferred for Silver and Gold data products; external locations are used for landing, checkpoints, quarantine payloads, and controlled exchange zones. ABAC with governed tags is preferred for consistent row and column enforcement, with table-level filters/masks only as a fallback.",
            "",
        ]
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate Databricks foundation evidence.")
    parser.add_argument("--outputs-dir", type=Path, default=Path("outputs/databricks_foundation"))
    parser.add_argument("--reports-dir", type=Path, default=Path("reports"))
    args = parser.parse_args()
    written = generate_outputs(args.outputs_dir, args.reports_dir, Path.cwd())
    for name in sorted(written):
        print(f"{name}: {written[name]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

