# ADR-0004: Managed Identity and Entra-First Authentication

- Status: Accepted
- Date: 2026-08-20

## Context

The platform will span databases, storage, Databricks, Key Vault, monitoring, CI/CD, and AI services. Static secrets increase operational risk and make access reviews harder.

## Decision

Use Microsoft Entra ID as the default identity provider and managed identities wherever supported. Use workload identity federation for CI/CD where available. Store unavoidable secrets in Key Vault and reference them through environment-specific deployment mechanisms.

## Consequences

This improves auditability and reduces secret sprawl. It requires careful RBAC design, environment separation, and local-development documentation.

## Alternatives Considered

- Use connection strings and shared keys: simple initially but weak for enterprise operations.
- Use service principals for all workloads: auditable but still introduces credential lifecycle management.
- Defer identity design: creates rework once infrastructure and pipelines are implemented.

