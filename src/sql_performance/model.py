from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Workload:
    workload_id: str
    sql_asset: str
    workload_type: str
    read_write_profile: str
    frequency: str
    concurrency_expectation: str
    business_criticality: str
    latency_sensitivity: str
    expected_data_volume: str
    blocking_sensitivity: str
    index_dependency: str
    candidate_tuning_technique: str


@dataclass(frozen=True)
class BaselineMetric:
    workload_id: str
    execution_duration_ms: int
    logical_reads: int
    cpu_proxy_ms: int
    rows_processed: int
    execution_count: int
    concurrency_class: str
    workload_type: str
    expected_latency_class: str
    metric_classification: str


@dataclass(frozen=True)
class QueryAnalysis:
    query_id: str
    workload_id: str
    sql_asset: str
    analysis_type: str
    expected_plan_risk: str
    evidence: str
    recommendation: str
    evidence_classification: str


@dataclass(frozen=True)
class IndexRecommendation:
    recommendation_id: str
    target_object: str
    recommendation_type: str
    proposed_index: str
    rationale: str
    expected_benefit: str
    write_overhead_consideration: str
    status: str


@dataclass(frozen=True)
class StrategyItem:
    item_id: str
    area: str
    recommendation: str
    rationale: str
    status: str
    evidence_classification: str

