# {{PLUGIN_NAME}}

This repository exposes skills under `skills/` — as a Claude Code
plugin when `.claude-plugin/` is present, otherwise as standalone
skills (the default for single-skill repos).

- Skill catalog and usage: see `README.md` (§ Skills).
- Behavioral rules that bind when any skill is active: `rules/AGENTS.md`.
- Skill frontmatter (`name`, `description`) in each `skills/*/SKILL.md`
  is the trigger contract — invoke the matching skill for its topics.

## Skill content shape

Each `SKILL.md` is a lean router (body ≤5 KB): frontmatter, a
how-to-use line, decision-rule one-liners, and a what-lives-where map.
`description:` stays ≤400 chars — trigger clause plus instrument/topic
names, no dates. Detail lives in `chapters/`/`references/`/
`cheatsheet.md`; each fact has exactly one home; verification lines are
one per unique URL. Do not grow `SKILL.md` instead of a supporting file.

## Git commit conventions

All commits in this repo follow:

- **Subject**: ≤50 characters, imperative mood, no trailing period, no
  `Initial:`/`Audit:`-style prefixes — the type lives in the verb.
- **Body**: explains why + what, wrapped at 72 characters, with bulleted
  detail where it aids scanning.
- **Layout**: blank line between subject and body.
- **Co-author trailer**: include a `Co-authored-by` trailer identifying
  the coding agent that authored the commit, using that agent's own
  convention — never another agent's:
  - Claude Code → `Co-Authored-By: Claude Code <noreply@anthropic.com>`
  - GitHub Copilot CLI →
    `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`
  - Antigravity →
    `Co-Authored-By: Antigravity <antigravity-cli@google.com>`
  - Any other agent with its own documented convention → use that
    agent's own trailer.
  - Unknown/undocumented agent → omit the trailer rather than guess.

This root `AGENTS.md` is the shared source of truth for agents that
read it natively. `CLAUDE.md`, `.github/copilot-instructions.md`, and
`GEMINI.md` each import it via `@AGENTS.md` (or `@../AGENTS.md` from
`.github/`) so all agent adapters stay in sync automatically.
