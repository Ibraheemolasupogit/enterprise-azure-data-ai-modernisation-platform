from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class QualityRule:
    dataset: str
    layer: str
    rule_id: str
    rule_category: str
    fields: str
    expectation: str
    severity: str
    action_on_failure: str
    owner_role: str
    evidence_classification: str


@dataclass(frozen=True)
class SeverityAction:
    severity: str
    default_action: str
    retry_behavior: str
    downstream_behavior: str
    manual_review_required: str


@dataclass(frozen=True)
class QualityResult:
    dataset: str
    rules_evaluated: int
    pass_count: int
    warning_count: int
    rejected_count: int
    quarantined_count: int
    critical_failures: int
    freshness_status: str
    replay_readiness: str
    evidence_classification: str


@dataclass(frozen=True)
class QuarantineItem:
    quarantine_target: str
    source_dataset: str
    rule_id: str
    rejected_record_key: str
    source_metadata: str
    failure_reason: str
    detected_at_utc: str
    raw_payload_policy: str
    remediation_status: str
    replay_eligibility: str


@dataclass(frozen=True)
class JobItem:
    job_id: str
    workflow: str
    purpose: str
    task_type: str
    compute: str
    parameters: str
    max_concurrent_runs: int
    evidence_classification: str


@dataclass(frozen=True)
class TaskDependency:
    workflow: str
    task_key: str
    depends_on: str
    upstream_data_dependency: str
    gate_behavior: str
    downstream_publication_allowed: str


@dataclass(frozen=True)
class ScheduleItem:
    workflow: str
    schedule: str
    rationale: str
    freshness_expectation: str
    breach_threshold: str
    business_impact: str
    escalation_intent: str


@dataclass(frozen=True)
class RetryPolicy:
    failure_class: str
    retry_count: int
    retry_delay_minutes: int
    timeout_minutes: int
    queueing_or_concurrency: str
    action: str


@dataclass(frozen=True)
class MatrixItem:
    item_id: str
    area: str
    target: str
    scenario: str
    response: str
    evidence_classification: str


@dataclass(frozen=True)
class PermissionItem:
    principal: str
    role: str
    scope: str
    permission: str
    rationale: str
    production_boundary: str


@dataclass(frozen=True)
class TraceabilityItem:
    source: str
    ingestion_task: str
    bronze_table: str
    bronze_gate: str
    silver_table: str
    silver_gate: str
    gold_product: str
    gold_gate: str
    publication_readiness: str

