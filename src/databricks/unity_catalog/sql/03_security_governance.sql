-- Least-privilege Unity Catalog access and fine-grained governance patterns.
-- Principal names are placeholders for Entra groups/service principals managed outside this repository.

GRANT USE CATALOG ON CATALOG contoso_freight_prod TO `grp-operational-analysts`;
GRANT USE SCHEMA ON SCHEMA contoso_freight_prod.gold TO `grp-operational-analysts`;
GRANT SELECT ON SCHEMA contoso_freight_prod.gold TO `grp-operational-analysts`;

GRANT USE CATALOG ON CATALOG contoso_freight_prod TO `spn-dbx-pipelines`;
GRANT USE SCHEMA ON SCHEMA contoso_freight_prod.bronze TO `spn-dbx-pipelines`;
GRANT USE SCHEMA ON SCHEMA contoso_freight_prod.silver TO `spn-dbx-pipelines`;
GRANT USE SCHEMA ON SCHEMA contoso_freight_prod.reference TO `spn-dbx-pipelines`;
GRANT MODIFY ON SCHEMA contoso_freight_prod.bronze TO `spn-dbx-pipelines`;
GRANT MODIFY ON SCHEMA contoso_freight_prod.silver TO `spn-dbx-pipelines`;

GRANT USE CATALOG ON CATALOG contoso_freight_prod TO `grp-security-auditors`;
GRANT USE SCHEMA ON SCHEMA contoso_freight_prod.audit TO `grp-security-auditors`;
GRANT SELECT ON SCHEMA contoso_freight_prod.audit TO `grp-security-auditors`;

CREATE FUNCTION IF NOT EXISTS contoso_freight_prod.gold.mask_email(email_value STRING)
RETURNS STRING
RETURN CASE
    WHEN is_account_group_member('grp-customer-pii-readers') THEN email_value
    WHEN email_value IS NULL THEN NULL
    ELSE regexp_replace(email_value, '(^.).*(@.*$)', '$1***$2')
END;

CREATE FUNCTION IF NOT EXISTS contoso_freight_prod.gold.allow_region(region_value STRING)
RETURNS BOOLEAN
RETURN is_account_group_member('grp-global-operations')
    OR (
        is_account_group_member('grp-uk-operations')
        AND region_value IN ('UK South', 'UK North')
    );

ALTER TABLE contoso_freight_prod.silver.customer_accounts
ALTER COLUMN contact_email
SET MASK contoso_freight_prod.gold.mask_email;

ALTER TABLE contoso_freight_prod.silver.shipments
SET ROW FILTER contoso_freight_prod.gold.allow_region ON (billing_region);

-- Governed tags and ABAC policies are account-level governance assets.
-- Define them in the Databricks account, then attach at catalog/schema/table/column scope.
-- ABAC is preferred for broad, tag-driven row and column controls across tables.

