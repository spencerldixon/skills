# Full engineer workflow

Use this path when SKILL.md selects the full workflow. Read this file only then.

## Set up once

1. Save `task.md` in the work folder: the goal, why it matters, relevant background and checkable outcomes. Use the supplied ticket key or a descriptive local ID. Reuse compatible work without overwriting existing reports.
2. Create `steps.md`. Append one line per completed step with its outcome and report path. Before each question, append `waiting: <question>`; after the answer, append the decision. Read it first on resume. Reuse passing checks and completed research unless their inputs changed.
3. Run [preflight](../../preflight/SKILL.md) for the intended checks. If blocked, report the blocker and stop unless setup is explicitly authorized and the bounded documented fix works.

## Execute

1. Resolve unanswered questions with targeted code checks, then write `spec.md`. If the request approves the spec in advance, verify each acceptance criterion maps to a spec item and a test, with no decisions the ticket leaves open. Otherwise, or if verification fails, open it per [show-to-human.md](../../references/show-to-human.md) and ask for approval. Proceed only with explicit approval.
2. Implement with a general-purpose subagent. Supply a compact approved brief, repository path, relevant file paths and exact test commands. Include the goal, why, acceptance criteria, constraints and baseline. Point to `task.md` and `spec.md` for missing detail, rather than asking it to rediscover Jira or vault context. Where supported, expose code/test tools only. Return changed files, commands/results and unfinished work, not raw logs.
3. Run [code-review](../../code-review/SKILL.md) with the work folder. It writes `review.md`.
4. If the verdict is `changes needed` or there are Should fix findings, run the fixer subagent with `review.md`.
5. For a changed Blocking fix, or a Blocking finding disputed as `not a defect`, rerun code-review on the fix and nearby risks only. Write `review-repair-N.md`. Supply the prior Blocking findings, not the fixer's claims. Return to step 4. Allow two repair rounds per blocker, then report the evidence and decision needed.
6. Report the review, fixes, verification limits and a plain-English change summary. Update the main state note before stopping.
7. Offer a manual walkthrough unless already declined. If requested, run [walkthrough](../../walkthrough/SKILL.md) and open it per show-to-human.md.
8. Ask whether to ship unless already authorized. If authorized, run [ship-it](../../ship-it/SKILL.md), preserving requested draft mode.
9. After a PR exists, run [watch-pr](../../watch-pr/SKILL.md) and notify the user of anything needing attention.
