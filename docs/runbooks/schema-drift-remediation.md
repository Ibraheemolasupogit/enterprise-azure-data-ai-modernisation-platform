# Schema Drift Remediation

Use this runbook when a target database differs from the committed `legacy_tms` SQL project model.

## Steps

1. Generate a drift report from the target database and committed dacpac.
2. Classify each difference as approved hotfix, emergency operational change, unauthorized change, or tooling noise.
3. For approved hotfixes, add the change to the SQL project and rerun `make validate-sql-cicd`.
4. For unauthorized changes, prepare a reviewed remediation script or restore from the approved backup boundary.
5. For permission drift, remove direct grants and express access through project roles.
6. Do not auto-delete reference data unless the authoritative source and business owner approve the removal.
7. Store the drift report with the release evidence.

