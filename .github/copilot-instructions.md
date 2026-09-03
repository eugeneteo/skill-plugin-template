# {{PLUGIN_NAME}} — GitHub Copilot instructions

This repository is a Claude Code plugin exposing skills under `skills/`.

- Skill catalog and usage: see `README.md` (§ Skills).
- Behavioral rules that bind when any skill is active: `rules/AGENTS.md`.
- Skill frontmatter (`name`, `description`) in each `skills/*/SKILL.md`
  is the trigger contract — consult the matching skill for its topics.

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
  - Any other agent with its own documented convention → use that
    agent's own trailer.
  - Unknown/undocumented agent → omit the trailer rather than guess.

Keep this file in sync with the root `AGENTS.md` and `CLAUDE.md`.
