---
name: preflight
description: Check that a repository can run its tests before implementation starts. Use before agent work, or when asked whether the local environment is ready.
---

# Preflight

Find what blocks work, fast. Change nothing unless setup is authorized.

1. Read repository instructions (`AGENTS.md`, `CLAUDE.md`, README) for tool versions, services, and the test command. Use `rg -n`; read only needed ranges.
2. Run each check and record the command and result:
   - Tool versions match the version files (`mise current` or equivalent).
   - Dependencies are installed (`bundle check`, `npm ls --depth=0`, or equivalent).
   - Each documented service (database, cache, search) responds on its documented host and port.
   - Free disk space is at least 2 GB.
   - If the checks above pass, one existing fast spec file passes with the documented test command.
3. For a failure, find the documented fix. Run it only if setup is authorized, then repeat the check.

Report `ready` or `blocked`, each failed check with its exact error and documented fix, in at most 100 words.
