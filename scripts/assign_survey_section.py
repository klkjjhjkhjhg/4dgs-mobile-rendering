#!/usr/bin/env python3
"""assign_survey_section.py
===========================

M2a 工具: 给 docs/appendix/paper-notes/ 下 54 篇 paper note 自动注入
`survey_section:` 字段, 注入到 0.5 元数据段末尾.

映射规则 (派系 → survey section):
  INDEX 派系 A (4DGS 表示)        → 3 (Representation)
  INDEX 派系 B (4DGS 加速)        → 4 (Training Acceleration)
  INDEX 派系 C (渲染加速)         → 5 (Rendering Acceleration)
  INDEX 派系 D (流式 + 移动端)     → 6 (Mobile Deployment)
  INDEX 派系 E (3DGS 静态加速)     → 4 或 5 (按 paper note 标题/相关性关键词判)
  INDEX 派系 F (Survey/Roadmap)   → 1 (Introduction, 引言中引用)

E 派系的细判: 含 "render/raster/Vulkan/mobile" 关键词 → 5
             含 "prune/quantiz/compress"           → 4

用法:
  python3 scripts/assign_survey_section.py            # 默认 dry-run, 输出建议
  python3 scripts/assign_survey_section.py --apply    # 实际写入
  python3 scripts/assign_survey_section.py --diff     # 只显示与已有 survey_section 不一致的
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple

REPO_ROOT = Path(__file__).resolve().parent.parent
INDEX = REPO_ROOT / "docs/appendix/paper-notes/INDEX.md"
NOTES_DIR = REPO_ROOT / "docs/appendix/paper-notes"

# 派系 → 默认 survey section (按 INDEX 大段标题)
FACTION_DEFAULT: Dict[str, int] = {
    "A": 3,  # 4DGS 表示
    "B": 4,  # 4DGS 加速
    "C": 5,  # 渲染加速
    "D": 6,  # 流式 + 移动端
    "F": 1,  # Survey / 引言
    # E 走关键词判
}

# E 派系细判关键词 (优先级: 训练 §4 强信号 > 渲染 §5 强信号)
E_TO_4 = ("prune", "quantiz", "compress", "sparsif", "compact",
          "vocab", "codebook", "tensor decompos", "coreset", "finetune")
E_TO_5 = ("vulkan", "snapdragon", "adreno", "jetson",
          "fpga", "asic", "hardware accelerator", "rasteriz", "tile-based")

# E 派系白名单 override (论文主题明确, 不走关键词)
E_OVERRIDE = {
    "2023-kerbl-3dgs": 2,  # 3DGS 原论文, §2 Background
}


def parse_index_faction() -> Dict[str, str]:
    """解析 INDEX.md, 返回 {filename_stem: 派系} 映射.

    派系识别: 行首 `## X. 标题` 算新派系, 之后 `| [YYYY-XXX.md](...)` 行收归该派系.
    """
    mapping: Dict[str, str] = {}
    current_faction = None
    for line in INDEX.read_text(encoding="utf-8").splitlines():
        m_faction = re.match(r"^## ([A-F])\. ", line)
        if m_faction:
            current_faction = m_faction.group(1)
            continue
        m_paper = re.search(r"\[(\d{4}-[a-z0-9-]+)\.md\]", line)
        if m_paper and current_faction:
            mapping[m_paper.group(1)] = current_faction
    return mapping


def classify_e_faction(stem: str) -> int:
    """E 派系按 paper note 标题/相关性关键词判 §4 vs §5."""
    # 白名单优先
    if stem in E_OVERRIDE:
        return E_OVERRIDE[stem]
    note_path = NOTES_DIR / f"{stem}.md"
    if not note_path.exists():
        return 4  # fallback
    text = note_path.read_text(encoding="utf-8")
    # 优先看相关性 blockquote (粗判用, 避免每次扫全文)
    head = "\n".join(text.splitlines()[:25]).lower()
    # §4 训练加速关键词优先 (prune/coreset 是训练阶段的强信号)
    if any(kw in head for kw in E_TO_4):
        return 4
    if any(kw in head for kw in E_TO_5):
        return 5
    return 4  # 兜底


def assign(faction_map: Dict[str, str]) -> List[Tuple[str, str, int]]:
    """返回 [(stem, faction, survey_section), ...] 全 54 篇."""
    out = []
    for stem, faction in sorted(faction_map.items()):
        if faction == "E":
            section = classify_e_faction(stem)
        else:
            section = FACTION_DEFAULT.get(faction, 4)
        out.append((stem, faction, section))
    return out


def inject_note(stem: str, section: int, *, apply: bool) -> bool:
    """在 paper note 的 0.5 元数据段末尾注入 `survey_section:` 字段.

    定位: 找包含 `## 0.5 元数据` 的行, 找到该段结束 (`##` 下一节) 之前插入.
    """
    path = NOTES_DIR / f"{stem}.md"
    text = path.read_text(encoding="utf-8")
    new_line = f"- **survey_section**: {section}"

    # 已有该字段 → 替换
    m_existing = re.search(r"^- \*\*survey_section\*\*:.*$", text, re.M)
    if m_existing:
        if apply:
            new_text = re.sub(
                r"^- \*\*survey_section\*\*:.*$", new_line, text, count=1, flags=re.M)
            path.write_text(new_text, encoding="utf-8")
        return True

    # 找 0.5 元数据段, 在该段第一个非 - 开头的行之前插入
    lines = text.splitlines()
    in_meta = False
    insert_at = None
    for i, line in enumerate(lines):
        if re.match(r"^## 0\.5 元数据", line):
            in_meta = True
            continue
        if in_meta and re.match(r"^## ", line):
            insert_at = i
            break
        if in_meta and line.strip() and not line.startswith("-") and insert_at is None:
            insert_at = i
            break
    if insert_at is None:
        print(f"WARN: {stem} 找不到 0.5 元数据段, 跳过", file=sys.stderr)
        return False
    lines.insert(insert_at, new_line)
    if apply:
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return True


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--apply", action="store_true", help="实际写入 (默认 dry-run)")
    p.add_argument("--diff", action="store_true", help="只显示与已有 survey_section 不一致的")
    args = p.parse_args()

    faction_map = parse_index_faction()
    if not faction_map:
        print("ERROR: INDEX 解析失败, 0 篇", file=sys.stderr)
        return 1

    rows = assign(faction_map)

    # 用文件系统实际存在的 note 文件名 anchor (避免 INDEX 拼写差异导致 FileNotFoundError)
    actual_stems = {
        p.stem: p
        for p in NOTES_DIR.glob("*.md")
        if p.stem != "INDEX"
    }
    # 配对: 用 stem 关键词模糊匹配 (year + first 3 chars of name)
    def find_actual(stem: str) -> Path | None:
        if stem in actual_stems:
            return actual_stems[stem]
        # INDEX 里的拼写错, 找相同年份 + 前缀的
        year_prefix = stem[:7]  # "2026-xy"
        for s, p in actual_stems.items():
            if s.startswith(year_prefix):
                # 进一步匹配: 名字前 3 字符相同
                if s[8:11] == stem[8:11]:
                    return p
        return None

    # 统计
    from collections import Counter
    by_section = Counter(s for _, _, s in rows)
    by_faction = Counter(f for _, f, _ in rows)
    print(f"=== 派系 → survey_section 分布 ===")
    for f in sorted(by_faction):
        cnt = by_faction[f]
        sect = ", ".join(f"§{s}" for _, ff, s in rows if ff == f)
        print(f"  派系 {f}: {cnt} 篇 → {sect}")
    print(f"\n=== survey_section 分布 ===")
    for s in sorted(by_section):
        print(f"  §{s}: {by_section[s]} 篇")

    # 按派系 + section 输出
    print(f"\n=== 全 {len(rows)} 篇明细 ===")
    miss = []
    for stem, f, s in rows:
        actual = find_actual(stem)
        if not actual:
            miss.append(stem)
            print(f"  ! [MISS] {stem}  → §{s} (paper note 文件不存在)")
            continue
        actual_stem = actual.stem
        flag = " " if inject_note(actual_stem, s, apply=False) else "!"
        if args.diff:
            # 检查是否已有一致
            note = actual.read_text(encoding="utf-8")
            m = re.search(r"^- \*\*survey_section\*\*: (\d+)$", note, re.M)
            if m and int(m.group(1)) == s:
                continue
        diff_mark = " (≠ INDEX)" if actual_stem != stem else ""
        print(f"  {flag} [{f}] {actual_stem}{diff_mark}  → §{s}")

    if miss:
        print(f"\nWARNING: {len(miss)} 篇 INDEX 提到但 paper note 缺失: {miss}")
        rows = [(s, f, sec) for s, f, sec in rows if find_actual(s)]

    if args.apply:
        applied = 0
        for stem, _, s in rows:
            actual = find_actual(stem)
            if actual and inject_note(actual.stem, s, apply=True):
                applied += 1
        print(f"\n=== 已注入 {applied} / {len(rows)} 篇 ===")
    else:
        print(f"\n(dry-run, 用 --apply 实际写入)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
