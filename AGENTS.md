# {{PLUGIN_NAME}}

This repository is a Claude Code plugin exposing skills under `skills/`.

- Skill catalog and usage: see `README.md` (§ Skills).
- Behavioral rules that bind when any skill is active: `rules/AGENTS.md`.
- Skill frontmatter (`name`, `description`) in each `skills/*/SKILL.md`
  is the trigger contract — invoke the matching skill for its topics.

This root `AGENTS.md` exists so Codex-compatible agents pick up the same
context automatically.
