#!/usr/bin/env bash

set -euo pipefail

readonly REPOSITORY_URL="https://github.com/spencerldixon/skills"
readonly REPOSITORY_DIR="$HOME/.local/share/spencerldixon-skills"
readonly CODEX_SKILLS_DIR="$HOME/.agents/skills"
readonly CLAUDE_SKILLS_DIR="$HOME/.claude/skills"
target=""

usage() {
  printf 'Usage: %s [codex|claude|both]\n' "$(basename "$0")"
}

fail() {
  printf 'Error: %s\n' "$1" >&2
  exit 1
}

read_selection() {
  local answer

  if [ -t 0 ]; then
    IFS= read -r answer
  elif [ -r /dev/tty ]; then
    IFS= read -r answer </dev/tty
  else
    return 1
  fi

  printf '%s\n' "$answer"
}

choose_target() {
  local selection

  if [ "$#" -gt 1 ]; then
    usage >&2
    exit 1
  fi

  if [ "$#" -eq 1 ]; then
    selection="$1"
  else
    printf 'Install skills for:\n'
    printf '  1) Codex\n'
    printf '  2) Claude Code\n'
    printf '  3) Both\n'
    printf 'Choose 1, 2, or 3: '

    if ! selection="$(read_selection)"; then
      fail 'No interactive terminal found. Pass codex, claude, or both as an argument.'
    fi
  fi

  case "$selection" in
    1 | codex)
      target="codex"
      ;;
    2 | claude)
      target="claude"
      ;;
    3 | both)
      target="both"
      ;;
    *)
      usage >&2
      fail 'Choose codex, claude, or both.'
      ;;
  esac
}

update_repository() {
  local origin_url

  command -v git >/dev/null 2>&1 || fail 'Git is required to install these skills.'

  mkdir -p "$(dirname "$REPOSITORY_DIR")"

  if [ -L "$REPOSITORY_DIR" ]; then
    fail "$REPOSITORY_DIR is a symlink; refusing to use it as the managed clone."
  elif [ -d "$REPOSITORY_DIR/.git" ]; then
    origin_url="$(git -C "$REPOSITORY_DIR" remote get-url origin 2>/dev/null || true)"

    case "$origin_url" in
      "$REPOSITORY_URL" | "$REPOSITORY_URL.git" | git@github.com:spencerldixon/skills.git | ssh://git@github.com/spencerldixon/skills.git)
        ;;
      *)
        fail "$REPOSITORY_DIR already exists but is not a clone of $REPOSITORY_URL"
        ;;
    esac

    printf 'Updating %s...\n' "$REPOSITORY_DIR"
    git -C "$REPOSITORY_DIR" pull --ff-only
  elif [ -e "$REPOSITORY_DIR" ]; then
    fail "$REPOSITORY_DIR already exists and is not a Git repository."
  else
    printf 'Cloning %s...\n' "$REPOSITORY_URL"
    git clone "$REPOSITORY_URL" "$REPOSITORY_DIR"
  fi
}

check_destinations() {
  local skills_dir="$1"
  local skill_file
  local skill_dir
  local destination

  for skill_file in "$REPOSITORY_DIR"/*/SKILL.md; do
    [ -f "$skill_file" ] || continue

    skill_dir="${skill_file%/SKILL.md}"
    destination="$skills_dir/$(basename "$skill_dir")"

    if [ -e "$destination" ] && [ ! -L "$destination" ]; then
      fail "$destination already exists and is not a symlink."
    fi
  done
}

install_skills() {
  local skills_dir="$1"
  local agent_name="$2"
  local installed_count=0
  local skill_file
  local skill_dir
  local destination

  mkdir -p "$skills_dir"

  for skill_file in "$REPOSITORY_DIR"/*/SKILL.md; do
    [ -f "$skill_file" ] || continue

    skill_dir="${skill_file%/SKILL.md}"
    destination="$skills_dir/$(basename "$skill_dir")"
    ln -sfn "$skill_dir" "$destination"
    printf 'Linked %s for %s.\n' "$(basename "$skill_dir")" "$agent_name"
    installed_count=$((installed_count + 1))
  done

  if [ "$installed_count" -eq 0 ]; then
    fail "No skills were found in $REPOSITORY_DIR."
  fi
}

main() {
  choose_target "$@"
  update_repository

  case "$target" in
    codex)
      check_destinations "$CODEX_SKILLS_DIR"
      install_skills "$CODEX_SKILLS_DIR" "Codex"
      ;;
    claude)
      check_destinations "$CLAUDE_SKILLS_DIR"
      install_skills "$CLAUDE_SKILLS_DIR" "Claude Code"
      ;;
    both)
      check_destinations "$CODEX_SKILLS_DIR"
      check_destinations "$CLAUDE_SKILLS_DIR"
      install_skills "$CODEX_SKILLS_DIR" "Codex"
      install_skills "$CLAUDE_SKILLS_DIR" "Claude Code"
      ;;
  esac

  printf 'Done. Restart your agent if the skills do not appear automatically.\n'
}

main "$@"
