# Synthetic Data Strategy

The platform uses the fictional Contoso Freight scenario for all future synthetic data. Synthetic data must be realistic enough to support transactional, analytical, and AI workloads while remaining entirely fabricated.

## Guiding Rules

- Do not use real customer, employee, shipment, vehicle, or location-sensitive operational data.
- Keep generated identifiers clearly synthetic.
- Model relationships consistently across domains.
- Preserve edge cases such as delayed shipments, depot congestion, maintenance incidents, returns, and customer escalations.
- Include classification metadata so governance examples can be meaningful.
- Version synthetic datasets and generation logic when they are added.

## Core Entities

- `customer_account`
- `shipment`
- `shipment_event`
- `route`
- `depot`
- `vehicle`
- `maintenance_work_order`
- `support_case`
- `disruption_event`
- `contract_service_level`

## Workload Support

Transactional workloads should exercise relational integrity, indexing, performance tuning, HA/DR, and operational automation.

Analytical workloads should support medallion processing, conformed dimensions, fact tables, data quality, late-arriving data, and lineage.

AI workloads should support grounded retrieval over shipment status, support cases, service-level commitments, disruption explanations, and operational knowledge articles.

