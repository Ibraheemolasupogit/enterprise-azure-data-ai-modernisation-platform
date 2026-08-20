from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT / "src/azure_sql/database_project/legacy_tms"


def main() -> int:
    required_terms = {
        "legacy_tms.sqlproj": "Microsoft.Build.Sql",
        "PostDeployment/ReferenceData.sql": "MERGE dbo.Depot",
        "Security/RolesAndPermissions.sql": "CREATE ROLE app_legacy_tms_writer",
        "Tests/static_schema_tests.sql": "dbo.Shipment",
    }
    failures: list[str] = []
    for relative_path, expected in required_terms.items():
        path = PROJECT_ROOT / relative_path
        if not path.is_file():
            failures.append(f"missing SQL project asset: {relative_path}")
            continue
        if expected not in path.read_text(encoding="utf-8"):
            failures.append(f"{relative_path} missing expected content: {expected}")
    if failures:
        print("SQL project static tests failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("SQL project static tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

