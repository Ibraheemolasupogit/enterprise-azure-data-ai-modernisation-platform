from __future__ import annotations

import re
from datetime import datetime
from typing import Any

EMAIL_PATTERN = re.compile(r"^[^@\s]+@synthetic\.contoso\.example$")
EVENT_TYPES = {"created", "allocated", "departed", "arrived", "delivered", "exception"}


def is_iso_timestamp(value: str) -> bool:
    try:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return False
    return True


def validate_operational_event(record: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    required = {
        "event_id",
        "event_type",
        "aggregate_type",
        "aggregate_id",
        "occurred_at",
        "schema_version",
        "payload",
    }
    missing = required - set(record)
    if missing:
        errors.append(f"missing fields: {sorted(missing)}")
    if record.get("event_type") not in EVENT_TYPES:
        errors.append("unknown event_type")
    if record.get("aggregate_type") != "shipment":
        errors.append("aggregate_type must be shipment")
    if not str(record.get("aggregate_id", "")).startswith("SHP"):
        errors.append("aggregate_id must use SHP identifier")
    if not is_iso_timestamp(str(record.get("occurred_at", ""))):
        errors.append("occurred_at must be ISO-8601")
    if not isinstance(record.get("payload"), dict):
        errors.append("payload must be an object")
    return errors


def validate_depot_feed_row(record: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for field in ("depot_code", "depot_name", "region", "capacity_units", "feed_version"):
        if field not in record:
            errors.append(f"missing {field}")
    if record.get("capacity_units") not in ("", None):
        try:
            int(str(record["capacity_units"]))
        except ValueError:
            errors.append("capacity_units must be numeric when present")
    return errors

