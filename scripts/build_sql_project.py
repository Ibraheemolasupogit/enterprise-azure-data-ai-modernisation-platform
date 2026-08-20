from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / "src/azure_sql/database_project/legacy_tms/legacy_tms.sqlproj"


def main() -> int:
    dotnet = shutil.which("dotnet")
    if dotnet is None:
        print("Cannot build SQL project: dotnet is not installed or not on PATH.")
        print("Install the .NET SDK and run `make build-sql-project` again.")
        return 2
    sdk_version_text = _selected_sdk_version(dotnet)
    print(f"dotnet selected SDK version: {sdk_version_text or 'unknown'}")
    sdk_version = _parse_sdk_version(sdk_version_text)
    if sdk_version is None or sdk_version[0] != 8:
        print("Cannot build SQL project: this repository requires .NET SDK 8.x.")
        print("global.json pins SDK selection to 8.0 with latestFeature roll-forward.")
        print("Install a current .NET 8 SDK and run `make build-sql-project` again.")
        return 2
    if not PROJECT.is_file():
        print(f"Cannot build SQL project: missing {PROJECT.relative_to(ROOT)}")
        return 1
    result = subprocess.run(
        [dotnet, "build", str(PROJECT), "--nologo"],
        cwd=ROOT,
        check=False,
    )
    return result.returncode


def _selected_sdk_version(dotnet: str) -> str | None:
    result = subprocess.run(
        [dotnet, "--version"],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return None
    return result.stdout.strip()


def _parse_sdk_version(raw_version: str | None) -> tuple[int, int] | None:
    if raw_version is None:
        return None
    parts = raw_version.split(".")
    if len(parts) >= 2 and parts[0].isdigit() and parts[1].isdigit():
        return (int(parts[0]), int(parts[1]))
    return None


if __name__ == "__main__":
    raise SystemExit(main())
