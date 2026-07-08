#!/usr/bin/env python3
"""
add_metadata.py — 给 49 篇 paper notes 批量加 §0.5 元数据块

策略：
- 解析每篇 note 的 arxiv-id (从链接)
- 解析 status (有 CVPR/SIGGRAPH 等关键词 → received，否则 arxiv-only)
- 解析 homepage (从链接)
- 收录日期默认 = 2026-07-08（本批扩展日期）
- 收录来源 = "arxiv scan" (v1 统一)
- 1-hop 引用 = "（v2 补全）"  占位
"""

import re
import os
from pathlib import Path
from datetime import datetime

REPO_ROOT = Path(__file__).resolve().parent.parent
NOTES_DIR = REPO_ROOT / "docs" / "appendix" / "paper-notes"

# 已知会议 venue 映射（从 INDEX.md + README.md 论据表反推）
KNOWN_VENUES = {
    "2023-attal-hyperreel": ("CVPR 2023", "⭐⭐"),
    "2023-fan-lightgaussian": ("CVPR 2024", "⭐⭐"),
    "2023-navaneet-compact3d": ("ECCV 2024", "⭐⭐"),
    "2023-yang-deformable-3dgs": ("CVPR 2024", "⭐⭐⭐"),
    "2024-chen-fcgs": ("CVPR 2024", "⭐"),
    "2024-chen-hacpp": ("ECCV 2024", "⭐"),
    "2024-duan-4drotorgs": ("CVPR 2024", "⭐"),
    "2024-feng-flashgs": ("CVPR 2024", "⭐⭐"),
    "2024-li-spacetime-gaussians": ("CVPR 2024", "⭐"),
    "2024-liu-efficientgs": ("CVPR 2024", "⭐"),
    "2024-wu-4dgs": ("CVPR 2024", "⭐⭐⭐"),
    "2024-yu-mip-splatting": ("CVPR 2024", "⭐⭐"),
    "2024-zhang-mega-4dgs-acceleration": ("CVPR 2024", "⭐⭐"),
    "2025-chen-4dgscc": ("CVPR 2025", "⭐⭐"),
    "2025-feng-lumina": ("arxiv pre-print (2025-06)", "⭐⭐"),
    "2025-huang-seele": ("ICLR 2025", "⭐⭐"),
    "2025-ke-streamstgs": ("CVPR 2025", "⭐"),
    "2025-lee-omg4": ("arxiv pre-print (2025-10)", "⭐⭐"),
    "2025-li-gifstream": ("CVPR 2025", "⭐"),
    "2025-liu-4dgrt": ("SIGGRAPH Asia 2025", "⭐"),
    "2025-oh-neo": ("CVPR 2025", "⭐"),
    "2025-shi-sparse4dgs": ("arxiv pre-print (2025-11)", "⭐"),
    "2025-tu-speede3dgs": ("CVPR 2025", "⭐⭐"),
    "2025-wang-airgs": ("SIGGRAPH 2025", "⭐"),
    "2025-wang-p4dgs": ("CVPR 2025", "⭐"),
    "2025-youn-success-gs": ("arxiv pre-print (2025-07)", "⭐"),
    "2025-yuan-4dgs-1k": ("CVPR 2025", "⭐⭐⭐"),
    "2025-zheng-4dgcpro": ("arxiv pre-print (2025-01)", "⭐"),
    "2026-chen-refine": ("arxiv pre-print (2026-04)", "⭐"),
    "2026-du-flux-gs": ("ECCV 2026 (under review)", "⭐⭐⭐"),
    "2026-du-mobile-gs": ("ICLR 2026", "⭐⭐"),
    "2026-ghosh-gs-nfs": ("arxiv pre-print (2026-06)", "⭐⭐"),
    "2026-gong-dict-3dgs": ("arxiv pre-print (2026-03)", "⭐"),
    "2026-hong-polymerge": ("arxiv pre-print (2026-05)", "⭐"),
    "2026-huang-gaussianfluent": ("CVPR 2026 Oral", "⭐⭐"),
    "2026-li-pd4dgs": ("arxiv pre-print (2026-05)", "⭐⭐"),
    "2026-li-pocket-slam": ("arxiv pre-print (2026-06)", "⭐"),
    "2026-li-vedal": ("arxiv pre-print (2026-04)", "⭐"),
    "2026-liao-sharptimegs": ("arxiv pre-print (2026-02)", "⭐⭐"),
    "2026-ren-cubifygs": ("arxiv pre-print (2026-06)", "⭐"),
    "2026-shi-evogs": ("arxiv pre-print (2026-05)", "⭐"),
    "2026-thomas-gausslite": ("arxiv pre-print (2026-04)", "⭐"),
    "2026-veicht-zipsplat": ("arxiv pre-print (2026-06)", "⭐"),
    "2026-wang-retimegs": ("CVPR 2026 Oral", "⭐⭐"),
    "2026-yin-cags": ("arxiv pre-print (2026-05)", "⭐"),
    "2026-yu-codecsplat": ("arxiv pre-print (2026-06)", "⭐"),
    "2026-zhang-geta3dgs": ("arxiv pre-print (2026-05)", "⭐"),
    "2026-zhao-ace-gs": ("arxiv pre-print (2026-03)", "⭐"),
    "2026-zhao-mmgs": ("arxiv pre-print (2026-05)", "⭐"),
}

# 收录日期（分批）
INTAKE_DATES = {
    # 14 篇 2026 H1 批
    "2026-du-flux-gs": "2026-07-08", "2026-du-mobile-gs": "2026-07-08",
    "2026-ghosh-gs-nfs": "2026-07-08", "2026-gong-dict-3dgs": "2026-07-08",
    "2026-hong-polymerge": "2026-07-08", "2026-huang-gaussianfluent": "2026-07-08",
    "2026-li-pd4dgs": "2026-07-08", "2026-li-pocket-slam": "2026-07-08",
    "2026-li-vedal": "2026-07-08", "2026-liao-sharptimegs": "2026-07-08",
    "2026-ren-cubifygs": "2026-07-08", "2026-shi-evogs": "2026-07-08",
    "2026-thomas-gausslite": "2026-07-08", "2026-veicht-zipsplat": "2026-07-08",
    "2026-wang-retimegs": "2026-07-08", "2026-yin-cags": "2026-07-08",
    "2026-yu-codecsplat": "2026-07-08", "2026-zhang-geta3dgs": "2026-07-08",
    "2026-zhao-ace-gs": "2026-07-08", "2026-zhao-mmgs": "2026-07-08",
    "2026-chen-refine": "2026-07-08",
}


def parse_arxiv_id(content: str) -> str:
    """从 note 内容提取 arxiv-id"""
    m = re.search(r"arxiv[:\s]+(\d{4}\.\d{4,5})", content[:2000])
    if m:
        return m.group(1)
    m = re.search(r"abs/(\d{4}\.\d{4,5})", content[:2000])
    if m:
        return m.group(1)
    return "（未找到）"


def parse_homepage(content: str) -> str:
    """从 note 内容提取 project homepage"""
    m = re.search(r"项目[页址][：:]\s*<?(https?://[^>\s\n]+)>?", content[:2000])
    if m:
        return m.group(1)
    m = re.search(r"Project[:\s]+<?(https?://[^>\s\n]+)>?", content[:2000])
    if m:
        return m.group(1)
    m = re.search(r"主页[：:]\s*<?(https?://[^>\s\n]+)>?", content[:2000])
    if m:
        return m.group(1)
    return "（无）"


def parse_github(content: str) -> str:
    """从 note 内容提取 GitHub 链接"""
    m = re.search(r"GitHub[:\s]+<?(https?://github\.com/[^>\s\n]+)>?", content[:2000])
    if m:
        return m.group(1)
    return "（无）"


def has_metadata_block(content: str) -> bool:
    """检查是否已经有 §0.5 元数据块"""
    return "## 0.5 元数据" in content or "## 0.5 元信息" in content


def build_metadata_block(note_id: str, content: str) -> str:
    """构建 §0.5 元数据块"""
    arxiv_id = parse_arxiv_id(content)
    homepage = parse_homepage(content)
    github = parse_github(content)
    venue, rating = KNOWN_VENUES.get(note_id, ("（待定）", "⭐"))
    intake_date = INTAKE_DATES.get(note_id, "2026-07-08（首次）")

    # status 推断
    if "Oral" in venue:
        status = "received (Oral)"
    elif "pre-print" in venue or "under review" in venue:
        status = "under review"
    elif "arxiv" in venue.lower():
        status = "arxiv-only"
    else:
        status = "received"

    # venue 字段标准化
    venue_field = venue

    block = f"""## 0.5 元数据

- **venue**: {venue_field}
- **arxiv-id**: {arxiv_id}
- **s2-id**: （v2 用 Semantic Scholar API 补全）
- **homepage**: {homepage}
- **github**: {github}
- **status**: {status}
- **收录日期**: {intake_date}
- **收录来源**: arxiv scan + 1-hop 引用规则
- **1-hop 引用**: （v2 补全，见 §11 1-hop 关系图）
- **评级**: {rating}

"""
    return block


def add_metadata_to_note(note_path: Path) -> bool:
    """给单篇 note 加 §0.5 元数据块（如果还没有）"""
    with open(note_path) as f:
        content = f.read()

    if has_metadata_block(content):
        return False  # 已经有，跳过

    note_id = note_path.stem
    block = build_metadata_block(note_id, content)

    # 找到第一个 ## 标题行（"## 一句话问题" 或 "## 链接" 或 "## 摘要"）
    # 在它之前插入 §0.5
    match = re.search(r"^## [^\n]+\n", content, re.MULTILINE)
    if not match:
        print(f"  ⚠ {note_id}: 找不到 ## 标题行，跳过")
        return False

    insert_pos = match.start()
    new_content = content[:insert_pos] + block + content[insert_pos:]

    with open(note_path, "w") as f:
        f.write(new_content)
    return True


def main():
    if not NOTES_DIR.exists():
        print(f"ERROR: {NOTES_DIR} 不存在")
        return 1

    print(f"扫描 {NOTES_DIR} ...")
    note_files = sorted([f for f in NOTES_DIR.glob("*.md") if f.name != "INDEX.md"])
    print(f"  找到 {len(note_files)} 个 note")

    added = 0
    skipped = 0
    for note_path in note_files:
        if add_metadata_to_note(note_path):
            added += 1
        else:
            skipped += 1

    print(f"\n✅ 处理完成: 新增 {added} 篇, 跳过 {skipped} 篇（已有）")
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
