CREATE INDEX [IX_ai_EmbeddingMetadata_WorkQueue]
ON [ai].[EmbeddingMetadata] ([EmbeddingStatus], [RetryCount], [RequestedAt]);
