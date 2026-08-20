-- Before: route/depot reporting relies on broad date/status aggregation over Shipment.
-- After: validate the focused migration-readiness index below with Query Store and actual plans.

CREATE NONCLUSTERED INDEX IX_Shipment_Route_Status_CreatedAt
ON dbo.Shipment (RouteId, ShipmentStatus, CreatedAtUtc)
INCLUDE (PromisedDeliveryAtUtc, DeliveredAtUtc);

-- Review write overhead and usage before keeping this index permanently.

