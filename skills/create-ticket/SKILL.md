---
name: create-ticket
description: Create a Jira ticket from notes, a draft or a finding, with a verified destination and relevant parent. Use when asked to create, raise or file a ticket, not for drafting only.
---
# Create ticket

1. Invocation authorizes creating one issue and setting its parent/status. Preview requests and editing this skill do not authorize Jira changes.
2. Use Jira MCP via `tool_search`; inspect tool schemas. Default Trade Tariff work to `https://transformuk.atlassian.net`, project **HMRC**, type **Task**, status **To Do**, intended board **155**. Explicit user choices override defaults; ask for unrelated work's destination.
3. Verify the exact project key, issue types and required fields. **OTT is not HMRC.** Boards use filters, not a creation field: inspect board 155's filter when supported; otherwise report visibility as unverified. Keep board configuration unchanged.
4. Use [write-ticket](../write-ticket/SKILL.md) for research, drafting and its Markdown handoff, then return here to publish. Reuse settled decisions and existing evidence; the Task default replaces its issue-type interview.
5. Search the destination project for duplicates and read plausible matches. Reuse an issue already created this session; ask before creating work already covered elsewhere.
6. Discover valid parent types and fields from Jira metadata. Read a user-supplied parent; otherwise search active Epics in the destination project, paginate summaries and read plausible descriptions. Use siblings to clarify scope when needed.
7. Auto-select a parent only when exactly one valid active candidate clearly covers the outcome and feature. Explain the scope match; title keywords or recency alone are insufficient. Ask when ambiguous, none fits or access is incomplete; leaving it unparented requires the user's choice.
8. Create once with the draft and selected parent. Use the verified `parent` or legacy Epic Link field as supported by the tool schema; discover custom field IDs. Cross-project parenting needs explicit direction. Leave assignee, sprint and priority at defaults unless requested or required.
9. Read back project, type, status and parent. If needed, use a discovered transition targeting To Do. Verify board inclusion when supported; never infer it from the project alone.
10. On uncertain creation results, search before retrying. Correct the existing issue instead of duplicating it. Delete/recreate requires explicit authorization and supported tools; report unavailable capabilities and partial failures honestly.
11. Return the linked ticket, project/type/status, linked parent with its scope reason, local draft link and any unresolved limitation. Claim completion only for fields read back successfully.
