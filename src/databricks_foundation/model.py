from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class WorkspaceStrategy:
    environment: str
    workspace_name: str
    purpose: str
    isolation_model: str
    region_assumption: str
    identity_boundary: str
    storage_boundary: str
    catalog_boundary: str
    promotion_model: str
    evidence_classification: str


@dataclass(frozen=True)
class ComputeStrategy:
    workload_class: str
    preferred_compute: str
    runtime_strategy: str
    autoscaling: str
    auto_termination_minutes: int
    photon: str
    worker_sizing: str
    policy: str
    library_scope: str
    cost_consideration: str
    security_implication: str
    production_restriction: str


@dataclass(frozen=True)
class NamespaceObject:
    environment: str
    catalog: str
    schema_name: str
    object_type: str
    object_name: str
    purpose: str
    managed_or_external: str
    source_asset: str
    evidence_classification: str


@dataclass(frozen=True)
class StorageBoundary:
    location_id: str
    environment: str
    storage_asset: str
    uc_object: str
    object_type: str
    intended_path: str
    access_method: str
    lifecycle_owner: str
    governance_owner: str
    deletion_behavior: str


@dataclass(frozen=True)
class AccessControl:
    principal: str
    principal_type: str
    scope: str
    privileges: str
    rationale: str
    production_boundary: str


@dataclass(frozen=True)
class FineGrainedSecurity:
    control_id: str
    domain: str
    target_object: str
    control_type: str
    protected_attribute: str
    enforcement_pattern: str
    fallback_pattern: str
    evidence_classification: str


@dataclass(frozen=True)
class GovernedTag:
    tag_name: str
    allowed_values: str
    applies_to: str
    steward_group: str
    policy_use: str
    examples: str


@dataclass(frozen=True)
class RetentionPolicy:
    dataset_zone: str
    log_retention: str
    deleted_file_retention: str
    vacuum_policy: str
    time_travel_need: str
    compliance_deletion_boundary: str
    adls_lifecycle: str


@dataclass(frozen=True)
class ReadinessItem:
    item_id: str
    area: str
    capability: str
    expected_evidence: str
    current_status: str
    evidence_classification: str


@dataclass(frozen=True)
class SharingDecision:
    decision_id: str
    sharing_pattern: str
    allowed_scope: str
    sensitive_data_rule: str
    audit_requirement: str
    revocation_model: str
    decision: str


@dataclass(frozen=True)
class FederationDecision:
    source_system: str
    federation_use_case: str
    ingestion_preference: str
    allowed_usage: str
    restriction: str
    decision: str


@dataclass(frozen=True)
class BundleTarget:
    target: str
    workspace_host_variable: str
    catalog_variable: str
    service_principal_requirement: str
    deployment_mode: str
    resource_boundary: str

