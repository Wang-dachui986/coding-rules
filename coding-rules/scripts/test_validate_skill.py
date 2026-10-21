# /// script
# requires-python = ">=3.11"
# dependencies = ["pytest>=8,<10"]
# ///
# ─── How to run ───
# uv run scripts/test_validate_skill.py
# python -m pytest -q scripts/test_validate_skill.py

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
    (root / "references/operating-model.md").write_text("# Operating\n", encoding="utf-8")
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
    assert "R1 contains R0-only heading" in result.stderr


def test_validator_requires_operating_model(tmp_path: Path) -> None:
    # Given: a fixture that omits the operating model SKILL.md tells Codex to read.
    _write_valid_fixture(tmp_path)
    (tmp_path / "references" / "operating-model.md").unlink()

    # When: the validator checks it.
    result = _run_validator(tmp_path)

    # Then: the missing reference is rejected even without a Markdown link to it.
    assert result.returncode == 1
    assert "missing: references/operating-model.md" in result.stderr


def test_validator_reports_invalid_utf8(tmp_path: Path) -> None:
    # Given: a required Markdown file that is not UTF-8.
    _write_valid_fixture(tmp_path)
    (tmp_path / "references" / "intake-model.md").write_bytes(b"\xff\xfe not utf-8")

    # When: the validator checks it.
    result = _run_validator(tmp_path)

    # Then: the encoding error is reported instead of raising.
    assert result.returncode == 1
    assert "not valid UTF-8: references/intake-model.md" in result.stderr


def test_shipped_skill_passes() -> None:
    # Given: the skill directory shipped in this repository.
    skill_root = Path(__file__).resolve().parent.parent

    # When: the validator checks that directory.
    result = _run_validator(skill_root)

    # Then: the published skill is accepted.
    assert result.returncode == 0, result.stderr


if __name__ == "__main__":
    import pytest

    raise SystemExit(pytest.main([__file__, "-q"]))
