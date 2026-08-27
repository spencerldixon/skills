# Skills

A collection of skills for development and workflow.

## Available skills

| Skill | Description |
| --- | --- |
| [ticket-writing](ticket-writing/) | Interviews you, researches the relevant code, and writes a clear Jira ticket following the included ticket temaplte. |

## Install

Clone the repository once:

```sh
mkdir -p "$HOME/.local/share"
git clone https://github.com/spencerdixon/skills.git "$HOME/.local/share/spencerdixon-skills"
```

### Codex

```sh
mkdir -p "$HOME/.agents/skills"
ln -s "$HOME/.local/share/spencerdixon-skills/ticket-writing" "$HOME/.agents/skills/ticket-writing"
```

Invoke it with `$ticket-writing`.

### Claude Code

```sh
mkdir -p "$HOME/.claude/skills"
ln -s "$HOME/.local/share/spencerdixon-skills/ticket-writing" "$HOME/.claude/skills/ticket-writing"
```

Invoke it with `/ticket-writing`.

Restart Codex or Claude Code if the new skill does not appear automatically.

## Update

Pull the latest version into the shared clone:

```sh
git -C "$HOME/.local/share/spencerdixon-skills" pull --ff-only
```

Because both installations are symlinks, the updated skill is available to Codex and Claude Code without copying it again. Restart the agent if it does not detect the change.
