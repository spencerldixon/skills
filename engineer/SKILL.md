---
name: engineer
description: Coordinate implementation and independent review of a ticket or bounded fix with subagents. Use a short workflow for clear changes and a planner for unresolved design. Ask for approval only at material decisions or required human checks.
---

# Engineer

Coordinate the work; delegate product code to the implementer. The user's request defines scope and authorization. Existing approval carries forward. Ask only when missing information prevents safe progress, and continue independent work meanwhile.

- **Bounded change:** concrete outcome, known area, no unresolved design. Implement, verify, review. A review with specific fixes is enough input.
- **Design work:** uncertain behavior, architecture, migrations, permissions, or several interacting areas. Plan first.

## Set up once

1. Read repository instructions; inspect branch, worktree, and checks with `rg -n` and targeted reads. A dirty tree is not a blocker: record a baseline of tracked and relevant untracked files and preserve it. Ask only about ambiguous ownership, conflicting edits, or destructive operations.
2. Save the task and checkable outcomes in `task.md`, keyed by the supplied ticket or a descriptive local ID (not a Jira key).
3. Artifact directory: the supplied one, else `${ENGINEER_ARTIFACT_ROOT:-~/.local/state/engineer}/<repo>/<task-id>/` as an absolute path outside the repository. Reuse this session's folder; for an older run, resume compatible work without overwriting reports, or use a new directory when scope differs.
4. On the default branch, create `<task-id>-<short-description>`; on a feature branch, stay. Ask before disturbing a merge, rebase, or detached work. Do not stage, commit, or publish without authorization.
5. Run `../preflight/SKILL.md`. If `blocked`, report the blockers and stop, unless setup is authorized and the documented fix works.
6. Keep one short `status.md`: scope, mode, baseline, decisions and approvals, current step, report paths, commands run with results, open limits. Update it at transitions; do not copy reports into it.

## Delegate

In Claude Code, use the plugin agents `planner`, `implementer`, and `reviewer`; their front matter sets tools, model, and effort, so do not override them. Elsewhere, start a fresh-context agent (Codex: `fork_turns="none"`) that reads `../agents/<role>.md`, with strong reasoning for planning and review and a cheaper model for implementation.

Pass only the job, task and report paths, repository, artifact directory, baseline, authorized scope, and the path to `../agent-feedback/SKILL.md`. Do not paste role instructions or the conversation. Each agent writes its report once and returns the path, a short outcome, and blockers. Planner and reviewer write only their reports; prompt rules are not a sandbox. If a runner cannot write files, use its output-file option.

## Execute

1. **Plan (design work):** planner writes `plan.md`. Ask its open questions as one structured prompt, recommended option first, and record answers in `status.md`. Resume the same planner with the answers (Claude Code: SendMessage), or start a new one with `plan.md` and the answers. Get approval only for a material decision the user has not authorized or a requested plan gate; otherwise state the approach in one line and proceed.
2. **Implement:** implementer reads `task.md` and `plan.md` and writes `build.md`.
3. **Verify:** run the relevant documented checks once yourself and record exact commands and results. A missing tool is a limitation, not a pass.
4. **Review:** reviewer reads the task, plan, diff against the baseline (tracked and relevant untracked files), and `../code-review/SKILL.md`, and writes `review.md`. Send blocking findings by report path to the implementer, verify, then have the reviewer check the repair.
5. **Human check:** only if important UI or device behavior is unverified, or the user asked. Reviewer follows `../walkthrough/SKILL.md` and writes `walkthrough.md`.
6. **Report:** outcome, verification, report links, and real limits. Follow `../agent-feedback/SKILL.md` yourself, then summarize `feedback.md`: propose repository-instruction lines for approval and list skill or tool suggestions. Apply none without approval. Use `../ship-it/SKILL.md` only when shipping is authorized.

Allow two repair rounds per blocker; then report the evidence and the decision needed. Preserve completed work. Do not rerun passing checks, completed research, or whole agents without a changed input.

## Human approval and checks

Before asking for approval or a human check, save the document and open it per [human-review.md](../references/human-review.md) in Neovim in a **new Ghostty tab**. Ask in chat and wait for an explicit answer before dependent actions.

## Language

Use concise Simplified Technical English. Define unfamiliar concepts when they affect a decision. Progress updates state new findings or completed checks; final replies stand alone.
