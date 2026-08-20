DECLARE @CustomerCode varchar(20) = 'CUST000001';

SELECT
    c.CustomerCode,
    c.LegalName,
    s.ShipmentCode,
    s.ShipmentStatus,
    s.PromisedDeliveryAtUtc
FROM dbo.CustomerAccount c
INNER JOIN dbo.Shipment s ON c.CustomerId = s.CustomerId
WHERE c.CustomerCode = @CustomerCode
  AND s.ShipmentStatus NOT IN ('delivered', 'cancelled')
ORDER BY s.PromisedDeliveryAtUtc;

