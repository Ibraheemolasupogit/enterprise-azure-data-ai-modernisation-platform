CREATE PROCEDURE dbo.usp_UpdateShipmentStatus
    @ShipmentCode varchar(30),
    @NewStatus varchar(30),
    @EventPayloadJson nvarchar(max) = NULL
AS
BEGIN
    SET NOCOUNT ON;
    SET XACT_ABORT ON;

    BEGIN TRANSACTION;

    UPDATE dbo.Shipment
    SET ShipmentStatus = @NewStatus,
        DeliveredAtUtc = CASE WHEN @NewStatus = 'delivered' THEN SYSUTCDATETIME() ELSE DeliveredAtUtc END
    WHERE ShipmentCode = @ShipmentCode;

    INSERT INTO dbo.ShipmentEventHistory (
        ShipmentId,
        EventSequence,
        EventType,
        EventTimestampUtc,
        SourceSystem,
        EventPayloadJson
    )
    SELECT
        s.ShipmentId,
        ISNULL(MAX(e.EventSequence), 0) + 1,
        @NewStatus,
        SYSUTCDATETIME(),
        'legacy_tms',
        @EventPayloadJson
    FROM dbo.Shipment AS s
    LEFT JOIN dbo.ShipmentEventHistory AS e ON s.ShipmentId = e.ShipmentId
    WHERE s.ShipmentCode = @ShipmentCode
    GROUP BY s.ShipmentId;

    COMMIT TRANSACTION;
END;

