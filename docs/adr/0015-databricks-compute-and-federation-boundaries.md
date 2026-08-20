# 0015 - Databricks Compute and Federation Boundaries

- Status: Accepted
- Date: 2026-08-20

## Context

Databricks must support interactive engineering, production jobs, SQL serving, future pipeline compute, and occasional compatibility cases. It also needs a clear position on query federation against operational databases.

## Decision

Use all-purpose compute only for development, jobs compute for production batch workloads, serverless jobs where available, SQL warehouses for curated consumption, future pipeline compute for Lakeflow-style processing, and classic compute by exception. Use federation only for discovery, profiling, transition, and reconciliation; production analytics should use ingested lakehouse data.

## Consequences

Operational databases remain systems of record and are not turned into analytical serving dependencies. Compute choices can be governed by workload class, policy, identity, cost, and runtime strategy.

