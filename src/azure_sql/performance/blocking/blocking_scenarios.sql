-- Scenario A: blocked reader/writer
-- Session 1:
-- BEGIN TRAN;
-- UPDATE dbo.Shipment SET ShipmentStatus = 'delayed' WHERE ShipmentCode = 'SHP000000001';
-- WAITFOR DELAY '00:02:00';
-- ROLLBACK;
--
-- Session 2:
-- SELECT * FROM dbo.Shipment WHERE ShipmentCode = 'SHP000000001';

-- Scenario B: writer/writer contention
-- Session 1 updates a shipment and holds the transaction.
-- Session 2 executes dbo.usp_UpdateShipmentStatus for the same shipment.

-- Scenario C: sleeping open transaction
-- Session opens a transaction, touches ShipmentEventHistory, then becomes idle.

