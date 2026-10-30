---
name: engineer
description: Implement a ticket or bounded fix, using a lightweight path for small, clear, low-risk changes and a full workflow for larger or risky work. Use when asked to implement, build or fix a ticket end to end, or take it to a pull request.
---

# Engineer

## Choose the path

Fetch the ticket once, or reuse complete current content already supplied. Read repo instructions and relevant code with targeted searches/ranges. State the path and reason in one sentence.

**Lightweight by default when all hold:** one repo; small local change; clear acceptance criteria; automated proof; no unresolved product decisions; no auth, permissions, personal-data handling, payments, destructive data changes, migrations, infrastructure or changed public/shared contracts. Testing existing routes or adding a larger test matrix alone does not force the full path.

**Full:** any condition fails, the user requests it, or investigation exposes wider scope/risk. Only then read [full-workflow.md](references/full-workflow.md). On escalation, reuse decisions and passing checks; create only missing artifacts.

## Shared safeguards

- Inspect branch/worktrees and baseline tracked/relevant untracked changes; preserve unrelated work. On the default branch create `<task-id>-<short-description>`; stay on a compatible feature branch. Ask before disturbing merges, rebases, detached work or ambiguous ownership.
- Use [vault.md](../references/vault.md) for the work folder and state note. Resume from saved state rather than restarting discovery.
- Staging, commits, pushes, PRs and Jira mutations require authorization. Preserve advance spec/shipping approval and draft mode.

## Lightweight

1. **Plan:** give a short inline goal, reason, acceptance criteria and test commands. An implementation request approves a plan making no new product decisions. Ask about missing decisions; honor explicit spec-approval gates.
2. **Ready:** run [preflight](../preflight/SKILL.md) for those tests. Stop on setup blockers rather than rebuilding the environment.
3. **Implement here:** this agent writes regression tests and the minimal fix. Verify a bug regression fails for the intended reason before the fix, then passes. Run affected tests, changed-file lint and repo-mandated checks; expand when callers or failures justify it.
4. **Review once:** use one independent read-only reviewer, or review here if delegation is unavailable. Supply the compact brief, baseline/diff command, relevant paths and test results. Check the diff, affected callers and regression coverage; return findings with file/line evidence and limits. Where supported, expose code-reading tools only. This replaces the full code-review workflow on this path: no scouting or merge agents. Fix confirmed findings here and rerun affected checks. Request focused repair review for Blocking fixes; after two failed repair rounds, stop with evidence and the decision needed. Escalate wider scope/risk.
5. **Record:** keep one short `<id>.md` state note: goal/criteria, repo/branch, decisions, checks/results, review verdict/limits and next action. Update at milestones and before stopping. Separate task/spec/build/brief/review files are unnecessary. If an orchestrator requires `steps.md`, retain only its progress and `waiting:`/decision signals there.
6. **Finish:** report changes, checks and limits. Offer walkthrough/shipping together unless already answered. If authorized, run ship-it; run watch-pr only after a PR exists. Otherwise stop for the user.

## Context budget

Use tiny Obsidian budgets first, increasing only for missing relevant evidence. Reuse the compact brief and results. Batch independent reads; bound output to summaries/errors without hiding acceptance criteria or relevant code. Pass workers facts, not instructions to rediscover Jira, the vault or the conversation. Record elapsed time and fresh/cache/output usage when available; budgets never excuse incomplete verification.
