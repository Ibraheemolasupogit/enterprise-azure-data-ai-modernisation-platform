from __future__ import annotations

import csv
from pathlib import Path

REQUIRED_FILES = [
    "source_ingestion_matrix.csv",
    "bronze_table_catalog.csv",
    "silver_transformation_catalog.csv",
    "gold_product_catalog.csv",
    "data_model_catalog.csv",
    "scd_strategy.csv",
    "schema_drift_matrix.csv",
    "checkpoint_strategy.csv",
    "quarantine_rules.csv",
    "replay_idempotency_matrix.csv",
    "physical_layout_strategy.csv",
    "pipeline_traceability.csv",
    "pipeline_readiness.csv",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def validate_outputs(outputs_dir: Path, repo_root: Path | None = None) -> list[str]:
    failures: list[str] = []
    for filename in REQUIRED_FILES:
        path = outputs_dir / filename
        if not path.is_file():
            failures.append(f"missing Databricks pipeline output: {filename}")
        elif not read_csv(path):
            failures.append(f"empty Databricks pipeline output: {filename}")
    if failures:
        return failures

    ingestion = read_csv(outputs_dir / "source_ingestion_matrix.csv")
    bronze = read_csv(outputs_dir / "bronze_table_catalog.csv")
    silver = read_csv(outputs_dir / "silver_transformation_catalog.csv")
    gold = read_csv(outputs_dir / "gold_product_catalog.csv")
    model = read_csv(outputs_dir / "data_model_catalog.csv")
    scd = read_csv(outputs_dir / "scd_strategy.csv")
    drift = read_csv(outputs_dir / "schema_drift_matrix.csv")
    checkpoints = read_csv(outputs_dir / "checkpoint_strategy.csv")
    quarantine = read_csv(outputs_dir / "quarantine_rules.csv")
    replay = read_csv(outputs_dir / "replay_idempotency_matrix.csv")
    layout = read_csv(outputs_dir / "physical_layout_strategy.csv")
    traceability = read_csv(outputs_dir / "pipeline_traceability.csv")
    readiness = read_csv(outputs_dir / "pipeline_readiness.csv")

    required_sources = {
        "legacy_tms",
        "billing_ops",
        "depot_reference_feed",
        "carrier_updates",
        "customer_service_export",
        "shipment_operational_events",
    }
    if required_sources - {row["source"] for row in ingestion}:
        failures.append("every source domain requires an ingestion pattern")
    if any(not row["bronze_target"].startswith("bronze.") for row in ingestion):
        failures.append("every ingestion row must map to a Bronze target")
    if any(not row["checkpoint_requirement"] for row in ingestion):
        failures.append("checkpoint requirements must be explicit")

    bronze_tables = {row["table_name"] for row in bronze}
    if {row["bronze_target"] for row in ingestion} - bronze_tables:
        failures.append("ingestion matrix references missing Bronze tables")
    if not all("_ingested_at_utc" in row["required_metadata"] for row in bronze):
        failures.append("Bronze tables must include ingestion timestamp metadata")

    if not all(row["bronze_sources"] for row in silver):
        failures.append("every Silver transformation requires source traceability")
    if not all(row["quarantine_output"].startswith("quarantine.") for row in silver):
        failures.append("every Silver transformation requires quarantine output")
    if not all(row["grain"] for row in gold):
        failures.append("every Gold product requires a grain")

    scd_text = " ".join(row["strategy"] for row in scd)
    for required in ("customer_id", "customer_sk", "effective_start_utc", "effective_end_utc"):
        if required not in scd_text:
            failures.append(f"SCD strategy missing {required}")
    if not any(row["object_role"] == "fact" for row in model):
        failures.append("data model requires facts")
    if not any(row["object_role"] == "dimension" for row in model):
        failures.append("data model requires dimensions")
    if not any(row["area"] == "changed type" for row in drift):
        failures.append("schema drift matrix must include changed type behavior")
    if not any(row["area"] == "schema location" for row in checkpoints):
        failures.append("checkpoint strategy must include Auto Loader schema location")
    if not quarantine:
        failures.append("quarantine rules are required")
    if not any(row["area"] == "event replay" for row in replay):
        failures.append("replay matrix must include event replay")
    if not any("liquid clustering" in row["strategy"] for row in layout):
        failures.append("physical layout should evaluate liquid clustering")
    if {row["source"] for row in traceability} != required_sources:
        failures.append("traceability must cover every source exactly once")
    if any("deployed" in row["rationale"].lower() for row in readiness):
        failures.append("readiness must not claim deployed runtime resources")

    if repo_root is not None:
        for required_path in (
            "src/databricks/pipelines/batch_ingestion.py",
            "src/databricks/pipelines/autoloader_carrier_updates.py",
            "src/databricks/pipelines/streaming_shipment_events.py",
            "src/databricks/transformations/silver_transformations.py",
            "src/databricks/models/gold_products.sql",
            "data/contracts/databricks/silver_shipments.schema.json",
            "data/contracts/databricks/gold_delivery_delay_metrics.schema.json",
        ):
            if not (repo_root / required_path).is_file():
                failures.append(f"missing Databricks pipeline asset: {required_path}")

    return failures

