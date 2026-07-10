#!/usr/bin/env python3
"""
check_drift.py — 演进图一致性检查脚本

跑在 evolution_gen.py 之后。fail = 必须修。

检查 3 处一致性：
1. 磁盘 note 文件数 vs INDEX.md 引用数
2. INDEX.md 引用数 vs evolution.json 节点数
3. evolution.json 派系分布 vs INDEX 派系分组标题数

Usage:
  python3 cron_scripts/check_drift.py
  python3 cron_scripts/check_drift.py --json  # 输出 JSON 供 cron 用

Exit code:
  0 = 全一致
  1 = 有 drift 项
"""

import argparse
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
NOTES_DIR = REPO_ROOT / "docs" / "appendix" / "paper-notes"
INDEX_FILE = NOTES_DIR / "INDEX.md"
JSON_FILE = REPO_ROOT / "docs" / "evolution" / "data" / "evolution.json"


def collect_note_ids_from_disk():
    """磁盘上的 paper note 文件名（去掉 .md 和 INDEX）"""
    return sorted([p.stem for p in NOTES_DIR.glob("*.md") if p.stem != "INDEX"])


def collect_note_ids_from_index():
    """从 INDEX.md 表格里提取的 note id（(2026-foo.md) 这种）"""
    text = INDEX_FILE.read_text() if INDEX_FILE.exists() else ""
    # 匹配 [title.md](title.md) 或 ([title.md](title.md))
    return sorted(set(re.findall(r"\((\d{4}-[a-z][a-z0-9\-]+)\.md\)", text)))


def collect_node_ids_from_json():
    """从 evolution.json 提取节点 id"""
    if not JSON_FILE.exists():
        return [], {}
    data = json.loads(JSON_FILE.read_text())
    nodes = data.get("nodes", [])
    ids = sorted([n["id"] for n in nodes])
    factions = {}
    for n in nodes:
        factions[n["faction"]] = factions.get(n["faction"], 0) + 1
    return ids, factions


def collect_factions_from_index():
    """从 INDEX.md 提取派系分组（A/B/C/D/E 的标题行）"""
    text = INDEX_FILE.read_text() if INDEX_FILE.exists() else ""
    # 匹配 ## A. xxx (N 篇) / ## A. xxx（N 篇） / ## A. xxx
    matches = re.findall(r"^## ([A-E])\.\s.*?[（(](\d+)\s*篇[)）]", text, re.MULTILINE)
    factions = {}
    for letter, count in matches:
        factions[letter] = int(count) if count else None
    return factions


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true", help="输出 JSON 格式")
    parser.add_argument("--strict", action="store_true", help="INDEX 派系计数 vs JSON 派系分布严格匹配")
    args = parser.parse_args()

    disk_ids = collect_note_ids_from_disk()
    index_ids = collect_note_ids_from_index()
    json_ids, json_factions = collect_node_ids_from_json()
    index_factions = collect_factions_from_index()

    report = {
        "disk_note_count": len(disk_ids),
        "index_ref_count": len(index_ids),
        "json_node_count": len(json_ids),
        "json_factions": json_factions,
        "index_factions": index_factions,
        "drifts": [],
    }

    # 1. 磁盘 vs INDEX
    disk_only = set(disk_ids) - set(index_ids)
    index_only_disk = set(index_ids) - set(disk_ids)
    if disk_only:
        report["drifts"].append({
            "type": "disk_only",
            "msg": f"磁盘有但 INDEX 没引用 ({len(disk_only)})",
            "ids": sorted(disk_only)[:10],
        })
    if index_only_disk:
        report["drifts"].append({
            "type": "index_only_disk",
            "msg": f"INDEX 引但磁盘没有 ({len(index_only_disk)})",
            "ids": sorted(index_only_disk)[:10],
        })

    # 2. INDEX vs JSON
    index_only_json = set(index_ids) - set(json_ids)
    json_only_index = set(json_ids) - set(index_ids)
    if index_only_json:
        report["drifts"].append({
            "type": "index_only_json",
            "msg": f"INDEX 有但 JSON 没节点 ({len(index_only_json)})",
            "ids": sorted(index_only_json)[:10],
        })
    if json_only_index:
        report["drifts"].append({
            "type": "json_only_index",
            "msg": f"JSON 有但 INDEX 没引用 ({len(json_only_index)})",
            "ids": sorted(json_only_index)[:10],
        })

    # 3. 派系计数（严格模式）
    if args.strict and index_factions:
        for letter, index_count in index_factions.items():
            json_count = json_factions.get(letter, 0)
            if json_count != index_count:
                report["drifts"].append({
                    "type": "faction_count_mismatch",
                    "msg": f"派系 {letter}: INDEX={index_count}, JSON={json_count}",
                })

    # 输出
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print("📊 演进图一致性检查")
        print(f"  磁盘 note 数:  {report['disk_note_count']}")
        print(f"  INDEX 引用数:  {report['index_ref_count']}")
        print(f"  JSON 节点数:   {report['json_node_count']}")
        print(f"  JSON 派系:     {json_factions}")
        print(f"  INDEX 派系:    {index_factions}")
        if report["drifts"]:
            print("\n❌ 不一致项:")
            for d in report["drifts"]:
                print(f"  [{d['type']}] {d['msg']}")
                if "ids" in d:
                    print(f"    ids: {d['ids']}")
            return 1
        print("\n✅ 全一致")
    return 0


if __name__ == "__main__":
    sys.exit(main())