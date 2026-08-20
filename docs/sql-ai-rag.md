# AI-Enabled SQL, Vector Search and Database-Native RAG

Milestone 13 adds a database-centric AI capability for the Customer Service / Shipment Operations Knowledge Assistant. The assistant answers grounded questions about shipment status, delay causes, case notes, carrier updates, depot context, and route context. It does not make autonomous decisions, approve refunds, reroute shipments, or write operational state.

## Data Flow

1. Operational and curated data is projected into AI-ready shipment, carrier, case, depot, and route documents.
2. Documents are registered in `ai.Document`.
3. Deterministic chunks are written to `ai.DocumentChunk`.
4. Embedding metadata is tracked in `ai.EmbeddingMetadata`.
5. Embeddings are generated asynchronously through `AI_GENERATE_EMBEDDINGS` or an approved Azure OpenAI external model boundary.
6. Vector and full-text retrieval run with shipment, account, depot, route, date, document type, sensitivity, lifecycle, and authorization filters.
7. Hybrid ranking uses reciprocal rank fusion over lexical and vector ranks.
8. SQL assembles context JSON with source citations.
9. Generation is invoked through an approved outbound Azure OpenAI boundary.
10. Retrieval and generation events are recorded in `ai.RetrievalAudit` and `ai.GenerationAudit`.

Refresh follows change detection, stale detection, pending re-embedding, validation, and retirement. AI calls are not made in OLTP triggers.

## Local vs Azure Boundary

Local validation covers deterministic chunking, hashing, stale-state detection, metadata filters, RRF fixtures, Precision@K, Recall@K, MRR, context JSON, and evidence classification.

Azure SQL validation is required for `VECTOR(1536)`, full-text catalog/index creation, `VECTOR_DISTANCE`, `VECTOR_SEARCH`, vector index/DiskANN behavior where supported, `AI_GENERATE_CHUNKS`, `AI_GENERATE_EMBEDDINGS`, `CREATE EXTERNAL MODEL`, and `sp_invoke_external_rest_endpoint`.

Azure OpenAI validation is required for real embeddings, chat generation, endpoint authorization, timeout behavior, token accounting, response parsing, and model-version evidence.

## Security and Governance

Retrieved content is untrusted. The prompt contract instructs the model to use only supplied context, cite sources, and state insufficiency when context does not support an answer. The SQL path applies authorization filters before ranking to reduce cross-customer exposure.

Roles are separated:

- `ai_app_executor` executes approved context/RAG procedures.
- `ai_data_curator` manages source and chunk metadata.
- `embedding_worker_identity` generates or refreshes embeddings.
- `ai_auditor` reviews audit metadata without unrestricted payload access.

Sensitive data controls exclude or redact contact information, shipment values, and billing details from AI context unless an approved use case explicitly permits them. Service notes may be embedded only after sensitivity labeling and prompt-injection handling.

## Evaluation

The deterministic evaluation dataset in `outputs/sql_ai/retrieval_evaluation_dataset.csv` maps shipment-operations questions to expected chunks. `outputs/sql_ai/retrieval_evaluation_results.csv` reports Precision@K, Recall@K, and MRR from local simulated rankings. These results prove deterministic retrieval plumbing only; they are not live embedding quality or performance claims.

