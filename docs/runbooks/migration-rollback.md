# Migration Rollback Design

## Decision Window

Rollback is safest before target writes begin. After target write acceptance, divergence analysis is required before any cutback.

## Triggers

- Failed validation gate.
- Failed business smoke test.
- Stale delta or incomplete final synchronization.
- Unacceptable error rate.
- Data reconciliation failure.

## Strategy

- Reactivate source system only through an approved go/no-go decision.
- Preserve target evidence and write logs.
- Avoid reverse synchronization unless explicitly designed and tested.
- Restore application connection configuration through controlled change.
- Retain migration evidence for incident review.

## Divergence Risk

Minimal-downtime migrations are harder to roll back after cutover because both source and target may have accepted writes. That risk must be reviewed during the rollback decision window.

