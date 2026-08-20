-- Hybrid retrieval with reciprocal rank fusion. No arbitrary learned weights.
WITH lexical AS
(
    SELECT c.ChunkId, ROW_NUMBER() OVER (ORDER BY ft.[RANK] DESC, c.ChunkId) AS rank_position
    FROM CONTAINSTABLE([ai].[DocumentChunk], [Content], @QuestionText) AS ft
    JOIN ai.DocumentChunk AS c ON c.ChunkId = ft.[KEY]
    WHERE c.ShipmentId = @ShipmentId AND c.AccountId = @AccountId
),
vector AS
(
    SELECT c.ChunkId,
           ROW_NUMBER() OVER (ORDER BY VECTOR_DISTANCE('cosine', c.EmbeddingVector, @QuestionEmbedding), c.ChunkId) AS rank_position
    FROM ai.DocumentChunk AS c
    WHERE c.ShipmentId = @ShipmentId
      AND c.AccountId = @AccountId
      AND c.LifecycleState = 'active'
      AND c.SensitivityLabel <> 'restricted'
),
rrf AS
(
    SELECT ChunkId, SUM(1.0 / (60 + rank_position)) AS rrf_score
    FROM (
        SELECT ChunkId, rank_position FROM lexical
        UNION ALL
        SELECT ChunkId, rank_position FROM vector
    ) AS ranks
    GROUP BY ChunkId
)
SELECT TOP (@TopK) ChunkId, rrf_score
FROM rrf
ORDER BY rrf_score DESC, ChunkId;

