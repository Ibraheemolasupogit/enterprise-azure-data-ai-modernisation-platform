from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class MonitoringItem:
    control_id: str
    workload: str
    component: str
    monitoring_source: str
    signal: str
    purpose: str
    owner: str
    evidence_classification: str


@dataclass(frozen=True)
class JobHealthRule:
    rule_id: str
    job_or_workflow: str
    condition: str
    threshold_or_detection: str
    freshness_impact: str
    owner: str
    runbook: str
    evidence_classification: str


@dataclass(frozen=True)
class PipelineStage:
    stage: str
    source_or_table: str
    status_signal: str
    count_signal: str
    freshness_signal: str
    latency_signal: str
    checkpoint_signal: str
    evidence_classification: str


@dataclass(frozen=True)
class TroubleshootingItem:
    symptom: str
    possible_cause: str
    diagnostic_evidence: str
    safe_remediation: str
    evidence_classification: str


@dataclass(frozen=True)
class OptimizationItem:
    target: str
    area: str
    current_or_expected_pattern: str
    recommendation: str
    performance_consideration: str
    cost_consideration: str
    evidence_classification: str


@dataclass(frozen=True)
class PolicyItem:
    policy_id: str
    environment: str
    control: str
    value_or_rule: str
    rationale: str
    evidence_classification: str


@dataclass(frozen=True)
class CostItem:
    dimension: str
    required_tag_or_source: str
    attribution_use: str
    owner: str
    evidence_classification: str


@dataclass(frozen=True)
class AlertItem:
    alert_id: str
    condition: str
    severity: str
    owner: str
    investigation_query: str
    runbook: str
    escalation_path: str
    evidence_classification: str


@dataclass(frozen=True)
class SloItem:
    workload: str
    freshness_target: str
    processing_target: str
    failure_tolerance: str
    recovery_target: str
    business_criticality: str
    evidence_classification: str


@dataclass(frozen=True)
class TraceabilityItem:
    workload: str
    job_or_pipeline: str
    monitoring_signal: str
    alert: str
    runbook: str
    owner: str
    cost_dimension: str
    optimization_control: str

