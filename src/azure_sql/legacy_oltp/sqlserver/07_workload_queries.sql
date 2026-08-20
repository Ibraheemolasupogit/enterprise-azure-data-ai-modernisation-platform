-- OLTP: customer lookup with active shipment summary.
EXEC dbo.usp_GetCustomerShipmentSummary @CustomerCode = 'CUST000001';

-- OLTP: create a shipment through a legacy stored procedure dependency.
EXEC dbo.usp_CreateShipment
    @CustomerCode = 'CUST000001',
    @RouteCode = 'DPN-DPM',
    @ExternalOrderRef = 'ORD-LEGACY-000001',
    @DeclaredValueGbp = 275.50,
    @HazmatFlag = 0;

-- OLTP / CDC candidate: status update writes Shipment and ShipmentEventHistory.
EXEC dbo.usp_UpdateShipmentStatus
    @ShipmentCode = 'SHP-EXAMPLE',
    @NewStatus = 'in_transit',
    @EventPayloadJson = N'{"scanner":"SCN101","status":"in_transit"}';

-- Operational reporting: credible legacy pain point competing with OLTP tables.
SELECT
    d.DepotCode,
    r.RouteCode,
    s.ShipmentStatus,
    COUNT_BIG(*) AS ShipmentCount,
    AVG(DATEDIFF(hour, s.CreatedAtUtc, SYSUTCDATETIME())) AS AverageAgeHours
FROM dbo.Shipment s
INNER JOIN dbo.Route r ON s.RouteId = r.RouteId
INNER JOIN dbo.Depot d ON r.OriginDepotId = d.DepotId
WHERE s.CreatedAtUtc >= DATEADD(day, -30, SYSUTCDATETIME())
GROUP BY d.DepotCode, r.RouteCode, s.ShipmentStatus
ORDER BY ShipmentCount DESC;

