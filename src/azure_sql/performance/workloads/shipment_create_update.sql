EXEC dbo.usp_CreateShipment
    @CustomerCode = 'CUST000001',
    @RouteCode = 'DPN-DPM',
    @ExternalOrderRef = 'ORD-PERF-000001',
    @DeclaredValueGbp = 275.50,
    @HazmatFlag = 0;

EXEC dbo.usp_UpdateShipmentStatus
    @ShipmentCode = 'SHP-PERF-000001',
    @NewStatus = 'in_transit',
    @EventPayloadJson = N'{"scanner":"SCN901","status":"in_transit"}';

