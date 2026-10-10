---
name: engineer
description: Coordinate implementation and independent review of a ticket or bounded fix with subagents. Use a short workflow for clear changes and a planner for unresolved design. Ask for approval only at material decisions or required human checks.
---

# Engineer

Coordinate the work; delegate product code to the implementor. The user's request defines scope and authorization. Existing approval carries forward.

## Choose the workflow

- **Bounded change:** concrete outcome, known affected area, no unresolved design. Send the task directly to the implementor, verify, then obtain an independent review. A review with specific fixes is enough input; do not require a separate ticket or planner.
- **Design work:** uncertainty about behavior, architecture, migrations, permissions, or several interacting areas. Use the planner first. Ask for approval only when the plan contains a material decision the user has not authorized, or the user requested a plan gate. Otherwise explain the approach briefly and proceed.
- Ask focused questions only when missing information prevents safe progress. Continue independent work. Do not force a ticket-writing interview for a clear request.

## Set up once

1. Read repository instructions and inspect branch, worktree, and relevant checks. A dirty tree is not itself a blocker. Preserve existing work and record a baseline for tracked and relevant untracked files. Ask only about ambiguous ownership, conflicting edits, or destructive operations.
2. Save the task and checkable outcomes in `task.md`. Use the supplied key, or generate a descriptive local ID without asking. Local IDs are not Jira tickets.
3. Use an explicit artifact directory when supplied; otherwise use `${ENGINEER_ARTIFACT_ROOT:-~/.local/state/engineer}/<repo>/<task-id>/`, expanded to an absolute path outside the repository. Reuse the active session's folder. For older runs, inspect status and resume compatible work without overwriting reports; create a new run directory when scope differs.
4. On the default branch, create `<task-id>-<short-description>`; on a feature branch, stay there. Ask before disturbing a merge/rebase or detached work. Do not stage, commit, or publish without authorization.
5. Maintain one short `status.md`: scope, mode, baseline, decisions/approval evidence, current step, report paths, commands actually run and results, unresolved limits. Update it at transitions; do not duplicate full reports in it.

## Delegate with minimal context

Resolve role files relative to this skill:
- `../agents/planner.md`
- `../agents/implementor.md`
- `../agents/reviewer.md`

Start with fresh context when supported (Codex collaboration: `fork_turns="none"`). Pass the role file path, task/report paths, repository and artifact directory, baseline, authorized scope, and the current job. Have the agent read its role instructions; do not paste those instructions or the conversation into its prompt. Read other files only as needed.

Each agent writes its report once to the assigned artifact path and returns only that path, a short outcome, and blockers. Planner and reviewer may write their assigned reports, but must not edit product files. Give them report-write capability; a tool-enforced read-only agent cannot write reports. If a runner only supports read-only execution, capture its report with the runner's output-file option and read the saved file rather than copying it through chat.

Use native subagent tools when available. With command-line runners, pass file paths and use their output-file or redirected output support. Keep logs separate from Markdown reports. Never claim prompt-level file restrictions are an operating-system sandbox.

Use the runtime's available/default model unless the user configures an available model per role. A cheaper implementor is reasonable for a precise bounded task; uncertain planning and independent review need stronger reasoning. Record the actual model when known. Do not infer cost savings from role names or invent model IDs. Agent roles do not imply model tiers.

## Execute

1. **Plan, when needed:** planner writes `plan.md` (normally at most 600 words). Resolve material questions; retain small assumptions in the plan. Use the approval procedure below only if a decision needs it.
2. **Implement:** implementor reads `task.md`, optional `plan.md`, and repository instructions. It writes `build.md`. Let it make routine implementation choices inside the authorized scope.
3. **Verify:** run the relevant documented checks yourself once after implementation. Record exact commands/results in `status.md`. Missing tools are a limitation, not a reason to invent a pass. Broaden checks only for a material unresolved concern.
4. **Review:** reviewer reads task, optional plan, actual diff/baseline, and `../code-review/SKILL.md`; writes `review.md`. Include tracked and relevant untracked changes. For a repo without commits use the saved baseline. Send blocking findings by report path to the implementor, verify changed code, then have the reviewer check the repair. Do not restart completed research.
5. **Human check, when needed:** if important UI/device behavior could not be verified, or the user requested it, reviewer follows `../walkthrough/SKILL.md` and writes `walkthrough.md`. Default to six core actions; separate optional edge/recovery checks. Otherwise skip this step and state automated evidence.
6. **Report:** concise outcome, verification, report links, and real limitations. No mandatory step/model table. If publishing requires a decision, present a concrete ready result; use `../ship-it/SKILL.md` only when shipping is authorized.

A failed check or review allows two repair rounds for the same blocker. After two unsuccessful rounds, report the evidence and required decision. Preserve completed work. Do not repeat passing checks or rerun entire agents without a changed input or unresolved concern.

## Human approval and check documents

Before asking for approval or a required human check, save the document and follow [human-review.md](../references/human-review.md) to open it in Neovim in a **new Ghostty tab**. Ask the decision in chat and wait for an explicit answer before dependent actions. Continue independent work where possible.

## Language

Use concise Simplified Technical English. Define unfamiliar concepts when they affect a decision. Progress updates should state new findings or completed checks; final replies must stand alone.
