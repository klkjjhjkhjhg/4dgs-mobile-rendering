#!/usr/bin/env python3
"""add_bib_entries.py

v5.45 ff: 用 paper note 0.5 元数据段 (venue / arxiv-id / 作者 / 标题) 生成
bib entry, 把 bib 从 60 → 100+.

用法:
  python3 scripts/add_bib_entries.py            # dry run, 只 print
  python3 scripts/add_bib_entries.py --apply    # 实际 modify survey.bib
"""
from __future__ import annotations
import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
BIB_PATH = REPO_ROOT / "docs/survey/survey.bib"
NOTES_DIR = REPO_ROOT / "docs/appendix/paper-notes"


def to_cite_key(stem: str) -> str:
    m = re.match(r"^(\d{4})-([a-z0-9-]+)$", stem)
    if not m:
        return stem.replace("-", "")
    year, name = m.groups()
    parts = name.split("-", 1)
    first = parts[0]
    rest = parts[1].replace("-", "") if len(parts) > 1 else ""
    return f"{first}{year}{rest}"


def clean_author(raw: str) -> str:
    s = re.sub(r"\*\*", "", raw)
    s = re.sub(r"¹|²|³|⁴|⁰|˒", "", s)
    s = re.sub(r"\*†|†", "", s)
    s = re.sub(r"\((?:通讯|Fellow[^)]*|IEEE|PDF[^)]*|[^()]*实测|[^()]*metadata|按[^()]*|[^()]*头部|对应[^()]*|等贡献[^()]*|共同一作[^()]*|⋆[^()]*|Corresponding[^()]*)\)", "", s)
    s = re.sub(r"（[^（）]*PDF[^）]*）", "", s)
    s = re.sub(r"（[^（）]*通讯[^）]*）", "", s)
    s = re.sub(r"（[^（）]*第一作者[^）]*）", "", s)
    s = re.sub(r"（[^（）]*双通讯[^）]*）", "", s)
    s = re.sub(r"（[^（）]*实测[^）]*）", "", s)
    s = re.sub(r"（[^（）]*⋆[^）]*）", "", s)
    s = s.replace(" and ", ", ").replace("、", ",")
    names = [n.strip() for n in s.split(",") if n.strip()]
    cleaned = []
    for n in names:
        n2 = re.sub(r"^[*†\s]+|[*†\s]+$", "", n).strip()
        if not n2 or len(n2) < 3:
            continue
        if any(skip in n2.lower() for skip in ["位", "metadata", "arxiv", "pdf", "贡献", "共同一作"]):
            continue
        cleaned.append(n2)
    return ", ".join(cleaned)


def extract_meta(text: str) -> dict:
    """抽 0.5 元数据段."""
    meta = {}
    title_m = re.search(r"^#\s+(.+?)$", text, re.M)
    if title_m:
        meta["title"] = title_m.group(1).strip()

    m_arxiv = re.search(r"^- \*\*arxiv-id\*\*:\s*(\S+)", text, re.M)
    if m_arxiv:
        meta["arxiv_id"] = m_arxiv.group(1).strip()

    m_venue = re.search(r"^- \*\*venue\*\*:\s*(.+)$", text, re.M)
    if m_venue:
        meta["venue"] = m_venue.group(1).strip()
    if "venue" not in meta:
        m_v2 = re.search(r"^\*\*会议\*\*:\s*(.+)", text, re.M)
        if m_v2:
            meta["venue"] = m_v2.group(1).strip()

    m_status = re.search(r"^- \*\*status\*\*:\s*(.+)$", text, re.M)
    if m_status:
        meta["status"] = m_status.group(1).strip()

    m_author = re.search(r"^- 作者:\s*(.+)$", text, re.M)
    if m_author:
        meta["author"] = clean_author(m_author.group(1))
    if "author" not in meta:
        m_a2 = re.search(r"^\*\*作者\*\*:\s*(.+)", text, re.M)
        if m_a2:
            meta["author"] = clean_author(m_a2.group(1))

    m_year = re.search(r"^- 年份:\s*(\d{4})", text, re.M)
    if m_year:
        meta["year"] = m_year.group(1)

    m_faction = re.search(r"^- faction:\s*([A-E])", text, re.M)
    if m_faction:
        meta["faction"] = m_faction.group(1)

    return meta


def parse_idx_faction(idx_text: str) -> dict[str, str]:
    """从 INDEX.md 表格抽 (filename -> faction)."""
    out = {}
    current = "?"
    for line in idx_text.split("\n"):
        if line.startswith("## "):
            m = re.match(r"^##\s+([A-E])\.\s", line)
            if m:
                current = m.group(1)
        elif line.startswith("| [") and current != "?":
            mm = re.match(r"^\| \[(\d{4}-[a-z0-9-]+\.md)\]", line)
            if mm:
                out[mm.group(1)] = current
    return out


def venue_to_bibtype(venue: str) -> tuple[str, str]:
    """return (bib_type, booktitle)."""
    v = venue.lower()
    if "arxiv" in v:
        return ("misc", "arXiv preprint")
    if "cvpr" in venue:
        return ("inproceedings", venue)
    if "eccv" in venue:
        return ("inproceedings", venue)
    if "iccv" in venue or "icv" in venue:
        return ("inproceedings", "ICCV 2025")
    if "siggraph" in venue or "tog" in v:
        return ("inproceedings", venue if "siggraph" in venue.lower() else "ACM SIGGRAPH / ACM TOG")
    if "iclr" in venue:
        return ("inproceedings", venue)
    if "neurips" in venue:
        return ("inproceedings", venue)
    if "icml" in venue:
        return ("inproceedings", venue)
    if "isca" in venue:
        return ("misc", venue)
    if "aaai" in venue:
        return ("inproceedings", venue)
    return ("misc", venue)


def make_entry(ck: str, meta: dict) -> str:
    title = meta.get("title", "Unknown Title")
    author = meta.get("author", "Unknown Author")
    if not author:
        author = "Unknown Author"
    year = meta.get("year", "2026")
    venue = meta.get("venue", "arXiv preprint")
    arxiv = meta.get("arxiv_id", "")

    bib_type, booktitle = venue_to_bibtype(venue)

    if arxiv and arxiv != "(待补)":
        if bib_type == "misc":
            booktitle = f"arXiv preprint arXiv:{arxiv}"

    author_field = f"  author={{{{{author}}}}},\n"
    eprint_line = ""
    if arxiv and arxiv != "(待补)":
        eprint_line = f"  eprint={{{arxiv}}},\n"

    note_field = f"  note={{paper-notes/{ck.replace('-', '_')[:60]}.md (auto-added by add_bib_entries.py v5.45)}}"

    lines = [
        f"@{bib_type}{{{ck},",
        f"  title={{{title}}}",
        author_field,
        f"  booktitle={{{booktitle}}},",
        f"  year={{{year}}},",
    ]
    if eprint_line:
        lines.append(eprint_line.rstrip())
    lines.append(note_field)
    lines.append("}")

    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true", help="actually write to bib")
    args = parser.parse_args()

    if not BIB_PATH.exists():
        print(f"ERR: bib not found at {BIB_PATH}", flush=True)
        return 1

    bib_text = BIB_PATH.read_text(encoding="utf-8")
    existing_keys = set(re.findall(r"^@\w+\{([^,]+),", bib_text, re.M))

    note_faction = parse_idx_faction((NOTES_DIR / "INDEX.md").read_text(encoding="utf-8"))

    candidates = []
    for p in sorted(NOTES_DIR.glob("*.md")):
        if p.stem == "INDEX":
            continue
        ck = to_cite_key(p.stem)
        if ck in existing_keys:
            continue
        text = p.read_text(encoding="utf-8")
        meta = extract_meta(text)
        if not meta.get("title") or meta.get("title") == "Unknown Title":
            continue
        if not meta.get("faction"):
            meta["faction"] = note_faction.get(p.name, "?")
        candidates.append((ck, p.stem, meta))

    faction_order = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4}
    candidates.sort(key=lambda x: (faction_order.get(x[2].get("faction", "Z"), 9), x[0]))

    print(f"=== add_bib_entries.py ===")
    print(f"Existing entries: {len(existing_keys)}")
    print(f"Candidates (to add): {len(candidates)}")
    print(f"Target: 100+ entries, currently would be {len(existing_keys) + len(candidates)}")
    print()
    print("=== distribution by faction ===")
    by_faction = {}
    for ck, stem, meta in candidates:
        f = meta.get("faction", "?")
        by_faction.setdefault(f, []).append((ck, meta.get("title", "")[:60]))
    for f in sorted(by_faction.keys()):
        print(f"  faction {f}: {len(by_faction[f])}")

    print()
    print("=== first 60 candidates (sorted by faction) ===")
    for ck, stem, meta in candidates[:60]:
        f = meta.get("faction", "?")
        title = meta.get("title", "")[:80]
        venue = meta.get("venue", "?")[:30]
        print(f"  [{ck:35}] [{f}] {venue:30} | {title}")

    if args.apply:
        new_entries = []
        for ck, stem, meta in candidates:
            entry = make_entry(ck, meta)
            new_entries.append(entry)

        new_bib = bib_text.rstrip() + "\n\n" + "\n\n".join(new_entries) + "\n"
        BIB_PATH.write_text(new_bib, encoding="utf-8")
        print(f"\n=== APPLIED: added {len(new_entries)} entries ===")
        print(f"new total: {len(existing_keys) + len(new_entries)} entries")
    else:
        print("\n=== DRY RUN (use --apply to write) ===")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
