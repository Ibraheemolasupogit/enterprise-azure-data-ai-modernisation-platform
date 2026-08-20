-- Target-ready AI schema assets. Requires Azure SQL vector runtime validation.
-- The database project contains equivalent persistent objects for deployment review.
SELECT
    'ai.Document, ai.DocumentChunk, ai.EmbeddingMetadata, ai.RetrievalAudit, ai.GenerationAudit' AS objects_defined,
    'DocumentChunk.EmbeddingVector VECTOR(1536)' AS vector_column,
    'configuration defined; requires Azure SQL validation' AS evidence_boundary;

