CREATE TABLE [ai].[RetrievalAudit]
(
    [RetrievalAuditId] UNIQUEIDENTIFIER NOT NULL CONSTRAINT [DF_ai_RetrievalAudit_Id] DEFAULT NEWID(),
    [RequestedAt] DATETIME2(3) NOT NULL CONSTRAINT [DF_ai_RetrievalAudit_RequestedAt] DEFAULT SYSUTCDATETIME(),
    [RequestingPrincipal] NVARCHAR(128) NOT NULL,
    [QuestionHash] CHAR(64) NOT NULL,
    [ShipmentId] NVARCHAR(40) NULL,
    [AccountId] NVARCHAR(40) NULL,
    [FiltersJson] NVARCHAR(MAX) NOT NULL,
    [TopK] INT NOT NULL,
    [RetrievalMode] NVARCHAR(40) NOT NULL,
    [RetrievedChunksJson] NVARCHAR(MAX) NULL,
    [Status] NVARCHAR(30) NOT NULL,
    [ErrorClass] NVARCHAR(120) NULL,
    [ErrorSummary] NVARCHAR(400) NULL,
    [LatencyMs] INT NULL,
    CONSTRAINT [PK_ai_RetrievalAudit] PRIMARY KEY CLUSTERED ([RetrievalAuditId]),
    CONSTRAINT [CK_ai_RetrievalAudit_Status] CHECK ([Status] IN ('succeeded', 'insufficient_context', 'failed', 'blocked'))
);
