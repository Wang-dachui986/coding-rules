---
name: coding-rules
description: Bootstrap, merge, and enforce a reusable project-governance system for coding projects. Use when the user invokes $coding-rules, starts a new multi-agent or multi-conversation project, asks to create AGENTS.md rules, task cards, role ownership, approval gates, handoff documents, context-recovery rules, or wants an existing project standardized without changing product code.
---

# coding-Rules

Build the governance surface, then stop. Treat explicit invocation as approval
only to inspect existing governance files, create or merge governance documents,
and validate those documents. It does not approve product changes, tests,
network access, Git operations, deployments, server access, purchases, messages,
or destructive actions.

## Bootstrap workflow

1. Locate the project root.
2. Read an existing `AGENTS.md` and existing governance/handoff files before
   writing. Preserve stricter instructions and user decisions.
3. Read [operating-model.md](references/operating-model.md).
4. Materialize the templates under
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

5. For a new project, copy the templates and replace bracketed placeholders
   with verified facts. Leave unknown decisions as `[待项目所有者确认]`.
6. For an existing project, merge instead of overwrite:
   - keep project-specific safety and approval rules;
   - keep established paths and role names when consistent;
   - add missing recovery, task-card, evidence, and handoff gates;
   - never silently weaken an existing rule.
7. Default to R0 plus R1-R3 only when the project needs durable parallel
   workstreams. For a small project, keep R0 and mark unused roles `IDLE`.
8. Validate that every referenced file exists, role ownership does not overlap,
   status vocabulary is consistent, module acceptance has one explicit entry,
   completion reports carry approval states, and no secret entered the documents.
9. Report created and merged files, unresolved placeholders, and the one next
   approval required. Do not begin product work.

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
- Do not create new conversations or redistribute ownership without owner
  approval.
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
