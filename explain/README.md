# Explain

`explain` helps explain a ticket, file, or codebase concept in plain english.

It follows these steps:

1. Establishes what you want explained from a file, ticket, question, or the conversation.
2. Researches the relevant code and traces how the pieces connect.
3. Confirms any assumptions with you before delivering the full explanation.
4. Leads with the problem the code solves, then walks one concrete example (such as a real request URL) through numbered step headings with verified line links.
5. Explains why the pieces are arranged this way and ends with a clear next action.

Explanations are written for a developer new to the codebase: they define
domain terms and internal names, not general programming vocabulary. They stay
short, scoped to what you asked, and easy to skim in a terminal. The skill explains the code in the conversation without
changing it.

## Usage

After installation, provide a file path, ticket text or link, or a question about
the codebase. You can omit the input when the conversation already identifies
what you want explained.

### Codex

```text
$explain app/models/order.rb
$explain Explain the ticket in tickets/order-confirmation.md
$explain How does signing in work, and why are the pieces split this way?
```

### Claude Code

```text
/explain app/models/order.rb
/explain Explain the ticket in tickets/order-confirmation.md
/explain How does signing in work, and why are the pieces split this way?
```
