from __future__ import annotations

from dataclasses import dataclass

EvidenceClass = str


@dataclass(frozen=True)
class SourceSystem:
    system_id: str
    system_name: str
    engine: str
    assumed_version: str
    business_domain: str
    workload_type: str
    database_size_gb: float
    database_size_evidence: EvidenceClass
    annual_growth_pct: float
    growth_evidence: EvidenceClass
    transaction_volume_per_day: int
    transaction_volume_evidence: EvidenceClass
    peak_workload: str
    availability_requirement: str
    rto_minutes: int
    rpo_minutes: int
    data_sensitivity: str
    dependencies: str
    integration_patterns: str
    authentication_model: str
    operational_owner: str
    business_criticality: str
    downtime_tolerance_minutes: int
    support_constraints: str
    technical_debt_indicators: str


@dataclass(frozen=True)
class Dependency:
    dependency_id: str
    source: str
    target: str
    dependency_type: str
    direction: str
    evidence_class: EvidenceClass
    evidence: str
    migration_relevance: str


@dataclass(frozen=True)
class CompatibilityFinding:
    finding_id: str
    source_object: str
    category: str
    severity: str
    affected_targets: str
    evidence: str
    remediation: str
    migration_impact: str
