# Write Ticket

`write-ticket` writes short, precise Jira tickets that a developer new to the codebase, or a coding agent with no other context, can pick up and finish without asking questions.

It follows these steps:

1. Interviews you, either from scratch or about the gaps in an existing ticket. It asks a few numbered questions per round, each with a suggested answer.
2. Researches the relevant code and history.
3. Asks a second round of questions, based on what the code shows, to settle scope and defaults.
4. Drafts the ticket, cuts it to length, and rereads it as an agent would.
5. Saves the ticket as a Markdown file at the path you choose.

## Ticket format

Tickets follow `references/ticket_guide.md`. A typical ticket is 200–600 words and has an actionable title followed by these sections:

1. Summary
2. Context
3. Technical: the specific changes and the rules they must follow. Spikes also say what to look for and where.
4. Resources: omitted when there are none.
5. Acceptance Criteria: three to five checks, using links, commands or exact results, that a human or an agent can carry out alone.

Bug and spike titles use `[BUG]` and `[SPIKE]` prefixes. Jira tickets and pull requests are always linked and followed by a brief explanation of their relevance, for example:

```markdown
[ABC-1234](https://jira.example/browse/ABC-1234) (adds the API path)
[backend PR #1234](https://github.com/example/backend/pull/1234) (changes authentication for the endpoint)
```

## Usage

Start with whatever you know. The skill will interview you before it researches or writes anything. Useful starting information includes:

- What is happening now and why it is a problem.
- What outcome you want.
- Who is affected.
- Examples, reproduction steps, screenshots, designs, or related work.
- The repository containing the relevant code.

You do not need to know the technical solution. The skill researches the code, separates confirmed facts from assumptions, and asks for clarification before it saves the finished Markdown ticket.

### Codex

```text
$write-ticket Help me write a ticket for this work.
```

Codex may also select the skill automatically when you ask it to draft or improve a Jira ticket.

### Claude Code

```text
/write-ticket Help me write a ticket for this work.
```

Claude Code may also select the skill automatically when your request matches its description.
