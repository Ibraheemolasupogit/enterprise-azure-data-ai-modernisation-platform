from __future__ import annotations

try:
    from pyspark.sql.types import (
        BooleanType,
        DoubleType,
        IntegerType,
        StringType,
        StructField,
        StructType,
        TimestampType,
    )
except ImportError:  # pragma: no cover - imported only in Databricks/Spark runtime.
    BooleanType = DoubleType = IntegerType = None
    StringType = StructField = StructType = TimestampType = None


def shipment_event_schema():
    return StructType(
        [
            StructField("event_id", StringType(), False),
            StructField("event_type", StringType(), False),
            StructField("aggregate_type", StringType(), False),
            StructField("aggregate_id", StringType(), False),
            StructField("occurred_at", TimestampType(), False),
            StructField("schema_version", IntegerType(), False),
            StructField("payload", StringType(), True),
        ]
    )


def shipment_schema():
    return StructType(
        [
            StructField("shipment_id", StringType(), False),
            StructField("customer_id", StringType(), False),
            StructField("route_id", StringType(), False),
            StructField("assigned_vehicle_id", StringType(), True),
            StructField("external_order_ref", StringType(), False),
            StructField("shipment_status", StringType(), False),
            StructField("created_at", TimestampType(), False),
            StructField("promised_delivery_at", TimestampType(), False),
            StructField("delivered_at", TimestampType(), True),
            StructField("declared_value_gbp", DoubleType(), False),
            StructField("hazmat_flag", BooleanType(), False),
        ]
    )
