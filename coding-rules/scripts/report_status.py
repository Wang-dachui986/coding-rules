# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
# ─── How to run ───
# uv run scripts/report_status.py <project-root> [--tasks-dir PATH] [--current-tasks PATH]

"""Print a Markdown status report from task cards and CURRENT-TASKS.md.

The report is a view, not acceptance evidence. A card is counted as accepted
only when its task status is ``COMPLETED_ACCEPTED`` and its ``证据状态`` is
``PASS``. ``NOT_RUN``, a missing evidence status, and any other evidence
status stay out of that count.

Default inputs are ``docs/governance/tasks/*.md`` and
``docs/governance/CURRENT-TASKS.md``, relative to the project root. Pass
``--tasks-dir`` and ``--current-tasks`` when the project kept other paths.
"""

from __future__ import annotations

import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

USAGE = (
    "usage: report_status.py <project-root> [--tasks-dir PATH] [--current-tasks PATH]"
)
DEFAULT_TASKS_DIR = "docs/governance/tasks"
DEFAULT_CURRENT_TASKS = "docs/governance/CURRENT-TASKS.md"
ACCEPTED_STATUS = "COMPLETED_ACCEPTED"
PASS_EVIDENCE = "PASS"
UNSET = "UNSET"
STATUS_ORDER = (
    "PLANNED",
    "WAITING_APPROVAL",
    "APPROVED",
    "IN_PROGRESS",
    "COMPLETED_MODULE_INPUT_READY",
    "COMPLETED_PENDING_REVIEW",
    "COMPLETED_ACCEPTED",
    "BLOCKED",
    "FAILED",
    "SUPERSEDED",
)
FIELD_PATTERN_NAMES = {
    "版本": "version",
    "负责人": "owner",
    "状态": "task_status",
    "预检结论": "preflight",
    "证据状态": "evidence",
}


@dataclass(frozen=True)
class TaskRecord:
    task_id: str
    source: str
    owner: str
    task_status: str
    preflight: str
    evidence: str
    placeholder: bool


def _clean(value: str) -> str:
    return value.strip().strip("`").strip()


def _token(value: str) -> str:
    text = _clean(value)
    if not text or text.startswith("[") or " / " in text:
        return UNSET
    return text


def _placeholder_id(task_id: str) -> bool:
    text = _clean(task_id)
    return not text or text.startswith("[") or text in {"待确认", "TASK-ID"}


def _field_map(text: str) -> dict[str, str]:
    found: dict[str, str] = {}
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped.startswith("- "):
            continue
        body = stripped[2:]
        if "：" in body:
            name, value = body.split("：", 1)
        elif ":" in body:
            name, value = body.split(":", 1)
        else:
            continue
        key = name.strip()
        if key in FIELD_PATTERN_NAMES and key not in found:
            found[key] = value.strip()
    return found


def parse_task_card(text: str, source: str) -> TaskRecord | None:
    task_id = ""
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("#") and "任务卡：" in stripped:
            task_id = _clean(stripped.split("任务卡：", 1)[1])
            break
    if not task_id:
        return None
    fields = _field_map(text)
    return TaskRecord(
        task_id=task_id,
        source=source,
        owner=_token(fields.get("负责人", "")),
        task_status=_token(fields.get("状态", "")),
        preflight=_token(fields.get("预检结论", "")),
        evidence=_token(fields.get("证据状态", "")),
        placeholder=_placeholder_id(task_id),
    )


def _split_row(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def _is_separator(cells: list[str]) -> bool:
    return bool(cells) and all(cell and set(cell) <= set("-: ") for cell in cells)


def parse_current_tasks(text: str) -> tuple[dict[str, str], list[list[str]], list[str]]:
    plan = {"问答模式": UNSET, "需求覆盖率": UNSET, "计划状态": UNSET}
    rows: list[list[str]] = []
    next_steps: list[str] = []
    in_table = False
    in_next = False
    for line in text.splitlines():
        if line.startswith("## "):
            in_next = line.startswith("## 下一步")
            in_table = False
            continue
        if in_next:
            if line.strip():
                next_steps.append(line.strip())
            continue
        if line.startswith("|") and "任务 ID" in line and not in_table and not rows:
            in_table = True
            continue
        if in_table:
            if not line.startswith("|"):
                in_table = False
            else:
                cells = _split_row(line)
                if not _is_separator(cells) and len(cells) >= 6:
                    rows.append(cells[:6])
                continue
        stripped = line.strip()
        for label in plan:
            prefix = f"- {label}"
            if stripped.startswith(prefix):
                rest = stripped[len(prefix) :].lstrip("：:").strip()
                plan[label] = _token(rest)
    return plan, rows, next_steps


def _path_cell(value: str) -> str | None:
    text = _clean(value)
    if not text or text.startswith("[") or " " in text or "://" in text:
        return None
    return text


def _read(path: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None


def _resolve(project_root: Path, raw: str) -> Path:
    path = Path(raw)
    if path.is_absolute():
        return path
    return project_root / path


def collect(project_root: Path, tasks_dir: Path, current_tasks: Path) -> tuple[list[TaskRecord], list[str], dict[str, str], list[str], bool]:
    records: list[TaskRecord] = []
    unparsed: list[str] = []
    seen: set[Path] = set()
    plan = {"问答模式": UNSET, "需求覆盖率": UNSET, "计划状态": UNSET}
    next_steps: list[str] = []
    current_exists = current_tasks.is_file()

    if tasks_dir.is_dir():
        for path in sorted(tasks_dir.glob("*.md")):
            if path.name.startswith("._"):
                continue
            seen.add(path.resolve())
            text = _read(path)
            source = path.resolve().relative_to(project_root).as_posix() if path.resolve().is_relative_to(project_root) else path.as_posix()
            if text is None:
                unparsed.append(source)
                continue
            record = parse_task_card(text, source)
            if record is None:
                unparsed.append(source)
            else:
                records.append(record)

    table_rows: list[list[str]] = []
    if current_exists:
        text = _read(current_tasks)
        if text is None:
            unparsed.append(_display(project_root, current_tasks))
        else:
            plan, table_rows, next_steps = parse_current_tasks(text)

    for cells in table_rows:
        task_id, owner, status, _scope, card_path, evidence = cells
        relative = _path_cell(card_path)
        if relative is not None:
            card = _resolve(project_root, relative)
            if card.is_file():
                resolved = card.resolve()
                if resolved in seen:
                    continue
                seen.add(resolved)
                card_text = _read(card)
                source = _display(project_root, card)
                if card_text is None:
                    unparsed.append(source)
                    continue
                record = parse_task_card(card_text, source)
                if record is None:
                    unparsed.append(source)
                else:
                    records.append(record)
                continue
        records.append(
            TaskRecord(
                task_id=_clean(task_id),
                source=_display(project_root, current_tasks),
                owner=_token(owner),
                task_status=_token(status),
                preflight=UNSET,
                evidence=_token(evidence),
                placeholder=_placeholder_id(task_id),
            )
        )
    return records, unparsed, plan, next_steps, current_exists


def _display(project_root: Path, path: Path) -> str:
    resolved = path.resolve()
    if resolved.is_relative_to(project_root):
        return resolved.relative_to(project_root).as_posix()
    return path.as_posix()


def _status_rows(records: list[TaskRecord]) -> list[tuple[str, int]]:
    counts = Counter(record.task_status for record in records if not record.placeholder)
    ordered = [status for status in STATUS_ORDER if counts[status]]
    unknown = sorted(status for status in counts if status not in STATUS_ORDER)
    return [(status, counts[status]) for status in ordered + unknown]


def _blocked(records: list[TaskRecord]) -> list[str]:
    lines: list[str] = []
    for record in records:
        if record.placeholder:
            continue
        if record.task_status == ACCEPTED_STATUS and record.evidence != PASS_EVIDENCE:
            lines.append(
                f"- `{record.task_id}`：任务状态 `{ACCEPTED_STATUS}`，证据状态 `{record.evidence}`"
            )
    return lines


def render_report(
    records: list[TaskRecord],
    unparsed: list[str],
    plan: dict[str, str],
    next_steps: list[str],
    *,
    current_exists: bool,
    current_label: str,
) -> str:
    real = [record for record in records if not record.placeholder]
    placeholders = [record for record in records if record.placeholder]
    accepted = [
        record
        for record in real
        if record.task_status == ACCEPTED_STATUS and record.evidence == PASS_EVIDENCE
    ]
    duplicate_ids = sorted(task_id for task_id, count in Counter(record.task_id for record in real).items() if count > 1)
    status_rows = _status_rows(records)
    blocked = _blocked(records)
    lines = [
        "# 项目状态报告",
        "",
        f"- 任务卡：`{len(real)}`",
        f"- 占位行：`{len(placeholders)}`",
        "- 说明：本报告是报告视图，不是验收证据。只有任务状态为"
        f" `{ACCEPTED_STATUS}` 且证据状态为 `{PASS_EVIDENCE}` 的任务计入已验收。"
        " `NOT_RUN` 不计入已验收。",
        "",
        "## 任务状态",
        "",
        "| 状态 | 数量 |",
        "|---|---:|",
    ]
    if status_rows:
        lines.extend(f"| `{status}` | {count} |" for status, count in status_rows)
    else:
        lines.append("| 无 | 0 |")
    lines.extend(["", "## 已验收", "", f"- 数量：`{len(accepted)}`", "", "## 不能视为已验收", ""])
    lines.extend(blocked or ["- 无。"])
    lines.extend(["", "## 重复任务 ID", ""])
    lines.extend(f"- `{task_id}`" for task_id in duplicate_ids)
    if not duplicate_ids:
        lines.append("- 无。")
    lines.extend(["", "## 未解析文件", ""])
    lines.extend(f"- `{path}`" for path in unparsed)
    if not unparsed:
        lines.append("- 无。")
    lines.extend(
        [
            "",
            "## 明细",
            "",
            "| 任务 ID | 来源 | 负责人 | 任务状态 | 预检结论 | 证据状态 |",
            "|---|---|---|---|---|---|",
        ]
    )
    ordered = sorted(records, key=lambda record: (record.placeholder, record.task_id, record.source))
    if ordered:
        for record in ordered:
            lines.append(
                f"| `{record.task_id}` | `{record.source}` | `{record.owner}` | "
                f"`{record.task_status}` | `{record.preflight}` | `{record.evidence}` |"
            )
    else:
        lines.append("| 无 | 无 | 无 | 无 | 无 | 无 |")
    lines.extend(["", "## 当前任务表", ""])
    if current_exists:
        lines.append(f"- 文件：`{current_label}`")
        lines.append(f"- 问答模式：`{plan.get('问答模式', UNSET)}`")
        lines.append(f"- 需求覆盖率：`{plan.get('需求覆盖率', UNSET)}`")
        lines.append(f"- 计划状态：`{plan.get('计划状态', UNSET)}`")
        lines.append("- 下一步：")
        if next_steps:
            lines.extend(f"  - {step}" for step in next_steps)
        else:
            lines.append("  - 无。")
    else:
        lines.append("- 文件：`缺失`")
    lines.append("")
    return "\n".join(lines)


def _parse_args(argv: list[str]) -> tuple[str, str, str] | None:
    positionals: list[str] = []
    tasks_dir = DEFAULT_TASKS_DIR
    current_tasks = DEFAULT_CURRENT_TASKS
    index = 0
    while index < len(argv):
        arg = argv[index]
        if arg in {"--tasks-dir", "--current-tasks"}:
            if index + 1 >= len(argv):
                return None
            value = argv[index + 1]
            if arg == "--tasks-dir":
                tasks_dir = value
            else:
                current_tasks = value
            index += 2
            continue
        if arg.startswith("-"):
            return None
        positionals.append(arg)
        index += 1
    if len(positionals) != 1:
        return None
    return positionals[0], tasks_dir, current_tasks


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    parsed = _parse_args(args)
    if parsed is None:
        print(USAGE, file=sys.stderr)
        return 2
    raw_root, raw_tasks, raw_current = parsed
    project_root = Path(raw_root).expanduser().resolve()
    if not project_root.is_dir():
        print("report: project root is not a directory", file=sys.stderr)
        return 2
    tasks_dir = _resolve(project_root, raw_tasks)
    current_tasks = _resolve(project_root, raw_current)
    card_paths = []
    if tasks_dir.is_dir():
        card_paths = [path for path in tasks_dir.glob("*.md") if not path.name.startswith("._")]
    if not current_tasks.is_file() and not card_paths:
        print("report: no CURRENT-TASKS.md and no task cards", file=sys.stderr)
        return 1
    records, unparsed, plan, next_steps, current_exists = collect(project_root, tasks_dir, current_tasks)
    sys.stdout.write(
        render_report(
            records,
            unparsed,
            plan,
            next_steps,
            current_exists=current_exists,
            current_label=_display(project_root, current_tasks),
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
