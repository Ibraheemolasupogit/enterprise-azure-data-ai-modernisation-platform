from __future__ import annotations

import csv
import hashlib
from pathlib import Path

from target_architecture.catalog import (
    ASSUMPTIONS,
    COMPONENTS,
    ENVIRONMENTS,
    RECOVERY_STRATEGIES,
    SECURITY_CONTROLS,
    TRACEABILITY,
    WORKLOAD_TARGETS,
)
from target_architecture.cli import generate_architecture
from target_architecture.validation import validate_architecture_outputs


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


def test_every_target_component_has_purpose_and_is_planned() -> None:
    assert COMPONENTS
    assert all(component.purpose for component in COMPONENTS)
    assert all(component.implementation_status == "planned" for component in COMPONENTS)
    planes = {component.plane for component in COMPONENTS}
    assert "Operational data plane" in planes
    assert "Data engineering / analytical plane" in planes
    assert "AI-enabled data plane" in planes
    assert "Control / security / operations plane" in planes


def test_every_workload_has_target_disposition() -> None:
    workloads = {target.workload_id: target for target in WORKLOAD_TARGETS}
    assert workloads["legacy_tms"].selected_service == "Azure SQL Managed Instance"
    assert "PostgreSQL" in workloads["billing_ops"].selected_service
    assert "Azure Databricks" in workloads["operational_reporting"].selected_service
    assert workloads["customer_service_search"].disposition == "retain"
    assert all(target.rejected_alternatives for target in workloads.values())


def test_security_controls_cover_core_assets() -> None:
    text = " ".join(control.applies_to_assets for control in SECURITY_CONTROLS)
    for asset in ("SQL MI", "PostgreSQL", "ADLS", "Databricks", "Key Vault"):
        assert asset in text
    assert any(control.control_name == "Managed workload identity" for control in SECURITY_CONTROLS)
    assert any("Row-Level Security" in control.target_mechanism for control in SECURITY_CONTROLS)


def test_recovery_matrix_assigns_rto_rpo_without_claiming_dr_tested() -> None:
    assert all(strategy.assumed_rto_minutes > 0 for strategy in RECOVERY_STRATEGIES)
    assert all(strategy.assumed_rpo_minutes > 0 for strategy in RECOVERY_STRATEGIES)
    assert all(strategy.validation_status == "not tested" for strategy in RECOVERY_STRATEGIES)


def test_environment_strategy_has_dev_test_prod_boundaries() -> None:
    envs = {environment.environment: environment for environment in ENVIRONMENTS}
    assert set(envs) == {"dev", "test", "prod"}
    assert "production" in envs["prod"].subscription_strategy
    assert "synthetic" in envs["dev"].data_policy


def test_assumptions_include_live_validation_items() -> None:
    assert any(
        assumption.classification == "requires live validation" for assumption in ASSUMPTIONS
    )
    assert any("SQL MI" in assumption.area for assumption in ASSUMPTIONS)
    assert all(assumption.impact_if_wrong for assumption in ASSUMPTIONS)


def test_traceability_maps_requirements_to_future_milestones() -> None:
    assert TRACEABILITY
    assert all(trace.future_implementation_milestone for trace in TRACEABILITY)
    assert any("SQL-COMP" in trace.assessment_finding for trace in TRACEABILITY)
    assert any(
        "streaming" in trace.future_implementation_milestone.lower()
        for trace in TRACEABILITY
    )


def test_architecture_outputs_generate_and_validate(tmp_path: Path) -> None:
    outputs_dir = tmp_path / "outputs" / "architecture"
    reports_dir = tmp_path / "reports"
    generate_architecture(outputs_dir, reports_dir)
    assert validate_architecture_outputs(outputs_dir) == []
    assert _read_csv(outputs_dir / "workload_target_matrix.csv")
    assert (reports_dir / "target_architecture_report.md").is_file()


def test_architecture_generation_is_deterministic(tmp_path: Path) -> None:
    first = tmp_path / "first"
    second = tmp_path / "second"
    generate_architecture(first / "outputs" / "architecture", first / "reports")
    generate_architecture(second / "outputs" / "architecture", second / "reports")
    assert _digest_tree(first) == _digest_tree(second)
