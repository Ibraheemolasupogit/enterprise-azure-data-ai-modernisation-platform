from __future__ import annotations

from pathlib import Path

from sql_cicd.validation import validate_outputs

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    failures = validate_outputs(ROOT / "outputs/sql_cicd", ROOT)
    if failures:
        print("SQL CI/CD validation failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("SQL CI/CD validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

