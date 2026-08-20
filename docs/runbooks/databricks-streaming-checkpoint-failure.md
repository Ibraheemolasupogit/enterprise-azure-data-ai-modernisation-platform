# Databricks Streaming Checkpoint Failure

## Trigger

Streaming task fails repeatedly or checkpoint state appears stale or inconsistent.

## Triage

Pause the stream, preserve the checkpoint, inspect recent source files/events, and identify the last committed offset.

## Evidence

Collect task logs, checkpoint path, source event range, watermark state, and quarantine records.

## Remediation

Fix source or code issue before restarting. Do not delete or overwrite checkpoints without approval.

## Replay/Rerun

Use an isolated replay path for event ranges, then merge idempotently by event id.

## Validation

Run streaming quality gate and downstream Silver/Gold gates.

## Escalation

Escalate repeated checkpoint failures to platform lead.

## Closure

Record checkpoint decision, replay range, and validation evidence.

