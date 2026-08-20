from __future__ import annotations

import hashlib
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GENERATORS = [
    [
        "python3",
        "-m",
        "target_architecture.cli",
        "--outputs-dir",
        "outputs/architecture",
        "--reports-dir",
        "reports",
    ],
    [
        "python3",
        "-m",
        "sql_cicd.cli",
        "--outputs-dir",
        "outputs/sql_cicd",
        "--reports-dir",
        "reports",
    ],
    ["python3", "-m", "sql_ai.cli", "--outputs-dir", "outputs/sql_ai", "--reports-dir", "reports"],
    [
        "python3",
        "-m",
        "application_integration.cli",
        "--outputs-dir",
        "outputs/application_integration",
        "--reports-dir",
        "reports",
    ],
    [
        "python3",
        "-m",
        "fabric_integration.cli",
        "--outputs-dir",
        "outputs/fabric_integration",
        "--reports-dir",
        "reports",
    ],
    [
        "python3",
        "-m",
        "final_assurance.cli",
        "--outputs-dir",
        "outputs/final_assurance",
        "--reports-dir",
        "reports",
    ],
]
TRACKED_DIRS = [
    ROOT / "outputs" / "architecture",
    ROOT / "outputs" / "sql_cicd",
    ROOT / "outputs" / "sql_ai",
    ROOT / "outputs" / "application_integration",
    ROOT / "outputs" / "fabric_integration",
    ROOT / "outputs" / "final_assurance",
    ROOT / "reports",
]


def hash_files() -> dict[str, str]:
    hashes: dict[str, str] = {}
    for directory in TRACKED_DIRS:
        if not directory.is_dir():
            continue
        for path in sorted(directory.rglob("*")):
            if path.is_file():
                hashes[str(path.relative_to(ROOT))] = hashlib.sha256(path.read_bytes()).hexdigest()
    return hashes


def main() -> int:
    before = hash_files()
    for command in GENERATORS:
        result = subprocess.run(command, cwd=ROOT, check=False)
        if result.returncode != 0:
            print(f"Generated-output check failed while running: {' '.join(command)}")
            return result.returncode
    after = hash_files()
    if before != after:
        changed_hashes = {key for key in before if before.get(key) != after.get(key)}
        changed = sorted(set(before) ^ set(after) | changed_hashes)
        print("Generated-output check failed; regenerated evidence differs:")
        for path in changed:
            print(f"- {path}")
        return 1
    print("Generated-output assurance passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
