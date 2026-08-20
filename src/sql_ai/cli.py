from __future__ import annotations

# ruff: noqa: E501
import argparse
import csv
from dataclasses import asdict, replace
from pathlib import Path
from typing import Any

from sql_ai.catalog import EMBEDDING_CONFIG, EVALUATION_QUERIES, SOURCE_DOCUMENTS
from sql_ai.chunking import CHUNK_LOGIC_VERSION, chunk_sources, content_hash, lifecycle_status
from sql_ai.model import DocumentChunk, EvaluationQuery
from sql_ai.retrieval import (
    assemble_context_json,
    evaluate_query,
    lexical_rank,
    metadata_filtered_chunks,
    reciprocal_rank_fusion,
    simulated_vector_rank,
)
from sql_ai.validation import validate_outputs


def generate_outputs(outputs_dir: Path, reports_dir: Path, repo_root: Path | None = None) -> dict[str, Path]:
    outputs_dir.mkdir(parents=True, exist_ok=True)
    reports_dir.mkdir(parents=True, exist_ok=True)
    chunks = chunk_sources(SOURCE_DOCUMENTS)
    queries = _queries_with_expected_chunks(chunks)
    written: dict[str, Path] = {}
    outputs = {
        "ai_use_case_catalog.csv": _use_cases(),
        "ai_schema_catalog.csv": _schema_catalog(),
        "document_source_matrix.csv": _source_matrix(),
        "chunking_strategy.csv": _chunking_strategy(chunks),
        "embedding_configuration.csv": _embedding_configuration(),
        "embedding_lifecycle.csv": _embedding_lifecycle(chunks),
        "change_detection_strategy.csv": _change_detection_strategy(),
        "lexical_search_catalog.csv": _lexical_search_catalog(),
        "vector_search_catalog.csv": _vector_search_catalog(),
        "hybrid_retrieval_strategy.csv": _hybrid_retrieval_strategy(),
        "retrieval_evaluation_dataset.csv": _evaluation_dataset(queries),
        "retrieval_evaluation_results.csv": _evaluation_results(queries, chunks),
        "rag_context_contract.csv": _context_contract(queries, chunks),
        "rag_execution_steps.csv": _rag_execution_steps(),
        "ai_security_matrix.csv": _security_matrix(),
        "ai_data_exposure_matrix.csv": _data_exposure_matrix(),
        "ai_audit_catalog.csv": _audit_catalog(),
        "ai_failure_handling.csv": _failure_handling(),
        "ai_cost_controls.csv": _cost_controls(),
        "sql_ai_readiness.csv": _readiness(),
    }
    for filename, rows in outputs.items():
        path = outputs_dir / filename
        _write_csv(path, rows)
        written[filename] = path
    report = reports_dir / "sql_ai_report.md"
    report.write_text(_report(), encoding="utf-8")
    written["sql_ai_report.md"] = report
    failures = validate_outputs(outputs_dir, repo_root or Path.cwd())
    if failures:
        joined = "\n".join(f"- {failure}" for failure in failures)
        raise RuntimeError(f"SQL AI validation failed:\n{joined}")
    return written


def _write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def _queries_with_expected_chunks(chunks: list[DocumentChunk]) -> list[EvaluationQuery]:
    first_by_doc_type = {
        chunk.document_type: chunk.chunk_id
        for chunk in sorted(chunks, key=lambda item: (item.document_type, item.chunk_ordinal))
    }
    expectations = {
        "eval-001": ("carrier_update", "shipment_status"),
        "eval-002": ("case_note",),
        "eval-003": ("depot_route",),
        "eval-004": ("shipment_status", "carrier_update", "case_note"),
        "eval-005": ("billing_case",),
        "eval-006": ("depot_route", "carrier_update"),
    }
    return [
        replace(query, expected_chunk_ids=tuple(first_by_doc_type[name] for name in expectations[query.query_id]))
        for query in EVALUATION_QUERIES
    ]


def _use_cases() -> list[dict[str, str]]:
    return [
        {
            "use_case_id": "sql-ai-001",
            "domain": "Customer Service / Shipment Operations",
            "assistant_scope": "Grounded knowledge assistant for shipment, delay, case note, carrier, depot, and route questions.",
            "excluded_scope": "No autonomous decisions, refunds, rerouting, operational writes, or ungrounded advice.",
            "primary_users": "customer service agents; shipment operations supervisors",
            "evidence_classification": "configuration defined",
        }
    ]


def _schema_catalog() -> list[dict[str, str]]:
    objects = [
        ("ai.Document", "source document registry and metadata"),
        ("ai.DocumentChunk", "deterministic chunks with VECTOR(1536) embedding column"),
        ("ai.EmbeddingMetadata", "provider, model, dimensions, hash, lifecycle, retry, and error status"),
        ("ai.RetrievalAudit", "retrieval request, filters, ranked chunks, identity, and status"),
        ("ai.GenerationAudit", "LLM invocation boundary, answer status, citations, and error summary"),
        ("ai.usp_AssembleRagContext", "SQL-native context JSON assembly for grounded generation"),
    ]
    return [
        {
            "object_name": name,
            "purpose": purpose,
            "project_asset": f"src/azure_sql/database_project/legacy_tms/{'StoredProcedures' if 'usp_' in name else 'Tables'}/{name}.sql",
            "evidence_classification": "configuration defined",
        }
        for name, purpose in objects
    ]


def _source_matrix() -> list[dict[str, str]]:
    return [
        {
            "document_id": source.document_id,
            "source_system": source.source_system,
            "document_type": source.document_type,
            "shipment_id": source.shipment_id,
            "account_id": source.account_id,
            "source_hash": content_hash(source),
            "ai_ready_boundary": "operational/curated source to ai.Document ingestion queue",
            "evidence_classification": "locally validated",
        }
        for source in SOURCE_DOCUMENTS
    ]


def _chunking_strategy(chunks: list[DocumentChunk]) -> list[dict[str, str | int]]:
    return [
        {
            "chunk_id": chunk.chunk_id,
            "document_id": chunk.document_id,
            "chunk_ordinal": chunk.chunk_ordinal,
            "chunk_logic_version": chunk.chunk_logic_version,
            "token_count_estimate": chunk.token_count_estimate,
            "content_hash": chunk.content_hash,
            "sql_function_boundary": "AI_GENERATE_CHUNKS target-ready example; local deterministic word-window validated",
            "evidence_classification": "locally validated",
        }
        for chunk in chunks
    ]


def _embedding_configuration() -> list[dict[str, str | int]]:
    return [
        {
            **asdict(EMBEDDING_CONFIG),
            "source_hash_policy": "embed only current chunk content hash with chunk logic version",
            "secret_policy": "no keys in repo; managed identity and database scoped credential placeholders only",
            "evidence_classification": "configuration defined",
        }
    ]


def _embedding_lifecycle(chunks: list[DocumentChunk]) -> list[dict[str, str | int]]:
    current = chunks[0]
    return [
        {
            "state": "current",
            "trigger": "content hash, chunk logic, model version, and dimensions all match",
            "example_status": lifecycle_status(current.content_hash, CHUNK_LOGIC_VERSION, "v1", 1536, current.content_hash, CHUNK_LOGIC_VERSION, "v1", 1536),
            "worker_action": "eligible for retrieval",
            "evidence_classification": "locally validated",
        },
        {
            "state": "stale",
            "trigger": "content, chunk logic, model version, or dimensions changed",
            "example_status": lifecycle_status("old", CHUNK_LOGIC_VERSION, "v1", 1536, current.content_hash, CHUNK_LOGIC_VERSION, "v1", 1536),
            "worker_action": "enqueue re-embedding asynchronously",
            "evidence_classification": "locally validated",
        },
        {"state": "pending", "trigger": "new or changed chunk awaiting embedding worker", "example_status": "pending", "worker_action": "generate embedding with retry policy", "evidence_classification": "configuration defined"},
        {"state": "failed", "trigger": "provider or dimension error exceeded retry policy", "example_status": "failed", "worker_action": "manual investigation and dead-letter review", "evidence_classification": "configuration defined"},
        {"state": "retired", "trigger": "source document retired or no longer authorized", "example_status": "retired", "worker_action": "exclude from retrieval", "evidence_classification": "configuration defined"},
    ]


def _change_detection_strategy() -> list[dict[str, str]]:
    return [
        {"strategy": "Change Tracking", "decision": "preferred", "reason": "captures committed OLTP row changes without invoking AI inside triggers", "worker_boundary": "async embedding worker reads changed source IDs", "evidence_classification": "configuration defined"},
        {"strategy": "CDC", "decision": "candidate for richer audit history", "reason": "useful when before/after lineage is required", "worker_boundary": "batch re-embedding queue", "evidence_classification": "configuration defined"},
        {"strategy": "triggers", "decision": "metadata only", "reason": "do not call AI from OLTP triggers; optionally write lightweight queue records", "worker_boundary": "transactional enqueue only", "evidence_classification": "configuration defined"},
        {"strategy": "Change Event Streaming", "decision": "future integration boundary", "reason": "appropriate for downstream event-driven refresh", "worker_boundary": "requires Azure validation", "evidence_classification": "requires Azure SQL validation"},
    ]


def _lexical_search_catalog() -> list[dict[str, str]]:
    return [
        {"asset": "full-text index on ai.DocumentChunk.Content", "strength": "exact terms, shipment IDs, carrier names, case IDs, and phrase matching", "limit": "misses semantic paraphrases and operational synonyms", "query_pattern": "CONTAINS/FREETEXT with metadata filters", "evidence_classification": "configuration defined"}
    ]


def _vector_search_catalog() -> list[dict[str, str | int]]:
    return [
        {"target_table": "ai.DocumentChunk", "vector_column": "EmbeddingVector", "dimensions": 1536, "distance_metric": "cosine", "query_pattern": "VECTOR_DISTANCE exact nearest neighbor", "index_boundary": "no vector index required; requires Azure SQL vector runtime", "evidence_classification": "requires Azure SQL validation"},
        {"target_table": "ai.DocumentChunk", "vector_column": "EmbeddingVector", "dimensions": 1536, "distance_metric": "cosine", "query_pattern": "VECTOR_SEARCH approximate nearest neighbor", "index_boundary": "DiskANN/vector index where supported; rebuild and runtime prerequisites required", "evidence_classification": "requires Azure SQL validation"},
    ]


def _hybrid_retrieval_strategy() -> list[dict[str, str]]:
    return [
        {"strategy": "reciprocal rank fusion", "inputs": "full-text rank plus vector rank", "ranking_rule": "RRF score = sum 1/(60 + rank) without arbitrary learned weights", "filters": "shipment, account, depot, route, doc type, source, date, sensitivity, lifecycle, authorization", "evidence_classification": "locally validated"}
    ]


def _evaluation_dataset(queries: list[EvaluationQuery]) -> list[dict[str, str | int]]:
    return [
        {"query_id": query.query_id, "question": query.question, "expected_chunk_ids": "|".join(query.expected_chunk_ids), "shipment_id": query.shipment_id, "account_id": query.account_id, "top_k": query.top_k, "evidence_classification": "locally validated"}
        for query in queries
    ]


def _evaluation_results(queries: list[EvaluationQuery], chunks: list[DocumentChunk]) -> list[dict[str, str | float]]:
    return [evaluate_query(query, chunks) for query in queries]


def _context_contract(queries: list[EvaluationQuery], chunks: list[DocumentChunk]) -> list[dict[str, str]]:
    query = queries[0]
    candidates = metadata_filtered_chunks(chunks, shipment_id=query.shipment_id, account_id=query.account_id)
    fused = reciprocal_rank_fusion([lexical_rank(query.question, candidates), simulated_vector_rank(query.query_id, candidates)])
    ranked_ids = [chunk_id for chunk_id, _ in fused[: query.top_k]]
    return [
        {
            "contract_id": "rag-context-json-v1",
            "required_fields": "question,grounding_policy,chunks[].chunk_id,document_id,rank,content,metadata,citation",
            "sample_context_json": assemble_context_json(query.question, ranked_ids, chunks),
            "evidence_classification": "locally validated",
        }
    ]


def _rag_execution_steps() -> list[dict[str, str | int]]:
    steps = [
        ("question received", "validate caller identity and metadata filters", "locally validated"),
        ("question embedding", "AI_GENERATE_EMBEDDINGS or Azure OpenAI endpoint boundary", "requires Azure OpenAI validation"),
        ("retrieval", "full-text plus VECTOR_DISTANCE/VECTOR_SEARCH with authorization filters", "requires Azure SQL validation"),
        ("hybrid ranking", "RRF top-k and freshness filtering", "locally validated"),
        ("context assembly", "FOR JSON/JSON_OBJECT context with citations", "locally validated"),
        ("generation", "sp_invoke_external_rest_endpoint to approved Azure OpenAI endpoint", "requires Azure OpenAI validation"),
        ("audit", "record retrieval and generation status without indiscriminate sensitive payload storage", "configuration defined"),
    ]
    return [
        {"step_number": index, "step": step, "implementation": implementation, "evidence_classification": classification}
        for index, (step, implementation, classification) in enumerate(steps, start=1)
    ]


def _security_matrix() -> list[dict[str, str]]:
    return [
        {"principal_or_role": "ai_app_executor", "allowed_access": "execute context assembly and RAG procedures; filtered read through approved views", "denied_access": "direct embedding writes, broad table ownership, cross-account reads", "evidence_classification": "configuration defined"},
        {"principal_or_role": "ai_data_curator", "allowed_access": "manage source mappings and retire documents", "denied_access": "invoke generation endpoint", "evidence_classification": "configuration defined"},
        {"principal_or_role": "ai_auditor", "allowed_access": "read audit summaries and metadata", "denied_access": "read unrestricted chunk payloads", "evidence_classification": "configuration defined"},
        {"principal_or_role": "embedding_worker_identity", "allowed_access": "read pending chunks and update embedding metadata/vector columns", "denied_access": "generation invocation and customer-service answer paths", "evidence_classification": "configuration defined"},
    ]


def _data_exposure_matrix() -> list[dict[str, str]]:
    return [
        {"data_class": "shipment status and events", "embedding_policy": "may be embedded", "ai_context_policy": "allow when authorized", "control": "shipment/account filters and RLS alignment", "evidence_classification": "configuration defined"},
        {"data_class": "contact information", "embedding_policy": "avoid where possible", "ai_context_policy": "exclude or redact", "control": "sanitized source projection before chunking", "evidence_classification": "configuration defined"},
        {"data_class": "shipment values and billing", "embedding_policy": "restricted", "ai_context_policy": "exclude or redact", "control": "billing status only unless explicit approved use case", "evidence_classification": "configuration defined"},
        {"data_class": "service case notes", "embedding_policy": "may be embedded after sensitivity labeling", "ai_context_policy": "allow when authorized", "control": "prompt-injection handling treats notes as untrusted content", "evidence_classification": "configuration defined"},
    ]


def _audit_catalog() -> list[dict[str, str]]:
    return [
        {"audit_event": "retrieval request", "captured_fields": "request id, identity, filters, top-k, chunk ids, ranks, status, error summary", "excluded_fields": "raw unrestricted prompt or sensitive full payload unless policy permits", "evidence_classification": "configuration defined"},
        {"audit_event": "generation request", "captured_fields": "answer id, model deployment/version, endpoint status, citation ids, status, latency/token placeholders", "excluded_fields": "secrets and unrestricted source payloads", "evidence_classification": "configuration defined"},
    ]


def _failure_handling() -> list[dict[str, str]]:
    modes = [
        ("provider unavailable", "retry with bounded backoff, mark pending, show grounded-unavailable fallback"),
        ("embedding error", "mark failed with error class, preserve source hash, manual retry"),
        ("stale embedding", "exclude stale chunk from retrieval unless emergency policy permits lexical-only fallback"),
        ("dimension mismatch", "fail validation, block retrieval/index rebuild, re-embed with configured dimensions"),
        ("no retrieval", "return insufficiency response with no generated answer"),
        ("model unavailable", "record generation failure and avoid fabricated answer"),
        ("timeout or throttling", "bounded retry, audit status, no hidden replay storm"),
        ("malformed model response", "reject response and record parse failure"),
        ("unsafe or insufficient grounding", "return insufficiency or escalation path"),
        ("suspected data leakage", "disable affected retrieval path, preserve audit, incident runbook"),
    ]
    return [
        {"failure_mode": mode, "handling": handling, "fallback": "grounded insufficiency or manual investigation; no autonomous action", "evidence_classification": "configuration defined"}
        for mode, handling in modes
    ]


def _cost_controls() -> list[dict[str, str]]:
    controls = [
        ("source hash dedupe", "avoid re-embedding unchanged chunks"),
        ("chunk count caps", "bound maximum chunks per document type"),
        ("top-k limits", "cap retrieved context per question"),
        ("question cache boundary", "cache retrieval metadata only when policy allows"),
        ("model change review", "dimension/model changes require explicit re-embedding plan"),
        ("generation token limit", "set maximum generation payload and response size per use case"),
    ]
    return [
        {"control": control, "purpose": purpose, "evidence_classification": "configuration defined"}
        for control, purpose in controls
    ]


def _readiness() -> list[dict[str, str]]:
    return [
        {"capability": "deterministic chunking and evaluation fixtures", "status": "locally validated", "evidence": "tests and outputs/sql_ai/*.csv"},
        {"capability": "SQL vector schema and search examples", "status": "requires Azure SQL validation", "evidence": "src/azure_sql/ai/search/*.sql"},
        {"capability": "SQL AI functions and external model pattern", "status": "requires Azure SQL validation", "evidence": "src/azure_sql/ai/embeddings/*.sql"},
        {"capability": "Azure OpenAI generation boundary", "status": "requires Azure OpenAI validation", "evidence": "src/azure_sql/ai/rag/sql_native_rag_sequence.sql"},
        {"capability": "security, audit, failure, and cost controls", "status": "configuration defined", "evidence": "outputs/sql_ai control matrices"},
    ]


def _report() -> str:
    return "\n".join(
        [
            "# AI-Enabled SQL, Vector Search, Hybrid Retrieval and Database-Native RAG Report",
            "",
            "Milestone 13 defines an implementation-ready, database-centric AI capability for a Customer Service / Shipment Operations Knowledge Assistant. The assistant answers shipment delay, case-note, carrier-update, depot, and route-context questions using grounded retrieval only. It does not make autonomous decisions, write operational state, approve refunds, reroute freight, or answer from model prior knowledge.",
            "",
            "## Architecture",
            "",
            "The target flow is operational and curated data to an AI-ready source projection, deterministic chunking, embedding generation, vector persistence, full-text and vector retrieval, reciprocal-rank-fusion hybrid ranking, context assembly, LLM generation, grounded response, and audit. Refresh follows change detection, stale detection, asynchronous re-embedding, validation, and retirement where required.",
            "",
            "## Local Boundary",
            "",
            "Local validation covers deterministic chunking, hashes, lifecycle status, metadata filtering, RRF ranking fixtures, evaluation metrics, context JSON, security matrices, and evidence classification. Local execution does not call Azure SQL AI functions, create external models, build vector indexes, generate real embeddings, or invoke Azure OpenAI.",
            "",
            "## Target SQL Boundary",
            "",
            "Target-ready SQL assets use `VECTOR(1536)`, `AI_GENERATE_CHUNKS`, `AI_GENERATE_EMBEDDINGS`, `CREATE EXTERNAL MODEL`, `VECTOR_DISTANCE`, `VECTOR_SEARCH`, full-text search, JSON context assembly, and `sp_invoke_external_rest_endpoint` patterns with managed identity placeholders. These assets require validation in a compatible Azure SQL runtime and approved Azure OpenAI environment.",
            "",
            "## Governance",
            "",
            "The implementation treats retrieved content as untrusted, applies authorization and metadata filters before ranking, separates embedding worker permissions from application execution, records retrieval and generation audits, and documents failure, leakage, grounding, and quality regression runbooks.",
            "",
        ]
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate SQL AI/RAG evidence.")
    parser.add_argument("--outputs-dir", type=Path, default=Path("outputs/sql_ai"))
    parser.add_argument("--reports-dir", type=Path, default=Path("reports"))
    args = parser.parse_args()
    written = generate_outputs(args.outputs_dir, args.reports_dir, Path.cwd())
    for name in sorted(written):
        print(f"{name}: {written[name]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
