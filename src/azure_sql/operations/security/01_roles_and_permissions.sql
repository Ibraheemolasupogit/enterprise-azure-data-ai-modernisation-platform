CREATE ROLE cf_platform_admin;
CREATE ROLE cf_db_admin;
CREATE ROLE cf_app_executor;
CREATE ROLE cf_deployment;
CREATE ROLE cf_operational_reader;
CREATE ROLE cf_security_auditor;
CREATE ROLE cf_automation_executor;

CREATE USER [grp-cf-platform-admins] FROM EXTERNAL PROVIDER;
CREATE USER [grp-cf-db-admins] FROM EXTERNAL PROVIDER;
CREATE USER [mi-cf-transport-app] FROM EXTERNAL PROVIDER;
CREATE USER [id-cf-sql-deploy] FROM EXTERNAL PROVIDER;
CREATE USER [grp-cf-operational-analysts] FROM EXTERNAL PROVIDER;
CREATE USER [grp-cf-security-auditors] FROM EXTERNAL PROVIDER;
CREATE USER [mi-cf-ops-automation] FROM EXTERNAL PROVIDER;

ALTER ROLE cf_platform_admin ADD MEMBER [grp-cf-platform-admins];
ALTER ROLE cf_db_admin ADD MEMBER [grp-cf-db-admins];
ALTER ROLE cf_app_executor ADD MEMBER [mi-cf-transport-app];
ALTER ROLE cf_deployment ADD MEMBER [id-cf-sql-deploy];
ALTER ROLE cf_operational_reader ADD MEMBER [grp-cf-operational-analysts];
ALTER ROLE cf_security_auditor ADD MEMBER [grp-cf-security-auditors];
ALTER ROLE cf_automation_executor ADD MEMBER [mi-cf-ops-automation];

GRANT VIEW DEFINITION TO cf_platform_admin;
GRANT ALTER ANY USER TO cf_platform_admin;

GRANT CONTROL ON DATABASE::legacy_tms TO cf_db_admin;

GRANT EXECUTE ON dbo.usp_CreateShipment TO cf_app_executor;
GRANT EXECUTE ON dbo.usp_UpdateShipmentStatus TO cf_app_executor;
GRANT SELECT ON dbo.vw_CustomerServiceSnapshot TO cf_operational_reader;
GRANT SELECT ON dbo.vw_OpenShipmentsByDepot TO cf_operational_reader;

GRANT ALTER, CONTROL, REFERENCES, SELECT, INSERT, UPDATE, DELETE ON SCHEMA::dbo TO cf_deployment;

GRANT VIEW DATABASE STATE TO cf_security_auditor;
GRANT SELECT ON SCHEMA::dbo TO cf_security_auditor;

GRANT EXECUTE ON SCHEMA::ops TO cf_automation_executor;

DENY DELETE ON SCHEMA::dbo TO cf_operational_reader;
DENY INSERT ON SCHEMA::dbo TO cf_operational_reader;
DENY UPDATE ON SCHEMA::dbo TO cf_operational_reader;

