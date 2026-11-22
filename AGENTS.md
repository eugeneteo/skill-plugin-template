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


## Source naming convention

Primary sources in `sources/` are strictly named `YYYYMMDD - Title.ext`:

- `YYYYMMDD` is the document's own date (issue, effective, or publication date),
  or the capture date for a web-page snapshot. Where a document is undated, use
  `YYYYMM00` from its best-evidence date and flag it as approximate in the inventory.
- `.pdf` for original documents and browser-rendered webpage snapshots,
  distinguished by a `(webpage PDF)` suffix. `.html` and `.md` may supplement
  snapshots, not replace them. `.xlsx` is for spreadsheet deliverables.
- Suffixes in parentheses mark provenance and status: `(page)`,
  `(page snapshot)`, `(page capture)`, `(public capture)`,
  `(public portal capture)`, `(narrative capture)` for web captures;
  `(informal consolidation, SSO)`, `(SSO capture)`, `(SSO print view, full text)`,
  `(Acts Supp …, SSO)`, `(Bill …, SSO Bills Supplement)` for statutory materials;
  `(draft)` / `(draft v1.0)` for unpublished drafts, `(consultation)` for
  consultation-stage material, and `(press release)` for media releases.
- No original loose download names (e.g. `download (1).pdf`, `temp.html`).

## Webpage source capture

For a primary source published as a webpage, retain a faithful PDF of the
fully loaded original webpage in `sources/`, then use **Folio** to create
its full page-anchored extraction in `extracts/`. A summary, rewritten
document or Markdown-generated PDF is not a primary-source snapshot.
Capture all relevant tabs, expanded content and detail panels. Validate
the rendered pages and extraction for missing content, blank tables,
clipping and unloaded sections.

Record original/final URLs, capture time, render method and PDF SHA-256.
Use the capture date in the filename and preserve the publication date
separately where verified. Cite the snapshot's derived PDF pages, not
invented issuer pagination. Retain original issuer PDFs separately.
Blocked or incomplete capture/extraction remains an explicit gap, never
a complete source record. See `rules/AGENTS.md`.

`extracts/` is committed; ignore only its scratch dirs and licensed-source
paths (path-specific carve-outs with a naming `.gitignore` comment). Each
extract carries overlay provenance (`overlay base:` / `unique-to:` header
plus per-page overlay comments); cite the base slug for carried-over
facts, the source's own slug for unique facts. See `rules/AGENTS.md`.

## Corpus & Alternative Index Maintenance

Whenever new source documents, extracts (`extracts/`), or regulatory guidance chapters are added or substantially revised in this repository:
- All source documents in `sources/` must be ingested via the **`folio`** skill by default (`python3 <path-to-folio>/scripts/folio_extract.py --sources sources/`), ensuring 100% passage coverage with zero gaps.
- Rerun the alternative index prompt (`/Users/xz/code/skills-plumbing/prompts/alt-index.md`) to regenerate `alt-index/keywords.md`, `alt-index/ideas.md`, `alt-index/stories.md`, and `alt-index/similar.md` (via `simindex.py`).
- Maintain index currency so that cross-document synthesis and page-anchored locators remain synchronized with the underlying extracts.

## Work tracking & docs currency

No `TODO.md` — actionable work lives as GitHub issues; changes land as
PRs or commits. When changing anything, update every relevant `.md`
(README, AGENTS, rules, SKILL descriptions) in the same change. See
`rules/AGENTS.md`.

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

## Fleet registry

This repo is catalogued in the fleet registry at
`~/code/skills-registry` (PRIVATE — never make it public). At the end
of every work session that changes this repo's skills, sources, or
reports — **before committing**:

1. Run
   `~/code/skills-plumbing/tools/registry-update.sh <this-repo-dirname> "<one-line status>"`
   to set the `Last status:` line in `registry/<repo>.md`.
2. Update this repo's row in `registry` repo's `CATALOG.md`
   (status / last commit / notes; folio coverage if the corpus changed).
3. Commit and push `skills-registry`.

Local-only repos (no GitHub remote) are not catalogued — see
`~/code/LOCAL-ONLY-REPOS.md`.

## Source chronology and precedence

Repos built from multiple source documents keep a chronology file
(e.g. `DOC-CHRONOLOGY.md` at the repo root) recording each source's
publication year, and **declare a precedence direction** — this is
domain-dependent and must be stated explicitly:

- **Newest-wins** for methods, standards, and technical guidance:
  when sources disagree, the later-published source supersedes the
  earlier; skills flag superseded content (cite both), never merge
  definitions.
- **Oldest-wins** for classical texts and historical sources: the
  earliest edition is the authoritative record; later editions are
  interpretations and are cited as such, never silently substituted.

Mechanics regardless of direction: verify years from title/copyright
pages at build time; record per-document offsets and cite tags; when
two sources diverge, present the divergence explicitly with both
cites.

This root `AGENTS.md` is the shared source of truth for agents that
read it natively. `CLAUDE.md`, `.github/copilot-instructions.md`, and
`GEMINI.md` each import it via `@AGENTS.md` (or `@../AGENTS.md` from
`.github/`) so all agent adapters stay in sync automatically.
