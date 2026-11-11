---
name: preflight
description: Check that a repository can run its intended tests, and stop costly setup detours. Use before implementing, fixing or testing code; when a test command fails for an environment reason such as a wrong runtime, missing gems or a stopped service; or when asked whether the local environment is ready.
---

Prove the intended checks can run. Leave the environment as you found it.

1. **Scope:** name the test and lint commands from repo instructions already read. A general readiness request covers the documented local test stack. Probe only what those commands need: VCR/WebMock tests need no live services.
2. **Probe:** in one batched command, check only the following in scope:
   - Runtimes, dependencies (`bundle check`, `npm ls --depth=0`) and services.
   - Disk: under 2 GB is a warning.
   - Freshness: `git fetch -q origin && git rev-list --count HEAD..origin/HEAD`; any commits behind is a warning.
   - Schema: the newest `db/migrate` timestamp is in the test database's `schema_migrations`, under any `search_path` in `config/database.yml`; a pending or unverified migration blocks.

   Leave out-of-scope tools and stopped services unprobed. Use read-only checks that cannot auto-install.
3. **Smoke:** once the probes pass, run one fast existing spec once. The evidence holds while runtime, lockfiles, services, config and worktree stay unchanged. A new worktree needs its own check.
4. **Blocked:** report the exact error and the smallest documented fix, or say none was found. Install, build or start anything only with explicit setup authorization: one bounded attempt, rerun the failed check, then stop.

Report `ready` or `blocked` in under 100 words: scope, smoke command and result, warnings. Quote failures and omit passing logs. Return evidence to the caller; update its existing wiki handoff only when the result matters for continuation. Routine passing checks stay in session context. Follow [vault.md](../../references/vault.md): no separate local report or save-permission prompt.
