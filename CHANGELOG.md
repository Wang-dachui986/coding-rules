# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project uses [semantic versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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
