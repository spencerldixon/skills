---
name: pr-summary
description: Write a pull request title and GitHub-ready Markdown summary from the actual changes, with an optional Jira ticket number. Follow the included What, Why, Ticket, and Risk template. Explain the change for a junior developer on their first day and use ASD-STE100 Simplified Technical English for technical concepts. Use for drafting or revising PR descriptions, not for creating tickets or publishing PRs.
---

# PR Summary

Write a title and description that a junior developer can understand on their first day. Assume no prior knowledge of the product, code, or feature.

Read [references/template.md](references/template.md) completely before drafting. It defines the output sections and deployment risk criteria. Use its risk guidance to assess the change; do not copy the guidance or HTML comments into the completed description.

## Establish the scope

Accept an optional Jira ticket number, such as `HMRC-1234`. Also accept a ticket link or text, a PR link or number, a branch, or a supplied diff. Use the current conversation and repository when no change is specified.

- Reuse information already supplied. Do not ask for a ticket number when none is provided; small PRs may have no ticket.
- Identify the changes that belong to this PR. For an existing PR, use its actual target branch and diff. For a local branch, identify its intended target and compare from their common ancestor; do not assume the target is `main`.
- Inspect the working tree before research. Keep unrelated staged, unstaged, and untracked changes out of the summary. Include uncommitted work only when it is part of the requested summary, and do not describe it as already committed.
- If the target or intended changes remain unclear, ask one focused question. Continue research that does not depend on the answer.
- Read the ticket through available read-only tools when a ticket is supplied. If access is unavailable, use supplied ticket text and repository evidence. Ask for missing context only when it materially affects the explanation; never infer ticket contents from its number.

Research and draft only. Do not edit product code, create commits, publish a PR, or update GitHub or Jira unless separately requested.

## Read the evidence

Read applicable repository instructions, the complete relevant diff, and enough surrounding code and documentation to establish:

- What this part of the product does and who uses it.
- What happened before the change and what happens after it.
- What changed in practice, including relevant configuration, data, dependencies, and tests.
- What can fail when the change reaches users and how easily the team can undo it.

Follow relevant callers and consumers when a changed function, field, or interface affects other code. Keep research proportional to the change.

Use the diff to describe what the PR actually implements. Use the ticket and supplied context to explain the problem and intended benefit. Do not claim that the PR completes every ticket requirement unless the evidence supports that claim. If the ticket and implementation differ, explain the actual scope.

Distinguish observed results from expectations. Tests in the repository show intended behavior; they do not prove a test run passed. Mention successful tests, performance gains, compatibility, or deployment results only when supporting results are available. Do not run tests merely to generate a summary; report material gaps when they affect the risk rating.

## Write for the reader

Introduce the product's relevant purpose, user, and workflow before relying on their names. Explain unfamiliar product terms and technical concepts at first use. Expand necessary acronyms and explain what they mean; omit unnecessary acronyms. Never guess an internal acronym's meaning.

Describe behavior before implementation details. For example, explain that a background job is work the application queues to run later before discussing a named job class. Use file or class names only when they help the reader understand the change, and explain their role. Avoid file inventories and unexplained internal shorthand.

Use ASD-STE100 Simplified Technical English for technical explanations. Apply its writing rules and controlled vocabulary, not only a plain-English tone. The [official standard](https://www.asd-ste100.org/assets/files/ASD-STE100_ISSUE9.pdf) provides the rules and dictionary; consult it for uncertain usage.

- Use approved words with their approved meanings and parts of speech. Use permitted technical nouns and verbs for established software terms.
- Use one term consistently for each concept. Preserve exact code identifiers when needed, and explain them separately.
- State who or what performs each action. Use passive voice in descriptions only when the actor is unknown.
- Keep descriptive sentences within 25 words. Keep instructions within 20 words, with one action per instruction.
- Give each sentence one subject and each paragraph one topic. Introduce information gradually; use no more than six sentences per paragraph.
- Use direct verbs, simple verb forms, and explicit connections between cause and result. Avoid idioms and long strings of nouns.

These reminders do not replace the standard's full rules and dictionary. Do not claim certified or verified STE compliance without the corresponding review. Keep this writing guidance out of the PR output.

## Create the title

With a ticket, use exactly this pattern:

`[TICKET_NUMBER] Short explanation of what this PR does`

For example: `[HMRC-1234] Show an error when an address cannot be saved`.

Without a ticket, omit the bracketed prefix entirely. Do not use `[N/A]` or invent a ticket number.

Use a short action phrase that names the affected behavior and outcome. The title must explain the change without the description. Avoid vague titles such as “Fix issue,” “Updates,” or an unexplained class name. Describe the implemented scope even if the ticket's title is broader.

## Fill the description

Keep the reference template's headings, punctuation, and order: `## What:`, `## Why:`, `## Ticket:`, and `## Risk:`. Retain the labels `**Risk level:**` and `**Reason for rating:**`. Do not add sections unless the user requests them.

### What

Start with one or two brief sentences explaining what the PR aims to achieve. Follow them with a bullet list of the practical changes. Each bullet must describe a concrete change in behavior, configuration, data, or tests. Group closely related edits; do not narrate every changed line.

### Why

Explain the context in simple English. Establish what the feature is for, who needs it, and the problem or limitation that led to the ticket or PR. Then explain what difference this change makes to the product or the people who maintain it. Use a small before-and-after example when it helps.

Make this section understandable without opening the ticket. Do not repeat the change list, use “required by the ticket” as the reason, or invent customer impact for internal maintenance. If the reason is not supported by the available evidence, obtain the missing context before presenting it as fact.

### Ticket

Use `[TICKET_NUMBER](verified-ticket-url)` when the URL is supplied or established from trusted project context. Never guess the Jira host. If only the number is available, include it with “Link unavailable.” If there is no ticket, write `N/A`.

### Risk

Assess the risk of deploying the complete change using the reference template. Choose exactly one rating: `🟢 Green`, `🟠 Amber`, or `🔴 Red`.

Use the highest applicable category; do not average risks across files. A small diff or passing tests do not override a higher-risk category in the template. Consider affected users and services, data changes, permissions, deployment dependencies, recovery, and relevant validation. Investigate material unknowns and account for unresolved uncertainty; do not treat missing evidence as proof of low risk.

Under `**Reason for rating:**`, write one or two sentences explaining how the evidence led to this rating. Name the main risk or reason the impact is limited. Include the most relevant test evidence, recovery constraint, or unresolved check when it explains the rating. Avoid generic claims such as “safe change” or “tests pass.”

Preserve the template's merge requirements when applicable: Amber needs a team discussion before merge; Red needs explicit approval from Thor or Neil before merge. Include the applicable requirement within the reason's sentence limit. Describe it as required unless there is evidence it is already complete. A risk rating does not authorize a merge, and drafting the summary does not require merge approval.

## Return copyable Markdown

Return the title in one fenced `text` block and the completed description in one fenced `markdown` block. The user can copy these into GitHub's separate title and description fields. Include no preamble, follow-up offer, drafting notes, template comments, or risk guide in the final output.

Before returning the result, verify that:

- The title communicates the actual change and uses the optional ticket prefix correctly.
- What has a one- or two-sentence introduction followed by practical change bullets.
- Why explains the need and product effect without assumed knowledge.
- Technical explanations follow the STE guidance, with necessary terms defined at first use.
- Every factual claim is supported, and the ticket status and links are accurate.
- Risk contains one rating and a one- or two-sentence reason grounded in the template.
- Both blocks contain completed content, with no placeholders or unrelated sections.
