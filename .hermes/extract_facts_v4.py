#!/usr/bin/env python3
"""
extract_facts_v4.py — extract 4 classes of factual claims from survey.tex
- cite: \\cite{...} usage in sec-1..9
- numeric: numbers with units (FPS, MB, ms, W, dB, %, ratio, etc.)
- author: "X et al. (year)" / "X & Y" inline text references
- eval: evaluative sentences ("faster than", "achieves", "outperforms", "first/only", etc.)

Output: /tmp/fact_queue_v4.json
"""
import os
import re
import json
import sys

SURVEY_DIR = os.path.expanduser('~/Codes/4dgs-mobile-rendering/docs/survey')
SECTIONS = ['sec-1-intro.tex', 'sec-2-background.tex', 'sec-3-representation.tex',
            'sec-4-training-acceleration.tex', 'sec-5-rendering-acceleration.tex',
            'sec-6-mobile-deployment.tex', 'sec-7-datasets-metrics.tex',
            'sec-8-discussion.tex', 'sec-9-conclusion.tex']

# Patterns
RE_CITE = re.compile(r'\\cite\{([^}]+)\}')
# Numeric with units
RE_NUM = re.compile(r'\b(\d+(?:[.,]\d+)?)\s*(FPS|fps|GB/s|MB/s|KB/s|MB|GB|KB|ms|s|min|h|hr|W|mW|TFLOPs|GFLOPs|FLOPS|dB|%|\\%|×|x)\b')
# Also catch bare numbers with no explicit unit when context suggests it's a claim
# (most of these will be filtered/validated by subagent, but they need to be IN the queue)
RE_BARE_NUM = re.compile(r'(?<![\\\w\d.])(\d{1,4}(?:[.,]\d+)?)(?:\s*(?:--|-|~)\s*(\d{1,4}(?:[.,]\d+)?))?(?:\s*(FPS|MB|GB|KB|ms|W|dB|%|×|x))?')
# Author inline ref
RE_AUTHOR = re.compile(r'\\emph\{([A-Z][a-zA-Z\\-]+(?:\s+(?:et\s+al\.|and|&|\\\&)\s+[A-Z][a-zA-Z\\-]+)?)\s*(?:\\(?:20\d{2}|19\d{2})\s*\(([^)]+)\))?')
# Eval claim: "X achieves Y" / "faster than" / "outperforms" / "first" / "only" / "key"
RE_EVAL = re.compile(r'\b(achieves?|outperform[s]?|faster\s+than|slower\s+than|state-of-the-art|SOTA|first\s+to|only|first|key\s+contribution|introduces?|presents?|proposes?)\b', re.IGNORECASE)

# Better author pattern: "Chen et al. (2024)" or "Park et al." (no year), or "Simon (2017)"
RE_AUTHOR2 = re.compile(r'([A-Z][a-zA-Z]+)\s+(?:et\s+al\.|and|&|\\\&)\s+(?:al\.\s+)?\(?(20\d{2}|19\d{2})?\)?')
# In-text citation author: "X (year)" in body
RE_AUTHOR3 = re.compile(r'([A-Z][a-zA-Z\-]+)\s+\((20\d{2})\)')

def extract_from_file(filepath):
    """Extract all 4 claim classes from a .tex file"""
    with open(filepath) as f:
        text = f.read()

    facts = []
    basename = os.path.basename(filepath)

    # Get line-by-line positions
    lines = text.split('\n')
    line_starts = [0]
    for line in lines[:-1]:
        line_starts.append(line_starts[-1] + len(line) + 1)

    # === Extract cite usages ===
    for m in RE_CITE.finditer(text):
        offset = m.start()
        line_no = sum(1 for s in line_starts if s <= offset)
        # Get context (1 line before, 1 after, 200 chars each side)
        ctx_start = max(0, offset - 250)
        ctx_end = min(len(text), offset + 250)
        context = text[ctx_start:ctx_end].replace('\n', ' ').strip()
        keys = m.group(1)
        for key in re.split(r'[\s,]+', keys):
            if key:
                facts.append({
                    'kind': 'cite',
                    'subkind': 'citekey',
                    'text': m.group(0),
                    'citekey': key,
                    'file': basename,
                    'offset': offset,
                    'context': context,
                })

    # === Extract numeric ===
    for m in RE_NUM.finditer(text):
        offset = m.start()
        num = m.group(1)
        unit = m.group(2)
        ctx_start = max(0, offset - 200)
        ctx_end = min(len(text), offset + 200)
        context = text[ctx_start:ctx_end].replace('\n', ' ').strip()
        facts.append({
            'kind': 'numeric',
            'subkind': unit.lower().replace('\\%', 'percent').replace('×', 'times'),
            'text': m.group(0),
            'value': num,
            'unit': unit,
            'file': basename,
            'offset': offset,
            'context': context,
        })

    # Also bare numeric: 30, 100, 60, etc. (with optional range and unit)
    for m in RE_BARE_NUM.finditer(text):
        offset = m.start()
        # Skip if already captured by RE_NUM
        already = any(f.get('offset') == offset and f.get('kind') == 'numeric' for f in facts)
        if already: continue
        full = m.group(0).strip()
        if not full: continue
        # Skip 4-digit year alone (no range, no unit)
        if re.match(r'^\d{4}$', full):
            continue
        # Skip single-digit standalone (likely noise from list/marker)
        if re.match(r'^\d$', full):
            continue
        # Must contain range/unit OR be 2+ digit
        if not m.group(2) and not m.group(3):
            try:
                v = int(m.group(1).replace(',', ''))
                if v < 10:  # single-or-double digit without unit/range = noise
                    continue
            except:
                continue
        ctx_start = max(0, offset - 200)
        ctx_end = min(len(text), offset + 200)
        context = text[ctx_start:ctx_end].replace('\n', ' ').strip()
        unit = m.group(3)
        facts.append({
            'kind': 'numeric',
            'subkind': (unit or 'bare').lower().replace('\\%', 'percent').replace('×', 'times'),
            'text': full,
            'value': m.group(1),
            'unit': unit,
            'value2': m.group(2),
            'file': basename,
            'offset': offset,
            'context': context,
        })

    # === Extract author claims (in-text "X et al." / "X & Y" references) ===
    # v4 approach: find any capitalized word + "et al." OR "and" pattern
    RE_AUTH4 = re.compile(r'(?<!\\)\b([A-Z][a-zA-Z\u00C0-\u017F]+(?:\s+[A-Z][a-zA-Z\u00C0-\u017F]+)?)\s+(?:et\s+al\.|and|&)\s+([A-Z][a-zA-Z\u00C0-\u017F]+)')
    seen_offsets = set()
    for m in RE_AUTH4.finditer(text):
        if m.start() in seen_offsets:
            continue
        seen_offsets.add(m.start())
        offset = m.start()
        ctx_start = max(0, offset - 200)
        ctx_end = min(len(text), offset + 250)
        context = text[ctx_start:ctx_end].replace('\n', ' ').strip()
        # Check for year
        year_m = re.search(r'\b(20\d{2}|19\d{2})\b', m.group(0))
        facts.append({
            'kind': 'author',
            'subkind': 'inline_ref',
            'text': m.group(0),
            'author1': m.group(1),
            'author2': m.group(2) if m.lastindex >= 2 else None,
            'year': year_m.group(1) if year_m else None,
            'file': basename,
            'offset': offset,
            'context': context,
        })

    # Also single author "X (year)" or "X et al. (year)"
    RE_AUTH5 = re.compile(r'(?<!\\)\b([A-Z][a-zA-Z\u00C0-\u017F]+)\s+et\s+al\.\s+\((20\d{2})\)')
    for m in RE_AUTH5.finditer(text):
        offset = m.start()
        if offset in seen_offsets: continue
        seen_offsets.add(offset)
        ctx_start = max(0, offset - 200)
        ctx_end = min(len(text), offset + 200)
        context = text[ctx_start:ctx_end].replace('\n', ' ').strip()
        facts.append({
            'kind': 'author',
            'subkind': 'inline_etal',
            'text': m.group(0),
            'author1': m.group(1),
            'year': m.group(2),
            'file': basename,
            'offset': offset,
            'context': context,
        })

    # === Extract eval claims (with numeric context) ===
    for m in RE_EVAL.finditer(text):
        offset = m.start()
        ctx_start = max(0, offset - 200)
        ctx_end = min(len(text), offset + 300)
        context = text[ctx_start:ctx_end].replace('\n', ' ').strip()
        # Get the sentence containing this eval (rough)
        # Find nearest cite before
        nearby_cite = RE_CITE.search(text[max(0, offset-300):offset])
        citekey = None
        if nearby_cite:
            citekey = re.split(r'[\s,]+', nearby_cite.group(1))[0]
        # Also check for numeric in context
        num_in_ctx = RE_NUM.search(context)
        facts.append({
            'kind': 'eval',
            'subkind': 'evaluative',
            'text': m.group(0),
            'eval_word': m.group(1).lower(),
            'citekey': citekey,
            'has_number': num_in_ctx is not None,
            'file': basename,
            'offset': offset,
            'context': context,
        })

    return facts

def main():
    all_facts = []
    sec_dir = os.path.join(SURVEY_DIR, 'sections')
    for sec in SECTIONS:
        fp = os.path.join(sec_dir, sec)
        if not os.path.exists(fp):
            print(f"SKIP: {fp}", file=sys.stderr)
            continue
        facts = extract_from_file(fp)
        all_facts.extend(facts)
        print(f"{sec}: {len(facts)} facts", file=sys.stderr)

    # Dedup by (file, offset, text)
    seen = set()
    deduped = []
    for f in all_facts:
        key = (f['file'], f['offset'], f['text'])
        if key in seen: continue
        seen.add(key)
        # assign fact_id
        f['fact_id'] = f"f{len(deduped):04d}"
        deduped.append(f)

    out_path = '/tmp/fact_queue_v4.json'
    with open(out_path, 'w') as f:
        json.dump(deduped, f, indent=2, ensure_ascii=False)

    # Summary
    by_kind = {}
    for f in deduped:
        k = f['kind']
        by_kind[k] = by_kind.get(k, 0) + 1
    print(f"\nTotal: {len(deduped)} facts", file=sys.stderr)
    for k, v in sorted(by_kind.items(), key=lambda x: -x[1]):
        print(f"  {k}: {v}", file=sys.stderr)
    print(f"\nWritten: {out_path}", file=sys.stderr)

if __name__ == '__main__':
    main()
