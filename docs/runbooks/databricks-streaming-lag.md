# Databricks Streaming Lag

## Trigger

Streaming input rate exceeds processing rate, watermark stalls, state grows, or lag breaches assumptions.

## Triage

Inspect source arrival rate, micro-batch duration, state size, late records, duplicates, and recent deploys.

## Evidence

Use Structured Streaming progress, checkpoint metadata, task logs, quarantine counts, and source event volume.

## Remediation

Resolve bad records, tune state/watermark logic, right-size compute, and replay only through approved isolated paths.

## Validation

Confirm watermark advances and lag returns within threshold.

## Escalation

Escalate repeated lag to streaming operator and platform lead.

## Closure

Record event range, checkpoint state, action, and validation.

