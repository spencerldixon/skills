---
name: walkthrough
description: Write a step-by-step guide that a person follows in a browser to see with their own eyes that a change works, or that a reported bug happens. Every step has an exact URL, parameters, the exact text to click or type, and the expected result, in Simplified Technical English. Use for human-in-the-loop verification of a build, branch, pull request or ticket, and for reproducing an issue by hand. Not for automated tests or code review.
---

# Walkthrough

Write a short guide that lets a person check a change with their own hands, one action at a time. Assume the app is installed, has data, and is running. Assume the reader will do exactly what each step says, and nothing more. If a step needs knowledge that is not on the page, the step is broken.

Research and write only. Do not change code, commit, push, or update tickets.

## 1. Find out what to walk through

Accept a ticket, a pull request, a branch, a diff, a bug report, or the current conversation. Read a referenced ticket with available read-only tools; never infer its contents from its key.

Decide what the walkthrough proves: a change works, or a bug happens. Use the environment the user names. Otherwise use the local app, with the host and port from the repository's config.

## 2. Find every fact in the source

Never write a URL, label or value from memory or from what is "usual".

- **What changed.** Read the diff and the acceptance criteria.
- **URLs.** Read the router (for example `config/routes.rb`) for the path and HTTP method. Read the controller for the query parameters it reads, where it redirects, and who can access it.
- **Screen text.** Copy button, link, field and message text from the views and translation files (for example `config/locales/*.yml`).
- **Data.** Use records that the seed data or fixtures create, with their real names.
- **Hidden results.** If a result is an email, a background job or a feature flag, give the exact URL or place to see it.
- **Existing tests.** System and feature tests often hold the exact clicks, data and expected text. Reuse them.

## 3. Write the walkthrough

Start with one or two sentences: what we are walking through, why, and the expected outcome. Then give one numbered list of actions.

Cover each acceptance criterion or claimed fix. Add one failure or edge case when the change has an important one, such as invalid input or a missing permission.

### Step rules

1. **One action per step.** Open, click, type, select, tick. Never "fill in the form" or "log in".
2. **Full URLs.** Write host, port, path and query string, for example http://localhost:3000/orders?status=paid&page=2. Never write "go to the orders page". Under each URL with query parameters, add a table: parameter, value, what it does.
3. **Values known in advance.** Name the exact record to use, and reach it by clicking its name. If the reader must use a value only known at runtime, such as a new ID, tell them where it appears and give an example.
4. **Screen text in bold, typed text in code.** Click **Save order**. Type `SAVE10` in the **Discount code** field. Use the exact text from the source, with the same capital letters.
5. **Expected results you can see.** After each step that changes the page, add **You see:** with the URL, the exact message, or what appears or disappears. Never write "it works" or "the page looks correct". For a bug, write **You see (the bug):**.
6. **Warnings before the step.** Put a warning before any step that deletes data, sends a real email or cannot be undone.
7. **Clean user switches.** When the walkthrough needs a different user, say which user, and tell the reader to use a private browser window.
8. **No page, no browser.** If the change is an API with no page, give an exact `curl` command. State the expected status code and the response fields to look at.

### Language

Write in ASD-STE100 Simplified Technical English ([official standard](https://www.asd-ste100.org/assets/files/ASD-STE100_ISSUE9.pdf)).

- Start each instruction with a verb. Give one instruction per sentence, in 20 words or fewer.
- Use one name for one thing. Use the exact screen label as the name.
- Use active voice. Do not use idioms, or words such as "just", "simply" or "obviously".

### Example

```markdown
# Walkthrough: Discount codes at checkout

Customers can now use a discount code when they place an order. This walkthrough checks that the code reduces the order total by 10%.

1. Open http://localhost:3000/orders/new?plan=pro

   | Parameter | Value | What it does |
   | --- | --- | --- |
   | `plan` | `pro` | Selects the **Pro** plan on the form. |

2. Type `SAVE10` in the **Discount code** field.
3. Click **Apply code**.

   **You see:** The text **Discount applied** below the field.

4. Click **Place order**.

   **You see:** The message **Order placed**. The **Total** line shows **£90.00**, not **£100.00**.

5. Click **New order**.
6. Type `NOTACODE` in the **Discount code** field.
7. Click **Apply code**.

   **You see:** The error **This code is not valid** below the field. The total does not change.
```

## 4. Check before you deliver

Confirm each item against the source:

- Every path exists in the router with that HTTP method, and the code reads every query parameter you use.
- Every label and message matches the view or translation file.
- Every record you name exists in the seed data or fixtures.
- Each expected result follows from the code on the branch.

If the app is running locally and you have a browser tool or `curl`, follow the steps yourself to confirm they work. This checks the guide; it does not replace the reader's check.

If you cannot confirm an item, add **(not verified)** to that step. Never present a guess as fact.

Return the walkthrough as Markdown in the conversation. Save it to a file only when the user asks.
