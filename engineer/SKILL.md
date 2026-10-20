---
name: engineer
description: A complete engineering workflow for planning, implementing and shipping changes
---

# Engineer

Make sure you have all the information needed to work independently before starting. If not, ask clarifying questions before beginning.

## Set up once

1. Read repository instructions; inspect branch, worktree, and checks with `rg -n` and targeted reads. A dirty tree is not a blocker: record a baseline of tracked and relevant untracked files and preserve it. Ask only about ambiguous ownership, conflicting edits, or destructive operations.
2. Save the task and checkable outcomes in `task.md`, keyed by the supplied ticket or a descriptive local ID (not a Jira key).
3. Artifact directory: the supplied one, else `${ENGINEER_ARTIFACT_ROOT:-~/.local/state/engineer}/<repo>/<task-id>/` as an absolute path outside the repository. Reuse this session's folder; for an older run, resume compatible work without overwriting reports, or use a new directory when scope differs.
4. On the default branch, create `<task-id>-<short-description>`; on a feature branch, stay. Ask before disturbing a merge, rebase, or detached work. Do not stage, commit, or publish without authorization.
5. Run `../preflight/SKILL.md`. If `blocked`, report the blockers and stop, unless setup is authorized and the documented fix works.

## Execute

0. Resolve any unanswered questions, make targeted checks with ripgrep to verify assumptions.
1. Write a spec for the work. Use `human-review` to open this and ask for approval. Do not proceed without explicit approval.
2. Implement the spec with a subagent
3. Run the `reviewer` subagent
4. Report the output of `reviewer`, and a roundup of the changes we've made in plain english.
5. Ask the user if they're happy to ship the changes, if so, run `ship-it`
6. Run `agent-feedback` for this session, review what went well, what didn't go well, and what we can tweak to improve performance and efficiency next time.

Allow two repair rounds per blocker; then report the evidence and the decision needed. Preserve completed work. Do not rerun passing checks, completed research, or whole agents without a changed input.

## Human approval and checks

Before asking for approval or a human check, save the document and open it per [human-review.md](../references/human-review.md) in Neovim in a **new Ghostty tab**. Ask in chat and wait for an explicit answer before dependent actions.
