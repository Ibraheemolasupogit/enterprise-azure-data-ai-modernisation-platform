from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SourceIngestion:
    source: str
    ingestion_mode: str
    expected_frequency: str
    landing_location: str
    bronze_target: str
    schema_contract: str
    checkpoint_requirement: str
    watermark_strategy: str
    error_handling: str
    replay_strategy: str
    idempotency_strategy: str
    evidence_classification: str


@dataclass(frozen=True)
class TableCatalog:
    table_name: str
    source: str
    grain: str
    key_columns: str
    required_metadata: str
    delta_features: str
    sensitivity: str
    evidence_classification: str


@dataclass(frozen=True)
class TransformationCatalog:
    silver_table: str
    bronze_sources: str
    transformation_type: str
    quality_checks: str
    accepted_output: str
    quarantine_output: str
    evidence_classification: str


@dataclass(frozen=True)
class GoldProduct:
    gold_product: str
    grain: str
    source_silver_tables: str
    measures: str
    downstream_use_case: str
    sensitive_data_handling: str
    evidence_classification: str


@dataclass(frozen=True)
class DataModelItem:
    object_name: str
    object_role: str
    grain: str
    business_key: str
    surrogate_key: str
    source_systems: str
    slowly_changing_behavior: str
    late_arriving_handling: str


@dataclass(frozen=True)
class StrategyItem:
    item_id: str
    area: str
    target: str
    strategy: str
    rationale: str
    evidence_classification: str


@dataclass(frozen=True)
class TraceabilityItem:
    source: str
    ingestion_pattern: str
    bronze_table: str
    silver_transformation: str
    gold_product: str
    consumer_or_use_case: str
    evidence_classification: str

