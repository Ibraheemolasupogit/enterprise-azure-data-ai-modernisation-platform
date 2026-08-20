from __future__ import annotations

from databricks.common.paths import checkpoint_path, landing_path, schema_path


def carrier_updates_stream(spark, catalog: str, storage_account: str, environment: str):
    source_path = landing_path(storage_account, "partner/carrier_updates")
    schema_location = schema_path(storage_account, environment, "carrier_updates")
    checkpoint = checkpoint_path(storage_account, environment, "autoloader/carrier_updates")
    return (
        spark.readStream.format("cloudFiles")
        .option("cloudFiles.format", "json")
        .option("cloudFiles.schemaLocation", schema_location)
        .option("cloudFiles.schemaEvolutionMode", "rescue")
        .option("rescuedDataColumn", "_rescued_data")
        .option("cloudFiles.inferColumnTypes", "true")
        .load(source_path)
        .writeStream.format("delta")
        .option("checkpointLocation", checkpoint)
        .outputMode("append")
        .toTable(f"{catalog}.bronze.carrier_updates")
    )


AUTO_LOADER_EXPECTATIONS = {
    "file_discovery": "cloudFiles exactly-once file discovery in Databricks runtime",
    "schema_location": "schema inference/evolution state stored outside data table",
    "checkpoint": "stream offset and commit log persisted under checkpoints container",
    "drift": "additive fields rescued first, promoted only after contract review",
    "runtime_boundary": "requires Databricks runtime validation",
}

