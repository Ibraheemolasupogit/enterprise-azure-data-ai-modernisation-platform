-- Target-ready lexical retrieval. Full-text catalog/index creation requires Azure SQL validation.
CREATE FULLTEXT CATALOG [ft_ai_document_chunk] AS DEFAULT;

CREATE FULLTEXT INDEX ON [ai].[DocumentChunk]([Content] LANGUAGE 1033)
KEY INDEX [PK_ai_DocumentChunk]
WITH CHANGE_TRACKING AUTO;

DECLARE @Question NVARCHAR(4000) = N'"missed line haul" OR carrier OR delay';

SELECT TOP (10)
    c.ChunkId,
    c.DocumentId,
    ft.[RANK] AS lexical_rank
FROM CONTAINSTABLE([ai].[DocumentChunk], [Content], @Question) AS ft
JOIN [ai].[DocumentChunk] AS c
  ON c.ChunkId = ft.[KEY]
WHERE c.LifecycleState = 'active'
  AND c.SensitivityLabel <> 'restricted';

