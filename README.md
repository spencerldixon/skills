# Skills

Skills for engineering work, for Claude Code, Codex and pi.

## Available skills

| Skill | Description |
| --- | --- |
| [goblin](beta/goblin/) | Fixes one demonstrable developer annoyance within 20 added plus deleted lines, with no new dependencies. Uses Sonnet in Claude Code. |
| [pick-up](beta/pick-up/) | Recovers unfinished work from the branch, ticket and PR, checks stale handoffs, and identifies the next action. |
| [standup](beta/standup/) | Drafts a short daily update from verified activity, grouping work by outcome and marking inferred plans. |
| [remember-this](beta/remember-this/) | Saves significant project knowledge, gotchas, decisions or essential WIP context, verifying claims and updating existing notes without duplication. |
| [engineer](beta/engineer/) | Runs a change from spec to pull request: approved spec, implementation subagent, `code-review`, fixer subagent, then `ship-it`. |
| [code-review](beta/code-review/) | Reviews a branch or diff with a context scout and two independent reviews, merges every point into one report, and gives a pass or changes-needed verdict. |
| [find-work](beta/find-work/) | Finds unassigned, unblocked Ready to Start and To Do tickets on boards 155 (HMRC) and 298 (AI), scores clarity, size, risk and proof, and triages each into Auto, Guided, Sharpen, Waiting or Split to help you or autopilot choose the next ticket. Returns results in the session without a vault report. |
| [write-ticket](skills/write-ticket/) | Interviews you, researches the relevant code, and writes a clear Jira ticket following the included ticket template. |
| [create-ticket](skills/create-ticket/) | Drafts and creates a Jira ticket with a verified destination and relevant parent. Defaults Trade Tariff work to HMRC Tasks in To Do. |
| [explain](skills/explain/) | Explains a ticket, file, or codebase concept in plain English with context and examples. |
| [pr-summary](skills/pr-summary/) | Writes a clear PR title and summary using the included template, with an optional Jira ticket and a deployment risk rating. |
| [walkthrough](skills/walkthrough/) | Writes a short human check for a browser, native application, or API, with exact actions and visible results. |
| [preflight](beta/preflight/) | Checks that a repo's tools, dependencies, services, disk space and one fast spec are ready before agent work starts. |
| [find-performance-issues](beta/find-performance-issues/) | Finds why a page, endpoint, job or query is slow, explains each issue in plain English, estimates the gain with the arithmetic shown, and validates it with a measurement or an exact check to run. |
| [autopilot](beta/autopilot/) | Runs under `/loop`: picks up `agent-ok` tickets, runs `engineer` in pi for each in its own worktree and Rex tab, opens draft PRs, and watches them with `watch-pr`. At most 2 tickets in flight. Never merges. |
| [watch-pr](beta/watch-pr/) | Runs under `/loop`: watches your open PRs and In Review tickets, fixes failed CI, lint errors and clear review comments, marks green drafts ready, and notifies you of new comments, fixes, blockers and PRs ready to merge. Never merges. |
| [ship-it](skills/ship-it/) | Commits your local work, pushes it, opens a pull request in each changed repo with `pr-summary`, comments the links on the Jira ticket once, and moves the ticket to In Review. |

## The engineer workflow

Ask for a ticket implementation or a bounded fix. The engineer:

1. Runs `preflight`, then writes a spec and opens it for your approval.
2. Implements the approved spec with a subagent.
3. Runs `code-review` itself: a context scout, two independent reviews and a merge, each in its own subagent.
4. Runs the `fixer` subagent: fixes for the review findings, lint with autocorrect, then the test suite.
5. Re-reviews any fix to a blocking finding, up to two repair rounds per blocker.
6. Reports the review and a plain-English roundup, offers an optional `walkthrough`, then runs `ship-it` if you approve.

Reports are written once. Agents start with fresh context, receive file paths, and return a path plus a short outcome. The coordinator keeps verification and decisions in one `steps.md`.

`~/wiki` is the only persistent store for agent artifacts. Keep only significant project knowledge, gotchas, consequential decisions, essential WIP and documents still needed by active work. Routine progress stays in session context. Agents maintain the wiki without asking conversational permission: update canonical notes, consolidate duplicates and recoverably cull outdated or spent material. Tool-enforced approvals still apply. [`references/vault.md`](references/vault.md) defines the quality gate, maintenance and paths. No Jira key is required. Dirty trees are preserved; only ambiguous or conflicting edits require a decision.

### Customising the agents

`pick-up`, `standup` and `remember-this` use `model: sonnet` in Claude Code. For OpenAI runtimes, prefer Sol when selecting the session or worker model; the Claude Code frontmatter does not configure those runtimes.

[`agents/fixer.md`](agents/fixer.md) holds the fixer role. It gets `Read, Edit, Grep, Glob, Bash, Write`; front matter sets Claude Code model `opus` and effort `medium`. The engineer and its implementation subagent run on the session model. Other runtimes ignore these fields; configure comparable models there.

`code-review` uses general-purpose subagents to collect facts and run independent, free-form reviews. They use read-only commands and write only their assigned report. The skill supplies their task instructions directly. Pi uses lowercase tool names, so pi needs its own copy of `fixer.md` in `~/.pi/agent/agents/`.

Keep repository-specific commands and conventions in each repo's `AGENTS.md`. The workflow and role reports should reference facts once, not repeat the conversation.

### Opening human review documents

Before a required approval or human check, open the document in Neovim in a new focused Rex pane using the short command in [`references/show-to-human.md`](references/show-to-human.md). If Rex is unavailable, report that and link the file. No helper scripts or synchronization step are needed.

## Install

Each tool installs this repo through its own marketplace or package manager. Updates come through the same tool.

### Claude Code

```sh
claude plugin marketplace add spencerldixon/skills
claude plugin install spencerldixon-skills@spencerldixon
```

Inside a session, `/plugin marketplace add spencerldixon/skills` works too. Claude Code prefixes plugin skills with the plugin name, for example `/spencerldixon-skills:engineer`.

### Codex

```sh
codex plugin marketplace add spencerldixon/skills
codex plugin add spencerldixon-skills@spencerldixon
```

### pi

```sh
pi install git:github.com/spencerldixon/skills

pi update git:github.com/spencerldixon/skills
```

## Upgrading from the install script

Earlier versions installed with `install.sh`, which linked each skill into `~/.claude/skills` and `~/.agents/skills`. Those links override the plugin versions, so remove them once, before installing as above:

```sh
curl -fsSL https://raw.githubusercontent.com/spencerldixon/skills/main/uninstall.sh | bash
```

The uninstaller only removes links that point into its clone at `~/.local/share/spencerldixon-skills`, then removes that clone.

## Repository layout

```
.claude-plugin/          Claude Code marketplace and plugin manifest
.codex-plugin/           Codex plugin manifest
.agents/plugins/         Codex marketplace
package.json             pi package manifest
skills/<name>/SKILL.md   reusable skills (Agent Skills format)
beta/<name>/SKILL.md     experimental skills and orchestrators
agents/<role>.md        shared agent roles and write scopes
references/             shared procedures: show-to-human, language, vault
```

## Adding a skill

1. Create `skills/<name>/SKILL.md` (or `beta/<name>/SKILL.md` for experimental work) with `name` and `description` frontmatter.
2. Copy the `## Language` section from another skill, so every skill talks to the user the same way.
3. Add `./skills/<name>` or `./beta/<name>` to `skills` in `.claude-plugin/plugin.json`.
4. Check the Claude Code manifest: `claude plugin validate .`

Keep per-skill `agents/openai.yaml` files inside their skill directories: they are Codex skill metadata, not the shared agent roles in the top-level `agents/` directory.

Always try to eval skills.
