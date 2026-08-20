from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SourceDocument:
    document_id: str
    source_system: str
    document_type: str
    title: str
    content: str
    shipment_id: str
    account_id: str
    depot_code: str
    route_code: str
    sensitivity: str
    lifecycle_state: str
    source_updated_at: str


@dataclass(frozen=True)
class DocumentChunk:
    chunk_id: str
    document_id: str
    chunk_ordinal: int
    content: str
    content_hash: str
    chunk_logic_version: str
    token_count_estimate: int
    shipment_id: str
    account_id: str
    depot_code: str
    route_code: str
    document_type: str
    sensitivity: str
    lifecycle_state: str


@dataclass(frozen=True)
class EmbeddingConfig:
    provider: str
    embedding_model: str
    model_version: str
    dimensions: int
    distance_metric: str
    external_model_name: str
    endpoint_placeholder: str
    identity_mode: str


@dataclass(frozen=True)
class EvaluationQuery:
    query_id: str
    question: str
    expected_chunk_ids: tuple[str, ...]
    shipment_id: str
    account_id: str
    top_k: int

