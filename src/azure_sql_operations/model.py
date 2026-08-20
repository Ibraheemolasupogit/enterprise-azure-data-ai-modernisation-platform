from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ConfigurationBaseline:
    setting: str
    value: str
    rationale: str
    evidence_classification: str
    requires_azure_validation: bool


@dataclass(frozen=True)
class SecurityRole:
    principal_type: str
    placeholder_principal: str
    database_role: str
    permissions: str
    least_privilege_rationale: str
    evidence_classification: str


@dataclass(frozen=True)
class SensitiveDataControl:
    asset: str
    sensitivity: str
    controls: str
    implementation_status: str
    evidence_classification: str


@dataclass(frozen=True)
class MonitoringItem:
    signal: str
    source: str
    kql_asset: str
    operational_purpose: str
    milestone_boundary: str


@dataclass(frozen=True)
class AlertRule:
    alert_name: str
    signal: str
    severity: str
    threshold_rationale: str
    evaluation_window: str
    action_group_intent: str
    runbook: str


@dataclass(frozen=True)
class AutomationItem:
    automation_name: str
    mechanism: str
    cadence: str
    purpose: str
    safety_boundary: str
    evidence_classification: str


@dataclass(frozen=True)
class ReadinessCheck:
    check_id: str
    area: str
    requirement: str
    status: str
    evidence: str
    control_or_runbook: str

