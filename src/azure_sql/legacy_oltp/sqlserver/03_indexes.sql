CREATE NONCLUSTERED INDEX IX_Shipment_Customer_Status
ON dbo.Shipment (CustomerId, ShipmentStatus)
INCLUDE (CreatedAtUtc, PromisedDeliveryAtUtc);

CREATE NONCLUSTERED INDEX IX_Shipment_CreatedAt
ON dbo.Shipment (CreatedAtUtc);

CREATE NONCLUSTERED INDEX IX_ShipmentEventHistory_Shipment_Sequence
ON dbo.ShipmentEventHistory (ShipmentId, EventSequence);

CREATE NONCLUSTERED INDEX IX_ShipmentEventHistory_EventTimestamp
ON dbo.ShipmentEventHistory (EventTimestampUtc);

CREATE NONCLUSTERED INDEX IX_Vehicle_HomeDepot
ON dbo.Vehicle (HomeDepotId, IsActive);

-- Credible legacy pain point: operational reporting filters by route/depot/status,
-- but the estate lacks a covering index for that access pattern.
-- Future assessment should decide whether to add one or move the workload analytically.

