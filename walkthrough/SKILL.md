---
name: walkthrough
description: Write a short human verification guide for a change or bug, with exact app actions and visible expected results. Use for browser, native app, or API checks; not automated testing or implementation.
---

# Walkthrough

Research and write only. Read the task, change, and relevant source. Use the actual surface: browser, native application, or API. Assume the application is running with data unless setup is necessary.

Write one or two sentences explaining what the check proves, followed by normally **six core actions or fewer**. Cover the main visible change and required human outcomes. Put extended failure/recovery checks in a separate optional section; required critical checks must remain in the core flow even if it needs more steps.

- One action per step, using exact labels in **bold** and typed values in `code`.
- Give full URLs and parameters for browser/API steps, or exact executable/document paths and menu labels for native apps. Do not invent a host, route, label, or record.
- Reuse existing safe fixture data. For runtime values, say exactly where to find them and what to skip when the record does not exist.
- After a state-changing action give **You see:** with an observable result. Reading source or tests is not a runtime pass.
- Prefer isolated fixtures. Before steps that change user settings/data, explain effects and restoration. Avoid real deletes, updates, messages, or other irreversible operations merely to verify a fix.
- Mark steps **(not verified)** when you could not perform them. Say when an edge case is covered only by automated evidence.

Check each instruction against source. If permitted tools and the app are available, try the guide without changing live data. Report unavailable checks plainly.

Write to the assigned artifact path when an orchestrator or user supplies one; return only the path and a short outcome. Otherwise return the guide in chat. When presenting it as a required human check, follow [human-review.md](../references/human-review.md) to open the document in Neovim in a new Ghostty tab before asking.

## Language

Use Simplified Technical English, active voice, and one instruction per sentence. Keep steps short and use the same name for the same thing.
