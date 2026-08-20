from __future__ import annotations

import hashlib
from pathlib import Path

from databricks_operations.catalog import (
    ALERTS,
    CLUSTER_POLICIES,
    COMPUTE_OPTIMIZATION,
    COST_ALLOCATION,
    COST_CONTROLS,
    DELTA_HEALTH,
    JOB_HEALTH,
    MONITORING,
    PIPELINE_OBSERVABILITY,
    READINESS,
    SLOS,
    SPARK_TROUBLESHOOTING,
    STREAMING_HEALTH,
    TRACEABILITY,
)
from databricks_operations.cli import generate_outputs
from databricks_operations.validation import validate_outputs

ROOT = Path(__file__).resolve().parents[1]


def _digest_tree(path: Path) -> str:
    digest = hashlib.sha256()
    for file_path in sorted(path.rglob("*")):
        if file_path.is_file():
            digest.update(str(file_path.relative_to(path)).encode("utf-8"))
            digest.update(file_path.read_bytes())
    return digest.hexdigest()


def test_monitoring_catalog_covers_critical_databricks_plane() -> None:
    workloads = {item.workload for item in MONITORING}
    assert "batch feeds" in workloads
    assert "relational increments" in workloads
    assert "shipment events" in workloads
    assert "Gold publication" in workloads
    assert any("system tables" in item.monitoring_source for item in MONITORING)
    assert not any(
        item.evidence_classification == "locally validated"
        and "runtime metrics" in item.monitoring_source
        for item in MONITORING
    )


def test_job_health_and_pipeline_observability_are_mapped() -> None:
    assert all(rule.runbook.startswith("docs/runbooks/") for rule in JOB_HEALTH)
    assert {stage.stage for stage in PIPELINE_OBSERVABILITY} >= {
        "source",
        "Bronze",
        "Silver",
        "Gold",
        "publication",
    }


def test_spark_delta_and_streaming_health_controls_are_specific() -> None:
    assert any(item.symptom == "skew" for item in SPARK_TROUBLESHOOTING)
    assert any("broadcast" in item.safe_remediation for item in SPARK_TROUBLESHOOTING)
    assert any("VACUUM" in item.recommendation for item in DELTA_HEALTH)
    assert any("predictive optimization" in item.area for item in DELTA_HEALTH)
    assert any("checkpoint" in rule.condition for rule in STREAMING_HEALTH)
    assert not any(
        "delete production checkpoints" in rule.threshold_or_detection
        for rule in STREAMING_HEALTH
    )


def test_compute_policies_and_cost_controls_are_production_minded() -> None:
    assert {"jobs compute", "serverless jobs or jobs compute", "SQL warehouse"} <= {
        item.area for item in COMPUTE_OPTIMIZATION
    }
    assert any(policy.control == "tags" for policy in CLUSTER_POLICIES)
    assert {"environment", "workspace", "job", "compute type", "domain"} <= {
        item.dimension for item in COST_ALLOCATION
    }
    assert {"preventive", "detective", "corrective"} <= {item.area for item in COST_CONTROLS}


def test_alerts_slos_and_traceability_are_complete() -> None:
    assert all(alert.runbook.startswith("docs/runbooks/") for alert in ALERTS)
    assert any(alert.condition == "checkpoint issue" for alert in ALERTS)
    assert any(alert.condition == "unusual usage/cost" for alert in ALERTS)
    assert {slo.workload for slo in SLOS} >= {
        "shipment event processing",
        "operational shipment Gold",
        "billing Gold",
        "service/incident Gold",
    }
    assert all(item.alert.startswith("alert-") for item in TRACEABILITY)
    assert all(item.runbook.startswith("docs/runbooks/") for item in TRACEABILITY)


def test_readiness_does_not_fake_runtime_validation() -> None:
    assert any(
        item.evidence_classification == "requires Databricks validation"
        for item in READINESS
    )
    assert not any(item.evidence_classification == "blocked" for item in READINESS)


def test_outputs_generate_validate_and_are_deterministic(tmp_path: Path) -> None:
    first = tmp_path / "first"
    second = tmp_path / "second"
    generate_outputs(first / "outputs" / "databricks_operations", first / "reports", ROOT)
    generate_outputs(second / "outputs" / "databricks_operations", second / "reports", ROOT)
    assert _digest_tree(first) == _digest_tree(second)
    assert validate_outputs(first / "outputs" / "databricks_operations", ROOT) == []
