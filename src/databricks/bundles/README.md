# Databricks Bundle Workspace

This directory is intentionally tracked so the repository keeps a stable location for
Databricks Asset Bundle-adjacent assets.

The root `databricks.yml` remains the bundle entrypoint for this platform. Milestone assets
currently define bundle resources and targets from the root file and supporting source
directories under `src/databricks/`. This directory is reserved for future bundle-local
configuration fragments or environment-specific bundle support files if the bundle grows beyond
the root layout.

No fake jobs, resources, or deployment artifacts are stored here.

