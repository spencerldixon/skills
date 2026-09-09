---
name: explain-this
description: Research and explain a ticket, file, feature, or codebase concept for a junior developer on their first day. Use for onboarding, code walkthroughs, and understanding how and why code fits together, with plain English, practical examples, numbered steps, and verified line references. Accept an optional file, ticket, or natural-language prompt; use conversation context when omitted. This is an explanation workflow, not ticket drafting or implementation.
---

# Explain This

Help the reader build a mental model they can reuse: why this exists, who needs it, what happens, where it happens, and why the pieces are arranged this way. Assume a junior developer on their first day with no product knowledge, limited familiarity with code, and a short attention span.

Research the workspace read-only and deliver the explanation in the conversation. Save a document or change code only if separately requested.

## 1. Establish what to explain

Accept any combination of:

- A file path, optionally with a line number, selected code, or a symbol such as a function or class name.
- A ticket's text, identifier, link, or local Markdown file.
- A prompt naming a feature, workflow, or concept, such as “how does signing in work?”
- No argument, when the current conversation or available editor context clearly identifies the subject.

Reuse context already supplied. If the subject or repository is unclear, ask one focused question before choosing an unrelated topic or surveying the whole codebase. A file is a starting point: follow its important callers and dependencies to explain its role.

Read a referenced ticket with available read-only tools. If it is inaccessible, ask for its relevant text or location; do not infer its contents from its identifier. Continue any independent code research that is possible.

## 2. Research the actual workflow

Read applicable repository instructions and focused documentation. Use `rg --files` and `rg` to find relevant files and symbols, then read enough surrounding code to understand their behaviour.

Trace the real path from the initiating person, system, or event to the final result:

- Identify the entry point and what calls it. Establish who uses the feature and the problem it solves from documentation, tickets, code, or user context.
- Follow the important decisions, transformations, state changes, and handoffs. Inspect relevant callers, services, models, storage, background work, external systems, and output code as applicable; do not force every codebase into a web-request pattern.
- Read focused tests, configuration, and schemas to check examples, edge cases, and conditions that change the path. Separate behaviour described by a test from behaviour you have actually observed running.
- For a ticket, distinguish the checked-out code's current behaviour, the requested change, and the intended benefit. Acceptance criteria describe what should be true when the work is done; they do not prove it already works.
- Consult focused history or design records when they help explain intent. State a component's observable responsibility confidently when supported; label inferred design rationale as inference. Code structure alone does not prove why its authors chose it.
- Verify source line numbers against the files you actually read, using tools such as `nl -ba`. Attach references to the specific claims they support, rather than giving an unexplained file list at the end.

Keep research proportional to the question. Follow enough connections to explain the main path and its important alternative or failure case. Avoid unrelated architecture tours. Identify boundaries you cannot inspect, including another repository, an external service, or unavailable runtime configuration.

Keep evidence distinct: **confirmed in source**, **reported by the user or ticket**, **inferred**, and **unknown**. Do not imply that reading code proves deployed behaviour, that reading tests means they passed, or that a plausible example is real production data.

## 3. Confirm assumptions before the full explanation

Before delivering the full explanation, check its scope and claims against the evidence. Resolve assumptions from the repository where possible instead of asking the user questions the code can answer.

If you still plan to rely on assumptions about the intended subject, users, terminology, business purpose, environment, or expected behaviour, briefly state them and ask the user to confirm or correct them. Use a short round of focused questions and explain what each answer will clarify. Wait for answers before delivering an explanation that depends on those assumptions; silence is not confirmation. Continue independent research while waiting.

Previously supplied confirmation counts; do not ask again. If no unconfirmed assumptions remain, say so briefly and proceed without manufacturing a question. User confirmation establishes their context or intent, but does not independently verify runtime behaviour.

Unresolved details that the explanation does not depend on may remain as explicitly labelled unknowns. Do not quietly adopt them as facts. Carry them into “Unknowns and who to ask” with a concrete question and a suggested source or contact.

## 4. Teach in small, connected steps

- Start with the real-world need, then introduce only the concepts needed to follow this code. Build from familiar actions and cause and effect before naming abstractions.
- Expand every acronym on first use and explain its meaning in ordinary language, including common ones such as API (application programming interface: a defined way for programs to communicate). Explain unfamiliar product terms and code vocabulary at first use too. Never guess an internal acronym's expansion; flag it for confirmation.
- Use one small, practical example throughout the explanation so the reader can follow the same input through each handoff to its result. Mark invented names, values, and scenarios as illustrative, and keep them consistent with the code. Include one relevant empty, invalid, or failure case when it helps explain the feature.
- Use descriptive headers, explicitly numbered workflow steps, short sentences, and paragraphs of two or three sentences. Aim for roughly 400–700 words for a typical feature, less for a small question; expand only when needed to preserve the explanation. Avoid deep bullet nesting and long code blocks.
- Make step titles describe actions, such as “Check whether the user can view the order.” Explain an identifier's job before asking the reader to remember its name.
- Use a friendly, encouraging tone and an occasional useful analogy. Map the analogy back to the real components and say where it stops fitting if that matters. Avoid baby talk, forced jokes, and words such as “obviously” or “just” that make difficulty sound like the reader's fault.
- Quote code only when a small excerpt teaches something prose cannot. Explain what the excerpt does and why it matters; label pseudocode and illustrative code clearly. Do not narrate every line or paste entire functions.
- Give clickable file links with verified line numbers beside the relevant step or claim. Use absolute local paths with a single line anchor and a readable label containing the filename and line number. Use verified remote line links when only remote source is available. Never invent a path, line number, or link.

## 5. Shape the explanation for skimming

Use this order, keeping each section proportional to the subject. The Summary and Context should provide the same orientation as a good ticket: purpose and users before implementation. These instructions are self-contained; another skill is not required.

### Summary

One or two plain-English sentences explaining what the subject does and why it matters. For a ticket, include the current problem and intended outcome. For existing code, describe its responsibility without inventing a defect or change request.

### Context: who uses this and why

Explain the relevant part of the product, the person or system using it, their goal, and what triggers this workflow. Introduce the practical example. Include history only when it is known and helps understanding.

### The few concepts you need

Briefly define the small set of ideas needed for this explanation, starting from first principles. For example, before discussing a background job, explain that some work can be queued to run later so a person does not have to wait for it. Omit this standalone section for a small question if inline definitions suffice.

### How it works, step by step

Start with a compact arrow flow or small diagram when it makes the connections clearer. Label the pieces with plain-English roles and distinguish work that happens later from work that happens immediately.

Then use a numbered list, usually three to seven steps. Each step should explain:

- What arrives or triggers the step, using the running example.
- Which component acts, what it does, and why that action is needed.
- What leaves or changes and which step receives it next.
- The relevant source location, with a verified line number.

Keep this in short connected prose within each numbered step, rather than repeating a four-field form. Show the visible result, not only the internal calls. For a ticket, make the point where behaviour should change clear and keep the proposed path distinct from existing code. For a static concept or data structure, number its construction and use or its relationships rather than inventing an execution sequence.

### Why the pieces are arranged this way

Explain the key responsibility boundaries and practical tradeoffs: what each separation enables, prevents, or costs. Ground historical reasons in evidence. Phrase an unrecorded rationale as “This separation allows…” or “A likely reason is…” rather than claiming to know the author's intent. Avoid repeating the walkthrough; incorporate this into the steps for a very small topic.

### Unknowns and who to ask

State what remains unresolved and why an answer matters. For each gap, give a precise question and the most useful next source or person. Use documented ownership when available; history can suggest someone familiar with the code but does not establish current ownership. Otherwise suggest a role, such as the feature maintainer or product manager, and label it as a suggested contact. Never invent a person's name or contact anyone automatically. If there are no material unknowns, say so briefly.

### Where to look next

Finish with one to three useful code landmarks or a small, optional reading exercise that reinforces the mental model, such as following the example through a named test. Explain what to look for. Avoid assigning homework, proposing unrelated changes, or asking a comprehension quiz unless invited.

## 6. Check before delivering

Review the explanation from the perspective of someone opening this repository for the first time:

- Can they explain who needs this and why it exists after the opening paragraphs?
- Can they follow one example from trigger to outcome, including the important handoffs?
- Are assumptions confirmed and current behaviour, requested changes, inferred rationale, and unknowns clearly distinguished?
- Are acronyms and unfamiliar terms explained before they become necessary?
- Do source links point to verified lines that support the adjacent claims?
- Are unresolved questions actionable, with an evidence-backed or explicitly suggested contact?
- Can they skim the headers and numbered steps without losing the thread?

Revise for clarity and remove repetition before responding. Do not expose a score or this checklist.
