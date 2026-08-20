from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IGNORED_PARTS = {".git", ".pytest_cache", ".ruff_cache", "__pycache__", ".venv"}
TEXT_SUFFIXES = {
    ".bicep",
    ".csv",
    ".json",
    ".kql",
    ".md",
    ".py",
    ".sql",
    ".toml",
    ".yaml",
    ".yml",
    ".graphql",
    ".example",
}

PATTERNS = [
    ("private key", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("access key", re.compile(r"\b(AccountKey|SharedAccessKey)=[^<;\s]{12,}", re.IGNORECASE)),
    ("sas token", re.compile(r"(\?|&)sig=[A-Za-z0-9%+/]{20,}", re.IGNORECASE)),
    ("bearer token", re.compile(r"\bBearer\s+[A-Za-z0-9._~+/=-]{20,}", re.IGNORECASE)),
    (
        "client secret",
        re.compile(r"\bclient[_-]?secret\b\s*[:=]\s*['\"][^<][^'\"]{8,}", re.IGNORECASE),
    ),
    (
        "api key",
        re.compile(
            r"\b(api[_-]?key|subscription[_-]?key)\b\s*[:=]\s*['\"][^<][^'\"]{8,}",
            re.IGNORECASE,
        ),
    ),
    ("password", re.compile(r"\bpassword\b\s*[:=]\s*['\"]?[^<\s'\"]{8,}", re.IGNORECASE)),
    ("github pat", re.compile(r"\bgh[pousr]_[A-Za-z0-9_]{20,}")),
]

ALLOWLIST_SNIPPETS = {
    "forbidden =",
    "password=|AccountKey=|SharedAccessSignature=",
    "No API keys",
    "no connection string or password is committed",
}


def iter_files() -> list[Path]:
    return sorted(
        path
        for path in ROOT.rglob("*")
        if path.is_file()
        and not any(part in IGNORED_PARTS for part in path.relative_to(ROOT).parts)
        and (path.suffix in TEXT_SUFFIXES or path.name.endswith(".env.example"))
    )


def main() -> int:
    findings: list[str] = []
    for path in iter_files():
        text = path.read_text(encoding="utf-8", errors="ignore")
        for line_number, line in enumerate(text.splitlines(), start=1):
            if any(snippet in line for snippet in ALLOWLIST_SNIPPETS):
                continue
            for label, pattern in PATTERNS:
                if pattern.search(line):
                    findings.append(f"{path.relative_to(ROOT)}:{line_number}: possible {label}")
    if findings:
        print("Secret assurance failed:")
        for finding in findings:
            print(f"- {finding}")
        return 1
    print("Secret assurance passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
