-- Target-ready embedding generation. Do not run from OLTP triggers.
UPDATE c
SET
    c.EmbeddingVector = AI_GENERATE_EMBEDDINGS(c.Content USE MODEL [ai].[shipment_ops_embedding_model]),
    c.UpdatedAt = SYSUTCDATETIME()
FROM ai.DocumentChunk AS c
JOIN ai.EmbeddingMetadata AS m
  ON m.ChunkId = c.ChunkId
WHERE m.EmbeddingStatus IN ('pending', 'stale')
  AND m.Dimensions = 1536
  AND c.LifecycleState = 'active';

