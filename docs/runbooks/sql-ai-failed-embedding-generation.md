# SQL AI Failed Embedding Generation

## Trigger

`ai.EmbeddingMetadata.EmbeddingStatus = 'failed'` or repeated worker retries for a pending/stale chunk.

## Response

1. Confirm the failure class and retry count in `ai.EmbeddingMetadata`.
2. Check whether the source chunk is still active and authorized.
3. Verify model name, dimensions, external model configuration, and managed identity access.
4. Retry only after the root cause is corrected.
5. Keep failed chunks excluded from vector retrieval until a current embedding is present.

## Evidence Boundary

Local evidence validates state classification only. Provider and runtime failures require Azure SQL and Azure OpenAI validation.

