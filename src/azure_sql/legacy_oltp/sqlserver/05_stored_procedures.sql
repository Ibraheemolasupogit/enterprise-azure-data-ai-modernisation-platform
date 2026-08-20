CREATE PROCEDURE dbo.usp_GetCustomerShipmentSummary
    @CustomerCode varchar(20)
AS
BEGIN
    SET NOCOUNT ON;

    SELECT
        c.CustomerCode,
        c.LegalName,
        s.ShipmentStatus,
        COUNT_BIG(*) AS ShipmentCount,
        SUM(CASE WHEN s.DeliveredAtUtc > s.PromisedDeliveryAtUtc THEN 1 ELSE 0 END) AS LateShipmentCount
    FROM dbo.CustomerAccount c
    INNER JOIN dbo.Shipment s ON c.CustomerId = s.CustomerId
    WHERE c.CustomerCode = @CustomerCode
    GROUP BY c.CustomerCode, c.LegalName, s.ShipmentStatus;
END;

GO

CREATE PROCEDURE dbo.usp_CreateShipment
    @CustomerCode varchar(20),
    @RouteCode varchar(40),
    @ExternalOrderRef varchar(40),
    @DeclaredValueGbp money,
    @HazmatFlag bit
AS
BEGIN
    SET NOCOUNT ON;

    INSERT INTO dbo.Shipment (
        ShipmentCode,
        CustomerId,
        RouteId,
        ExternalOrderRef,
        ShipmentStatus,
        CreatedAtUtc,
        PromisedDeliveryAtUtc,
        DeclaredValueGbp,
        HazmatFlag,
        LegacyOptionsJson
    )
    SELECT
        CONCAT('SHP-', CONVERT(varchar(36), NEWID())),
        c.CustomerId,
        r.RouteId,
        @ExternalOrderRef,
        'created',
        SYSUTCDATETIME(),
        DATEADD(hour, r.PlannedHours + 24, SYSUTCDATETIME()),
        @DeclaredValueGbp,
        @HazmatFlag,
        N'{"source":"legacy-procedure"}'
    FROM dbo.CustomerAccount c
    CROSS JOIN dbo.Route r
    WHERE c.CustomerCode = @CustomerCode
      AND r.RouteCode = @RouteCode;
END;

GO

CREATE PROCEDURE dbo.usp_UpdateShipmentStatus
    @ShipmentCode varchar(30),
    @NewStatus varchar(30),
    @EventPayloadJson nvarchar(max) = NULL
AS
BEGIN
    SET NOCOUNT ON;

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
    FROM dbo.Shipment s
    LEFT JOIN dbo.ShipmentEventHistory e ON s.ShipmentId = e.ShipmentId
    WHERE s.ShipmentCode = @ShipmentCode
    GROUP BY s.ShipmentId;
END;

