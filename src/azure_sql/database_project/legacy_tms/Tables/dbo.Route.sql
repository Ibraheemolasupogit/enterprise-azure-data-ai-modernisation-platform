CREATE TABLE dbo.Route (
    RouteId int IDENTITY(1,1) NOT NULL,
    RouteCode varchar(40) NOT NULL,
    OriginDepotId int NOT NULL,
    DestinationDepotId int NOT NULL,
    PlannedHours int NOT NULL,
    IsHazmatEnabled bit NOT NULL CONSTRAINT DF_Route_IsHazmatEnabled DEFAULT (0),
    CONSTRAINT PK_Route PRIMARY KEY CLUSTERED (RouteId),
    CONSTRAINT FK_Route_OriginDepot FOREIGN KEY (OriginDepotId) REFERENCES dbo.Depot(DepotId),
    CONSTRAINT FK_Route_DestinationDepot FOREIGN KEY (DestinationDepotId) REFERENCES dbo.Depot(DepotId)
);

