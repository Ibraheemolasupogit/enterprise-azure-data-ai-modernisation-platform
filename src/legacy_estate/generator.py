from __future__ import annotations

import argparse
import csv
import json
import random
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

from legacy_estate.config import DEFAULT_SEED, PROFILE_SPECS

BASE_TIME = datetime(2026, 1, 1, 8, 0, tzinfo=UTC)
SERVICE_TIERS = ("standard", "priority", "critical")
SHIPMENT_STATUSES = ("created", "allocated", "in_transit", "delayed", "delivered", "cancelled")
CASE_REASONS = ("late_delivery", "damaged_goods", "invoice_query", "address_change", "lost_item")
PAYMENT_METHODS = ("bank_transfer", "card", "direct_debit")


def generate_estate(
    output_dir: Path,
    profile_name: str = "tiny",
    seed: int = DEFAULT_SEED,
    include_defects: bool = True,
) -> dict[str, Any]:
    """Generate deterministic synthetic source-system files and return a manifest."""

    if profile_name not in PROFILE_SPECS:
        valid = ", ".join(sorted(PROFILE_SPECS))
        raise ValueError(f"Unknown profile '{profile_name}'. Valid profiles: {valid}")

    profile = PROFILE_SPECS[profile_name]
    rng = random.Random(seed)
    output_dir.mkdir(parents=True, exist_ok=True)

    customers = _customers(profile.customers, rng)
    depots = _depots(profile.depots)
    routes = _routes(depots)
    vehicles = _vehicles(profile.vehicles, depots, rng)
    shipments = _shipments(profile.shipments, customers, routes, vehicles, rng)
    shipment_events = _shipment_events(shipments, profile.event_multiplier, rng, include_defects)
    invoices = _invoices(shipments, rng)
    payments = _payments(invoices, profile.payment_ratio, rng)
    cases = _cases(profile.cases, customers, shipments, rng, include_defects)
    case_notes = _case_notes(cases, rng)
    depot_feed = _depot_reference_feed(depots, include_defects)
    carrier_updates = _carrier_updates(shipments, rng, include_defects)
    operational_events = _operational_events(shipment_events, rng, include_defects)
    anomalies = _anomaly_catalog(include_defects)

    tables_dir = output_dir / "legacy_oltp"
    files_dir = output_dir / "file_feeds"
    events_dir = output_dir / "events"
    secondary_dir = output_dir / "secondary_billing"
    for directory in (tables_dir, files_dir, events_dir, secondary_dir):
        directory.mkdir(parents=True, exist_ok=True)

    _write_csv(tables_dir / "customers.csv", customers)
    _write_csv(tables_dir / "depots.csv", depots)
    _write_csv(tables_dir / "routes.csv", routes)
    _write_csv(tables_dir / "vehicles.csv", vehicles)
    _write_csv(tables_dir / "shipments.csv", shipments)
    _write_csv(tables_dir / "shipment_events.csv", shipment_events)
    _write_csv(secondary_dir / "invoices.csv", invoices)
    _write_csv(secondary_dir / "payments.csv", payments)
    _write_csv(secondary_dir / "service_cases.csv", cases)
    _write_csv(secondary_dir / "case_notes.csv", case_notes)
    _write_csv(files_dir / "depot_reference_feed.csv", depot_feed)
    _write_json(files_dir / "carrier_updates.json", carrier_updates)
    _write_csv(files_dir / "customer_service_export.csv", _service_export(cases, case_notes))
    _write_jsonl(events_dir / "shipment_operational_events.jsonl", operational_events)
    _write_json(output_dir / "data_quality_issues.json", anomalies)

    manifest = {
        "scenario": "contoso_freight",
        "profile": profile_name,
        "seed": seed,
        "generated_at_utc": BASE_TIME.isoformat(),
        "include_defects": include_defects,
        "row_counts": {
            "customers": len(customers),
            "depots": len(depots),
            "routes": len(routes),
            "vehicles": len(vehicles),
            "shipments": len(shipments),
            "shipment_events": len(shipment_events),
            "invoices": len(invoices),
            "payments": len(payments),
            "service_cases": len(cases),
            "case_notes": len(case_notes),
            "operational_events": len(operational_events),
        },
    }
    _write_json(output_dir / "manifest.json", manifest)
    return manifest


def _customers(count: int, rng: random.Random) -> list[dict[str, Any]]:
    regions = ("north", "south", "midlands", "scotland", "wales")
    rows = []
    for idx in range(1, count + 1):
        rows.append(
            {
                "customer_id": f"CUST{idx:06d}",
                "account_number": f"AC{100000 + idx}",
                "legal_name": f"Contoso Synthetic Account {idx:04d}",
                "service_tier": rng.choices(SERVICE_TIERS, weights=(65, 28, 7))[0],
                "billing_region": rng.choice(regions),
                "created_at": _iso(BASE_TIME - timedelta(days=rng.randint(90, 2_400))),
                "is_active": rng.random() > 0.04,
                "contact_email": f"ops{idx:04d}@synthetic.contoso.example",
            }
        )
    if count >= 4:
        rows[-1]["account_number"] = rows[1]["account_number"]
        rows[-1]["legal_name"] = rows[1]["legal_name"] + " Ltd"
    return rows


def _depots(count: int) -> list[dict[str, Any]]:
    cities = [
        ("DPN", "Newcastle", "north"),
        ("DPM", "Manchester", "north"),
        ("DPB", "Birmingham", "midlands"),
        ("DPL", "London Gateway", "south"),
        ("DPC", "Cardiff", "wales"),
        ("DPE", "Edinburgh", "scotland"),
        ("DPG", "Glasgow", "scotland"),
        ("DPS", "Southampton", "south"),
    ]
    rows = []
    for idx in range(count):
        code, city, region = cities[idx % len(cities)]
        suffix = idx // len(cities)
        depot_code = f"{code}{suffix}" if suffix else code
        rows.append(
            {
                "depot_id": f"DEPOT{idx + 1:03d}",
                "depot_code": depot_code,
                "depot_name": f"{city} Depot",
                "region": region,
                "capacity_units": 400 + (idx * 75),
                "timezone": "Europe/London",
                "is_active": idx % 11 != 0,
            }
        )
    return rows


def _routes(depots: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    route_id = 1
    for origin in depots:
        for destination in depots:
            if origin["depot_id"] == destination["depot_id"]:
                continue
            if route_id % 3 == 0 or len(depots) <= 4:
                rows.append(
                    {
                        "route_id": f"ROUTE{route_id:05d}",
                        "origin_depot_id": origin["depot_id"],
                        "destination_depot_id": destination["depot_id"],
                        "route_code": f"{origin['depot_code']}-{destination['depot_code']}",
                        "planned_hours": 4 + (route_id % 13),
                        "is_hazmat_enabled": route_id % 7 == 0,
                    }
                )
            route_id += 1
    return rows


def _vehicles(
    count: int, depots: list[dict[str, Any]], rng: random.Random
) -> list[dict[str, Any]]:
    rows = []
    for idx in range(1, count + 1):
        rows.append(
            {
                "vehicle_id": f"VEH{idx:06d}",
                "home_depot_id": rng.choice(depots)["depot_id"],
                "registration_number": f"CF{idx:05d}",
                "vehicle_type": rng.choice(("tractor", "rigid", "van", "trailer")),
                "telematics_device_id": f"TEL-{rng.randint(100000, 999999)}",
                "in_service_date": _date(BASE_TIME - timedelta(days=rng.randint(120, 2_900))),
                "is_active": rng.random() > 0.08,
            }
        )
    return rows


def _shipments(
    count: int,
    customers: list[dict[str, Any]],
    routes: list[dict[str, Any]],
    vehicles: list[dict[str, Any]],
    rng: random.Random,
) -> list[dict[str, Any]]:
    rows = []
    for idx in range(1, count + 1):
        created_at = BASE_TIME + timedelta(minutes=idx * 37)
        route = rng.choice(routes)
        status = rng.choices(SHIPMENT_STATUSES, weights=(8, 12, 23, 9, 44, 4))[0]
        promised_at = created_at + timedelta(hours=int(route["planned_hours"]) + rng.randint(6, 72))
        delivered_at = (
            promised_at + timedelta(hours=rng.randint(-8, 24))
            if status == "delivered"
            else ""
        )
        rows.append(
            {
                "shipment_id": f"SHP{idx:09d}",
                "customer_id": rng.choice(customers)["customer_id"],
                "route_id": route["route_id"],
                "assigned_vehicle_id": rng.choice(vehicles)["vehicle_id"],
                "external_order_ref": f"ORD-{2026}-{idx:08d}",
                "shipment_status": status,
                "created_at": _iso(created_at),
                "promised_delivery_at": _iso(promised_at),
                "delivered_at": _iso(delivered_at) if delivered_at else "",
                "declared_value_gbp": round(rng.uniform(50, 8_500), 2),
                "hazmat_flag": rng.random() < 0.04,
                "legacy_options_json": json.dumps(
                    {"temperatureControlled": rng.random() < 0.09, "tailLift": rng.random() < 0.22},
                    sort_keys=True,
                ),
            }
        )
    return rows


def _shipment_events(
    shipments: list[dict[str, Any]],
    event_multiplier: int,
    rng: random.Random,
    include_defects: bool,
) -> list[dict[str, Any]]:
    event_types = ("created", "allocated", "departed", "arrived", "delivered", "exception")
    rows = []
    for shipment in shipments:
        created_at = datetime.fromisoformat(str(shipment["created_at"]))
        for sequence in range(1, event_multiplier + 1):
            event_time = created_at + timedelta(hours=sequence * rng.randint(2, 8))
            event_type = event_types[min(sequence - 1, len(event_types) - 1)]
            rows.append(
                {
                    "event_id": f"EVT{len(rows) + 1:012d}",
                    "shipment_id": shipment["shipment_id"],
                    "event_sequence": sequence,
                    "event_type": event_type,
                    "event_timestamp": _iso(event_time),
                    "source_system": "legacy_tms",
                    "event_payload_json": json.dumps(
                        {"status": event_type, "scanner": f"SCN{rng.randint(100, 999)}"},
                        sort_keys=True,
                    ),
                }
            )
    if include_defects and rows:
        duplicate = dict(rows[min(4, len(rows) - 1)])
        duplicate["event_id"] = "EVT_DUPLICATE_DELIVERY"
        rows.append(duplicate)
        rows[min(8, len(rows) - 1)]["event_timestamp"] = _iso(BASE_TIME - timedelta(days=30))
    return rows


def _invoices(shipments: list[dict[str, Any]], rng: random.Random) -> list[dict[str, Any]]:
    rows = []
    for idx, shipment in enumerate(shipments, start=1):
        issue_date = datetime.fromisoformat(str(shipment["created_at"])).date() + timedelta(days=1)
        amount = round(float(shipment["declared_value_gbp"]) * rng.uniform(0.07, 0.18) + 35, 2)
        rows.append(
            {
                "invoice_id": f"INV{idx:09d}",
                "shipment_id": shipment["shipment_id"],
                "customer_ref": shipment["customer_id"].replace("CUST", "ACCT-"),
                "invoice_date": issue_date.isoformat(),
                "due_date": (issue_date + timedelta(days=30)).isoformat(),
                "invoice_status": rng.choices(
                    ("issued", "paid", "overdue", "void"),
                    (25, 55, 17, 3),
                )[0],
                "net_amount_gbp": amount,
                "tax_amount_gbp": round(amount * 0.2, 2),
            }
        )
    return rows


def _payments(
    invoices: list[dict[str, Any]], payment_ratio: float, rng: random.Random
) -> list[dict[str, Any]]:
    rows = []
    for invoice in invoices:
        if rng.random() > payment_ratio:
            continue
        paid_date = datetime.fromisoformat(str(invoice["invoice_date"])).date() + timedelta(
            days=rng.randint(2, 45)
        )
        rows.append(
            {
                "payment_id": f"PAY{len(rows) + 1:09d}",
                "invoice_id": invoice["invoice_id"],
                "paid_date": paid_date.isoformat(),
                "payment_method": rng.choice(PAYMENT_METHODS),
                "amount_gbp": round(
                    float(invoice["net_amount_gbp"]) + float(invoice["tax_amount_gbp"]),
                    2,
                ),
                "legacy_batch_id": f"BATCH-{paid_date:%Y%m%d}-{rng.randint(1, 12):02d}",
            }
        )
    return rows


def _cases(
    count: int,
    customers: list[dict[str, Any]],
    shipments: list[dict[str, Any]],
    rng: random.Random,
    include_defects: bool,
) -> list[dict[str, Any]]:
    rows = []
    for idx in range(1, count + 1):
        opened_at = BASE_TIME + timedelta(hours=rng.randint(1, 24 * 120))
        shipment = rng.choice(shipments)
        email = f"service{idx:04d}@synthetic.contoso.example"
        if include_defects and idx == max(2, count // 3):
            email = "not-an-email"
        rows.append(
            {
                "case_id": f"CASE{idx:08d}",
                "customer_id": shipment["customer_id"],
                "shipment_id": shipment["shipment_id"],
                "case_reason": rng.choice(CASE_REASONS),
                "case_status": rng.choice(
                    ("open", "pending_customer", "resolved", "closed", "LEGACY_X")
                ),
                "opened_at": _iso(opened_at),
                "closed_at": _iso(opened_at + timedelta(hours=rng.randint(3, 120)))
                if rng.random() > 0.25
                else "",
                "contact_email": email,
            }
        )
    if include_defects and rows:
        rows[-1]["shipment_id"] = "SHP999999999"
    return rows


def _case_notes(cases: list[dict[str, Any]], rng: random.Random) -> list[dict[str, Any]]:
    rows = []
    for case in cases:
        for note_idx in range(1, rng.randint(2, 4)):
            rows.append(
                {
                    "case_note_id": f"NOTE{len(rows) + 1:09d}",
                    "case_id": case["case_id"],
                    "note_sequence": note_idx,
                    "note_timestamp": case["opened_at"],
                    "agent_team": rng.choice(("frontline", "claims", "depot_ops", "billing")),
                    "note_text": (
                        f"Synthetic note {note_idx} for {case['case_reason']} on "
                        f"{case['shipment_id']}. No real personal data."
                    ),
                }
            )
    return rows


def _depot_reference_feed(
    depots: list[dict[str, Any]], include_defects: bool
) -> list[dict[str, Any]]:
    rows = [
        {
            "depot_code": depot["depot_code"],
            "depot_name": depot["depot_name"],
            "region": depot["region"].upper(),
            "capacity_units": depot["capacity_units"],
            "feed_version": "v1",
        }
        for depot in depots
    ]
    if include_defects and rows:
        rows[0]["capacity_units"] = ""
        rows.append({**rows[1], "depot_name": rows[1]["depot_name"] + " duplicate"})
    return rows


def _carrier_updates(
    shipments: list[dict[str, Any]], rng: random.Random, include_defects: bool
) -> list[dict[str, Any]]:
    rows = []
    for shipment in shipments[: max(5, len(shipments) // 5)]:
        rows.append(
            {
                "carrier_update_id": f"CAR-{len(rows) + 1:08d}",
                "partner_code": rng.choice(("NORTHWAY", "EUROLINE", "CITYFREIGHT")),
                "external_order_ref": shipment["external_order_ref"],
                "partner_status": rng.choice(("accepted", "collected", "delayed", "delivered")),
                "update_timestamp": shipment["created_at"],
                "schema_version": 1,
            }
        )
    if include_defects and rows:
        rows[-1]["schema_version"] = 2
        rows[-1]["partner_eta_text"] = "tomorrow afternoon"
    return rows


def _operational_events(
    shipment_events: list[dict[str, Any]], rng: random.Random, include_defects: bool
) -> list[dict[str, Any]]:
    rows = []
    for event in shipment_events:
        rows.append(
            {
                "event_id": event["event_id"],
                "event_type": event["event_type"],
                "aggregate_type": "shipment",
                "aggregate_id": event["shipment_id"],
                "occurred_at": event["event_timestamp"],
                "schema_version": 1,
                "payload": json.loads(str(event["event_payload_json"])),
            }
        )
    if include_defects and len(rows) >= 3:
        rows.insert(1, dict(rows[0]))
        rows[2]["occurred_at"] = _iso(BASE_TIME - timedelta(days=60))
        rows[-1]["schema_version"] = 2
        rows[-1]["payload"]["legacy_status_code"] = rng.choice(("DLY", "UNK", "CLOSED"))
    return rows


def _service_export(
    cases: list[dict[str, Any]], notes: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    first_note_by_case = {note["case_id"]: note for note in notes}
    return [
        {
            "case_id": case["case_id"],
            "shipment_ref": case["shipment_id"],
            "customer_ref": case["customer_id"].replace("CUST", "ACCT-"),
            "case_status": case["case_status"],
            "opened_at": case["opened_at"],
            "first_note_text": first_note_by_case.get(case["case_id"], {}).get("note_text", ""),
        }
        for case in cases
    ]


def _anomaly_catalog(include_defects: bool) -> list[dict[str, str]]:
    if not include_defects:
        return []
    return [
        {
            "issue_code": "DUPLICATE_CUSTOMER_ACCOUNT",
            "location": "legacy_oltp/customers.csv",
            "description": (
                "Two synthetic customer rows share an account number with variant legal names."
            ),
        },
        {
            "issue_code": "MISSING_DEPOT_CAPACITY",
            "location": "file_feeds/depot_reference_feed.csv",
            "description": "One depot feed row has a null capacity value.",
        },
        {
            "issue_code": "INVALID_CASE_EMAIL",
            "location": "secondary_billing/service_cases.csv",
            "description": "One customer-service export row contains a malformed email.",
        },
        {
            "issue_code": "CASE_REFERENTIAL_ANOMALY",
            "location": "secondary_billing/service_cases.csv",
            "description": "One service case references an unknown shipment identifier.",
        },
        {
            "issue_code": "DUPLICATE_AND_OUT_OF_ORDER_EVENT",
            "location": "events/shipment_operational_events.jsonl",
            "description": (
                "Operational events include duplicate delivery and late-arriving records."
            ),
        },
        {
            "issue_code": "SCHEMA_DRIFT",
            "location": "file_feeds/carrier_updates.json",
            "description": "One carrier update uses schema_version 2 and an extra ETA text field.",
        },
    ]


def _write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def _write_json(path: Path, rows: Any) -> None:
    path.write_text(json.dumps(rows, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.write_text(
        "".join(json.dumps(row, sort_keys=True) + "\n" for row in rows),
        encoding="utf-8",
    )


def _iso(value: datetime) -> str:
    return value.isoformat().replace("+00:00", "Z")


def _date(value: datetime) -> str:
    return value.date().isoformat()


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate the Contoso Freight legacy estate.")
    parser.add_argument("--profile", choices=sorted(PROFILE_SPECS), default="tiny")
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    parser.add_argument("--output-dir", type=Path, default=Path("data/raw/legacy_estate"))
    parser.add_argument("--no-defects", action="store_true")
    args = parser.parse_args()

    manifest = generate_estate(
        output_dir=args.output_dir,
        profile_name=args.profile,
        seed=args.seed,
        include_defects=not args.no_defects,
    )
    print(json.dumps(manifest, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
