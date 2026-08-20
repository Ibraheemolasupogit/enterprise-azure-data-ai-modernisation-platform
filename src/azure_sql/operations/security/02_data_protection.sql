ADD SENSITIVITY CLASSIFICATION TO dbo.CustomerAccount.ContactEmail
WITH (LABEL = 'Confidential', INFORMATION_TYPE = 'Contact Info');

ADD SENSITIVITY CLASSIFICATION TO dbo.CustomerAccount.LegalName
WITH (LABEL = 'Confidential', INFORMATION_TYPE = 'Customer Account');

ADD SENSITIVITY CLASSIFICATION TO dbo.Shipment.DeclaredValueGbp
WITH (LABEL = 'Confidential', INFORMATION_TYPE = 'Commercial Value');

ALTER TABLE dbo.CustomerAccount
ALTER COLUMN ContactEmail ADD MASKED WITH (FUNCTION = 'email()');

ALTER TABLE dbo.CustomerAccount
ALTER COLUMN LegalName ADD MASKED WITH (FUNCTION = 'partial(2,"XXXX",2)');

CREATE SCHEMA security;
GO

CREATE FUNCTION security.fn_depot_access(@BillingRegion varchar(40))
RETURNS TABLE
WITH SCHEMABINDING
AS
RETURN SELECT 1 AS access_result
WHERE IS_MEMBER('cf_db_admin') = 1
   OR IS_MEMBER('cf_security_auditor') = 1
   OR @BillingRegion = CAST(SESSION_CONTEXT(N'billing_region') AS varchar(40));
GO

CREATE SECURITY POLICY security.CustomerRegionFilter
ADD FILTER PREDICATE security.fn_depot_access(BillingRegion) ON dbo.CustomerAccount
WITH (STATE = OFF);

-- RLS is intentionally OFF in Milestone 6 until business regional-access rules are validated.

