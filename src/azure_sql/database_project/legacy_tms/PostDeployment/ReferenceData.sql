MERGE dbo.Depot AS target
USING (
    VALUES
        ('LON01', N'London Gateway', 'UK South', 1200, 'GMT Standard Time', 1),
        ('MAN01', N'Manchester North', 'UK North', 850, 'GMT Standard Time', 1),
        ('AMS01', N'Amsterdam Hub', 'West Europe', 1100, 'W. Europe Standard Time', 1),
        ('DUB01', N'Dublin Freight', 'North Europe', 650, 'GMT Standard Time', 1)
) AS source (DepotCode, DepotName, Region, CapacityUnits, TimeZoneName, IsActive)
ON target.DepotCode = source.DepotCode
WHEN MATCHED THEN
    UPDATE SET
        DepotName = source.DepotName,
        Region = source.Region,
        CapacityUnits = source.CapacityUnits,
        TimeZoneName = source.TimeZoneName,
        IsActive = source.IsActive
WHEN NOT MATCHED BY TARGET THEN
    INSERT (DepotCode, DepotName, Region, CapacityUnits, TimeZoneName, IsActive)
    VALUES (source.DepotCode, source.DepotName, source.Region, source.CapacityUnits, source.TimeZoneName, source.IsActive);

GO

MERGE dbo.Route AS target
USING (
    SELECT 'LON-MAN-001', o.DepotId, d.DepotId, 6, 0
    FROM dbo.Depot AS o
    CROSS JOIN dbo.Depot AS d
    WHERE o.DepotCode = 'LON01' AND d.DepotCode = 'MAN01'
    UNION ALL
    SELECT 'MAN-LON-001', o.DepotId, d.DepotId, 6, 0
    FROM dbo.Depot AS o
    CROSS JOIN dbo.Depot AS d
    WHERE o.DepotCode = 'MAN01' AND d.DepotCode = 'LON01'
    UNION ALL
    SELECT 'LON-AMS-001', o.DepotId, d.DepotId, 10, 1
    FROM dbo.Depot AS o
    CROSS JOIN dbo.Depot AS d
    WHERE o.DepotCode = 'LON01' AND d.DepotCode = 'AMS01'
    UNION ALL
    SELECT 'AMS-DUB-001', o.DepotId, d.DepotId, 18, 0
    FROM dbo.Depot AS o
    CROSS JOIN dbo.Depot AS d
    WHERE o.DepotCode = 'AMS01' AND d.DepotCode = 'DUB01'
    UNION ALL
    SELECT 'DUB-LON-001', o.DepotId, d.DepotId, 14, 0
    FROM dbo.Depot AS o
    CROSS JOIN dbo.Depot AS d
    WHERE o.DepotCode = 'DUB01' AND d.DepotCode = 'LON01'
) AS source (RouteCode, OriginDepotId, DestinationDepotId, PlannedHours, IsHazmatEnabled)
ON target.RouteCode = source.RouteCode
WHEN MATCHED THEN
    UPDATE SET
        OriginDepotId = source.OriginDepotId,
        DestinationDepotId = source.DestinationDepotId,
        PlannedHours = source.PlannedHours,
        IsHazmatEnabled = source.IsHazmatEnabled
WHEN NOT MATCHED BY TARGET THEN
    INSERT (RouteCode, OriginDepotId, DestinationDepotId, PlannedHours, IsHazmatEnabled)
    VALUES (source.RouteCode, source.OriginDepotId, source.DestinationDepotId, source.PlannedHours, source.IsHazmatEnabled);

