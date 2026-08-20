.PHONY: help validate test lint docs-check structure-check assessment-check architecture-check migration-check generate-estate generate-workload assess-estate validate-architecture migrate-local validate-migration

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
	@echo "  make generate-estate Generate the default synthetic legacy estate"
	@echo "  make generate-workload Generate the default workload simulation"
	@echo "  make assess-estate   Generate and validate estate assessment outputs"

validate: docs-check structure-check assessment-check architecture-check migration-check test lint

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
