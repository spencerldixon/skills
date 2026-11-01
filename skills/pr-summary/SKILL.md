---
name: pr-summary
description: Write a pull request title and GitHub-ready Markdown summary from the actual changes, with an optional Jira ticket number. Follow the included What, Why, Ticket, and Risk template. Write short, plain-English summaries a junior developer can follow, based on ASD-STE100 Simplified Technical English principles. Use for drafting or revising PR descriptions, not for creating tickets or publishing PRs.
argument-hint: "[ticket-number]"
model: sonnet
effort: medium
allowed-tools: Bash(git status *) Bash(git diff *) Bash(git log *) Bash(git show *) Bash(git merge-base *) Bash(git branch *) Bash(git rev-parse *) Bash(gh pr view *) Bash(gh pr diff *)
---

# PR Summary

Write a PR title and description that a reviewer can read in under a minute, and that a junior developer new to this codebase can still follow.

Read [references/template.md](references/template.md) before drafting. It defines the output sections and the deployment risk criteria. Use the risk guidance to assess the change; do not copy the guidance or HTML comments into the output.

## Establish the scope

Accept an optional Jira ticket number, such as `HMRC-1234`. Also accept a ticket link or text, a PR link or number, a branch, or a supplied diff. Use the current conversation and repository when no change is specified.

- Reuse information already supplied. Do not ask for a ticket number when none is given; small PRs often have no ticket. A ticket number in the branch name counts as supplied.
- For an existing PR, use its actual target branch and diff. For a local branch, find its intended target and compare from the common ancestor; do not assume `main` without checking.
- Check the working tree first. Leave unrelated staged, unstaged, and untracked changes out. Include uncommitted work only when it is part of the request, and do not describe it as committed.
- If the target or scope is still unclear, ask one focused question.
- Read the ticket through available read-only tools when one is supplied. Never infer ticket contents from its number.

Research and draft only. Do not edit code, commit, publish a PR, or update GitHub or Jira unless separately asked.

## Read the evidence

Read the complete diff and enough surrounding code to know:

- What this part of the product does, and what changes for users or maintainers.
- What the change touches in practice: behavior, configuration, data, dependencies, tests.
- What could fail in production and how easily the team can undo it.

Follow callers when a changed interface affects other code. Keep research proportional: a one-line dependency bump needs a glance at the changelog or lockfile, not a codebase tour.

Describe what the diff implements, not what the ticket asks for. If they differ, say what this PR covers. Tests in the diff show intended behavior; they do not prove a test run passed. Claim test results, performance gains, or compatibility only when you have evidence.

## Write for the reader

The reader is a developer who knows Ruby, Rails, web services, and common tooling, but is new to this product and this team. So:

- Give context only where it explains this change. Do not introduce the product, the service, its users, or the team; the reader works here. "XI imports TARIC files" helps if the PR changes the import. "The Online Trade Tariff is a public HMRC service" never does.
- Explain domain terms and uncommon jargon (for example "TARIC", "oplog", "declarable") in a few words at first use. Do not explain general engineering concepts such as a Gemfile, a background job, or a migration.
- Expand an acronym only when you know its meaning. If you do not, describe the term by its role from the evidence instead, for example "the QRS report (the weekly export that finance reads)". Never guess an expansion, and never leave an unfamiliar term unexplained.
- Lead with behavior, then implementation. Name a file, class, or metric only when the reviewer needs it to check or act on the change.

Write in plain, direct English, following the principles of ASD-STE100 Simplified Technical English:

- Short sentences (aim for under 20 words) in active voice, with a clear actor.
- One idea per sentence. One term per concept, used consistently.
- Simple verb forms and concrete nouns. No idioms, filler, or long noun stacks.

The goal is clarity, not compliance. Prefer a natural sentence a colleague would write over a stilted one that follows a rule to the letter. Keep this guidance out of the PR output.

## Keep it short

Length should match the change, not the effort spent researching it. Every sentence should tell the reviewer something they need. Cut restatements, background they already know, and anything visible from the file list.

Rough budgets for the full description (excluding headings):

- Trivial change (dependency bump, copy fix, config tweak): 40–80 words. One-sentence What, one bullet or none, one-sentence Why.
- Typical change: 100–200 words. What has two to five bullets.
- Large or high-risk change: up to about 300 words. Spend the extra words on Why and Risk, not on listing edits.

When over budget, cut implementation detail (identifiers, namespaces, spec case lists) and background first. Keep the reasons and effects; they are what the reviewer cannot get from the diff.

## Create the title

With a ticket: `[TICKET_NUMBER] Short explanation of what this PR does`, for example `[HMRC-1234] Show an error when an address cannot be saved`.

Without a ticket, omit the prefix. Do not use `[N/A]` or invent a number.

Use a short action phrase that names the behavior that changes. The title should make sense without the description. Avoid vague titles such as "Fix issue" or a bare class name.

## Fill the description

Keep the template's headings, in order: `## What:`, `## Why:`, `## Ticket:`, `## Risk:`, with the labels `**Risk level:**` and `**Reason for rating:**`. Do not add sections unless asked.

**What:** one sentence on what the PR achieves, then bullets for the practical changes. Each bullet is one concrete change in behavior, configuration, data, or tests, in one or two short sentences. Group related edits; do not list every file.

A bare change invites the questions "is that intended?" and "so what?". When a reviewer could ask either, answer it in the same bullet with a short reason or effect. This matters most for anything that looks like a removal, a skipped step, or a regression: say why it is correct, or the reviewer will suspect a bug. For example, "XI sends no sync age from Sunday to Tuesday, because TARIC publishes no files on those days" rather than "XI sends no sync age from Sunday to Tuesday."

**Why:** open with the main motivation in the first sentence, for example "The team is removing New Relic." Then add only the context needed to see why this change solves it, and what is better afterwards. Make it understandable without the ticket. Do not repeat the What bullets, say "required by the ticket", or invent customer impact for internal work. If the reason is not in the evidence, say so briefly or ask, rather than inventing one. Use a before-and-after example only when the behavior change is hard to picture.

**Ticket:** `[TICKET_NUMBER](url)` when the URL is supplied or known from trusted project context. Never guess the Jira host. With only a number, write the number and "Link unavailable". With no ticket, write `N/A`.

**Risk:** choose exactly one of `🟢 Green`, `🟠 Amber`, `🔴 Red` using the template. Use the highest category that applies; a small diff or passing tests do not lower it. Missing evidence is not proof of low risk.

Under `**Reason for rating:**`, write one or two sentences that name the main risk, or why the impact is limited. Mention the recovery path or an unresolved check when it explains the rating. For Amber, note that a team discussion is needed before merge. For Red, note that explicit approval from Thor or Neil is needed before merge. Avoid generic claims such as "safe change" or "tests pass".

## Example

A typical-size result. Match this density, not its content.

```text
[HMRC-1234] Show an error when an address cannot be saved
```

```markdown
## What:
Users now see an error message when the address form fails to save, instead of a blank page.

- The address controller re-renders the form with the validation errors when the save fails.
- The controller no longer logs the full address on failure, because the log is not a safe place for personal data.
- A new request spec covers a failed save.

## Why:
Traders could not tell why their address did not save. When they entered an invalid postcode, the save failed silently and the page went blank. Now the form stays on screen and shows which field to fix.

## Ticket:
HMRC-1234 (Link unavailable)

## Risk:
**Risk level:** 🟢 Green

**Reason for rating:**
The change only affects the failure path of one form and does not touch stored data. A revert restores the old behavior.
```

## Return copyable Markdown

Return the title in one fenced `text` block and the description in one fenced `markdown` block, ready to paste into GitHub. No preamble, follow-up offers, drafting notes, template comments, or risk guide.

Before returning, check:

- The title names the actual change and uses the ticket prefix correctly.
- Every claim is backed by the diff, ticket, or code you read.
- Why opens with the main motivation. No bullet leaves the reviewer wondering if a change is a bug.
- Every unfamiliar term or acronym is explained at first use, and no product introduction is included.
- The length fits the size of the change. Cut anything the reviewer would skim past.
- Risk has one rating and a one- or two-sentence reason grounded in the template.
- No placeholders or extra sections remain.
