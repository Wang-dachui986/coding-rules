# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project uses [semantic versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

Target version: 0.2.0. These notes describe unreleased work. Publishing them does not create a tag or a GitHub Release.

### Added

- `scripts/scaffold_governance.py` copies missing governance templates into a project. Empty and existing projects both only gain files that are not already there. The command never deletes, moves, renames, or overwrites a file, and it does not fill placeholders or merge rules into an existing file. It refuses the filesystem root and any target inside the skill directory. `mode: empty` reports the skill's emptiness rule; it does not change that write rule. `--dry-run` prints the paths. `$coding-rules` may use the command for the initialization copy it is already allowed to make. Semantic merge, thread setup, and intake stay with the skill.
- `scripts/report_status.py` prints a Markdown status report from `docs/governance/tasks/*.md`, task-card paths named in `CURRENT-TASKS.md`, and that file's task table. A table path that points at a task card uses the card and does not count that row again. `--tasks-dir` and `--current-tasks` select other paths. A card is counted as accepted only when its task status is `COMPLETED_ACCEPTED` and its `证据状态` is `PASS`. `NOT_RUN`, a missing evidence status, and any other evidence status are listed under 不能视为已验收. The report is a view, not acceptance, and initialization does not approve running it.
- `docs/governance/CHECKLISTS.md`, with sections for R0 light receipt, the one module acceptance, and release. The checklist adds no status values. A `NOT_RUN` item is not a pass, and finishing a list does not approve the next task or the release.
- Task cards record `证据状态` as `PASS`, `FAILED`, `NOT_RUN`, or `LIMITED`. The blank template defaults to `NOT_RUN`.
- Validator checks for the checklist headings, the task-card sections and evidence field, `SKILL.md` mentions of the two commands and the checklist, and the command files themselves.

### Changed

- An empty project now receives twelve governance paths. The twelfth is `docs/governance/CHECKLISTS.md`.

## [0.1.0] - 2026-10-21

First public snapshot of the `coding-rules` Codex skill. The behavior below is
what `SKILL.md`, the references, and the templates specify. This repository
does not include a sample application, credentials, or recorded project
evidence.

### Added

- Codex skill `coding-rules` (`SKILL.md` and `agents/openai.yaml`), invoked as `$coding-rules`
- Empty-project setup that copies the governance templates, and a non-destructive merge for projects that already have files
- Deterministic merge order: deduplicate identical rules, keep a stricter project rule, add a missing non-conflicting gate, keep the project's path or role name when the meaning matches, and stop when objectives or permissions conflict
- Templates for `AGENTS.md`, operating rules, workstreams, current tasks, the task-card template, the handoff protocol, and handoffs for PROJECT, R0, R1, R2, and R3
- R0 as the only planner and distributor; R1–R3 execute one approved task card each and do not report total progress or draft the next card
- First-run reuse or creation of three long-lived R1–R3 threads, titled `<project-name> · R1` through `R3`, left `IDLE` until R0 distributes an approved card. If thread tools are unavailable, the roles are marked `NOT_CREATED` and three ready-to-send prompts are provided
- `LIGHT` and `FULL` intake, one question per reply, and a weighted 95% coverage gate before a plan in `WAITING_REVIEW`
- Separate status vocabularies for requirements mode, plan, task, approval, verification, conversation, preflight, and receipt
- Read-only dispatch-conflict preflight (`READY_FOR_OWNER_APPROVAL` or `REVISE_REQUIRED`) before distribution
- Light receipt between subtasks, automatic drafting of the next card as `WAITING_APPROVAL`, and one systematic module acceptance after that module's subtasks and shared integration
- Context-recovery reads, evidence rules, secret-handling rules, CodeGraph usage when it is already available, and an optional development-progress artifact maintained only by R0
- `scripts/validate_skill.py` and `scripts/test_validate_skill.py`
- GitHub Actions CI, a `v*` tag workflow that zips the skill and attaches it to a GitHub Release, and community health files

### Fixed

- The validator now requires `references/operating-model.md`, which `SKILL.md` tells Codex to read during bootstrap
- The validator reports a Markdown or YAML file that is not valid UTF-8 instead of exiting with a traceback
- `uv run scripts/test_validate_skill.py` runs the tests
- Tracked Python bytecode caches are removed and ignored
- The README no longer says a mature project can waive requirements intake from `AGENTS.md`. The skill always offers `LIGHT` and `FULL` after initialization. That waiver is not defined in the skill or the templates

[Unreleased]: https://github.com/Wang-dachui986/coding-rules/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/Wang-dachui986/coding-rules/releases/tag/v0.1.0
