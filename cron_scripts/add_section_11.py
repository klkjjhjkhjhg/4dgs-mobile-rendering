#!/usr/bin/env python3
"""
add_section_11.py — 给 5 篇示范 paper note 加 §11 1-hop 关系图

5 篇示范: 3DGS / 4DGS / Mobile-GS / Lumina / Flux-GS
"""

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
NOTES_DIR = REPO_ROOT / "docs" / "appendix" / "paper-notes"

# 5 篇示范的 §11 内容（基于已知引用关系 + 49 篇 INDEX 验证）
SECTION_11 = {
    "2023-kerbl-3dgs": """## 11. 1-hop 关系图

### 11.1 引用的相关工作 (downstream)

3DGS 原论文是**起点**——后续几乎所有 3DGS / 4DGS 工作都引用它：

- 3DGS → 4DGS 演化：[2024-wu-4dgs](2024-wu-4dgs.md)（4DGS 原论文）+ [2023-yang-deformable-3dgs](2023-yang-deformable-3dgs.md)（Deformable 3DGS）
- 3DGS 加速：[2024-yu-mip-splatting](2024-yu-mip-splatting.md) + [2023-fan-lightgaussian](2023-fan-lightgaussian.md) + [2024-liu-efficientgs](2024-liu-efficientgs.md)
- 3DGS 移动端：[2025-feng-lumina](2025-feng-lumina.md) + [2026-du-mobile-gs](2026-du-mobile-gs.md) + [2026-du-flux-gs](2026-du-flux-gs.md)
- 4DGS-1K：[2025-yuan-4dgs-1k](2025-yuan-4dgs-1k.md) 等

### 11.2 被引用的后续工作 (upstream)

**全部 49 篇后续工作均引用此 paper**（引用密度最高）。
**v2 用 S2 API 自动拉取完整 cited-by 列表**。
""",
    "2023-yang-deformable-3dgs": """## 11. 1-hop 关系图

### 11.1 引用的相关工作 (downstream)

Deformable 3DGS 是 3DGS → 4DGS 演化的**早期桥梁**：

- **3DGS 原论文**：[2023-kerbl-3dgs](2023-kerbl-3dgs.md)
- **后续 4DGS 工作引用了它**：
  - [2024-wu-4dgs](2024-wu-4dgs.md)（4DGS 原论文，canonical + deformation 范式继承）
  - [2024-li-spacetime-gaussians](2024-li-spacetime-gaussians.md)（geometry-aware KNN 时空网格）
  - [2024-duan-4drotorgs](2024-duan-4drotorgs.md)（canonical rotation，D-NeRF 1257 FPS）

### 11.2 被引用的后续工作 (upstream)

**v2 用 S2 API 自动拉取**。
""",
    "2024-wu-4dgs": """## 11. 1-hop 关系图

### 11.1 引用的相关工作 (downstream)

4DGS 原论文是**4DGS 起点**——后续所有 4DGS 工作的引用基线：

- **3DGS 原论文**：[2023-kerbl-3dgs](2023-kerbl-3dgs.md)
- **Deformable 3DGS**：[2023-yang-deformable-3dgs](2023-yang-deformable-3dgs.md)（canonical + deformation 范式起源）
- **后续 4DGS 加速工作**（全部引用 4DGS 原论文）：
  - [2024-zhang-mega-4dgs-acceleration](2024-zhang-mega-4dgs-acceleration.md)（MEGA，buffer-A/B 残差）
  - [2024-feng-flashgs](2024-feng-flashgs.md)（FlashGS）
  - [2024-chen-hacpp](2024-chen-hacpp.md)（HACPP）
  - [2025-yuan-4dgs-1k](2025-yuan-4dgs-1k.md)（4DGS-1K，动静态分离，**本项目直接对标**）
  - [2025-chen-4dgscc](2025-chen-4dgscc.md)（4DGS-CC，contextual coding）
  - [2025-oh-neo](2025-oh-neo.md)（NEO）
  - [2025-zheng-4dgcpro](2025-zheng-4dgcpro.md)（4DGCPro）
  - [2025-huang-seele](2025-huang-seele.md)（Seele）
  - [2025-li-gifstream](2025-li-gifstream.md)（GifStream）
  - [2025-ke-streamstgs](2025-ke-streamstgs.md)（StreamSTGS）
  - [2025-wang-p4dgs](2025-wang-p4dgs.md)（P4DGS）
  - [2025-youn-success-gs](2025-youn-success-gs.md)（Success-GS）
  - [2025-shi-sparse4dgs](2025-shi-sparse4dgs.md)（Sparse4DGS）
  - [2025-liu-4dgrt](2025-liu-4dgrt.md)（4DGRT）
  - [2025-lee-omg4](2025-lee-omg4.md)（OMG4）
  - [2025-tu-speede3dgs](2025-tu-speede3dgs.md)（SpeeDe3DGS，13.71×）
  - [2026-wang-retimegs](2026-wang-retimegs.md)（RetimeGS，CVPR 2026 Oral）
  - [2026-huang-gaussianfluent](2026-huang-gaussianfluent.md)（GaussianFluent，CVPR 2026 Oral）
  - [2026-liao-sharptimegs](2026-liao-sharptimegs.md)（SharpTimeGS）
  - [2026-li-pd4dgs](2026-li-pd4dgs.md)（PD-4DGS）
  - [2026-yin-cags](2026-yin-cags.md)（CAGS）
  - [2026-li-vedal](2026-li-vedal.md)（VEDAL）
  - [2026-ghosh-gs-nfs](2026-ghosh-gs-nfs.md)（GS-NFS，NVIDIA Jetson 4DGS 25 FPS）
  - [2026-zhao-mmgs](2026-zhao-mmgs.md)（MMGS）
  - [2026-yu-codecsplat](2026-yu-codecsplat.md)（CodecSplat）
  - [2026-li-pocket-slam](2026-li-pocket-slam.md)（Pocket-SLAM）
  - [2026-huang-gaussianfluent](2026-huang-gaussianfluent.md) 等

### 11.2 被引用的后续工作 (upstream)

**4DGS 是 4DGS 派系所有工作的引用基线**——**v2 用 S2 API 自动拉取完整 cited-by 列表**。
""",
    "2025-feng-lumina": """## 11. 1-hop 关系图

### 11.1 引用的相关工作 (downstream)

Lumina 30 references（来自 Semantic Scholar 2026-07-08 验证）：

- **核心相关（7 条）全部已在 INDEX**（**Lumina 30 references 验证案例**）：
  - [2023-kerbl-3dgs](2023-kerbl-3dgs.md)（3DGS 原论文）
  - [2023-yang-deformable-3dgs](2023-yang-deformable-3dgs.md)（Deformable 3DGS）
  - [2024-wu-4dgs](2024-wu-4dgs.md)（4DGS 原论文）
  - [2024-yu-mip-splatting](2024-yu-mip-splatting.md)（Mip-Splatting）
  - [2024-li-spacetime-gaussians](2024-li-spacetime-gaussians.md)（Scaffold-GS 系）
  - [2025-chen-4dgscc](2025-chen-4dgscc.md)（4DGS-CC）
  - [2026-du-mobile-gs](2026-du-mobile-gs.md)（Mobile-GS）

- **23 条不相关**：医学 / 自动驾驶 / SLAM / 任务规划 / 行人预测 / 路径规划 / 双目匹配 / 运动捕捉（**不在本项目调研范围**）

### 11.2 被引用的后续工作 (upstream)

- [2026-du-mobile-gs](2026-du-mobile-gs.md)（Mobile-GS 引用 Lumina 体系结构 co-design）
- [2026-du-flux-gs](2026-du-flux-gs.md)（Flux-GS 也关注 mobile）

**v2 用 S2 API 自动拉取完整 cited-by 列表**。
""",
    "2026-du-mobile-gs": """## 11. 1-hop 关系图

### 11.1 引用的相关工作 (downstream)

Mobile-GS 是小米 / 3DGS 移动端 SOTA：

- **3DGS 原论文**：[2023-kerbl-3dgs](2023-kerbl-3dgs.md)
- **Lumina**：[2025-feng-lumina](2025-feng-lumina.md)（体系结构 co-design 前置工作）
- **Snap 8 Gen 3 实测 127 FPS @ 4.6 MB**（ICLR 2026，深度感知 + OIT + NVQ + 剪枝 5 件套）

### 11.2 被引用的后续工作 (upstream)

- [2026-du-flux-gs](2026-du-flux-gs.md)（Flux-GS 在 Mobile-GS 基础上进一步优化，Snap 8 Gen 3 147 FPS @ 2.1 MB）

**v2 用 S2 API 自动拉取完整 cited-by 列表**。
""",
    "2026-du-flux-gs": """## 11. 1-hop 关系图

### 11.1 引用的相关工作 (downstream)

Flux-GS 是 3DGS 移动端 SOTA（Snap 8 Gen 3 实测 147 FPS @ 2.1 MB）：

- **3DGS 原论文**：[2023-kerbl-3dgs](2023-kerbl-3dgs.md)
- **Mobile-GS**：[2026-du-mobile-gs](2026-du-mobile-gs.md)（直接前置工作）

### 11.2 被引用的后续工作 (upstream)

**v2 用 S2 API 自动拉取完整 cited-by 列表**——预计会成为 3DGS 移动端后续工作的引用基线。
""",
}


def add_section_11(note_id: str) -> bool:
    """给单篇 note 加 §11（如果还没有）"""
    note_path = NOTES_DIR / f"{note_id}.md"
    if not note_path.exists():
        print(f"  ⚠ {note_id}: 文件不存在")
        return False

    with open(note_path) as f:
        content = f.read()

    if "## 11. 1-hop 关系图" in content:
        return False  # 已经有

    section_11 = SECTION_11.get(note_id)
    if not section_11:
        print(f"  ⚠ {note_id}: 没有 §11 内容")
        return False

    # 追加到文末
    new_content = content.rstrip() + "\n\n" + section_11
    with open(note_path, "w") as f:
        f.write(new_content)
    return True


def main():
    added = 0
    skipped = 0
    for note_id in SECTION_11.keys():
        if add_section_11(note_id):
            print(f"  ✅ {note_id}: 加 §11")
            added += 1
        else:
            print(f"  ⏭ {note_id}: 跳过")
            skipped += 1

    print(f"\n✅ 5 篇示范: 新增 §11 = {added} 篇, 跳过 = {skipped} 篇")


if __name__ == "__main__":
    main()
