from __future__ import annotations

import argparse

from databricks_orchestration.quality import classify_retry, gate_allows_publication


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Databricks Lakeflow Jobs task entrypoint.")
    parser.add_argument("--environment", required=True)
    parser.add_argument("--catalog", required=True)
    parser.add_argument("--source-system", default="all")
    parser.add_argument("--processing-date", required=True)
    parser.add_argument(
        "--load-type",
        choices=["batch", "incremental", "streaming", "backfill"],
        required=True,
    )
    parser.add_argument("--checkpoint-path", default="")
    parser.add_argument("--schema", default="")
    parser.add_argument("--replay-mode", choices=["none", "quarantine", "range"], default="none")
    parser.add_argument("--task", required=True)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    print(f"task={args.task}")
    print(f"environment={args.environment}")
    print(f"catalog={args.catalog}")
    print(f"source_system={args.source_system}")
    print(f"load_type={args.load_type}")
    print(f"retry_policy={classify_retry('transient platform failure')}")
    gate_result = gate_allows_publication({"dummy": {"critical_failures": 0}}, ["dummy"])
    print(f"publication_gate={gate_result}")
    print("runtime_boundary=requires Databricks runtime validation")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
