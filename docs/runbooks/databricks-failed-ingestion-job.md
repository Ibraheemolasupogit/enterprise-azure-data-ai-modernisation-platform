# Databricks Failed Ingestion Job

## Trigger

An ingestion task fails or misses its freshness threshold.

## Triage

Identify source, workflow, task key, processing date, checkpoint path, and latest source availability.

## Evidence

Collect job run id, task logs, source manifest, checkpoint state, quality result row, and quarantine records.

## Remediation

Retry only transient source or platform failures. For malformed files or schema drift, quarantine and request source-owner review.

## Replay/Rerun

Rerun the failed task when idempotency key and checkpoint state are safe. Use controlled replay for partial batches.

## Validation

Re-run Bronze and Silver quality gates before allowing downstream Gold tasks.

## Escalation

Escalate repeated failures to platform operator and source owner.

## Closure

Record cause, action, rerun id, and quality evidence.

