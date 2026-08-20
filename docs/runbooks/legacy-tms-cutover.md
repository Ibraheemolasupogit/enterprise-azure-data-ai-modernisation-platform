# Legacy TMS Cutover Runbook

## Entry Criteria

- Wave 0 prerequisites complete.
- Compatibility blockers triaged.
- Backup and rollback evidence available.
- Application owners approve write freeze window.
- Local migration factory evidence reviewed.

## Cutover Steps

1. Announce freeze checkpoint.
2. Quiesce application writes.
3. Complete final delta synchronization.
4. Run PRE-CUTOVER validation gates.
5. Confirm rollback readiness.
6. Switch application connection configuration in the real environment.
7. Run smoke checks for customer lookup, shipment creation, status update, and reporting placeholder.
8. Hold go/no-go checkpoint.
9. Capture evidence and sign-off.

Milestone 5 does not perform real DNS or application connection changes.

## Rollback Trigger

- Failed final reconciliation.
- Stale delta.
- Failed smoke check.
- Unexpected error-rate increase.
- Business owner no-go.

## Exit Criteria

- Required live gates passed in a real environment.
- Hypercare handover accepted.
- Rollback window decision recorded.

