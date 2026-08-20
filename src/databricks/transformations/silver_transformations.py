from __future__ import annotations

from pyspark.sql import functions as F


def normalize_shipment_status(column):
    return (
        F.when(column == "allocated", "assigned")
        .when(column == "exception", "delayed")
        .otherwise(column)
    )


def silver_shipments(bronze_shipments, customers, routes):
    return (
        bronze_shipments.withColumn(
            "shipment_status",
            normalize_shipment_status(F.lower("shipment_status")),
        )
        .withColumn("created_at_utc", F.to_timestamp("created_at"))
        .withColumn("promised_delivery_at_utc", F.to_timestamp("promised_delivery_at"))
        .join(customers.select("customer_id"), "customer_id", "left_semi")
        .join(routes.select("route_id"), "route_id", "left_semi")
        .dropDuplicates(["shipment_id"])
    )


def invalid_shipments(bronze_shipments, customers, routes):
    customer_ids = customers.select("customer_id")
    route_ids = routes.select("route_id")
    return (
        bronze_shipments.join(customer_ids, "customer_id", "left_anti")
        .unionByName(bronze_shipments.join(route_ids, "route_id", "left_anti"))
        .withColumn("_quarantine_reason", F.lit("referential validation failed"))
    )


def silver_service_cases(bronze_cases, shipments):
    return (
        bronze_cases.withColumn("opened_at_utc", F.to_timestamp("opened_at"))
        .join(shipments.select("shipment_id"), "shipment_id", "left_semi")
        .filter(F.col("contact_email").rlike(r"^[^@\s]+@synthetic\.contoso\.example$"))
        .dropDuplicates(["case_id"])
    )
