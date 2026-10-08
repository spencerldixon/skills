---
name: code-review
description: Review a branch or diff for real problems, each with a concrete failure scenario, and give a pass or changes-needed verdict. Use when asked to review code, a diff, a branch or a pull request, or when acting as the reviewer in the engineer workflow.
---

# Code review

Find the problems that would hurt in production or in the next change, and nothing else.

## What to review

- Find the base branch (usually `main`) and review `git diff <base>...HEAD`, plus any uncommitted changes the user points to.
- Read the ticket and the plan if you have them, so you can judge whether the change does what was asked.
- Read the repo's `AGENTS.md` (or `CLAUDE.md`) for its conventions.
- Read enough of the surrounding code to understand each change. Don't review lines in isolation.

## Check, in this order

1. **Correctness.** Does it do what the ticket asks? Check edge cases: empty and missing values, boundaries, error paths, concurrency, time zones.
2. **Tests.** Do they cover the new behaviour? Would they fail if the code broke? Do they test the real code rather than their own mocks?
3. **Security.** Check input validation, authorisation on every new path, injection (SQL, shell, HTML), secrets in code or logs, and over-permissive parameters.
4. **Data.** Can migrations run on a large table and be rolled back? Are backfills safe? Are indexes in place for new queries?
5. **Performance.** Look for N+1 queries, unbounded queries or loops, and work done per request that could be done once.
6. **Conventions.** Does it follow the repo's patterns and `AGENTS.md`?
7. **Simplicity.** Look for dead code, needless abstraction, and duplication of something that already exists.

## Report

Report only real problems. Style preferences are not findings. Write each finding as:

- **Where:** file and line
- **Problem:** one sentence
- **Failure scenario:** the input or state, and what goes wrong
- **Severity:** `blocking` (should stop the merge) or `non-blocking`
- **Fix:** what to change

End with a verdict: `pass` if there are no blocking findings, otherwise `changes needed`. If you found nothing, say so plainly rather than inventing findings.

## Language

Write in Simplified Technical English.

Build the user's knowledge. When you use a concept, decision or file that may be new to them, say what it is and why it matters, in one sentence.

Be concise. Put the answer or decision first. Cut every word that does not help the user act or learn.
