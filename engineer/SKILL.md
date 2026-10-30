---
name: engineer
description: Run a ticket or bounded fix from spec to pull request - approved spec, implementation subagent, code-review, fixer subagent, then ship-it. Use when asked to implement, build or fix a ticket end to end, or to take a change all the way to a pull request.
---

# Engineer

Make sure you have all the information needed to work independently before starting. If not, ask clarifying questions before beginning. Do not ask what the request already answers, such as an approval given in advance.

## Set up once

1. Read repository instructions; inspect branch, worktree, and checks with `rg -n` and targeted reads. A dirty tree is not a blocker: record a baseline of tracked and relevant untracked files and preserve it. Ask only about ambiguous ownership, conflicting edits, or destructive operations.
2. Save the task in `task.md`, keyed by the supplied ticket or a descriptive local ID (not a Jira key). Write the goal and the reason for it (who needs the change, and what goes wrong without it), the background the ticket gives, and the checkable outcomes. Agents that read only this file make better choices when they know why. Leave out discussion that does not change what to build.
3. Use the work folder from [vault.md](../references/vault.md). Reuse this session's folder; for an older run, resume compatible work without overwriting reports, or use a new folder when scope differs.
4. Create `steps.md` in the work folder. After each step, append one line: the step, its outcome, and the path to its report. Before each question to the user, append `waiting: <question>`; after the answer, append the decision. Read it first when you resume. Preserve completed work: do not rerun passing checks, completed research, or whole agents without a changed input.
5. On the default branch, create `<task-id>-<short-description>`; on a feature branch, stay. Ask before disturbing a merge, rebase, or detached work. Do not stage, commit, or publish without authorization.
6. Run `../preflight/SKILL.md`. If `blocked`, report the blockers and stop, unless setup is authorized and the documented fix works.

## Execute

1. Resolve any unanswered questions and verify assumptions with targeted `rg -n` checks. Then write `spec.md` in the work folder. If the request approves the spec in advance, check it yourself: each acceptance criterion in the ticket maps to a spec item and a test, and the spec makes no decision the ticket leaves open. Otherwise, or if the check fails, open it per [show-to-human.md](../references/show-to-human.md) and ask for approval. Do not proceed without explicit approval.
2. Implement the spec with a general-purpose subagent. Give it the paths to `task.md` and `spec.md`, the repository path, and this brief: implement the spec, add or update tests that prove each outcome in `task.md`, run those tests, and return only the changed files, the test commands with their results, and anything left undone.
3. Run `code-review` yourself, with the work folder. It writes `review.md`.
4. If the verdict is `changes needed` or the review has Should fix findings, run the `fixer` subagent with the path to `review.md`.
5. If the fixer changed code for a Blocking finding, or reported one as `not a defect`, run `code-review` again as a repair review: the fix and nearby risks only, written to `review-repair-N.md`. Give it the Blocking findings from the last report as the ticket text, and not the fixer's report: the review checks the code, not the fixer's claims. Then go back to step 4 with that report. Allow two repair rounds per blocker; then report the evidence and the decision needed.
6. Report the review, the output of `fixer`, and a roundup of the changes we've made in plain English.
7. Ask the user if they would like a manual walkthrough. If yes, run `walkthrough` and open it per [show-to-human.md](../references/show-to-human.md).
8. Ask the user if they're happy to ship the changes. If so, run `ship-it`.
9. Run `watch-pr` and notify me with anything that needs my attention.
