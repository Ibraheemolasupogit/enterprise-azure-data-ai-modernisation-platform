from __future__ import annotations

from pathlib import Path

from sql_ai.validation import validate_outputs


def main() -> int:
    failures = validate_outputs(Path("outputs/sql_ai"), Path.cwd())
    if failures:
        for failure in failures:
            print(f"SQL AI validation failure: {failure}")
        return 1
    print("SQL AI validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
