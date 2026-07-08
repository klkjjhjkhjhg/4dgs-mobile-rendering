#!/usr/bin/env python3
"""
evolution_gen.py — 演进图数据生成器

读 49 篇 paper notes，生成 docs/evolution/data/evolution.json

v1: 只生成节点列表（id/label/year/faction/arxiv/rating）
v2: 补全边（用 S2 API 拉 references）
"""

import os
import re
import json
import sys
from pathlib import Path

# 路径: cron_scripts/evolution_gen.py
# 仓库根: ../../  (从 cron_scripts/ 回到仓库根)
REPO_ROOT = Path(__file__).resolve().parent.parent
NOTES_DIR = REPO_ROOT / "docs" / "appendix" / "paper-notes"
INDEX_FILE = NOTES_DIR / "INDEX.md"
OUTPUT_FILE = REPO_ROOT / "docs" / "evolution" / "data" / "evolution.json"

# 派系关键词 → faction 映射
FACTION_KEYWORDS = {
    "A": ["4dgs", "4d gaussian", "4dgs-1k", "spacetime", "deformable", "4dgrt", "rotorgs", "retimegs", "gaussianfluent"],
    "B": ["4dgscc", "4dgcpro", "mega", "flashgs", "hacpp", "seele", "omg4", "speede3dgs", "sharptimegs", "pd4dgs", "cags", "success-gs", "p4dgs", "airgs", "vedal"],
    "C": ["mip-splatting", "lightgaussian", "compact3d", "efficientgs", "fcgs", "scaffold", "ace-gs", "evogs", "dict-3dgs", "geta3dgs", "polymerge", "zipsplat", "cubifygs", "refine"],
    "D": ["mobile-gs", "gs-nfs", "streamstgs", "gifstream", "gausslite", "mmgs", "codecsplat", "pocket-slam", "flux-gs"],
    "E": ["lumina"],
}

RATING_KEYWORDS = {
    "⭐⭐⭐": ["本项目直接对标", "直接对标", "原论文"],
    "⭐⭐": ["高相关", "对标", "重点"],
    "⭐": [],
}


def parse_index_faction(index_path: Path) -> dict:
    """从 INDEX.md 解析每篇 note 的派系。返回 {note_id: faction}"""
    faction_map = {}
    current_faction = None
    with open(index_path) as f:
        for line in f:
            # 派系标题: "## A. 4DGS 表示"
            m = re.match(r"## ([A-E])\.\s", line)
            if m:
                current_faction = m.group(1)
                continue
            # note 链接: [2024-wu-4dgs.md](2024-wu-4dgs.md) | arxiv | year | 一句话 | 评级
            m = re.search(r"\[(\d{4}-[a-z\-]+)\.md\]", line)
            if m and current_faction:
                note_id = m.group(1)
                faction_map[note_id] = current_faction
    return faction_map


def parse_note_meta(note_path: Path) -> dict:
    """从单篇 note 解析元数据（label / arxiv / year）"""
    meta = {"id": note_path.stem, "label": note_path.stem, "arxiv": None, "year": None}

    # arxiv 链接
    with open(note_path) as f:
        content = f.read(2000)  # 只读前 2KB
    m = re.search(r"arxiv[:\s]+(\d{4}\.\d{4,5})", content)
    if m:
        meta["arxiv"] = m.group(1)
    m = re.search(r"abs/(\d{4}\.\d{4,5})", content)
    if m:
        meta["arxiv"] = m.group(1)

    # title (# 标题行)
    with open(note_path) as f:
        first_line = f.readline().strip()
    m = re.match(r"# \d{4}-[a-z\-]+ · (.+)", first_line)
    if m:
        meta["label"] = m.group(1).strip()
    else:
        meta["label"] = note_path.stem.split("-", 2)[-1].upper() if "-" in note_path.stem else note_path.stem

    return meta


def derive_year_from_filename(note_id: str) -> float:
    """从文件名解析年份，精确到月（如果月份有）"""
    m = re.match(r"(\d{4})-([a-z\-]+)", note_id)
    if not m:
        return 2025.0
    year = int(m.group(1))
    author = m.group(2)
    # 简单启发式：作者首字母索引到月份（不严谨，但 v1 够用）
    # 真实情况用 INDEX.md 的 year 列
    return float(year)  # v1 只给整数年，月份后续从 INDEX.md 补


def derive_year_from_index(index_path: Path) -> dict:
    """从 INDEX.md 解析 {note_id: year_float}"""
    year_map = {}
    with open(index_path) as f:
        for line in f:
            m = re.search(r"\[(\d{4}-[a-z\-]+)\.md\]\(.*?\)\s*\|\s*(\d{4}\.\d{1,2})", line)
            if m:
                note_id = m.group(1)
                year = float(m.group(2))
                year_map[note_id] = year
    return year_map


def derive_rating(note_id: str, index_path: Path) -> str:
    """从 INDEX.md 解析评级"""
    with open(index_path) as f:
        for line in f:
            m = re.search(rf"\[{re.escape(note_id)}\.md\].*?\|\s*([⭐]+)", line)
            if m:
                return m.group(1)
    return "⭐"


def classify_faction(note_id: str, label: str, index_faction: dict) -> str:
    """优先用 INDEX.md 派系，否则用关键词分类"""
    if note_id in index_faction:
        return index_faction[note_id]
    text = (note_id + " " + label).lower()
    for faction, keywords in FACTION_KEYWORDS.items():
        for kw in keywords:
            if kw in text:
                return faction
    return "C"  # 默认派系 C（3DGS 加速）


def build_node(note_id: str, label: str, year: float, faction: str, arxiv: str, rating: str) -> dict:
    return {
        "id": note_id,
        "label": label,
        "year": year,
        "faction": faction,
        "arxiv": arxiv,
        "refs": 0,  # v2 用 S2 API 计算
        "rating": rating
    }


def main():
    if not NOTES_DIR.exists():
        print(f"ERROR: {NOTES_DIR} 不存在", file=sys.stderr)
        sys.exit(1)

    print(f"扫描 {NOTES_DIR} ...")
    note_files = sorted([f for f in NOTES_DIR.glob("*.md") if f.name != "INDEX.md"])
    print(f"  找到 {len(note_files)} 个 note")

    # 解析 INDEX.md
    print(f"解析 {INDEX_FILE} ...")
    index_faction = parse_index_faction(INDEX_FILE)
    index_year = derive_year_from_index(INDEX_FILE)
    print(f"  派系覆盖: {len(index_faction)} 篇")
    print(f"  年份覆盖: {len(index_year)} 篇")

    # 生成节点
    nodes = []
    for note_path in note_files:
        note_id = note_path.stem
        meta = parse_note_meta(note_path)
        year = index_year.get(note_id, derive_year_from_filename(note_id))
        rating = derive_rating(note_id, INDEX_FILE)
        faction = classify_faction(note_id, meta["label"], index_faction)
        nodes.append(build_node(note_id, meta["label"], year, faction, meta["arxiv"], rating))

    # 生成基础 evolution.json（v1：只含节点，边为空）
    output = {
        "meta": {
            "title": "4DGS / 3DGS Mobile Rendering 演进图",
            "total_nodes": len(nodes),
            "factions": {
                "A": {"name": "4DGS 表示", "color": "#e74c3c", "y": 0},
                "B": {"name": "4DGS 加速 / 动静态分离", "color": "#3498db", "y": 1},
                "C": {"name": "3DGS 加速", "color": "#2ecc71", "y": 2},
                "D": {"name": "移动端 / 流式落地", "color": "#f1c40f", "y": 3},
                "E": {"name": "Cross-disciplinary", "color": "#9b59b6", "y": 4}
            },
            "turning_points": [
                {"id": "T1", "label": "3DGS 起点", "year": 2023.7, "x": 2023.7},
                {"id": "T2", "label": "4DGS 起点", "year": 2024.1, "x": 2024.1},
                {"id": "T3", "label": "4DGS-1K 动静态分离", "year": 2025.3, "x": 2025.3},
                {"id": "T4", "label": "Lumina 移动端 + 体系结构", "year": 2025.4, "x": 2025.4}
            ],
            "year_range": [2023.0, 2026.7]
        },
        "nodes": nodes,
        "edges": []  # v1 留空，v2 用 S2 API 补全
    }

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    # v1.1: 保留已有 evolution.json 的手写边（如果存在）
    # 这样 cron 重新跑时只更新节点，不会丢手写的引用关系
    if OUTPUT_FILE.exists():
        with open(OUTPUT_FILE) as f:
            old = json.load(f)
            existing_edges = old.get("edges", [])
        output["edges"] = existing_edges
        print(f"  保留 {len(existing_edges)} 条手写边")

    with open(OUTPUT_FILE, "w") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"\n✅ 生成 {len(nodes)} 节点 → {OUTPUT_FILE}")
    print(f"   派系分布: A={sum(1 for n in nodes if n['faction']=='A')} "
          f"B={sum(1 for n in nodes if n['faction']=='B')} "
          f"C={sum(1 for n in nodes if n['faction']=='C')} "
          f"D={sum(1 for n in nodes if n['faction']=='D')} "
          f"E={sum(1 for n in nodes if n['faction']=='E')}")


if __name__ == "__main__":
    main()
