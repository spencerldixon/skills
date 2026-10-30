---
name: preflight
description: Check that a repository is set up and can run its tests before implementation starts. Use before agent work, or when asked whether the local environment is ready.
---

# Preflight

Diagnose readiness for the intended checks, not an environment rebuild.

1. **Scope:** name the test/lint commands and their prerequisites. Reuse repo instructions already read; otherwise search/read relevant ranges. A general readiness request covers the documented local test stack; state that broader scope.
2. **Check once:** batch cheap read-only checks; retain exact commands/results.
   - Verify required runtime versions and dependencies (`bundle check`, `npm ls --depth=0`, or equivalent). Reuse an existing verified toolchain available to the worktree. Check availability before commands that auto-install; avoid unrelated inherited tools or per-worktree runtime builds.
   - Probe only required services. VCR/WebMock tests need no live backend unless setup says otherwise. Avoid starting the full stack for isolated tests.
   - Check disk. Below 2 GB is a warning; block if a documented minimum is unmet, a check cannot safely run or a required write fails. A warning authorizes neither cleanup nor installation.
   - Run one existing fast relevant spec once prerequisites pass, plus required lint/runtime smoke checks. Build assets only if required and setup is authorized; otherwise missing assets block readiness.
3. **Reuse:** passing evidence from this run remains valid while runtime, lockfiles, services/config and worktree inputs are unchanged. A new worktree needs its own dependency/smoke check. Repeat failed or invalidated checks, not the entire preflight. Implementation changes still require regression tests.
4. **Setup blocker:** report the exact error and smallest documented fix (or none found). An implementation request alone does not authorize runtime/dependency installation, asset builds or service provisioning. With explicit setup authorization, try one bounded documented fix and rerun the failed check. Source compilation, toolchain upgrades, destructive cleanup, undocumented work or more than about five minutes require a separate setup decision first. After one unsuccessful attempt, stop. Global toolchain changes need explicit authorization.

Report `ready` or `blocked` in at most 100 words: scope, smoke command/result, warnings and blockers/fixes. Save evidence in the caller's existing state note, not a separate report. Bound successful output; preserve failure diagnostics. `ready` covers only the stated checks, not the full stack.
