from __future__ import annotations

# ruff: noqa: E501
import argparse
from pathlib import Path

from estate_assessment.rules import (
    compatibility_rows,
    dependency_rows,
    inventory_rows,
    migration_complexity,
    migration_wave_plan,
    risk_register,
    target_service_decisions,
    workload_classifications,
    write_csv,
)
from estate_assessment.validation import validate_assessment_outputs

OUTPUT_FILES = {
    "inventory": "database_estate_inventory.csv",
    "dependencies": "estate_dependencies.csv",
    "compatibility": "compatibility_assessment.csv",
    "workloads": "workload_classification.csv",
    "targets": "target_service_decisions.csv",
    "complexity": "migration_complexity.csv",
    "waves": "migration_wave_plan.csv",
    "risks": "modernisation_risk_register.csv",
}


def generate_assessment(outputs_dir: Path, reports_dir: Path) -> dict[str, Path]:
    outputs_dir.mkdir(parents=True, exist_ok=True)
    reports_dir.mkdir(parents=True, exist_ok=True)

    datasets = {
        "inventory": inventory_rows(),
        "dependencies": dependency_rows(),
        "compatibility": compatibility_rows(),
        "workloads": workload_classifications(),
        "targets": target_service_decisions(),
        "complexity": migration_complexity(),
        "waves": migration_wave_plan(),
        "risks": risk_register(),
    }

    written: dict[str, Path] = {}
    for key, rows in datasets.items():
        path = outputs_dir / OUTPUT_FILES[key]
        write_csv(path, rows)
        written[key] = path

    report_path = reports_dir / "estate_assessment_report.md"
    report_path.write_text(_report(datasets), encoding="utf-8")
    written["report"] = report_path

    failures = validate_assessment_outputs(outputs_dir)
    if failures:
        joined = "\n".join(f"- {failure}" for failure in failures)
        raise RuntimeError(f"Assessment output validation failed:\n{joined}")
    return written


def _report(datasets: dict[str, list[dict[str, object]]]) -> str:
    inventory = datasets["inventory"]
    compatibility = datasets["compatibility"]
    targets = datasets["targets"]
    complexity = datasets["complexity"]
    waves = datasets["waves"]
    risks = datasets["risks"]

    high_findings = [row for row in compatibility if row["severity"] == "high"]
    high_complexity = [row for row in complexity if row["complexity_classification"] == "high"]
    high_risks = [row for row in risks if row["risk_rating"] in {"high", "critical"}]

    lines = [
        "# Estate Assessment and Modernisation Decisioning",
        "",
        "Milestone 3 produces a deterministic local assessment of the synthetic Contoso Freight estate. It does not run Microsoft cloud assessment tools, deploy Azure resources, or perform migration.",
        "",
        "## Evidence Boundary",
        "",
        "- Locally measured: derived from repository scripts, contracts, samples, or workload fixtures.",
        "- Derived evidence: inferred from the synthetic estate design and deterministic workload model.",
        "- Synthetic assumption: explicit planning assumption used to make the assessment realistic.",
        "- Requires live estate validation: cannot be proven from local fixtures and must be checked in a real customer environment.",
        "",
        "## Current-State Findings",
        "",
        f"- Source systems assessed: {len(inventory)}.",
        f"- Compatibility findings: {len(compatibility)} total, {len(high_findings)} high severity.",
        f"- High-complexity migrations: {', '.join(row['system_id'] for row in high_complexity) or 'none'}.",
        "- The legacy transport management system is the most constrained workload because of stored procedure coupling, reporting contention, history growth, and unvalidated instance settings.",
        "- Billing and service operations are relational but have cross-source identifier mismatch that must be remediated before integrated migration or analytics.",
        "- File and event feeds are better treated as ingestion and data-quality candidates than as direct database migration units.",
        "",
        "## Workload Segmentation",
        "",
        "| Workload | Category | Evidence |",
        "| --- | --- | --- |",
    ]
    for row in datasets["workloads"]:
        lines.append(f"| {row['workload_id']} | {row['category']} | {row['evidence_class']} |")

    lines.extend(
        [
            "",
            "## Recommended Azure Targets",
            "",
            "| Workload/System | Selected target | Disposition | Rationale |",
            "| --- | --- | --- | --- |",
        ]
    )
    for row in targets:
        lines.append(
            "| "
            f"{row['workload_or_system']} | {row['selected_target']} | "
            f"{row['modernisation_disposition']} | {row['selection_rationale']} |"
        )

    lines.extend(
        [
            "",
            "## Migration Strategy",
            "",
            "- Complete Wave 0 discovery and remediation before moving production workloads.",
            "- Offload low-risk feeds and operational reporting before moving the core OLTP system.",
            "- Replatform PostgreSQL-like billing separately from SQL Server-style transport workloads.",
            "- Move the business-critical transport OLTP workload only after compatibility, identity, HA/DR, and performance baselines are validated.",
            "",
            "## Migration Waves",
            "",
            "| Wave | Included systems | Approach |",
            "| --- | --- | --- |",
        ]
    )
    for row in waves:
        lines.append(
            f"| {row['wave']} - {row['wave_name']} | {row['included_systems']} | "
            f"{row['expected_migration_approach']} |"
        )

    lines.extend(
        [
            "",
            "## Major Risks",
            "",
            "| Risk | Rating | Mitigation |",
            "| --- | --- | --- |",
        ]
    )
    for row in high_risks:
        lines.append(f"| {row['risk_category']} | {row['risk_rating']} | {row['mitigation']} |")

    lines.extend(
        [
            "",
            "## Prerequisites",
            "",
            "- Live estate validation for database size, growth, collation, SQL Agent dependencies, identity model, and production workload telemetry.",
            "- Procedure-level regression tests for shipment create/update behaviour.",
            "- Data classification and access model for customer, billing, case, and operational event data.",
            "- Reconciliation framework for invoice, payment, shipment, and event counts.",
            "- HA/DR and rollback design before business-critical workload movement.",
            "",
            "## Unresolved Questions for a Real Environment",
            "",
            "- What are the actual database sizes, growth rates, query baselines, wait statistics, and peak concurrency?",
            "- Which SQL Agent jobs, linked servers, CLR objects, SSIS packages, or filesystem dependencies exist outside the local source scripts?",
            "- What identities, groups, application credentials, and privileged access paths are currently used?",
            "- What outage windows and contractual RTO/RPO commitments have business approval?",
            "- Which reports are still required, and which can be retired or replaced by curated data products?",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate Contoso Freight estate assessment outputs."
    )
    parser.add_argument("--outputs-dir", type=Path, default=Path("outputs"))
    parser.add_argument("--reports-dir", type=Path, default=Path("reports"))
    args = parser.parse_args()

    written = generate_assessment(args.outputs_dir, args.reports_dir)
    for key in sorted(written):
        print(f"{key}: {written[key]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
