CREATE PROCEDURE dbo.usp_CreateShipment
    @CustomerCode varchar(20),
    @RouteCode varchar(40),
    @ExternalOrderRef varchar(40),
    @DeclaredValueGbp money,
    @HazmatFlag bit
AS
BEGIN
    SET NOCOUNT ON;
    SET XACT_ABORT ON;

    BEGIN TRANSACTION;

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
        N'{"source":"database-project"}'
    FROM dbo.CustomerAccount AS c
    INNER JOIN dbo.Route AS r ON r.RouteCode = @RouteCode
    WHERE c.CustomerCode = @CustomerCode;

    COMMIT TRANSACTION;
END;

