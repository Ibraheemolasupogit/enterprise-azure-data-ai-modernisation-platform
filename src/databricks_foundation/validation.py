from __future__ import annotations

import csv
from pathlib import Path

REQUIRED_FILES = [
    "workspace_strategy.csv",
    "compute_strategy.csv",
    "unity_catalog_namespace.csv",
    "storage_boundary.csv",
    "access_control_matrix.csv",
    "fine_grained_security.csv",
    "governed_tag_catalog.csv",
    "retention_policy.csv",
    "lineage_readiness.csv",
    "audit_catalog.csv",
    "delta_sharing_matrix.csv",
    "federation_decisions.csv",
    "bundle_target_matrix.csv",
    "platform_readiness.csv",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def validate_outputs(outputs_dir: Path, repo_root: Path | None = None) -> list[str]:
    failures: list[str] = []
    for filename in REQUIRED_FILES:
        path = outputs_dir / filename
        if not path.is_file():
            failures.append(f"missing Databricks foundation output: {filename}")
        elif not read_csv(path):
            failures.append(f"empty Databricks foundation output: {filename}")
    if failures:
        return failures

    workspaces = read_csv(outputs_dir / "workspace_strategy.csv")
    compute = read_csv(outputs_dir / "compute_strategy.csv")
    namespace = read_csv(outputs_dir / "unity_catalog_namespace.csv")
    storage = read_csv(outputs_dir / "storage_boundary.csv")
    access = read_csv(outputs_dir / "access_control_matrix.csv")
    fine_grained = read_csv(outputs_dir / "fine_grained_security.csv")
    tags = read_csv(outputs_dir / "governed_tag_catalog.csv")
    retention = read_csv(outputs_dir / "retention_policy.csv")
    lineage = read_csv(outputs_dir / "lineage_readiness.csv")
    audit = read_csv(outputs_dir / "audit_catalog.csv")
    sharing = read_csv(outputs_dir / "delta_sharing_matrix.csv")
    federation = read_csv(outputs_dir / "federation_decisions.csv")
    bundle = read_csv(outputs_dir / "bundle_target_matrix.csv")
    readiness = read_csv(outputs_dir / "platform_readiness.csv")

    envs = {"dev", "test", "prod"}
    if {row["environment"] for row in workspaces} != envs:
        failures.append("workspace strategy must cover dev, test, and prod")
    if {row["target"] for row in bundle} != envs:
        failures.append("bundle targets must cover dev, test, and prod")
    for env in envs:
        catalog = f"contoso_freight_{env}"
        schemas = {
            row["schema_name"]
            for row in namespace
            if row["catalog"] == catalog and row["object_type"] == "schema"
        }
        if {"bronze", "silver", "gold", "reference", "quarantine", "audit"} - schemas:
            failures.append(f"{catalog} missing required schemas")

    required_compute = {
        "interactive engineering",
        "batch ingestion job",
        "event ingestion",
        "SQL serving",
        "future Delta Live Tables/Lakeflow pipeline",
    }
    if required_compute - {row["workload_class"] for row in compute}:
        failures.append("compute strategy missing required workload classes")
    if any("benchmark" in row["cost_consideration"].lower() for row in compute):
        failures.append("compute strategy must not fabricate benchmarks")

    storage_ids = {row["location_id"] for row in storage}
    if len(storage_ids) != len(storage):
        failures.append("storage boundary contains duplicate location ids")
    if any(
        "key" in row["access_method"].lower() or "sas" in row["access_method"].lower()
        for row in storage
    ):
        failures.append("storage access must not use keys or SAS tokens")

    if not any(row["principal_type"] == "service principal" for row in access):
        failures.append("access model must include service principals")
    if any(row["privileges"] == "ALL PRIVILEGES" for row in access):
        failures.append("least privilege model must not grant ALL PRIVILEGES")

    if not any(row["control_type"] == "column mask" for row in fine_grained):
        failures.append("fine-grained controls must include column masking")
    if not any(row["control_type"] == "row filter" for row in fine_grained):
        failures.append("fine-grained controls must include row filtering")
    if not any(row["tag_name"] == "pii" for row in tags):
        failures.append("governed tags must include pii")
    if not all(row["policy_use"] for row in tags):
        failures.append("governed tags require policy usage")

    retention_zones = {row["dataset_zone"] for row in retention}
    if {"bronze", "silver", "gold", "reference", "quarantine", "audit"} - retention_zones:
        failures.append("retention policy must cover all zones")
    if any("blindly" in row["vacuum_policy"].lower() for row in retention):
        failures.append("retention policy must not blindly reduce retention")

    if not any(row["area"] == "column lineage" for row in lineage):
        failures.append("lineage readiness must include column lineage")
    if not any(row["area"] == "secret access" for row in audit):
        failures.append("audit catalog must include secret access")
    if not any(row["decision"] == "restricted" for row in sharing):
        failures.append("Delta Sharing matrix must include restricted patterns")
    if not any(row["decision"] == "limited federation" for row in federation):
        failures.append("federation decisions must distinguish limited federation from ingestion")
    if any("deployed" in row["current_status"].lower() for row in readiness):
        failures.append("readiness must not claim deployed resources")

    if repo_root is not None:
        for required_path in (
            "databricks.yml",
            "infra/modules/databricks/foundation.bicep",
            "src/databricks/unity_catalog/sql/01_catalogs_schemas.sql",
            "src/databricks/unity_catalog/sql/02_tables_views_volumes.sql",
            "src/databricks/unity_catalog/sql/03_security_governance.sql",
            "src/databricks/unity_catalog/sql/04_audit_lineage_queries.sql",
        ):
            if not (repo_root / required_path).is_file():
                failures.append(f"missing Databricks foundation asset: {required_path}")

    return failures
