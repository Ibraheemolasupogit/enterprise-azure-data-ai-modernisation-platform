# ADR-0007: Relational vs Cosmos DB Disposition

- Status: Accepted
- Date: 2026-08-20

## Context

The assessment must consider Azure Cosmos DB where genuinely relevant, but the current estate is dominated by transactional relational workloads, batch/file feeds, operational events, and analytical/reporting needs.

## Decision

Do not select Azure Cosmos DB as a primary Milestone 3 target. Retain it as a possible later serving option only if a specific low-latency document access pattern is proven by future requirements.

## Consequences

The architecture avoids forcing an Azure service into the solution without evidence. Future search, RAG, or operational API milestones may revisit Cosmos DB if they produce a justified access pattern and data model.

## Alternatives Considered

- Use Cosmos DB for shipments or cases now: rejected because relational constraints, migration sequencing, and analytical processing are more important current drivers.
- Use Cosmos DB for raw events: rejected because lakehouse ingestion and Delta processing are the better fit for event history and replay.
- Ignore Cosmos DB entirely: rejected because future serving workloads may justify it.

