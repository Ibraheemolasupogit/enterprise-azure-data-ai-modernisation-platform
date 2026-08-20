from __future__ import annotations

from pathlib import Path

from estate_assessment.validation import validate_assessment_outputs


def main() -> int:
    failures = validate_assessment_outputs(Path("outputs"))
    if failures:
        print("Assessment validation failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("Assessment validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
