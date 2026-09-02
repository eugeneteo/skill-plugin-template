# {{PLUGIN_NAME}}

{{ONE_PARAGRAPH_OVERVIEW}}.

This repository is the **skill plugin template**. To create a new plugin
from it:

1. Clone the template and delete `skills/example-skill/`.
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
3. Drop skills into `skills/`.

`claude plugin validate .` warns about the `{{…}}` placeholders until you
replace them — that is expected.

## Create a skills-only variant

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
| Codex | `~/.agents/skills/` | `$REPO_ROOT/.agents/skills/` |
| Antigravity / Gemini CLI | `~/.gemini/config/skills/<name>/` | `<workspace-root>/.agents/skills/<name>/` |

**Which shape to choose:** keep `.claude-plugin/` (full plugin) when you
want one-command install, the namespace prefix, and semver releases. Go
skills-only when the skills are personal or single-purpose and a
symlink-or-copy install is enough.

## Skills

The following table lists the plugin's skills. Add one row per skill:

| Skill | Source | Use for |
|---|---|---|
| [example-skill](skills/example-skill/SKILL.md) | {{SOURCE_DOCUMENTS}} | What it covers |

## Prerequisites & Dependencies

- Claude Code, or one of the other supported agents below.
- Any MCP servers, runtimes, or external services the skills depend on.
  List each with its install or add command, or write "None".

## Installation

### Claude Code

Install the plugin from the repository's marketplace manifest:

```bash
claude plugin marketplace add {{GITHUB_OWNER}}/{{REPO_NAME}}
claude plugin install {{PLUGIN_NAME}}@{{REPO_NAME}}
```

### GitHub Copilot CLI

Clone the repository. The `.github/copilot-instructions.md` file gives
Copilot CLI the plugin context, and Copilot reads the skills under
`skills/` as reference material:

```bash
git clone https://github.com/{{GITHUB_OWNER}}/{{REPO_NAME}}.git
```

### Codex

Clone the repository. The root `AGENTS.md` gives Codex the plugin context
automatically, and Codex consults `skills/*/SKILL.md` per the catalog
above:

```bash
git clone https://github.com/{{GITHUB_OWNER}}/{{REPO_NAME}}.git
```

### Antigravity / Gemini CLI

Clone the repository and symlink the plugin root:

```bash
git clone https://github.com/{{GITHUB_OWNER}}/{{REPO_NAME}}.git
ln -sfn ~/path/to/{{REPO_NAME}} ~/.gemini/config/plugins/{{PLUGIN_NAME}}
```

## Usage Examples

Provide one example prompt for each skill.

## Sources & Keeping Fresh

Optional section. Describe your `sources/` conventions and how to run
`refresh/verify-primary.sh`. Delete this section if not applicable.

## Rules & Precedence

Optional section. Summarize `rules/AGENTS.md`. Delete this section if
not applicable.

## Versioning

Versions follow semver in `.claude-plugin/plugin.json` and are mirrored
in the `metadata.version` field of `.claude-plugin/marketplace.json`.
Bump both files on every release.

## License

This template is licensed under [GPL-3.0](LICENSE). If you build a
plugin or skill repository from this template and make it public, you
must license that repository under GPL-3.0 as well and include its
source. Private, unpublished use has no obligations.
