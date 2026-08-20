-- Unity Catalog namespace foundation for Contoso Freight.
-- Execute in a Databricks workspace after metastore assignment and workspace-catalog bindings.

CREATE CATALOG IF NOT EXISTS contoso_freight_dev
COMMENT 'Development catalog for Contoso Freight Databricks platform assets.';

CREATE CATALOG IF NOT EXISTS contoso_freight_test
COMMENT 'Test catalog for release validation and integration testing.';

CREATE CATALOG IF NOT EXISTS contoso_freight_prod
COMMENT 'Production catalog for governed Contoso Freight analytical data products.';

CREATE SCHEMA IF NOT EXISTS contoso_freight_prod.bronze
COMMENT 'Raw landed data after future ingestion with minimal normalization.';

CREATE SCHEMA IF NOT EXISTS contoso_freight_prod.silver
COMMENT 'Conformed, quality-checked analytical data prepared for product use.';

CREATE SCHEMA IF NOT EXISTS contoso_freight_prod.gold
COMMENT 'Curated and governed analytical data products.';

CREATE SCHEMA IF NOT EXISTS contoso_freight_prod.reference
COMMENT 'Governed reference and lookup data.';

CREATE SCHEMA IF NOT EXISTS contoso_freight_prod.quarantine
COMMENT 'Invalid or restricted records pending triage.';

CREATE SCHEMA IF NOT EXISTS contoso_freight_prod.audit
COMMENT 'Pipeline, quality, lineage, and security evidence.';

-- Repeat the schema pattern for dev/test through automation variables in Databricks Asset Bundles.

