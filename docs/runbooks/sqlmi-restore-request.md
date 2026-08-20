# SQL MI Restore Request

## Trigger

Restore request, suspected data loss, or recovery drill.

## Triage

- Confirm restore reason, source database, target point in time, and business owner approval.
- Confirm retention availability and target environment.
- Confirm no active migration/cutover conflict.

## Evidence

- Request approval.
- Required restore point.
- Expected validation queries.
- Post-restore reconciliation result.

## Action

- In Azure, execute PITR or restore procedure through approved tooling.
- Locally, Milestone 6 only validates the runbook and evidence requirements.

## Escalation

Escalate if requested restore point is outside retention or business impact is Sev1.

## Validation

- Database online.
- Row-count sanity checks pass.
- Critical procedures compile.
- Business owner accepts restored point.

## Closure

Record restore timeline, validation, requester sign-off, and retention follow-up.

