CREATE TABLE [ai].[Document]
(
    [DocumentId] NVARCHAR(80) NOT NULL,
    [SourceSystem] NVARCHAR(80) NOT NULL,
    [DocumentType] NVARCHAR(60) NOT NULL,
    [Title] NVARCHAR(200) NOT NULL,
    [SourceUri] NVARCHAR(400) NULL,
    [ShipmentId] NVARCHAR(40) NULL,
    [AccountId] NVARCHAR(40) NULL,
    [DepotCode] NVARCHAR(20) NULL,
    [RouteCode] NVARCHAR(40) NULL,
    [SensitivityLabel] NVARCHAR(40) NOT NULL,
    [LifecycleState] NVARCHAR(20) NOT NULL,
    [SourceUpdatedAt] DATETIME2(3) NOT NULL,
    [SourceContentHash] CHAR(64) NOT NULL,
    [CreatedAt] DATETIME2(3) NOT NULL CONSTRAINT [DF_ai_Document_CreatedAt] DEFAULT SYSUTCDATETIME(),
    [UpdatedAt] DATETIME2(3) NOT NULL CONSTRAINT [DF_ai_Document_UpdatedAt] DEFAULT SYSUTCDATETIME(),
    CONSTRAINT [PK_ai_Document] PRIMARY KEY CLUSTERED ([DocumentId]),
    CONSTRAINT [CK_ai_Document_LifecycleState] CHECK ([LifecycleState] IN ('active', 'retired', 'pending', 'failed')),
    CONSTRAINT [CK_ai_Document_SensitivityLabel] CHECK ([SensitivityLabel] IN ('public', 'internal', 'confidential', 'restricted'))
);

CREATE INDEX [IX_ai_Document_ShipmentAccount]
ON [ai].[Document] ([ShipmentId], [AccountId], [LifecycleState], [SensitivityLabel]);

