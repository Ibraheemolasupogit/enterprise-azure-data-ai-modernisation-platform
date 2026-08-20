from __future__ import annotations

QUALITY_EXPECTATIONS = {
    "bronze_metadata_present": {
        "expression": (
            "_ingested_at_utc IS NOT NULL "
            "AND _source_system IS NOT NULL "
            "AND _record_hash IS NOT NULL"
        ),
        "mode": "expect_or_fail",
    },
    "shipment_business_keys_present": {
        "expression": (
            "shipment_id IS NOT NULL "
            "AND customer_id IS NOT NULL "
            "AND route_id IS NOT NULL"
        ),
        "mode": "expect_or_fail",
    },
    "shipment_status_valid": {
        "expression": (
            "shipment_status IN "
            "('created','assigned','in_transit','delayed','delivered','cancelled')"
        ),
        "mode": "expect_or_drop",
    },
    "delivery_delay_metric_valid": {
        "expression": "late_count <= delivered_count AND late_rate BETWEEN 0 AND 1",
        "mode": "expect_or_fail",
    },
    "service_case_email_valid": {
        "expression": "contact_email RLIKE '^[^@\\\\s]+@synthetic\\\\.contoso\\\\.example$'",
        "mode": "expect_or_drop",
    },
}


def expectation_mode(rule_id: str) -> str:
    return QUALITY_EXPECTATIONS[rule_id]["mode"]


def publication_allowed(critical_failures: int) -> bool:
    return critical_failures == 0
