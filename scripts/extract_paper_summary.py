#!/usr/bin/env python3
"""extract_paper_summary.py
============================

M2b 工具: 从 54 篇 paper notes 抽取 1 句话问题 / 方法核心 / 关键数字,
生成可粘到 survey section 的 LaTeX \\item 段落.

输出格式 (每个 paper 一段):
  \\item \\textbf{2023-kerbl-3dgs}~\\cite{kerbl20233dgs}: 3D Gaussian Splatting
        原论文, 显式点云 + 可微分光栅化. 方法核心: 各向异性 3D 高斯椭球表示 +
        alpha-blending 光栅化. 关键数字: 1080p @ 30 FPS desktop.

用法:
  python3 scripts/extract_paper_summary.py              # 全 54 篇输出到 stdout
  python3 scripts/extract_paper_summary.py --section 3  # 只看 §3 的 paper
  python3 scripts/extract_paper_summary.py --top 5 3    # §3 前 5 篇
  python3 scripts/extract_paper_summary.py --stem 2023-kerbl-3dgs  # 指定单篇
  python3 scripts/extract_paper_summary.py --section 3 --apply sections/sec-3-representation.tex
                                                     # 直接 inject 到 section 文件
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
NOTES_DIR = REPO_ROOT / "docs/appendix/paper-notes"
SECTIONS_DIR = REPO_ROOT / "docs/survey/sections"


def parse_meta(text: str) -> dict:
    """抽 0.5 元数据段."""
    meta = {}
    m_section = re.search(r"^- \*\*survey_section\*\*: (\d+)$", text, re.M)
    if m_section:
        meta["survey_section"] = int(m_section.group(1))
    m_venue = re.search(r"^- \*\*venue\*\*:\s*(.+)$", text, re.M)
    if m_venue:
        meta["venue"] = m_venue.group(1).strip()
    m_year_arxiv = re.search(r"^- \*\*arxiv-id\*\*:\s*(\d{2})(\d{2})\.", text, re.M)
    if m_year_arxiv:
        meta["year"] = f"20{m_year_arxiv.group(1)}"
    else:
        m_year = re.search(r"^- \*\*年份\*\*:\s*(20\d{2})", text, re.M)
        if m_year:
            meta["year"] = m_year.group(1)
    return meta


def extract_section(text: str, prefix: str) -> str:
    """抽 ## <prefix>(...) 之后到下一个 ## 之前的内容, 拼成 1-2 句短文."""
    m = re.search(rf"^##\s*{re.escape(prefix)}[^\n]*$", text, re.M)
    if not m:
        return ""
    after = text[m.end():]
    # 找到下一个 ## 开头
    nxt = re.search(r"^##\s+", after, re.M)
    body = after[: nxt.start()].strip() if nxt else after.strip()
    # 去掉 bullet (- / *) 标记, 拼成 1 段
    lines = []
    for line in body.splitlines():
        line = re.sub(r"^[-*]\s+", "", line.strip())
        if line and not line.startswith("#"):
            lines.append(line)
    return " ".join(lines).strip()


def shorten(text: str, max_chars: int = 200) -> str:
    """压成 1 句短文 (去掉粗体/超链等 markdown 标记)."""
    text = re.sub(r"\*\*([^*]+)\*\*", r"\1", text)
    text = re.sub(r"`([^`]+)`", r"\1", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"\\cite\{[^}]+\}", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    # 截到 max_chars 内的第一个句号
    if len(text) > max_chars:
        cut = text[:max_chars]
        # 找最近的句号 / 逗号
        for sep in [",", ";", "。", "，", "；", "，"]:
            idx = cut.rfind(sep)
            if idx > max_chars * 0.5:
                cut = cut[:idx]
                break
        text = cut.rstrip() + "..."
    return text


def to_cite_key(stem: str) -> str:
    """2023-kerbl-3dgs -> kerbl20233dgs (survey.bib 命名规范).

    规则: name 拆 first-word + rest, bib_key = first + year + rest (去 dash).
    例子:
      2023-kerbl-3dgs        -> kerbl + 2023 + 3dgs = kerbl20233dgs
      2024-wu-4dgs           -> wu + 2024 + 4dgs = wu20244dgs
      2026-du-mobile-gs      -> du + 2026 + mobilegs = du2026mobilegs
      2025-feng-lumina       -> feng + 2025 + lumina = feng2025lumina
    """
    m = re.match(r"^(\d{4})-([a-z0-9-]+)$", stem)
    if not m:
        return stem.replace("-", "")
    year, name = m.groups()
    parts = name.split("-", 1)
    first = parts[0]
    rest = parts[1].replace("-", "") if len(parts) > 1 else ""
    return f"{first}{year}{rest}"


def format_item(stem: str, text: str) -> str:
    """生成 \\item 段落."""
    cite = to_cite_key(stem)
    # 截到 2 个句号内 (避免太长)
    parts = re.split(r"([。.!?])", text)
    # parts 是 [text, punct, text, punct, ...]
    short = ""
    for i in range(0, len(parts) - 1, 2):
        short += parts[i] + parts[i + 1]
        if short.count("。") + short.count(".") >= 2:
            break
    if not short:
        short = text[:150]
    short = re.sub(r"\s+", " ", short).strip().rstrip(",;，；") + "."
    return f"\\item \\textbf{{{stem}}}~\\cite{{{cite}}}: {short}"


def extract_authors(text: str) -> str:
    """从 '## 年份 / 作者' 段抽作者列表.

    兼容两种格式:
      - **作者**(4 位,按 arxiv metadata): Yuheng Yuan, ...   (行内, 一行)
      - **作者**: Yuheng Yuan, ...                          (行内, 简单)
    """
    # 找 **作者** 字段所在行, 抓冒号后的内容
    m = re.search(r"^\- \*\*作者\*\*[^*]*:\s*(.+)$", text, re.M)
    if not m:
        return ""
    raw = m.group(1).strip()
    # 去掉可能的星号和括号注释
    raw = re.sub(r"\*\*", "", raw)
    raw = re.sub(r"\([^)]*\)", "", raw)
    # 提取 "X 位,按 arxiv metadata" 之类注释
    m_note = re.match(r"^([^,]+(?:,\s*[^,]+){0,15})", raw)
    if m_note:
        return m_note.group(1).strip()
    return raw[:200]


def extract_title(text: str) -> str:
    """从第一行 H1 抽 title (去掉 'YYYY-XXX · ' 前缀)."""
    m = re.search(r"^# \d{4}-[a-z0-9-]+\s*[·:]\s*(.+)$", text, re.M)
    if m:
        return m.group(1).strip()
    return ""


def make_bib_entry(stem: str) -> str:
    path = NOTES_DIR / f"{stem}.md"
    if not path.exists():
        return ""
    text = path.read_text(encoding="utf-8")
    meta = parse_meta(text)
    title = extract_title(text)
    authors = extract_authors(text)
    year = meta.get("year", "20XX")
    venue = meta.get("venue", "preprint")
    cite = to_cite_key(stem)

    # venue 决定 entry type
    venue_l = venue.lower()
    if any(k in venue_l for k in ["arxiv", "preprint"]):
        entry_type = "misc"
        bib_venue = "arXiv preprint"
    elif any(k in venue_l for k in ["siggraph", "siggraph asia"]):
        entry_type = "inproceedings"
        bib_venue = "ACM SIGGRAPH"
    elif any(k in venue_l for k in ["cvpr", "iccv", "eccv", "iclr", "icml"]):
        entry_type = "inproceedings"
        bib_venue = venue
    elif "tog" in venue_l or "transactions" in venue_l:
        entry_type = "article"
        bib_venue = "ACM Transactions on Graphics"
    else:
        entry_type = "misc"
        bib_venue = venue

    author_short = authors if len(authors) < 80 else authors.split(",")[0] + ", et al."
    # 用 {} 包住 author 字段, 避免 BibTeX 误解析
    return (
        f"@{entry_type}{{{cite},\n"
        f"  title={{{title}}},\n"
        f"  author={{{{{author_short}}}}},\n"
        f"  booktitle={{{bib_venue}}},\n"
        f"  year={{{year}}},\n"
        f"  note={{paper-notes/{stem}.md}}\n"
        f"}}"
    )


def extract_one(stem: str) -> dict | None:
    path = NOTES_DIR / f"{stem}.md"
    if not path.exists():
        return None
    text = path.read_text(encoding="utf-8")
    meta = parse_meta(text)
    q = extract_section(text, "一句话问题")
    m = extract_section(text, "方法核心")
    n = extract_section(text, "关键数字")
    return {
        "stem": stem,
        "meta": meta,
        "question": shorten(q, 120),
        "method": shorten(m, 180),
        "numbers": shorten(n, 120),
        "combined": f"{shorten(q, 80)} 方法: {shorten(m, 100)} 数字: {shorten(n, 80)}",
    }


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--section", type=int, help="只看指定 survey_section")
    p.add_argument("--top", type=int, default=0, help="只输出前 N 篇 (按 stem 排序)")
    p.add_argument("--stem", help="只输出指定 paper")
    p.add_argument("--apply", type=int, help="inject 到对应 sec-N 文件 (N = 这个值)")
    p.add_argument("--bib", action="store_true", help="同时生成 bib 条目 (stdout)")
    args = p.parse_args()

    stems = sorted(
        p.stem
        for p in NOTES_DIR.glob("*.md")
        if p.stem != "INDEX"
    )
    if args.stem:
        stems = [args.stem]

    out = []
    for stem in stems:
        info = extract_one(stem)
        if not info:
            continue
        if args.section is not None and info["meta"].get("survey_section") != args.section:
            continue
        out.append(info)

    # 先按 --section 过滤 (--apply 时忽略, apply 自己用 sec 参数)
    if args.section is not None and args.apply is None:
        out = [info for info in out
               if info["meta"].get("survey_section") == args.section]
    if args.top:
        out = out[: args.top]

    if args.apply is not None:
        # apply 模式: 跑全 54 篇, 选 survey_section = apply 的 paper
        sec = args.apply
        items = []
        for info in out:
            if info["meta"].get("survey_section") == sec:
                items.append(format_item(info["stem"], info["combined"]))
        if items:
            inject_to_section(sec, items)
        print(f"=== 已 inject {len(items)} \\item 到 sec-{sec} ===")
        return 0

    if args.bib:
        # 输出所有 paper 的 bib 条目 (用于扩 survey.bib)
        seen = set()
        for info in out:
            cite = to_cite_key(info["stem"])
            if cite in seen:
                continue
            seen.add(cite)
            print(make_bib_entry(info["stem"]))
            print()
        return 0

    # 默认 stdout 输出
    for info in out:
        print(f"\n--- {info['stem']} (sec={info['meta'].get('survey_section')}, "
              f"venue={info['meta'].get('venue', '?')}) ---")
        print(f"Q: {info['question']}")
        print(f"M: {info['method']}")
        print(f"N: {info['numbers']}")
        print(f"\n>>> {format_item(info['stem'], info['combined'])}")
    print(f"\n=== 共 {len(out)} 篇 ===")
    return 0


def inject_to_section(sec: int, items: list[str]) -> None:
    """把 \\item 段 inject 到 sec-N-xxx.tex 的适当位置.

    策略: 在最后一个 \\subsection 末尾 + \\bigskip 之前, 替换占位段.
    """
    name_map = {
        1: "intro", 2: "background", 3: "representation",
        4: "training-acceleration", 5: "rendering-acceleration",
        6: "mobile-deployment", 7: "datasets-metrics",
        8: "discussion", 9: "conclusion",
    }
    sec_file = SECTIONS_DIR / f"sec-{sec}-{name_map[sec]}.tex"
    text = sec_file.read_text(encoding="utf-8")

    itemize = "\\begin{itemize}\n" + "\n".join(items) + "\n\\end{itemize}\n"

    # 找 paper notes 索引那行, 在它前面插入
    marker = "\\noindent\\textbf{本节对应 paper notes 索引}"
    if marker in text:
        # 替换 marker 前的"空 / 占位"位置
        new_text = text.replace(marker, itemize + marker, 1)
    else:
        # 末尾追加
        new_text = text.rstrip() + "\n\n" + itemize

    sec_file.write_text(new_text, encoding="utf-8")


if __name__ == "__main__":
    sys.exit(main())
