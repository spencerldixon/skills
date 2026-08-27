# General advice

Use clear, non-technical language.
Write tickets for other people to pick up.
Assume no prior knowledge of the service, write tickets for a junior developer on their first day.
Tickets should contain all the context and materials the reader needs to make the change.
Tickets should describe a clear “done” state, acceptance criteria is the best way to do this.

A good ticket should contain five sections:

1. Summary - a one or two sentence description of the issue and outcome
2. Context - a plain english primer on any context, concepts, and history that helps the reader understand the feature, how users use it, and the work required
3. Technical - technical talk about the issue, implementation details, constraints and considerations
4. Resources - anything helpful to understanding or completing the ticket; screenshots, urls, videos, etc
5. Acceptance Criteria - a clear definition of when the ticket is done and any proof required

# Ticket Title

Write a short, specific title that explains the work to be done and the outcome, without having to open the ticket.

If a ticket is a bug or spike, prefix [BUG] or [SPIKE] to the front of the title.

A good title should:

- Make sense without opening the ticket
- Be actionable
- Not assume prior knowledge of the service or issue
- Describe the outcome, not just the general topic

Bad examples - vague, no clear action or outcome:

- Search page no search results error message
- Job X keeps failing

Good examples - specific, outcome defined, actionable:

- Add a “no results found” message to the search page when no results are found
- Job X failed on day Y with error Z, investigate, write report and open a new ticket for suggested fix.

# 1. Summary

In one or two sentences, clearly explain the problem and desired outcome of the ticket. Use plain, non-technical language.

Write this for a junior developer on their first day who has no prior knowledge of the service.

Include:

- What is happening now
- Why it’s a problem
- What needs to be added, changed or removed
- What the outcome of the ticket is 

Example:

When a user searches for a commodity here (url), and there are no matching results (search for xyz), the service currently displays an empty page. This doesn’t make it clear if the search completed successfully or if something went wrong. Update the page so that users are shown a clear message of “No results were found”, and what they can do next.

# 2. Context

In a short paragraph, explain any context, concepts, history, and terminology that helps a junior developer understand the role of this feature within the service.
Explain why this feature exists, who uses it and how they use it.
Use non-technical language and give practical examples of how a user would interact with this where possible
This is a good opportunity to educate and build knowledge on how our users use the product.

Include:

- A brief history of the feature and why it exists
- What the current behaviour is
- Why the current behaviour is a problem
- Who is affected and why
- How the user benefits from the change this ticket implements

Example:

```
Our users search for products to find their commodity code. That code is then used on customs declarations and helps determine what duties, taxes and measures apply to the goods they are trading.

When searching for a commodity that doesn’t exist, a user currently gets a blank page. Without a clear message users could think that:

The search has failed
The page is still loading
Their product cannot be classified
They cannot continue their journey

The page should explain the search completed successfully and help the user try again.
```

# 3. Technical

Give the developer reading this ticket practical information needed to investigate and implement the change.

Include:

- Steps to reproduce
- Links to pages featuring the issue (URLs are helpful in establishing a starting point of investigation)
- Parameters for testing (helpful in reproducing the issue)
- Known facts: what has been observed or confirmed
- Suspected cause: theories that still require investigation
- Open questions: decisions or unknowns that could affect the work
- Implementation suggestions
- Requirements to meet
- Anything out of scope

Example:

```
## Steps to reproduce:

1. Open https://www.trade-tariff.service.gov.uk/find_commodity
2. Enter ottnosearchresults
3. Submit the search
4. Observe the blank page (see screenshot in resources)

## Helpful links:
Commodity search page: https://www.trade-tariff.service.gov.uk/find_commodity
Search route: https://www.trade-tariff.service.gov.uk/search?q={search-term}
Example no results search: https://www.trade-tariff.service.gov.uk/search?q=ottnoresultstest7f3a91c2

## Technical Requirements:
No changes needed to the actual search.
Add the copy "No results found for #{search term}, please try again" to the currently empty search results page
Write a test to ensure this copy is present on the page when searching for a commodity that doesn't exist
Ensure the change passes WCAG2.1
Ensure the change looks good on mobile
Mockup of the design can be found in the resources / attached to this ticket.
```

# 4. Resources

Add anything that could be helpful in understanding, completing or verifying the work.

You can add:

- Screenshots
- Videos
- Design or prototype links
- Copy or assets
- URLs to replicate the issue
- Links to resources that may be helpful; stack overflow, blogs, github repos
- Other tickets that may contain additional context or dependent work
- Confluence documentation

# 5. Acceptance Criteria

A clear definition of when the ticket is done and if any proof is required. 
Acceptance criteria should be specific and testable. 
Use checkboxes or bullet points. 
Keep it short and sweet, do not overwhelm the developer, aim for around 3-5 acceptance criteria.

Example:

- A no-results message is shown when a search returns no matches
- The submitted search term is included in the message
- Add a test to ensure the message appears on the page when there are no search matches
- The change looks good on mobile
- The page meets WCAG2.0 standards
- A screenshot of the completed change is attached to this ticket
