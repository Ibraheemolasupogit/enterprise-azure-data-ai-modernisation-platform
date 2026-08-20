SELECT
    r.RouteCode,
    COUNT_BIG(*) AS DeliveredShipmentCount,
    SUM(CASE WHEN s.DeliveredAtUtc > s.PromisedDeliveryAtUtc THEN 1 ELSE 0 END) AS LateShipmentCount,
    AVG(DATEDIFF(hour, s.PromisedDeliveryAtUtc, s.DeliveredAtUtc)) AS AverageDelayHours
FROM dbo.Shipment s
INNER JOIN dbo.Route r ON s.RouteId = r.RouteId
WHERE s.ShipmentStatus = 'delivered'
  AND s.DeliveredAtUtc >= DATEADD(day, -90, SYSUTCDATETIME())
GROUP BY r.RouteCode
ORDER BY LateShipmentCount DESC;

