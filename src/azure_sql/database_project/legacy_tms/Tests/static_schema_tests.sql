-- Static assertions for reviewer-driven database tests.
-- These checks are intended for SQL Server-compatible validation environments.

SELECT 'dbo.CustomerAccount' AS RequiredObject
WHERE OBJECT_ID('dbo.CustomerAccount', 'U') IS NOT NULL;

SELECT 'dbo.Shipment' AS RequiredObject
WHERE OBJECT_ID('dbo.Shipment', 'U') IS NOT NULL;

SELECT 'dbo.usp_UpdateShipmentStatus' AS RequiredObject
WHERE OBJECT_ID('dbo.usp_UpdateShipmentStatus', 'P') IS NOT NULL;

