from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class MigrationManifest:
    migration_id: str
    source_system: str
    source_engine_version_assumption: str
    target_service: str
    target_engine_version_assumption: str
    migration_wave: str
    disposition: str
    preferred_migration_mode: str
    expected_downtime_minutes: int
    rto_minutes: int
    rpo_minutes: int
    schema_objects: str
    data_domains: str
    dependency_prerequisites: str
    compatibility_blockers: str
    remediation_status: str
    validation_rules: str
    cutover_owner_role: str
    rollback_trigger: str
    hypercare_period: str
    evidence_classification: str


@dataclass(frozen=True)
class Remediation:
    compatibility_finding: str
    source_object: str
    required_remediation: str
    target_object: str
    status: str
    validation_evidence: str


@dataclass(frozen=True)
class ValidationGate:
    migration_id: str
    gate_stage: str
    gate_name: str
    status: str
    evidence_classification: str
    evidence: str
    stop_on_failure: bool


@dataclass(frozen=True)
class ToolIntegration:
    tool_name: str
    migration_phase: str
    real_integration_point: str
    local_adapter_boundary: str
    evidence_expected_in_real_engagement: str

