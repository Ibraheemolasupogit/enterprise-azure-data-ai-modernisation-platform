from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ProjectObject:
    object_id: str
    object_type: str
    schema_name: str
    object_name: str
    source_path: str
    deployment_phase: str
    owner: str
    evidence_classification: str


@dataclass(frozen=True)
class TraceabilityItem:
    requirement_id: str
    source_requirement: str
    database_object: str
    project_asset: str
    validation_asset: str
    release_gate: str


@dataclass(frozen=True)
class ReferenceDataItem:
    dataset_id: str
    target_table: str
    key_columns: str
    row_count: int
    deployment_method: str
    idempotency_strategy: str
    source_asset: str


@dataclass(frozen=True)
class LifecycleRule:
    rule_id: str
    area: str
    rule: str
    enforcement_point: str
    failure_action: str
    rollback_boundary: str


@dataclass(frozen=True)
class DriftScenario:
    scenario_id: str
    drift_type: str
    example_change: str
    detection_method: str
    expected_response: str
    automation_boundary: str


@dataclass(frozen=True)
class PromotionEnvironment:
    environment: str
    branch_or_trigger: str
    approval_gate: str
    deployment_mode: str
    data_safety_level: str
    evidence_required: str


@dataclass(frozen=True)
class DatabaseTest:
    test_id: str
    test_type: str
    target: str
    assertion: str
    execution_context: str
    required_for_release: str


@dataclass(frozen=True)
class RegressionGate:
    gate_id: str
    area: str
    measured_artifact: str
    threshold: str
    evidence_source: str
    release_decision: str


@dataclass(frozen=True)
class ReleaseReadinessItem:
    check_id: str
    area: str
    check: str
    status: str
    evidence: str
    deferred_boundary: str

