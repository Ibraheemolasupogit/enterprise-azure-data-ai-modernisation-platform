from __future__ import annotations

from pathlib import Path

from databricks_foundation.validation import validate_outputs

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    failures = validate_outputs(ROOT / "outputs/databricks_foundation", ROOT)
    if failures:
        print("Databricks foundation validation failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("Databricks foundation validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

