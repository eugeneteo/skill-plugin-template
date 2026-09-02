---
name: example-skill
description: Knowledge base for {{WHAT_THIS_SKILL_COVERS}}. Use when {{TRIGGER_CONDITIONS}}, citing specific provisions, or {{OTHER_TRIGGER}}.
---

# Example Skill

Replace this with the skill's core knowledge. Keep `SKILL.md` lean —
progressive-disclosure material lives in the supporting files below.

## Layout

- `references/` — deep-dive material loaded on demand (or `chapters/`,
  `cheatsheet.md`, `glossary.md`, `patterns.md` for book-to-skill skills)
- `scripts/` — optional helper scripts

## Frontmatter rules

- `name`: unquoted, kebab-case, matches the directory name.
- `description`: one sentence of what it is + "Use when …" trigger clause.
  Triggers live in the description prose, not a separate `Triggers:` list.
