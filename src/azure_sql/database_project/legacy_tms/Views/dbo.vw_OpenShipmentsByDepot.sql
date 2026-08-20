CREATE VIEW dbo.vw_OpenShipmentsByDepot
AS
SELECT
    d.DepotCode,
    d.DepotName,
    r.RouteCode,
    s.ShipmentStatus,
    COUNT_BIG(*) AS OpenShipmentCount,
    MIN(s.CreatedAtUtc) AS OldestOpenShipmentCreatedAtUtc
FROM dbo.Shipment AS s
INNER JOIN dbo.Route AS r ON s.RouteId = r.RouteId
INNER JOIN dbo.Depot AS d ON r.OriginDepotId = d.DepotId
WHERE s.ShipmentStatus IN ('created', 'assigned', 'in_transit', 'delayed')
GROUP BY d.DepotCode, d.DepotName, r.RouteCode, s.ShipmentStatus;

