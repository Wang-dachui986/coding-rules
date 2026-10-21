# coding-rules

[![CI](https://github.com/Wang-dachui986/coding-rules/actions/workflows/ci.yml/badge.svg)](https://github.com/Wang-dachui986/coding-rules/actions/workflows/ci.yml)
[![MIT License](https://img.shields.io/github/license/Wang-dachui986/coding-rules)](LICENSE)

[English](#english) · [中文](#中文)

## English

`coding-rules` is an MIT-licensed [Codex](https://developers.openai.com/codex/skills) skill for project governance. In Codex CLI or the IDE extension you invoke it with `$coding-rules`. It writes approval rules, role handoffs, and task-card templates into a coding project, then asks requirements questions until a plan is ready for review. The skill also ships a non-destructive scaffold command, a task-card status report, and checklists for receipt, module acceptance, and release.

The skill directory is [`coding-rules/`](coding-rules/). The repository root is the maintainer-facing project around that skill. There is no sample application, no credentials, and no recorded run of a product project in this repository.

### What it is

On an explicit `$coding-rules` invocation, Codex is instructed to:

1. Treat the current conversation as **R0**.
2. Classify the tree as an existing project or an empty project. Version-control metadata, editor metadata, OS metadata, caches, and generated governance files are ignored for that decision. Secret-shaped files are not read.
3. For an empty project, copy the templates in [`coding-rules/assets/project-governance/`](coding-rules/assets/project-governance/) and replace bracketed placeholders only with verified facts. Unknown decisions stay `[待项目所有者确认]`.
4. For an existing project, merge governance into the files that are already there. The merge never deletes, moves, renames, or overwrites project files. The order is fixed: keep one copy of an identical rule; keep a stricter project rule; add a missing non-conflicting gate; keep the project's path or role name when the meaning matches and record the mapping; stop and ask the owner when objectives or permissions conflict.
5. Create or reuse three long-lived local threads, `<project-name> · R1`, `<project-name> · R2`, and `<project-name> · R3`. Each starts `IDLE`. Existing role threads are reused. Short-lived subagents are not substitutes. If thread tools are missing or creation fails, each missing role is marked `NOT_CREATED` and Codex must give you three prompts to send yourself. It must not claim that initialization succeeded.
6. Offer **LIGHT** or **FULL** requirements intake and ask one question per reply until the planning gate in [`coding-rules/references/intake-model.md`](coding-rules/references/intake-model.md) is met, then present a plan in status `WAITING_REVIEW`.

That invocation authorizes only the read-only classification, the non-destructive governance write, validation of those governance files, and creation of the missing R1–R3 threads. It does not approve product edits, tests, network access, Git, deployment, server access, purchases, messages outside those initialization threads, or destructive actions.

Files an empty project receives (twelve paths):

```text
AGENTS.md
docs/governance/OPERATING-RULES.md
docs/governance/WORKSTREAMS.md
docs/governance/CURRENT-TASKS.md
docs/governance/TASK-CARD-TEMPLATE.md
docs/governance/CHECKLISTS.md
docs/governance/HANDOFF-PROTOCOL.md
docs/handoffs/PROJECT.md
docs/handoffs/R0.md
docs/handoffs/R1.md
docs/handoffs/R2.md
docs/handoffs/R3.md
```

After initialization, the operating model in [`coding-rules/references/operating-model.md`](coding-rules/references/operating-model.md) is the source for roles, statuses, task cards, preflight, receipt, and module acceptance. In short:

- **R0** is the only role that plans, writes task cards, distributes them, checks integration, and reports total progress.
- **R1, R2, and R3** execute one owner-approved card each. They verify, update their own handoff, return facts to R0, and wait. Their normal finished state is `COMPLETED_MODULE_INPUT_READY`, which is not system acceptance.
- The template's default duty split is a starting point, not a claim about your repository. `WORKSTREAMS.md` leaves file ownership as `[待确认]` until the project sets it. The defaults written in the template are: R1 for core business, backend, data, and automated tests; R2 for platform, integration, deployment, operations, and security boundaries; R3 for frontend, interaction, documentation surfaces, and browser QA.
- Before distribution, R0 runs one read-only dispatch-conflict preflight. Distribution is allowed only when that preflight is recorded as `READY_FOR_OWNER_APPROVAL` and you approve that exact card version. Preflight is not approval.
- Between subtasks, R0 does a light receipt check and drafts the next card as `WAITING_APPROVAL`. Drafting does not distribute or execute it. You can say that the current task is the last one; R0 then finishes receipt and the handoff without drafting another card.
- One systematic acceptance runs only after that module's subtasks, shared integration, and required runtime surfaces are done.
- Discussion needs no approval. Mutations and external operations have to be inside an approved task card.
- When a project keeps a development-progress artifact, R0 is the only editor. The template does not invent a path for it; the placeholder is `[待项目所有者确认]`. The tracker is a report, not acceptance evidence.
- When CodeGraph is already available, the skill tells Codex to use it before code search and impact analysis. If the project is not indexed, Codex must not initialize CodeGraph silently.
- Passwords, tokens, private keys, cookies, full server addresses, private URLs, user data, and raw access logs do not go in governance documents.

These statuses are recorded in separate fields. Approval, verification, and preflight results are not written into the task status:

| Field | Values |
| --- | --- |
| Requirements mode | `LIGHT`, `FULL` |
| Plan | `DISCOVERY`, `WAITING_REVIEW`, `APPROVED`, `SUPERSEDED` |
| Task | `PLANNED`, `WAITING_APPROVAL`, `APPROVED`, `IN_PROGRESS`, `COMPLETED_MODULE_INPUT_READY`, `COMPLETED_PENDING_REVIEW`, `COMPLETED_ACCEPTED`, `BLOCKED`, `FAILED`, `SUPERSEDED` |
| Approval | `NOT_REQUIRED`, `WAITING_APPROVAL`, `APPROVED_NOT_EXECUTED`, `COMPLETED`, `BLOCKED` |
| Verification | `PASS`, `FAILED`, `NOT_RUN`, `LIMITED` |
| Conversation | `IDLE`, `IN_PROGRESS`, `NOT_CREATED`, `BLOCKED` |
| Preflight | `READY_FOR_OWNER_APPROVAL`, `REVISE_REQUIRED` |
| Receipt | `ACCEPTED_AS_MODULE_INPUT`, `REJECTED`, `BLOCKED_SAFE_STOP_ACCEPTED_NOT_MODULE_INPUT` |

A verified answer, or `NOT_APPLICABLE` that you confirm, scores coverage. The weights sum to 100:

| Dimension | Weight |
| --- | ---: |
| Goal and observable outcome | 15 |
| Users and core scenarios | 10 |
| Scope and explicit exclusions | 15 |
| Existing project state and reusable assets | 10 |
| Functional requirements and key flows | 15 |
| Data, interfaces, and external dependencies | 10 |
| Security, performance, reliability, and compliance | 10 |
| Environment, deployment, and compatibility | 5 |
| Verification, acceptance, and definition of done | 5 |
| Risks, approvals, and operational boundaries | 5 |

Intake stops only when coverage is at least 95%, the goal, scope, definition of done, security and approval boundary, and blocking dependencies are known, and no open question would change the architecture, data model, delivery scope, or risk level. `LIGHT` may cover an irrelevant dimension with a confirmed `NOT_APPLICABLE`. `FULL` has to collect enough fact in each dimension to plan modules. Neither mode lowers the approval or evidence rules.

### Who it is for

Use it if you want Codex, on a repository you are willing to add governance files to, to keep an approval boundary and a written handoff across conversations.

It fits a project that will split work across one controller conversation (R0) and up to three long-lived execution conversations (R1–R3). It also fits a single conversation that should still leave task cards and handoffs on disk.

It is not a hosted tracker, a sample codebase, or a plugin marketplace listing. Installing the skill does not connect your repository to this GitHub project.

### Install

The directory Codex loads is the inner `coding-rules/` folder, the one that contains `SKILL.md`.

Codex's current user-skill directory is `~/.agents/skills`. A single repository can load it from `.agents/skills/` instead. Those locations are documented at <https://developers.openai.com/codex/skills>. This repository's original install path, `~/.codex/skills`, is `$CODEX_HOME/skills`. The built-in `$skill-installer` skill still installs into that directory. Copy the skill to either place. Codex notices a new skill on its own; restart it if `$coding-rules` does not appear.

```bash
git clone https://github.com/Wang-dachui986/coding-rules.git
cd coding-rules

# Current user-skill location
mkdir -p ~/.agents/skills
cp -R coding-rules ~/.agents/skills/coding-rules

# $CODEX_HOME/skills. $skill-installer writes here.
mkdir -p ~/.codex/skills
cp -R coding-rules ~/.codex/skills/coding-rules
```

For one repository, copy that same directory to `<that-repo>/.agents/skills/coding-rules`.

To install from GitHub with Codex, invoke `$skill-installer` and ask it to install repository `Wang-dachui986/coding-rules` at path `coding-rules` (ref `main`). That path is the skill directory, not the repository root.

A published release zip has the same inner directory plus `LICENSE` at the archive root. The current release is [v0.2.0](https://github.com/Wang-dachui986/coding-rules/releases/tag/v0.2.0). [CHANGELOG.md](CHANGELOG.md) describes that release and the earlier `0.1.0` snapshot.

### Usage

Open Codex in the project you want to govern and send:

```text
$coding-rules
```

If you already know the intake mode, say so in the same request (`LIGHT` or `FULL`). The skill then skips the mode question and asks the first requirements question.

You stay in the R0 conversation for requests and approvals. R0 is instructed to plan, prepare task cards, obtain approval, and distribute approved cards. You do not have to manage R1–R3 yourself unless a thread could not be created.

Every later approved task, and every resume after context compression or a "continue" message, starts by re-reading `AGENTS.md`, `docs/handoffs/PROJECT.md`, the active role handoff, the approved task card, and the inputs that card cites. Chat memory is not a substitute.

### Scaffold, status report, and checklists

From the installed skill directory, or from `coding-rules/` in a git checkout:

```bash
# Copy governance templates. Missing files only; nothing is overwritten.
uv run scripts/scaffold_governance.py /path/to/project

# Show the same paths without writing.
uv run scripts/scaffold_governance.py /path/to/project --dry-run

# Status report from task cards. This is a view, not acceptance.
uv run scripts/report_status.py /path/to/project
```

`scaffold_governance.py` finds its templates next to the script, so the current directory does not matter. `mode: empty` means the project has no meaningful files besides ignored metadata and the governance templates themselves. In both modes the command creates paths that are absent and prints `skipped-existing` for paths that are already there. It does not fill `[待项目所有者确认]` placeholders and it does not merge rules into an existing `AGENTS.md`. `$coding-rules` still does that semantic merge, creates or reuses the R1–R3 threads, and runs intake. The first invocation may use the scaffold command for the file copy it is already allowed to make.

`report_status.py` reads `docs/governance/tasks/*.md`, any task-card path named in `docs/governance/CURRENT-TASKS.md`, and that file's task table. A path that points at a task card uses the card and does not count the table row again. Pass `--tasks-dir` and `--current-tasks` when the project kept other paths. A card is counted as accepted only when its task status is `COMPLETED_ACCEPTED` and its `证据状态` is `PASS`. `NOT_RUN`, a missing evidence status, and any other evidence status are listed under 不能视为已验收. Placeholder rows such as `[待确认]` are not counted as tasks. Running the report is a command; initialization does not approve it. R0 may use the output as the progress view after a command is allowed. R1–R3 do not use it to edit that view.

`docs/governance/CHECKLISTS.md` has three sections: R0 light receipt, the one module acceptance, and release. R0 copies the matching section into the handoff or evidence and marks each item with the existing verification vocabulary. The checklist adds no statuses. A `NOT_RUN` item is not a pass, and finishing a list does not approve the next task or the release.

Without uv, call `python3 scripts/scaffold_governance.py` and `python3 scripts/report_status.py` with the same arguments.

### Worked example

This is an illustration of the rules in `SKILL.md`. It is not a transcript from a Codex session, and this repository does not contain a `notes-api` project.

1. The target is an empty directory, `notes-api`. No source files, docs, or tests are in it. You install the skill, restart Codex if needed, open Codex in `notes-api`, and send `$coding-rules`.
2. Codex classifies the tree as empty. It copies the twelve governance paths listed above, and may do that copy with `scaffold_governance.py`. Fields it cannot verify stay `[待项目所有者确认]`. It does not invent a language, framework, or feature list.
3. It lists existing project threads, then creates any missing long-lived thread titled `notes-api · R1`, `notes-api · R2`, and `notes-api · R3`. Each role prompt tells that thread to read the rules and wait `IDLE`. No product file is edited. No test, network call, or Git command is run.
4. If those thread tools are unavailable, the handoff records `NOT_CREATED` and you receive three prompts. Initialization is not described as successful.
5. Codex asks you to choose `LIGHT` or `FULL`. Suppose you answer `LIGHT`.
6. It asks one question: what observable outcome `notes-api` must produce. You answer. It records every fact in the answer, then asks the single highest-impact question that is still open. Confirmed `NOT_APPLICABLE` answers can fill dimensions that do not apply. It does not draft a task card during this questioning.
7. Suppose the answers cover at least 95% of the weighted table, and the goal, scope, definition of done, security and approval boundary, and blocking dependencies are known. Codex posts a `WAITING_REVIEW` plan: its understanding, the coverage figure, remaining non-blocking unknowns, proposed scope, milestones, acceptance, and risks. Nothing is executed.
8. You approve that plan. Only then may R0 draft a task card from `docs/governance/TASK-CARD-TEMPLATE.md`. The card has one owner, an id, a version, allowed files and commands, forbidden actions, validation, stop conditions, and the handoffs to read and update. R0 runs the read-only preflight against the workspace, the last accepted baseline, handoffs, dependencies, file ownership, allowed paths, validation, and stop conditions.
9. A conflict, missing permission, or impossible check produces `REVISE_REQUIRED`. R0 revises the card and returns it for approval. It does not distribute the old text.
10. A recorded `READY_FOR_OWNER_APPROVAL` result plus your approval of that exact version lets R0 send the card, unchanged, to the named role. That role's completion report lists what it finished, files it changed, commands it actually ran, `NOT_RUN` items, and blockers. It does not report total project progress. The usual status it can reach is `COMPLETED_MODULE_INPUT_READY`.
11. R0 checks card identity, scope, handoff, evidence, dependencies, and high-risk stop conditions, and fills section 1 of `docs/governance/CHECKLISTS.md` in the handoff or evidence. It updates the R0 and PROJECT handoffs when those checks pass, then drafts the next card as `WAITING_APPROVAL` and waits. Your approval of the first card does not approve the next one.
12. After the module's subtasks and shared integration are done, R0 runs one systematic acceptance and fills section 2 of the checklist. Section 3 is for a later release or deployment, which still needs its own approval. You decide the following step. A task card counts as accepted in `report_status.py` only after its task status is `COMPLETED_ACCEPTED` and its `证据状态` is `PASS`. The blank template leaves `证据状态` as `NOT_RUN`.

An existing project differs at steps 2 and 6. Codex reads the non-secret tree and the development docs first, reports verified facts, gaps, non-destructive additions, and decisions it needs, and does not ask again for facts those files already state. Stricter rules already in the project stay. Product files stay where they are.

### Validation

From a git checkout or from the installed skill directory:

```bash
cd coding-rules
uv run scripts/validate_skill.py
uv run scripts/test_validate_skill.py
```

Python 3.11 or newer is required. Without [uv](https://docs.astral.sh/uv/):

```bash
cd coding-rules
python3 scripts/validate_skill.py
python3 -m pip install "pytest>=8,<10"
python3 -m pytest -q scripts/test_validate_skill.py
```

`scripts/validate_skill.py` checks the skill directory:

- required files exist, including `references/operating-model.md`, `references/intake-model.md`, `docs/governance/CHECKLISTS.md`, `scripts/scaffold_governance.py`, and `scripts/report_status.py`
- `SKILL.md` starts with the `coding-rules` frontmatter, has a description, and names the scaffold command, the status report, and `CHECKLISTS.md`
- relative links in `SKILL.md` resolve
- the checklist keeps its three section headings, and the task-card template keeps its required sections plus `证据状态`
- R1, R2, and R3 handoffs do not contain the R0-only headings `## 项目总进度` or `## 下一步顺序及审批状态`
- `._*` and `.DS_Store` files are absent
- Markdown and YAML files are valid UTF-8 and do not match the script's secret-shaped patterns

It does not launch Codex, and it does not test the project you apply the skill to. An optional argument is a skill root: `uv run scripts/validate_skill.py /path/to/skill`.

CI runs those two commands on Python 3.11 and 3.12 for every push and pull request, then builds the skill zip with `python3 scripts/package_skill.py`. The workflow is [`.github/workflows/ci.yml`](.github/workflows/ci.yml). The badge above reads that workflow's status on the default branch. It stays neutral until the workflow file is on `main`.

Pushing a tag such as `v0.2.0` runs [`.github/workflows/release.yml`](.github/workflows/release.yml). The tag is what starts the workflow. The workflow validates the skill, zips it as `coding-rules-<version>.zip`, and creates the GitHub Release when one does not already exist for that tag. [v0.2.0](https://github.com/Wang-dachui986/coding-rules/releases/tag/v0.2.0) is the published release. The change list is [CHANGELOG.md](CHANGELOG.md).

### Repository layout

```text
.
├── README.md
├── LICENSE
├── CHANGELOG.md
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
├── SECURITY.md
├── scripts/package_skill.py
├── .github/workflows/ci.yml
├── .github/workflows/release.yml
└── coding-rules/
    ├── SKILL.md
    ├── agents/openai.yaml
    ├── references/intake-model.md
    ├── references/operating-model.md
    ├── scripts/validate_skill.py
    ├── scripts/test_validate_skill.py
    ├── scripts/scaffold_governance.py
    ├── scripts/report_status.py
    └── assets/project-governance/
```

`agents/openai.yaml` is the skill's display metadata: the name shown in Codex, a short Chinese description, and the default prompt.

### FAQ

**Does `$coding-rules` modify my application?**
No. The invocation may add or merge governance files only. It does not edit product code.

**Will it run tests, Git, or the network because I invoked it?**
No. Those actions need to be listed in a later task card that you approve. A returned "done" from R1–R3 is not acceptance and does not approve the next card.

**What is the difference between an empty project and an existing one?**
An empty project gets the templates copied in. An existing project gets a non-destructive merge. The skill must not invent a stack for an empty project, and it must not re-ask a question the existing docs already answer.

**What is the difference between LIGHT and FULL?**
`LIGHT` asks less, for a small or well-bounded effort. `FULL` goes through users, flows, functions, data, interfaces, non-functional needs, environments, delivery, risks, and acceptance in more detail. The approval, evidence, and 95% gate still apply. You can switch mode later; answers already confirmed are kept.

**Can a mature project skip intake?**
The skill does not define that waiver. After initialization it offers `LIGHT` and `FULL`. An existing project still gets a non-secret scan first, and questions those files already answer are not asked again.

**What if Codex cannot create the R1–R3 threads?**
Those roles are marked `NOT_CREATED`. You get three prompts to send yourself. The skill must not report that thread setup succeeded.

**Who is allowed to state total progress and the next step?**
Only R0. R1–R3 report their own card, evidence, limits, and that the result went back to R0.

**Can I copy the governance files without a Codex conversation?**
Yes. From the skill directory, `uv run scripts/scaffold_governance.py /path/to/project` creates every missing template and leaves existing files untouched. It does not fill placeholders, merge an existing `AGENTS.md`, create threads, or approve product work. `$coding-rules` still does the semantic merge, the R1–R3 threads, and intake.

**When does the status report count a task as accepted?**
Only when the task status is `COMPLETED_ACCEPTED` and `证据状态` is `PASS`. `NOT_RUN` stays in the 不能视为已验收 section. The report is a view R0 can paste into the progress artifact after a command is approved. It is not acceptance evidence.

**Why are the templates in Chinese?**
The skill text, role prompts, and templates in this repository are written in Chinese. The validator checks structure, not translation.

**Does a green validator run mean Codex followed the skill?**
No. It means this skill directory passed the file checks listed above.

**Where are the community docs?**
[CONTRIBUTING.md](CONTRIBUTING.md), [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md), and [SECURITY.md](SECURITY.md). Bugs and feature ideas use the issue templates. Please do not put secrets in an issue.

### Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Behavior changes belong in the skill and the templates, and the README should be updated only to match those files.

### License

MIT License. Copyright (c) 2026 Wang-dachui986. See [LICENSE](LICENSE).

## 中文

一个面向 Codex 编程项目的通用治理 Skill。它会为新项目或现有项目建立：

- `AGENTS.md` 执行与审批规则；
- R0–R3 角色分工和任务卡；
- 多对话任务分发规范；
- 上下文压缩、中断恢复和交接文档；
- R1–R3 定向验证、R0 轻量接收和模块末单次系统验收；
- 完成汇报、项目总进度、下一步顺序和逐项审批状态；
- R0 唯一维护开发进度制品，并在每次任务闭环后同步功能、审批和更新日志；
- 首次调用时检查已有项目或空项目，非破坏性部署规则并创建或复用 R1–R3
  长期执行对话；
- `LIGHT` 轻量问答与 `FULL` 全量问答两种需求收集模式；
- 每次只询问一个最高优先级问题，需求覆盖率达到 95% 后才提交计划审阅；
- 现有项目先扫描非秘密文件和开发文档，再给出已验证现状、缺口和非破坏性
  调整建议；
- 空项目直接进行需求发现，不臆造技术栈或业务需求；
- 计划先进入 `WAITING_REVIEW`，获得批准后才允许执行；
- 独立的需求、计划、任务、审批、验证、对话、预检和接收状态命名空间；
- 确定性治理合并规则与可直接运行的 Skill 验证器；
- 证据真实性、CodeGraph 和验收闭环规则；
- 非破坏性脚手架：只补齐缺失的治理文件，不覆盖已有文件；
- 从任务卡生成状态报告，证据状态不是 `PASS` 时不计入已验收；
- 轻量接收、模块验收和发布三份检查清单。

本仓库只包含通用项目开发治理规则和空白模板，不包含任何具体项目源码、凭据或运行证据。

### 安装

```bash
git clone https://github.com/Wang-dachui986/coding-rules.git
mkdir -p ~/.codex/skills
cp -R coding-rules/coding-rules ~/.codex/skills/coding-rules
```

若技能没有出现在列表里，重新打开 Codex。

当前文档中的用户技能目录是 `~/.agents/skills`。上面的 `~/.codex/skills` 是本仓库原来的安装路径，也是 `$CODEX_HOME/skills`；内置的 `$skill-installer` 仍安装到那里。同一份内层 `coding-rules` 目录（含 `SKILL.md` 的那一层）放到任一位置即可。

```bash
mkdir -p ~/.agents/skills
cp -R coding-rules/coding-rules ~/.agents/skills/coding-rules
```

只想在某一个仓库里使用时，把同一目录放到该仓库的 `.agents/skills/coding-rules`。

### 调用

在目标项目的 Codex 对话中输入：

```text
$coding-rules
```

Skill 会先判断项目是否已有有效文件。已有项目只安全合并规则，不删除、移动、
重命名或覆盖项目文件；空项目直接生成治理和交接模板。首次调用还会复用已有
R1–R3 对话并补建缺失角色，三个角色保持 `IDLE` 等待 R0 分发获批任务卡。
它不会因调用而自动修改产品代码、运行测试、联网、执行 Git 操作、部署或
访问服务器。

初始化完成后可以选择：

- `LIGHT`：适合小项目或边界清晰的需求，问题更少、更直接；
- `FULL`：适合大型项目，详细覆盖用户、流程、功能、数据、接口、非功能需求、
  环境、交付、风险和验收。

无论选择哪种模式，Skill 每次只问一个问题。只有加权需求覆盖率至少达到
95%、阻塞维度已经明确且不存在重大歧义时，才会生成状态为
`WAITING_REVIEW` 的计划供用户审阅。计划获批后，R0 才会编制任务卡并把获批
任务分发给 R1–R3；用户无需分别管理三个执行对话。

初始化之后一定会提供 `LIGHT` 和 `FULL`。Skill 和模板里没有“成熟项目可在
`AGENTS.md` 里免除这轮问答”的规则。已有项目会先读非秘密文档，文件里已经
写明的问题不会再问。

### 合并与验证

现有项目采用确定性、非破坏性合并顺序：相同规则去重，项目中更严格的规则
保留，缺失且不冲突的治理门槛补入；路径或角色名称不同但语义一致时保留项目
现有命名；目标或权限发生冲突时停止写入并交由用户决定。

安装后可以运行内置检查：

```bash
cd ~/.codex/skills/coding-rules
uv run scripts/validate_skill.py
uv run scripts/test_validate_skill.py
```

在本仓库中，把目录换成检出的 `coding-rules/` 即可。校验器只检查 Skill 目录，
不会启动 Codex，也不会测试你之后套用规则的产品项目。校验还会确认检查清单的
三个章节都在、任务卡模板含有 `证据状态`，并且 `SKILL.md` 提到下面两条命令。

### 脚手架、状态报告与检查清单

在已安装的 Skill 目录或本仓库的 `coding-rules/` 中运行：

```bash
# 只创建缺失的治理模板，不覆盖已有文件
uv run scripts/scaffold_governance.py /path/to/project

# 只打印将创建和将跳过的路径
uv run scripts/scaffold_governance.py /path/to/project --dry-run

# 从任务卡生成状态报告。这是报告视图，不是验收证据
uv run scripts/report_status.py /path/to/project
```

没有 uv 时，把命令换成 `python3 scripts/scaffold_governance.py` 和
`python3 scripts/report_status.py`，参数相同。

`scaffold_governance.py` 按脚本所在位置寻找模板，不依赖当前目录。
`mode: empty` 表示除被忽略的元数据和治理模板之外，没有有效项目文件。
空项目和已有项目都只补缺失文件，已存在的路径打印 `skipped-existing`。
脚本不填写 `[待项目所有者确认]`，也不把规则合并进已有的 `AGENTS.md`。
语义合并、R1–R3 对话和需求问答仍由 `$coding-rules` 完成。首次调用可以用
脚手架完成它本来就获准的那次非破坏性复制。

`report_status.py` 读取 `docs/governance/tasks/*.md`、`CURRENT-TASKS.md`
表格里写明的任务卡路径，以及这张表本身。路径指向任务卡时以任务卡为准，
不把同一路径再计一次。项目如果保留了别的路径，用
`--tasks-dir` 和 `--current-tasks` 传入。只有任务状态为 `COMPLETED_ACCEPTED`
且 `证据状态` 为 `PASS` 的卡计入已验收。`NOT_RUN`、缺失或其它证据状态列入
「不能视为已验收」。`[待确认]` 这类占位行不计入任务。空白任务卡的证据状态
默认是 `NOT_RUN`。运行报告是一条命令，初始化并不批准它。R0 可以在命令获批后
把标准输出当作进度视图；R1–R3 不用它修改进度制品。

`docs/governance/CHECKLISTS.md` 有三节：R0 轻量接收、一次模块系统性验收、
发布检查。R0 把对应章节抄入交接或证据，并用现有验证状态填写。清单不新增
状态词。`NOT_RUN` 不是通过，填完清单也不批准下一张任务卡或本次发布。

### 仓库结构

```text
.
├── README.md
├── LICENSE
├── CHANGELOG.md
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
├── SECURITY.md
├── scripts/package_skill.py
└── coding-rules/
    ├── SKILL.md
    ├── agents/openai.yaml
    ├── scripts/validate_skill.py
    ├── scripts/test_validate_skill.py
    ├── scripts/scaffold_governance.py
    ├── scripts/report_status.py
    ├── references/intake-model.md
    ├── references/operating-model.md
    └── assets/project-governance/
```

贡献、行为准则和安全报告见 [CONTRIBUTING.md](CONTRIBUTING.md)、[CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) 和 [SECURITY.md](SECURITY.md)。版本说明见 [CHANGELOG.md](CHANGELOG.md)。

### 许可证

MIT License。见 [LICENSE](LICENSE)。
