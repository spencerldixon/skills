---
name: autopilot
description: Run an autonomous orchestrator loop that picks up Jira tickets, runs the engineer workflow for each in its own worktree and Rex tab, opens draft pull requests, and watches them through CI and review. Run it under /loop. Never merges.
---

# Autopilot

Each run is one round: watch the work in flight, then start new work if there is room. Run it under `/loop autopilot` to repeat. Each ticket runs `engineer` in pi, in its own worktree and Rex tab, and stops in that tab when it needs the user.

## Settings

No more than 2 tickets in flight.

At most 2 tickets in flight, the current repository plus any the user names, and the state file `autopilot.md` and stop file `STOP` at the paths in [vault.md](../references/vault.md).

For tickets this skill picks from the `find-work` Auto bucket only, invoking this skill authorizes: assigning them to the user, moving them to In Progress, creating branches and worktrees, starting pi in Rex tabs, and committing, pushing, opening draft pull requests and marking them ready through `engineer`, `ship-it` and `watch-pr`. Never merge, force push, delete branches, rebase a pushed branch, or touch any other ticket.

## 1. Start the round

1. If the stop file exists, report "Stopped: stop file present" and end the round. Under `/loop`, end the loop too.
2. Read the state file. Create it when missing, as a table with the columns Ticket, Summary, Repo, Stage, PR, CI, Window, Work folder, Last event and Updated. Stages: `engineering`, `pr-open`, `ready-to-merge`, `needs-you`, `done`, `skipped`.
3. On the first round only: check `gh auth status` and `command -v pi`, load the Jira (Atlassian) and `PushNotification` tools with tool search, and get the user's Jira account ID with `atlassianUserInfo`. If any check fails, report it and stop.

## 2. Watch each ticket that is not done or skipped

- **`engineering`:** a pull request from the branch (`gh pr list --head <branch> --state all --json url`) moves it to `pr-open`. Park it (see Park a ticket) when the last line of `<Work folder>/steps.md` starts with `waiting:`, when nothing changes for 60 minutes (with the output of `rex capture -s "$REX_SESSION" -w <Window> --trim | tail -40`), or when the window is gone from `rex window ls -s "$REX_SESSION"` and there is no pull request ("session ended without a result").
- **`pr-open` and `ready-to-merge`:** run `watch-pr` (`../watch-pr/SKILL.md`) with the PR URLs, the worktree path, the work folder and the ticket key. Set the stage from its result. On `merged`: close the window with `rex window close`, run `git worktree remove <path>` without `--force` (if it fails, leave it and record why), and set the stage to `done`.
- **`needs-you`:** the user answers in the ticket's tab. When `steps.md` gets a new line after the park, set the stage back to the one in brackets. A ticket the user drops, unassigns or closes becomes `done`; leave its worktree, branch and tab for the user.

## 3. Start new work

1. Count the rows that are not `done` or `skipped`, including `needs-you`, so a stuck loop stops picking up work. If the count is at the limit, start nothing. Otherwise run `find-work` (`../find-work/SKILL.md`) in list mode, and take the first `auto` ticket not in the state file.
2. Read the ticket and decide which repository it belongs to. If the ticket and the code do not make it clear, skip it and record why in the round report.
3. Check the ticket again in a new subagent that has seen no other ticket. `find-work` scores many tickets in one pass and rates its own certainty, and both make scores less reliable. Give the subagent only the ticket key, the repository path and these questions. Ask for `yes` or `no` and one line of evidence for each:
   - Does the ticket have acceptance criteria that a test or command can check?
   - Does it say which behaviour must change, and where?
   - Are all questions in its description and comments answered?
   - Can the work be done without a product, design or copy decision?
   - Is the change outside the High risk areas in `find-work` step 4?

   If any answer is `no` or unsure, add a row with the stage `skipped` and the failed question in **Last event**, then take the next `auto` ticket from the same list. A wrong pick wastes a whole run, and a skipped ticket costs nothing. To let a later round try a skipped ticket again, the user deletes its row.
4. Assign the ticket to the user and move it with a transition whose target is In Progress. Read both back. If either fails, skip the ticket.
5. Name the work. **Summary:** two to five words from the title, in sentence case, for example `Show address save error`. **Branch:** `<KEY>-<summary as lowercase words joined by hyphens>`. **Worktree:** `<repo parent>/.worktrees/<repo>/<branch>`. **Work folder:** from [vault.md](../references/vault.md).
6. Create the worktree from the latest default branch, and open the ticket's tab without taking focus:
   ```sh
   git -C <repo> fetch origin && git -C <repo> worktree add -b <branch> <worktree> origin/<default>
   rex window new -s "$REX_SESSION" "<KEY> <Summary>" --focus=false --keep-open --json -c <worktree> -- \
     pi --name "<KEY> <Summary>" "/skill:engineer <KEY>. Approved in advance: the spec, and shipping with ship-it --draft. Skip the walkthrough."
   ```
7. Record the window ID from the JSON output, and add a row with the stage `engineering`.

## 4. Park a ticket

Set the stage to `needs-you`. In **Last event**, write the reason and the stage it came from in brackets, for example `waiting: which endpoint? (engineering)`. Send one push notification per reason: `<KEY> needs you in tab "<KEY> <Summary>": <reason>`. The user answers in the tab, so do not answer for them, comment on Jira or wait. Leave the worktree, branch and tab in place.

## 5. End the round

Write the state file. Report one line per ticket that changed, one line with the totals by stage, and each `needs-you` ticket with its tab name and reason. Send a push notification when a ticket reaches `ready-to-merge`. Under `/loop`, wait about 10 minutes while a ticket is `engineering` or CI is running, and about 30 minutes when nothing is moving. Follow [language.md](../references/language.md): keep lines short and put the ticket key first.
