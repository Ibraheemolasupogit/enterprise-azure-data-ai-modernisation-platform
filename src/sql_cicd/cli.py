from __future__ import annotations

# ruff: noqa: E501
import argparse
import csv
import hashlib
import json
import shutil
import subprocess
from dataclasses import asdict
from pathlib import Path
from typing import Any

from sql_cicd.catalog import (
    DATABASE_TESTS,
    DRIFT_SCENARIOS,
    PERFORMANCE_GATES,
    PROJECT_OBJECTS,
    PROMOTION_MATRIX,
    REFERENCE_DATA,
    RELEASE_READINESS,
    SAFETY_RULES,
    SECURITY_GATES,
    TRACEABILITY,
)
from sql_cicd.validation import validate_outputs

OUTPUTS = {
    "sql_project_inventory.csv": PROJECT_OBJECTS,
    "database_object_traceability.csv": TRACEABILITY,
    "reference_data_manifest.csv": REFERENCE_DATA,
    "deployment_safety_rules.csv": SAFETY_RULES,
    "schema_drift_scenarios.csv": DRIFT_SCENARIOS,
    "environment_promotion_matrix.csv": PROMOTION_MATRIX,
    "database_test_catalog.csv": DATABASE_TESTS,
    "performance_regression_gate.csv": PERFORMANCE_GATES,
    "security_regression_gate.csv": SECURITY_GATES,
    "release_readiness.csv": RELEASE_READINESS,
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
    manifest_path = outputs_dir / "release_manifest.json"
    manifest_path.write_text(
        json.dumps(_release_manifest(outputs_dir), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    written["release_manifest.json"] = manifest_path
    report = reports_dir / "sql_cicd_report.md"
    report.write_text(_report(), encoding="utf-8")
    written["sql_cicd_report.md"] = report
    failures = validate_outputs(outputs_dir, repo_root or Path.cwd())
    if failures:
        joined = "\n".join(f"- {failure}" for failure in failures)
        raise RuntimeError(f"SQL CI/CD validation failed:\n{joined}")
    return written


def _write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def _release_manifest(outputs_dir: Path) -> dict[str, Any]:
    output_files = sorted(OUTPUTS)
    return {
        "database": "legacy_tms",
        "project": "src/azure_sql/database_project/legacy_tms/legacy_tms.sqlproj",
        "dacpac_expected_path": "src/azure_sql/database_project/legacy_tms/bin/Debug/legacy_tms.dacpac",
        "evidence_boundary": "local static evidence; no Azure deployment performed",
        "tooling": {
            "dotnet_available": shutil.which("dotnet") is not None,
            "highest_dotnet_sdk": _highest_dotnet_sdk(),
            "dotnet_sdk_8_or_newer": _dotnet_sdk_supported(),
            "sqlpackage_available": shutil.which("sqlpackage") is not None,
            "build_command": "make build-sql-project",
            "publish_command": "deferred to approved GitHub Actions environment",
        },
        "outputs": output_files,
        "output_hashes": {
            filename: _sha256(outputs_dir / filename)
            for filename in output_files
            if (outputs_dir / filename).is_file()
        },
        "release_gates": [
            "schema build",
            "deployment preview",
            "drift classification",
            "reference data manifest",
            "performance regression gate",
            "security regression gate",
            "environment approval",
        ],
    }


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _highest_dotnet_sdk() -> str:
    dotnet = shutil.which("dotnet")
    if dotnet is None:
        return "not found"
    result = subprocess.run(
        [dotnet, "--list-sdks"],
        check=False,
        capture_output=True,
        text=True,
    )
    versions = [line.split()[0] for line in result.stdout.splitlines() if line.split()]
    return sorted(versions)[-1] if versions else "unknown"


def _dotnet_sdk_supported() -> bool:
    version = _highest_dotnet_sdk()
    if version in {"not found", "unknown"}:
        return False
    parts = version.split(".")
    return bool(parts and parts[0].isdigit() and int(parts[0]) >= 8)


def _report() -> str:
    return "\n".join(
        [
            "# SQL Database Development Lifecycle and CI/CD Report",
            "",
            "Milestone 8 implements database-as-code assets for the `legacy_tms` Azure SQL Managed Instance target. It defines an SDK-style SQL project, deterministic release evidence, reference-data deployment boundaries, drift scenarios, safety rules, regression gates, and GitHub Actions workflows. It does not publish to Azure, execute live sqlpackage deployment actions, or claim production validation.",
            "",
            "## SQL Project",
            "",
            "The SQL project is located at `src/azure_sql/database_project/legacy_tms/legacy_tms.sqlproj` and uses `Microsoft.Build.Sql`. Schema files are split by object so tables, views, procedures, security assets, pre-deployment checks, post-deployment reference data, and tests can be reviewed independently.",
            "",
            "## Build and Dacpac",
            "",
            "`make build-sql-project` runs a real `dotnet build` when the SDK restore toolchain is available. If `dotnet` is absent, the command fails clearly instead of reporting a fake dacpac.",
            "",
            "## Reference Data",
            "",
            "Reference depots and routes are deployed with deterministic natural-key `MERGE` statements. The post-deployment script updates/inserts known reference rows and does not automatically delete unexpected rows.",
            "",
            "## Drift and Safety",
            "",
            "Release controls require deploy preview, drift classification, destructive-change review, role/grant traceability, and environment approval before production promotion. Rollback is bounded to the previous dacpac and database backup/restore point; data migrations remain separate reviewed scripts.",
            "",
            "## Testing and Regression Gates",
            "",
            "Static tests validate project structure, traceability, manifest determinism, reference data, drift scenarios, and safety gates. Performance and security gates connect this milestone to the prior SQL operations and performance evidence without inventing live Azure measurements.",
            "",
        ]
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate SQL CI/CD release evidence.")
    parser.add_argument("--outputs-dir", type=Path, default=Path("outputs/sql_cicd"))
    parser.add_argument("--reports-dir", type=Path, default=Path("reports"))
    args = parser.parse_args()
    written = generate_outputs(args.outputs_dir, args.reports_dir, Path.cwd())
    for name in sorted(written):
        print(f"{name}: {written[name]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
