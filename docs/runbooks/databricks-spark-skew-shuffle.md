# Databricks Spark Skew and Shuffle Issue

## Trigger

Spark stages show skew, high shuffle, slow tasks, or repeated stage retries.

## Triage

Identify joins, aggregations, key distribution, partition sizes, and AQE behavior.

## Evidence

Use Spark UI stages, task time distribution, shuffle read/write, spill metrics, and query plan.

## Remediation

Filter earlier, broadcast small dimensions when justified, let AQE handle skew where possible, repartition by evidence, and avoid broad hints without plan evidence.

## Validation

Compare runtime, shuffle, and freshness after change in Databricks.

## Escalation

Escalate persistent skew on business keys to data modelling owner.

## Closure

Record affected query, keys, evidence, and approved remediation.

