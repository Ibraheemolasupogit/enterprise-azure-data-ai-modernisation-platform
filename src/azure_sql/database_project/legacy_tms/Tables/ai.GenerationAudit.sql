CREATE TABLE [ai].[GenerationAudit]
(
    [GenerationAuditId] UNIQUEIDENTIFIER NOT NULL CONSTRAINT [DF_ai_GenerationAudit_Id] DEFAULT NEWID(),
    [RetrievalAuditId] UNIQUEIDENTIFIER NOT NULL,
    [GeneratedAt] DATETIME2(3) NOT NULL CONSTRAINT [DF_ai_GenerationAudit_GeneratedAt] DEFAULT SYSUTCDATETIME(),
    [RequestingPrincipal] SYSNAME NOT NULL,
    [ModelDeployment] NVARCHAR(128) NOT NULL,
    [ModelVersion] NVARCHAR(80) NULL,
    [EndpointName] NVARCHAR(128) NOT NULL,
    [PromptContractVersion] NVARCHAR(80) NOT NULL,
    [CitationChunkIdsJson] NVARCHAR(MAX) NOT NULL,
    [AnswerHash] CHAR(64) NULL,
    [Status] NVARCHAR(30) NOT NULL,
    [LatencyMs] INT NULL,
    [PromptTokens] INT NULL,
    [CompletionTokens] INT NULL,
    [ErrorClass] NVARCHAR(120) NULL,
    [ErrorSummary] NVARCHAR(400) NULL,
    CONSTRAINT [PK_ai_GenerationAudit] PRIMARY KEY CLUSTERED ([GenerationAuditId]),
    CONSTRAINT [FK_ai_GenerationAudit_RetrievalAudit] FOREIGN KEY ([RetrievalAuditId]) REFERENCES [ai].[RetrievalAudit] ([RetrievalAuditId]),
    CONSTRAINT [CK_ai_GenerationAudit_Status] CHECK ([Status] IN ('succeeded', 'insufficient_context', 'failed', 'blocked'))
);

