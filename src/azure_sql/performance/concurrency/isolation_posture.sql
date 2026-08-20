-- Target posture recommendation:
-- Keep READ COMMITTED as the compatibility baseline for migration.
-- Evaluate READ_COMMITTED_SNAPSHOT after workload testing if reader/writer blocking is material.
-- SNAPSHOT may help specific workflows but introduces version-store and write-conflict trade-offs.
-- SERIALIZABLE should remain limited to workflows requiring strict range protection.
-- Optimized locking applicability requires SQL MI/Azure SQL feature validation.

SELECT
    name,
    snapshot_isolation_state_desc,
    is_read_committed_snapshot_on
FROM sys.databases
WHERE name = DB_NAME();

