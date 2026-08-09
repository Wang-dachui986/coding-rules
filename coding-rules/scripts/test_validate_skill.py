# /// script
# requires-python = ">=3.11"
# dependencies = ["pytest>=8,<9"]
# ///
# ─── How to run ───
# uv run --with pytest pytest -q scripts/test_validate_skill.py

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def _run_validator(skill_root: Path) -> subprocess.CompletedProcess[str]:
    validator = Path(__file__).with_name("validate_skill.py")
    return subprocess.run(
        [sys.executable, str(validator), str(skill_root)],
        check=False,
        capture_output=True,
        text=True,
    )


def _write_valid_fixture(root: Path) -> None:
    (root / "agents").mkdir(parents=True)
    (root / "references").mkdir()
    handoffs = root / "assets/project-governance/docs/handoffs"
    governance = root / "assets/project-governance/docs/governance"
    handoffs.mkdir(parents=True)
    governance.mkdir(parents=True)
    (root / "SKILL.md").write_text(
        "---\nname: coding-rules\ndescription: governance\n---\n"
        "[intake](references/intake-model.md)\n",
        encoding="utf-8",
    )
    (root / "agents/openai.yaml").write_text("interface:\n  display_name: coding-Rules\n", encoding="utf-8")
    (root / "references/intake-model.md").write_text("# Intake\n", encoding="utf-8")
    for role in ("R0", "R1", "R2", "R3", "PROJECT"):
        (handoffs / f"{role}.md").write_text(f"# {role}\n", encoding="utf-8")
    for name in (
        "CURRENT-TASKS",
        "HANDOFF-PROTOCOL",
        "OPERATING-RULES",
        "TASK-CARD-TEMPLATE",
        "WORKSTREAMS",
    ):
        (governance / f"{name}.md").write_text(f"# {name}\n", encoding="utf-8")
    (root / "assets/project-governance/AGENTS.md").write_text("# Rules\n", encoding="utf-8")


def test_validator_accepts_complete_structure(tmp_path: Path) -> None:
    # Given: a structurally complete skill fixture.
    _write_valid_fixture(tmp_path)

    # When: the validator checks it.
    result = _run_validator(tmp_path)

    # Then: the structure is accepted.
    assert result.returncode == 0, result.stderr


def test_validator_rejects_execution_role_authority(tmp_path: Path) -> None:
    # Given: an execution-role handoff containing an R0-only heading.
    _write_valid_fixture(tmp_path)
    handoff = tmp_path / "assets/project-governance/docs/handoffs/R1.md"
    handoff.write_text("# R1\n## 项目总进度\n", encoding="utf-8")

    # When: the validator checks it.
    result = _run_validator(tmp_path)

    # Then: the authority violation is rejected.
    assert result.returncode == 1
