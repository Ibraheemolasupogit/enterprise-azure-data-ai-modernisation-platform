from __future__ import annotations

from pathlib import Path

from scripts import validate_docs, validate_structure

ROOT = Path(__file__).resolve().parents[1]


def test_required_foundation_structure_exists() -> None:
    assert validate_structure.validate_required_paths() == []


def test_readme_positions_current_scope_honestly() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "does not deploy Azure resources" in readme
    assert "does not claim working AI workloads" in readme
    assert "certification" not in readme.lower()


def test_initial_adrs_have_required_metadata() -> None:
    assert validate_structure.validate_adr_metadata() == []


def test_roadmap_preserves_required_scope() -> None:
    assert validate_structure.validate_roadmap_scope() == []


def test_markdown_links_are_valid() -> None:
    assert validate_docs.validate_links() == []

