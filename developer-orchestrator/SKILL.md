---
name: developer-orchestrator
description: Run the engineering workflow on a ticket, from ticket to pull request, by handing each step to a subagent (scout, planner, implementer, reviewer). Stops for your approval after the plan and before the pull request. Use when asked to work a ticket end to end, to orchestrate development, or to run the engineering workflow.
---

# Developer orchestrator: engineering workflow

You coordinate the work. Subagents do it. You do not write product code yourself.

## Agents

Each agent is a small file in `../agents/`, relative to this skill directory. Its frontmatter sets the agent's model tier and tools; its body is the agent's instructions. To customise an agent, edit its file.

- `../agents/scout.md`: reads the ticket and the code, writes the brief
- `../agents/planner.md`: turns the brief into a plan of small, tested tasks
- `../agents/implementer.md`: builds the plan test-first and commits
- `../agents/reviewer.md`: reviews the branch with the `code-review` skill

Resolve all bundled paths relative to this skill directory, not the working repository. Pass absolute paths to subagents. The working repository is where the ticket is implemented and where `.conductor/` results are saved.

## Models

Pick each subagent's model from its agent's tier. Edit this table to change models.

| Tier | Claude Code | pi | Codex |
| --- | --- | --- | --- |
| small | `haiku` | `openai-codex/gpt-6.1-sol:low` | your default model |
| mid | `sonnet` | `openai-codex/gpt-6.1-sol:medium` | your default model |
| frontier | `opus-5.5:xhigh` | `openai-codex/gpt-6.1-sol:high` | your default model |

## Starting a subagent

Give every subagent three things:
1. The agent file's body as its instructions.
2. The step's task.
3. The paths of the files it must read.

Its final reply is its result. Save that reply, unchanged, to the step's result file.

How to start one depends on the tool you are running in. Each way enforces the agent's `tools` setting:

- **Claude Code:** use the Agent tool. For `tools: read-only` use the `Plan` subagent type, which has no file-editing tools; for `tools: full` use `general-purpose`. Put the agent's instructions at the top of the prompt and set `model` from the table.
- **pi:** run it with bash, without a timeout (the implementer can take many minutes), and save its output:
  `pi -p --no-session --model <model> --tools <tools> --append-system-prompt <agent file> "<task and paths>" > <result file>`
  For `tools: read-only` pass `--tools read,grep,find,ls,bash`. For `tools: full` leave out `--tools`.
- **Codex:** run it with bash, using a long timeout if your shell tool has one:
  `codex exec -s <read-only or workspace-write> -C <repo root> -o <result file> "<agent instructions, task and paths>"`

## Before you start

1. Get the ticket from the user's message or a file. If it has no clear outcome or acceptance criteria, say so, suggest the `ticket-writing` skill, and stop.
2. Pick a run id, usually the ticket key, such as `PROJ-123`.
3. Create `.conductor/<run-id>/` in the repo root and save the ticket there as `ticket.md`. If git doesn't ignore `.conductor/`, add it to `.git/info/exclude`.
4. Check the working tree is clean. If it isn't, stop and ask the user.
5. Create a branch for the work. Use the repo's naming convention from `AGENTS.md` or `CONTRIBUTING.md`; if there is none, ask the user.

## Steps

All result files go in `.conductor/<run-id>/`.

1. **Scout** → `brief.md`: what the ticket asks for, acceptance criteria, relevant files, and the exact commands that run the tests and the linter.
2. **Planner** reads the ticket and the brief → `plan.md`.
3. **Gate: plan.** Show the user the plan. Ask them to approve it, revise it with a note, or stop. Wait for the answer. For a revision, run the planner again with the note.
4. **Implementer** reads the ticket, the brief and the plan, builds every task test-first and commits each task → `build.md`.
5. **Verify.** Run the test and lint commands yourself. Never take a subagent's word that tests pass. If anything fails, send the failing output to the implementer to fix, then verify again. After two failed rounds, stop and report to the user.
6. **Reviewer** reads the ticket, the plan and the diff, and follows the `code-review` skill (`../code-review/SKILL.md` from this file) → `review.md`. If it reports blocking findings, send them to the implementer, verify again, and have the reviewer check the fixes. After two rounds, stop and report to the user.
7. **Pull request.** Use the `pr-summary` skill (`../pr-summary/SKILL.md` from this file) yourself to write the title and body to `pr.md`.
8. **Gate: pull request.** Show the user `pr.md`. Push the branch and open the pull request (for example with `gh pr create`) only after they say yes.
9. **Report.** End with a table of each step: agent, model, outcome, result file.

## Rules

- Pass file paths between steps, never your own summaries of them.
- Never skip a gate, even when the output looks fine.
- Do not edit product code yourself. Send changes to the implementer.
- If a subagent fails twice in a row, stop and tell the user what happened.
