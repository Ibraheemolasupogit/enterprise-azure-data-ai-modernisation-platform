# Security and Governance Model

## Identity

Microsoft Entra ID is the default identity provider for human and workload access. Managed identities are preferred for Azure services. Service principals are used only where managed identity is not supported or where CI/CD federation requires explicit application identities.

## Secret Management

No secrets are committed to this repository. Future implementations should use Key Vault references, workload federation, managed identity, and environment-specific deployment variables. Local samples must use placeholders or documented environment variables only.

## Access Control

Access is designed around least privilege:

- Separate platform, data engineering, database operations, analytics, and AI application roles.
- Scope permissions by environment.
- Use Azure RBAC for resource control-plane permissions.
- Use SQL roles, Unity Catalog grants, and storage ACLs for data-plane permissions.
- Apply row-level security and masking where business rules require scoped visibility.

## Governance and Lineage

Future milestones should integrate with Microsoft Purview where appropriate for:

- Asset cataloguing.
- Classification.
- Lineage.
- Ownership.
- Glossary and data product metadata.

Unity Catalog should govern Databricks assets and align with Purview-facing metadata where possible.

## Audit and Monitoring

The platform should emit audit and operational signals to Azure Monitor and Log Analytics. Required signal families include:

- SQL auditing and query performance.
- Databricks job and pipeline execution.
- Data quality failures.
- Identity and access changes.
- Key Vault access.
- Cost and capacity anomalies.

