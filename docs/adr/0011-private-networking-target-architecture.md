# ADR-0011: Private Networking Target Architecture

- Status: Accepted
- Date: 2026-08-20

## Context

The target platform spans operational databases, storage, Databricks, Key Vault, monitoring, applications, CI/CD, and administrative access. Production data-plane exposure should be restricted.

## Decision

Use private connectivity as the production target: VNet segmentation, SQL MI delegated subnet, private endpoints, Private DNS, controlled administration, and restricted egress. Portfolio/dev environments may use documented simplifications where needed.

## Consequences

This improves security posture but increases DNS, routing, firewall, and operational complexity. Later IaC milestones must parameterise networking cleanly by environment.

## Alternatives Considered

- Public endpoints for production: rejected for the target architecture.
- Force full private networking for local development: rejected because it would make portfolio validation unnecessarily difficult.

