# {{PLUGIN_NAME}}

{{ONE_PARAGRAPH_OVERVIEW}}.

This repository is the **skill plugin template**. To create a new plugin
from it:

1. Clone the template and delete `skills/example-skill/` — and delete
   `.claude-plugin/` too if the repo will hold only one skill (see
   below).
2. Replace the `{{…}}` placeholders in `.claude-plugin/plugin.json`,
   `.claude-plugin/marketplace.json`, `AGENTS.md`,
   `.github/copilot-instructions.md`, and this README:
   - `{{PLUGIN_NAME}}` — the plugin's kebab-case name
   - `{{REPO_NAME}}` — the repository name
   - `{{GITHUB_OWNER}}` — the GitHub account that hosts the repository
   - `{{AUTHOR_NAME}}` — the maintainer's name
   - `{{SOURCE_DOCUMENTS}}` — what the skills are built from
   - `{{ONE_PARAGRAPH_OVERVIEW}}`, `{{ONE_SENTENCE_PLUGIN_DESCRIPTION}}`,
     `{{ONE_SENTENCE_MARKETPLACE_DESCRIPTION}}`, `{{WHAT_THIS_SKILL_COVERS}}`,
     `{{TRIGGER_CONDITIONS}}`, `{{OTHER_TRIGGER}}` — descriptive text
3. Add your skills to the `skills/` directory.

If the repo will hold **only one skill**, skip the plugin entirely —
see **Skills-only shape (single-skill repos)** below. A plugin needs
a reason (two or more skills, or a namespace/install story) to exist.

`claude plugin validate .` warns about the `{{…}}` placeholders until you
replace them — that is expected.

## Skills-only shape (single-skill repos)

To create a repository with standalone skills and no plugin, follow the
steps above but **delete the `.claude-plugin/` directory**. The skills
still work through the open Agent Skills standard, but you lose the
one-command plugin install and the `/plugin-name:skill` namespace. To
install, copy or symlink the skill folders into each agent's discovery
path:

| Agent | Personal path | Project path |
|---|---|---|
| Claude Code | `~/.claude/skills/<name>/` | `.claude/skills/<name>/` |
| GitHub Copilot CLI | `~/.copilot/skills/` or `~/.agents/skills/` | `.github/skills/`, `.agents/skills/` |
| Antigravity / Gemini CLI | `~/.gemini/config/skills/<name>/` | `<workspace-root>/.agents/skills/<name>/` |

**Which shape to choose:** decide by skill count first. **One skill ⇒
skills-only** — a plugin wrapper around a single skill adds nothing but
boilerplate (a second name to track, `plugin:skill` addressing for one
entry), so delete `.claude-plugin/`. Reach for the full plugin only when
the repo ships **two or more skills** that benefit from one-command
install, a shared namespace prefix, and semver releases.

**Flat-namespace hosts:** for hosts without a plugin namespace, expand
the skill names when you copy the folders — rename each folder, and its
`SKILL.md` `name:` field, which must match, to
`<plugin-name>-<skill-name>` (for example, a plugin named `acme-docs`
with a skill folder `search/` becomes `acme-docs-search`) so they cannot
collide with other installed skills.

## Skills

The following table lists the plugin's skills. Add one row per skill:

| Skill | Source | Use for |
|---|---|---|
| [example-skill](skills/example-skill/SKILL.md) | {{SOURCE_DOCUMENTS}} | What it covers |

## Skill content shape

Every `SKILL.md` in this repo follows the **router pattern** — the entry
file routes, it does not carry the detail:

- **Lean router, body ≤5 KB**: frontmatter, a how-to-use/invocation
  line, decision-rule one-liners, and a "what lives where" map. Nothing
  else.
- **`description:` ≤400 chars**: the trigger clause ("Use when …") plus
  the instrument/topic names a user would name in a prompt. No dates —
  dates live in the body or `chapters/`, where they can be re-verified.
- **Detail lives in supporting files**: `chapters/`, `references/`,
  `cheatsheet.md`, `glossary.md`, `patterns.md` — loaded on demand, so
  their size never costs always-on tokens.
- **Single source of truth per fact**: one fact, one home. The router
  summarizes in one line and points; the supporting file owns the full
  statement, table, and citation.
- **Verification lines: one per unique URL** — collapse repeated
  citation chains; keep the date and marker verbatim on that one line.
- **Quote typography is a fidelity contract**: quoted text is verbatim
  from the original source with a cite (page cite when paginated);
  the skill's own coined heuristics wear italics, never quotes.

`skills/example-skill/SKILL.md` exemplifies the shape.

## Scope policy

State what the plugin compiles and what it deliberately tracks but does
not fully summarize. The rule: listing an adjacent source is never an
accident, and omitting its summary is never an oversight — each is a
per-source scope decision recorded here or in the watch list. If the
domain has an authority hierarchy (what outranks what), summarize it
here or point to `rules/AGENTS.md`.

## Prerequisites & Dependencies

- Claude Code, or one of the other supported agents below.
- Any MCP servers, runtimes, or external services the skills depend on.
  List each with its install or add command, or write "None".

## Repository structure

Show the repository layout so readers can navigate without cloning:

```text
{{REPO_NAME}}/
├── .claude-plugin/
│   ├── plugin.json
│   └── marketplace.json   (single-plugin marketplace index)
├── rules/
│   └── AGENTS.md
├── skills/
│   └── example-skill/
├── sources/
└── refresh/
```

In a skills-only repo, `.claude-plugin/` is absent.

## Shared helpers

If your plugin needs shared fetch/cache/feed infrastructure, vendor it
from your own shared-helpers repository: run its vendoring script
against this repo, commit the resulting `lib/` and lockfile, and copy
its drift-check workflow so CI fails if the vendored copy drifts.

## Installation

The commands in this section are the plugin-shape installs used by
multi-skill repos. A skills-only repo instead copies or symlinks the
skill folders into each agent's discovery path, per the table in the
[skills-only shape](#skills-only-shape-single-skill-repos) section.

### Claude Code

Install the plugin from the repository's marketplace manifest:

```bash
claude plugin marketplace add {{GITHUB_OWNER}}/{{REPO_NAME}}
claude plugin install {{PLUGIN_NAME}}@{{REPO_NAME}}
```

If the repository built from this template is private, install from the
local working copy instead — `claude plugin marketplace add
~/path/to/{{REPO_NAME}}` — and do not add it to any public marketplace.

### GitHub Copilot CLI

Copilot CLI supports plugin marketplaces natively:

```bash
copilot plugin marketplace add {{GITHUB_OWNER}}/{{REPO_NAME}}
copilot plugin install {{PLUGIN_NAME}}@{{REPO_NAME}}
```

When working from a clone, `.github/copilot-instructions.md` gives
Copilot CLI the plugin context.

### Antigravity / Gemini CLI

Antigravity supports plugins — install from a local clone:

```bash
git clone https://github.com/{{GITHUB_OWNER}}/{{REPO_NAME}}.git
agy plugin install ~/path/to/{{REPO_NAME}}
```

Or symlink the plugin root:

```bash
ln -sfn ~/path/to/{{REPO_NAME}} ~/.gemini/config/plugins/{{PLUGIN_NAME}}
```

The root `GEMINI.md` gives Gemini CLI/Antigravity the plugin context automatically.

## Usage Examples

Provide one example prompt for each skill.

## Sources & Keeping Fresh

Optional section. Describe your `sources/` conventions and how to run
`refresh/verify-primary.sh`. Delete this section if not applicable.
Where a claim's freshness matters, carry a dated marker — "re-checked
YYYY-MM-DD" — on the heading, row, or item it applies to, and re-verify
the date each time you touch the item.

## Rules & Precedence

Optional section. Summarize `rules/AGENTS.md`. Delete this section if
not applicable.

## Watch List & Known Gaps

Optional but recommended for any plugin grounded in sources that change.
Keep a running list of:

- **Watch** items — known-stale or in-flux sources, with the dated
  re-check commitment and where to re-check.
- **Unverified** items — claims resting on secondary sources, marked
  explicitly so no skill states them as fact.
- **Verified negatives** — things checked and confirmed not to exist,
  so they are never chased again.

## Versioning

Applies only when `.claude-plugin/` exists. In a skills-only repo,
delete this section.

Versions follow semver in `.claude-plugin/plugin.json` and are mirrored
in the `metadata.version` field of `.claude-plugin/marketplace.json`.
Bump both files on every release, and state the current version in this
section — "(currently X.Y.Z)" — so README/manifest drift is visible at
a glance.

## License

This template is licensed under [GPL-3.0](LICENSE). If you keep a
repository built from this template private, the license places no
obligations on you. If you make that repository public, you must
license it under GPL-3.0 as well and include its source.

---

Template created by [@eugeneteo](https://github.com/eugeneteo).
