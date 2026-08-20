# Databricks Backfill and Replay Request

## Trigger

A data owner requests historical reload, quarantine replay, or corrected-range processing.

## Triage

Confirm source range, target range, reason, expected volume, affected products, and current processing isolation.

## Evidence

Collect source manifests, contracts, quality rules, current target version, and rollback boundary.

## Remediation

Prepare a reviewed backfill plan with validation gates and owner approval.

## Replay/Rerun

Run the controlled backfill/replay workflow. Do not reset active streaming checkpoints.

## Validation

Reconcile counts, quality results, and Gold aggregates.

## Escalation

Escalate large-volume or production-impacting backfills to the platform lead.

## Closure

Record target versions, reconciliation, and downstream publication status.

