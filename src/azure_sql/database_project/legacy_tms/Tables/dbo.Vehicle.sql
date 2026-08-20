CREATE TABLE dbo.Vehicle (
    VehicleId int IDENTITY(1,1) NOT NULL,
    VehicleCode varchar(20) NOT NULL,
    HomeDepotId int NOT NULL,
    RegistrationNumber varchar(20) NOT NULL,
    VehicleType varchar(30) NOT NULL,
    TelematicsDeviceId varchar(40) NULL,
    InServiceDate date NOT NULL,
    IsActive bit NOT NULL CONSTRAINT DF_Vehicle_IsActive DEFAULT (1),
    CONSTRAINT PK_Vehicle PRIMARY KEY CLUSTERED (VehicleId),
    CONSTRAINT UQ_Vehicle_VehicleCode UNIQUE (VehicleCode),
    CONSTRAINT FK_Vehicle_HomeDepot FOREIGN KEY (HomeDepotId) REFERENCES dbo.Depot(DepotId)
);

