# Databricks Audit Investigation

Use this runbook when investigating Databricks access, administrative changes, or sensitive-data usage.

## Steps

1. Identify the affected workspace, catalog, schema, object, principal, and time window.
2. Query Unity Catalog audit events and workspace diagnostic logs.
3. Review compute events for cluster, warehouse, policy, and runtime changes.
4. Review job or pipeline events when production workflows exist.
5. Review secret access events for unexpected scope or Key Vault-backed reads.
6. Use table and column lineage to identify downstream impact when available.
7. Preserve evidence in the audit schema or case record.
8. Apply grant, policy, tag, or compute-policy remediation through pull request and approved deployment.

