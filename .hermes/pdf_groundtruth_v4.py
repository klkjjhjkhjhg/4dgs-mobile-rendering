#!/usr/bin/env python3
"""
pdf_groundtruth.py — for each numeric claim in fact_queue_v4, find the cited paper PDF
and search for the actual value, returning ground truth.

Approach:
1. For each fact, identify the closest \cite{...} in the same .tex
2. Map cite key → arxiv ID via paper-notes/INDEX.md
3. Read .pdfs/<arxiv-id>.pdf with pypdf
4. Search the PDF text for the value (with unit variations)
5. Return matches with surrounding context

Output: /tmp/groundtruth_v4.json
"""
import os
import re
import json
import sys
import glob

import pypdf

SURVEY_ROOT = os.path.expanduser('~/Codes/4dgs-mobile-rendering')
PDF_DIR = os.path.join(SURVEY_ROOT, '.pdfs')
NOTES_DIR = os.path.join(SURVEY_ROOT, 'docs/appendix/paper-notes')
INDEX_FILE = os.path.join(NOTES_DIR, 'INDEX.md')

# Build arxiv-id <-> cite-key mapping from INDEX.md
def load_index():
    """Returns {citekey_candidate: arxiv_id} from INDEX.md and paper-notes"""
    with open(INDEX_FILE) as f:
        idx = f.read()
    mapping = {}
    # Parse table rows: | [year-author-paper.md](year-author-paper.md) | arxiv | year | ... |
    for line in idx.split('\n'):
        m = re.search(r'\[\d{4}-([\w]+)-([\w\-]+)\.md\]\(\1-\2\.md\)\s*\|\s*(\d{4}\.\d{4,5})', line)
        if m:
            author, paper, arxiv = m.groups()
            # Generate possible cite keys: <author><year><paper>, variations
            year_match = re.search(r'(\d{4})', line)
            if year_match:
                year = year_match.group(1)
                # Try several variations
                for ck in [
                    f'{author}{year}{paper.replace("-", "")}',
                    f'{author}{year}{paper}',
                    f'{author}{year}{paper.replace("-", "gs")}',
                ]:
                    mapping[ck.lower()] = arxiv
                    mapping[ck] = arxiv
    return mapping

# Also build direct PDF->citekey mapping from .pdfs/ arxiv IDs
def load_arxiv_to_citekey():
    """Read paper-notes/ for arxiv-id and try to derive citekey"""
    mapping = {}
    for note_file in glob.glob(os.path.join(NOTES_DIR, '*.md')):
        fname = os.path.basename(note_file)
        if fname == 'INDEX.md': continue
        with open(note_file) as f:
            content = f.read()
        m = re.search(r'arxiv-id[:\s]*\*?\*?[:\s]*(\d{4}\.\d{4,5})', content)
        if not m: continue
        arxiv = m.group(1)
        # Find citekey in content (look for `\cite{xxx}` patterns near top)
        cks = re.findall(r'\\cite\{([^}]+)\}', content)
        for ck in cks[:3]:
            mapping[ck] = arxiv
        # Also derive from filename
        m2 = re.match(r'(\d{4})-([\w]+)-([\w\-]+)', fname)
        if m2:
            year, author, paper = m2.groups()
            for ck in [
                f'{author}{year}{paper.replace("-", "")}',
                f'{author}{year}{paper}',
                f'{author}{year}{paper.replace("-", "gs")}',
            ]:
                if ck not in mapping:
                    mapping[ck] = arxiv
    return mapping

# Read survey.bib for authoritative cite key -> arxiv id
def load_bib_to_arxiv():
    with open(os.path.join(SURVEY_ROOT, 'docs/survey/survey.bib')) as f:
        bib = f.read()
    result = {}
    entries = re.split(r'\n(?=@\w+\{)', bib)
    for e in entries:
        m = re.match(r'@\w+\{([^,]+),', e)
        if not m: continue
        key = m.group(1).strip()
        # Look for eprint field
        eid = re.search(r'eprint=\{(\d{4}\.\d{4,5})\}', e)
        if eid:
            result[key] = eid.group(1)
    return result

# Also read paper-notes for arxiv-id and try derive citekey
def build_citekey_to_arxiv():
    """Combined mapping"""
    result = {}
    result.update(load_bib_to_arxiv())
    # From paper-notes, get arxiv-id and back-derive citekey from filename
    for note_file in glob.glob(os.path.join(NOTES_DIR, '*.md')):
        fname = os.path.basename(note_file)
        if fname == 'INDEX.md': continue
        with open(note_file) as f:
            content = f.read()
        m = re.search(r'arxiv-id[:\s]*\*?\*?[:\s]*(\d{4}\.\d{4,5})', content)
        if not m: continue
        arxiv = m.group(1)
        # Derive citekey from filename
        m2 = re.match(r'(\d{4})-([\w]+)-([\w\-]+)', fname)
        if m2:
            year, author, paper = m2.groups()
            for ck in [
                f'{author}{year}{paper.replace("-", "")}',
                f'{author}{year}{paper}',
                f'{author}{year}{paper.replace("-", "gs")}',
                f'{author}{year}',  # short form
            ]:
                if ck not in result:
                    result[ck] = arxiv
    return result

# Read PDF text once
def read_pdf(arxiv_id, max_pages=None):
    fp = os.path.join(PDF_DIR, f'{arxiv_id}.pdf')
    if not os.path.exists(fp):
        return None
    try:
        reader = pypdf.PdfReader(fp)
        n = min(len(reader.pages), max_pages) if max_pages else len(reader.pages)
        text = ''
        for i in range(n):
            try:
                text += '\n' + reader.pages[i].extract_text()
            except:
                continue
        return text
    except Exception as e:
        return None

def find_value_in_pdf(pdf_text, value, unit, value2=None, context_window=200):
    """Search for value in PDF text, return matches with context"""
    if not pdf_text or not value: return []
    matches = []
    # Build search patterns
    patterns = []
    v = value.replace(',', '')
    # Try various formats: "30 FPS", "30fps", "30~FPS", "30 Frame Per Second"
    if unit:
        unit_lower = unit.lower()
        if unit_lower in ['fps']:
            patterns.append(re.escape(v) + r'\s*' + re.escape(unit))
            patterns.append(re.escape(v) + r'\s*[Ff]rame[s]?/[Ss]ec')
        elif unit_lower in ['mb', 'gb', 'kb']:
            patterns.append(re.escape(v) + r'\s*' + re.escape(unit))
        elif unit_lower in ['ms', 's', 'min', 'h']:
            patterns.append(re.escape(v) + r'\s*' + re.escape(unit))
        elif unit_lower in ['w', 'mw']:
            patterns.append(re.escape(v) + r'\s*' + re.escape(unit))
        elif unit_lower in ['db']:
            patterns.append(re.escape(v) + r'\s*' + re.escape(unit))
        elif unit_lower in ['%']:
            patterns.append(re.escape(v) + r'\s*%')
    else:
        # Bare number
        patterns.append(r'\b' + re.escape(v) + r'\b')
        if value2:
            v2 = value2.replace(',', '')
            patterns.append(re.escape(v) + r'\s*[\-~]\s*' + re.escape(v2))
    # Search
    for pat in patterns:
        for m in re.finditer(pat, pdf_text):
            ctx_start = max(0, m.start() - context_window)
            ctx_end = min(len(pdf_text), m.end() + context_window)
            ctx = pdf_text[ctx_start:ctx_end].replace('\n', ' ').strip()
            matches.append({
                'match': m.group(0),
                'position': m.start(),
                'context': ctx,
            })
            if len(matches) >= 5:
                return matches
    return matches

# Get cite key from fact context
def find_cite_in_context(context):
    """Extract cite key from fact context"""
    m = re.search(r'\\cite\{([^}]+)\}', context)
    if m:
        return m.group(1).split(',')[0].strip()
    return None

def main():
    # Load fact queue
    with open('/tmp/fact_queue_v4.json') as f:
        queue = json.load(f)

    # Load mappings
    bib2arxiv = build_citekey_to_arxiv()
    print(f"Loaded {len(bib2arxiv)} citekey->arxiv mappings", file=sys.stderr)

    # Build cache of PDF texts
    pdf_cache = {}
    def get_pdf(arxiv_id):
        if arxiv_id not in pdf_cache:
            pdf_cache[arxiv_id] = read_pdf(arxiv_id)
        return pdf_cache[arxiv_id]

    # Process numeric facts
    numeric_facts = [f for f in queue if f['kind'] == 'numeric']
    results = []
    for i, fact in enumerate(numeric_facts):
        if i % 50 == 0:
            print(f"Processing {i}/{len(numeric_facts)}", file=sys.stderr)
        citekey = find_cite_in_context(fact['context'])
        arxiv_id = bib2arxiv.get(citekey) if citekey else None
        if not arxiv_id:
            # Try to find ANY cite in context
            cite_m = re.search(r'\\cite\{([^}]+)\}', fact['context'])
            if cite_m:
                # Try each
                for ck in cite_m.group(1).split(','):
                    ck = ck.strip()
                    if ck in bib2arxiv:
                        arxiv_id = bib2arxiv[ck]
                        citekey = ck
                        break
        groundtruth = {
            'fact_id': fact['fact_id'],
            'citekey': citekey,
            'arxiv_id': arxiv_id,
            'value': fact.get('value'),
            'value2': fact.get('value2'),
            'unit': fact.get('unit'),
            'matches_in_pdf': [],
            'found_in_pdf': False,
        }
        if arxiv_id:
            pdf_text = get_pdf(arxiv_id)
            if pdf_text:
                matches = find_value_in_pdf(pdf_text, fact.get('value', ''), fact.get('unit', ''), fact.get('value2'))
                groundtruth['matches_in_pdf'] = matches
                groundtruth['found_in_pdf'] = len(matches) > 0
                if matches:
                    groundtruth['best_match_context'] = matches[0]['context']
        results.append(groundtruth)

    out_path = '/tmp/groundtruth_v4.json'
    with open(out_path, 'w') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    # Summary
    n_total = len(results)
    n_with_pdf = sum(1 for r in results if r['arxiv_id'])
    n_found = sum(1 for r in results if r['found_in_pdf'])
    print(f"\nTotal: {n_total}", file=sys.stderr)
    print(f"With arxiv ID: {n_with_pdf}", file=sys.stderr)
    print(f"Value found in PDF: {n_found}", file=sys.stderr)
    print(f"Written: {out_path}", file=sys.stderr)

if __name__ == '__main__':
    main()
