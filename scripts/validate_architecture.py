from __future__ import annotations

from pathlib import Path

from target_architecture.validation import validate_architecture_outputs


def main() -> int:
    failures = validate_architecture_outputs(Path("outputs/architecture"))
    if failures:
        print("Architecture validation failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("Architecture validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

