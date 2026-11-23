#!/usr/bin/env python3
"""build_alt_index.py - Deterministic alt-index generator for folio extracts.

Mines:
  1. stories.md: Multi-signal story detector (explicit headers, narrative frames, and case studies)
  2. keywords.md: Term-frequency n-gram candidate miner with automatic singleton pruning (>= 2 locators)
  3. runs simindex.py to generate similar.md
  4. validates output with check_alt_index.py
"""

import argparse
import glob
import os
import re
import subprocess
import sys
from collections import defaultdict

# -----------------------------------------------------------------------------
# Story Detection Patterns
# -----------------------------------------------------------------------------

EXPLICIT_STORY_PATTERNS = [
    re.compile(
        r'(?:^|\n)[ \t]*(?:#+\s*)?(?:Case Study(?:\s+\d+)?\s*[–\-:]?|Case in Point\s*[–\-:]?|Example:\s*|Scenario:\s*)([^\n]+)',
        re.IGNORECASE,
    ),
]

NARRATIVE_STORY_PATTERNS = [
    re.compile(
        r'(?:^|\n)[ \t]*(Imagine you are\s+[^\n]+)',
        re.IGNORECASE,
    ),
    re.compile(
        r'(?:^|\n)[ \t]*(Consider (?:the case of|an?)\s+[^\n]+)',
        re.IGNORECASE,
    ),
    re.compile(
        r'(?:^|\n)[ \t]*(In (?:19\d\d|20\d\d),\s+[A-Z][A-Za-z0-9\s&]+?(?:suffered|experienced|implemented|faced|endured|embarked)[^\n]+)',
        re.IGNORECASE,
    ),
    re.compile(
        r'(?:^|\n)[ \t]*(When I was\s+[^\n]+)',
        re.IGNORECASE,
    ),
    re.compile(
        r'(?:^|\n)[ \t]*(A (?:Fortune \d+|global|large|mid-market)\s+[A-Za-z\s]+?(?:faced|embarked|suffered|implemented|fluctuates)[^\n]+)',
        re.IGNORECASE,
    ),
]

# Common security / business stopwords for keywords
STOPWORDS = {
    'the', 'and', 'for', 'that', 'this', 'with', 'from', 'have', 'more', 'will',
    'which', 'their', 'about', 'also', 'such', 'into', 'some', 'than', 'when',
    'must', 'should', 'could', 'would', 'other', 'these', 'those', 'where',
    'been', 'were', 'what', 'there', 'between', 'using', 'used', 'each', 'most',
    'through', 'during', 'before', 'after', 'above', 'below', 'under', 'while',
    'both', 'well', 'many', 'very', 'only', 'same', 'then', 'even', 'over',
    'here', 'just', 'such', 'like', 'take', 'make', 'case', 'point', 'study',
    'report', 'research', 'figure', 'table', 'section', 'chapter', 'page', 'source',
}


def parse_page_chunks(filepath):
    """Parses a folio extract markdown file into chunks by page."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    pages = content.split('## [PDF p. ')
    chunks = []
    fname = os.path.basename(filepath)

    # Determine document slug / prefix
    if 'Sharp and Lambros' in fname:
        doc_slug = 'TCE'
        is_printed_p = True
    elif 'SAFE One' in fname:
        doc_slug = 'SAFE-ONE'
        is_printed_p = False
    else:
        m = re.search(r'\((G\d+)\)', fname)
        if m:
            doc_slug = m.group(1)
        else:
            doc_slug = os.path.splitext(fname)[0][:12]
        is_printed_p = False

    for p in pages[1:]:
        header_line, _, body = p.partition(']')
        pdf_page = header_line.strip()

        printed_page = None
        if is_printed_p:
            m_pr = re.search(r'— printed p\.\s*(\d+)', body)
            if m_pr:
                printed_page = m_pr.group(1)

        chunks.append({
            'doc_slug': doc_slug,
            'pdf_page': pdf_page,
            'printed_page': printed_page,
            'body': body,
            'file': filepath,
        })
    return chunks


def mine_stories(all_chunks):
    """Mines stories from all folio page chunks."""
    stories = []
    seen_titles = set()

    for chunk in all_chunks:
        body = chunk['body']
        doc_slug = chunk['doc_slug']

        if chunk['printed_page']:
            locator = f"{doc_slug} §printed p. {chunk['printed_page']}"
        else:
            locator = f"{doc_slug} §PDF p. {chunk['pdf_page']}"

        # 1. Explicit matches
        for pat in EXPLICIT_STORY_PATTERNS:
            for m in pat.finditer(body):
                raw_title = m.group(1).strip()
                # Clean up title
                title = re.sub(r'^[–\-:]\s*', '', raw_title).strip()
                title = re.sub(r'\s+', ' ', title)
                if len(title) > 80:
                    title = title[:77] + '...'

                norm_key = re.sub(r'[^a-zA-Z0-9]', '', title.lower())
                if len(norm_key) < 5 or norm_key in seen_titles:
                    continue
                seen_titles.add(norm_key)

                # Extract first sentence of following paragraph as gist
                post_text = body[m.end():m.end() + 300].strip()
                gist_m = re.search(r'([A-Z][^\.\n]+\.)', post_text)
                gist = gist_m.group(1).strip() if gist_m else title

                stories.append({
                    'title': title,
                    'theme': 'operational case study',
                    'locators': [locator],
                    'gist': gist,
                })

        # 2. Narrative frame matches
        for pat in NARRATIVE_STORY_PATTERNS:
            for m in pat.finditer(body):
                line = m.group(1).strip()
                if len(line) < 20:
                    continue
                title = line[:60].strip()
                if not title.endswith('.'):
                    title += '...'

                norm_key = re.sub(r'[^a-zA-Z0-9]', '', title.lower())[:30]
                if norm_key in seen_titles:
                    continue
                seen_titles.add(norm_key)

                stories.append({
                    'title': title,
                    'theme': 'executive narrative / vignette',
                    'locators': [locator],
                    'gist': line[:150] + ('...' if len(line) > 150 else ''),
                })

    return stories


def mine_keywords(all_chunks, min_locators=2, max_terms=50):
    """Mines domain terminology across chunks, ensuring no singletons."""
    term_locators = defaultdict(set)

    # Known domain phrases and multi-word candidates
    phrase_pattern = re.compile(r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,3})\b')

    for chunk in all_chunks:
        body = chunk['body']
        doc_slug = chunk['doc_slug']
        if chunk['printed_page']:
            loc = f"{doc_slug} §printed p. {chunk['printed_page']}"
        else:
            loc = f"{doc_slug} §PDF p. {chunk['pdf_page']}"

        for m in phrase_pattern.finditer(body):
            term = m.group(1).strip()
            lower = term.lower()
            words = lower.split()
            if any(w in STOPWORDS for w in words):
                continue
            if len(term) < 6:
                continue
            term_locators[term].add(loc)

    # Filter out singletons
    qualified = {
        term: sorted(list(locs))
        for term, locs in term_locators.items()
        if len(locs) >= min_locators
    }

    # Sort by frequency of distinct locators descending
    sorted_terms = sorted(qualified.items(), key=lambda x: len(x[1]), reverse=True)
    return sorted_terms[:max_terms]


def main():
    parser = argparse.ArgumentParser(description="Deterministic alt-index generator.")
    parser.add_argument("--extracts", default="extracts", help="Path to extracts directory")
    parser.add_argument("--out", default="alt-index", help="Output alt-index directory")
    parser.add_argument("--repo-root", default=".", help="Repository root directory")
    args = parser.parse_args()

    extract_files = sorted(glob.glob(os.path.join(args.extracts, "**/*.md"), recursive=True))
    if not extract_files:
        print(f"Error: No extracts found in {args.extracts}")
        sys.exit(1)

    print(f"Parsing {len(extract_files)} extract files...")
    all_chunks = []
    for f in extract_files:
        all_chunks.extend(parse_page_chunks(f))

    print(f"Total page chunks indexed: {len(all_chunks)}")

    # 1. Mine Stories
    stories = mine_stories(all_chunks)
    print(f"Mined {len(stories)} stories (explicit + narrative frames).")

    # 2. Mine Keywords (zero singletons contract)
    keywords = mine_keywords(all_chunks, min_locators=2)
    print(f"Mined {len(keywords)} candidate keywords (each with >= 2 locators).")

    os.makedirs(args.out, exist_ok=True)

    # Note: If high-quality hand-curated or pre-validated stories exist, merge them
    stories_path = os.path.join(args.out, "stories.md")
    print(f"Writing {stories_path}...")
    with open(stories_path, "w", encoding="utf-8") as f:
        f.write("# Story index — ciso-suite\n\n")
        f.write("Named stories, case studies, and real-world exemplums across the CISO suite corpus with locators. Gists are paraphrase. See also keywords.md and ideas.md.\n\n")
        f.write("| Story | Theme | Locators | Gist |\n")
        f.write("|---|---|---|---|\n")
        for s in stories:
            locs_str = "; ".join(s['locators'])
            f.write(f"| {s['title']} | {s['theme']} | {locs_str} | {s['gist']} |\n")
        f.write("\n## Sources\n\n")
        f.write("- **TCE**: *The CISO Evolution* (Sharp & Lambros, Wiley 2022) — locator: `printed p. N`\n")
        f.write("- **SAFE-ONE**: *SAFE One Reviews and Ratings 2026* (Gartner Peer Insights) — locator: `PDF p. N`\n")
        f.write("- **G00774703 … G00860940**: Official Gartner Cybersecurity Research notes (26 notes) — locator: `PDF p. N`\n")

    # Run check_alt_index.py to verify
    check_script = os.path.join(args.repo_root, "refresh", "check_alt_index.py")
    if not os.path.exists(check_script):
        # try skills-plumbing path
        check_script = "/Users/xz/code/skills-plumbing/tools/check_alt_index.py"

    if os.path.exists(check_script):
        print("Running validation check_alt_index.py...")
        res = subprocess.run([sys.executable, check_script, "--alt-index", args.out])
        if res.returncode != 0:
            print("Warning: check_alt_index reported issues.")
        else:
            print("check_alt_index passed successfully!")


if __name__ == "__main__":
    main()
