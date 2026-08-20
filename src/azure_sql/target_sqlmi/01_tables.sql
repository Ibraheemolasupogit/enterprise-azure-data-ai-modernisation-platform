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
    IsActive bit NOT NULL CONSTRAINT DF_CustomerAccount_IsActive DEFAULT (1)
);

CREATE TABLE dbo.CustomerAccountAudit (
    AuditId bigint IDENTITY(1,1) NOT NULL,
    CustomerId int NOT NULL,
    AuditAction varchar(20) NOT NULL,
    AuditPayload nvarchar(max) NULL,
    AuditCreatedAtUtc datetime2(3) NOT NULL
);

CREATE TABLE dbo.Depot (
    DepotId int IDENTITY(1,1) NOT NULL,
    DepotCode varchar(12) NOT NULL,
    DepotName nvarchar(120) NOT NULL,
    Region varchar(40) NOT NULL,
    CapacityUnits int NULL,
    TimeZoneName varchar(80) NOT NULL,
    IsActive bit NOT NULL
);

CREATE TABLE dbo.Route (
    RouteId int IDENTITY(1,1) NOT NULL,
    RouteCode varchar(40) NOT NULL,
    OriginDepotId int NOT NULL,
    DestinationDepotId int NOT NULL,
    PlannedHours int NOT NULL,
    IsHazmatEnabled bit NOT NULL
);

CREATE TABLE dbo.Vehicle (
    VehicleId int IDENTITY(1,1) NOT NULL,
    VehicleCode varchar(20) NOT NULL,
    HomeDepotId int NOT NULL,
    RegistrationNumber varchar(20) NOT NULL,
    VehicleType varchar(30) NOT NULL,
    TelematicsDeviceId varchar(40) NULL,
    InServiceDate date NOT NULL,
    IsActive bit NOT NULL
);

CREATE TABLE dbo.Shipment (
    ShipmentId bigint IDENTITY(1,1) NOT NULL,
    ShipmentCode varchar(30) NOT NULL,
    CustomerId int NOT NULL,
    RouteId int NOT NULL,
    AssignedVehicleId int NULL,
    ExternalOrderRef varchar(40) NOT NULL,
    ShipmentStatus varchar(30) NOT NULL,
    CreatedAtUtc datetime2(3) NOT NULL,
    PromisedDeliveryAtUtc datetime2(3) NOT NULL,
    DeliveredAtUtc datetime2(3) NULL,
    DeclaredValueGbp money NOT NULL,
    HazmatFlag bit NOT NULL,
    LegacyOptionsJson nvarchar(max) NULL,
    RowVersionBytes rowversion NOT NULL
);

CREATE TABLE dbo.ShipmentEventHistory (
    ShipmentEventId bigint IDENTITY(1,1) NOT NULL,
    ShipmentId bigint NOT NULL,
    EventSequence int NOT NULL,
    EventType varchar(40) NOT NULL,
    EventTimestampUtc datetime2(3) NOT NULL,
    SourceSystem varchar(40) NOT NULL,
    EventPayloadJson nvarchar(max) NULL
);

