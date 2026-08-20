from __future__ import annotations


def landing_path(storage_account: str, source: str) -> str:
    return f"abfss://landing@{storage_account}.dfs.core.windows.net/{source}/"


def checkpoint_path(storage_account: str, environment: str, source: str) -> str:
    return f"abfss://checkpoints@{storage_account}.dfs.core.windows.net/{environment}/{source}/"


def schema_path(storage_account: str, environment: str, source: str) -> str:
    return f"abfss://checkpoints@{storage_account}.dfs.core.windows.net/{environment}/schemas/{source}/"

