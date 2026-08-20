from __future__ import annotations

import csv
import hashlib
import json
import re
from collections import defaultdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

VALID_SHIPMENT_STATUSES = {
    "created",
    "allocated",
    "assigned",
    "departed",
    "arrived",
    "in_transit",
    "delayed",
    "exception",
    "delivered",
    "cancelled",
}
EMAIL_PATTERN = re.compile(r"^[^@\s]+@synthetic\.contoso\.example$")


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def read_json_array(path: Path) -> list[dict[str, Any]]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def bronze_rows(
    records: list[dict[str, Any]],
    source_system: str,
    source_entity: str,
    schema_version_field: str = "schema_version",
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for ordinal, record in enumerate(records, start=1):
        payload = json.dumps(record, sort_keys=True)
        rows.append(
            {
                **record,
                "_source_system": source_system,
                "_source_entity": source_entity,
                "_ingested_at_utc": "2026-01-01T00:00:00Z",
                "_source_ordinal": ordinal,
                "_schema_version": str(record.get(schema_version_field, "1")),
                "_record_hash": stable_hash(payload),
                "_raw_payload": payload,
            }
        )
    return rows


def normalize_status(value: str) -> str:
    normalized = value.strip().lower().replace(" ", "_")
    aliases = {"allocated": "assigned", "exception": "delayed"}
    return aliases.get(normalized, normalized)


def parse_timestamp(value: str) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def stable_hash(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def transform_shipments(
    shipment_rows: list[dict[str, str]],
    customer_rows: list[dict[str, str]],
    route_rows: list[dict[str, str]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    customers = {row["customer_id"] for row in customer_rows}
    routes = {row["route_id"] for row in route_rows}
    accepted: list[dict[str, Any]] = []
    quarantine: list[dict[str, Any]] = []
    seen: set[str] = set()
    for row in shipment_rows:
        errors: list[str] = []
        shipment_id = row.get("shipment_id", "")
        if not shipment_id:
            errors.append("missing shipment_id")
        if shipment_id in seen:
            errors.append("duplicate shipment_id")
        seen.add(shipment_id)
        if row.get("customer_id") not in customers:
            errors.append("unknown customer_id")
        if row.get("route_id") not in routes:
            errors.append("unknown route_id")
        status = normalize_status(row.get("shipment_status", ""))
        if status not in VALID_SHIPMENT_STATUSES:
            errors.append("invalid shipment_status")
        created_at = parse_timestamp(row.get("created_at", ""))
        promised_at = parse_timestamp(row.get("promised_delivery_at", ""))
        delivered_at = parse_timestamp(row.get("delivered_at", ""))
        if created_at is None:
            errors.append("invalid created_at")
        if promised_at is None:
            errors.append("invalid promised_delivery_at")
        try:
            declared_value = float(row.get("declared_value_gbp", ""))
        except ValueError:
            declared_value = -1.0
        if declared_value < 0:
            errors.append("negative or invalid declared_value_gbp")
        if errors:
            quarantine.append(
                {"source": "legacy_tms.shipments", "business_key": shipment_id, "errors": errors}
            )
            continue
        accepted.append(
            {
                "shipment_id": shipment_id,
                "customer_id": row["customer_id"],
                "route_id": row["route_id"],
                "assigned_vehicle_id": row.get("assigned_vehicle_id", ""),
                "external_order_ref": row["external_order_ref"],
                "shipment_status": status,
                "created_at_utc": created_at.isoformat(),
                "promised_delivery_at_utc": promised_at.isoformat(),
                "delivered_at_utc": delivered_at.isoformat() if delivered_at else "",
                "declared_value_gbp": round(declared_value, 2),
                "hazmat_flag": row.get("hazmat_flag", "").lower() == "true",
            }
        )
    return accepted, quarantine


def transform_depots(
    feed_rows: list[dict[str, str]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    accepted: list[dict[str, Any]] = []
    quarantine: list[dict[str, Any]] = []
    for row in feed_rows:
        errors: list[str] = []
        depot_code = row.get("depot_code", "")
        if not depot_code:
            errors.append("missing depot_code")
        capacity_raw = row.get("capacity_units", "")
        capacity_units: int | None
        if capacity_raw in {"", None}:
            capacity_units = None
            errors.append("missing capacity_units")
        else:
            try:
                capacity_units = int(capacity_raw)
            except ValueError:
                capacity_units = None
                errors.append("invalid capacity_units")
        if errors:
            quarantine.append(
                {"source": "depot_reference_feed", "business_key": depot_code, "errors": errors}
            )
        accepted.append(
            {
                "depot_code": depot_code,
                "depot_name": row.get("depot_name", "").strip(),
                "region": row.get("region", "").strip().lower(),
                "capacity_units": capacity_units,
                "feed_version": row.get("feed_version", ""),
            }
        )
    return accepted, quarantine


def transform_service_cases(
    case_rows: list[dict[str, str]],
    shipment_rows: list[dict[str, str]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    shipment_ids = {row["shipment_id"] for row in shipment_rows}
    accepted: list[dict[str, Any]] = []
    quarantine: list[dict[str, Any]] = []
    for row in case_rows:
        errors: list[str] = []
        case_id = row.get("case_id", "")
        if row.get("shipment_id") not in shipment_ids:
            errors.append("unknown shipment_id")
        email = row.get("contact_email", "")
        if email and not EMAIL_PATTERN.match(email):
            errors.append("invalid contact_email")
        opened_at = parse_timestamp(row.get("opened_at", ""))
        if opened_at is None:
            errors.append("invalid opened_at")
        record = {
            "case_id": case_id,
            "customer_id": row.get("customer_id", ""),
            "shipment_id": row.get("shipment_id", ""),
            "case_reason": row.get("case_reason", ""),
            "case_status": row.get("case_status", "").lower(),
            "opened_at_utc": opened_at.isoformat() if opened_at else "",
            "closed_at_utc": row.get("closed_at", ""),
            "contact_email": email,
        }
        if errors:
            quarantine.append(
                {"source": "billing_ops.service_cases", "business_key": case_id, "errors": errors}
            )
        else:
            accepted.append(record)
    return accepted, quarantine


def deduplicate_events(
    events: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    accepted: list[dict[str, Any]] = []
    quarantine: list[dict[str, Any]] = []
    seen: set[str] = set()
    latest_by_shipment: dict[str, datetime] = {}
    for event in events:
        errors: list[str] = []
        event_id = str(event.get("event_id", ""))
        if event_id in seen:
            errors.append("duplicate event_id")
        seen.add(event_id)
        occurred_at = parse_timestamp(str(event.get("occurred_at", "")))
        shipment_id = str(event.get("aggregate_id", ""))
        if occurred_at is None:
            errors.append("invalid occurred_at")
        previous = latest_by_shipment.get(shipment_id)
        if occurred_at and previous and occurred_at < previous:
            errors.append("late or out-of-order event")
        if occurred_at and (previous is None or occurred_at > previous):
            latest_by_shipment[shipment_id] = occurred_at
        if errors:
            quarantine.append(
                {
                    "source": "shipment_operational_events",
                    "business_key": event_id,
                    "errors": errors,
                }
            )
            continue
        accepted.append(
            {
                "event_id": event_id,
                "shipment_id": shipment_id,
                "event_type": normalize_status(str(event.get("event_type", ""))),
                "occurred_at_utc": occurred_at.isoformat() if occurred_at else "",
                "schema_version": int(event.get("schema_version", 1)),
                "payload_hash": stable_hash(json.dumps(event.get("payload", {}), sort_keys=True)),
            }
        )
    return accepted, quarantine


def detect_carrier_schema_drift(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    expected = {
        "carrier_update_id": str,
        "external_order_ref": str,
        "partner_code": str,
        "partner_status": str,
        "schema_version": int,
        "update_timestamp": str,
    }
    drift: list[dict[str, Any]] = []
    for record in records:
        unexpected = sorted(set(record) - set(expected))
        changed_type = [
            field
            for field, expected_type in expected.items()
            if field in record and not isinstance(record[field], expected_type)
        ]
        if unexpected:
            drift.append(
                {
                    "carrier_update_id": record.get("carrier_update_id", ""),
                    "drift_type": "additive field",
                    "fields": unexpected,
                    "behavior": "rescue and evolve after review",
                }
            )
        if changed_type:
            drift.append(
                {
                    "carrier_update_id": record.get("carrier_update_id", ""),
                    "drift_type": "changed type",
                    "fields": changed_type,
                    "behavior": "quarantine and fail contract validation",
                }
            )
    return drift


def scd_type2_customer_dimension(
    prior_rows: list[dict[str, Any]],
    incoming_rows: list[dict[str, Any]],
    effective_at: str,
) -> list[dict[str, Any]]:
    result = [dict(row) for row in prior_rows]
    current_by_key = {
        row["customer_id"]: row
        for row in result
        if row.get("is_current") is True
    }
    next_key = 1 + max((int(row["customer_sk"]) for row in result), default=0)
    for incoming in incoming_rows:
        business_key = incoming["customer_id"]
        change_hash = stable_hash(
            "|".join(
                str(incoming.get(field, ""))
                for field in ("account_number", "legal_name", "service_tier", "billing_region")
            )
        )
        current = current_by_key.get(business_key)
        if current and current.get("change_hash") == change_hash:
            continue
        if current:
            current["effective_end_utc"] = effective_at
            current["is_current"] = False
        new_row = {
            "customer_sk": next_key,
            "customer_id": business_key,
            "account_number": incoming["account_number"],
            "legal_name": incoming["legal_name"],
            "service_tier": incoming["service_tier"],
            "billing_region": incoming["billing_region"],
            "effective_start_utc": effective_at,
            "effective_end_utc": "9999-12-31T00:00:00Z",
            "is_current": True,
            "change_hash": change_hash,
        }
        next_key += 1
        result.append(new_row)
        current_by_key[business_key] = new_row
    return result


def shipment_operations_gold(shipments: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[tuple[str, str], dict[str, Any]] = {}
    for row in shipments:
        created_day = row["created_at_utc"][:10]
        key = (created_day, row["shipment_status"])
        group = grouped.setdefault(
            key,
            {
                "metric_date": created_day,
                "shipment_status": row["shipment_status"],
                "shipment_count": 0,
            },
        )
        group["shipment_count"] += 1
    return sorted(grouped.values(), key=lambda item: (item["metric_date"], item["shipment_status"]))


def delivery_delay_gold(shipments: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[str, dict[str, Any]] = defaultdict(
        lambda: {"metric_date": "", "delivered_count": 0, "late_count": 0}
    )
    for row in shipments:
        if not row["delivered_at_utc"]:
            continue
        delivered = parse_timestamp(row["delivered_at_utc"])
        promised = parse_timestamp(row["promised_delivery_at_utc"])
        if delivered is None or promised is None:
            continue
        metric_date = delivered.date().isoformat()
        group = grouped[metric_date]
        group["metric_date"] = metric_date
        group["delivered_count"] += 1
        if delivered > promised:
            group["late_count"] += 1
    for group in grouped.values():
        delivered_count = group["delivered_count"]
        group["late_rate"] = (
            round(group["late_count"] / delivered_count, 4) if delivered_count else 0
        )
    return sorted(grouped.values(), key=lambda item: item["metric_date"])


def billing_revenue_gold(invoices: list[dict[str, str]]) -> list[dict[str, Any]]:
    grouped: dict[str, dict[str, Any]] = {}
    for row in invoices:
        invoice_month = row["invoice_date"][:7]
        group = grouped.setdefault(
            invoice_month,
            {"invoice_month": invoice_month, "invoice_count": 0, "net_revenue_gbp": 0.0},
        )
        group["invoice_count"] += 1
        if row["invoice_status"] != "void":
            group["net_revenue_gbp"] += float(row["net_amount_gbp"])
    for group in grouped.values():
        group["net_revenue_gbp"] = round(group["net_revenue_gbp"], 2)
    return sorted(grouped.values(), key=lambda item: item["invoice_month"])


def current_utc_marker() -> str:
    return datetime(2026, 1, 1, tzinfo=UTC).isoformat().replace("+00:00", "Z")
