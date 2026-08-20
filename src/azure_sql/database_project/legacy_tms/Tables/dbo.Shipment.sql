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
    RowVersionBytes rowversion NOT NULL,
    CONSTRAINT PK_Shipment PRIMARY KEY CLUSTERED (ShipmentId),
    CONSTRAINT UQ_Shipment_ShipmentCode UNIQUE (ShipmentCode),
    CONSTRAINT FK_Shipment_CustomerAccount FOREIGN KEY (CustomerId) REFERENCES dbo.CustomerAccount(CustomerId),
    CONSTRAINT FK_Shipment_Route FOREIGN KEY (RouteId) REFERENCES dbo.Route(RouteId),
    CONSTRAINT FK_Shipment_Vehicle FOREIGN KEY (AssignedVehicleId) REFERENCES dbo.Vehicle(VehicleId),
    CONSTRAINT CK_Shipment_Status CHECK (ShipmentStatus IN ('created', 'assigned', 'in_transit', 'delayed', 'delivered', 'cancelled'))
);

GO

CREATE NONCLUSTERED INDEX IX_Shipment_Customer_Status
ON dbo.Shipment (CustomerId, ShipmentStatus)
INCLUDE (CreatedAtUtc, PromisedDeliveryAtUtc);

GO

CREATE NONCLUSTERED INDEX IX_Shipment_Route_Status_CreatedAt
ON dbo.Shipment (RouteId, ShipmentStatus, CreatedAtUtc)
INCLUDE (PromisedDeliveryAtUtc, DeliveredAtUtc);

