# What a good ticket is

A ticket tells someone else what to change, why, and how to prove it is done. That reader has only the ticket and the repository. They may be a junior developer on their first day in this codebase, or a coding agent.

Both readers need the same thing: a short ticket in which every sentence matters. A developer stops reading a long ticket. An agent reads all of it and treats every passing remark as an instruction. So be surgical. Write what the reader needs to do the work and nothing else, in plain, human language.

**Length.** A reader should take in a ticket in about two minutes. Aim for roughly 200–400 words for a small story or bug, and up to about 600 for a large change or a spike. If a draft is longer, cut it before you add anything. A long ticket usually means one of these:

- Facts the reader can see in the code.
- Several sections that say the same thing.
- Detail about how to do the work that the reader can work out for themselves.

**Language.** Plain English and short sentences. Define this product's domain terms and internal names, such as "commodity code", "geo area 1400" or "organization membership". Do not define everyday developer terms such as API, AWS, database, background job or system test.

A ticket has these sections, in this order:

1. **Summary:** the problem and the outcome, in one to three sentences.
2. **Context:** what the reader needs to understand about this feature, its users, and why the work matters.
3. **Technical:** the specific changes to make, with their constraints and the reasons for any choices.
4. **Resources:** useful links and attachments. Leave this section out if there are none.
5. **Acceptance Criteria:** the checks that prove the work is done.

# Title

Short, specific and actionable, with one outcome. It must make sense without opening the ticket and must describe the outcome, not only the topic. If a title needs "and" to join two outcomes, consider whether there are two tickets. Put [BUG] or [SPIKE] at the front of the title for a bug or a spike.

- Bad: "Search page no search results error message"
- Good: "Add a 'No results found' message to the search page"
- Good: "[SPIKE] Find out why job X failed on 3 March with error Z and raise a fix ticket"

# 1. Summary

One to three sentences: what happens now, why it is a problem, and what the ticket changes.

> When a search has no matches, the search page is blank, so users can't tell whether it worked. Show "No results found for <term>" and a link back to the search box.

# 2. Context

A short paragraph about this feature: who uses it, how, and why the current behaviour hurts them. Include history only when it explains a decision, for example "HMRC rejected sending XI users to the UK site because…". Do not introduce the whole product or the company.

# 3. Technical

State what has to change, and why. A reader should finish this section knowing where to make each change and what rule constrains it. Use only the parts below that the ticket needs. Most tickets need two or three of them.

- **Reproduce** (bugs): numbered steps with full links, then one line each for expected and actual behaviour.
- **Changes:** a short numbered list of the specific changes. Each item names the one place to change, as a code link with a line number, and gives the reason when the reason is not obvious. Name the pattern to copy if there is one. Do not list every file the reader might open; they can find those.
- **Constraints:** rules the change must follow that the reader might otherwise break, such as "admins only", "keep users on the XI site", "no new Go dependencies" or a repository convention. Give the reason in a few words.
- **Suspected cause** (bugs and spikes, when the cause is not yet known): the likely explanations, with the evidence for each.
- **Questions to answer** (spikes): numbered questions, the time box, and the deliverable. Say what to do if the time box ends with questions still open.
- **How to find the evidence** (spikes and bugs that need logs or data): where to look, the exact query or filter to run, and what a match looks like. For example: the log group, a CloudWatch Logs Insights query filtering on `error_class`, and the fields that identify one job run. A reader who knows what they are looking for finishes the spike; one who doesn't, browses.
- **Open questions:** only what the interview could not settle. Each one gives the default to use until someone answers. Most tickets have none.
- **Out of scope:** only when the reader is likely to wander into related work, which is common in spikes. One line per item, without repeating anything said elsewhere.

Write facts as plain statements. Do not prefix them with labels such as "Confirmed:", "Decided:" or "Assumption:". Put a decision where it applies, with its reason: "Keep the page on the XI site. HMRC agreed in March 2026 that sending traders to the UK site confuses them." Do not repeat one point in several places.

Use full Markdown links wherever the reader will click: production and local URLs, code, pull requests and tickets. For example, [the XI geo area page](http://localhost:3001/xi/geographical_areas/1400) or [geographical_areas_controller.rb:12](https://github.com/org/repo/blob/main/app/controllers/geographical_areas_controller.rb#L12).

Example:

```
### Reproduce

1. Open [a search with no matches](http://localhost:3001/search?q=ottnoresultstest)
2. Expected: "No results found for ottnoresultstest". Actual: a blank results area.

### Changes

1. Render a no-results message in [search/_results.html.erb:4](link) when `@results` is empty. Copy the empty state in [_no_measures.html.erb](link).
2. Add a request spec next to [search_spec.rb](link).

### Constraints

- Do not change the search query. Only the empty state is wrong.
```

# 4. Resources

Links that help someone understand or check the work, each with a few words on why it matters: designs, screenshots, related tickets and pull requests, documentation. Leave the section out when there is nothing to add. Do not write "no resources were supplied" or "no screenshot available".

# 5. Acceptance Criteria

Three to five checks. A human reviewer and a coding agent both use them to confirm the work is done, so each check must be one they can carry out without asking anyone:

- Something to observe at a linked URL, with the exact expected result.
- A command that must pass.
- A measurable fact, such as "one email is sent" or "the old link returns 'This invitation is not valid'".

The criteria are the verification. Do not add a separate "How to verify" section that repeats them. Put all test expectations in one criterion: the suite command passes, including new tests for the named behaviour. Ask for tests only where they are useful.

```
- [ ] [A search with no matches](http://localhost:3001/search?q=ottnoresultstest) shows "No results found for ottnoresultstest".
- [ ] A search with matches looks the same as before.
- [ ] `bundle exec rspec` passes, including a new request spec for the no-results message.
- [ ] A screenshot of the new message is attached to the ticket.
```

# Before saving

- Could a reader act on this ticket in about two minutes of reading? If not, cut it.
- Does every sentence change what the reader does or understands? Delete the rest, including notes about the writer's environment and statements that something is missing.
- Does Technical name the specific changes and constraints, not a list of files?
- Could an agent prove every acceptance criterion itself?
- Is every Jira ticket and pull request linked, with a short note on why it is relevant?
- Is everything true? Check that nothing is invented and that no suspicion is presented as a fact.
