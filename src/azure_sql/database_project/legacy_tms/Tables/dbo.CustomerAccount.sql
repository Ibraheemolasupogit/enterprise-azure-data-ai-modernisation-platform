CREATE TABLE dbo.CustomerAccount (
    CustomerId int IDENTITY(1,1) NOT NULL,
    CustomerCode varchar(20) NOT NULL,
    AccountNumber varchar(30) NOT NULL,
    LegalName nvarchar(200) NOT NULL,
    ServiceTier varchar(20) NOT NULL,
    BillingRegion varchar(40) NOT NULL,
    ContactEmail nvarchar(256) NULL,
    LegacyCustomerMemo nvarchar(max) NULL,
    CreatedAtUtc datetime2(3) NOT NULL,
    IsActive bit NOT NULL CONSTRAINT DF_CustomerAccount_IsActive DEFAULT (1),
    CONSTRAINT PK_CustomerAccount PRIMARY KEY CLUSTERED (CustomerId),
    CONSTRAINT UQ_CustomerAccount_CustomerCode UNIQUE (CustomerCode),
    CONSTRAINT CK_CustomerAccount_ServiceTier CHECK (ServiceTier IN ('standard', 'priority', 'critical'))
);

