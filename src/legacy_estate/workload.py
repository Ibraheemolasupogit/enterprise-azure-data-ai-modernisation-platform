from __future__ import annotations

import argparse
import json
import random
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

from legacy_estate.config import DEFAULT_SEED

WORKLOAD_TYPES = (
    "customer_lookup",
    "create_shipment",
    "update_shipment_status",
    "invoice_lookup",
    "route_depot_reporting",
    "incident_case_creation",
    "analytical_delay_report",
)


def generate_workload(
    output_path: Path | None = None,
    operations: int = 50,
    seed: int = DEFAULT_SEED,
) -> list[dict[str, Any]]:
    rng = random.Random(seed)
    base_time = datetime(2026, 1, 2, 8, 0, tzinfo=UTC)
    rows = []
    for idx in range(operations):
        workload_type = rng.choices(
            WORKLOAD_TYPES,
            weights=(22, 16, 22, 12, 10, 10, 8),
        )[0]
        rows.append(_operation(idx + 1, workload_type, base_time, rng))

    if output_path is not None:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(
            "".join(json.dumps(row, sort_keys=True) + "\n" for row in rows),
            encoding="utf-8",
        )
    return rows


def _operation(
    sequence: int,
    workload_type: str,
    base_time: datetime,
    rng: random.Random,
) -> dict[str, Any]:
    occurred_at = base_time + timedelta(seconds=sequence * rng.randint(3, 25))
    customer_id = f"CUST{rng.randint(1, 120):06d}"
    shipment_id = f"SHP{rng.randint(1, 1_000):09d}"
    operation = {
        "operation_id": f"WL{sequence:010d}",
        "workload_type": workload_type,
        "occurred_at": occurred_at.isoformat().replace("+00:00", "Z"),
        "classification": _classification(workload_type),
        "candidate_cdc_source": workload_type
        in {"create_shipment", "update_shipment_status", "incident_case_creation"},
    }
    if workload_type == "customer_lookup":
        operation["parameters"] = {"customer_id": customer_id, "include_open_shipments": True}
    elif workload_type == "create_shipment":
        operation["parameters"] = {
            "customer_id": customer_id,
            "route_id": f"ROUTE{rng.randint(1, 60):05d}",
            "declared_value_gbp": round(rng.uniform(50, 5_000), 2),
        }
    elif workload_type == "update_shipment_status":
        operation["parameters"] = {
            "shipment_id": shipment_id,
            "new_status": rng.choice(("allocated", "in_transit", "delayed", "delivered")),
        }
    elif workload_type == "invoice_lookup":
        operation["parameters"] = {"invoice_id": f"INV{rng.randint(1, 1_000):09d}"}
    elif workload_type == "route_depot_reporting":
        operation["parameters"] = {"depot_id": f"DEPOT{rng.randint(1, 12):03d}", "window_hours": 24}
    elif workload_type == "incident_case_creation":
        operation["parameters"] = {
            "shipment_id": shipment_id,
            "case_reason": rng.choice(("late_delivery", "damaged_goods", "invoice_query")),
        }
    else:
        operation["parameters"] = {"report_date": "2026-01-02", "group_by": "route"}
    return operation


def _classification(workload_type: str) -> str:
    if workload_type in {"route_depot_reporting"}:
        return "operational_reporting"
    if workload_type in {"analytical_delay_report"}:
        return "candidate_analytical"
    return "oltp"


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate deterministic workload operations.")
    parser.add_argument("--operations", type=int, default=50)
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    parser.add_argument(
        "--output-path",
        type=Path,
        default=Path("data/raw/legacy_estate/workload.jsonl"),
    )
    args = parser.parse_args()
    rows = generate_workload(args.output_path, args.operations, args.seed)
    print(json.dumps({"operations": len(rows), "output_path": str(args.output_path)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
