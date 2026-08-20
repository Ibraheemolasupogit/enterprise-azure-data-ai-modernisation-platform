# AI-Enabled SQL, Vector Search, Hybrid Retrieval and Database-Native RAG Report

Milestone 13 defines an implementation-ready, database-centric AI capability for a Customer Service / Shipment Operations Knowledge Assistant. The assistant answers shipment delay, case-note, carrier-update, depot, and route-context questions using grounded retrieval only. It does not make autonomous decisions, write operational state, approve refunds, reroute freight, or answer from model prior knowledge.

## Architecture

The target flow is operational and curated data to an AI-ready source projection, deterministic chunking, embedding generation, vector persistence, full-text and vector retrieval, reciprocal-rank-fusion hybrid ranking, context assembly, LLM generation, grounded response, and audit. Refresh follows change detection, stale detection, asynchronous re-embedding, validation, and retirement where required.

## Local Boundary

Local validation covers deterministic chunking, hashes, lifecycle status, metadata filtering, RRF ranking fixtures, evaluation metrics, context JSON, security matrices, and evidence classification. Local execution does not call Azure SQL AI functions, create external models, build vector indexes, generate real embeddings, or invoke Azure OpenAI.

## Target SQL Boundary

Target-ready SQL assets use `VECTOR(1536)`, `AI_GENERATE_CHUNKS`, `AI_GENERATE_EMBEDDINGS`, `CREATE EXTERNAL MODEL`, `VECTOR_DISTANCE`, `VECTOR_SEARCH`, full-text search, JSON context assembly, and `sp_invoke_external_rest_endpoint` patterns with managed identity placeholders. These assets require validation in a compatible Azure SQL runtime and approved Azure OpenAI environment.

## Governance

The implementation treats retrieved content as untrusted, applies authorization and metadata filters before ranking, separates embedding worker permissions from application execution, records retrieval and generation audits, and documents failure, leakage, grounding, and quality regression runbooks.
