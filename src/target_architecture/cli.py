from __future__ import annotations

# ruff: noqa: E501
import argparse
import csv
from pathlib import Path
from typing import Any

from target_architecture.catalog import (
    ASSUMPTIONS,
    COMPONENTS,
    ENVIRONMENTS,
    RECOVERY_STRATEGIES,
    SECURITY_CONTROLS,
    TRACEABILITY,
    WORKLOAD_TARGETS,
)
from target_architecture.validation import validate_architecture_outputs

OUTPUTS = {
    "target_component_catalog.csv": COMPONENTS,
    "workload_target_matrix.csv": WORKLOAD_TARGETS,
    "security_control_matrix.csv": SECURITY_CONTROLS,
    "recovery_strategy_matrix.csv": RECOVERY_STRATEGIES,
    "environment_matrix.csv": ENVIRONMENTS,
    "assumption_register.csv": ASSUMPTIONS,
    "architecture_traceability.csv": TRACEABILITY,
}


def generate_architecture(outputs_dir: Path, reports_dir: Path) -> dict[str, Path]:
    outputs_dir.mkdir(parents=True, exist_ok=True)
    reports_dir.mkdir(parents=True, exist_ok=True)
    written: dict[str, Path] = {}
    for filename, rows in OUTPUTS.items():
        path = outputs_dir / filename
        _write_csv(path, [dict(row.__dict__) for row in rows])
        written[filename] = path

    report = reports_dir / "target_architecture_report.md"
    report.write_text(_report(), encoding="utf-8")
    written["target_architecture_report.md"] = report

    failures = validate_architecture_outputs(outputs_dir)
    if failures:
        joined = "\n".join(f"- {failure}" for failure in failures)
        raise RuntimeError(f"Architecture validation failed:\n{joined}")
    return written


def _write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def _report() -> str:
    services = sorted({component.azure_service for component in COMPONENTS})
    service_lines = [f"- {service}" for service in services]
    return "\n".join(
        [
            "# Target-State Architecture Report",
            "",
            "Milestone 4 formalises the implementation-ready target architecture for Contoso Freight. It does not deploy Azure resources, implement migration, build Databricks pipelines, or implement AI search/RAG.",
            "",
            "## Target Architecture Planes",
            "",
            "- Operational data plane: Azure SQL Managed Instance for `legacy_tms` and Azure Database for PostgreSQL Flexible Server for `billing_ops`.",
            "- Data engineering / analytical plane: Azure Databricks, ADLS Gen2, Delta Lake, Bronze/Silver/Gold, Unity Catalog, batch, CDC, and streaming design boundaries.",
            "- AI-enabled data plane: future boundary for Azure SQL native AI/vector features, embeddings, hybrid search, Azure OpenAI, RAG, and secure API/MCP integration.",
            "- Control / security / operations plane: Entra ID, managed identities, Key Vault, private networking, Azure Monitor, Log Analytics, CI/CD, IaC, audit, and governance controls.",
            "",
            "## Azure Services",
            "",
            *service_lines,
            "",
            "## Operational Database Decisions",
            "",
            "- Azure SQL Managed Instance remains the initial target for `legacy_tms` because stored procedures, SQL Server compatibility risk, instance-level unknowns, networking constraints, and low downtime tolerance make Azure SQL Database a later optimisation rather than the first migration target.",
            "- The decision would change toward Azure SQL Database if live discovery proves no instance-level dependencies, acceptable procedure compatibility, no cross-database assumptions, and lower operational complexity. It would change toward SQL Server on Azure VM only if hard unsupported dependencies require OS/instance control.",
            "- Azure Database for PostgreSQL Flexible Server is the target for `billing_ops` because the source is PostgreSQL-like and engine conversion to Azure SQL is not currently justified.",
            "",
            "## Databricks and Storage Design",
            "",
            "- Databricks owns batch, CDC/incremental, streaming/event ingestion, data quality, medallion processing, and analytical offload.",
            "- ADLS Gen2 stores landing/raw, bronze, silver, gold, checkpoints, schema metadata, quarantine, and audit/evidence zones.",
            "- Unity Catalog governs lakehouse catalogs, schemas, grants, lineage, and the managed-vs-external table boundary.",
            "- Job compute is preferred for production pipelines; interactive compute remains a development concern. Serverless/classic choices require region, policy, and workload validation.",
            "",
            "## Networking and Identity",
            "",
            "- Production target architecture prefers private data-plane connectivity using VNet segmentation, private endpoints, Private DNS, and restricted administrative paths.",
            "- Portfolio/dev implementation may simplify access while preserving the production architecture decision in documentation and IaC structure.",
            "- Identity is Entra-first with managed identities for workloads, federated CI/CD identity, database groups/users, Databricks service identities, and least-privilege storage/Key Vault access.",
            "",
            "## HA/DR",
            "",
            "- Critical transport OLTP assumes RTO 60 minutes and RPO 15 minutes.",
            "- Billing/service assumes RTO 240 minutes and RPO 60 minutes.",
            "- Analytical processing assumes restartable jobs, replayable sources, and RTO/RPO tiers aligned to data freshness requirements.",
            "- DR is not tested in Milestone 4.",
            "",
            "## Assumptions Requiring Live Validation",
            "",
            "- SQL MI compute/storage sizing, collation, SQL Agent dependencies, and production workload telemetry.",
            "- PostgreSQL connection profile, write pattern, month-end billing workload, storage growth, and HA requirements.",
            "- Corporate DNS, firewall, routing, private endpoint, and administrative-access constraints.",
            "- Databricks compute mode, Lakeflow fit, workload concurrency, and serverless availability.",
            "- Regulatory need for customer-managed keys and exact audit/log retention.",
            "",
        ]
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate target architecture outputs.")
    parser.add_argument("--outputs-dir", type=Path, default=Path("outputs/architecture"))
    parser.add_argument("--reports-dir", type=Path, default=Path("reports"))
    args = parser.parse_args()
    written = generate_architecture(args.outputs_dir, args.reports_dir)
    for name in sorted(written):
        print(f"{name}: {written[name]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
