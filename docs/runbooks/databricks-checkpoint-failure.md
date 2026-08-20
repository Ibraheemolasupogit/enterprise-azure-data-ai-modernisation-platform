# Databricks Checkpoint Failure

## Trigger

Checkpoint age or state indicates stalled, corrupt, or incompatible stream recovery.

## Triage

Pause the stream, preserve checkpoint contents, identify last committed offset and recent schema/code changes.

## Evidence

Collect checkpoint path, stream progress, task logs, source event range, and deployment version.

## Remediation

Do not delete production checkpoints by default. Fix code/schema issues first. Use isolated replay paths when checkpoint reset is approved.

## Validation

Restart safely, confirm no duplicate target records, and validate downstream freshness.

## Escalation

Escalate checkpoint reset requests to platform lead.

## Closure

Record reset decision, replay range, merge evidence, and downstream validation.

