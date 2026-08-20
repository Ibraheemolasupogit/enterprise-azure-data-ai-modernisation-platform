# SQL AI Vector Dimension Mismatch

## Trigger

Embedding dimensions do not match `ai.DocumentChunk.EmbeddingVector` or vector index configuration.

## Response

1. Stop embedding writes and vector retrieval for the affected model/version.
2. Confirm configured dimensions in the external model, metadata, vector column, and index definition.
3. Do not coerce or truncate vectors.
4. Re-embed with the approved dimensions and rebuild vector index assets where supported.
5. Re-run SQL AI validation and retrieval evaluation.

## Evidence Boundary

Dimension checks are configuration-defined locally. Runtime vector enforcement requires Azure SQL validation.

