CREATE VIEW dbo.vw_OpenShipmentsByDepot
AS
SELECT
    d.DepotCode,
    d.DepotName,
    r.RouteCode,
    s.ShipmentStatus,
    COUNT_BIG(*) AS OpenShipmentCount,
    MIN(s.CreatedAtUtc) AS OldestCreatedAtUtc,
    MAX(s.PromisedDeliveryAtUtc) AS LatestPromisedDeliveryAtUtc
FROM dbo.Shipment s
INNER JOIN dbo.Route r ON s.RouteId = r.RouteId
INNER JOIN dbo.Depot d ON r.OriginDepotId = d.DepotId
WHERE s.ShipmentStatus NOT IN ('delivered', 'cancelled')
GROUP BY d.DepotCode, d.DepotName, r.RouteCode, s.ShipmentStatus;

GO

CREATE VIEW dbo.vw_CustomerServiceSnapshot
AS
SELECT
    c.CustomerCode,
    c.AccountNumber,
    c.LegalName,
    s.ShipmentCode,
    s.ExternalOrderRef,
    s.ShipmentStatus,
    s.PromisedDeliveryAtUtc,
    s.DeliveredAtUtc,
    s.LegacyOptionsJson
FROM dbo.CustomerAccount c
INNER JOIN dbo.Shipment s ON c.CustomerId = s.CustomerId;

