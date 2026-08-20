from __future__ import annotations

from pathlib import Path

from application_integration.validation import validate_outputs


def main() -> int:
    failures = validate_outputs(Path("outputs/application_integration"), Path.cwd())
    if failures:
        for failure in failures:
            print(f"Application integration validation failure: {failure}")
        return 1
    print("Application integration validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
