# Microsoft Fabric Downstream Integration Boundary Report

Milestone 15 defines only the downstream integration contract between this Azure Data & AI platform and Microsoft Fabric. It does not create Fabric workspaces, Lakehouses, Warehouses, semantic models, Power BI assets, Fabric pipelines, notebooks, Real-Time Intelligence assets, or Fabric deployment pipelines.

The recommended boundary is Azure Databricks governed Gold Delta products published through an ADLS/Delta boundary, then consumed by Fabric through OneLake shortcuts or a supported interoperability pattern where runtime validation confirms suitability. Controlled batch copy is retained as an exception for finance snapshot or retention requirements.

Azure owns operational sources, Azure SQL, Databricks ingestion and Gold production, data quality, lineage to Gold, contracts, and publication readiness. Fabric owns downstream ingestion/shortcut choices, OneLake/Lakehouse/Warehouse implementation, semantic models, Power BI, Fabric-side RLS/OLS, monitoring, governance, CI/CD, and adoption.
