CREATE TABLE dbo.Depot (
    DepotId int IDENTITY(1,1) NOT NULL,
    DepotCode varchar(12) NOT NULL,
    DepotName nvarchar(120) NOT NULL,
    Region varchar(40) NOT NULL,
    CapacityUnits int NULL,
    TimeZoneName varchar(80) NOT NULL,
    IsActive bit NOT NULL CONSTRAINT DF_Depot_IsActive DEFAULT (1),
    CONSTRAINT PK_Depot PRIMARY KEY CLUSTERED (DepotId),
    CONSTRAINT UQ_Depot_DepotCode UNIQUE (DepotCode)
);

