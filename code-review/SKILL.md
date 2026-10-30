---
name: code-review
description: Review a branch or diff for every change the author should make - bugs, risks, design, tests and docs, including effects on other repos - and give a pass or changes-needed verdict that only blocking findings fail. Use when asked to review code, a diff, a branch or a pull request, or when the engineer workflow reaches review.
---

# Code review

Use this process. It finds the most issues because the reviews are free-form and independent, and the shape is added only at the end.

1. **Brief:** collect the facts about the change.
2. **Reach:** find code in other repos that the change affects.
3. **Review:** run two independent, free-form reviews.
4. **Merge:** combine every point, check each against the code, and write one report.

Write all working files to the artifact directory when one is given. Otherwise use the work folder in [vault.md](../references/vault.md). Leave repository files unchanged.

**Small change:** when the diff is under 100 changed lines in one repo and names nothing from the boundary list in step 2, skip step 2 and write `reach.md` as one line: "Skipped: small change." Run review 1 only in step 3. Do steps 1 and 4 as usual.

## 1. Brief

- Find the base branch (usually `main`) and the head. Include uncommitted changes when the user points to them.
- Collect the ticket, plan or PR title and description, if you have them.
- Write `brief.md`: the repo path, the base and head refs, the diff command (`git diff <base>...<head>`), the changed files, and the ticket text. Facts only. Leave out opinions.

Done when `brief.md` exists.

## 2. Reach

Find where the change reaches outside this repo.

- The **workspace** is the repos that `AGENTS.md`, `CLAUDE.md` or the README names, plus sibling git repos in the parent directory whose `origin` remote has the same owner as this repo. Ignore other siblings.
- From the diff, list the names that cross a boundary: routes and URL paths, API fields and status codes, queue, job and event names, env vars and config keys, database tables and columns, shared files, and package names.
- Search the workspace for each name with `rg -n`. For each hit, record the file and line, and one line on what that code does with it (calls it, consumes it, duplicates it, configures it).

Then collect two kinds of facts inside this repo:

- **One-sided changes.** For each changed file, find its siblings: files with a parallel name or place that differ by one token, such as an environment, region, service, tenant or locale (`worker_uk.tf` and `worker_xi.tf`, `staging.yml` and `production.yml`). For each sibling the diff leaves unchanged, list the added or removed lines that it does not have.
- **Entry paths.** For each class, method, constant, config key and env var whose signature, behaviour or value the diff changes, list **every** reference with `rg -n`, not only the ones the change is about. When a name has more than 20 references, record the count and the 20 nearest to the change, and say so. Follow each recorded reference up to its entry point (controller action, job, rake task, scheduled task, event listener or CLI command). Record which deployment runs it (service, worker, queue or region) and any guard on the way (a service check, a feature flag).

Write `reach.md` as tables. Facts only: leave out whether a path is safe. If there is no workspace, or nothing matches, say so in one line.

Run this step in the `context-scout` agent when it exists, else in a general-purpose subagent with read-only tools. Give it this section's instructions and the paths to `brief.md` and `reach.md`.

Done when every boundary name, changed file and changed symbol has been searched.

## 3. Review

Run **two** independent reviews. Use subagents when you can, started at the same time. Use the `plain-reviewer` agent when it exists, else a general-purpose subagent with read-only tools and no review instructions of its own. Give review 1 exactly this prompt, with the paths filled in:

> Review the change described in `<brief.md>`. Code in other repos that the change touches is listed in `<reach.md>`; read it where it matters. Read any code you need. This is a review only: change no files, and do not load a code-review skill. Write your full review to `<review-1.md>`.

Give review 2 the same prompt without the `reach.md` sentence, writing to `review-2.md`. Different inputs make the two reviews look in different places. Step 4 checks `reach.md` either way.

Add nothing else. Plain, free-form reviews find more issues than guided ones.

If you cannot start subagents, write one review yourself in the same free-form way. Use your own judgement and format, as if this skill had no report rules. Save it as `review-1.md`, then go to step 4.

Done when each review file exists.

## 4. Merge

When you also coordinate other work (for example the engineer workflow), run this step in a subagent to keep your own context small. Give it the paths to `brief.md`, `reach.md` and the review files, and the path to this skill's section 4. Ask it to return only the report path, the verdict and the blockers.

Read every review. List every point they raise. Merge points that name the same defect at the same place. Keep the best explanation of each.

Check each point against the code:

- **Confirmed** or **not provable either way:** keep it. For an unproven point, state the defect as a fact, then say in "Why it matters" what the author must confirm.
- **Disproved:** drop it only when you can cite the code that makes it safe. List it under **Dropped** with that evidence in one line.

Every point that was not disproved goes in the report. A missed point costs more than an extra one.

Then read `reach.md`. For each one-sided change and each entry path that no review explains, add a finding: name the sibling or path, and say what breaks if it needs the same change. Drop it only with the same evidence as above, covering every path.

### Report

Put the verdict first, then the findings, most severe first. Write each finding as:

- **Where:** file and line
- **Problem:** the defect, stated as a fact in one sentence
- **Why it matters:** the input or state, and what goes wrong
- **Fix:** the change to make

Sort the findings into two tiers:

- **Blocking:** wrong behaviour, lost or exposed data, a security gap, a failed deploy, a hidden failure, a break in another repo, or a test that cannot catch a regression.
- **Should fix:** everything else the author should change: design, readability, naming, tests, docs and copy.

End with **Dropped** (one line each) and **Limits** (what nobody could check, such as production config or a repo that is not on disk).

Verdict: `changes needed` if there is any Blocking finding. Otherwise `pass`, with any Should fix findings still listed. A pending human check is a verification limit, not a blocker. For a repair, review the fix and nearby risks only.

Write the report to `review.md` in the artifact directory when one is given, and return only its path, the verdict and the blockers. Otherwise return the report in chat.

## Language

Follow [language.md](../references/language.md). For each finding, say what to change and why. When a finding uses a concept the author may not know, explain it in one sentence.
