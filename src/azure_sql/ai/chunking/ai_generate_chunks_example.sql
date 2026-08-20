-- Target-ready chunking example. Do not execute locally.
-- Replace arguments with the syntax supported by the selected Azure SQL runtime.
SELECT
    d.DocumentId,
    generated.chunk_ordinal,
    generated.chunk_text,
    HASHBYTES('SHA2_256', CONVERT(VARBINARY(MAX), generated.chunk_text)) AS chunk_hash
FROM ai.Document AS d
CROSS APPLY AI_GENERATE_CHUNKS(
    source => d.Title + CHAR(10) + CONVERT(NVARCHAR(MAX), d.SourceContentHash),
    chunk_type => 'fixed_size',
    chunk_size => 800,
    overlap => 120
) AS generated
WHERE d.LifecycleState = 'active';

