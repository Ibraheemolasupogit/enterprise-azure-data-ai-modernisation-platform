from __future__ import annotations

import json

from sql_ai.catalog import SOURCE_DOCUMENTS
from sql_ai.chunking import (
    CHUNK_LOGIC_VERSION,
    chunk_document,
    chunk_sources,
    content_hash,
    lifecycle_status,
)
from sql_ai.cli import _queries_with_expected_chunks
from sql_ai.retrieval import (
    assemble_context_json,
    evaluate_query,
    lexical_rank,
    metadata_filtered_chunks,
    reciprocal_rank_fusion,
    simulated_vector_rank,
)


def test_chunking_is_deterministic_and_traceable() -> None:
    first = chunk_document(SOURCE_DOCUMENTS[0])
    second = chunk_document(SOURCE_DOCUMENTS[0])
    assert first == second
    assert first[0].document_id == SOURCE_DOCUMENTS[0].document_id
    assert first[0].shipment_id == "SHP1001"
    assert first[0].content_hash
    assert content_hash(SOURCE_DOCUMENTS[0]) == content_hash(SOURCE_DOCUMENTS[0])


def test_lifecycle_marks_stale_when_content_model_logic_or_dimensions_change() -> None:
    chunk = chunk_document(SOURCE_DOCUMENTS[0])[0]
    current_args = (chunk.content_hash, CHUNK_LOGIC_VERSION, "v1", 1536)
    assert lifecycle_status(*current_args, *current_args) == "current"
    assert lifecycle_status(
        "old",
        CHUNK_LOGIC_VERSION,
        "v1",
        1536,
        *current_args,
    ) == "stale"
    assert lifecycle_status(
        chunk.content_hash,
        "old",
        "v1",
        1536,
        *current_args,
    ) == "stale"
    assert lifecycle_status(
        chunk.content_hash,
        CHUNK_LOGIC_VERSION,
        "old",
        1536,
        *current_args,
    ) == "stale"
    assert lifecycle_status(
        chunk.content_hash,
        CHUNK_LOGIC_VERSION,
        "v1",
        3072,
        *current_args,
    ) == "stale"


def test_metadata_filters_enforce_shipment_account_lifecycle_and_sensitivity() -> None:
    chunks = chunk_sources(SOURCE_DOCUMENTS)
    filtered = metadata_filtered_chunks(chunks, shipment_id="SHP1001", account_id="ACC-100")
    assert filtered
    assert {chunk.shipment_id for chunk in filtered} == {"SHP1001"}
    assert {chunk.account_id for chunk in filtered} == {"ACC-100"}
    assert all(chunk.lifecycle_state == "active" for chunk in filtered)
    assert all(chunk.sensitivity != "restricted" for chunk in filtered)


def test_rrf_prefers_items_high_in_both_rankings() -> None:
    fused = reciprocal_rank_fusion([["a", "b", "c"], ["b", "a", "d"]])
    assert fused[0][0] in {"a", "b"}
    assert {chunk_id for chunk_id, _ in fused[:2]} == {"a", "b"}


def test_retrieval_metrics_are_deterministic() -> None:
    chunks = chunk_sources(SOURCE_DOCUMENTS)
    queries = _queries_with_expected_chunks(chunks)
    results = [evaluate_query(query, chunks) for query in queries]
    assert all(float(result["precision_at_k"]) > 0 for result in results)
    assert all(float(result["recall_at_k"]) > 0 for result in results)
    assert all(float(result["mrr"]) > 0 for result in results)
    assert all(result["evidence_classification"] == "simulated" for result in results)


def test_rankers_and_context_assembly_preserve_sources_and_citations() -> None:
    chunks = chunk_sources(SOURCE_DOCUMENTS)
    query = _queries_with_expected_chunks(chunks)[0]
    candidates = metadata_filtered_chunks(
        chunks,
        shipment_id=query.shipment_id,
        account_id=query.account_id,
    )
    lexical = lexical_rank(query.question, candidates)
    vector = simulated_vector_rank(query.query_id, candidates)
    fused = reciprocal_rank_fusion([lexical, vector])
    ranked_ids = [chunk_id for chunk_id, _ in fused[: query.top_k]]
    context_json = assemble_context_json(query.question, ranked_ids, chunks)
    payload = json.loads(context_json)
    assert payload["grounding_policy"] == "use-context-only"
    assert payload["chunks"]
    assert all("citation" in chunk for chunk in payload["chunks"])
    assert all(chunk["metadata"]["shipment_id"] == "SHP1001" for chunk in payload["chunks"])
