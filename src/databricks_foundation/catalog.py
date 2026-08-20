from __future__ import annotations

# ruff: noqa: E501
from databricks_foundation.model import (
    AccessControl,
    BundleTarget,
    ComputeStrategy,
    FederationDecision,
    FineGrainedSecurity,
    GovernedTag,
    NamespaceObject,
    ReadinessItem,
    RetentionPolicy,
    SharingDecision,
    StorageBoundary,
    WorkspaceStrategy,
)

ENVIRONMENTS = ("dev", "test", "prod")
REGION = "uksouth"


def _schema_purpose(schema: str) -> str:
    purposes = {
        "bronze": "raw landed data after future ingestion with minimal normalization",
        "silver": "conformed, quality-checked analytical data",
        "gold": "curated data products and governed consumption views",
        "reference": "governed reference and lookup data",
        "quarantine": "invalid or restricted records pending triage",
        "audit": "pipeline, quality, lineage, and security evidence",
    }
    return purposes[schema]

WORKSPACES = [
    WorkspaceStrategy("dev", "adb-contoso-freight-dev-uksouth", "engineering development and exploratory validation", "single workspace isolated by Azure resource group, VNet, UC catalog binding, and non-production identities", REGION, "developer groups and non-production workload identities only", "dev ADLS account and dev external locations", "contoso_freight_dev only", "feature branch -> PR -> dev bundle target", "configuration defined"),
    WorkspaceStrategy("test", "adb-contoso-freight-test-uksouth", "release verification, integration testing, and masked data-product validation", "single test workspace isolated from dev/prod with protected CI/CD identity", REGION, "test data-engineering groups and deployment identity", "test ADLS account and test external locations", "contoso_freight_test only", "main branch or release branch -> approved test target", "configuration defined"),
    WorkspaceStrategy("prod", "adb-contoso-freight-prod-uksouth", "production analytical platform and governed data products", "single production workspace with protected environment approval and restricted admin access", REGION, "production service principals and approved operating groups", "production ADLS account and production external locations", "contoso_freight_prod only", "approved release -> protected prod bundle target", "configuration defined"),
]

COMPUTE = [
    ComputeStrategy("interactive engineering", "all-purpose compute", "current LTS runtime; upgrade through policy after compatibility testing", "min 1 max 4 workers", 30, "enabled where supported", "small general purpose workers for dev only", "policy-interactive-dev", "workspace or cluster policy approved libraries", "low idle tolerance through auto-termination", "developer identity; no production data writes", "not allowed for production pipeline writes"),
    ComputeStrategy("batch ingestion job", "jobs compute", "current LTS runtime pinned by bundle variable", "min 2 max 8 workers", 15, "enabled for Delta-heavy processing", "standard workers sized by file volume after Azure validation", "policy-jobs-standard", "job-scoped wheel requirements only", "ephemeral compute limits idle spend", "runs as pipeline workload identity", "production requires service principal and cluster policy"),
    ComputeStrategy("event ingestion", "serverless jobs where available", "Databricks-managed current runtime", "serverless elastic", 0, "platform managed", "serverless sizing requires Azure validation", "policy-serverless-jobs", "bundle-defined dependencies only", "pay-per-use; validate cold-start and concurrency", "least privilege through UC and workload identity", "fallback to jobs compute if serverless unavailable"),
    ComputeStrategy("SQL serving", "SQL warehouse", "serverless or pro SQL warehouse based on region availability", "small to medium with auto-stop", 10, "enabled by warehouse engine", "start small; tune with query history", "policy-sql-warehouse", "SQL functions only", "separate serving cost envelope", "read-only analyst groups", "no direct Bronze access in production"),
    ComputeStrategy("future Delta Live Tables/Lakeflow pipeline", "pipeline compute", "pipeline-managed LTS-compatible runtime", "autoscale by pipeline configuration", 0, "enabled where compatible", "sizing deferred until pipeline milestone", "policy-pipeline", "pipeline-scoped libraries", "continuous pipelines need explicit cost approval", "runs as pipeline workload identity", "not implemented in this milestone"),
    ComputeStrategy("legacy compatibility", "classic compute only by exception", "specific runtime documented with expiry date", "fixed or limited autoscale", 20, "disabled unless tested", "minimum viable workers", "policy-classic-exception", "pre-approved library list", "requires exception due operational overhead", "narrow network and data access", "time-bound exception only"),
]

SCHEMAS = ("bronze", "silver", "gold", "reference", "quarantine", "audit")

NAMESPACE = [
    NamespaceObject(env, f"contoso_freight_{env}", schema, "schema", schema, _schema_purpose(schema), "catalog-managed metadata", "src/databricks/unity_catalog/sql/01_catalogs_schemas.sql", "configuration defined")
    for env in ENVIRONMENTS
    for schema in SCHEMAS
] + [
    NamespaceObject("prod", "contoso_freight_prod", "bronze", "managed table", "shipment_events_raw", "raw operational shipment events landed for later quality processing", "managed table", "src/databricks/unity_catalog/sql/02_tables_views_volumes.sql", "configuration defined"),
    NamespaceObject("prod", "contoso_freight_prod", "silver", "managed table", "shipments", "conformed shipment records after future transformation", "managed table", "src/databricks/unity_catalog/sql/02_tables_views_volumes.sql", "configuration defined"),
    NamespaceObject("prod", "contoso_freight_prod", "silver", "managed table", "customer_accounts", "conformed customer/account analytical records", "managed table", "src/databricks/unity_catalog/sql/02_tables_views_volumes.sql", "configuration defined"),
    NamespaceObject("prod", "contoso_freight_prod", "reference", "managed table", "depots_routes", "governed depot and route reference data", "managed table", "src/databricks/unity_catalog/sql/02_tables_views_volumes.sql", "configuration defined"),
    NamespaceObject("prod", "contoso_freight_prod", "silver", "managed table", "billing_service_cases", "billing and service case analytical boundary", "managed table", "src/databricks/unity_catalog/sql/02_tables_views_volumes.sql", "configuration defined"),
    NamespaceObject("prod", "contoso_freight_prod", "gold", "view", "shipment_reliability", "curated future data product for operational analytics", "managed view", "src/databricks/unity_catalog/sql/02_tables_views_volumes.sql", "configuration defined"),
    NamespaceObject("prod", "contoso_freight_prod", "quarantine", "managed volume", "invalid_records", "quarantine payload storage for rejected records", "managed volume", "src/databricks/unity_catalog/sql/02_tables_views_volumes.sql", "configuration defined"),
    NamespaceObject("prod", "contoso_freight_prod", "audit", "managed table", "data_quality_events", "future data quality and pipeline audit events", "managed table", "src/databricks/unity_catalog/sql/02_tables_views_volumes.sql", "configuration defined"),
    NamespaceObject("prod", "contoso_freight_prod", "gold", "function", "mask_email", "reusable masking helper for customer contact fields", "SQL function", "src/databricks/unity_catalog/sql/03_security_governance.sql", "configuration defined"),
    NamespaceObject("prod", "contoso_freight_prod", "gold", "future boundary", "AI/BI Genie candidate objects", "future governed consumption over curated Gold objects only", "not implemented", "docs/databricks-platform-foundation.md", "requires Azure validation"),
]

STORAGE = [
    StorageBoundary("stg-001", "dev", "stcontosofreightdev", "cred_contoso_freight_dev", "storage credential", "abfss://<container>@stcontosofreightdev.dfs.core.windows.net/", "access connector managed identity", "platform engineering", "Unity Catalog", "storage lifecycle controlled by ADLS and UC object type"),
    StorageBoundary("stg-002", "dev", "stcontosofreightdev/landing", "extloc_dev_landing", "external location", "abfss://landing@stcontosofreightdev.dfs.core.windows.net/", "storage credential", "data engineering", "Unity Catalog", "external files retained by ADLS lifecycle"),
    StorageBoundary("stg-003", "test", "stcontosofreighttest/landing", "extloc_test_landing", "external location", "abfss://landing@stcontosofreighttest.dfs.core.windows.net/", "storage credential", "data engineering", "Unity Catalog", "external files retained by ADLS lifecycle"),
    StorageBoundary("stg-004", "prod", "stcontosofreightprod/landing", "extloc_prod_landing", "external location", "abfss://landing@stcontosofreightprod.dfs.core.windows.net/", "storage credential", "data engineering", "Unity Catalog", "external files retained by ADLS lifecycle"),
    StorageBoundary("stg-005", "prod", "stcontosofreightprod/checkpoints", "extloc_prod_checkpoints", "external location", "abfss://checkpoints@stcontosofreightprod.dfs.core.windows.net/", "storage credential", "pipeline platform", "Unity Catalog", "checkpoint retention follows pipeline recovery policy"),
    StorageBoundary("stg-006", "prod", "stcontosofreightprod/exchange", "extloc_prod_exchange", "external location", "abfss://exchange@stcontosofreightprod.dfs.core.windows.net/", "storage credential", "data product owner", "Unity Catalog", "external exchange data explicitly time-bound"),
]

ACCESS = [
    AccessControl("grp-platform-admins", "group", "metastore and workspace admin boundary", "MANAGE only where platform-owned", "administer workspaces, catalogs, policies, credentials", "break-glass and platform operations only"),
    AccessControl("grp-data-engineers", "group", "dev/test catalogs", "USE CATALOG; USE SCHEMA; CREATE TABLE; CREATE VOLUME; MODIFY", "build and validate analytical objects before promotion", "no direct prod MODIFY outside approved deployment"),
    AccessControl("spn-dbx-pipelines", "service principal", "bronze/silver/reference/quarantine schemas", "USE CATALOG; USE SCHEMA; SELECT; MODIFY; CREATE TABLE; CREATE VOLUME", "run ingestion and transformation workloads in later milestones", "production identity bound to protected workflows"),
    AccessControl("grp-data-quality-operators", "group", "quarantine and audit schemas", "USE CATALOG; USE SCHEMA; SELECT; MODIFY", "triage rejected records and data quality events", "no broad Gold write access"),
    AccessControl("grp-operational-analysts", "group", "gold schema", "USE CATALOG; USE SCHEMA; SELECT; EXECUTE", "consume curated operational analytics", "no Bronze or raw service-case detail access"),
    AccessControl("grp-security-auditors", "group", "audit schema and system tables", "USE CATALOG; USE SCHEMA; SELECT", "investigate lineage, audit, and administrative changes", "read-only"),
    AccessControl("grp-downstream-consumers", "group", "shared Gold views or Delta shares", "SELECT", "consume approved data products", "recipient-specific grants only"),
    AccessControl("spn-dbx-cicd", "service principal", "bundle target workspace and catalog", "USE CATALOG; USE SCHEMA; CREATE TABLE; MODIFY; EXECUTE", "deploy approved bundle resources", "prod requires protected environment approval"),
]

FINE_GRAINED = [
    FineGrainedSecurity("fg-001", "customer", "silver.customer_accounts.contact_email", "column mask", "customer contact email", "ABAC column mask policy based on governed tag pii=email", "table-level MASK with gold.mask_email where ABAC is unavailable", "configuration defined"),
    FineGrainedSecurity("fg-002", "operations", "silver.shipments.billing_region", "row filter", "regional operational data", "ABAC row filter by domain and region tags for analyst groups", "table-level ROW FILTER function for limited regional access", "configuration defined"),
    FineGrainedSecurity("fg-003", "service", "silver.billing_service_cases.case_detail", "column mask", "service-case narrative text", "ABAC sensitivity=restricted policy masks details except approved service groups", "dynamic view only for transitional consumers", "configuration defined"),
    FineGrainedSecurity("fg-004", "quarantine", "quarantine.invalid_records", "schema privilege boundary", "invalid source payloads", "restricted schema grants and audit logging", "separate quarantine views for operators", "configuration defined"),
]

TAGS = [
    GovernedTag("pii", "none,email,identifier,contact", "columns and tables", "grp-data-governance", "drive PII column masking and discoverability", "customer_accounts.contact_email=pii:email"),
    GovernedTag("sensitivity", "public,internal,confidential,restricted", "catalogs, schemas, tables, columns", "grp-security-auditors", "masking, sharing restrictions, and review workflows", "billing_service_cases.case_detail=sensitivity:restricted"),
    GovernedTag("domain", "shipment,customer,depot_route,billing_service,operations", "schemas and tables", "grp-data-governance", "domain ownership and restricted-domain access", "shipments=domain:shipment"),
    GovernedTag("lifecycle", "landing,bronze,silver,gold,reference,quarantine,audit", "schemas, tables, volumes", "grp-platform-admins", "retention and promotion controls", "gold.shipment_reliability=lifecycle:gold"),
    GovernedTag("environment", "dev,test,prod", "catalogs and external locations", "grp-platform-admins", "workspace/catalog binding and environment isolation", "contoso_freight_prod=environment:prod"),
]

RETENTION = [
    RetentionPolicy("bronze", "90 days", "14 days minimum", "VACUUM no shorter than deleted-file retention after recovery checks", "short-term replay and ingestion defect diagnosis", "delete requests handled by downstream purge workflow after lineage review", "cool tier after 30 days for raw external files"),
    RetentionPolicy("silver", "180 days", "30 days", "scheduled VACUUM after quality validation", "business correction and backfill support", "privacy deletion propagated from source mapping", "managed table lifecycle through Unity Catalog"),
    RetentionPolicy("gold", "365 days", "30 days", "conservative VACUUM after product-owner approval", "consumer recovery and reporting reproducibility", "deletion may require regenerated aggregates", "managed table lifecycle through Unity Catalog"),
    RetentionPolicy("reference", "365 days", "30 days", "VACUUM only after reference release cycle", "reference rollback and audit", "hard deletes require stewardship approval", "managed table lifecycle through Unity Catalog"),
    RetentionPolicy("quarantine", "90 days", "30 days", "purge after triage SLA and audit capture", "defect investigation", "sensitive payload deletion can override normal retention", "ADLS lifecycle for raw quarantined payloads"),
    RetentionPolicy("audit", "730 days", "90 days", "no aggressive VACUUM; align with investigation needs", "security and operational investigations", "legal/security hold can extend retention", "archive tier after 180 days where supported"),
]

LINEAGE = [
    ReadinessItem("lin-001", "table lineage", "Unity Catalog table lineage", "source -> bronze -> silver -> gold lineage after pipelines exist", "designed; no fabricated graph", "requires Azure validation"),
    ReadinessItem("lin-002", "column lineage", "Unity Catalog column lineage", "customer/contact and shipment-status transformations traced", "designed; future pipeline evidence", "requires Azure validation"),
    ReadinessItem("lin-003", "job lineage", "job and bundle lineage", "job run to output table links", "bundle foundation only", "requires Azure validation"),
    ReadinessItem("lin-004", "impact analysis", "downstream dependency review", "affected Gold views and shares identified before schema changes", "configuration defined", "configuration defined"),
    ReadinessItem("lin-005", "system tables", "system.access and lineage tables", "queryable lineage/audit evidence retained", "query assets defined", "requires Azure validation"),
]

AUDIT = [
    ReadinessItem("aud-001", "Unity Catalog events", "grants, ownership, policy and tag changes", "system table query and Log Analytics export", "query assets defined", "requires Azure validation"),
    ReadinessItem("aud-002", "workspace events", "workspace, repo, notebook, and admin changes", "audit log diagnostics", "configuration defined", "requires Azure validation"),
    ReadinessItem("aud-003", "compute events", "cluster/warehouse creation, policy use, termination", "system tables and diagnostic logs", "configuration defined", "requires Azure validation"),
    ReadinessItem("aud-004", "job/pipeline events", "future job and pipeline run events", "bundle deployment and run history", "deferred until pipelines exist", "requires Azure validation"),
    ReadinessItem("aud-005", "secret access", "secret scope and Key Vault-backed access", "secret access events", "boundary defined; no secrets committed", "requires Azure validation"),
    ReadinessItem("aud-006", "security investigation", "who accessed restricted customer/service data", "audit query templates", "query assets defined", "requires Azure validation"),
]

SHARING = [
    SharingDecision("share-001", "Databricks-to-Databricks", "approved internal or partner recipients", "share Gold/reference only; no raw PII/service-case detail", "recipient, object, and query access audit", "revoke recipient or share grant", "allowed by exception"),
    SharingDecision("share-002", "open Delta Sharing", "external recipients without Databricks", "public/open recipients receive non-sensitive aggregates only", "download/access event review", "expire recipient credential and remove table", "restricted"),
    SharingDecision("share-003", "internal consumers", "internal analytics domains", "prefer catalog grants over shares inside same account", "Unity Catalog audit events", "revoke group grants", "prefer grants"),
    SharingDecision("share-004", "external exchange zone", "contracted data exchange", "exchange external location with time-bound approval", "external location and share audit", "remove external location/share", "future capability only"),
]

FEDERATION = [
    FederationDecision("legacy_tms Azure SQL MI", "schema discovery and short transition queries", "replicated analytical ingestion for production analytics", "limited read-only transition diagnostics", "not primary reporting or ingestion architecture", "limited federation"),
    FederationDecision("billing_ops PostgreSQL Flexible Server", "source profiling and reconciliation", "batch/CDC ingestion for analytical use", "read-only profiling in dev/test", "no operational workload coupling", "limited federation"),
    FederationDecision("partner files in ADLS", "not applicable", "file ingestion through external locations", "external tables only for landing inspection", "do not federate file feeds", "ingest"),
    FederationDecision("future APIs", "contract discovery", "ingestion through governed landing zone", "small metadata checks only", "no broad live query dependency", "defer"),
]

BUNDLE_TARGETS = [
    BundleTarget("dev", "${var.dev_workspace_host}", "${var.dev_catalog}", "non-production deployment service principal or developer identity", "development", "catalogs, schemas, policies, and future jobs for dev only"),
    BundleTarget("test", "${var.test_workspace_host}", "${var.test_catalog}", "CI/CD service principal", "release validation", "catalogs, schemas, policies, and future jobs for test only"),
    BundleTarget("prod", "${var.prod_workspace_host}", "${var.prod_catalog}", "production service principal with protected environment approval", "production", "production catalog and approved resources only"),
]

READINESS = [
    ReadinessItem("ready-001", "workspace", "dev/test/prod workspace strategy", "workspace_strategy.csv", "ready for IaC validation", "configuration defined"),
    ReadinessItem("ready-002", "infrastructure", "Bicep module is switch-gated and contains no secrets", "infra/modules/databricks/foundation.bicep", "declared only", "configuration defined"),
    ReadinessItem("ready-003", "compute", "compute decision framework and policies", "compute_strategy.csv", "ready for Azure validation", "configuration defined"),
    ReadinessItem("ready-004", "Unity Catalog", "catalogs, schemas, tables, views, functions, volumes", "unity_catalog_namespace.csv", "DDL assets defined", "configuration defined"),
    ReadinessItem("ready-005", "storage", "access connector, storage credential and external location model", "storage_boundary.csv", "no keys or SAS tokens", "configuration defined"),
    ReadinessItem("ready-006", "security", "least privilege, ABAC, row/column control patterns", "fine_grained_security.csv", "policy-ready", "configuration defined"),
    ReadinessItem("ready-007", "lineage", "Unity Catalog lineage expectations", "lineage_readiness.csv", "no fabricated lineage", "requires Azure validation"),
    ReadinessItem("ready-008", "audit", "system table and Log Analytics audit boundary", "audit_catalog.csv", "query templates defined", "requires Azure validation"),
    ReadinessItem("ready-009", "bundle", "Databricks Asset Bundle targets", "databricks.yml", "foundation defined with no fake workloads", "locally validated"),
]
