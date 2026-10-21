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
    (root / "scripts").mkdir()
    handoffs = root / "assets/project-governance/docs/handoffs"
    governance = root / "assets/project-governance/docs/governance"
    handoffs.mkdir(parents=True)
    governance.mkdir(parents=True)
    (root / "SKILL.md").write_text(
        "---\nname: coding-rules\ndescription: governance\n---\n"
        "[intake](references/intake-model.md)\n"
        "scaffold_governance.py report_status.py CHECKLISTS.md\n",
        encoding="utf-8",
    )
    (root / "agents/openai.yaml").write_text("interface:\n  display_name: coding-Rules\n", encoding="utf-8")
    (root / "references/intake-model.md").write_text("# Intake\n", encoding="utf-8")
    (root / "references/operating-model.md").write_text("# Operating\n", encoding="utf-8")
    (root / "scripts/scaffold_governance.py").write_text("# stub\n", encoding="utf-8")
    (root / "scripts/report_status.py").write_text("# stub\n", encoding="utf-8")
    for role in ("R0", "R1", "R2", "R3", "PROJECT"):
        (handoffs / f"{role}.md").write_text(f"# {role}\n", encoding="utf-8")
    for name in (
        "CURRENT-TASKS",
        "HANDOFF-PROTOCOL",
        "OPERATING-RULES",
        "WORKSTREAMS",
    ):
        (governance / f"{name}.md").write_text(f"# {name}\n", encoding="utf-8")
    (governance / "CHECKLISTS.md").write_text(
        "# 检查清单\n## 1. R0 轻量接收\n## 2. 模块系统性验收\n## 3. 发布检查\n",
        encoding="utf-8",
    )
    (governance / "TASK-CARD-TEMPLATE.md").write_text(
        "# 任务卡\n## 目标与完成定义\n## 禁止事项\n## 验证与验收\n"
        "- 证据状态：`NOT_RUN`\n## 交接\n## 返回 R0\n",
        encoding="utf-8",
    )
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


def test_validator_requires_checklist_heading(tmp_path: Path) -> None:
    # Given: a checklist that drops the release section.
    _write_valid_fixture(tmp_path)
    checklist = tmp_path / "assets/project-governance/docs/governance/CHECKLISTS.md"
    checklist.write_text("# 检查清单\n## 1. R0 轻量接收\n## 2. 模块系统性验收\n", encoding="utf-8")

    # When: the validator checks it.
    result = _run_validator(tmp_path)

    # Then: the missing gate is rejected.
    assert result.returncode == 1
    assert "CHECKLISTS.md missing heading: ## 3. 发布检查" in result.stderr


def test_validator_requires_task_card_evidence(tmp_path: Path) -> None:
    # Given: a task-card template without an evidence status.
    _write_valid_fixture(tmp_path)
    template = tmp_path / "assets/project-governance/docs/governance/TASK-CARD-TEMPLATE.md"
    template.write_text(
        "# 任务卡\n## 目标与完成定义\n## 禁止事项\n## 验证与验收\n## 交接\n## 返回 R0\n",
        encoding="utf-8",
    )

    # When: the validator checks it.
    result = _run_validator(tmp_path)

    # Then: the evidence field is required.
    assert result.returncode == 1
    assert "TASK-CARD-TEMPLATE.md missing 证据状态" in result.stderr


def test_validator_requires_skill_command_mentions(tmp_path: Path) -> None:
    # Given: SKILL.md that no longer names the scaffold command.
    _write_valid_fixture(tmp_path)
    (tmp_path / "SKILL.md").write_text(
        "---\nname: coding-rules\ndescription: governance\n---\n"
        "[intake](references/intake-model.md)\n"
        "report_status.py CHECKLISTS.md\n",
        encoding="utf-8",
    )

    # When: the validator checks it.
    result = _run_validator(tmp_path)

    # Then: the missing command mention is rejected.
    assert result.returncode == 1
    assert "SKILL.md does not mention scaffold_governance.py" in result.stderr


def test_validator_requires_governance_commands(tmp_path: Path) -> None:
    # Given: a skill tree that drops the status report command.
    _write_valid_fixture(tmp_path)
    (tmp_path / "scripts/report_status.py").unlink()

    # When: the validator checks it.
    result = _run_validator(tmp_path)

    # Then: the command file is required.
    assert result.returncode == 1
    assert "missing: scripts/report_status.py" in result.stderr


def _run_script(name: str, *args: object) -> subprocess.CompletedProcess[str]:
    script = Path(__file__).with_name(name)
    return subprocess.run(
        [sys.executable, str(script), *[str(arg) for arg in args]],
        check=False,
        capture_output=True,
        text=True,
    )


def _task_card(task_id: str, status: str, evidence: str, owner: str = "R1") -> str:
    return (
        f"# 任务卡：`{task_id}`\n"
        f"- 负责人：`{owner}`\n"
        f"- 状态：`{status}`\n"
        "- 预检结论：`READY_FOR_OWNER_APPROVAL`\n"
        f"- 证据状态：`{evidence}`\n"
    )


def test_scaffold_creates_missing_templates_and_does_not_overwrite(tmp_path: Path) -> None:
    # Given: an empty directory that only has ignored metadata, then a second run.
    project = tmp_path / "empty-app"
    project.mkdir()
    (project / ".git").mkdir()
    (project / ".git" / "config").write_text("ignored\n", encoding="utf-8")
    (project / ".DS_Store").write_text("ignored\n", encoding="utf-8")
    skill_checklist = (
        Path(__file__).resolve().parent.parent
        / "assets/project-governance/docs/governance/CHECKLISTS.md"
    )

    # When: the scaffold copies templates, then runs again.
    first = _run_script("scaffold_governance.py", project)
    checklist_bytes = (project / "docs/governance/CHECKLISTS.md").read_bytes()
    second = _run_script("scaffold_governance.py", project)

    # Then: the first run creates the checklist unchanged, and the second run writes nothing.
    assert first.returncode == 0, first.stderr
    assert "mode: empty" in first.stdout
    assert "dry-run: no" in first.stdout
    assert "created: docs/governance/CHECKLISTS.md" in first.stdout
    assert checklist_bytes == skill_checklist.read_bytes()
    assert second.returncode == 0, second.stderr
    assert "mode: empty" in second.stdout
    assert "skipped-existing: AGENTS.md" in second.stdout
    assert "created:" not in second.stdout
    assert (project / "docs/governance/CHECKLISTS.md").read_bytes() == checklist_bytes


def test_scaffold_skips_existing_project_files(tmp_path: Path) -> None:
    # Given: a project that already has product text and its own AGENTS.md.
    project = tmp_path / "existing-app"
    project.mkdir()
    (project / "README.md").write_text("product\n", encoding="utf-8")
    (project / "AGENTS.md").write_text("# keep project rules\n", encoding="utf-8")

    # When: the scaffold runs.
    result = _run_script("scaffold_governance.py", project)

    # Then: product rules stay, and only missing governance files are created.
    assert result.returncode == 0, result.stderr
    assert "mode: existing" in result.stdout
    assert "skipped-existing: AGENTS.md" in result.stdout
    assert "created: docs/governance/CHECKLISTS.md" in result.stdout
    assert (project / "AGENTS.md").read_text(encoding="utf-8") == "# keep project rules\n"
    assert (project / "docs/governance/CHECKLISTS.md").is_file()


def test_scaffold_preserves_a_lone_agents_file(tmp_path: Path) -> None:
    # Given: a directory whose only meaningful-looking file is governance, which the skill ignores.
    project = tmp_path / "rules-only"
    project.mkdir()
    (project / "AGENTS.md").write_text("# custom\n", encoding="utf-8")

    # When: the scaffold classifies and copies.
    result = _run_script("scaffold_governance.py", project)

    # Then: the mode is empty and the existing file is still not overwritten.
    assert result.returncode == 0, result.stderr
    assert "mode: empty" in result.stdout
    assert "skipped-existing: AGENTS.md" in result.stdout
    assert (project / "AGENTS.md").read_text(encoding="utf-8") == "# custom\n"


def test_scaffold_dry_run_writes_nothing(tmp_path: Path) -> None:
    # Given: a project path that does not exist yet.
    target = tmp_path / "fresh"

    # When: the scaffold is asked to print only.
    result = _run_script("scaffold_governance.py", "--dry-run", target)

    # Then: the directory is absent and the output names the files it would create.
    assert result.returncode == 0, result.stderr
    assert not target.exists()
    assert "dry-run: yes" in result.stdout
    assert "would-create: AGENTS.md" in result.stdout
    assert "created:" not in result.stdout


def test_scaffold_refuses_the_skill_directory() -> None:
    # Given: the skill directory that contains the templates.
    skill_root = Path(__file__).resolve().parent.parent

    # When: the scaffold is pointed at that directory.
    result = _run_script("scaffold_governance.py", skill_root)

    # Then: it refuses and does not write a project AGENTS.md into the skill.
    assert result.returncode == 2
    assert "skill directory" in result.stderr
    assert not (skill_root / "AGENTS.md").exists()


def test_scaffold_refuses_filesystem_root() -> None:
    # Given: the filesystem root.
    # When: the scaffold is pointed at it, including a dry run.
    result = _run_script("scaffold_governance.py", "--dry-run", "/")

    # Then: it refuses before listing or writing project files.
    assert result.returncode == 2
    assert "filesystem root" in result.stderr
    assert "would-create:" not in result.stdout


def test_scaffold_rejects_a_file_target(tmp_path: Path) -> None:
    # Given: a path that is a file.
    target = tmp_path / "notes.txt"
    target.write_text("x\n", encoding="utf-8")

    # When: the scaffold is pointed at that file.
    result = _run_script("scaffold_governance.py", target)

    # Then: it refuses.
    assert result.returncode == 2
    assert "not a directory" in result.stderr
    assert target.read_text(encoding="utf-8") == "x\n"


def test_scaffold_writes_every_template_the_validator_requires(tmp_path: Path) -> None:
    # Given: the template paths the validator requires.
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from validate_skill import REQUIRED_PATHS

    project = tmp_path / "covered"
    prefix = "assets/project-governance/"

    # When: the scaffold creates a project.
    result = _run_script("scaffold_governance.py", project)

    # Then: every governance template required by the validator is present.
    assert result.returncode == 0, result.stderr
    required = [path.removeprefix(prefix) for path in REQUIRED_PATHS if path.startswith(prefix)]
    assert required
    for relative in required:
        assert (project / relative).is_file(), relative
        assert f"created: {relative}" in result.stdout


def test_scaffold_ignores_dependency_metadata(tmp_path: Path) -> None:
    # Given: a directory that only contains a dependency cache.
    project = tmp_path / "cached"
    module = project / "node_modules"
    module.mkdir(parents=True)
    (module / "left-pad.js").write_text("x\n", encoding="utf-8")

    # When: the scaffold classifies it.
    result = _run_script("scaffold_governance.py", project)

    # Then: the cache does not make the project look existing.
    assert result.returncode == 0, result.stderr
    assert "mode: empty" in result.stdout


def test_report_counts_pass_only_and_keeps_not_run_unaccepted(tmp_path: Path) -> None:
    # Given: one accepted card, one completed card whose evidence was not run, and one module input.
    tasks = tmp_path / "docs/governance/tasks"
    tasks.mkdir(parents=True)
    (tasks / "done.md").write_text(
        _task_card("TASK-DONE", "COMPLETED_ACCEPTED", "PASS"),
        encoding="utf-8",
    )
    (tasks / "gap.md").write_text(
        _task_card("TASK-GAP", "COMPLETED_ACCEPTED", "NOT_RUN"),
        encoding="utf-8",
    )
    (tasks / "ready.md").write_text(
        _task_card("TASK-READY", "COMPLETED_MODULE_INPUT_READY", "PASS"),
        encoding="utf-8",
    )

    # When: the report is generated.
    result = _run_script("report_status.py", tmp_path)

    # Then: only the PASS card is accepted, and NOT_RUN stays visible as NOT_RUN.
    assert result.returncode == 0, result.stderr
    assert "- 任务卡：`3`" in result.stdout
    assert "- 数量：`1`" in result.stdout
    assert "`TASK-GAP`：任务状态 `COMPLETED_ACCEPTED`，证据状态 `NOT_RUN`" in result.stdout
    assert "| 任务 ID | 来源 | 负责人 | 任务状态 | 预检结论 | 证据状态 |" in result.stdout
    assert "`NOT_RUN`" in result.stdout
    assert "TASK-GAP" in result.stdout
    gap_line = next(line for line in result.stdout.splitlines() if "TASK-GAP" in line and line.startswith("|"))
    assert "`NOT_RUN`" in gap_line
    assert "`PASS`" not in gap_line


def test_report_rejects_accepted_status_without_evidence(tmp_path: Path) -> None:
    # Given: a card marked accepted with no evidence field.
    tasks = tmp_path / "docs/governance/tasks"
    tasks.mkdir(parents=True)
    (tasks / "bare.md").write_text(
        "# 任务卡：`TASK-BARE`\n- 负责人：`R2`\n- 状态：`COMPLETED_ACCEPTED`\n",
        encoding="utf-8",
    )

    # When: the report is generated.
    result = _run_script("report_status.py", tmp_path)

    # Then: missing evidence is UNSET and the card is not accepted.
    assert result.returncode == 0, result.stderr
    assert "- 数量：`0`" in result.stdout
    assert "证据状态 `UNSET`" in result.stdout


def test_report_treats_unfilled_evidence_menu_as_unset(tmp_path: Path) -> None:
    # Given: a card whose evidence field is still the slash-separated menu.
    tasks = tmp_path / "docs/governance/tasks"
    tasks.mkdir(parents=True)
    (tasks / "menu.md").write_text(
        _task_card("TASK-MENU", "COMPLETED_ACCEPTED", "PASS / FAILED / NOT_RUN / LIMITED"),
        encoding="utf-8",
    )

    # When: the report is generated.
    result = _run_script("report_status.py", tmp_path)

    # Then: the menu is not treated as PASS.
    assert result.returncode == 0, result.stderr
    assert "- 数量：`0`" in result.stdout
    assert "证据状态 `UNSET`" in result.stdout


def test_report_does_not_double_count_a_table_path(tmp_path: Path) -> None:
    # Given: one card that is also named in CURRENT-TASKS.md, plus a placeholder row.
    tasks = tmp_path / "docs/governance/tasks"
    tasks.mkdir(parents=True)
    (tasks / "one.md").write_text(
        _task_card("TASK-1", "IN_PROGRESS", "NOT_RUN", owner="R3"),
        encoding="utf-8",
    )
    governance = tmp_path / "docs/governance"
    (governance / "CURRENT-TASKS.md").write_text(
        "# 当前任务分配\n"
        "- 问答模式：`LIGHT`\n"
        "- 需求覆盖率：`40%`\n"
        "- 计划状态：`WAITING_REVIEW`\n"
        "\n## 当前唯一权威任务\n\n"
        "| 任务 ID | 负责人 | 状态 | 批准范围 | 任务卡 | 证据 |\n"
        "|---|---|---|---|---|---|\n"
        "| `TASK-1` | `R3` | `IN_PROGRESS` | `src/` | `docs/governance/tasks/one.md` | `NOT_RUN` |\n"
        "| `[待确认]` | `R0` | `WAITING_APPROVAL` | `[待确认]` | `[路径]` | `NOT_RUN` |\n"
        "\n## 下一步与审批状态\n\n"
        "1. 审阅计划：`WAITING_APPROVAL`\n",
        encoding="utf-8",
    )

    # When: the report is generated.
    result = _run_script("report_status.py", tmp_path)

    # Then: the card appears once, the placeholder is separate, and the plan fields are echoed.
    assert result.returncode == 0, result.stderr
    assert "- 任务卡：`1`" in result.stdout
    assert "- 占位行：`1`" in result.stdout
    assert "- 数量：`0`" in result.stdout
    assert result.stdout.count("| `TASK-1` |") == 1
    assert "- 问答模式：`LIGHT`" in result.stdout
    assert "- 需求覆盖率：`40%`" in result.stdout
    assert "- 计划状态：`WAITING_REVIEW`" in result.stdout
    assert "审阅计划：`WAITING_APPROVAL`" in result.stdout
    status_section = result.stdout.split("## 已验收", 1)[0]
    assert "`WAITING_APPROVAL`" not in status_section


def test_report_reads_a_renamed_tasks_directory(tmp_path: Path) -> None:
    # Given: cards stored outside the default directory.
    cards = tmp_path / "cards"
    cards.mkdir()
    (cards / "lib.md").write_text(_task_card("TASK-LIB", "APPROVED", "NOT_RUN"), encoding="utf-8")

    # When: the report is pointed at that directory.
    result = _run_script("report_status.py", tmp_path, "--tasks-dir", "cards")

    # Then: the card is included.
    assert result.returncode == 0, result.stderr
    assert "`TASK-LIB`" in result.stdout
    assert "`cards/lib.md`" in result.stdout


def test_report_lists_duplicate_ids_and_unparsed_files(tmp_path: Path) -> None:
    # Given: two cards with one id, and a markdown file that is not a task card.
    tasks = tmp_path / "docs/governance/tasks"
    tasks.mkdir(parents=True)
    (tasks / "a.md").write_text(_task_card("TASK-DUP", "PLANNED", "NOT_RUN"), encoding="utf-8")
    (tasks / "b.md").write_text(_task_card("TASK-DUP", "PLANNED", "NOT_RUN", owner="R2"), encoding="utf-8")
    (tasks / "notes.md").write_text("# notes\n", encoding="utf-8")

    # When: the report is generated.
    result = _run_script("report_status.py", tmp_path)

    # Then: the duplicate and the unparsed file are both named.
    assert result.returncode == 0, result.stderr
    assert "- 任务卡：`2`" in result.stdout
    duplicate_at = result.stdout.index("## 重复任务 ID")
    unparsed_at = result.stdout.index("## 未解析文件")
    assert "`TASK-DUP`" in result.stdout[duplicate_at:unparsed_at]
    assert "`docs/governance/tasks/notes.md`" in result.stdout[unparsed_at:]


def test_report_requires_a_status_source(tmp_path: Path) -> None:
    # Given: a project with no current-task file and no task cards.
    project = tmp_path / "blank"
    project.mkdir()

    # When: the report runs.
    result = _run_script("report_status.py", project)

    # Then: it fails instead of inventing a status.
    assert result.returncode == 1
    assert "no CURRENT-TASKS.md and no task cards" in result.stderr


def test_scaffold_report_on_a_fresh_project_keeps_the_placeholder(tmp_path: Path) -> None:
    # Given: a project created only by the scaffold.
    project = tmp_path / "governed"
    created = _run_script("scaffold_governance.py", project)

    # When: the status report reads the generated current-task file.
    result = _run_script("report_status.py", project)

    # Then: the placeholder is not accepted work.
    assert created.returncode == 0, created.stderr
    assert result.returncode == 0, result.stderr
    assert "- 占位行：`1`" in result.stdout
    assert "- 任务卡：`0`" in result.stdout
    assert "- 数量：`0`" in result.stdout
    assert "| 无 | 0 |" in result.stdout


def test_package_contains_new_governance_files() -> None:
    # Given: the repository packaging script, when this checkout has one.
    package_script = Path(__file__).resolve().parents[2] / "scripts" / "package_skill.py"
    if not package_script.is_file():
        import pytest

        pytest.skip("package script is not in this checkout")

    # When: the skill is zipped.
    result = subprocess.run(
        [sys.executable, str(package_script), "agent-test"],
        check=False,
        capture_output=True,
        text=True,
    )

    # Then: the archive contains the new commands and checklist, and no bytecode.
    assert result.returncode == 0, result.stderr
    import zipfile

    zip_path = Path(result.stdout.strip())
    with zipfile.ZipFile(zip_path) as archive:
        names = set(archive.namelist())
    zip_path.unlink(missing_ok=True)
    for required in (
        "coding-rules/scripts/scaffold_governance.py",
        "coding-rules/scripts/report_status.py",
        "coding-rules/assets/project-governance/docs/governance/CHECKLISTS.md",
    ):
        assert required in names
    assert not any(name.endswith(".pyc") or "/__pycache__/" in f"/{name}" for name in names)


def test_blank_task_card_defaults_evidence_to_not_run() -> None:
    # Given: the task-card template shipped with the skill.
    template = (
        Path(__file__).resolve().parent.parent
        / "assets/project-governance/docs/governance/TASK-CARD-TEMPLATE.md"
    )

    # When: the default evidence field is read.
    text = template.read_text(encoding="utf-8")

    # Then: an unfilled card cannot be counted as accepted.
    assert "- 证据状态：`NOT_RUN`" in text


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
