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

