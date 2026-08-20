CREATE VIEW dbo.vw_CustomerServiceSnapshot
AS
SELECT
    c.CustomerCode,
    c.LegalName,
    c.ServiceTier,
    s.ShipmentCode,
    s.ShipmentStatus,
    s.PromisedDeliveryAtUtc,
    s.DeliveredAtUtc,
    r.RouteCode
FROM dbo.CustomerAccount AS c
INNER JOIN dbo.Shipment AS s ON c.CustomerId = s.CustomerId
INNER JOIN dbo.Route AS r ON s.RouteId = r.RouteId
WHERE c.IsActive = 1;

