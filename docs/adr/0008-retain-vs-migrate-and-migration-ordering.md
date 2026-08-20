# ADR-0008: Retain vs Migrate and Migration Ordering

- Status: Accepted
- Date: 2026-08-20

## Context

The assessment identifies business-critical workloads, dependencies, compatibility findings, and data-quality issues. Migrating every workload immediately would amplify risk and ignore prerequisite remediation.

## Decision

Use staged migration waves:

- Wave 0: prerequisites and remediation.
- Wave 1: low-risk feeds and analytical offload foundations.
- Wave 2: secondary relational billing/service source.
- Wave 3: business-critical transport OLTP.

Retain customer-service search temporarily until governed data products, security trimming, and access controls exist.

## Consequences

The plan reduces risk by handling dependencies and reporting pressure before the most critical OLTP workload. It also makes clear that retention can be a deliberate modernisation decision, not a failure to migrate.

## Alternatives Considered

- Move the core OLTP workload first: rejected because it has the highest coupling and compatibility risk.
- Migrate all systems in parallel: rejected because dependency and rollback complexity would be too high.
- Retain all systems: rejected because it leaves reporting contention, governance gaps, and integration debt unresolved.

