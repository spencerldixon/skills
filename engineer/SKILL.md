---
name: engineer
description: Run the engineering workflow on a ticket by handing each step to a subagent (planner, implementor, reviewer), from ticket to a change that is reviewed and checked by hand. Stops for your approval after the plan, and for your own check with a walkthrough. Use when asked to work a ticket end to end, to engineer a ticket, or to run the engineering workflow.
---

# Engineer: engineering workflow

You coordinate the work. Subagents do it. You do not write product code yourself.

A frontier model plans so that a mid-tier model can build. The implementor follows the plan literally and cannot ask questions, so the plan holds the thinking.

## Agents

Each agent is a small file in `../agents/`, relative to this skill directory. Its frontmatter sets the agent's model tier and tools; its body is the agent's instructions. To customise an agent, edit its file.

- `../agents/planner.md`: reads the ticket and the code, writes the plan
- `../agents/implementor.md`: builds the plan test-first
- `../agents/reviewer.md`: reviews the change with the `code-review` skill, then writes a walkthrough with the `walkthrough` skill

Resolve all bundled paths relative to this skill directory, not the working repository. Pass absolute paths to subagents. The working repository is where the ticket is implemented. Results are saved in the ticket folder, outside the repository.

## Models

Pick each subagent's model from its agent's tier. Edit this table to change models.

| Tier | Claude Code | pi | Codex |
| --- | --- | --- | --- |
| small | `haiku` | `openai-codex/gpt-6.1-sol:low` | your default model |
| mid | `sonnet` | `openai-codex/gpt-6.1-sol:medium` | your default model |
| frontier | `opus-5.5:xhigh` | `openai-codex/gpt-6.0-astra:xhigh` | your default model |

## Starting a subagent

Give every subagent three things:
1. The agent file's body as its instructions.
2. The step's task.
3. The paths of the files it must read.

Its final reply is its result. Save that reply, unchanged, to the step's result file.

How to start one depends on the tool you are running in. Each way enforces the agent's `tools` setting:

- **Claude Code:** use the Agent tool. For `tools: read-only` use the `Plan` subagent type, which has no file-editing tools; for `tools: full` use `general-purpose`. Put the agent's instructions at the top of the prompt and set `model` from the table.
- **pi:** run it with bash, without a timeout (the implementor can take many minutes), and save its output:
  `pi -p --no-session --model <model> --tools <tools> --append-system-prompt <agent file> "<task and paths>" > <result file>`
  For `tools: read-only` pass `--tools read,grep,find,ls,bash`. For `tools: full` leave out `--tools`.
- **Codex:** run it with bash, using a long timeout if your shell tool has one:
  `codex exec -s <read-only or workspace-write> -C <repo root> -o <result file> "<agent instructions, task and paths>"`

## Before you start

1. Get the ticket from the user's message, a file, or a Jira key read with the Jira MCP's read tools. If it has no clear outcome or acceptance criteria, say so, suggest the `write-ticket` skill, and stop.
2. Create the ticket folder `~/Rails/trade-tariff/tickets/<KEY>/`, such as `~/Rails/trade-tariff/tickets/HMRC-1234/`, and save the ticket there as `ticket.md`. If the ticket has no key, ask for one. If the folder has files from an earlier run, ask whether to continue from them or start again.
3. Check the working tree is clean. If it isn't, stop and ask the user.
4. If you are on the default branch, create a branch named `<KEY>-short-descriptive-name`, such as `HMRC-1234-show-address-save-error`. On any other branch, stay on it.

## Steps

All result files go in the ticket folder.

1. **Plan.** The planner reads the ticket → `plan.md`. If its reply is only a `## Questions` section, save it as `questions.md`, ask the user, and run the planner again with the answers.
2. **Gate: plan.** Show the user the plan. Ask them to approve it, revise it with a note, or stop. Wait for the answer. For a revision, run the planner again with the note and the previous plan.
3. **Build.** The implementor reads the ticket and the plan, and builds every task test-first → `build.md`.
4. **Verify.** Run the plan's test and lint commands yourself. Never take a subagent's word that tests pass. If anything fails, send the failing output to the implementor, then verify again.
5. **Review.** The reviewer reads the ticket, the plan and the change, and does its review job with the `code-review` skill (`../code-review/SKILL.md` from this file) → `review.md`. The change is uncommitted, so tell it to review `git diff <default branch>` and the untracked files that `git status` lists. If it reports blocking findings, send them to the implementor, verify again, and have the reviewer check the fixes.
6. **Walkthrough.** The reviewer reads the ticket, the plan and the change, and does its walkthrough job with the `walkthrough` skill (`../walkthrough/SKILL.md` from this file) → `walkthrough.md`.
7. **Gate: human check.** Show the user the walkthrough. Ask them to follow it and reply with pass, or the step that failed and what they saw. Wait for the answer. For a failure, send the step and what they saw to the implementor, then go back to step 4.
8. **Report.** End with a table of each step: agent, model, outcome, result file. Then ask the user whether to ship. On yes, use the `ship-it` skill (`../ship-it/SKILL.md` from this file).

## Rules

- Pass file paths between steps, never your own summaries of them.
- Never skip a gate, even when the output looks fine.
- Do not edit product code yourself. Send changes to the implementor.
- Each loop back to the implementor (steps 4, 5 and 7) gets two rounds. After two failed rounds, stop and report to the user.
- If a subagent fails twice in a row, stop and tell the user what happened.

## Language

Write in Simplified Technical English.

Build the user's knowledge. When you use a concept, decision or file that may be new to them, say what it is and why it matters, in one sentence.

Be concise. Put the answer or decision first. Cut every word that does not help the user act or learn.

At each gate, start with two or three sentences: what happened, the main decision and why, and what you need from the user.
