# SQL Database Release Rollback

Use this runbook when a `legacy_tms` database release fails validation after deployment.

## Scope

This runbook covers schema releases produced from the SQL project dacpac. It does not cover application rollback, bulk data repair, or Databricks pipeline rollback.

## Steps

1. Stop the promotion workflow and prevent further publishes to the environment.
2. Capture the failed release manifest, deployment report, deployment script, and current incident notes.
3. Classify the failure as schema incompatibility, permission regression, reference-data issue, or performance regression.
4. Prefer a forward fix when the failure is small and data-compatible.
5. Restore to the approved backup or restore point when data loss, destructive drift, or broad application failure is present.
6. Re-run smoke tests, security checks, and performance gates before reopening promotion.
7. Back-port any approved hotfix into the SQL project before the next release.

## Evidence Required

- Release manifest from `outputs/sql_cicd/release_manifest.json`.
- Dacpac identifier and deployment report.
- Backup or restore point identifier from the target environment.
- Decision record for forward fix or restore.

