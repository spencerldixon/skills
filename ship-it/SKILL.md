---
name: ship-it
description: Ship finished local work for review across one or more repositories, with GitHub pull requests written by pr-summary and a Jira ticket update. Use when asked to ship it, ship the work, open or raise the pull request for a ticket, or push the work for review. Not for drafting a PR description only; use pr-summary for that.
---

# Ship it

Turn the local work for a ticket into open pull requests, then tell Jira about them. Invoking this skill is the user's go-ahead to commit, push, open pull requests, comment on the ticket and move it. Stop and ask only where this skill says so.

Use the GitHub MCP for pull requests and the Jira (Atlassian) MCP for the ticket. Load deferred tools with tool search. If the GitHub MCP is unavailable, use `gh`. The Jira site is `https://transformuk.atlassian.net`.

Where this skill requires a decision, prepare the concrete scope or conflict document and follow [human-review.md](../references/human-review.md) to open it before asking. Invoking ship-it remains authorization for its stated actions; do not add another confirmation gate.

## 1. Find the ticket and the repositories

- **Ticket key**, such as `HMRC-1234`: take it from the user's message, the conversation or the current branch name. If there is none, ask for it. Never invent one.
- Read the ticket with the Jira MCP to confirm it exists. Use its title and description to name the branch.
- **Repositories:** the current repository, plus any others the user names or that you changed for this ticket in this session. Run `git status` in each. Skip a repository with no uncommitted changes and no commits ahead of its default branch.

Do steps 2 to 4 for each repository. Do step 5 once, after every pull request is open.

## 2. Branch

Find the default branch with `git symbolic-ref --short refs/remotes/origin/HEAD` (drop the `origin/`), or from the GitHub MCP.

- **On the default branch, or another long-lived branch** such as `main`, `master`, `develop` or `release/*`: run `git switch -c <name>`. This takes the uncommitted work with it. Name the branch `TICKETNUMBER-short-descriptive-name`: the key in capitals, then two to five lowercase words joined by hyphens, for example `HMRC-1234-show-address-save-error`. Use the same name in every repository for this ticket.
- **On any other branch:** stay on it. Do not rename it.
- **Detached HEAD, or a merge or rebase in progress:** stop and ask.

## 3. Commit

- Read `git status` and `git diff`. Stage the files that belong to this work by name. Do not use `git add -A` or `git add .`.
- Never stage secrets or local-only files, such as `.env` files, credentials, keys, logs or build output.
- If you cannot tell whether a change belongs to this work, ask. Leave unrelated changes uncommitted and list them in the report.
- Write the commit message as one plain-English sentence that says what the work does, for a teammate reading `git log`. For example: `Show an error when an address cannot be saved`. Use no ticket prefix, no type prefix such as `feat:`, and no body.
- If a commit hook fails because of this work, fix it and commit again. Otherwise stop and report. Never use `--no-verify`.
- If nothing is uncommitted but the branch has commits to ship, skip the commit.

## 4. Push and open the pull request

1. Run `git push -u origin <branch>`. Never force push. If the push is rejected, stop and report.
2. Look for an open pull request from this branch. If one exists, reuse its URL and do not open another.
3. Otherwise, use the `pr-summary` skill (`../pr-summary/SKILL.md` from this file) on this branch against the default branch. Give it the ticket key and the ticket URL, `https://transformuk.atlassian.net/browse/<KEY>`.
4. Take the title from its `text` block and the description from its `markdown` block. Send only the content inside the fences, never the fences.
5. Open the pull request with the GitHub MCP: owner and repo from `git remote get-url origin`, head is the branch, base is the default branch, not a draft. With `gh`, write the description to a file in the scratchpad and run `gh pr create --base <default> --title "<title>" --body-file <file>`.
6. Read the pull request back and check its formatting:
   - The title is `[KEY] Short explanation`.
   - The description starts with `## What:`, and each heading is on its own line.
   - Line breaks are real, with no literal `\n`.
   - No code fences wrap the description, and no HTML template comments remain.

   Fix any problem by updating the pull request.

If any repository fails in steps 2 to 4, stop before step 5 and report what was done. A second run reuses the pushed branches and open pull requests.

## 5. Update Jira once

1. Add one comment to the ticket, in this shape:

   ```markdown
   <One sentence that says what the pull request does.>

   - <repository name>: <pull request URL>
   ```

   With several pull requests, write one sentence for the whole change and list every pull request, one per line. Post one comment, never one per repository. If the ticket already has a comment with these links, do not post again.
2. Move the ticket to **In Review**. Get the ticket's available transitions and use the one whose target status is In Review. Never guess a transition ID. If the ticket is already In Review, skip this. If no transition leads there, leave the status and report the transitions that are available.

## 6. Report

End with only this:

```markdown
**Pull requests**
- <repository name>: <pull request URL>

**Jira:** https://transformuk.atlassian.net/browse/<KEY> (moved to In Review)
```

Replace "moved to In Review" with the reason when the ticket did not move. Add one line for anything left out, such as uncommitted unrelated changes or skipped repositories.

## Language

Write in Simplified Technical English.

Build the user's knowledge. When you use a concept, decision or file that may be new to them, say what it is and why it matters, in one sentence.

Be concise. Put the answer or decision first. Cut every word that does not help the user act or learn.
