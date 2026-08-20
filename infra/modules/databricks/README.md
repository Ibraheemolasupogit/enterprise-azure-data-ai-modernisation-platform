# Databricks Foundation Module

This module declares the Azure resources required for the Databricks platform foundation: workspace, ADLS Gen2 storage, containers, access connector managed identity, and Log Analytics diagnostics. It is switch-gated from `infra/main.bicep` and is not deployed by local validation.

The module intentionally contains no storage keys, SAS tokens, workspace tokens, or production connection details. Unity Catalog storage credentials and external locations are represented in SQL assets and require real Azure Databricks account/workspace validation.

