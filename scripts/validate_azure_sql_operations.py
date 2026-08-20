from __future__ import annotations

from pathlib import Path

from azure_sql_operations.validation import validate_outputs


def main() -> int:
    failures = validate_outputs(Path("outputs/azure_sql_operations"))
    if failures:
        print("Azure SQL operations validation failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("Azure SQL operations validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

