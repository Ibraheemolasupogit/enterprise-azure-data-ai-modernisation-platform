from __future__ import annotations

from pathlib import Path

from sql_performance.validation import validate_outputs


def main() -> int:
    failures = validate_outputs(Path("outputs/sql_performance"))
    if failures:
        print("SQL performance validation failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("SQL performance validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

