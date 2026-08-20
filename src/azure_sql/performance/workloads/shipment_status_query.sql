DECLARE @ShipmentCode varchar(30) = 'SHP000000001';

SELECT
    s.ShipmentCode,
    s.ShipmentStatus,
    e.EventSequence,
    e.EventType,
    e.EventTimestampUtc
FROM dbo.Shipment s
LEFT JOIN dbo.ShipmentEventHistory e ON s.ShipmentId = e.ShipmentId
WHERE s.ShipmentCode = @ShipmentCode
ORDER BY e.EventSequence DESC;

