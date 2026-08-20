from __future__ import annotations

from pathlib import Path

from fabric_integration.validation import validate_outputs


def main() -> int:
    failures = validate_outputs(Path("outputs/fabric_integration"), Path.cwd())
    if failures:
        for failure in failures:
            print(f"Fabric integration validation failure: {failure}")
        return 1
    print("Fabric integration validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
