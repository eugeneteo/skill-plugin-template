#!/usr/bin/env bash
# Install the {{PLUGIN_NAME}} skills into a flat-namespace skills directory.
#
# Claude Code and Copilot CLI plugin installs need no script — install
# the .claude-plugin/ manifest instead and skills are namespaced
# (/{{PLUGIN_NAME}}:search). This script is for hosts without a plugin
# concept (Codex, Antigravity, Gemini CLI, manual Copilot CLI installs),
# where each skill is known by its folder name and a generic name like
# "search" can collide with other installed skills.
#
# Each skill folder is copied to <target>/{{PLUGIN_NAME}}-<name> and the name:
# field in its SKILL.md is rewritten to match, so the installed copies
# are collision-free while this repo keeps its plain names.
#
# Usage:
#   ./install.sh <target-skills-dir> [--force]
#
# Examples:
#   ./install.sh ~/.agents/skills                # Codex / Copilot CLI
#   ./install.sh ~/.gemini/config/skills         # Antigravity / Gemini CLI
#
# Re-running refreshes existing installs only with --force.
set -euo pipefail

if [ $# -lt 1 ]; then
  echo "Usage: ./install.sh <target-skills-dir> [--force]" >&2
  exit 1
fi

TARGET="$1"
FORCE=0
[ "${2:-}" = "--force" ] && FORCE=1

REPO="$(cd "$(dirname "$0")" && pwd)"
PREFIX="${PREFIX:-{{PLUGIN_NAME}}}"

if [ ! -d "$REPO/skills" ]; then
  echo "Error: $REPO/skills not found — run from the repository root." >&2
  exit 1
fi

mkdir -p "$TARGET"

installed=0
for src in "$REPO"/skills/*/; do
  name="$(basename "$src")"
  dest="$TARGET/$PREFIX-$name"

  if [ -e "$dest" ] && [ "$FORCE" -ne 1 ]; then
    echo "skip  $dest (exists; use --force to refresh)"
    continue
  fi

  rm -rf "$dest"
  cp -R "$src" "$dest"

  # Keep the frontmatter name in sync with the (prefixed) folder name.
  sed -i '' -e "1,10s/^name: .*/name: $PREFIX-$name/" "$dest/SKILL.md" 2>/dev/null \
    || sed -i "1,10s/^name: .*/name: $PREFIX-$name/" "$dest/SKILL.md"

  # Pin the distiller path in the installed copy so it points at the
  # prefixed folder's scripts directory.
  sed -i '' -e "s|<path-to-installed-skill>/search/scripts/learn-distill.mjs|$dest/scripts/learn-distill.mjs|" "$dest/SKILL.md" 2>/dev/null \
    || sed -i "s|<path-to-installed-skill>/search/scripts/learn-distill.mjs|$dest/scripts/learn-distill.mjs|" "$dest/SKILL.md"

  echo "install  $dest"
  installed=$((installed + 1))
done

echo
echo "Done: $installed skill(s) installed to $TARGET with prefix '$PREFIX-'."
echo "Restart your agent, then confirm the skills appear (invoke e.g. /{{PLUGIN_NAME}}-<skill-name>)."
