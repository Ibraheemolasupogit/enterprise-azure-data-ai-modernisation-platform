from __future__ import annotations

from databricks.common.paths import checkpoint_path, landing_path


def copy_depot_reference_sql(catalog: str, storage_account: str) -> str:
    source_path = landing_path(storage_account, "partner/depot_reference")
    return f"""
COPY INTO {catalog}.bronze.depot_reference_feed
FROM '{source_path}'
FILEFORMAT = CSV
FORMAT_OPTIONS ('header' = 'true', 'inferSchema' = 'false')
COPY_OPTIONS ('mergeSchema' = 'false');
"""


def load_customer_service_export(spark, catalog: str, storage_account: str):
    source_path = landing_path(storage_account, "customer_service_export")
    checkpoint = checkpoint_path(storage_account, "${bundle.target}", "customer_service_export")
    return (
        spark.read.format("csv")
        .option("header", "true")
        .load(source_path)
        .withColumn("_source_system", spark.sql.functions.lit("customer_service_export"))
        .write.format("delta")
        .mode("append")
        .option("checkpointLocation", checkpoint)
        .saveAsTable(f"{catalog}.bronze.customer_service_export")
    )


def incremental_merge_sql(catalog: str) -> str:
    return f"""
MERGE INTO {catalog}.silver.billing_invoices AS target
USING {catalog}.bronze.billing_ops_invoices AS source
ON target.invoice_id = source.invoice_id
WHEN MATCHED AND source._record_hash <> target._record_hash THEN UPDATE SET *
WHEN NOT MATCHED THEN INSERT *;
"""

