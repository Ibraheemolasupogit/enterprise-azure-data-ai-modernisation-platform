from __future__ import annotations

import argparse

from databricks.pipelines.autoloader_carrier_updates import AUTO_LOADER_EXPECTATIONS
from databricks.pipelines.streaming_shipment_events import STREAMING_SEMANTICS


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Databricks ingestion module wiring.")
    parser.add_argument("--catalog", required=True)
    parser.add_argument("--environment", required=True)
    args = parser.parse_args()
    print(f"Catalog: {args.catalog}")
    print(f"Environment: {args.environment}")
    print(f"Auto Loader boundary: {AUTO_LOADER_EXPECTATIONS['runtime_boundary']}")
    print(f"Streaming watermark: {STREAMING_SEMANTICS['watermark']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
