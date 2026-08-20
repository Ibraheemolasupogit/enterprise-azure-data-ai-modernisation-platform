from __future__ import annotations

from pathlib import Path

from migration_factory.validation import validate_migration_outputs


def main() -> int:
    failures = validate_migration_outputs(Path("outputs/migration"))
    if failures:
        print("Migration validation failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("Migration validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

