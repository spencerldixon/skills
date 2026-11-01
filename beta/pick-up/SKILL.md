---
name: pick-up
description: Recover unfinished work on a branch or ticket and identify the next action when asked to pick up, resume or recover context.
model: sonnet
---
Read the task and existing handoff; inspect branch, worktree status, staged and unstaged changes, and at most 20 relevant commits.
Check the associated ticket, PR, CI and review when available; compare their claims with the current code and report unavailable evidence.
Report the goal, completed work, uncommitted work, verification still needed, blockers and one concrete next action, with evidence links.
Treat old notes as leads, not proof; distinguish a passing check from a claim that it passed. Preserve unrelated edits. Resume implementation only when requested. Follow [language.md](../../references/language.md).
