---
name: example-skill
description: Knowledge base for {{WHAT_THIS_SKILL_COVERS}}. Use when {{TRIGGER_CONDITIONS}}, citing specific provisions, or {{OTHER_TRIGGER}}.
---

# Example Skill

Replace this with the skill's core knowledge, structured as a lean
router: this file routes, the supporting files carry the detail.

## How to use

Answer from the supporting files below; load only the section the
prompt needs. Keep `SKILL.md` at or under a 5 KB body.

## Decision rules

- Triggers live in the `description:` prose (≤400 chars, instrument
  and topic names, no dates), not a separate `Triggers:` list.
- One fact, one home: summarize here in one line and point; the
  supporting file owns the full statement, table, and citation.
- Verification lines: one per unique URL, date and marker verbatim.

## What lives where

- `references/` — deep-dive material loaded on demand (or `chapters/`,
  `cheatsheet.md`, `glossary.md`, `patterns.md` for book-to-skill skills)
- `scripts/` — optional helper scripts

## Frontmatter rules

- `name`: unquoted, kebab-case, matches the directory name.
- `description`: one sentence of what it is + "Use when …" trigger clause.
  Triggers live in the description prose, not a separate `Triggers:` list.
