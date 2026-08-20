IF OBJECT_ID('dbo.usp_GetCustomerShipmentSummary', 'P') IS NOT NULL DROP PROCEDURE dbo.usp_GetCustomerShipmentSummary;
IF OBJECT_ID('dbo.usp_CreateShipment', 'P') IS NOT NULL DROP PROCEDURE dbo.usp_CreateShipment;
IF OBJECT_ID('dbo.usp_UpdateShipmentStatus', 'P') IS NOT NULL DROP PROCEDURE dbo.usp_UpdateShipmentStatus;
IF OBJECT_ID('dbo.vw_OpenShipmentsByDepot', 'V') IS NOT NULL DROP VIEW dbo.vw_OpenShipmentsByDepot;
IF OBJECT_ID('dbo.vw_CustomerServiceSnapshot', 'V') IS NOT NULL DROP VIEW dbo.vw_CustomerServiceSnapshot;
IF OBJECT_ID('dbo.ShipmentEventHistory', 'U') IS NOT NULL DROP TABLE dbo.ShipmentEventHistory;
IF OBJECT_ID('dbo.ShipmentIncident', 'U') IS NOT NULL DROP TABLE dbo.ShipmentIncident;
IF OBJECT_ID('dbo.Shipment', 'U') IS NOT NULL DROP TABLE dbo.Shipment;
IF OBJECT_ID('dbo.Vehicle', 'U') IS NOT NULL DROP TABLE dbo.Vehicle;
IF OBJECT_ID('dbo.Route', 'U') IS NOT NULL DROP TABLE dbo.Route;
IF OBJECT_ID('dbo.Depot', 'U') IS NOT NULL DROP TABLE dbo.Depot;
IF OBJECT_ID('dbo.CustomerAccountAudit', 'U') IS NOT NULL DROP TABLE dbo.CustomerAccountAudit;
IF OBJECT_ID('dbo.CustomerAccount', 'U') IS NOT NULL DROP TABLE dbo.CustomerAccount;

