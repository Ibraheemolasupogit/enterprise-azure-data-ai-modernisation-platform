INSERT INTO dbo.Depot (DepotCode, DepotName, Region, CapacityUnits, TimeZoneName, IsActive)
VALUES
    ('DPN', N'Newcastle Depot', 'north', 400, 'Europe/London', 1),
    ('DPM', N'Manchester Depot', 'north', 475, 'Europe/London', 1),
    ('DPB', N'Birmingham Depot', 'midlands', 550, 'Europe/London', 1),
    ('DPL', N'London Gateway Depot', 'south', 625, 'Europe/London', 1);

INSERT INTO dbo.Route (RouteCode, OriginDepotId, DestinationDepotId, PlannedHours, IsHazmatEnabled)
SELECT 'DPN-DPM', o.DepotId, d.DepotId, 4, 1
FROM dbo.Depot o
CROSS JOIN dbo.Depot d
WHERE o.DepotCode = 'DPN' AND d.DepotCode = 'DPM';

INSERT INTO dbo.Route (RouteCode, OriginDepotId, DestinationDepotId, PlannedHours, IsHazmatEnabled)
SELECT 'DPM-DPL', o.DepotId, d.DepotId, 9, 0
FROM dbo.Depot o
CROSS JOIN dbo.Depot d
WHERE o.DepotCode = 'DPM' AND d.DepotCode = 'DPL';

