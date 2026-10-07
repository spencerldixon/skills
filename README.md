# Skills

Skills for engineering work, for Claude Code, Codex and pi.

## Available skills

| Skill | Description |
| --- | --- |
| [developer-orchestrator](developer-orchestrator/) | Works a ticket end to end with subagents (scout, planner, implementer, reviewer), and stops for your approval after the plan and before the pull request. |
| [code-review](code-review/) | Reviews a branch or diff for real problems, each with a concrete failure scenario, and gives a pass or changes-needed verdict. |
| [find-available-work](find-available-work/) | Finds unassigned Ready to Start tickets on Jira board 155 and rates clarity and complexity to help you choose your next ticket. |
| [ticket-writing](ticket-writing/) | Interviews you, researches the relevant code, and writes a clear Jira ticket following the included ticket template. |
| [explain](explain/) | Explains a ticket, file, or codebase concept in plain English with context and examples. |
| [pr-summary](pr-summary/) | Writes a clear PR title and summary using the included template, with an optional Jira ticket and a deployment risk rating. |

## The developer orchestrator workflow

Ask your agent to work a ticket, for example "use the developer-orchestrator skill on PROJ-123" with the ticket pasted in or as a file. The orchestrator coordinates and never writes product code itself:

1. **Scout** reads the ticket and the code, and writes a brief with the exact test and lint commands.
2. **Planner** writes a plan of small tasks, each with the test that proves it. **You approve the plan.**
3. **Implementer** builds the plan test-first and commits each task.
4. The orchestrator runs the tests and linter itself, and sends failures back to the implementer.
5. **Reviewer** reviews the branch with the `code-review` skill. Blocking findings go back to the implementer.
6. The orchestrator drafts the pull request with `pr-summary`. **You approve before anything is pushed.**

Each step's output is saved in `.conductor/<run-id>/` in the repo, which git is told to ignore.

### Customising the agents

The agents are small files in [`agents/`](agents/). Each one's frontmatter sets its model tier (`small`, `mid` or `frontier`) and its tools (`read-only` or `full`). The body is its instructions. Edit a file to change an agent.

The steps, approval gates, and tier-to-model table are in [`developer-orchestrator/SKILL.md`](developer-orchestrator/SKILL.md), with a model column each for Claude Code, pi and Codex. To add an agent, add a file in `agents/` and a step in the orchestrator skill.

Skills provide reusable instructions, agents define roles, and the developer-orchestrator skill connects them. These are prompt-based definitions, not an executable runner.

Put repo-specific rules, such as test commands, conventions and known traps, in each repo's `AGENTS.md` rather than in the agents. Every subagent reads it.

## Install

Each tool installs this repo through its own marketplace or package manager. Updates come through the same tool.

### Claude Code

```sh
claude plugin marketplace add spencerldixon/skills
claude plugin install spencerldixon-skills@spencerldixon
```

Inside a session, `/plugin marketplace add spencerldixon/skills` works too. Claude Code prefixes plugin skills with the plugin name, for example `/spencerldixon-skills:developer-orchestrator`.

### Codex

```sh
codex plugin marketplace add spencerldixon/skills
codex plugin add spencerldixon-skills@spencerldixon
```

### pi

```sh
pi install git:github.com/spencerldixon/skills
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
agents/<role>.md        shared agent roles, model tiers and tool settings
uninstall.sh             removes installs made by the old install script
```

## Adding a skill

1. Create `<name>/SKILL.md` with `name` and `description` frontmatter.
2. Add `./<name>` to `skills` in `.claude-plugin/plugin.json`.
3. Check the Claude Code manifest: `claude plugin validate .`

Keep per-skill `agents/openai.yaml` files inside their skill directories: they are Codex skill metadata, not the shared agent roles in the top-level `agents/` directory.
