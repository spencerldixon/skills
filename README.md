# Skills

Skills for engineering work, for Claude Code, Codex and pi.

## Available skills

| Skill | Description |
| --- | --- |
| [engineer](engineer/) | Runs a change from spec to pull request: approved spec, implementation subagent, reviewer subagent, then `ship-it`. |
| [code-review](code-review/) | Reviews a branch or diff for real problems, each with a concrete failure scenario, and gives a pass or changes-needed verdict. |
| [find-work](find-work/) | Finds unassigned, unblocked Ready to Start and To Do tickets across every Jira project you can access and rates clarity and complexity to help you choose your next ticket. |
| [write-ticket](write-ticket/) | Interviews you, researches the relevant code, and writes a clear Jira ticket following the included ticket template. |
| [create-ticket](create-ticket/) | Drafts and creates a Jira ticket with a verified destination and relevant parent. Defaults Trade Tariff work to HMRC Tasks in To Do. |
| [explain](explain/) | Explains a ticket, file, or codebase concept in plain English with context and examples. |
| [pr-summary](pr-summary/) | Writes a clear PR title and summary using the included template, with an optional Jira ticket and a deployment risk rating. |
| [walkthrough](walkthrough/) | Writes a short human check for a browser, native application, or API, with exact actions and visible results. |
| [preflight](preflight/) | Checks that a repo's tools, dependencies, services, disk space and one fast spec are ready before agent work starts. |
| [find-performance-issues](find-performance-issues/) | Finds low to medium effort performance fixes, such as N+1 queries, slow subqueries and repeated work, that give at least a 2x gain, and rates each by effort and gain. |
| [agent-feedback](agent-feedback/) | Lets agents record lessons and suggest instruction, tool or process changes, for you to approve. |
| [ship-it](ship-it/) | Commits your local work, pushes it, opens a pull request in each changed repo with `pr-summary`, comments the links on the Jira ticket once, and moves the ticket to In Review. |

## The engineer workflow

Ask for a ticket implementation or a bounded fix. The engineer:

1. Runs `preflight`, then writes a spec and opens it for your approval.
2. Implements the approved spec with a subagent.
3. Runs the `reviewer` subagent: lint with autocorrect, `code-review`, the test suite, and an optional `walkthrough`.
4. Reports the review and a plain-English roundup, then runs `ship-it` if you approve.
5. Runs `agent-feedback`; proposed instruction changes are applied only with approval.

Reports are written once. Agents start with fresh context, receive file paths, and return a path plus a short outcome. The coordinator keeps verification and decisions in one `status.md`.

Artifacts default to `~/.local/state/engineer/<repo>/<task-id>/`, outside the repository. Set `ENGINEER_ARTIFACT_ROOT` or supply a directory to change it. No Jira key is required for local work. Dirty trees are recorded and preserved; only ambiguous or conflicting edits require a decision.

### Customising the agents

[`agents/reviewer.md`](agents/reviewer.md) holds the reviewer role. It gets `Read, Grep, Glob, Bash, Write`; front matter sets Claude Code model `opus` and effort `medium`. The engineer and its implementation subagent run on the session model. Other runtimes ignore these fields; configure comparable models there.

Keep repository-specific commands and conventions in each repo's `AGENTS.md`. The workflow and role reports should reference facts once, not repeat the conversation.

### Opening human review documents

Before a required approval or human check, open the document in Neovim in a new focused Rex pane using the short command in [`references/human-review.md`](references/human-review.md). If Rex is unavailable, report that and link the file. No helper scripts or synchronization step are needed.

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
<name>/SKILL.md          reusable skills and orchestrators (Agent Skills format)
agents/<role>.md        shared agent roles and write scopes
references/             shared human review procedure
```

## Adding a skill

1. Create `<name>/SKILL.md` with `name` and `description` frontmatter.
2. Copy the `## Language` section from another skill, so every skill talks to the user the same way.
3. Add `./<name>` to `skills` in `.claude-plugin/plugin.json`.
4. Check the Claude Code manifest: `claude plugin validate .`

Keep per-skill `agents/openai.yaml` files inside their skill directories: they are Codex skill metadata, not the shared agent roles in the top-level `agents/` directory.

Always try to eval skills.
