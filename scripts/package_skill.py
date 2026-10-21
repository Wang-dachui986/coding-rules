#!/usr/bin/env python3
"""Zip the installable coding-rules skill for a GitHub Release.

The archive contains LICENSE and the coding-rules/ directory. SKILL.md is
inside that directory, which is the folder Codex loads as a skill.
"""

from __future__ import annotations

import re
import sys
import zipfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILL_DIR = REPO_ROOT / "coding-rules"
SKIP_DIR_NAMES = {"__pycache__", ".pytest_cache"}
SKIP_FILE_NAMES = {".DS_Store"}
VERSION_PATTERN = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*")
REQUIRED_NAMES = (
    "LICENSE",
    "coding-rules/SKILL.md",
    "coding-rules/agents/openai.yaml",
    "coding-rules/references/operating-model.md",
    "coding-rules/scripts/validate_skill.py",
    "coding-rules/scripts/scaffold_governance.py",
    "coding-rules/scripts/report_status.py",
    "coding-rules/assets/project-governance/docs/governance/CHECKLISTS.md",
)


def _should_skip(path: Path) -> bool:
    if path.name.startswith("._") or path.name in SKIP_FILE_NAMES:
        return True
    if path.suffix == ".pyc":
        return True
    return bool(SKIP_DIR_NAMES.intersection(path.parts))


def package(version: str) -> Path:
    if VERSION_PATTERN.fullmatch(version) is None:
        raise SystemExit(f"unsupported version: {version!r}")
    if not (REPO_ROOT / "LICENSE").is_file():
        raise SystemExit("missing LICENSE")
    if not SKILL_DIR.is_dir():
        raise SystemExit("missing coding-rules skill directory")

    dest = REPO_ROOT / "dist" / f"coding-rules-{version}.zip"
    dest.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(dest, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.write(REPO_ROOT / "LICENSE", "LICENSE")
        for path in sorted(SKILL_DIR.rglob("*")):
            if not path.is_file() or _should_skip(path):
                continue
            archive.write(path, path.relative_to(REPO_ROOT).as_posix())
        names = set(archive.namelist())

    missing = [name for name in REQUIRED_NAMES if name not in names]
    if missing:
        raise SystemExit(f"package missing {missing}")
    leaked = [name for name in names if name.endswith(".pyc") or "/__pycache__/" in f"/{name}"]
    if leaked:
        raise SystemExit(f"package contains generated files: {leaked}")
    return dest


def main() -> int:
    version = sys.argv[1] if len(sys.argv) == 2 else "dev"
    print(package(version))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
