CREATE TABLE dbo.CustomerAccountAudit (
    AuditId bigint IDENTITY(1,1) NOT NULL,
    CustomerId int NOT NULL,
    AuditAction varchar(20) NOT NULL,
    AuditPayload nvarchar(max) NULL,
    AuditCreatedAtUtc datetime2(3) NOT NULL,
    CONSTRAINT PK_CustomerAccountAudit PRIMARY KEY CLUSTERED (AuditId),
    CONSTRAINT FK_CustomerAccountAudit_CustomerAccount
        FOREIGN KEY (CustomerId) REFERENCES dbo.CustomerAccount(CustomerId)
);

