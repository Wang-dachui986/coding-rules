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
   status vocabulary is consistent, and no secret entered the documents.
9. Report created and merged files, unresolved placeholders, and the one next
   approval required. Do not begin product work.

## Enforcement after bootstrap

- Read `docs/handoffs/PROJECT.md`, the active role handoff, and the approved
  task card before continuing after interruption or context compression.
- R0 is the only durable task-distribution and integration entry.
- R1-R3 execute only owner-approved task cards distributed by R0.
- Discussion and explanation need no approval. Mutating actions and external
  operations follow the generated approval boundary.
- Every task card must name one owner, exact scope, allowed files/actions,
  validation, forbidden actions, stop conditions, and handoff updates.
- Finish a small feature as one loop:
  `complete inspection → concentrated fix → targeted verification → one full acceptance`.
- Do not claim completion without actual evidence and updated handoffs.
- Separate verified fact, inference, not-run, blocked, failed, and approved but
  unexecuted work.
- Never place passwords, tokens, private keys, full server addresses, cookies,
  private URLs, user data, or raw access logs in governance documents.

## Conversation and agent routing

- Use long-lived project conversations only for durable workstreams with
  independent ownership.
- Use short-lived subagents only for bounded parallel review or research when
  project rules and the user permit delegation.
- Do not create new conversations or redistribute ownership without owner
  approval.
- Send each role the approved task card unchanged, including the files to read
  first and handoffs to update last.
- R0 independently accepts or rejects returned evidence; a role's completion
  claim is not final acceptance.

## Code intelligence

When CodeGraph is available, use it before code search, call-chain analysis,
debugging, or modification impact analysis. Do not reread source already
returned by CodeGraph. If the project is not indexed, stop using CodeGraph and
follow the environment's indexing policy; do not initialize it silently.

## Template handling

Templates are output assets, not project truth. Replace placeholders only with
verified information. If merging would overwrite a meaningful existing rule,
stop and request one precise decision.
