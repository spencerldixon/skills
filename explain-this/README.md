# Explain This

`explain-this` helps explain a ticket, file, or codebase concept in plain english.

It follows these steps:

1. Establishes what you want explained from a file, ticket, question, or the conversation.
2. Researches the relevant code and traces how the pieces connect.
3. Confirms any assumptions with you before delivering the full explanation.
4. Explains who uses the feature, why it exists, and how it works through numbered steps, practical examples, and verified line references.
5. Flags unknowns with specific questions and suggested people or roles to ask.

Explanations use plain English, define acronyms and unfamiliar terms, and build
from first principles. Short sections and descriptive headers make them easy to
skim and revisit. The skill explains the code in the conversation without
changing it.

## Usage

After installation, provide a file path, ticket text or link, or a question about
the codebase. You can omit the input when the conversation already identifies
what you want explained.

### Codex

```text
$explain-this app/models/order.rb
$explain-this Explain the ticket in tickets/order-confirmation.md
$explain-this How does signing in work, and why are the pieces split this way?
```

### Claude Code

```text
/explain-this app/models/order.rb
/explain-this Explain the ticket in tickets/order-confirmation.md
/explain-this How does signing in work, and why are the pieces split this way?
```
