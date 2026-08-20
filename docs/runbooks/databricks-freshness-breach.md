# Databricks Freshness Breach

## Trigger

A dataset exceeds its freshness breach threshold.

## Triage

Identify last successful task, source arrival time, checkpoint lag, and downstream Gold impact.

## Evidence

Collect schedule matrix row, latest job run, quality result freshness status, and source manifest.

## Remediation

Resolve source delay, restart transient failures, or pause publication if Silver/Gold freshness is unreliable.

## Replay/Rerun

Rerun from the last safe checkpoint or batch manifest.

## Validation

Confirm freshness status returns within threshold and dependent Gold products are refreshed.

## Escalation

Escalate to source owner and platform operator when breach exceeds business-impact threshold.

## Closure

Record breach duration, impacted products, and remediation.

