from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class FabricProduct:
    product_id: str
    gold_product: str
    owner: str
    grain: str
    source: str
    authoritative_platform: str
    schema_version: str
    freshness: str
    sensitivity: str
    quality_status: str
    fabric_eligible: str


@dataclass(frozen=True)
class ContractField:
    dataset: str
    schema_version: str
    field: str
    data_type: str
    nullable: str
    key: str
    semantic_meaning: str
    sensitivity: str
    allowed_consumer_class: str
    freshness_expectation: str
    quality_expectation: str
    lifecycle: str


@dataclass(frozen=True)
class PatternDecision:
    product_id: str
    pattern: str
    decision: str
    use_case: str
    data_duplication: str
    latency: str
    governance: str
    ownership: str
    cost: str
    operational_complexity: str
    limitations: str

