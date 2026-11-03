# Plugin rules (optional)

Behavioral rules that apply whenever any skill in this plugin is active.
Delete this file if the plugin has no cross-skill rules.

- State the precedence order between skills, if one exists.
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
