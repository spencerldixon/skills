---
name: ticket-writing
description: Interview the user, research the relevant code, and write or improve a Jira ticket in the team's preferred format before saving it as Markdown. Use for Jira ticket drafting and refinement, not for implementing the ticket or changing Jira itself.
---

# Ticket Writing

Create a Jira-ready Markdown ticket that another developer can pick up without prior knowledge of the service.

Before beginning the user-facing workflow, read [references/ticket_guide.md](references/ticket_guide.md) completely. Treat it as the ticket-writing rubric.

## Workflow

### 1. Interview the user

Begin by interviewing the user. Do not research the code or draft the ticket until the user has had an opportunity to provide context.

Use short, focused rounds of questions rather than one large questionnaire. Reuse information already supplied and ask only for missing details that could improve the ticket. Establish:

- The problem or opportunity, the current behaviour, and the desired outcome.
- Who is affected, how they use the service, and why the work matters.
- Whether this is ordinary delivery work, a bug, or a spike.
- Known facts, suspected causes, examples, reproduction steps, constraints, dependencies, and anything out of scope.
- Existing resources, including screenshots, designs, documentation, Jira tickets, pull requests, and URLs.
- What must be true when the work is done and what proof is expected.
- Which repository or repositories contain the relevant code.
- The Markdown output path. Suggest a slugified ticket title in the current directory when the user has no preference.

Do not force the user to answer questions that code research can answer. Once there is enough information to identify useful research starting points, move on to research.

### 2. Research the code

Research the relevant workspace read-only. If the repository is not discoverable, ask the user for its location.

- Read applicable repository instructions and focused documentation.
- Trace the current behaviour through relevant entry points, code, configuration, tests, schemas, and recent history.
- Find practical starting points, existing patterns, likely tests, constraints, and related work.
- Inspect referenced tickets or pull requests with available read-only tools when access permits.
- Keep research proportional to the ticket. Do not implement the change, edit product code, create Jira issues, or modify pull requests.

Maintain clear evidence boundaries:

- **Confirmed:** directly supported by code, tests, history, accessible links, or user-provided evidence.
- **Reported:** supplied by the user but not independently verified.
- **Suspected:** a plausible explanation that still needs investigation.
- **Open:** an unresolved decision or missing fact.

Never turn suspected or open information into a stated fact.

### 3. Clarify material gaps

After research, explain only the findings needed to resolve meaningful gaps. Ask focused follow-up questions when an answer could change the outcome, scope, implementation constraints, or acceptance criteria.

Do not block on optional detail. Preserve a genuine implementation question in the Technical section when resolving it is part of the ticket, but resolve product and scope decisions before finalising the ticket.

### 4. Draft the ticket

Use this Markdown structure:

```markdown
# <Actionable ticket title>

## Summary

## Context

## Technical

## Resources

## Acceptance Criteria
```

Follow the packaged guide closely:

- Prefix bug titles with `[BUG]` and spike titles with `[SPIKE]`.
- Explain the user and service context in plain English before technical detail.
- Write for a junior developer on their first day and define unfamiliar terms.
- Make the title understandable without opening the ticket.
- Include reproduction steps, known facts, suspected causes, constraints, implementation starting points, testing expectations, open questions, and out-of-scope boundaries when relevant.
- If no resources exist, retain the Resources section and say `No additional resources were supplied.`
- Use around three to five concise, specific, testable acceptance criteria unless the work genuinely requires a different number.
- Do not invent requirements, code behaviour, evidence, links, or resources.

### 5. Format ticket and pull request links

Every Jira ticket or pull request reference must be a Markdown link followed immediately by a short parenthetical explanation of why it is relevant:

```markdown
[ABC-1234](https://jira.example/browse/ABC-1234) (adds the API path)
[backend PR #1234](https://github.com/example/backend/pull/1234) (changes authentication for the endpoint)
```

Apply this rule throughout the ticket. Never write a bare identifier such as `ABC-1234` or `PR #1234`, and never provide a ticket or pull request link without the explanation.

Keep the explanation short and specific to its relevance to this ticket. Do not merely repeat the linked ticket or pull request title.

Resolve URLs from user input, repository remotes and history, or accessible read-only tooling. Do not guess a URL. If a relevant identifier has no confirmed URL, ask the user for it before finalising. Omit the reference only when the user agrees it is unnecessary.

### 6. Evaluate and revise

Before writing the file, evaluate the entire draft against [references/ticket_guide.md](references/ticket_guide.md). Revise it until every applicable check passes:

- The title is short, specific, actionable, outcome-led, and correctly prefixed.
- Summary states the current problem, why it matters, the requested change, and outcome in one or two sentences.
- Context teaches the necessary concepts, history, users, current behaviour, problem, and benefit in plain English.
- Technical gives practical investigation and implementation starting points while distinguishing facts, suspicions, and open questions.
- Resources contain useful material or explicitly state that none was supplied.
- Acceptance criteria describe a clear, testable done state and any required proof.
- Every ticket and pull request reference is linked and has a brief relevance explanation.
- The ticket is self-contained, concise, and free of invented claims.
- The language is aimed at a junior developer on their first day of work with no prior knowledge of the product.

Do not expose a mechanical score. If a material gap remains, return to clarification instead of saving an incomplete ticket.

### 7. Save and hand off

Write the final reviewed draft to the agreed `.md` path. Treat the request to use this skill as permission to create that one ticket file, but not to overwrite an existing file.

If the destination exists, stop and ask whether to overwrite it or use a different path. Do not silently replace it.

After saving, provide:

- A clickable link to the Markdown file.
- A one-sentence description of the ticket produced.
- Any intentionally retained open questions or unverified evidence; say explicitly when there are none.
