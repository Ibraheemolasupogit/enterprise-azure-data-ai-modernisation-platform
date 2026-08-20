# SQL AI Stale Embeddings

## Trigger

Content hash, chunk logic version, embedding model version, or vector dimensions changed.

## Response

1. Mark affected metadata rows as `stale`.
2. Exclude stale vectors from vector retrieval.
3. Enqueue asynchronous re-embedding.
4. Validate dimensions before updating `ai.DocumentChunk.EmbeddingVector`.
5. Record completion or failure in `ai.EmbeddingMetadata`.

## Evidence Boundary

Local tests validate stale detection. Re-embedding requires Azure validation.

