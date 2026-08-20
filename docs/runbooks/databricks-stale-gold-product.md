# Databricks Stale Gold Product

## Trigger

Gold product exceeds freshness breach threshold.

## Triage

Identify upstream Bronze/Silver status, quality gates, job run history, SQL warehouse status, and source availability.

## Evidence

Use pipeline observability, quality results, job history, and query history.

## Remediation

Fix upstream failure, rerun from validated Silver, and keep publication blocked if critical gates fail.

## Validation

Confirm Gold max metric date and consumer freshness recover.

## Escalation

Escalate high-criticality product breach to analytics owner and business owner.

## Closure

Record affected product, cause, rerun id, and freshness recovery time.

