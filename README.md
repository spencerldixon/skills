# Skills

Skills for engineering work, for Claude Code, Codex and pi.

## Available skills

| Skill | Description |
| --- | --- |
| [engineer](engineer/) | Implements bounded fixes with an implementor and independent reviewer; adds planning and approval when material decisions need them. |
| [code-review](code-review/) | Reviews a branch or diff for real problems, each with a concrete failure scenario, and gives a pass or changes-needed verdict. |
| [designer](designer/) | Designs minimalist interfaces with Basecoat UI and Tailwind, with accessibility, responsive layout, copy, performance, and SEO checks. |
| [find-available-work](find-available-work/) | Finds unassigned Ready to Start tickets on Jira board 155 and rates clarity and complexity to help you choose your next ticket. |
| [write-ticket](write-ticket/) | Interviews you, researches the relevant code, and writes a clear Jira ticket following the included ticket template. |
| [explain](explain/) | Explains a ticket, file, or codebase concept in plain English with context and examples. |
| [pr-summary](pr-summary/) | Writes a clear PR title and summary using the included template, with an optional Jira ticket and a deployment risk rating. |
| [walkthrough](walkthrough/) | Writes a short human check for a browser, native application, or API, with exact actions and visible results. |
| [ship-it](ship-it/) | Commits your local work, pushes it, opens a pull request in each changed repo with `pr-summary`, comments the links on the Jira ticket once, and moves the ticket to In Review. |

## The engineer workflow

Ask for a ticket implementation or a bounded fix. The engineer delegates product code and preserves existing work:

1. **Clear fix:** implementor builds it, the coordinator verifies, and an independent reviewer checks it.
2. **Uncertain design:** planner first writes a concise plan. Approval is needed only for material unapproved decisions or an explicitly requested plan gate.
3. **Unverified UI/device behavior:** reviewer supplies a short human check. Required approval/check documents open automatically in Neovim in a new Ghostty tab.
4. Publish only with authorization; `ship-it` handles its stated external actions.

Reports are written once. Agents start with fresh context, receive file paths, and return a path plus a short outcome. The coordinator keeps verification and decisions in one `status.md`.

Artifacts default to `~/.local/state/engineer/<repo>/<task-id>/`, outside the repository. Set `ENGINEER_ARTIFACT_ROOT` or supply a directory to change it. No Jira key is required for local work. Dirty trees are recorded and preserved; only ambiguous or conflicting edits require a decision.

### Customising the agents

[`agents/`](agents/) contains the planner, implementor, and reviewer instructions. `tools: report-only` means product files are read-only but the assigned report can be written; `tools: full` permits authorized implementation. These definitions are prompts, not an executable runner or enforced sandbox. Configure runner permissions to match.

The runtime's default model is used unless an available model is configured per role. There are no implied model tiers or claimed savings. A cheaper implementor can suit a precise task; preserve independent review and stronger reasoning where uncertainty matters.

Keep repository-specific commands and conventions in each repo's `AGENTS.md`. The workflow and role reports should reference facts once, not repeat the conversation.

### Opening human review documents

Before a required approval or human check, open the document in Neovim in a new Ghostty tab using the short command in [`references/human-review.md`](references/human-review.md). If macOS automation is blocked, report that and link the file. No helper scripts or synchronization step are needed.

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
uninstall.sh             removes installs made by the old install script
```

## Adding a skill

1. Create `<name>/SKILL.md` with `name` and `description` frontmatter.
2. Copy the `## Language` section from another skill, so every skill talks to the user the same way.
3. Add `./<name>` to `skills` in `.claude-plugin/plugin.json`.
4. Check the Claude Code manifest: `claude plugin validate .`

Keep per-skill `agents/openai.yaml` files inside their skill directories: they are Codex skill metadata, not the shared agent roles in the top-level `agents/` directory.
