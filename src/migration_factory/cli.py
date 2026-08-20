from __future__ import annotations

import argparse
from pathlib import Path

from migration_factory.execution import run_migration_factory
from migration_factory.validation import validate_migration_outputs


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the local Contoso Freight migration factory.")
    parser.add_argument(
        "--system",
        default="",
        help="Optional system scope: legacy_tms or billing_ops.",
    )
    parser.add_argument("--outputs-dir", type=Path, default=Path("outputs/migration"))
    parser.add_argument("--reports-dir", type=Path, default=Path("reports"))
    parser.add_argument("--failure-scenario", default="")
    args = parser.parse_args()

    written = run_migration_factory(
        args.outputs_dir,
        args.reports_dir,
        system=args.system,
        failure_scenario=args.failure_scenario,
    )
    failures = []
    if not args.failure_scenario and not args.system:
        failures = validate_migration_outputs(args.outputs_dir)
    if failures:
        for failure in failures:
            print(f"- {failure}")
        return 1
    for name in sorted(written):
        print(f"{name}: {written[name]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
