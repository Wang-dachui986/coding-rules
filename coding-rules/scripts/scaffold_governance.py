# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
# ─── How to run ───
# uv run scripts/scaffold_governance.py <project-root> [--dry-run]

"""Copy missing coding-rules governance templates into a project.

The command creates files that are not already there. It does not delete,
move, rename, or overwrite, and it does not fill placeholders or merge text
into an existing file. Semantic merge stays with ``$coding-rules``.

``mode: empty`` means the skill's emptiness rule: version-control metadata,
editor metadata, OS metadata, caches, and the governance templates themselves
do not count as meaningful project files. A directory that only holds those
templates is still ``empty``. The mode does not change the write rule.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

IGNORED_DIR_NAMES = {
    ".git",
    ".hg",
    ".svn",
    ".idea",
    ".vscode",
    ".cursor",
    "__pycache__",
    ".pytest_cache",
    "node_modules",
    "dist",
    "build",
    ".next",
    "coverage",
    ".venv",
    "venv",
}
IGNORED_FILE_NAMES = {".DS_Store"}
USAGE = "usage: scaffold_governance.py <project-root> [--dry-run]"


def _skill_root() -> Path:
    return Path(__file__).resolve().parent.parent


def _governance_root() -> Path:
    return _skill_root() / "assets" / "project-governance"


def _ignored_file(path: Path) -> bool:
    return path.name.startswith("._") or path.name in IGNORED_FILE_NAMES or path.suffix == ".pyc"


def template_files(governance_root: Path) -> list[Path]:
    files: list[Path] = []
    for path in sorted(governance_root.rglob("*")):
        if path.is_file() and not _ignored_file(path):
            files.append(path)
    return files


def _meaningful_files(root: Path, governance_paths: set[str]) -> list[Path]:
    found: list[Path] = []
    if not root.is_dir():
        return found
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [name for name in dirnames if name not in IGNORED_DIR_NAMES and not name.startswith("._")]
        for name in filenames:
            path = Path(dirpath) / name
            if _ignored_file(path):
                continue
            relative = path.relative_to(root).as_posix()
            if relative in governance_paths:
                continue
            found.append(path)
    return found


def _refuse_skill_target(target: Path) -> str | None:
    if target == Path(target.anchor):
        return "scaffold: target is the filesystem root"
    skill_root = _skill_root()
    if target == skill_root or skill_root in target.parents:
        return "scaffold: target is inside the skill directory"
    return None


def plan(target: Path, governance_root: Path) -> tuple[str, list[str], list[str]]:
    templates = template_files(governance_root)
    relative_paths = [path.relative_to(governance_root).as_posix() for path in templates]
    if target.is_dir():
        mode = "empty" if not _meaningful_files(target, set(relative_paths)) else "existing"
    else:
        mode = "empty"
    created: list[str] = []
    skipped: list[str] = []
    for relative in relative_paths:
        destination = target / relative
        if destination.exists() or destination.is_symlink():
            skipped.append(relative)
        else:
            created.append(relative)
    return mode, created, skipped


def _render(mode: str, dry_run: bool, created: list[str], skipped: list[str]) -> str:
    verb = "would-create" if dry_run else "created"
    lines = [f"mode: {mode}", f"dry-run: {'yes' if dry_run else 'no'}"]
    lines.extend(f"{verb}: {relative}" for relative in created)
    lines.extend(f"skipped-existing: {relative}" for relative in skipped)
    return "\n".join(lines) + "\n"


def apply_scaffold(target: Path, *, dry_run: bool) -> tuple[int, str]:
    refusal = _refuse_skill_target(target)
    if refusal is not None:
        return 2, refusal + "\n"
    governance_root = _governance_root()
    if not governance_root.is_dir() or not template_files(governance_root):
        return 2, "scaffold: governance templates are missing\n"
    if target.exists() and not target.is_dir():
        return 2, f"scaffold: target is not a directory: {target}\n"
    mode, created, skipped = plan(target, governance_root)
    if not dry_run:
        target.mkdir(parents=True, exist_ok=True)
        for relative in created:
            source = governance_root / relative
            destination = target / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            try:
                fd = os.open(destination, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o644)
            except FileExistsError:
                skipped.append(relative)
                continue
            with os.fdopen(fd, "wb") as handle:
                handle.write(source.read_bytes())
        created = [relative for relative in created if relative not in skipped]
    return 0, _render(mode, dry_run, created, skipped)


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    dry_run = False
    targets: list[str] = []
    for arg in args:
        if arg == "--dry-run":
            dry_run = True
        elif arg.startswith("-"):
            print(USAGE, file=sys.stderr)
            return 2
        else:
            targets.append(arg)
    if len(targets) != 1:
        print(USAGE, file=sys.stderr)
        return 2
    target = Path(targets[0]).expanduser().resolve()
    code, output = apply_scaffold(target, dry_run=dry_run)
    stream = sys.stdout if code == 0 else sys.stderr
    stream.write(output)
    return code


if __name__ == "__main__":
    raise SystemExit(main())
