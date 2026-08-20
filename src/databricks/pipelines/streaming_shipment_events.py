from __future__ import annotations

from databricks.common.paths import checkpoint_path, landing_path
from databricks.common.schemas import shipment_event_schema


def shipment_event_stream(spark, catalog: str, storage_account: str, environment: str):
    source_path = landing_path(storage_account, "events/shipment_operational_events")
    checkpoint = checkpoint_path(
        storage_account,
        environment,
        "streaming/shipment_operational_events",
    )
    events = (
        spark.readStream.schema(shipment_event_schema())
        .json(source_path)
        .withWatermark("occurred_at", "2 hours")
        .dropDuplicates(["event_id"])
    )
    return (
        events.writeStream.format("delta")
        .option("checkpointLocation", checkpoint)
        .outputMode("append")
        .toTable(f"{catalog}.bronze.shipment_operational_events")
    )


STREAMING_SEMANTICS = {
    "event_time": "occurred_at",
    "watermark": "2 hours for representative late-arrival handling",
    "dedupe": "event_id",
    "output_mode": "append after deduplication",
    "late_events": "events later than watermark require quarantine/replay workflow",
}
