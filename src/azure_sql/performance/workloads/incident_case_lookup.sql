DECLARE @ShipmentCode varchar(30) = 'SHP000000001';

SELECT
    s.ShipmentCode,
    i.IncidentCode,
    i.IncidentStatus,
    i.IncidentOpenedAtUtc,
    i.IncidentClosedAtUtc
FROM dbo.Shipment s
INNER JOIN dbo.ShipmentIncident i ON s.ShipmentId = i.ShipmentId
WHERE s.ShipmentCode = @ShipmentCode
ORDER BY i.IncidentOpenedAtUtc DESC;

