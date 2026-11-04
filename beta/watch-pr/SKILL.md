---
name: watch-pr
description: Watch PRs for failing CI, merge conflicts and new review activity, report only what changed, and fix small blockers. Use when asked to watch, babysit or check on PRs, including under /loop. Never merges.
---

# Watch PR

Use `gh` to watch for PR activity only in the given scope.
If given no scope, watch only open and draft PRs i have authored.
Watch known PRs until merged or closed.
Query only what you need.
Report what needs attention; merge conflicts, failing CI, new review activity, new comments, unresolved threads.
On the first run, show me a list of my current PRs and their state, and tell me what needs attention. 
On subsequent runs, only show me new or changed actions.
Make your report concise and easy to scan quickly, use bullet points. Sacrifice grammar for the sake of brevity. 
Make links clickable.
If rerunning the CI or a small bounded change would get the PR over the line, run it or use a [fixer](../../agents/fixer.md) to fix it and commit the change. Report this to the user. If you are not confident in fixing this yourself, or it is a bigger change, report back to the user.
Only change code on PRs I authored.
Never merge. Report the PR as ready and leave merging to me.
