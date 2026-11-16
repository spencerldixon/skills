---
name: code-review
description: Review a branch, diff or pull request and end with a pass or changes-needed verdict. Use when asked to review code, a diff, a branch or a pull request.
---

# Code review

Benchmarks on our shipped PRs showed a free-form review finds the most issues. Checklists, filters and fixed formats each cost recall, so this skill adds structure only after the review.

1. Find the base (usually `main`) and the head. Include uncommitted changes when the user points to them. Collect the PR title and ticket if you have them.
2. Review `git diff <base>...<head>` freely. Read any code you need, including sibling repos in the parent directory that the change touches. Report every point the author should change, each with file and line. Done when every changed file has been read.
3. After the review, add one line: `Verdict: changes-needed` when any point is wrong behaviour, lost or exposed data, a security gap, a failed deploy or a break in another repo. Otherwise `Verdict: pass`. Keep every point from step 2 in full.

Leave repository files unchanged.
