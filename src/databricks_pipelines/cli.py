from __future__ import annotations

# ruff: noqa: E501
import argparse
import csv
from dataclasses import asdict
from pathlib import Path
from typing import Any

from databricks_pipelines.catalog import (
    BRONZE_TABLES,
    CHECKPOINTS,
    DATA_MODEL,
    GOLD_PRODUCTS,
    INGESTION,
    PHYSICAL_LAYOUT,
    QUARANTINE,
    READINESS,
    REPLAY,
    SCD,
    SCHEMA_DRIFT,
    SILVER_TRANSFORMATIONS,
    TRACEABILITY,
)
from databricks_pipelines.validation import validate_outputs

OUTPUTS = {
    "source_ingestion_matrix.csv": INGESTION,
    "bronze_table_catalog.csv": BRONZE_TABLES,
    "silver_transformation_catalog.csv": SILVER_TRANSFORMATIONS,
    "gold_product_catalog.csv": GOLD_PRODUCTS,
    "data_model_catalog.csv": DATA_MODEL,
    "scd_strategy.csv": SCD,
    "schema_drift_matrix.csv": SCHEMA_DRIFT,
    "checkpoint_strategy.csv": CHECKPOINTS,
    "quarantine_rules.csv": QUARANTINE,
    "replay_idempotency_matrix.csv": REPLAY,
    "physical_layout_strategy.csv": PHYSICAL_LAYOUT,
    "pipeline_traceability.csv": TRACEABILITY,
    "pipeline_readiness.csv": READINESS,
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
    report = reports_dir / "databricks_pipelines_report.md"
    report.write_text(_report(), encoding="utf-8")
    written["databricks_pipelines_report.md"] = report
    failures = validate_outputs(outputs_dir, repo_root or Path.cwd())
    if failures:
        joined = "\n".join(f"- {failure}" for failure in failures)
        raise RuntimeError(f"Databricks pipeline validation failed:\n{joined}")
    return written


def _write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def _report() -> str:
    return "\n".join(
        [
            "# Databricks Ingestion and Medallion Processing Report",
            "",
            "Milestone 10 implements a reproducible Databricks data-engineering layer for Contoso Freight. It defines ingestion patterns, Bronze/Silver/Gold processing, Delta Lake modelling, SCD Type 2, schema drift handling, quarantine, replay/idempotency, physical layout strategy, contracts, and deterministic local validation evidence.",
            "",
            "No Azure Databricks runtime, Auto Loader stream, Structured Streaming query, Lakeflow pipeline, OPTIMIZE/VACUUM command, or production schedule was executed by this milestone.",
            "",
            "## Evidence Boundary",
            "",
            "- Locally validated: pure transformation functions, SCD2 behavior, dedupe, quarantine routing, Gold aggregations, evidence generation, and tests.",
            "- Configuration defined: Spark/SQL pipeline assets, Delta table features, Auto Loader options, checkpoint paths, Asset Bundle resource placeholders.",
            "- Simulated: deterministic local change/event fixtures model CDC and streaming anomalies.",
            "- Requires Databricks runtime validation: actual Auto Loader exactly-once file discovery, Structured Streaming offsets/watermarks, Delta MERGE/CDF, schema evolution, liquid clustering, and runtime performance.",
            "",
            "## Medallion Design",
            "",
            "Bronze preserves source fidelity and metadata. Silver performs trustworthy normalization, dedupe, referential checks, and quarantine routing. Gold exposes five representative analytical products with explicit grain and downstream use cases.",
            "",
            "## Deferred Boundaries",
            "",
            "Formal Lakeflow orchestration, data quality expectations framework, monitoring/optimization, AI/search/RAG, API integration, Fabric assets, FinOps, and production assurance remain deferred.",
            "",
        ]
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate Databricks pipeline evidence.")
    parser.add_argument("--outputs-dir", type=Path, default=Path("outputs/databricks_pipelines"))
    parser.add_argument("--reports-dir", type=Path, default=Path("reports"))
    args = parser.parse_args()
    written = generate_outputs(args.outputs_dir, args.reports_dir, Path.cwd())
    for name in sorted(written):
        print(f"{name}: {written[name]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

