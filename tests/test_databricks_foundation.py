from __future__ import annotations

import csv
import hashlib
from pathlib import Path

from databricks_foundation.catalog import (
    ACCESS,
    BUNDLE_TARGETS,
    COMPUTE,
    FEDERATION,
    FINE_GRAINED,
    NAMESPACE,
    RETENTION,
    SHARING,
    STORAGE,
    TAGS,
    WORKSPACES,
)
from databricks_foundation.cli import generate_outputs
from databricks_foundation.validation import validate_outputs

ROOT = Path(__file__).resolve().parents[1]


def _digest_tree(path: Path) -> str:
    digest = hashlib.sha256()
    for file_path in sorted(path.rglob("*")):
        if file_path.is_file():
            digest.update(str(file_path.relative_to(path)).encode("utf-8"))
            digest.update(file_path.read_bytes())
    return digest.hexdigest()


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def test_workspace_and_namespace_model_cover_environments() -> None:
    envs = {"dev", "test", "prod"}
    assert {workspace.environment for workspace in WORKSPACES} == envs
    for env in envs:
        catalog = f"contoso_freight_{env}"
        schemas = {
            item.schema_name
            for item in NAMESPACE
            if item.catalog == catalog and item.object_type == "schema"
        }
        assert {"bronze", "silver", "gold", "reference", "quarantine", "audit"} <= schemas


def test_compute_strategy_maps_practical_workload_classes() -> None:
    workloads = {item.workload_class for item in COMPUTE}
    assert "interactive engineering" in workloads
    assert "batch ingestion job" in workloads
    assert "event ingestion" in workloads
    assert "SQL serving" in workloads
    assert "future Delta Live Tables/Lakeflow pipeline" in workloads
    assert all("benchmark" not in item.cost_consideration.lower() for item in COMPUTE)
    assert any(item.production_restriction.startswith("not allowed") for item in COMPUTE)


def test_storage_boundaries_use_managed_identity_not_keys() -> None:
    assert any(item.object_type == "storage credential" for item in STORAGE)
    assert any(item.object_type == "external location" for item in STORAGE)
    assert all("key" not in item.access_method.lower() for item in STORAGE)
    assert all("sas" not in item.access_method.lower() for item in STORAGE)


def test_access_and_fine_grained_security_are_least_privilege() -> None:
    assert any(item.principal_type == "service principal" for item in ACCESS)
    assert not any(item.privileges == "ALL PRIVILEGES" for item in ACCESS)
    assert any(item.control_type == "column mask" for item in FINE_GRAINED)
    assert any(item.control_type == "row filter" for item in FINE_GRAINED)
    assert any(item.tag_name == "pii" for item in TAGS)
    assert any(item.tag_name == "sensitivity" for item in TAGS)


def test_retention_sharing_federation_and_bundle_boundaries() -> None:
    assert {"bronze", "silver", "gold", "reference", "quarantine", "audit"} <= {
        item.dataset_zone for item in RETENTION
    }
    assert any(item.decision == "restricted" for item in SHARING)
    assert any(item.decision == "limited federation" for item in FEDERATION)
    assert any(item.decision == "ingest" for item in FEDERATION)
    assert {item.target for item in BUNDLE_TARGETS} == {"dev", "test", "prod"}


def test_outputs_generate_validate_and_are_deterministic(tmp_path: Path) -> None:
    first = tmp_path / "first"
    second = tmp_path / "second"
    generate_outputs(first / "outputs" / "databricks_foundation", first / "reports", ROOT)
    generate_outputs(second / "outputs" / "databricks_foundation", second / "reports", ROOT)
    assert _digest_tree(first) == _digest_tree(second)
    assert validate_outputs(first / "outputs" / "databricks_foundation", ROOT) == []
    assert _read_csv(
        first / "outputs" / "databricks_foundation" / "platform_readiness.csv"
    )

