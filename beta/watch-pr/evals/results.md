# Watch PR evaluation

The revised skill was evaluated through an independent agent using the current runtime's configured model. No named model or external model CLI was required. These are tabletop decisions, not live PR workflow tests.

| Scenario | Assertions met |
| --- | --- |
| Stale green CI from an older commit | 4/4 |
| Teammate changes the branch before commit | 5/5 |
| Repeated and edited review comment | 4/4 |
| Interrupted push already completed remotely | 5/5 |
| Configured model with no override, gh, Jira or scheduler | 5/5 |

The reviewer received only the final skill and raw fixtures, without expected answers. Its responses were manually scored against all 23 assertions in `evals.json`. It correctly used the available connector and configured model, reported one-shot operation without a scheduler, and preserved the repair and CI safeguards.

The provider-independent runner was also checked for stdin delivery, nonzero evaluator exits, empty responses and stopping further invocations after an error. Synthetic transport checks were not scored as model evaluations. Frontmatter, links, the 18-line limit and scoped whitespace checks passed.

Prepare requests without invoking a model:

```sh
python3 beta/watch-pr/evals/run.py --prepare-only
```

Evaluate the prepared requests using the host's agent tools, or supply a tool-disabled evaluator command accepting stdin with `--command` as the final option. The chosen runtime owns tool restrictions, model selection and spending controls. The runner has no provider or model default; it stores outputs in a temporary directory and never automatically scores a response as a pass.

## Local execution with fake GitHub

Native watcher and fixer agents ran the skill against `local_fixture.py`, temporary repositories and local bare Git remotes. GitHub responses were simulated. Repairs, regression tests, lint, commits, pushes and state writes were real local operations. No PR was opened and no GitHub network operation was performed.

| Scenario | Observed result |
| --- | --- |
| Stale green CI | Remote unchanged; draft retained; current-head CI awaited |
| External branch update | Requested fix already present remotely; pending patch preserved exactly; no duplicate commit |
| Seeded interrupted-push state | Existing remote commit reconciled; attempt count remained 1; CI pending |
| Failed CI plus new review comment | One scoped fix commit and regression test; tests and lint passed; local remote SHA verified |
| Unchanged next round | Remote SHA, event log and repair count unchanged |
| Edited review comment | One additional regression-test commit; all 3 tests and lint passed; count advanced to 2 |

An observational pre-receive hook on the final local push confirmed the new intended SHA, pushing phase and attempt count were already persisted before the remote received the commit. Both repair pushes left clean worktrees and retained the draft with CI pending.

Create another isolated fixture in a new directory:

```sh
python3 beta/watch-pr/evals/local_fixture.py setup /tmp/watch-pr-sandbox
python3 beta/watch-pr/evals/local_fixture.py gh /tmp/watch-pr-sandbox/lifecycle pr view fixture
```

Run the host's watcher agent once per case, supplying its repository and `work` folder. Route all GitHub calls through the fake service command above, allow only local Git remotes, and prohibit real connectors, networking and writes outside the fixture. Capture state, tool calls and emitted updates. The fixture controller can introduce the next event:

```sh
python3 beta/watch-pr/evals/local_fixture.py advance /tmp/watch-pr-sandbox/lifecycle failure
python3 beta/watch-pr/evals/local_fixture.py advance /tmp/watch-pr-sandbox/lifecycle edited-comment
```

Run separate watcher rounds between events, including an unchanged round after the first repair. The controller does not itself run or grade the watcher. Setup, event transitions, unsupported-operation rejection and protection against overwriting existing fixtures were also checked locally.

Real GitHub authorization and API behavior, hosted CI, scheduling, lock enforcement and recovery from an actual process termination remain untested. These runs do not establish reliability across models or runtimes.
