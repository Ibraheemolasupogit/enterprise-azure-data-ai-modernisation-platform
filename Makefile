.PHONY: help validate test lint docs-check structure-check assessment-check architecture-check migration-check azure-sql-operations-check sql-performance-check sql-cicd-check sql-ai-check databricks-foundation-check databricks-pipelines-check databricks-orchestration-check databricks-operations-check generate-estate generate-workload assess-estate validate-architecture migrate-local validate-migration validate-azure-sql-operations generate-sql-performance-evidence validate-sql-performance generate-sql-release-evidence validate-sql-cicd generate-sql-ai-evidence validate-sql-ai build-sql-project test-sql-project generate-databricks-foundation-evidence validate-databricks-foundation generate-databricks-pipeline-evidence validate-databricks-pipelines generate-databricks-orchestration-evidence validate-databricks-orchestration generate-databricks-operations-evidence validate-databricks-operations

PYTHON ?= python3

help:
	@echo "Available commands:"
	@echo "  make validate        Run all local validation"
	@echo "  make test            Run pytest"
	@echo "  make lint            Run Ruff if installed"
	@echo "  make docs-check      Validate documentation links and required docs"
	@echo "  make structure-check Validate repository foundation structure"
	@echo "  make assessment-check Validate generated assessment outputs"
	@echo "  make validate-architecture Generate and validate architecture outputs"
	@echo "  make migrate-local    Run local deterministic migration factory"
	@echo "  make validate-migration Validate generated migration evidence"
	@echo "  make validate-azure-sql-operations Generate and validate Azure SQL operations evidence"
	@echo "  make validate-sql-performance Generate and validate SQL performance evidence"
	@echo "  make validate-sql-cicd Generate and validate SQL database lifecycle evidence"
	@echo "  make validate-sql-ai Generate and validate SQL AI/vector/RAG evidence"
	@echo "  make validate-databricks-foundation Generate and validate Databricks foundation evidence"
	@echo "  make validate-databricks-pipelines Generate and validate Databricks pipeline evidence"
	@echo "  make validate-databricks-orchestration Generate and validate Databricks orchestration evidence"
	@echo "  make validate-databricks-operations Generate and validate Databricks operations evidence"
	@echo "  make build-sql-project Build the SQL project dacpac when dotnet is available"
	@echo "  make test-sql-project Run static SQL project tests"
	@echo "  make generate-estate Generate the default synthetic legacy estate"
	@echo "  make generate-workload Generate the default workload simulation"
	@echo "  make assess-estate   Generate and validate estate assessment outputs"

validate: docs-check structure-check assessment-check architecture-check migration-check azure-sql-operations-check sql-performance-check sql-cicd-check sql-ai-check databricks-foundation-check databricks-pipelines-check databricks-orchestration-check databricks-operations-check test lint

test:
	$(PYTHON) -m pytest

lint:
	$(PYTHON) -m ruff check .

docs-check:
	$(PYTHON) scripts/validate_docs.py

structure-check:
	$(PYTHON) scripts/validate_structure.py

assessment-check:
	$(PYTHON) scripts/validate_assessment.py

architecture-check:
	$(PYTHON) scripts/validate_architecture.py

migration-check:
	$(PYTHON) scripts/validate_migration.py

azure-sql-operations-check:
	$(PYTHON) scripts/validate_azure_sql_operations.py

sql-performance-check:
	$(PYTHON) scripts/validate_sql_performance.py

sql-cicd-check:
	$(PYTHON) scripts/validate_sql_cicd.py

sql-ai-check:
	$(PYTHON) scripts/validate_sql_ai.py

databricks-foundation-check:
	$(PYTHON) scripts/validate_databricks_foundation.py

databricks-pipelines-check:
	$(PYTHON) scripts/validate_databricks_pipelines.py

databricks-orchestration-check:
	$(PYTHON) scripts/validate_databricks_orchestration.py

databricks-operations-check:
	$(PYTHON) scripts/validate_databricks_operations.py

generate-estate:
	$(PYTHON) -m legacy_estate.generator --profile development --output-dir data/raw/legacy_estate

generate-workload:
	$(PYTHON) -m legacy_estate.workload --operations 250 --output-path data/raw/legacy_estate/workload.jsonl

assess-estate:
	$(PYTHON) -m estate_assessment.cli --outputs-dir outputs --reports-dir reports

validate-architecture:
	$(PYTHON) -m target_architecture.cli --outputs-dir outputs/architecture --reports-dir reports
	$(PYTHON) scripts/validate_architecture.py

migrate-local:
	$(PYTHON) -m migration_factory.cli --system "$(SYSTEM)" --outputs-dir outputs/migration --reports-dir reports

validate-migration:
	$(PYTHON) scripts/validate_migration.py

validate-azure-sql-operations:
	$(PYTHON) -m azure_sql_operations.cli --outputs-dir outputs/azure_sql_operations --reports-dir reports
	$(PYTHON) scripts/validate_azure_sql_operations.py

generate-sql-performance-evidence:
	$(PYTHON) -m sql_performance.cli --outputs-dir outputs/sql_performance --reports-dir reports

validate-sql-performance: generate-sql-performance-evidence
	$(PYTHON) scripts/validate_sql_performance.py

generate-sql-release-evidence:
	$(PYTHON) -m sql_cicd.cli --outputs-dir outputs/sql_cicd --reports-dir reports

validate-sql-cicd: generate-sql-release-evidence test-sql-project
	$(PYTHON) scripts/validate_sql_cicd.py

generate-sql-ai-evidence:
	$(PYTHON) -m sql_ai.cli --outputs-dir outputs/sql_ai --reports-dir reports

validate-sql-ai: generate-sql-ai-evidence
	$(PYTHON) scripts/validate_sql_ai.py

build-sql-project:
	$(PYTHON) scripts/build_sql_project.py

test-sql-project:
	$(PYTHON) scripts/test_sql_project.py

generate-databricks-foundation-evidence:
	$(PYTHON) -m databricks_foundation.cli --outputs-dir outputs/databricks_foundation --reports-dir reports

validate-databricks-foundation: generate-databricks-foundation-evidence
	$(PYTHON) scripts/validate_databricks_foundation.py

generate-databricks-pipeline-evidence:
	$(PYTHON) -m databricks_pipelines.cli --outputs-dir outputs/databricks_pipelines --reports-dir reports

validate-databricks-pipelines: generate-databricks-pipeline-evidence
	$(PYTHON) scripts/validate_databricks_pipelines.py

generate-databricks-orchestration-evidence:
	$(PYTHON) -m databricks_orchestration.cli --outputs-dir outputs/databricks_orchestration --reports-dir reports

validate-databricks-orchestration: generate-databricks-orchestration-evidence
	$(PYTHON) scripts/validate_databricks_orchestration.py

generate-databricks-operations-evidence:
	$(PYTHON) -m databricks_operations.cli --outputs-dir outputs/databricks_operations --reports-dir reports

validate-databricks-operations: generate-databricks-operations-evidence
	$(PYTHON) scripts/validate_databricks_operations.py
