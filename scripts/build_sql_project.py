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
    sdk_version = _highest_sdk_version(dotnet)
    if sdk_version is None or sdk_version < (8, 0):
        version_text = ".".join(str(part) for part in sdk_version) if sdk_version else "unknown"
        print("Cannot build SQL project: .NET SDK 8.0 or newer is required.")
        print(f"Detected highest .NET SDK version: {version_text}")
        print("Install a current .NET SDK and run `make build-sql-project` again.")
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


def _highest_sdk_version(dotnet: str) -> tuple[int, int] | None:
    result = subprocess.run(
        [dotnet, "--list-sdks"],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    versions: list[tuple[int, int]] = []
    for line in result.stdout.splitlines():
        raw_version = line.split()[0]
        parts = raw_version.split(".")
        if len(parts) >= 2 and parts[0].isdigit() and parts[1].isdigit():
            versions.append((int(parts[0]), int(parts[1])))
    return max(versions) if versions else None


if __name__ == "__main__":
    raise SystemExit(main())
