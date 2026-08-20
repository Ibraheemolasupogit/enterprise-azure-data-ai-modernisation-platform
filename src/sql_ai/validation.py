from __future__ import annotations

import csv
from pathlib import Path

REQUIRED_FILES = [
    "ai_use_case_catalog.csv",
    "ai_schema_catalog.csv",
    "document_source_matrix.csv",
    "chunking_strategy.csv",
    "embedding_configuration.csv",
    "embedding_lifecycle.csv",
    "change_detection_strategy.csv",
    "lexical_search_catalog.csv",
    "vector_search_catalog.csv",
    "hybrid_retrieval_strategy.csv",
    "retrieval_evaluation_dataset.csv",
    "retrieval_evaluation_results.csv",
    "rag_context_contract.csv",
    "rag_execution_steps.csv",
    "ai_security_matrix.csv",
    "ai_data_exposure_matrix.csv",
    "ai_audit_catalog.csv",
    "ai_failure_handling.csv",
    "ai_cost_controls.csv",
    "sql_ai_readiness.csv",
]

CLASSIFICATIONS = {
    "locally validated",
    "configuration defined",
    "simulated",
    "requires Azure SQL validation",
    "requires Azure OpenAI validation",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def validate_outputs(outputs_dir: Path, repo_root: Path) -> list[str]:
    failures: list[str] = []
    for filename in REQUIRED_FILES:
        path = outputs_dir / filename
        if not path.is_file():
            failures.append(f"missing SQL AI output: {filename}")
        elif not read_csv(path):
            failures.append(f"empty SQL AI output: {filename}")
    if failures:
        return failures

    for filename in REQUIRED_FILES:
        rows = read_csv(outputs_dir / filename)
        if "evidence_classification" in rows[0]:
            unknown = {row["evidence_classification"] for row in rows} - CLASSIFICATIONS
            if unknown:
                failures.append(
                    f"{filename} has unsupported evidence classifications: {sorted(unknown)}"
                )

    required_assets = [
        "src/azure_sql/ai/schema/01_ai_tables.sql",
        "src/azure_sql/ai/chunking/ai_generate_chunks_example.sql",
        "src/azure_sql/ai/embeddings/create_external_model_example.sql",
        "src/azure_sql/ai/embeddings/ai_generate_embeddings_example.sql",
        "src/azure_sql/ai/search/full_text_search.sql",
        "src/azure_sql/ai/search/vector_search.sql",
        "src/azure_sql/ai/search/hybrid_rrf.sql",
        "src/azure_sql/ai/rag/sql_native_rag_sequence.sql",
        "src/azure_sql/ai/security/ai_security.sql",
        "src/azure_sql/ai/audit/audit_queries.sql",
        "src/azure_sql/ai/examples/context_payload.sql",
        "src/azure_sql/database_project/legacy_tms/Schemas/ai.sql",
        "src/azure_sql/database_project/legacy_tms/Tables/ai.Document.sql",
        "src/azure_sql/database_project/legacy_tms/Tables/ai.DocumentChunk.sql",
        "src/azure_sql/database_project/legacy_tms/Tables/ai.EmbeddingMetadata.sql",
        "src/azure_sql/database_project/legacy_tms/Tables/ai.RetrievalAudit.sql",
        "src/azure_sql/database_project/legacy_tms/Tables/ai.GenerationAudit.sql",
        "src/azure_sql/database_project/legacy_tms/StoredProcedures/ai.usp_AssembleRagContext.sql",
        "src/azure_sql/database_project/legacy_tms/Security/AiRolesAndPermissions.sql",
        "reports/sql_ai_report.md",
        "docs/sql-ai-rag.md",
    ]
    missing_assets = [asset for asset in required_assets if not (repo_root / asset).is_file()]
    if missing_assets:
        failures.append(f"missing SQL AI assets: {missing_assets}")

    readiness = read_csv(outputs_dir / "sql_ai_readiness.csv")
    if not any(row["status"] == "requires Azure SQL validation" for row in readiness):
        failures.append("readiness must preserve Azure SQL validation boundary")
    if not any(row["status"] == "requires Azure OpenAI validation" for row in readiness):
        failures.append("readiness must preserve Azure OpenAI validation boundary")

    security = read_csv(outputs_dir / "ai_security_matrix.csv")
    for role in {"ai_app_executor", "ai_data_curator", "ai_auditor", "embedding_worker_identity"}:
        if role not in {row["principal_or_role"] for row in security}:
            failures.append(f"security matrix missing {role}")

    exposure = read_csv(outputs_dir / "ai_data_exposure_matrix.csv")
    if not any(row["ai_context_policy"] == "exclude or redact" for row in exposure):
        failures.append("data exposure matrix must include exclude or redact controls")

    failure = read_csv(outputs_dir / "ai_failure_handling.csv")
    for required in ("dimension mismatch", "provider unavailable", "suspected data leakage"):
        if not any(required in row["failure_mode"] for row in failure):
            failures.append(f"failure handling missing {required}")

    sql_text = "\n".join(
        (repo_root / path).read_text(encoding="utf-8")
        for path in required_assets
        if path.endswith(".sql") and (repo_root / path).is_file()
    )
    required_sql_terms = (
        "VECTOR(",
        "VECTOR_DISTANCE",
        "VECTOR_SEARCH",
        "AI_GENERATE_EMBEDDINGS",
        "AI_GENERATE_CHUNKS",
        "sp_invoke_external_rest_endpoint",
    )
    for term in required_sql_terms:
        if term not in sql_text:
            failures.append(f"SQL AI assets missing {term}")
    if "SECRET =" in sql_text and "<" not in sql_text:
        failures.append("SQL AI assets must not contain concrete secrets")

    return failures
