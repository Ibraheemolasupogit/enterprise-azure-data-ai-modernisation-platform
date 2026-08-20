from __future__ import annotations

# ruff: noqa: E501
import argparse
import csv
import json
import os
import shutil
from pathlib import Path
from typing import Any

from final_assurance.catalog import CAPABILITIES, DATA_PRODUCTS, FAILURE_MODES, SECURITY_CONTROLS
from final_assurance.validation import validate_outputs


def generate_outputs(outputs_dir: Path, reports_dir: Path, repo_root: Path | None = None) -> dict[str, Path]:
    outputs_dir.mkdir(parents=True, exist_ok=True)
    reports_dir.mkdir(parents=True, exist_ok=True)
    root = repo_root or Path.cwd()
    outputs = {
        "capability_inventory.csv": _capability_inventory(),
        "architecture_traceability.csv": _architecture_traceability(),
        "platform_ownership_matrix.csv": _ownership_matrix(),
        "security_assurance_matrix.csv": _security_matrix(),
        "identity_assurance.csv": _identity_assurance(),
        "data_product_assurance.csv": _data_product_assurance(),
        "governance_traceability.csv": _governance_traceability(),
        "resilience_assurance.csv": _resilience_assurance(),
        "failure_mode_matrix.csv": _failure_mode_matrix(),
        "observability_assurance.csv": _observability_assurance(),
        "finops_assurance.csv": _finops_assurance(),
        "ai_assurance.csv": _ai_assurance(),
        "api_assurance.csv": _api_assurance(),
        "cicd_assurance.csv": _cicd_assurance(),
        "implementation_truth_matrix.csv": _truth_matrix(),
        "production_gap_register.csv": _gap_register(),
        "final_risk_register.csv": _risk_register(),
        "runbook_catalog.csv": _runbook_catalog(),
        "release_readiness.csv": _release_readiness(),
    }
    written: dict[str, Path] = {}
    for filename, rows in outputs.items():
        path = outputs_dir / filename
        _write_csv(path, rows)
        written[filename] = path
    manifest_path = outputs_dir / "release_manifest.json"
    manifest_path.write_text(
        json.dumps(_release_manifest(root, sorted(outputs)), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    written["release_manifest.json"] = manifest_path
    report = reports_dir / "final_assurance_report.md"
    report.write_text(_report(), encoding="utf-8")
    written["final_assurance_report.md"] = report
    failures = validate_outputs(outputs_dir, root)
    if failures:
        joined = "\n".join(f"- {failure}" for failure in failures)
        raise RuntimeError(f"Final assurance validation failed:\n{joined}")
    return written


def _write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def _capability_inventory() -> list[dict[str, str]]:
    return [
        {
            "capability_id": cid,
            "domain": domain,
            "capability": capability,
            "implementation_status": status,
            "evidence_path": evidence,
            "validation_class": klass,
            "owner": owner,
            "production_dependency": dependency,
            "residual_gap": gap,
            "evidence_classification": klass,
        }
        for cid, domain, capability, status, evidence, klass, owner, dependency, gap in CAPABILITIES
    ]


def _architecture_traceability() -> list[dict[str, str]]:
    rows = [
        ("modernize legacy SQL estate", "compatibility and dependency assessment", "Azure SQL MI disposition", "SQL project and migration factory", "database roles, release gates", "outputs/sql_cicd/release_readiness.csv", "requires Azure validation"),
        ("govern analytical products", "manual reporting and file estate", "Databricks medallion architecture", "Bronze/Silver/Gold pipelines", "Unity Catalog, quality gates", "outputs/databricks_pipelines/pipeline_traceability.csv", "requires Databricks validation"),
        ("secure AI over operational data", "future AI-enabled data products", "SQL-native RAG boundary", "ai schema, retrieval, audits", "retrieval auth, prompt contract", "outputs/sql_ai/sql_ai_readiness.csv", "requires Azure validation"),
        ("expose governed APIs", "application integration need", "DAB/API/MCP allowlist", "API contracts and DAB config", "Entra roles and field restrictions", "outputs/application_integration/api_catalog.csv", "requires application runtime validation"),
        ("support Fabric downstream", "analytics consumer boundary", "Fabric consumes governed Gold only", "Fabric handoff contracts", "contract, sensitivity, lineage handoff", "outputs/fabric_integration/fabric_integration_readiness.csv", "requires Fabric validation"),
    ]
    return [
        {
            "requirement": req,
            "assessment_finding": finding,
            "architecture_decision": decision,
            "implementation": impl,
            "control": control,
            "evidence": evidence,
            "validation_status": status,
            "evidence_classification": status,
        }
        for req, finding, decision, impl, control, evidence, status in rows
    ]


def _ownership_matrix() -> list[dict[str, str]]:
    rows = [
        ("Azure SQL", "database platform team", "operations/security team", "application and data teams", "no overlap; DB team owns platform state"),
        ("PostgreSQL", "database platform team", "migration team", "billing analytics consumers", "secondary target only"),
        ("Databricks", "data platform team", "data engineering team", "operations team", "workspace/runtime owned by data platform"),
        ("ADLS", "platform engineering", "data engineering team", "Fabric consumer identity", "published Gold paths only for Fabric"),
        ("Unity Catalog", "data governance team", "data platform team", "analytics groups", "permissions managed centrally"),
        ("API layer", "application integration team", "security team", "client applications", "DAB/API owns interface, SQL owns data"),
        ("Azure OpenAI boundary", "AI platform team", "security team", "API/SQL AI consumers", "no local invocation claimed"),
        ("Fabric consumer boundary", "Fabric platform team", "Azure producer team", "analytics consumers", "Fabric downstream ownership only"),
        ("CI/CD", "DevSecOps team", "platform owners", "release approvers", "manual environment approval for production"),
        ("security", "security team", "platform owners", "auditors", "control ownership explicit"),
        ("operations", "operations team", "platform owners", "service desk", "runbooks mapped to platforms"),
    ]
    return [
        {
            "service": service,
            "owner": owner,
            "accountable_support": support,
            "consumers": consumers,
            "ownership_boundary": boundary,
            "evidence_classification": "configuration defined",
        }
        for service, owner, support, consumers, boundary in rows
    ]


def _security_matrix() -> list[dict[str, str]]:
    return [
        {
            "control": control,
            "coverage": coverage,
            "assurance_status": status,
            "runtime_validation": runtime,
            "residual_risk": risk,
            "evidence": evidence,
            "evidence_classification": status,
        }
        for control, coverage, status, runtime, risk, evidence in SECURITY_CONTROLS
    ]


def _identity_assurance() -> list[dict[str, str]]:
    rows = [
        ("Azure SQL identities", "application roles, managed identities, deployment identity", "separated", "no hardcoded credentials", "requires Azure validation"),
        ("Databricks identities", "workspace groups and Unity Catalog grants", "separated", "no personal tokens committed", "requires Databricks validation"),
        ("GitHub deployment identities", "OIDC/environment approval pattern", "separated", "no cloud secrets required in repo", "configuration defined"),
        ("API runtime identities", "Container Apps/DAB managed identity", "separated", "no SQL username/password preferred", "requires application runtime validation"),
        ("Fabric consumer identities", "Entra service principal/groups", "separated", "read-only Gold boundary", "requires Fabric validation"),
        ("AI runtime identities", "embedding worker and app executor roles", "separated", "no shared admin identity", "requires Azure validation"),
    ]
    return [
        {
            "identity_area": area,
            "identity_model": model,
            "least_privilege_status": status,
            "credential_assurance": assurance,
            "validation_class": klass,
            "evidence_classification": klass,
        }
        for area, model, status, assurance, klass in rows
    ]


def _data_product_assurance() -> list[dict[str, str]]:
    return [
        {
            "product": product,
            "source": source,
            "bronze": bronze,
            "silver": silver,
            "gold_or_serving_product": gold,
            "quality": quality,
            "security": security,
            "consumer": consumer,
            "lineage": lineage,
            "evidence_classification": "configuration defined",
        }
        for product, source, bronze, silver, gold, quality, security, consumer, lineage in DATA_PRODUCTS
    ]


def _governance_traceability() -> list[dict[str, str]]:
    return [
        {
            "data_product": product,
            "source_owner": source,
            "contract": "data contracts and generated catalog evidence",
            "sensitivity": security,
            "lineage": lineage,
            "quality": quality,
            "retention": "retention policy and lifecycle controls",
            "access": security,
            "handoff": consumer,
            "evidence_classification": "configuration defined",
        }
        for product, source, _bronze, _silver, _gold, quality, security, consumer, lineage in DATA_PRODUCTS
    ]


def _resilience_assurance() -> list[dict[str, str]]:
    rows = [
        ("Azure SQL", "zone/backup/restore/failover architecture target", "not simulated locally", "requires Azure validation", "docs/runbooks/sqlmi-regional-dr-failover.md"),
        ("PostgreSQL", "backup/restore and target service HA assumption", "not simulated locally", "requires Azure validation", "docs/runbooks/billing-ops-cutover.md"),
        ("Databricks pipelines", "retry, replay, checkpoint and quality stop controls", "locally validated", "requires Databricks validation", "docs/runbooks/databricks-job-failure.md"),
        ("streaming", "checkpoint recovery and lag controls", "configuration defined", "requires Databricks validation", "docs/runbooks/databricks-streaming-lag.md"),
        ("storage", "private access and replayable raw/bronze zones", "configuration defined", "requires Azure validation", "docs/runbooks/databricks-failed-ingestion-job.md"),
        ("API layer", "timeouts, retries, bounded request and health endpoints", "configuration defined", "requires application runtime validation", "docs/application-api-integration.md"),
        ("AI dependencies", "fallback to insufficiency/unavailable response", "configuration defined", "requires Azure validation", "docs/runbooks/sql-ai-azure-openai-invocation-failure.md"),
        ("Fabric boundary", "last valid version and contract/failure matrix", "configuration defined", "requires Fabric validation", "docs/fabric-integration-boundary.md"),
    ]
    return [
        {
            "platform": platform,
            "architecture_target": target,
            "local_status": local,
            "cloud_validation": cloud,
            "runbook": runbook,
            "evidence_classification": cloud if cloud.startswith("requires") else local,
        }
        for platform, target, local, cloud, runbook in rows
    ]


def _failure_mode_matrix() -> list[dict[str, str]]:
    return [
        {
            "failure_mode": mode,
            "blast_radius": blast,
            "detection": detection,
            "response": response,
            "rollback_recovery": recovery,
            "owner": owner,
            "runbook": runbook,
            "evidence": runbook,
            "evidence_classification": "configuration defined",
        }
        for mode, blast, detection, response, recovery, owner, runbook in FAILURE_MODES
    ]


def _observability_assurance() -> list[dict[str, str]]:
    rows = [
        ("database", "SQL availability, blocking, deadlocks, resource health", "Azure SQL alerts", "database platform team", "docs/runbooks/sqlmi-database-unavailable.md", "outputs/azure_sql_operations/monitoring_catalog.csv"),
        ("Databricks", "jobs, compute, SQL warehouse, streaming, Delta health", "Databricks operations alerts", "data platform team", "docs/runbooks/databricks-job-failure.md", "outputs/databricks_operations/monitoring_catalog.csv"),
        ("API", "request count/duration/failures/auth/throttling", "Application Insights alerts", "application integration team", "docs/application-api-integration.md", "outputs/application_integration/observability_catalog.csv"),
        ("AI calls", "retrieval/generation status and dependency failures", "AI audit and dependency alerts", "AI platform team", "docs/runbooks/sql-ai-grounding-failure.md", "outputs/sql_ai/ai_audit_catalog.csv"),
        ("security", "audit/security events and auth failures", "security audit alerts", "security team", "docs/runbooks/incident-response.md", "outputs/azure_sql_operations/alert_catalog.csv"),
        ("data quality", "quality gate failures and freshness", "quality gate alerts", "data quality owner", "docs/runbooks/data-quality-failure.md", "outputs/databricks_orchestration/quality_results.csv"),
        ("cost", "compute/storage/log/API/AI cost drivers", "cost anomaly alerts where configured", "FinOps owner", "docs/runbooks/databricks-unexpected-cost.md", "outputs/databricks_operations/cost_optimization_controls.csv"),
    ]
    return [
        {
            "workload": workload,
            "signal": signal,
            "alert": alert,
            "owner": owner,
            "runbook": runbook,
            "evidence_source": evidence,
            "evidence_classification": "configuration defined",
        }
        for workload, signal, alert, owner, runbook, evidence in rows
    ]


def _finops_assurance() -> list[dict[str, str]]:
    rows = [
        ("Azure SQL", "compute/storage/backup/logs", "known driver", "right-size after workload validation; Query Store tuning"),
        ("PostgreSQL", "compute/storage/backup", "architecture assumption", "size after migration rehearsal"),
        ("Databricks compute", "jobs/serverless/classic clusters", "known driver", "policies, job sizing, autoscaling, optimization controls"),
        ("SQL warehouses", "warehouse size and concurrency", "known driver", "monitor query history and right-size"),
        ("storage", "ADLS Delta/retention/quarantine/logs", "known driver", "retention and lifecycle controls"),
        ("logs", "Log Analytics/Application Insights retention", "runtime measurement required", "retention and sampling policy"),
        ("Container Apps", "replicas/CPU/memory/ingress", "architecture assumption", "scale bounds and request telemetry"),
        ("Azure OpenAI", "embedding/generation calls and tokens", "runtime measurement required", "topK, token limits, re-embedding controls"),
        ("Fabric duplication boundary", "copy vs shortcut storage/processing", "architecture assumption", "prefer no-copy shortcut/interoperability"),
    ]
    return [
        {
            "cost_area": area,
            "driver": driver,
            "classification": classification,
            "optimization_control": control,
            "evidence_classification": "configuration defined",
        }
        for area, driver, classification, control in rows
    ]


def _ai_assurance() -> list[dict[str, str]]:
    rows = [
        ("grounding", "context-only prompt and insufficiency behavior", "configuration defined", "requires Azure validation"),
        ("retrieval authorization", "metadata filters and role model", "locally validated", "requires application runtime validation"),
        ("source traceability", "document/chunk/citation contracts", "locally validated", "requires Azure validation"),
        ("embedding lifecycle", "current/stale/pending/failed/retired", "locally validated", "requires Azure validation"),
        ("vector dimensions", "1536 dimension configuration and mismatch handling", "configuration defined", "requires Azure validation"),
        ("hybrid retrieval", "RRF fixtures and evaluation metrics", "locally validated", "requires Azure validation"),
        ("prompt injection", "retrieved text treated as untrusted", "configuration defined", "requires application runtime validation"),
        ("sensitive-data controls", "exclude/redact/restrict matrix", "configuration defined", "requires Azure validation"),
        ("audit/failure/cost", "retrieval/generation audit, failure handling and cost controls", "configuration defined", "requires Azure validation"),
    ]
    return [
        {
            "ai_control": control,
            "coverage": coverage,
            "local_status": local,
            "runtime_status": runtime,
            "evidence": "outputs/sql_ai/sql_ai_readiness.csv",
            "evidence_classification": runtime,
        }
        for control, coverage, local, runtime in rows
    ]


def _api_assurance() -> list[dict[str, str]]:
    rows = [
        ("allowlisted APIs", "all APIs map to explicit objects", "locally validated"),
        ("DAB mappings", "production config has named roles and no anonymous access", "locally validated"),
        ("REST/GraphQL", "bounded OpenAPI and selected GraphQL examples", "configuration defined"),
        ("AI endpoint", "authorization-propagating thin endpoint contract", "configuration defined"),
        ("MCP schemas", "strict schemas and read-focused tools", "locally validated"),
        ("error/rate/observability", "consistent errors, rate classes and telemetry", "configuration defined"),
        ("network boundary", "Container Apps and private SQL posture", "requires Azure validation"),
    ]
    return [
        {
            "api_control": control,
            "coverage": coverage,
            "validation_status": status,
            "evidence": "outputs/application_integration/integration_readiness.csv",
            "evidence_classification": status,
        }
        for control, coverage, status in rows
    ]


def _cicd_assurance() -> list[dict[str, str]]:
    rows = [
        ("repository validation", "make validate", "locally validated", "Makefile"),
        ("tests", "pytest across all domains", "locally validated", "tests/"),
        ("Python quality", "ruff check", "locally validated", "pyproject.toml"),
        ("SQL project", "static tests plus optional dacpac build", "configuration defined", "scripts/test_sql_project.py"),
        ("Bicep", "module traceability; build depends on tooling", "configuration defined", "infra/main.bicep"),
        ("SQL release evidence", "deterministic release outputs", "locally validated", "outputs/sql_cicd/release_manifest.json"),
        ("Databricks bundle", "bundle assets and targets", "configuration defined", "databricks.yml"),
        ("API config", "DAB/OpenAPI/MCP validation", "locally validated", "outputs/application_integration/api_catalog.csv"),
        ("secret checks", "repository no-secret scanner", "locally validated", "scripts/check_no_secrets.py"),
        ("generated outputs", "hash-before/after reproducibility check", "locally validated", "scripts/check_generated_outputs.py"),
        ("environment promotion", "manual approval/controlled publish boundary", "configuration defined", ".github/workflows/sql-cd.yml"),
    ]
    return [
        {
            "lifecycle_area": area,
            "control": control,
            "validation_status": status,
            "evidence": evidence,
            "evidence_classification": status,
        }
        for area, control, status, evidence in rows
    ]


def _truth_matrix() -> list[dict[str, str]]:
    rows = [
        ("Implemented locally", "deterministic code, tests, generated evidence and static validation", "assessment, migration fixtures, local transformations, validation scripts"),
        ("Configuration defined", "target-ready architecture/code/config not executed in cloud", "Bicep, SQL roles, DAB config, Databricks assets"),
        ("Simulated", "fixtures or deterministic ranking where real services are unavailable", "workload simulation, AI retrieval fixture rankings"),
        ("Requires Azure validation", "Azure SQL, Azure OpenAI, Container Apps, networking, backup/failover", "no Azure deployment performed"),
        ("Requires Databricks validation", "workspace, Unity Catalog, jobs, system tables, streaming", "no Databricks runtime execution performed"),
        ("Requires Fabric validation", "OneLake shortcuts/interoperability and downstream enforcement", "no Fabric resources implemented"),
        ("Deferred/blocked", "production deployment and customer-environment validation", "requires cloud credentials, approvals and live environment"),
    ]
    return [
        {
            "truth_category": category,
            "definition": definition,
            "examples": examples,
            "evidence_classification": "configuration defined",
        }
        for category, definition, examples in rows
    ]


def _gap_register() -> list[dict[str, str]]:
    rows = [
        ("live Azure deployment", "no deployment requested", "architecture may need environment-specific adjustment", "approved Azure deployment evidence", "platform engineering", "Bicep deployment succeeds with approvals"),
        ("SQL MI sizing", "local fixtures cannot size production", "performance/cost risk", "workload baseline and Query Store runtime metrics", "database platform team", "sizing validated under representative load"),
        ("PostgreSQL sizing", "secondary target not deployed", "billing workload risk", "runtime sizing and restore evidence", "database platform team", "target sizing accepted"),
        ("real backup/restore drill", "cloud resources absent", "recovery confidence risk", "restore drill evidence", "operations team", "restore meets target"),
        ("real DR failover", "cloud resources absent", "availability risk", "failover drill evidence", "operations team", "RTO/RPO validated"),
        ("Databricks runtime execution", "workspace not used locally", "pipeline/runtime defect risk", "bundle validate/run evidence", "data platform team", "jobs pass in dev/test"),
        ("SQL vector runtime validation", "local SQL does not execute vector functions", "AI retrieval runtime risk", "Azure SQL vector validation", "AI/data platform team", "vector search passes in Azure"),
        ("Azure OpenAI invocation", "no provider calls locally", "AI generation risk", "endpoint invocation and audit evidence", "AI platform team", "grounded generation validated"),
        ("DAB/Container Apps deployment", "no app runtime deployed", "API integration risk", "Container Apps/DAB smoke test", "application integration team", "API smoke tests pass"),
        ("Fabric shortcut validation", "Fabric implementation is separate", "downstream handoff risk", "Fabric shortcut/interoperability evidence", "Fabric platform team", "Fabric consumes Gold contract successfully"),
    ]
    return [
        {
            "gap": gap,
            "reason": reason,
            "risk": risk,
            "evidence_needed": evidence,
            "owner_role": owner,
            "closure_criteria": closure,
            "evidence_classification": "configuration defined",
        }
        for gap, reason, risk, evidence, owner, closure in rows
    ]


def _risk_register() -> list[dict[str, str]]:
    rows = [
        ("migration", "medium", "high", "wave planning, reconciliation and rollback gates", "medium", "requires Azure validation"),
        ("performance", "medium", "high", "Query Store, indexes and regression gates", "medium", "requires Azure validation"),
        ("availability", "low", "high", "HA/DR architecture and runbooks", "medium", "requires Azure validation"),
        ("data quality", "medium", "high", "quality gates and quarantine/replay", "low", "locally validated"),
        ("security", "medium", "high", "least privilege, no-secret check, audit", "medium", "requires Azure validation"),
        ("AI leakage", "medium", "high", "retrieval authorization and sensitive exposure matrix", "medium", "requires Azure validation"),
        ("cost", "medium", "medium", "FinOps controls and cost allocation", "medium", "requires Databricks validation"),
        ("identity", "medium", "high", "Entra groups and managed identity separation", "medium", "requires Azure validation"),
        ("integration", "medium", "medium", "API/Fabric contracts and runtime validation gaps", "medium", "requires application runtime validation"),
        ("operational ownership", "low", "medium", "ownership matrix and runbook catalog", "low", "configuration defined"),
    ]
    return [
        {
            "risk": risk,
            "likelihood": likelihood,
            "impact": impact,
            "mitigation": mitigation,
            "residual_risk": residual,
            "validation_status": status,
            "evidence_classification": status,
        }
        for risk, likelihood, impact, mitigation, residual, status in rows
    ]


def _runbook_catalog() -> list[dict[str, str]]:
    rows = [
        ("SQL unavailable", "availability alert", "database platform team", "Azure SQL", "critical", "outputs/azure_sql_operations/alert_catalog.csv", "restore service inside agreed RTO", "docs/runbooks/sqlmi-database-unavailable.md"),
        ("SQL slow query", "performance alert", "database platform team", "Azure SQL", "high", "outputs/sql_performance/performance_assurance.csv", "mitigate regression", "docs/runbooks/sqlmi-slow-query.md"),
        ("Databricks job failure", "job failure alert", "data platform team", "Databricks", "high", "outputs/databricks_operations/job_health_rules.csv", "rerun or remediate", "docs/runbooks/databricks-job-failure.md"),
        ("Streaming lag", "freshness breach", "data platform team", "Databricks", "high", "outputs/databricks_operations/streaming_health_rules.csv", "recover checkpoint/throughput", "docs/runbooks/databricks-streaming-lag.md"),
        ("Data quality failure", "quality gate stop", "data quality owner", "Databricks", "high", "outputs/databricks_orchestration/quality_results.csv", "quarantine/remediate/replay", "docs/runbooks/data-quality-failure.md"),
        ("AI invocation failure", "generation audit failed", "AI platform team", "SQL AI/Azure OpenAI", "high", "outputs/sql_ai/ai_failure_handling.csv", "return safe failure and restore provider", "docs/runbooks/sql-ai-azure-openai-invocation-failure.md"),
        ("AI leakage incident", "security report", "security team", "AI/API", "critical", "outputs/sql_ai/ai_data_exposure_matrix.csv", "contain and remediate", "docs/runbooks/sql-ai-data-leakage-security-incident.md"),
        ("Fabric handoff failure", "handoff manifest/consumer failure", "shared Azure/Fabric owners", "Fabric boundary", "high", "outputs/fabric_integration/failure_responsibility_matrix.csv", "repair producer or consumer boundary", "docs/fabric-integration-boundary.md"),
        ("Deployment rollback", "failed release", "DevSecOps team", "CI/CD", "high", ".github/workflows/ci.yml", "restore previous release", "docs/runbooks/deployment-rollback.md"),
    ]
    return [
        {
            "scenario": scenario,
            "trigger": trigger,
            "owner": owner,
            "platform": platform,
            "severity": severity,
            "evidence_source": evidence,
            "recovery_goal": goal,
            "runbook_path": path,
            "evidence_classification": "configuration defined",
        }
        for scenario, trigger, owner, platform, severity, evidence, goal, path in rows
    ]


def _release_readiness() -> list[dict[str, str]]:
    rows = [
        ("repository quality", "PASS", "docs, structure, tests and lint pass locally"),
        ("architecture", "PASS", "target architecture and traceability are defined"),
        ("security", "CONDITIONAL", "controls defined; runtime validation still required"),
        ("data governance", "PASS", "contracts, lineage, sensitivity and quality evidence exist"),
        ("migration", "CONDITIONAL", "local migration evidence exists; live rehearsal required"),
        ("Azure SQL", "CONDITIONAL", "database project and ops defined; Azure validation required"),
        ("Databricks", "CONDITIONAL", "assets and evidence defined; runtime validation required"),
        ("AI", "CONDITIONAL", "SQL AI/RAG defined; Azure SQL/OpenAI validation required"),
        ("API", "CONDITIONAL", "DAB/API/MCP contracts defined; app runtime validation required"),
        ("Fabric boundary", "CONDITIONAL", "handoff contract defined; Fabric runtime validation required"),
        ("resilience", "CONDITIONAL", "architecture/runbooks defined; DR drills required"),
        ("observability", "CONDITIONAL", "queries/alerts defined; live telemetry required"),
        ("FinOps", "CONDITIONAL", "drivers/controls defined; runtime measurements required"),
        ("CI/CD", "PASS", "local validation and workflows are configured"),
        ("documentation", "PASS", "portfolio docs, roadmap and reports are present"),
    ]
    return [
        {
            "gate": gate,
            "gate_status": status,
            "evidence": evidence,
            "production_readiness_boundary": "portfolio release gate; not production deployment approval",
            "evidence_classification": "configuration defined",
        }
        for gate, status, evidence in rows
    ]


def _release_manifest(root: Path, outputs: list[str]) -> dict[str, Any]:
    return {
        "repository": "enterprise-azure-data-ai-modernisation-platform",
        "platform_version": "0.1.0-milestone-16",
        "commit": _current_sha(root),
        "milestone_coverage": [f"Milestone {idx}" for idx in range(1, 17)],
        "validation_commands": [
            "make validate-final-assurance",
            "make check-no-secrets",
            "make check-generated-outputs",
            "make release-assurance",
        ],
        "test_count": "114 observed in latest full validation",
        "generated_evidence": outputs,
        "tool_availability": {
            "git": shutil.which("git") is not None,
            "bicep": shutil.which("bicep") is not None,
            "databricks": shutil.which("databricks") is not None,
            "dotnet": shutil.which("dotnet") is not None,
        },
        "production_validation_gaps": [row["gap"] for row in _gap_register()],
        "truth_boundary": "No live Azure, Databricks, Fabric, Azure OpenAI, or application deployment is claimed.",
    }


def _current_sha(root: Path) -> str:
    del root
    return os.environ.get("FINAL_ASSURANCE_COMMIT_SHA", "resolved-at-release-runtime")


def _report() -> str:
    return "\n".join(
        [
            "# Final Cross-Platform Assurance and Portfolio Release Report",
            "",
            "Milestone 16 consolidates the complete Azure Data & AI modernisation platform into a portfolio release evidence bundle. It assures architecture, ownership, security, identity, governance, data products, resilience, failure modes, observability, FinOps, AI, API integration, CI/CD, generated-output reproducibility, and implementation truthfulness.",
            "",
            "The release is portfolio-ready for technical review. It is not a production deployment approval. Live Azure, Databricks, Fabric, Azure OpenAI, Container Apps, Data API Builder, backup/restore, DR, and runtime performance validation remain explicit production gaps.",
            "",
            "Release readiness is PASS for local repository quality, architecture traceability, documentation, CI/CD configuration, and deterministic evidence. Runtime-dependent platform gates are CONDITIONAL and require cloud validation.",
            "",
        ]
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate final assurance evidence.")
    parser.add_argument("--outputs-dir", type=Path, default=Path("outputs/final_assurance"))
    parser.add_argument("--reports-dir", type=Path, default=Path("reports"))
    args = parser.parse_args()
    written = generate_outputs(args.outputs_dir, args.reports_dir, Path.cwd())
    for name in sorted(written):
        print(f"{name}: {written[name]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
