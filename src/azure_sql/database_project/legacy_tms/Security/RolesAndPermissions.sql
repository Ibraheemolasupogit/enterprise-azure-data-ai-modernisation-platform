CREATE ROLE app_legacy_tms_reader;
GO
CREATE ROLE app_legacy_tms_writer;
GO
CREATE ROLE app_legacy_tms_operator;
GO

GRANT SELECT ON dbo.vw_OpenShipmentsByDepot TO app_legacy_tms_reader;
GRANT SELECT ON dbo.vw_CustomerServiceSnapshot TO app_legacy_tms_reader;
GRANT EXECUTE ON dbo.usp_CreateShipment TO app_legacy_tms_writer;
GRANT EXECUTE ON dbo.usp_UpdateShipmentStatus TO app_legacy_tms_writer;
GRANT VIEW DEFINITION TO app_legacy_tms_operator;

