CREATE TABLE dbo.ShipmentEventHistory (
    ShipmentEventId bigint IDENTITY(1,1) NOT NULL,
    ShipmentId bigint NOT NULL,
    EventSequence int NOT NULL,
    EventType varchar(40) NOT NULL,
    EventTimestampUtc datetime2(3) NOT NULL,
    SourceSystem varchar(40) NOT NULL,
    EventPayloadJson nvarchar(max) NULL,
    CONSTRAINT PK_ShipmentEventHistory PRIMARY KEY CLUSTERED (ShipmentEventId),
    CONSTRAINT UQ_ShipmentEventHistory_Shipment_Sequence UNIQUE (ShipmentId, EventSequence),
    CONSTRAINT FK_ShipmentEventHistory_Shipment FOREIGN KEY (ShipmentId) REFERENCES dbo.Shipment(ShipmentId)
);

GO

CREATE NONCLUSTERED INDEX IX_ShipmentEventHistory_Shipment_Sequence
ON dbo.ShipmentEventHistory (ShipmentId, EventSequence);

