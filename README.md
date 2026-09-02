# {{PLUGIN_NAME}}

{{ONE_PARAGRAPH_OVERVIEW}}.

> This repository is the **plugin skeleton template**. To create a new
> plugin from it: clone, replace the `{{…}}` placeholders in
> `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`,
> `AGENTS.md`, `.github/copilot-instructions.md`, and this README, then
> drop skills into `skills/`. Delete `skills/example-skill/` when done.

## Skills

| Skill | Description | Example invoke |
|---|---|---|
| `example-skill` | What it covers | `{{PLUGIN_NAME}}:example-skill` |

## Prerequisites & Dependencies

- Claude Code (or one of the other supported agents below).
- MCP servers, runtimes, or external services the skills depend on —
  list each with its install/add command, or write "None".

## Installation

### Claude Code

```bash
claude plugin marketplace add {{GITHUB_OWNER}}/{{REPO_NAME}}
claude plugin install {{PLUGIN_NAME}}@{{REPO_NAME}}
```

### GitHub Copilot CLI

Clone the repo and point Copilot CLI at it via its instructions file
(`.github/copilot-instructions.md` is included); skills under `skills/`
are read as reference material.

```bash
git clone https://github.com/{{GITHUB_OWNER}}/{{REPO_NAME}}.git
```

### Codex

Clone the repo — the root `AGENTS.md` gives Codex the plugin context
automatically; consult `skills/*/SKILL.md` per the catalog above.

```bash
git clone https://github.com/{{GITHUB_OWNER}}/{{REPO_NAME}}.git
```

### Antigravity / Gemini CLI

Clone the repo and symlink the plugin root:

```bash
git clone https://github.com/{{GITHUB_OWNER}}/{{REPO_NAME}}.git
ln -s ~/path/to/{{REPO_NAME}} ~/.gemini/config/plugins/{{PLUGIN_NAME}}
```

## Usage Examples

One example prompt per skill.

## Sources & Keeping Fresh

Optional section — describe `sources/` conventions and how to run
`refresh/verify-primary.sh`. Delete if not applicable.

## Rules & Precedence

Optional section — summarize `rules/AGENTS.md`. Delete if not applicable.

## Versioning

Versions are semver in `.claude-plugin/plugin.json` and mirrored in the
`metadata.version` of `.claude-plugin/marketplace.json`. Bump both on
every release.
