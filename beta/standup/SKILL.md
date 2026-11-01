---
name: standup
description: Draft a short standup update from recent work when asked for a daily update or standup notes; does not post it.
model: sonnet
---
Use the requested period; otherwise cover work since the previous working day in the user's timezone, including Friday for a Monday update.
Read available commits, PRs, ticket activity and work notes for that period; use author identity and timestamps to isolate the user's work. Bound each history read to 20 commits and disclose truncation.
Group by outcome or ticket, not commit; distinguish implemented, awaiting review and merged work. Do not count the same change twice or claim team activity as the user's.
Draft Yesterday / Today / Blockers in first person, normally six bullets total or fewer; derive Today from explicit plans or remaining work, mark inferred plans, and disclose missing sources instead of inventing progress or saying no blockers. Follow [language.md](../../references/language.md). Return the draft without posting it.
