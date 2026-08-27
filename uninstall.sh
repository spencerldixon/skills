#!/usr/bin/env bash

set -euo pipefail

readonly REPOSITORY_URL="https://github.com/spencerldixon/skills"
readonly REPOSITORY_DIR="$HOME/.local/share/spencerldixon-skills"
readonly CODEX_SKILLS_DIR="$HOME/.agents/skills"
readonly CLAUDE_SKILLS_DIR="$HOME/.claude/skills"

fail() {
  printf 'Error: %s\n' "$1" >&2
  exit 1
}

is_expected_repository() {
  local origin_url

  [ -d "$REPOSITORY_DIR/.git" ] || return 1

  origin_url="$(git -C "$REPOSITORY_DIR" remote get-url origin 2>/dev/null || true)"

  case "$origin_url" in
    "$REPOSITORY_URL" | "$REPOSITORY_URL.git" | git@github.com:spencerldixon/skills.git | ssh://git@github.com/spencerldixon/skills.git)
      return 0
      ;;
    *)
      return 1
      ;;
  esac
}

remove_skill_links() {
  local skills_dir="$1"
  local agent_name="$2"
  local removed_count=0
  local destination
  local link_target

  [ -d "$skills_dir" ] || return 0

  for destination in "$skills_dir"/*; do
    [ -L "$destination" ] || continue

    link_target="$(readlink "$destination")"
    case "$link_target" in
      "$REPOSITORY_DIR"/*)
        rm "$destination"
        printf 'Removed %s symlink %s.\n' "$agent_name" "$destination"
        removed_count=$((removed_count + 1))
        ;;
    esac
  done

  if [ "$removed_count" -eq 0 ]; then
    printf 'No installed %s symlinks found.\n' "$agent_name"
  fi
}

verify_repository_removal() {
  local expected_dir="$HOME/.local/share/spencerldixon-skills"
  [ "$REPOSITORY_DIR" = "$expected_dir" ] || fail 'Refusing to remove an unexpected repository path.'

  if [ ! -e "$REPOSITORY_DIR" ] && [ ! -L "$REPOSITORY_DIR" ]; then
    return 0
  fi

  [ ! -L "$REPOSITORY_DIR" ] || fail "$REPOSITORY_DIR is a symlink; it was not removed."
  command -v git >/dev/null 2>&1 || fail 'Git is required to verify the repository before removing it.'
  is_expected_repository || fail "$REPOSITORY_DIR is not the expected $REPOSITORY_URL clone; it was not removed."
}

remove_repository() {
  if [ ! -e "$REPOSITORY_DIR" ]; then
    printf 'Repository is already absent: %s\n' "$REPOSITORY_DIR"
    return 0
  fi

  rm -rf "$REPOSITORY_DIR"
  printf 'Removed repository %s.\n' "$REPOSITORY_DIR"
}

main() {
  verify_repository_removal
  remove_skill_links "$CODEX_SKILLS_DIR" "Codex"
  remove_skill_links "$CLAUDE_SKILLS_DIR" "Claude Code"
  remove_repository
  printf 'Uninstall complete.\n'
}

main "$@"
