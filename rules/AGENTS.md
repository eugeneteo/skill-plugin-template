# Plugin rules (optional)

Behavioral rules that apply whenever any skill in this plugin is active.
Delete this file if the plugin has no cross-skill rules.

- State the precedence order between skills, if one exists.
- **Canonical corpus layout**:
  - `sources/` (or `sources/<topic>/`): Raw upstream source documents (PDF, DOCX, HTML, MD).
  - `extracts/` (or `extracts/<topic>/`): Folio extracts with anchors (`## [PDF p. N]` or `## [section N]`). Extracts MUST always live at the repository root `extracts/` (or `extracts/<topic>/` mirroring `sources/<topic>/`); never nest `extracts/` inside `sources/`.
  - `coverage/` (or `coverage/<topic>/`): Passage coverage files concluding with `Coverage:` footers.
  - `alt-index/`: Alternate index (`ideas.md`, `keywords.md`, `stories.md`).
- **Folio by default (corpus ingestion & citation)**:
  - For a webpage source, first retain a faithful browser-rendered PDF of
    the fully loaded original page in `sources/`, then extract the full PDF
    with Folio into `extracts/`. Capture relevant tabs and detail panels.
    A summary or Markdown-generated PDF does not qualify.
  - Record original/final URLs, capture time, render method and PDF hash.
    Validate rendered pages and every extraction page. Label webpage PDFs
    distinctly from issuer PDFs; cite their derived snapshot pagination.
    Missing or blocked content must remain explicitly incomplete.
  - All source document ingestion (`sources/` -> `extracts/`) must default to the
    **`folio`** skill (`python3 <path-to-folio>/scripts/folio_extract.py --sources sources/ --out extracts/`).
    Extracts must strictly follow folio standards (`## [PDF p. N]` anchors and
    `<!-- Provenance ... -->` headers).
  - Every source added to `sources/` must be paired with its rendered folio extract in
    `extracts/` before committing.
  - All page-cited quote verification and locator checking must use the **`folio`**
    skill (`folio_cite.py find / page / list`) as the normative citation interface.
- **Two-stage retrieval and index funnel** (when `alt-index/` is present):
  - **Stage 1 (Triage via index)**: Query `alt-index/` first (`ideas.md`,
    `keywords.md`, `stories.md`) to rapidly locate relevant through-lines,
    source abbreviations, and exact folio anchors (`source §p. N` or
    `§section`). Jump directly to those anchors in `extracts/` to read the
    substantive context.
  - **Stage 2 (Escalation to deep search)**: `alt-index/` is an accelerator,
    never the exhaustive verdict. Absence from `alt-index/` NEVER means absence
    from the corpus. When an index lookup misses, or when the prompt demands
    fine-grained detail (specific sub-clauses, parameters, numerical thresholds,
    or procedural edge cases), escalate immediately to targeted grep across
    `extracts/` or direct chapter reads.
  - **Grounding contract**: Never cite `alt-index/` itself as primary authority.
    All claims and quotes must be grounded in and cited to the underlying source
    document, statutory rule, or folio page.
- Quote typography is a fidelity contract: text inside quotation
  marks is verbatim from an original source and carries a cite
  (page cite when the source is paginated). The skill's own named
  heuristics and coined phrases wear italics, never quotation marks.
  Never fix a quote against its source by editing the quote; correct
  it to the source text, never the reverse.
- Keep rules short; deep knowledge belongs in skills.
