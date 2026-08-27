# Skills

A collection of skills for development and workflow.

## Available skills

| Skill | Description |
| --- | --- |
| [ticket-writing](ticket-writing/) | Interviews you, researches the relevant code, and writes a clear Jira ticket following the included ticket template. |

## Install

Run the installer from an interactive terminal:

```sh
curl -fsSL https://raw.githubusercontent.com/spencerldixon/skills/main/install.sh | bash
```

It asks whether to install the skills for Codex, Claude Code, or both. The installer:

- Clones `https://github.com/spencerldixon/skills` to
  `~/.local/share/spencerldixon-skills`.
- Creates a symlink for every skill in `~/.agents/skills` for Codex,
  `~/.claude/skills` for Claude Code, or both.
- Safely refreshes the clone and symlinks when run again.

To skip the prompt, pass `codex`, `claude`, or `both`:

```sh
curl -fsSL https://raw.githubusercontent.com/spencerldixon/skills/main/install.sh | bash -s -- both
```

## Update

Run the installer again. It pulls updates with `--ff-only` and adds symlinks for any
new skills:

```sh
curl -fsSL https://raw.githubusercontent.com/spencerldixon/skills/main/install.sh | bash
```

## Uninstall

Run the uninstaller to remove the Codex and Claude Code symlinks created by the
installer, then remove the shared repository clone:

```sh
curl -fsSL https://raw.githubusercontent.com/spencerldixon/skills/main/uninstall.sh | bash
```

The uninstaller only removes symlinks pointing into the managed clone and verifies
the repository origin before deleting it. It is safe to run again after the skills
have already been removed.
