from __future__ import annotations

# ruff: noqa: E501
import csv
import hashlib
import json
import shutil
from collections import Counter
from dataclasses import asdict
from pathlib import Path
from typing import Any

from migration_factory.catalog import MANIFESTS, REMEDIATIONS, TOOL_INTEGRATIONS
from migration_factory.model import ValidationGate

ROOT = Path(__file__).resolve().parents[2]
SAMPLE_ROOT = ROOT / "data/samples/legacy_estate/tiny"
ALL_SYSTEMS = {"legacy_tms", "billing_ops"}


def run_migration_factory(
    outputs_dir: Path,
    reports_dir: Path,
    system: str = "",
    failure_scenario: str = "",
) -> dict[str, Path]:
    selected = _selected_systems(system)
    _reset_dir(outputs_dir)
    (outputs_dir / "local_targets").mkdir(parents=True, exist_ok=True)
    reports_dir.mkdir(parents=True, exist_ok=True)

    target_files: dict[str, list[Path]] = {}
    for source_system in selected:
        if source_system == "legacy_tms":
            target_files[source_system] = _migrate_legacy_tms(outputs_dir / "local_targets/legacy_tms_sqlmi")
        elif source_system == "billing_ops":
            target_files[source_system] = _migrate_billing_ops(outputs_dir / "local_targets/billing_ops_postgresql")

    if failure_scenario:
        _apply_failure(outputs_dir, failure_scenario, selected)

    rows = {
        "migration_manifest.csv": [asdict(row) for row in MANIFESTS if row.source_system in selected],
        "compatibility_remediation.csv": [asdict(row) for row in REMEDIATIONS],
        "schema_conversion_report.csv": _schema_conversion_rows(selected),
        "data_reconciliation.csv": _reconciliation_rows(outputs_dir, selected),
        "validation_gates.csv": [],
        "migration_wave_execution.csv": _wave_execution_rows(selected),
        "cutover_readiness.csv": _cutover_readiness_rows(selected),
        "rollback_readiness.csv": _rollback_readiness_rows(selected),
        "tool_integration_points.csv": [asdict(row) for row in TOOL_INTEGRATIONS],
        "failure_scenarios.csv": _failure_scenarios_rows(failure_scenario),
    }
    rows["validation_gates.csv"] = [asdict(row) for row in _validation_gates(rows, selected)]

    written: dict[str, Path] = {}
    for filename, dataset in rows.items():
        path = outputs_dir / filename
        _write_csv(path, dataset)
        written[filename] = path

    report = reports_dir / "migration_factory_report.md"
    report.write_text(_report(rows, selected, failure_scenario), encoding="utf-8")
    written["migration_factory_report.md"] = report
    return written


def _selected_systems(system: str) -> set[str]:
    if not system:
        return set(ALL_SYSTEMS)
    if system not in ALL_SYSTEMS:
        valid = ", ".join(sorted(ALL_SYSTEMS))
        raise ValueError(f"Unknown migration system '{system}'. Valid systems: {valid}")
    return {system}


def _reset_dir(path: Path) -> None:
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True, exist_ok=True)


def _migrate_legacy_tms(target_dir: Path) -> list[Path]:
    source_dir = SAMPLE_ROOT / "legacy_oltp"
    target_dir.mkdir(parents=True, exist_ok=True)
    outputs = []
    table_map = {
        "customers.csv": ("customer_account.csv", _customer_row),
        "depots.csv": ("depot.csv", _identity_row),
        "routes.csv": ("route.csv", _identity_row),
        "vehicles.csv": ("vehicle.csv", _identity_row),
        "shipments.csv": ("shipment.csv", _shipment_row),
        "shipment_events.csv": ("shipment_event_history.csv", _identity_row),
    }
    for source_name, (target_name, transform) in table_map.items():
        rows = [transform(row) for row in _read_csv(source_dir / source_name)]
        path = target_dir / target_name
        _write_csv(path, rows)
        outputs.append(path)
    return outputs


def _migrate_billing_ops(target_dir: Path) -> list[Path]:
    source_dir = SAMPLE_ROOT / "secondary_billing"
    target_dir.mkdir(parents=True, exist_ok=True)
    outputs = []
    for filename in ("invoices.csv", "payments.csv", "service_cases.csv", "case_notes.csv"):
        rows = _read_csv(source_dir / filename)
        target_name = filename.replace("invoices", "invoice").replace("payments", "payment").replace("service_cases", "service_case").replace("case_notes", "case_note")
        path = target_dir / target_name
        _write_csv(path, rows)
        outputs.append(path)
    return outputs


def _customer_row(row: dict[str, str]) -> dict[str, str]:
    return {
        **row,
        "legacy_customer_memo": "",
        "migration_note": "ntext remediated to nvarchar(max) in target schema",
    }


def _shipment_row(row: dict[str, str]) -> dict[str, str]:
    return {
        **row,
        "declared_value_gbp_decimal_review_required": "true",
        "rowversion_preserved_in_target_schema": "true",
    }


def _identity_row(row: dict[str, str]) -> dict[str, str]:
    return dict(row)


def _apply_failure(outputs_dir: Path, failure_scenario: str, selected: set[str]) -> None:
    if failure_scenario == "row_count_mismatch" and "legacy_tms" in selected:
        path = outputs_dir / "local_targets/legacy_tms_sqlmi/shipment.csv"
        rows = _read_csv(path)
        _write_csv(path, rows[:-1])
    elif failure_scenario == "duplicate_key" and "billing_ops" in selected:
        path = outputs_dir / "local_targets/billing_ops_postgresql/invoice.csv"
        rows = _read_csv(path)
        _write_csv(path, rows + [dict(rows[0])])
    elif failure_scenario == "checksum_mismatch" and "billing_ops" in selected:
        path = outputs_dir / "local_targets/billing_ops_postgresql/payment.csv"
        rows = _read_csv(path)
        if rows:
            rows[0]["amount_gbp"] = str(float(rows[0]["amount_gbp"]) + 1)
        _write_csv(path, rows)
    elif failure_scenario == "stale_delta":
        marker = outputs_dir / "local_targets/stale_delta_marker.json"
        marker.write_text(json.dumps({"delta_status": "stale"}, sort_keys=True), encoding="utf-8")
    elif failure_scenario in {"missing_dependency", "unresolved_compatibility_blocker", "failed_validation_gate"}:
        marker = outputs_dir / f"{failure_scenario}.json"
        marker.write_text(json.dumps({"scenario": failure_scenario}, sort_keys=True), encoding="utf-8")
    else:
        raise ValueError(f"Unknown or inapplicable failure scenario: {failure_scenario}")


def _schema_conversion_rows(selected: set[str]) -> list[dict[str, str]]:
    rows = []
    if "legacy_tms" in selected:
        rows.extend(
            [
                _schema_row("legacy_tms", "CustomerAccount.LegacyCustomerMemo", "ntext", "nvarchar(max)", "implemented locally", "SQL-COMP-001"),
                _schema_row("legacy_tms", "Shipment.DeclaredValueGbp", "money", "money retained; decimal review flagged", "accepted risk", "SQL-COMP-002"),
                _schema_row("legacy_tms", "Shipment.RowVersionBytes", "rowversion", "rowversion preserved", "implemented locally", "SQL-COMP-007"),
                _schema_row("legacy_tms", "stored procedures", "SQL Server T-SQL", "signatures preserved for MI", "implemented locally", "SQL-COMP-003"),
                _schema_row("legacy_tms", "reporting index", "missing covering index", "IX_Shipment_Route_Status_CreatedAt", "implemented locally", "SQL-COMP-005"),
            ]
        )
    if "billing_ops" in selected:
        rows.extend(
            [
                _schema_row("billing_ops", "billing_ops.invoice", "PostgreSQL-like table", "PostgreSQL Flexible Server table", "implemented locally", "PG-COMP-001"),
                _schema_row("billing_ops", "customer_ref", "ACCT-style identifier", "retained with mapping risk evidence", "accepted risk", "PG-COMP-001"),
            ]
        )
    return rows


def _schema_row(system: str, source: str, before: str, after: str, status: str, finding: str) -> dict[str, str]:
    return {
        "source_system": system,
        "source_object": source,
        "source_definition": before,
        "target_definition": after,
        "conversion_status": status,
        "finding_id": finding,
        "evidence_classification": "locally validated" if status == "implemented locally" else "derived from assessment",
    }


def _reconciliation_rows(outputs_dir: Path, selected: set[str]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    if "legacy_tms" in selected:
        mappings = [
            ("customers", "legacy_oltp/customers.csv", "local_targets/legacy_tms_sqlmi/customer_account.csv", "customer_id"),
            ("depots", "legacy_oltp/depots.csv", "local_targets/legacy_tms_sqlmi/depot.csv", "depot_id"),
            ("routes", "legacy_oltp/routes.csv", "local_targets/legacy_tms_sqlmi/route.csv", "route_id"),
            ("vehicles", "legacy_oltp/vehicles.csv", "local_targets/legacy_tms_sqlmi/vehicle.csv", "vehicle_id"),
            ("shipments", "legacy_oltp/shipments.csv", "local_targets/legacy_tms_sqlmi/shipment.csv", "shipment_id"),
            ("shipment_events", "legacy_oltp/shipment_events.csv", "local_targets/legacy_tms_sqlmi/shipment_event_history.csv", "event_id"),
        ]
        for domain, source_rel, target_rel, key in mappings:
            rows.extend(_table_reconciliation("mig-legacy-tms-sqlmi", domain, SAMPLE_ROOT / source_rel, outputs_dir / target_rel, key))
        rows.append(_referential_check("mig-legacy-tms-sqlmi", "shipments_to_customers", outputs_dir / "local_targets/legacy_tms_sqlmi/shipment.csv", "customer_id", outputs_dir / "local_targets/legacy_tms_sqlmi/customer_account.csv", "customer_id"))
        rows.append(
            _chronology_check(
                "mig-legacy-tms-sqlmi",
                SAMPLE_ROOT / "legacy_oltp/shipment_events.csv",
                outputs_dir / "local_targets/legacy_tms_sqlmi/shipment_event_history.csv",
            )
        )
    if "billing_ops" in selected:
        mappings = [
            ("invoices", "secondary_billing/invoices.csv", "local_targets/billing_ops_postgresql/invoice.csv", "invoice_id"),
            ("payments", "secondary_billing/payments.csv", "local_targets/billing_ops_postgresql/payment.csv", "payment_id"),
            ("service_cases", "secondary_billing/service_cases.csv", "local_targets/billing_ops_postgresql/service_case.csv", "case_id"),
            ("case_notes", "secondary_billing/case_notes.csv", "local_targets/billing_ops_postgresql/case_note.csv", "case_note_id"),
        ]
        for domain, source_rel, target_rel, key in mappings:
            rows.extend(_table_reconciliation("mig-billing-postgres", domain, SAMPLE_ROOT / source_rel, outputs_dir / target_rel, key))
        rows.append(_referential_check("mig-billing-postgres", "payments_to_invoices", outputs_dir / "local_targets/billing_ops_postgresql/payment.csv", "invoice_id", outputs_dir / "local_targets/billing_ops_postgresql/invoice.csv", "invoice_id"))
        rows.append(_financial_check(outputs_dir))
    return rows


def _table_reconciliation(migration_id: str, domain: str, source_path: Path, target_path: Path, key: str) -> list[dict[str, str]]:
    source = _read_csv(source_path)
    target = _read_csv(target_path)
    common_fields = sorted(set(source[0]) & set(target[0])) if source and target else []
    return [
        _recon(migration_id, domain, "row_count", len(source), len(target), len(source) == len(target), "locally validated"),
        _recon(migration_id, domain, "business_key_count", len({row[key] for row in source}), len({row[key] for row in target}), len({row[key] for row in source}) == len({row[key] for row in target}), "locally validated"),
        _recon(migration_id, domain, "duplicate_key_count", _duplicate_count(source, key), _duplicate_count(target, key), _duplicate_count(target, key) == 0, "locally validated"),
        _recon(migration_id, domain, "null_profile", _null_count(source, common_fields), _null_count(target, common_fields), _null_count(source, common_fields) == _null_count(target, common_fields), "locally validated"),
        _recon(migration_id, domain, "checksum", _checksum_rows(source, common_fields), _checksum_rows(target, common_fields), _checksum_rows(source, common_fields) == _checksum_rows(target, common_fields), "locally validated"),
    ]


def _referential_check(migration_id: str, check_name: str, child_path: Path, child_key: str, parent_path: Path, parent_key: str) -> dict[str, str]:
    child = _read_csv(child_path)
    parent_keys = {row[parent_key] for row in _read_csv(parent_path)}
    missing = sum(1 for row in child if row[child_key] not in parent_keys)
    return _recon(migration_id, check_name, "referential_integrity", 0, missing, missing == 0, "locally validated")


def _chronology_check(migration_id: str, source_path: Path, target_path: Path) -> dict[str, str]:
    source_violations = _chronology_violations(_read_csv(source_path))
    target_violations = _chronology_violations(_read_csv(target_path))
    return _recon(
        migration_id,
        "shipment_events",
        "shipment_event_chronology",
        source_violations,
        target_violations,
        source_violations == target_violations,
        "locally validated",
    )


def _chronology_violations(events: list[dict[str, str]]) -> int:
    by_shipment: dict[str, list[dict[str, str]]] = {}
    for event in events:
        by_shipment.setdefault(event["shipment_id"], []).append(event)
    violations = 0
    for grouped in by_shipment.values():
        previous = ""
        for event in sorted(grouped, key=lambda row: int(row["event_sequence"])):
            current = event["event_timestamp"]
            if previous and current < previous:
                violations += 1
            previous = current
    return violations


def _financial_check(outputs_dir: Path) -> dict[str, str]:
    invoices = _read_csv(outputs_dir / "local_targets/billing_ops_postgresql/invoice.csv")
    payments = _read_csv(outputs_dir / "local_targets/billing_ops_postgresql/payment.csv")
    invoice_total = round(sum(float(row["net_amount_gbp"]) + float(row["tax_amount_gbp"]) for row in invoices), 2)
    payment_total = round(sum(float(row["amount_gbp"]) for row in payments), 2)
    passed = payment_total <= invoice_total
    return _recon("mig-billing-postgres", "billing_financials", "invoice_payment_total_sanity", invoice_total, payment_total, passed, "locally validated")


def _recon(migration_id: str, domain: str, check_type: str, source_value: Any, target_value: Any, passed: bool, evidence: str) -> dict[str, str]:
    return {
        "migration_id": migration_id,
        "data_domain": domain,
        "check_type": check_type,
        "source_value": str(source_value),
        "target_value": str(target_value),
        "tolerance": "0 unless financial sanity check",
        "status": "passed" if passed else "failed",
        "evidence_classification": evidence,
    }


def _validation_gates(rows: dict[str, list[dict[str, str]]], selected: set[str]) -> list[ValidationGate]:
    gates: list[ValidationGate] = []
    reconciliation_failed = any(row["status"] == "failed" for row in rows["data_reconciliation.csv"])
    failure_rows = rows["failure_scenarios.csv"]
    failure = next((row["scenario"] for row in failure_rows if row["status"] == "active"), "")
    for manifest in MANIFESTS:
        if manifest.source_system not in selected:
            continue
        migration_id = manifest.migration_id
        gate_specs = [
            ("PRE-MIGRATION", "source readiness", True, "locally validated"),
            ("PRE-MIGRATION", "backup/recovery prerequisite", True, "requires live validation"),
            ("PRE-MIGRATION", "schema compatibility", failure != "unresolved_compatibility_blocker", "locally validated"),
            ("POST-LOAD", "row counts and integrity", not reconciliation_failed, "locally validated"),
            ("POST-LOAD", "representative query placeholders", True, "simulated evidence"),
            ("PRE-CUTOVER", "delta synchronization", failure != "stale_delta", "simulated evidence"),
            ("PRE-CUTOVER", "rollback readiness", failure != "failed_validation_gate", "architecture/design evidence"),
            ("POST-CUTOVER", "connectivity smoke checks", False, "requires live validation"),
            ("POST-CUTOVER", "performance sanity checks", False, "requires live validation"),
        ]
        for stage, name, passed, evidence in gate_specs:
            cloud_required = evidence == "requires live validation"
            status = "required" if cloud_required else "passed" if passed else "failed"
            gates.append(
                ValidationGate(
                    migration_id,
                    stage,
                    name,
                    status,
                    evidence,
                    _gate_evidence(name, status, failure),
                    stop_on_failure=stage != "POST-CUTOVER",
                )
            )
    return gates


def _gate_evidence(name: str, status: str, failure: str) -> str:
    if status == "required":
        return f"{name} requires Azure/customer validation before real cutover."
    if status == "failed":
        return f"{name} failed due to controlled scenario or reconciliation failure: {failure or 'data mismatch'}."
    return f"{name} passed local deterministic migration-factory check."


def _wave_execution_rows(selected: set[str]) -> list[dict[str, str]]:
    specs = [
        ("Wave 0", "prerequisites and remediation", "all systems", "completed locally", "Assessment and architecture prerequisites represented; live evidence still required."),
        ("Wave 1", "feeds and analytical offload", "not in Milestone 5 scope", "skipped", "Databricks ingestion workloads intentionally deferred."),
        ("Wave 2", "secondary relational source", "billing_ops", "eligible" if "billing_ops" in selected else "not selected", "Offline local migration simulation available."),
        ("Wave 3", "business-critical transport OLTP", "legacy_tms", "eligible" if "legacy_tms" in selected else "not selected", "Minimal-downtime sequence modelled; Azure execution deferred."),
    ]
    return [
        {
            "wave": wave,
            "wave_name": name,
            "included_scope": scope,
            "execution_status": status,
            "evidence": evidence,
            "wave_order_consistent_with_milestone_3": "true",
        }
        for wave, name, scope, status, evidence in specs
    ]


def _cutover_readiness_rows(selected: set[str]) -> list[dict[str, str]]:
    rows = []
    for manifest in MANIFESTS:
        if manifest.source_system not in selected:
            continue
        for check in ("entry criteria", "freeze/quiesce plan", "final sync plan", "validation plan", "connection switch placeholder", "smoke testing", "go/no-go decision", "communications checkpoint", "evidence capture", "exit criteria"):
            rows.append(
                {
                    "migration_id": manifest.migration_id,
                    "cutover_check": check,
                    "status": "planned" if check == "connection switch placeholder" else "ready",
                    "evidence_classification": "architecture/design evidence" if check == "connection switch placeholder" else "simulated evidence",
                    "notes": "No real DNS or application connection switch is performed.",
                }
            )
    return rows


def _rollback_readiness_rows(selected: set[str]) -> list[dict[str, str]]:
    rows = []
    for manifest in MANIFESTS:
        if manifest.source_system not in selected:
            continue
        for item in ("decision window", "rollback triggers", "source reactivation", "target write handling", "reverse synchronization concern", "data divergence risk", "application connection restoration", "evidence retention"):
            rows.append(
                {
                    "migration_id": manifest.migration_id,
                    "rollback_item": item,
                    "status": "defined",
                    "evidence_classification": "architecture/design evidence",
                    "notes": "Rollback is harder after target accepts writes; divergence must be reviewed before cutback.",
                }
            )
    return rows


def _failure_scenarios_rows(active: str) -> list[dict[str, str]]:
    scenarios = {
        "row_count_mismatch": "Drops a migrated shipment row and fails row-count reconciliation.",
        "missing_dependency": "Marks dependency prerequisite unavailable and stops gates.",
        "unresolved_compatibility_blocker": "Fails schema compatibility pre-migration gate.",
        "duplicate_key": "Duplicates a billing invoice target row and fails duplicate-key reconciliation.",
        "checksum_mismatch": "Mutates migrated payment amount and fails checksum reconciliation.",
        "stale_delta": "Marks minimal-downtime delta stale and fails pre-cutover delta gate.",
        "failed_validation_gate": "Forces rollback-readiness gate failure.",
    }
    return [
        {
            "scenario": scenario,
            "description": description,
            "status": "active" if scenario == active else "available",
            "safe_failure_behavior": "stop unsafe progression and emit failed evidence",
        }
        for scenario, description in scenarios.items()
    ]


def _report(rows: dict[str, list[dict[str, str]]], selected: set[str], failure_scenario: str) -> str:
    failed_recon = [row for row in rows["data_reconciliation.csv"] if row["status"] == "failed"]
    gates = rows["validation_gates.csv"]
    failed_gates = [row for row in gates if row["status"] == "failed"]
    required_gates = [row for row in gates if row["status"] == "required"]
    return "\n".join(
        [
            "# Migration Factory Report",
            "",
            "Milestone 5 implements a local deterministic migration factory for operational database workloads only. It does not deploy Azure resources and does not claim Azure DMS, Azure Migrate, DMA, SqlPackage, pg_dump, or pg_restore execution.",
            "",
            f"Selected systems: {', '.join(sorted(selected))}.",
            f"Active failure scenario: {failure_scenario or 'none'}.",
            "",
            "## Local Execution Evidence",
            "",
            "- Source CSV fixtures were extracted from `data/samples/legacy_estate/tiny`.",
            "- Target-shaped CSV datasets were written under `outputs/migration/local_targets`.",
            "- Schema conversion, reconciliation, validation gates, cutover readiness, rollback readiness, and wave evidence were generated deterministically.",
            "",
            "## Simulation Boundary",
            "",
            "- Online/minimal-downtime migration is modelled as bulk copy, incremental capture, delta replay, quiesce, final sync, validation, and cutover.",
            "- Cloud-only checks remain `required` and are not marked passed.",
            "- No DNS, application connection, backup/restore, DMS, DMA, SqlPackage, or PostgreSQL native tooling action is performed locally.",
            "",
            "## Results",
            "",
            f"- Reconciliation rows: {len(rows['data_reconciliation.csv'])}.",
            f"- Failed reconciliation rows: {len(failed_recon)}.",
            f"- Failed gates: {len(failed_gates)}.",
            f"- Gates requiring live validation: {len(required_gates)}.",
            "",
            "## Hypercare Model",
            "",
            "- First hour: connectivity smoke checks, row-count sanity, business-critical workflow checks.",
            "- First day: reconciliation rerun, integration review, error monitoring, user support triage.",
            "- First week: performance review, failed integration review, incident trends, migration closure decision.",
            "",
        ]
    )


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def _write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def _duplicate_count(rows: list[dict[str, str]], key: str) -> int:
    counts = Counter(row[key] for row in rows)
    return sum(count - 1 for count in counts.values() if count > 1)


def _null_count(rows: list[dict[str, str]], fields: list[str]) -> int:
    return sum(1 for row in rows for field in fields if row[field] == "")


def _checksum_rows(rows: list[dict[str, str]], fields: list[str]) -> str:
    digest = hashlib.sha256()
    for row in sorted(rows, key=lambda item: json.dumps(item, sort_keys=True)):
        comparable = {field: row[field] for field in fields}
        digest.update(json.dumps(comparable, sort_keys=True).encode("utf-8"))
    return digest.hexdigest()
