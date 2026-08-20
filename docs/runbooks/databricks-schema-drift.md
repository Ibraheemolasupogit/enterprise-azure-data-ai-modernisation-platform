# Databricks Schema Drift

## Trigger

Auto Loader rescued data, contract validation, or parsing detects unexpected fields, type changes, or malformed JSON.

## Triage

Classify drift as additive, unexpected, dangerous type change, or malformed input.

## Evidence

Collect rescued data, source file, schema version, contract version, and affected pipeline task.

## Remediation

Additive drift can be reviewed and promoted through contract change. Dangerous type changes and malformed inputs remain quarantined.

## Replay/Rerun

Replay from landing after contract update. Preserve schema-location state unless a reset is explicitly approved.

## Validation

Run schema conformity and Silver quality gates.

## Escalation

Escalate dangerous source changes to the source owner and governance reviewer.

## Closure

Record contract version and replay evidence.

