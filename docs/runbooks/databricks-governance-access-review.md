# Databricks Governance Access Review

Use this runbook to review Unity Catalog access for Contoso Freight data objects.

## Steps

1. Export grants for catalogs, schemas, tables, functions, volumes, storage credentials, and external locations.
2. Compare grants with `outputs/databricks_foundation/access_control_matrix.csv`.
3. Confirm production write access belongs only to approved service principals and operating groups.
4. Confirm analysts consume Gold objects rather than Bronze or unrestricted Silver objects.
5. Review governed tags for `pii`, `sensitivity`, `domain`, `lifecycle`, and `environment`.
6. Validate row-filter and column-mask policies against sensitive customer and service-case objects.
7. Revoke direct grants that bypass the documented persona model.
8. Record exceptions with owner, expiry date, and remediation path.

