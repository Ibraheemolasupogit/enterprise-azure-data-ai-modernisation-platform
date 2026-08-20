ALTER TABLE dbo.CustomerAccount
ADD CONSTRAINT PK_CustomerAccount PRIMARY KEY CLUSTERED (CustomerId);

ALTER TABLE dbo.CustomerAccount
ADD CONSTRAINT UQ_CustomerAccount_CustomerCode UNIQUE (CustomerCode);

ALTER TABLE dbo.CustomerAccount
ADD CONSTRAINT CK_CustomerAccount_ServiceTier CHECK (ServiceTier IN ('standard', 'priority', 'critical'));

ALTER TABLE dbo.CustomerAccountAudit
ADD CONSTRAINT PK_CustomerAccountAudit PRIMARY KEY CLUSTERED (AuditId);

ALTER TABLE dbo.CustomerAccountAudit
ADD CONSTRAINT FK_CustomerAccountAudit_CustomerAccount
FOREIGN KEY (CustomerId) REFERENCES dbo.CustomerAccount(CustomerId);

ALTER TABLE dbo.Depot
ADD CONSTRAINT PK_Depot PRIMARY KEY CLUSTERED (DepotId);

ALTER TABLE dbo.Depot
ADD CONSTRAINT UQ_Depot_DepotCode UNIQUE (DepotCode);

ALTER TABLE dbo.Route
ADD CONSTRAINT PK_Route PRIMARY KEY CLUSTERED (RouteId);

ALTER TABLE dbo.Route
ADD CONSTRAINT FK_Route_OriginDepot FOREIGN KEY (OriginDepotId) REFERENCES dbo.Depot(DepotId);

ALTER TABLE dbo.Route
ADD CONSTRAINT FK_Route_DestinationDepot FOREIGN KEY (DestinationDepotId) REFERENCES dbo.Depot(DepotId);

ALTER TABLE dbo.Vehicle
ADD CONSTRAINT PK_Vehicle PRIMARY KEY CLUSTERED (VehicleId);

ALTER TABLE dbo.Vehicle
ADD CONSTRAINT FK_Vehicle_HomeDepot FOREIGN KEY (HomeDepotId) REFERENCES dbo.Depot(DepotId);

ALTER TABLE dbo.Shipment
ADD CONSTRAINT PK_Shipment PRIMARY KEY CLUSTERED (ShipmentId);

ALTER TABLE dbo.Shipment
ADD CONSTRAINT FK_Shipment_CustomerAccount FOREIGN KEY (CustomerId) REFERENCES dbo.CustomerAccount(CustomerId);

ALTER TABLE dbo.Shipment
ADD CONSTRAINT FK_Shipment_Route FOREIGN KEY (RouteId) REFERENCES dbo.Route(RouteId);

ALTER TABLE dbo.ShipmentEventHistory
ADD CONSTRAINT PK_ShipmentEventHistory PRIMARY KEY CLUSTERED (ShipmentEventId);

ALTER TABLE dbo.ShipmentEventHistory
ADD CONSTRAINT FK_ShipmentEventHistory_Shipment FOREIGN KEY (ShipmentId) REFERENCES dbo.Shipment(ShipmentId);

CREATE NONCLUSTERED INDEX IX_Shipment_Customer_Status
ON dbo.Shipment (CustomerId, ShipmentStatus)
INCLUDE (CreatedAtUtc, PromisedDeliveryAtUtc);

CREATE NONCLUSTERED INDEX IX_Shipment_Route_Status_CreatedAt
ON dbo.Shipment (RouteId, ShipmentStatus, CreatedAtUtc)
INCLUDE (PromisedDeliveryAtUtc, DeliveredAtUtc);

CREATE NONCLUSTERED INDEX IX_ShipmentEventHistory_Shipment_Sequence
ON dbo.ShipmentEventHistory (ShipmentId, EventSequence);

