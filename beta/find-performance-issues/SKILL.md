---
name: find-performance-issues
description: Find why a page, endpoint, job or query is slow, and find performance quick wins in a codebase. Sweeps the whole code path for candidates, then verifies the top few, explaining each issue in plain English with an estimated gain, the arithmetic behind it and a validation step. Covers N+1 queries, slow or spilling SQL, missing indexes, broken caching, missing memoization, repeated API calls, redundant job work and wasteful loops. Use when asked to find performance issues, audit a page, endpoint or job, explain why something is slow, or look for quick wins, even if the user only describes a symptom such as "the 30-day view takes 30 seconds". Not for implementing the fixes.
---

# Find performance issues

Find the changes that would make a real code path faster, explain each one so a developer new to the codebase can follow it, estimate the gain, and show how the estimate was checked. Change no repository files.

The aim is to find the issues an experienced engineer would fix after profiling in production. Those are often not dramatic: a cache that never hits, an aggregate that spills to disk, a method that recomputes on every call, a nightly job that redoes work nothing asked for. Missing a real issue costs more than reporting one that turns out small.

Work in two passes. The first pass is wide and cheap: read the whole path and list every candidate, without writing any scripts. The second pass is deep and narrow: verify only the top few. Breadth finds issues; depth proves them. Spending the budget on proof before the sweep is finished is the usual way real issues get missed.

## Pass 1: sweep (wide, cheap)

### 1. Find the path

Read the repository instructions first (`AGENTS.md`, `CLAUDE.md`, architecture docs).

Start from what the user names: a symptom, page, endpoint, job or ticket. A symptom is evidence:

- "Slow for 30 days, fine for 24 hours" means the cost grows with data size. Look at what scales with the range: rows read, rows expanded, loops over buckets, memory used by sorts and aggregates.
- "Slow even though we cache it" means the cache saves no work. Check what runs before the cache lookup and whether a hit really skips rendering.
- "Slow on a cold render" means look at everything a cache miss does, including content the user cannot see yet.
- "A job takes 30 minutes" means look at how much of the run does useful work, and what it does to the database while it runs.

If there is no symptom, pick the hot paths: the most-used pages and endpoints, and scheduled jobs over large tables.

### 2. Read every step

Follow the path end to end. For a request: route, controller and its callbacks, services, models, queries, serializers, the view, every partial, helpers, presenters and the layout. For a job: schedule, worker, every service it calls, every query and write. Use `rg -n` and read only the ranges you need, but read every file on the path. Issues hide at the boundaries, such as a controller that calls an API before the view checks its cache.

While reading, keep a call count. Note each method called from a template or loop, and how many times it runs per request or per run. A presenter method called from two partials, rendered once per row, runs 2 x rows times.

### 3. Check every file against these patterns

Go through the list for each file on the path. These are the usual causes, not the only ones.

**Database**
- N+1 queries: associations read inside loops, views or serializers without eager loading; a lookup by id per row (`Model[id]`, `find`) that one batched query could replace; an insert followed by a select that `RETURNING` would avoid.
- A `count`, `exists?` or query per row; loading records only to count, sum or pluck.
- Missing indexes on filtered, joined or ordered columns; `LIKE 'x%'` on a plain btree index.
- SQL that grows badly with range: correlated subqueries; `jsonb_array_elements` or `unnest` that expands many values per row; aggregates (`count(DISTINCT)`, `bool_or`, `bit_or`, `GROUP BY`) that carry wide columns, such as a whole JSONB row, into the grouping step. These can spill to disk once the data passes `work_mem`. PostgreSQL estimates 100 rows for set-returning functions, so its plan can be badly wrong. The usual fix is to select only the small fields first (for example in a `MATERIALIZED` CTE) and expand after.

**Caching**
- Work done before the cache lookup, so a hit still pays for it. In Rails views, `content = capture do ... end` followed by `cache(key) { concat(content) }` renders everything on every request. Use `cache`/`cache_if` around the work itself.
- API calls or queries in the controller whose results are only used inside a cached fragment.
- Data that is the same for every request (reference lists, schemes, countries) fetched on every request.
- Cache keys that change on every request (tracking params, request ids), or that miss values the output depends on.
- Cache options in the wrong place, for example `expires_in` inside the key array.

**Repeated work**
- Methods that recompute on every call: `@x = ...` where `@x ||= ...` was meant, or no memoization at all. Check presenters and models used by views closely: a predicate called once in a row partial and again in a modal or references partial is computed twice per item. For methods that can return `false` or `nil`, `||=` does not cache; use `defined?(@x)`.
- The same query, API call, file read or calculation done twice in one request or loop.

**Deferrable work**
- Content rendered on every page load that most users never open: hidden tabs, modals, collapsed sections. Rendering it lazily (on click, or in a separate request) removes its cost from the first render.
- Slow work in a request that belongs in a job.

**Jobs and batch work**
- A whole run that could be skipped: the job rebuilds everything on each run even when its inputs (source version, record set) have not changed. A fingerprint of the inputs, checked at the start, makes an unchanged run return in milliseconds.
- Rows rewritten when nothing changed: upserts with an unconditional `DO UPDATE`, saves that always touch a timestamp, audit or version rows written on every save.
- Per-row writes that a bulk insert or update fixes.
- One long transaction around the whole run: it holds locks and blocks vacuum, and can slow other traffic on the same database.

**Loops and payloads**
- O(n²) lookups: `find`, `select`, `index` or `include?` over a list inside a loop over the same list. A hash or set from `group_by` or `index_by` fixes it.
- Unpaginated lists, over-fetched columns, large payloads decoded and re-encoded on every request.

### 4. Write the candidate list

Before going deeper, write down every candidate in one line each: location, what is wrong, and a rough guess at the gain. Keep anything plausible. This list is the input to pass 2 and the source of the "Smaller wins" section; nothing on it gets thrown away.

Rank it: the most likely cause of the user's symptom first, then by expected gain. When you have no symptom, rank by gain on the hottest path.

## Pass 2: verify (deep, narrow)

Take the top 3 candidates. For each one:

1. **Confirm it.** Re-read the code and its callers. Check the call count and the data size, using schema, fixtures, VCR cassettes, seeds, comments, constants and production numbers from docs or commit messages.
2. **Estimate the gain** and show the arithmetic so the reader can check it: "3 calls per request to 1", "30 buckets x 30 days of rows to 1 pass", "101 queries to 2". Say which path the gain applies to: cache hits, misses, 30-day views only, unchanged nightly runs. Give a range when unsure and mark unmeasured estimates with `~`.
3. **Validate it**, choosing the cheapest check that settles the question:
   - **Traced:** the call count or data flow, with `path:line` references. Enough for most findings.
   - **Measured:** a small read-only benchmark, only when the gain is uncertain and a script can settle it in a few minutes. Model the pattern in plain Ruby with realistic sizes, or run `EXPLAIN (ANALYZE, BUFFERS)` if a database is already available. Do not start servers or install software. Put scripts in a scratch or temp directory, never in the repository. Show the command and the result.
   - **To confirm:** always give the exact check the user can run: the `EXPLAIN` query and what to look for (`external merge`, `Disk:`, `temp written`), the log line or metric to compare before and after, or the spec to add.

Say which level each finding reached. Do not present an estimate as a measurement.

For the remaining candidates, a traced call count or a one-line reason is enough.

## Report

Write in plain English for a developer new to the codebase. Use short sentences, one idea per sentence, and active voice. Explain the mechanism: why this code is slow, not only that it is.

Start with two or three sentences: what is most likely causing the slowness, and what you did (read-only analysis, benchmarks run, nothing changed).

Then the verified findings, in ranked order. For each, use a short numbered section:

- **Title**: what is wrong, in a few words, plus the gain and effort, for example "(~10x on 30-day views, low effort)".
- **Where**: `path:line` references.
- **Why it is slow**: the mechanism, in two to five sentences. Name the methods and say how often they run.
- **Fix**: what to change. Mention anything the fix must keep working, for example `content_for` calls that a cached block would skip.
- **Gain**: the estimate and its arithmetic.
- **Validation**: the level reached, the evidence, and the exact check to confirm it.

After the verified findings:

- **Other findings**: every remaining candidate from pass 1, one or two lines each, with location, fix and rough gain.
- **Checked, no issue**: one line listing what you read and found fine, so the reader knows what was covered.
- **Not performance, worth a look**: correctness bugs found on the way, such as a cache key that serves one user's data to another. Keep this short.
- **Suggested order**: which fixes to do first and why.

Do not implement fixes unless asked.
