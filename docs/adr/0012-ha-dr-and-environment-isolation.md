# ADR-0012: HA/DR and Environment Isolation

- Status: Accepted
- Date: 2026-08-20

## Context

Milestone 3 established criticality, RTO/RPO assumptions, and migration-wave risk. Milestone 4 must translate those into target architecture principles without claiming DR has been tested.

## Decision

Use tiered recovery objectives and environment isolation. Dev, test, and prod remain separate configuration and security boundaries. Production requires explicit backup, HA, monitoring, rollback, and recovery validation before migration.

## Consequences

Architecture can be implemented through Bicep later with environment parameters and promotion gates. Exact HA/DR configuration remains subject to live validation and cost trade-offs.

## Alternatives Considered

- One-size-fits-all HA/DR: rejected because feed, analytical, billing, and OLTP tiers have different recovery needs.
- Single shared environment: rejected because production protections and promotion evidence are required.

