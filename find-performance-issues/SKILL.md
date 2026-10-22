---
name: find-performance-issues
description: Find low to medium effort changes that make a codebase measurably faster, such as N+1 queries, slow subqueries, missing indexes and repeated work, and rate each by effort and gain. Use when asked to find performance issues, quick wins, or why something is slow. Not for implementing the fixes.
---

# Find performance issues

Find changes that make a real code path at least 2x faster for low or medium effort. Change nothing.

1. Read repository instructions, then find hot paths: routes, controllers, jobs, serializers, views and code called in loops. If a path, feature or ticket is given, start there. Use `rg -n`; read only needed ranges.
2. Look for:
   - N+1 queries: associations or queries inside loops, views or serializers without eager loading.
   - Slow queries: correlated subqueries, a `count` or `exists?` per row, missing indexes on filtered, joined or ordered columns, loading records only to count, sum or pluck.
   - Repeated work: the same query, API call, file read or calculation done twice in one request or loop; missing memoization or caching.
   - Wasteful loops: O(n²) lookups a hash or set fixes, per-row writes a bulk insert or update fixes, slow work in a request that belongs in a job.
   - Heavy payloads: unpaginated lists, over-fetched columns or fields, large uncompressed assets.
3. Confirm each finding by reading its callers and the data size (schema, scopes, seeds, comments). Drop findings on rare paths, small data, or under 2x gain. Where a cheap read-only measurement exists (query log, `EXPLAIN`, benchmark), run it and cite the result.
4. Rate each finding:
   - **Effort**: Low (local change, under an hour) or Medium (several files or a migration, a day or less). Drop anything bigger.
   - **Gain**: 2x, 5x or 10x+ on the affected path, with the reason, for example "101 queries to 2". Mark unmeasured estimates with `*`.
5. Show one table sorted by gain descending, then effort ascending. Write locations as `path:line`.

| # | Location | Problem | Fix | Effort | Gain |
| --- | --- | --- | --- | --- | --- |

6. Below the table, list areas checked with no wins in one line. Do not implement fixes unless asked.
