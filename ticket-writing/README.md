# Ticket Writing

`ticket-writing` is a skill for creating clear, self-contained Jira tickets in a preferred format.

It follows these steps:

1. Interviews you to understand the problem, users, outcome, constraints, and definition of done.
2. Researches the relevant code and history for confirmed context and implementation starting points.
3. Asks follow-up questions when important information is still missing.
4. Drafts and reviews the ticket against the packaged `ticket_guide.md`
5. Saves the finished ticket as a Markdown file at the path you choose.

## Ticket format

Tickets are written against the template and guidance in `ticket_guide.md`

Tickets contain an actionable title followed by these sections:

1. Summary
2. Context
3. Technical
4. Resources
5. Acceptance Criteria

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
$ticket-writing Help me write a ticket for this work.
```

Codex may also select the skill automatically when you ask it to draft or improve a Jira ticket.

### Claude Code

```text
/ticket-writing Help me write a ticket for this work.
```

Claude Code may also select the skill automatically when your request matches its description.
