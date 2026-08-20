from __future__ import annotations

from dataclasses import dataclass

EvidenceClass = str


@dataclass(frozen=True)
class ArchitectureComponent:
    component_id: str
    component_name: str
    plane: str
    azure_service: str
    purpose: str
    implementation_status: str
    evidence_class: EvidenceClass
    key_decision: str
    not_used_alternatives: str


@dataclass(frozen=True)
class WorkloadTarget:
    workload_id: str
    source_system: str
    selected_target_component: str
    selected_service: str
    disposition: str
    rationale: str
    rejected_alternatives: str
    architecture_decision: str
    implementation_milestone: str


@dataclass(frozen=True)
class SecurityControl:
    control_id: str
    control_name: str
    control_category: str
    applies_to_assets: str
    target_mechanism: str
    implementation_status: str
    evidence_class: EvidenceClass
    future_milestone: str


@dataclass(frozen=True)
class RecoveryStrategy:
    workload_tier: str
    applies_to: str
    assumed_rto_minutes: int
    assumed_rpo_minutes: int
    target_ha_design: str
    target_dr_design: str
    backup_restore: str
    validation_status: str
    evidence_class: EvidenceClass


@dataclass(frozen=True)
class EnvironmentDefinition:
    environment: str
    subscription_strategy: str
    resource_group_pattern: str
    data_policy: str
    network_policy: str
    secrets_policy: str
    ci_cd_promotion: str
    production_protection: str


@dataclass(frozen=True)
class Assumption:
    assumption_id: str
    area: str
    assumption: str
    classification: EvidenceClass
    validation_required: str
    impact_if_wrong: str


@dataclass(frozen=True)
class Traceability:
    trace_id: str
    business_requirement: str
    assessment_finding: str
    architecture_decision: str
    target_component: str
    future_implementation_milestone: str

