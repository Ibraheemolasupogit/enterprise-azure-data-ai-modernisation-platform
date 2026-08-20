from __future__ import annotations

from final_assurance.catalog import CAPABILITIES, DATA_PRODUCTS, FAILURE_MODES, SECURITY_CONTROLS
from final_assurance.cli import (
    _architecture_traceability,
    _gap_register,
    _observability_assurance,
    _ownership_matrix,
    _release_readiness,
    _runbook_catalog,
    _truth_matrix,
)


def test_capability_inventory_covers_major_domains() -> None:
    domains = {row[1] for row in CAPABILITIES}
    assert {
        "assessment",
        "architecture",
        "migration",
        "Azure SQL",
        "Databricks",
        "AI-enabled SQL",
        "API integration",
        "Fabric boundary",
        "FinOps",
    } <= domains
    assert all(row[4] for row in CAPABILITIES)


def test_architecture_traceability_has_no_orphan_implementation() -> None:
    rows = _architecture_traceability()
    assert rows
    assert all(row["requirement"] for row in rows)
    assert all(row["implementation"] for row in rows)
    assert all(row["evidence"] for row in rows)


def test_ownership_and_security_are_explicit() -> None:
    ownership = _ownership_matrix()
    assert not any(row["owner"] == "ambiguous" for row in ownership)
    assert {row["service"] for row in ownership} >= {
        "Azure SQL",
        "Databricks",
        "API layer",
        "Fabric consumer boundary",
    }
    assert {row[0] for row in SECURITY_CONTROLS} >= {
        "Entra ID",
        "managed identities",
        "database roles",
        "API authorization",
        "MCP allowlisting",
    }


def test_data_products_and_failure_modes_are_mapped() -> None:
    assert {row[0] for row in DATA_PRODUCTS} >= {
        "shipment operations",
        "delivery delays",
        "billing/revenue",
        "AI grounding corpus",
    }
    assert all(row[4] for row in DATA_PRODUCTS)
    assert {row[0] for row in FAILURE_MODES} >= {
        "Azure SQL outage",
        "Databricks job failure",
        "Azure OpenAI unavailable",
        "Fabric handoff failure",
    }


def test_observability_maps_to_runbooks() -> None:
    runbooks = {row["runbook_path"] for row in _runbook_catalog()}
    assert "docs/runbooks/databricks-job-failure.md" in runbooks
    assert "docs/fabric-integration-boundary.md" in runbooks
    assert all(row["runbook"] for row in _observability_assurance())


def test_truth_gaps_and_release_gates_are_honest() -> None:
    truth = {row["truth_category"] for row in _truth_matrix()}
    assert {
        "Implemented locally",
        "Configuration defined",
        "Requires Azure validation",
        "Requires Databricks validation",
        "Requires Fabric validation",
        "Deferred/blocked",
    } <= truth
    gaps = {row["gap"] for row in _gap_register()}
    assert "Azure OpenAI invocation" in gaps
    assert "Fabric shortcut validation" in gaps
    readiness = _release_readiness()
    assert any(row["gate_status"] == "CONDITIONAL" for row in readiness)
    assert not any("production deployment approval" in row["gate_status"] for row in readiness)

