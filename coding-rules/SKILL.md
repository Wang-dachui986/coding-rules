---
name: coding-rules
description: Bootstrap, merge, and enforce a reusable project-governance system for coding projects. Use when the user invokes $coding-rules, starts a new multi-agent or multi-conversation project, asks to create AGENTS.md rules, task cards, role ownership, approval gates, handoff documents, context-recovery rules, or wants an existing project standardized without changing product code.
---

# coding-Rules

Build the governance surface and initialize the execution conversations, then
stop. A first explicit invocation authorizes read-only project classification,
non-destructive governance creation or merge, validation, and creation of the
three missing long-lived R1-R3 project threads. It does not approve product
changes, tests, network access, Git operations, deployments, server access,
purchases, messages outside those initialization threads, or destructive
actions.

## Bootstrap workflow

1. Locate the project root and treat the current conversation as R0.
2. Inspect the project tree without reading secrets. Ignore VCS metadata,
   editor metadata, OS metadata, caches, and generated governance files when
   deciding whether meaningful project files exist.
   - If meaningful code, configuration, documentation, assets, or tests exist,
     classify it as an existing project and merge governance without deleting,
     moving, renaming, or overwriting project files.
   - If no meaningful project files exist, classify it as an empty project and
     materialize the governance files directly.
3. Read an existing `AGENTS.md` and existing governance/handoff files before
   writing. Preserve stricter instructions and user decisions.
4. Read [operating-model.md](references/operating-model.md).
5. Materialize the templates under
   [project-governance](assets/project-governance/) into the project:

   ```text
   AGENTS.md
   docs/governance/OPERATING-RULES.md
   docs/governance/WORKSTREAMS.md
   docs/governance/CURRENT-TASKS.md
   docs/governance/TASK-CARD-TEMPLATE.md
   docs/governance/HANDOFF-PROTOCOL.md
   docs/handoffs/PROJECT.md
   docs/handoffs/R0.md
   docs/handoffs/R1.md
   docs/handoffs/R2.md
   docs/handoffs/R3.md
   ```

6. For an empty project, copy the templates and replace bracketed placeholders
   with verified facts. Leave unknown decisions as `[待项目所有者确认]`.
7. For an existing project, merge instead of overwrite:
   - keep project-specific safety and approval rules;
   - keep established paths and role names when consistent;
   - add missing recovery, task-card, evidence, and handoff gates;
   - never silently weaken an existing rule.
8. On first initialization, create or recover the execution conversations:
   - Use `list_projects` to resolve the current saved project, then
     `list_threads` to inspect existing project threads before creating anything.
   - Reuse any existing R1, R2, or R3 thread. Create exactly one long-lived local
     project thread for each missing role; never create duplicates and never use
     short-lived subagents as substitutes.
   - Use `create_thread` with the resolved project and local environment, then
     `set_thread_title` when available. Title threads consistently as
     `<project-name> · R1`, `<project-name> · R2`, and `<project-name> · R3`.
   - Use this role prompt, replacing `<ROLE>` only: "You are <ROLE>, a long-lived
     execution role for this project. Read AGENTS.md, docs/handoffs/PROJECT.md,
     docs/handoffs/<ROLE>.md, and docs/governance/WORKSTREAMS.md. Set your status
     to IDLE. Do not plan the project, create task cards, modify product files,
     run commands or tests, or contact other roles. Wait for an owner-approved
     task card distributed by R0."
   - Record verified thread identifiers/status in `WORKSTREAMS.md` and the role
     handoffs when the tools expose them. Never invent an identifier.
   - If project/thread tools are unavailable or thread creation fails, mark each
     uncreated role `NOT_CREATED`, provide three ready-to-send role prompts, and
     state the exact blocker. Do not claim initialization succeeded.
   - Emit any created-thread UI directives required by the active Codex product
     so the new threads are visible to the user.
9. Validate that every referenced file exists, role ownership does not overlap,
   status vocabulary is consistent, module acceptance has one explicit entry,
   completion reports carry approval states, R1-R3 thread status is truthful,
   and no secret entered the documents.
10. End with a concise onboarding message that explains R1, R2, and R3 and says:
    the user only needs to continue in R0; R0 plans, prepares task cards, obtains
    approval, and distributes approved cards automatically. Report created or
    reused role threads, unresolved placeholders, and the next approval required.
    Do not begin product work.

## Enforcement after bootstrap

- At every approved task start, and again after interruption, context
  compression, or a “continue/next” request, read `AGENTS.md`, PROJECT, the
  active role handoff, the approved task card, and its referenced inputs. Do
  not rely on chat memory or a previous read.
- R0 is the only durable task-distribution and integration entry.
- R1-R3 execute only owner-approved task cards distributed by R0.
- R1-R3 never plan the project, draft or alter follow-up cards, assign other
  roles, calculate total progress, or propose project-wide next steps. They
  execute, verify, update their own handoff, return facts to R0, and wait.
- Discussion and explanation need no approval. Mutating actions and external
  operations follow the generated approval boundary.
- Every task card must name one owner, exact scope, allowed files/actions,
  validation, forbidden actions, stop conditions, and handoff updates.
- Each R1-R3 subtask follows:
  `complete inspection → concentrated fix → targeted verification → handoff`.
  Its maximum normal result is `COMPLETED_MODULE_INPUT_READY`, not system
  acceptance.
- Between subtasks, R0 performs only a light receipt check of card identity,
  scope, handoff, evidence, dependencies, and high-risk stop conditions. Do
  not rerun full tests, builds, or browser matrices for every role.
- After every R1-R3 result, R0 automatically completes that light receipt,
  updates R0 and PROJECT handoffs as needed, and drafts the next repair or
  module task card. Do not ask separately whether to draft the next card.
- Freeze the next card's ID, version, scope, `WAITING_APPROVAL` status, and
  digest, then report it to the owner. Drafting is governance closeout only:
  never distribute or execute the card before explicit owner approval.
- Before any R1-R3 distribution, R0 performs one lightweight read-only
  dispatch-conflict preflight against the current workspace, last accepted
  baseline, role handoffs, dependencies, file ownership, allowed paths,
  validation, and stop conditions. Use CodeGraph for code impact. Do not run
  full tests or acceptance during this preflight.
- If the preflight finds a missing file permission, conflicting objective,
  insufficient frozen input, overlapping active ownership, impossible
  validation, or an already-known stop condition, do not distribute. Revise
  the card, issue a new version/digest, and return it for owner approval.
- Only a recorded `READY_FOR_OWNER_APPROVAL` preflight plus explicit approval
  of that exact card version permits distribution. Preflight is not approval.
- Run one systematic acceptance only after the predefined module's subtasks,
  shared integration, and required runtime surfaces are complete.
- Escalate security, secret exposure, data-loss risk, real product blockers,
  contract conflicts, and out-of-scope edits immediately. If the owner
  ratifies a shared-file exception, record the exact file and non-expanding
  boundary before continuing.
- Do not claim completion without actual evidence and updated handoffs.
- Separate verified fact, inference, not-run, blocked, failed, and approved but
  unexecuted work.
- Never place passwords, tokens, private keys, full server addresses, cookies,
  private URLs, user data, or raw access logs in governance documents.
- R1-R3 completion responses and handoffs list only completed work, changed
  files, actual validation and NOT_RUN items, evidence, blockers/limits, and
  that the result was returned to R0. They do not report total project
  progress or design follow-up work.
- Only R0 reports total project progress, drafts ordered next tasks, assigns
  approval states, and asks the owner for the next approval. Current approval
  never authorizes the next task.
- When a project uses a durable development-progress artifact, R0 is its only
  maintainer. At every task closeout, R0 updates the affected feature rows,
  approvals, update log, as-of date, and project summary from accepted evidence.
  R1-R3 only return verified facts in their handoffs and never edit the tracker.
- A progress tracker is a reporting view, not an acceptance source. Keep
  evidence-backed system-acceptance progress separate from planning estimates
  or arithmetic averages, and never mark `NOT_RUN` work as accepted.
- If the tracker is a spreadsheet, keep one stable owner-facing path and verify
  key formulas, formula errors, and every changed sheet's visual rendering after
  each update.

## Conversation and agent routing

- Use long-lived project conversations only for durable workstreams with
  independent ownership.
- Use short-lived subagents only for bounded parallel review or research when
  project rules and the user permit delegation.
- A first explicit `$coding-rules` invocation is approval to create exactly the
  missing R1-R3 initialization threads described above. Outside that one
  non-executing initialization, do not create conversations or redistribute
  ownership without owner approval.
- Before any creation, list existing project threads and reuse matching roles.
  Never create a second R1, R2, or R3 thread for the same project.
- Send each role the approved task card unchanged, including the files to read
  first and handoffs to update last.
- Distribution evidence must cite the dispatch-conflict preflight artifact,
  exact card digest, resolved conflicts, and remaining limitations.
- Finalize approval source, status, version, and any fixed digest before
  distribution. If the card changes afterward, issue a new version/digest and
  obtain any approval required by the project instead of silently drifting it.
- Prefer the existing long-lived role conversation and confirm that it
  received or started the task when thread tools expose that state.
- R0 independently accepts or rejects returned evidence; a role's completion
  claim is not final acceptance.
- A returned completion, failure, or blocker triggers R0's automatic closeout
  sequence: light receipt, handoff update, next-card draft, owner report, and
  approval wait. It never authorizes distribution or product execution.

## Code intelligence

When CodeGraph is available, use it before code search, call-chain analysis,
debugging, or modification impact analysis. Do not reread source already
returned by CodeGraph. If the project is not indexed, stop using CodeGraph and
follow the environment's indexing policy; do not initialize it silently.

## Template handling

Templates are output assets, not project truth. Replace placeholders only with
verified information. If merging would overwrite a meaningful existing rule,
stop and request one precise decision.
