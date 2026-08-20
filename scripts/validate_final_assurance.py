from __future__ import annotations

from pathlib import Path

from final_assurance.validation import validate_outputs


def main() -> int:
    failures = validate_outputs(Path("outputs/final_assurance"), Path.cwd())
    if failures:
        for failure in failures:
            print(f"Final assurance validation failure: {failure}")
        return 1
    print("Final assurance validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
