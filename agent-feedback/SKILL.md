---
name: agent-feedback
description: Record lessons from agent work and suggest what would help the next agent. Use at the end of a planner, implementer, reviewer, or engineer job.
---

# Agent feedback

Record only what would change how the next agent works. No entry is better than a generic one.

Append at most three entries to `feedback.md` in the artifact directory:

```markdown
- **<role>, <type>:** <what happened, with evidence: `path:line`, command, or error>
  **Suggest:** <exact line to add or change, and the file it belongs in>
```

Types: `repo-fact` (true but not discoverable from code), `instruction` (a skill or repository instruction was wrong or missing), `tool` (a script, command, or fixture would have saved work), `process` (a workflow step was wasted or missing).

Do not edit instructions or skills. Do not record secrets, personal data, or facts the repository already states.
