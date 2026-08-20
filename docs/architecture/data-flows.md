# Data Flow Model

This document defines the intended data-flow model for later milestones. It is not an implemented pipeline inventory.

## Scenario Domains

Contoso Freight uses one coherent synthetic enterprise domain:

- Shipments: bookings, consignments, routes, milestones, proof of delivery.
- Depots: capacity, handling events, exceptions, regional operations.
- Fleet: vehicles, trailers, maintenance plans, telematics summaries.
- Customers: accounts, contracts, service tiers, support interactions.
- Disruptions: weather, depot congestion, route incidents, delay reasons.

These domains support transactional, analytical, and AI workloads without creating separate mini-projects.

## Planned Flow Types

| Flow | Source | Landing | Processing | Serving |
| --- | --- | --- | --- | --- |
| Batch reference data | SQL exports or generated fixtures | ADLS bronze | Databricks standardisation | Gold dimensions |
| CDC transactional data | SQL Server / Azure SQL | ADLS bronze Delta | Silver conformance and quality | Operational analytics |
| Streaming events | Event sources in later milestones | Delta bronze streaming tables | Streaming quality and aggregation | Fresh operational views |
| Operational SQL AI | Azure SQL tables | In database | Vector or semantic operations where appropriate | SQL APIs and apps |
| RAG knowledge | Curated data products and documents | Search/vector index | Chunking, embeddings, filtering | Grounded assistant APIs |

## Data Contract Expectations

Later implementations should define:

- Source ownership and schema contracts.
- Primary keys, natural keys, and late-arriving data behaviour.
- Classification and retention requirements.
- Quality checks and failure handling.
- Lineage from source to serving layer.
- Cost and freshness expectations.

