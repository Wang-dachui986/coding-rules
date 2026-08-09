# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
# ─── How to run ───
# uv run scripts/validate_skill.py [skill-root]

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Final

REQUIRED_PATHS: Final = (
    "SKILL.md",
    "agents/openai.yaml",
    "references/intake-model.md",
    "assets/project-governance/AGENTS.md",
    "assets/project-governance/docs/governance/CURRENT-TASKS.md",
    "assets/project-governance/docs/governance/HANDOFF-PROTOCOL.md",
    "assets/project-governance/docs/governance/OPERATING-RULES.md",
    "assets/project-governance/docs/governance/TASK-CARD-TEMPLATE.md",
    "assets/project-governance/docs/governance/WORKSTREAMS.md",
    "assets/project-governance/docs/handoffs/PROJECT.md",
    "assets/project-governance/docs/handoffs/R0.md",
    "assets/project-governance/docs/handoffs/R1.md",
    "assets/project-governance/docs/handoffs/R2.md",
    "assets/project-governance/docs/handoffs/R3.md",
)
FORBIDDEN_ROLE_HEADINGS: Final = ("## 项目总进度", "## 下一步顺序及审批状态")
LINK_PATTERN: Final = re.compile(r"\[[^]]+\]\(([^)]+)\)")
SECRET_PATTERN: Final = re.compile(
    r"BEGIN (?:RSA|OPENSSH|EC) PRIVATE KEY|vless://|password\s*[:=]|"
    r"token\s*[:=]|cookie\s*[:=]",
    re.IGNORECASE,
)


def validate(skill_root: Path) -> list[str]:
    errors = [f"missing: {path}" for path in REQUIRED_PATHS if not (skill_root / path).exists()]
    skill_file = skill_root / "SKILL.md"
    if skill_file.exists():
        text = skill_file.read_text(encoding="utf-8")
        if not text.startswith("---\nname: coding-rules\n") or "\ndescription:" not in text:
            errors.append("invalid SKILL.md frontmatter")
        for target in LINK_PATTERN.findall(text):
            if "://" not in target and not (skill_file.parent / target).resolve().exists():
                errors.append(f"broken SKILL.md link: {target}")

    for role in ("R1", "R2", "R3"):
        handoff = skill_root / f"assets/project-governance/docs/handoffs/{role}.md"
        if handoff.exists():
            text = handoff.read_text(encoding="utf-8")
            errors.extend(
                f"{role} contains R0-only heading: {heading}"
                for heading in FORBIDDEN_ROLE_HEADINGS
                if heading in text
            )

    for path in skill_root.rglob("*"):
        if path.name.startswith("._") or path.name == ".DS_Store":
            errors.append(f"metadata file: {path.relative_to(skill_root)}")
        if path.is_file() and path.suffix in {".md", ".yaml"}:
            if SECRET_PATTERN.search(path.read_text(encoding="utf-8")):
                errors.append(f"secret-shaped content: {path.relative_to(skill_root)}")
    return errors


def main() -> int:
    root = Path(sys.argv[1]).resolve() if len(sys.argv) == 2 else Path(__file__).parent.parent
    errors = validate(root)
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(f"OK: {root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
