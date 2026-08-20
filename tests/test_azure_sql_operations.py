from __future__ import annotations

import csv
import hashlib
from pathlib import Path

from azure_sql_operations.catalog import (
    ALERT_CATALOG,
    AUTOMATION_CATALOG,
    CONFIGURATION_BASELINE,
    HA_DR_READINESS,
    SECURITY_ROLES,
    SENSITIVE_CONTROLS,
)
from azure_sql_operations.cli import generate_outputs
from azure_sql_operations.validation import validate_outputs


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


def test_configuration_baseline_preserves_sql_mi_decision() -> None:
    settings = {row.setting: row for row in CONFIGURATION_BASELINE}
    assert settings["target_service"].value == "Azure SQL Managed Instance"
    assert settings["public_endpoint"].value == "Disabled for production target"
    assert "TLS 1.2" in settings["minimum_tls"].value
    assert settings["compute"].requires_azure_validation


def test_role_model_uses_least_privilege_and_managed_identity() -> None:
    assert any(role.principal_type == "Managed identity" for role in SECURITY_ROLES)
    assert all(role.least_privilege_rationale for role in SECURITY_ROLES)
    assert any("EXECUTE" in role.permissions for role in SECURITY_ROLES)
    assert not any("password" in role.placeholder_principal.lower() for role in SECURITY_ROLES)


def test_sensitive_controls_cover_masking_rls_and_schema_assets() -> None:
    controls = " ".join(control.controls for control in SENSITIVE_CONTROLS)
    assets = {control.asset for control in SENSITIVE_CONTROLS}
    assert "Dynamic Data Masking" in controls
    assert "Row-Level Security" in controls
    assert "dbo.CustomerAccount.ContactEmail" in assets
    assert "dbo.Shipment.DeclaredValueGbp" in assets


def test_alerts_map_to_runbooks() -> None:
    assert ALERT_CATALOG
    for alert in ALERT_CATALOG:
        assert Path(alert.runbook).is_file()
        assert alert.threshold_rationale
    assert any(alert.signal == "database_unavailable" for alert in ALERT_CATALOG)


def test_automation_avoids_performance_milestone_scope_creep() -> None:
    assert any(item.mechanism == "SQL Agent on Managed Instance" for item in AUTOMATION_CATALOG)
    assert not any("blanket index rebuild" in item.purpose.lower() for item in AUTOMATION_CATALOG)
    assert any("statistics" in item.automation_name for item in AUTOMATION_CATALOG)


def test_hadr_readiness_traces_architecture_without_claiming_execution() -> None:
    assert any(check.area == "DR" for check in HA_DR_READINESS)
    assert any(check.requirement.startswith("RTO 60") for check in HA_DR_READINESS)
    assert any(check.status == "requires Azure validation" for check in HA_DR_READINESS)


def test_outputs_generate_validate_and_are_deterministic(tmp_path: Path) -> None:
    first = tmp_path / "first"
    second = tmp_path / "second"
    generate_outputs(first / "outputs" / "azure_sql_operations", first / "reports")
    generate_outputs(second / "outputs" / "azure_sql_operations", second / "reports")
    assert _digest_tree(first) == _digest_tree(second)
    assert validate_outputs(first / "outputs" / "azure_sql_operations") == []
    assert _read_csv(first / "outputs" / "azure_sql_operations" / "operational_readiness.csv")

