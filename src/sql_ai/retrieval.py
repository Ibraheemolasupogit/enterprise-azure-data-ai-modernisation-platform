from __future__ import annotations

import json
import re
from collections import defaultdict

from sql_ai.model import DocumentChunk, EvaluationQuery


def tokenize(value: str) -> set[str]:
    return {
        token
        for token in re.findall(r"[a-z0-9]+", value.lower())
        if token not in {"the", "and", "for", "with", "what", "why", "about"}
    }


def metadata_filtered_chunks(
    chunks: list[DocumentChunk],
    *,
    shipment_id: str = "",
    account_id: str = "",
    lifecycle_state: str = "active",
) -> list[DocumentChunk]:
    return [
        chunk
        for chunk in chunks
        if (not shipment_id or chunk.shipment_id == shipment_id)
        and (not account_id or chunk.account_id == account_id)
        and chunk.lifecycle_state == lifecycle_state
        and chunk.sensitivity != "restricted"
    ]


def lexical_rank(question: str, chunks: list[DocumentChunk]) -> list[str]:
    question_tokens = tokenize(question)
    scored = []
    for chunk in chunks:
        overlap = len(question_tokens & tokenize(chunk.content))
        scored.append((overlap, chunk.chunk_id))
    return [
        chunk_id
        for score, chunk_id in sorted(scored, key=lambda item: (-item[0], item[1]))
        if score > 0
    ]


def simulated_vector_rank(query_id: str, chunks: list[DocumentChunk]) -> list[str]:
    # Deterministic fixture ranking substitutes for Azure embedding execution.
    affinity = {
        "eval-001": ["carrier_update", "shipment_status", "case_note"],
        "eval-002": ["case_note", "shipment_status", "carrier_update"],
        "eval-003": ["depot_route", "shipment_status", "carrier_update"],
        "eval-004": ["shipment_status", "case_note", "carrier_update"],
        "eval-005": ["billing_case", "case_note", "shipment_status"],
        "eval-006": ["carrier_update", "depot_route", "shipment_status"],
    }.get(query_id, [])
    scored = []
    for chunk in chunks:
        score = len(affinity) + 1
        for index, doc_type in enumerate(affinity):
            if chunk.document_type == doc_type:
                score = index
                break
        scored.append((score, chunk.chunk_id))
    return [chunk_id for score, chunk_id in sorted(scored, key=lambda item: (item[0], item[1]))]


def reciprocal_rank_fusion(
    rankings: list[list[str]],
    *,
    k: int = 60,
) -> list[tuple[str, float]]:
    scores: dict[str, float] = defaultdict(float)
    for ranking in rankings:
        for position, chunk_id in enumerate(ranking, start=1):
            scores[chunk_id] += 1.0 / (k + position)
    return sorted(scores.items(), key=lambda item: (-item[1], item[0]))


def evaluate_query(
    query: EvaluationQuery,
    chunks: list[DocumentChunk],
) -> dict[str, str | float]:
    candidates = metadata_filtered_chunks(
        chunks,
        shipment_id=query.shipment_id,
        account_id=query.account_id,
    )
    lexical = lexical_rank(query.question, candidates)
    vector = simulated_vector_rank(query.query_id, candidates)
    fused = reciprocal_rank_fusion([lexical, vector])
    retrieved = [chunk_id for chunk_id, _score in fused[: query.top_k]]
    expected = set(query.expected_chunk_ids)
    hits = [chunk_id for chunk_id in retrieved if chunk_id in expected]
    first_hit = next(
        (idx for idx, chunk_id in enumerate(retrieved, start=1) if chunk_id in expected),
        0,
    )
    return {
        "query_id": query.query_id,
        "retrieved_chunk_ids": "|".join(retrieved),
        "expected_chunk_ids": "|".join(query.expected_chunk_ids),
        "precision_at_k": round(len(hits) / query.top_k, 4),
        "recall_at_k": round(len(hits) / len(expected), 4),
        "mrr": round(1 / first_hit, 4) if first_hit else 0.0,
        "evidence_classification": "simulated",
    }


def assemble_context_json(
    question: str,
    ranked_chunk_ids: list[str],
    chunks: list[DocumentChunk],
) -> str:
    by_id = {chunk.chunk_id: chunk for chunk in chunks}
    context = {
        "question": question,
        "grounding_policy": "use-context-only",
        "chunks": [
            {
                "chunk_id": chunk_id,
                "document_id": by_id[chunk_id].document_id,
                "rank": rank,
                "content": by_id[chunk_id].content,
                "metadata": {
                    "shipment_id": by_id[chunk_id].shipment_id,
                    "account_id": by_id[chunk_id].account_id,
                    "depot_code": by_id[chunk_id].depot_code,
                    "route_code": by_id[chunk_id].route_code,
                    "document_type": by_id[chunk_id].document_type,
                    "sensitivity": by_id[chunk_id].sensitivity,
                },
                "citation": f"{by_id[chunk_id].document_id}#{by_id[chunk_id].chunk_ordinal}",
            }
            for rank, chunk_id in enumerate(ranked_chunk_ids, start=1)
            if chunk_id in by_id
        ],
    }
    return json.dumps(context, sort_keys=True)
