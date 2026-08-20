# Infrastructure

Infrastructure is Bicep-first. Milestone 1 provides only the structure and parameterisation pattern; it does not define deployable enterprise resources yet.

## Layout

- `main.bicep`: future composition root.
- `modules/`: reusable capability modules.
- `parameters/`: environment-specific parameter placeholders.
- `scripts/`: future deployment helper scripts.

## Environment Pattern

Use one parameter file per environment:

- `parameters/dev.bicepparam`
- `parameters/test.bicepparam`
- `parameters/prod.bicepparam`

Secrets must be supplied through secure deployment mechanisms such as Key Vault references or federated CI/CD variables, never committed parameters.

