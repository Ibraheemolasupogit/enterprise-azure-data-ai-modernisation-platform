from __future__ import annotations

import hashlib

from sql_ai.model import DocumentChunk, SourceDocument

CHUNK_LOGIC_VERSION = "deterministic-word-window-v1"


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def content_hash(source: SourceDocument) -> str:
    return sha256_text(
        "|".join(
            [
                source.document_id,
                source.source_system,
                source.document_type,
                source.title,
                source.content,
                source.source_updated_at,
            ]
        )
    )


def chunk_document(
    source: SourceDocument,
    max_words: int = 44,
    overlap_words: int = 8,
) -> list[DocumentChunk]:
    if overlap_words >= max_words:
        raise ValueError("overlap_words must be smaller than max_words")
    words = source.content.split()
    chunks: list[DocumentChunk] = []
    step = max_words - overlap_words
    source_hash = content_hash(source)
    for ordinal, start in enumerate(range(0, len(words), step), start=1):
        segment = " ".join(words[start : start + max_words])
        if not segment:
            continue
        chunk_hash = sha256_text(f"{source.document_id}|{ordinal}|{segment}|{source_hash}")
        chunks.append(
            DocumentChunk(
                chunk_id=f"chunk-{chunk_hash[:16]}",
                document_id=source.document_id,
                chunk_ordinal=ordinal,
                content=segment,
                content_hash=chunk_hash,
                chunk_logic_version=CHUNK_LOGIC_VERSION,
                token_count_estimate=len(segment.split()),
                shipment_id=source.shipment_id,
                account_id=source.account_id,
                depot_code=source.depot_code,
                route_code=source.route_code,
                document_type=source.document_type,
                sensitivity=source.sensitivity,
                lifecycle_state=source.lifecycle_state,
            )
        )
        if start + max_words >= len(words):
            break
    return chunks


def chunk_sources(sources: list[SourceDocument]) -> list[DocumentChunk]:
    chunks: list[DocumentChunk] = []
    for source in sources:
        chunks.extend(chunk_document(source))
    return chunks


def lifecycle_status(
    stored_content_hash: str,
    stored_chunk_logic_version: str,
    stored_model_version: str,
    stored_dimensions: int,
    current_content_hash: str,
    current_chunk_logic_version: str,
    current_model_version: str,
    current_dimensions: int,
) -> str:
    if stored_dimensions != current_dimensions:
        return "stale"
    if stored_model_version != current_model_version:
        return "stale"
    if stored_chunk_logic_version != current_chunk_logic_version:
        return "stale"
    if stored_content_hash != current_content_hash:
        return "stale"
    return "current"

