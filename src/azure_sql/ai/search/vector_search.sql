-- Target-ready vector retrieval examples. Requires Azure SQL vector support.
DECLARE @QuestionEmbedding VECTOR(1536);

SELECT TOP (10)
    c.ChunkId,
    c.DocumentId,
    VECTOR_DISTANCE('cosine', c.EmbeddingVector, @QuestionEmbedding) AS distance
FROM ai.DocumentChunk AS c
WHERE c.LifecycleState = 'active'
  AND c.SensitivityLabel <> 'restricted'
ORDER BY VECTOR_DISTANCE('cosine', c.EmbeddingVector, @QuestionEmbedding);

SELECT TOP (10) WITH APPROXIMATE
    c.ChunkId,
    c.DocumentId,
    vs.distance
FROM VECTOR_SEARCH(
    TABLE = ai.DocumentChunk AS c,
    COLUMN = EmbeddingVector,
    SIMILAR_TO = @QuestionEmbedding,
    METRIC = 'cosine'
) AS vs;

-- Vector index configuration boundary:
-- target table ai.DocumentChunk, column EmbeddingVector, dimensions 1536,
-- distance cosine, algorithm DiskANN/vector index where supported,
-- rebuild after model or dimension change.
