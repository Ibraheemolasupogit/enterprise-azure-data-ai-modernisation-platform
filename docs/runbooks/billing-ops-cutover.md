# Billing Ops Cutover Runbook

## Entry Criteria

- Identifier mapping risk accepted or remediated.
- Invoice/payment reconciliation passed.
- Service-case workflow smoke checks prepared.
- Offline outage window approved.
- Rollback source reactivation plan approved.

## Cutover Steps

1. Announce billing/service freeze.
2. Stop source writes.
3. Execute final export and load in the real environment.
4. Run POST-LOAD validation.
5. Run invoice/payment reconciliation.
6. Switch application connection configuration.
7. Run invoice lookup, payment lookup, and case creation smoke checks.
8. Capture go/no-go decision.
9. Open hypercare window.

Milestone 5 only models these steps locally.

## Rollback Trigger

- Reconciliation failure.
- Duplicate key failure.
- Case workflow failure.
- Business owner no-go.

## Exit Criteria

- Finance owner accepts reconciliation.
- Service owner accepts workflow validation.
- Hypercare checks scheduled.

