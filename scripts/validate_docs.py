from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MARKDOWN_LINK = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")


def iter_markdown_files() -> list[Path]:
    ignored_parts = {".git", ".venv", ".pytest_cache", ".ruff_cache"}
    return sorted(
        path
        for path in ROOT.rglob("*.md")
        if not any(part in ignored_parts for part in path.relative_to(ROOT).parts)
    )


def target_exists(source: Path, target: str) -> bool:
    if target.startswith(("http://", "https://", "mailto:")):
        return True
    clean_target = target.split("#", maxsplit=1)[0]
    if not clean_target:
        return True
    return (source.parent / clean_target).resolve().exists()


def validate_links() -> list[str]:
    failures: list[str] = []
    for path in iter_markdown_files():
        text = path.read_text(encoding="utf-8")
        for match in MARKDOWN_LINK.finditer(text):
            target = match.group(1)
            if not target_exists(path, target):
                failures.append(f"{path.relative_to(ROOT)} has broken link: {target}")
    return failures


def validate_no_recruiter_language() -> list[str]:
    forbidden_terms = ["recruiter", "certification"]
    failures: list[str] = []
    for path in iter_markdown_files():
        text = path.read_text(encoding="utf-8").lower()
        for term in forbidden_terms:
            if term in text:
                relative_path = path.relative_to(ROOT)
                failures.append(
                    f"{relative_path} contains forbidden positioning term: {term}"
                )
    return failures


def main() -> int:
    failures = validate_links() + validate_no_recruiter_language()
    if failures:
        print("Documentation validation failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("Documentation validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
