CREATE OR ALTER PROCEDURE dbo.usp_GetCustomerShipmentSummaryByTier
    @ServiceTier varchar(20)
AS
BEGIN
    SET NOCOUNT ON;

    SELECT
        c.ServiceTier,
        c.CustomerCode,
        COUNT_BIG(*) AS ShipmentCount,
        SUM(CASE WHEN s.ShipmentStatus = 'delayed' THEN 1 ELSE 0 END) AS DelayedShipmentCount
    FROM dbo.CustomerAccount c
    INNER JOIN dbo.Shipment s ON c.CustomerId = s.CustomerId
    WHERE c.ServiceTier = @ServiceTier
    GROUP BY c.ServiceTier, c.CustomerCode
    ORDER BY ShipmentCount DESC;
END;

-- Critical-tier customers may be a small, high-value subset while standard customers are broad.
-- Investigate skew through Query Store runtime stats before using plan forcing, Query Store hints,
-- OPTION(RECOMPILE), or parameter-sensitive plan features where available.

