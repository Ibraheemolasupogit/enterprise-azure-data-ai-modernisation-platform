# Environment Strategy

## Environment Separation

The repository is structured for `dev`, `test`, and `prod` from the start. Milestone 1 includes parameter placeholders only; it does not deploy resources.

| Environment | Intent | Promotion expectation |
| --- | --- | --- |
| `dev` | Developer iteration, synthetic data, low-cost settings | Pull request validation and local checks |
| `test` | Integrated platform validation and release rehearsal | Automated deployment from approved branches |
| `prod` | Production-grade reference target | Controlled promotion with documented rollback |

## Configuration Rules

- Shared resource definitions belong in reusable modules.
- Environment-specific values belong in parameter files.
- Secrets are never stored in parameter files.
- Naming should include workload, environment, region, and resource role once implementation begins.
- Drift detection and policy checks should be added before real infrastructure promotion.

