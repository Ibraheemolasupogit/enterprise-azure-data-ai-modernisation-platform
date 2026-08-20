# ADR-0005: Bicep Infrastructure as Code

- Status: Accepted
- Date: 2026-08-20

## Context

The platform is Azure-native and needs readable, source-controlled infrastructure definitions that can later support environment parameterisation, CI/CD gates, policy checks, and repeatable deployment.

## Decision

Use Bicep as the default Infrastructure as Code language for Azure resources. Structure modules by platform capability and keep environment-specific values in parameter files.

## Consequences

Bicep keeps Azure resource modelling explicit and close to ARM semantics. The repository can later add What-If validation, policy checks, and deployment workflows. If a future component has a strong reason to use another tool, that decision must be captured in a new ADR.

## Alternatives Considered

- Terraform: strong multi-cloud ecosystem, but this repository is intentionally Azure-focused and does not need provider abstraction at this stage.
- ARM JSON: native but verbose and harder to maintain.
- Manual portal deployment: not repeatable or reviewable enough for the platform goals.

