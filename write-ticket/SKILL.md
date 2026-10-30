---
name: write-ticket
description: Interview the user, research the code, and write or refine a short, precise ticket (story, bug or spike) that a developer new to the codebase, or a coding agent with no other context, can pick up and finish without asking questions. Starts from scratch or from an existing ticket, Jira issue or rough notes, and saves Markdown in the team's five-section format. Use for drafting, refining or tightening tickets, not for implementing them or changing Jira.
---

# Write Ticket

The ticket is the whole briefing. Whoever picks it up gets the ticket and the repository, and nothing from this conversation.

Write for two readers at once:

- **A junior developer on their first day in this codebase.** They know general programming and common tools. They do not know this product's domain language, internal names or history.
- **A coding agent.** It reads every word literally and acts on it. It fills gaps with guesses and follows asides as if they were instructions.

Both readers need the same ticket. It is short, and every sentence matters. It names the specific changes and the rules they must follow, and its acceptance criteria let the reader prove the work is done. Your job is mostly to decide what to leave out.

Read [references/ticket_guide.md](references/ticket_guide.md) before you start. It defines the sections, the length budget, the wording and the final checklist. You need no other file from this skill unless step 7 says so.

## 1. Find the starting point

**Refining an existing ticket.** The user may supply a file, pasted text, a Jira key or a link. Read it with the tools you have. Never infer a ticket's contents from its identifier. Then:

- Tell the user in two or three sentences what you understand the ticket to ask for. A wrong reading is cheaper to fix now than after research.
- Identify the gaps that only the user can fill, and ask about them in the interview.
- Keep every fact, link and decision from the original that the reader needs. If you think something in the original is wrong, say so to the user rather than dropping it quietly.

**Starting from scratch.** Ask what the problem is and what outcome the user wants, unless they have already said.

## 2. Interview the user

Interview the user before researching. Then research, and ask a second round of questions informed by the code. Two short rounds are usually enough.

- **Ask only what only the user knows:** the outcome, why it matters, who it affects, scope, decisions already made, constraints, links, and what proof of done they expect. Do not ask what the code, history or documentation can answer.
- **Keep rounds short:** three to five numbered questions, so the user can reply "1. yes 2. no, admins only".
- **Suggest an answer when you can,** for example "I'd suggest a new link that lasts 7 days and makes the old one stop working. OK?". Confirming a suggestion is faster than writing an answer from nothing.
- **Reuse what you already have.** Skip anything already answered.

By the end of the interview, know:

- The problem, the desired outcome, and why it matters.
- Who is affected.
- The ticket type: story, bug or spike. A spike is time-boxed investigation that produces findings, not a change to the product.
- Examples, reproduction steps, URLs and error messages.
- Decisions already made, and the reasons for them.
- Scope.
- Useful links: tickets, pull requests, designs and screenshots. If Slack notifications are in scope, ask for a permalink to a representative message.
- What proves the work is done.
- The repositories, if you cannot find them yourself.
- The output path. If the user has no preference, use `ticket.md` in the work folder from [vault.md](../references/vault.md).

**When the user does not know.** Never fill a gap silently. Close it in this order:

1. Research it.
2. Propose a sensible default in the next round, and write it into the ticket as a plain requirement once the user agrees.
3. If it is still unknown and it matters, ask who decides. Record it as an open question with a default to use until someone answers. If the main questions are all open, the work is probably a spike, so suggest one.

The aim is a ticket with few or no open questions.

## 3. Research the code

Research read-only. Do not change product code, create Jira issues or modify pull requests.

- Read repository instructions such as `AGENTS.md`, `CLAUDE.md` and `README.md`. They often hold constraints the reader must follow.
- Trace the current behaviour through the entry points, code, configuration and tests.
- Check the history for related work, or for work already done, partly done or reverted.
- Find what the reader needs: the one place to make each change, the pattern to copy, the rules that constrain the change, and the commands that prove it works. Take commands from repository documentation or CI configuration; do not invent them.
- Verify every path and line number you will cite.

Keep track of what you have confirmed and what you only suspect. In the ticket, write confirmed facts as plain statements. Put suspicions under "Suspected cause". Never present a guess as a fact.

Research efficiently. Every tool call adds a turn, and every turn re-reads everything gathered so far, so a large file dump early on is paid for again on every later turn.

- **Batch independent reads.** Make them as parallel tool calls or in one shell command, not one at a time.
- **Search, then read ranges.** Find symbols with `rg -n`, then read only the lines around them, for example `sed -n 40,90p`. Read a whole file only when it is short or you need all of it.
- **Bound history.** Use `git log -n 20 --oneline -- <path>`, or `--grep`, rather than an open-ended log.
- **Stay in the repositories that matter.** Do not read installed gems, packages or unrelated projects unless the ticket depends on them.
- **Stop when you can name** where each change goes, the rules it must follow, and the commands or checks that prove it. More than that helps you choose what to say, but very little of it belongs in the ticket.

## 4. Ask the follow-up round

Share only the findings that change a question, for example "the expired invite is still in the database, but the settings page only lists pending ones". Then ask about the gaps the research exposed. Settle product and scope decisions now, including any default you plan to write as a requirement.

## 5. Draft the ticket

Write the ticket as the guide describes. Do not invent requirements, behaviour, evidence, links, people or resources.

### Ticket and pull request links

Every Jira ticket or pull request must be a Markdown link, followed by a short note in brackets saying why it is relevant:

```markdown
[ABC-1234](https://jira.example/browse/ABC-1234) (adds the API path)
```

Never guess a URL. Take URLs from the user, repository remotes or history, or read-only tools. If you do not have a URL for an identifier that matters, ask for it.

Link code with the repository's web URL when you know it, for example a GitHub `blob/<commit>/path#L12` link. Otherwise use a repository-relative path with a line number.

## 6. Cut, then read it cold

Shorten the draft first, using the guide's length budget and its "Before saving" checklist. Then reread it as the coding agent with only this ticket and the repository:

- Would you know what to change, which rules to follow and when to stop?
- What would you have to guess? Fix each guess in the fewest words, or take it back to the user.
- Could you prove each acceptance criterion yourself?

Do not show the user this checklist.

## 7. Save and hand off

Write the ticket to the agreed `.md` path. Using this skill gives permission to create that one file. It does not give permission to overwrite an existing file. If the path exists, ask whether to overwrite it or use another path. Only in that case, read and follow [show-to-human.md](../references/show-to-human.md) for the decision.

Then give the user:

- A clickable link to the file.
- One sentence describing the ticket.
- Any open questions or unverified claims left in the ticket, or a statement that there are none.
