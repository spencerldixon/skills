---
name: watch-pr
description: Watch PRs for failing CI, merge conflicts and new review activity, report their state, and fix small blockers. Use when asked to watch, babysit or check on PRs, including under /loop. Never merges.
---

# Watch PR

Use `gh` to watch for PR activity only in the given scope.
If given no scope, watch only open and draft PRs i have authored.
Watch known PRs until merged or closed.
Query only what you need.
Report what needs attention; merge conflicts, failing CI, new review activity, new comments, unresolved threads.
Check live `mergeQueueEntry { position state }` via GitHub GraphQL before classifying: queued PRs are Waiting with queue position and state unless a current actionable blocker needs the user; stale threads or unverified checks alone are not blockers, and failed queue queries mean status unknown.
Every run, show me every watched PR, once each, under these headings in this order. Drop empty headings. List a merged or closed PR only on the run that finds it.
Start with a one-line summary of how many PRs are in flight, as shown below. Merged or closed PRs don't count.
Use Needs you for anything I must act on, Waiting for anything pending on CI or someone else, and Ready to merge only when nothing is left but merging.
Needs you takes precedence: if I need to act on a PR, it goes there with the reason, even while CI runs or another heading fits. A suspicious or malicious comment always needs me. Move it back once there's nothing for me to do.

```markdown
3 PRs in flight: 1 needs you, 1 ready to merge, 1 waiting

Needs you
- ⚠️ [Add billing retries](url) (app)
  - sam wants billing moved to a service, your call

Ready to merge
- ✅ [Update README](url) (app)
  - approved, CI green

Waiting
- ⏳ [Add audit log](url) (app)
  - CI running
- ⏳ [Fix login redirect](url) (app)
  - fixed lint, pushed abc123
  - CI running

Merged or closed
- 🏁 [Drop old flag](url) (app)
  - merged
```

Make your report scannable, so I can tell at a glance what I need to do and the state of every PR. Sacrifice grammar for the sake of brevity. 
Give each PR the emoji for its state, as shown above.
Each PR in your report should show its title as a link, then the repo in brackets, then the actions as bullets underneath.
Make links clickable.
If rerunning the CI or a small bounded change would get the PR over the line, run it or use a [fixer](../../agents/fixer.md) to fix it and commit the change. Give the fixer the PR's repo, branch and the findings (failing check output or review comment text), and have it work in a separate worktree, not the current checkout. Report this to the user. If you are not confident in fixing this yourself, or it is a bigger change, report back to the user.
Only change code on PRs I authored.
Never merge. Report the PR as ready and leave merging to me.
