# Skills

Skills for engineering work, for Claude Code, Codex and pi.

## Available skills

| Skill | Description |
| --- | --- |
| [goblin](beta/goblin/) | Fixes one demonstrable developer annoyance within 20 added plus deleted lines, with no new dependencies. Uses Opus in Claude Code. |
| [standup](skills/standup/) | Drafts a short daily update from verified activity, grouping work by outcome and marking inferred plans. |
| [code-review](beta/code-review/) | Reviews a branch or diff with a context scout and two independent reviews, merges every point into one report, and gives a pass or changes-needed verdict. |
| [find-work](beta/find-work/) | Finds up to 10 unassigned, unblocked HMRC and AI Jira tickets, rates clarity, complexity and size, and returns one ranked table to help you choose the next ticket. Read-only. |
| [write-ticket](skills/write-ticket/) | Interviews you, researches the relevant code, and writes a clear Jira ticket following the included ticket template. |
| [create-ticket](skills/create-ticket/) | Drafts and creates a Jira ticket with a verified destination and relevant parent. Defaults Trade Tariff work to HMRC Tasks in To Do. |
| [explain](skills/explain/) | Explains a ticket, file, or codebase concept in plain English with context and examples. |
| [pr-summary](skills/pr-summary/) | Writes a clear PR title and summary using the included template, with an optional Jira ticket and a deployment risk rating. |
| [walkthrough](skills/walkthrough/) | Writes a short human check for a browser, native application, or API, with exact actions and visible results. |
| [preflight](beta/preflight/) | Checks that a repo's tools, dependencies, services, disk space and one fast spec are ready before agent work starts. |
| [find-performance-issues](beta/find-performance-issues/) | Finds why a page, endpoint, job or query is slow, explains each issue in plain English, estimates the gain with the arithmetic shown, and validates it with a measurement or an exact check to run. |
| [watch-pr](skills/watch-pr/) | Runs under `/loop`: watches your open PRs, reruns flaky CI, fixes small blockers on PRs you authored, and reports every PR at a glance under Needs you, Ready to merge and Waiting. Never merges. |
| [ship-it](skills/ship-it/) | Commits your local work, pushes it, opens a pull request in each changed repo with `pr-summary`, comments the links on the Jira ticket once, and moves the ticket to In Review. |

## Agents and the wiki

`~/wiki` is the only persistent store for agent artifacts. Keep only significant project knowledge, gotchas, consequential decisions, essential WIP and documents still needed by active work. Routine progress stays in session context. Agents maintain the wiki without asking conversational permission: update canonical notes, consolidate duplicates and recoverably cull outdated or spent material. Tool-enforced approvals still apply. [`references/vault.md`](references/vault.md) defines the quality gate, maintenance and paths. No Jira key is required. Dirty trees are preserved; only ambiguous or conflicting edits require a decision.

### Customising the agents

`standup` uses `model: sonnet` in Claude Code. For OpenAI runtimes, prefer Sol when selecting the session or worker model; the Claude Code frontmatter does not configure those runtimes.

[`agents/fixer.md`](agents/fixer.md) holds the fixer role. It gets `Read, Edit, Grep, Glob, Bash, Write`; front matter sets Claude Code model `opus` and effort `medium`. Other runtimes ignore these fields; configure comparable models there.

`code-review` uses general-purpose subagents to collect facts and run independent, free-form reviews. They use read-only commands and write only their assigned report. The skill supplies their task instructions directly. Pi uses lowercase tool names, so pi needs its own copy of `fixer.md` in `~/.pi/agent/agents/`.

Keep repository-specific commands and conventions in each repo's `AGENTS.md`.

### Opening human review documents

Before a required approval or human check, open the document in Neovim in a new focused Rex pane using the short command in [`references/show-to-human.md`](references/show-to-human.md). If Rex is unavailable, report that and link the file. No helper scripts or synchronization step are needed.

## Install

Each tool installs this repo through its own marketplace or package manager. Updates come through the same tool.

### Claude Code

```sh
claude plugin marketplace add spencerldixon/skills
claude plugin install spencerldixon-skills@spencerldixon
```

Inside a session, `/plugin marketplace add spencerldixon/skills` works too. Claude Code prefixes plugin skills with the plugin name, for example `/spencerldixon-skills:watch-pr`.

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
2. Add a `## Language` section that links `references/language.md`, so every skill talks to the user the same way.
3. Add `./skills/<name>` or `./beta/<name>` to `skills` in `.claude-plugin/plugin.json`.
4. Check the Claude Code manifest: `claude plugin validate .`

Keep per-skill `agents/openai.yaml` files inside their skill directories: they are Codex skill metadata, not the shared agent roles in the top-level `agents/` directory.

Always try to eval skills.
