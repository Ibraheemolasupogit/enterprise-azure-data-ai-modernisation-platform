from __future__ import annotations

from fabric_integration.catalog import CONTRACT_FIELDS, PATTERN_DECISIONS, PRODUCTS
from fabric_integration.cli import (
    _boundary_matrix,
    _failure_matrix,
    _identity_access,
    _lineage_handoff,
    _publication_gate,
    _sensitivity_handoff,
    _versioning_policy,
)


def test_product_catalog_is_gold_only_and_complete() -> None:
    assert {product.gold_product for product in PRODUCTS} == {
        "gold.shipment_operations_performance",
        "gold.depot_route_performance",
        "gold.delivery_delay_metrics",
        "gold.billing_revenue_summary",
        "gold.service_incident_summary",
    }
    assert all(product.fabric_eligible.startswith("eligible") for product in PRODUCTS)
    assert not any(
        product.gold_product.startswith(("bronze.", "silver.")) for product in PRODUCTS
    )


def test_every_product_has_contract_and_pattern() -> None:
    product_ids = {product.product_id for product in PRODUCTS}
    product_names = {product.gold_product for product in PRODUCTS}
    assert product_names <= {field.dataset for field in CONTRACT_FIELDS}
    assert product_ids <= {decision.product_id for decision in PATTERN_DECISIONS}
    assert all(field.schema_version == "1.0.0" for field in CONTRACT_FIELDS)
    assert all(field.sensitivity for field in CONTRACT_FIELDS)


def test_publication_gate_and_lineage_cover_all_products() -> None:
    product_ids = {product.product_id for product in PRODUCTS}
    gates = _publication_gate()
    lineage = _lineage_handoff()
    assert product_ids == {row["product_id"] for row in gates}
    assert product_ids == {row["product_id"] for row in lineage}
    assert all("critical quality checks passed" in row["required_conditions"] for row in gates)
    assert all(
        "no fabricated end-to-end graph" in row["cross_platform_lineage_claim"]
        for row in lineage
    )


def test_identity_and_sensitivity_handoff_are_least_privilege() -> None:
    identities = _identity_access()
    assert all("SAS" not in row["preferred_auth"] for row in identities)
    assert all("storage account key" not in row["preferred_auth"].lower() for row in identities)
    assert any("no Bronze/Silver" in row["storage_boundary"] for row in identities)
    sensitivity = _sensitivity_handoff()
    assert {row["product_id"] for row in sensitivity} == {
        product.product_id for product in PRODUCTS
    }
    assert all("not claimed" in row["automatic_propagation_claim"] for row in sensitivity)


def test_failure_ownership_and_boundary_are_not_ambiguous() -> None:
    boundary = _boundary_matrix()
    assert {"Azure Data & AI platform", "Fabric platform", "Shared"} <= {
        row["owner"] for row in boundary
    }
    assert not any(row["owner"] == "ambiguous" for row in boundary)
    failures = _failure_matrix()
    assert any(row["owner"] == "Azure Data & AI platform" for row in failures)
    assert any(row["owner"] == "Fabric platform" for row in failures)
    assert any(row["owner"] == "Shared" for row in failures)


def test_versioning_policy_covers_compatibility_classes() -> None:
    assert {"backward compatible", "review required", "breaking"} <= {
        row["classification"] for row in _versioning_policy()
    }
