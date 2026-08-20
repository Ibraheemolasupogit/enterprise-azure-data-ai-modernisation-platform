CREATE TABLE [ai].[EmbeddingMetadata]
(
    [EmbeddingMetadataId] BIGINT IDENTITY(1,1) NOT NULL,
    [ChunkId] NVARCHAR(80) NOT NULL,
    [Provider] NVARCHAR(80) NOT NULL,
    [ExternalModelName] NVARCHAR(128) NOT NULL,
    [ModelName] NVARCHAR(128) NOT NULL,
    [ModelVersion] NVARCHAR(80) NOT NULL,
    [Dimensions] INT NOT NULL,
    [DistanceMetric] NVARCHAR(30) NOT NULL,
    [SourceContentHash] CHAR(64) NOT NULL,
    [ChunkLogicVersion] NVARCHAR(80) NOT NULL,
    [LifecycleState] NVARCHAR(20) NOT NULL,
    [EmbeddingStatus] NVARCHAR(20) NOT NULL,
    [RetryCount] INT NOT NULL CONSTRAINT [DF_ai_EmbeddingMetadata_RetryCount] DEFAULT 0,
    [LastErrorClass] NVARCHAR(120) NULL,
    [LastErrorSummary] NVARCHAR(400) NULL,
    [RequestedAt] DATETIME2(3) NOT NULL CONSTRAINT [DF_ai_EmbeddingMetadata_RequestedAt] DEFAULT SYSUTCDATETIME(),
    [EmbeddedAt] DATETIME2(3) NULL,
    CONSTRAINT [PK_ai_EmbeddingMetadata] PRIMARY KEY CLUSTERED ([EmbeddingMetadataId]),
    CONSTRAINT [FK_ai_EmbeddingMetadata_Chunk] FOREIGN KEY ([ChunkId]) REFERENCES [ai].[DocumentChunk] ([ChunkId]),
    CONSTRAINT [CK_ai_EmbeddingMetadata_State] CHECK ([LifecycleState] IN ('current', 'stale', 'pending', 'failed', 'retired')),
    CONSTRAINT [CK_ai_EmbeddingMetadata_Status] CHECK ([EmbeddingStatus] IN ('current', 'stale', 'pending', 'failed', 'retired')),
    CONSTRAINT [CK_ai_EmbeddingMetadata_Dimensions] CHECK ([Dimensions] > 0)
);

CREATE INDEX [IX_ai_EmbeddingMetadata_WorkQueue]
ON [ai].[EmbeddingMetadata] ([EmbeddingStatus], [RetryCount], [RequestedAt]);

