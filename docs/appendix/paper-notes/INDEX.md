# Paper Notes 索引（按主线分组）

> **本地 PDF stash**: `/.pdfs/`（仓库根目录，**不进 git**，见 `.gitignore`）
> **命名约定**: 大部分用纯 arxiv id（`<arxiv-id>.pdf`），4 篇"早期下"的用易读命名（`4DGS-1K.pdf` / `wu-4dgs.pdf` 等）
> **总计**: **33 篇 paper notes ↔ 33 个本地 PDF**，**约 525 MB**
> **标记**: ⭐⭐⭐ = 本项目直接对标 / ⭐⭐ = 高相关 / ⭐ = 参考
> **本批扩展（25 H2 ~ 26 H1）**: 14 篇（双跳引用链 + arxiv API + Semantic Scholar cited-by 抓出）

---

## A. 4DGS 表示（高精度表示主线，9 篇）

| paper | arxiv id | year | 一句话 | 评 |
|---|---|---|---|---|
| [2024-wu-4dgs.md](2024-wu-4dgs.md) | 2310.08528 | 2023-10 | 4DGS 原论文，canonical + deformation field | ⭐⭐⭐ |
| [2023-yang-deformable-3dgs.md](2023-yang-deformable-3dgs.md) | 2309.13101 | 2023-09 | Deformable 3DGS，canonical anchor + per-frame deformation（NeRF 系起源） | ⭐⭐⭐ |
| [2025-yuan-4dgs-1k.md](2025-yuan-4dgs-1k.md) | 2503.16422 | 2025-03 | **本项目直接对标**，STV 评分 + temporal mask（动静态分离的隐式版本） | ⭐⭐⭐ |
| [2023-attal-hyperreel.md](2023-attal-hyperreel.md) | 2301.02238 | 2023-01 | HyperReel，关键帧 + 光流 warp（NeRF-style 4D） | ⭐⭐ |
| [2024-zhang-mega-4dgs-acceleration.md](2024-zhang-mega-4dgs-acceleration.md) | 2410.13613 | 2024-10 | MEGA，buffer-A/B 残差编码（结构化分离） | ⭐⭐ |
| [2024-duan-4drotorgs.md](2024-duan-4drotorgs.md) | 2402.03306 | 2024-02 | 4D-RotorGS，**canonical rotation**，D-NeRF 1257 FPS（动静态分离的另一变体） | ⭐ |
| [2024-li-spacetime-gaussians.md](2024-li-spacetime-gaussians.md) | 2312.16812 | 2023-12 | Spacetime Gaussians，geometry-aware KNN 时空网格 | ⭐ |
| [2025-shi-sparse4dgs.md](2025-shi-sparse4dgs.md) | 2511.07122 | 2025-11 | Sparse4DGS，稀疏化 + 4DGS 加速 | ⭐ |
| [2025-liu-4dgrt.md](2025-liu-4dgrt.md) | 2509.10759 | 2025-09 | 4DGRT，4DGS Ray Tracing（NTU+Intel） | ⭐ |

---

## B. 4DGS 加速 / 动静态分离（25-26 主线之三，6 篇）

| paper | arxiv id | year | 一句话 | 评 |
|---|---|---|---|---|
| [2026-liao-sharptimegs.md](2026-liao-sharptimegs.md) | 2602.02989 | 2026-02 | **SharpTimeGS**，lifespan modulation 时间/动态分层（隐式动静态分离） | ⭐⭐ |
| [2025-lee-omg4.md](2025-lee-omg4.md) | 2510.03857 | 2025-10 | **OMG4**，minimal 4DGS，imperceptible 时间部分剪枝 | ⭐⭐ |
| [2026-yin-cags.md](2026-yin-cags.md) | 2605.09279 | 2026-05 | **CAGS**，色彩自适应的动静态分层 streaming | ⭐ |
| [2025-tu-speede3dgs.md](2025-tu-speede3dgs.md) | 2506.07917 | 2025-06 | **SpeeDe3DGS**，temporal pruning + motion compensation（UMD, 13.71×） | ⭐⭐ |
| [2025-chen-4dgscc.md](2025-chen-4dgscc.md) | 2504.18925 | 2025-04 | **4DGS-CC**，contextual coding framework | ⭐⭐ |
| [2026-li-pd4dgs.md](2026-li-pd4dgs.md) | 2605.11427 | 2026-05 | **PD-4DGS**，progressive decomposition + R-DO（TMC 一致性） | ⭐⭐ |

---

## C. 渲染加速（pipeline 级，含 3DGS + 4DGS，8 篇）

| paper | arxiv id | year | 一句话 | 评 |
|---|---|---|---|---|
| [2026-du-mobile-gs.md](2026-du-mobile-gs.md) | 2603.11531 | 2026-03 | **Mobile-GS**，Snap 8 Gen 3 上 127 FPS（**Vulkan 2.0**） | ⭐⭐⭐ |
| [2025-feng-lumina.md](2025-feng-lumina.md) | 2506.05682 | 2025-06 | **Lumina: Real-Time Mobile Neural Rendering**，SJTU+Rochester，**4.5× speedup + 5.3× energy** | ⭐⭐⭐ |
| [2025-oh-neo.md](2025-oh-neo.md) | 2511.12930 | 2025-11 | **Neo: On-Device 3DGS** with **Reuse-and-Update Sorting Accelerator** | ⭐⭐⭐ |
| [2024-yu-mip-splatting.md](2024-yu-mip-splatting.md) | 2311.16493 | 2023-11 | Mip-Splatting，CVPR 2024 best student（尺度修正） | ⭐⭐ |
| [2024-feng-flashgs.md](2024-feng-flashgs.md) | 2408.07967 | 2024-08 | FlashGS，CVPR 2025 | ⭐⭐ |
| [2024-liu-efficientgs.md](2024-liu-efficientgs.md) | 2404.12777 | 2024-04 | EfficientGS | ⭐ |
| [2024-chen-fcgs.md](2024-chen-fcgs.md) | 2410.08017 | 2024-10 | FCGS，Monash U（频率压缩） | ⭐ |
| [2024-chen-hacpp.md](2024-chen-hacpp.md) | 2501.12255 | 2025-01 | HAC++，ECCV 2024（hierarchical anchor compression） | ⭐ |

---

## D. 流式 streaming / 移动端落地（6 篇）

| paper | arxiv id | year | 一句话 | 评 |
|---|---|---|---|---|
| [2025-wang-airgs.md](2025-wang-airgs.md) | 2512.20943 | 2025-12 | **AirGS**，4DGS streaming + ILP pruning（**6× 训练加速** + 50% transmission） | ⭐⭐ |
| [2025-ke-streamstgs.md](2025-ke-streamstgs.md) | 2511.06046 | 2025-11 | **StreamSTGS**，streaming spatial-temporal grids（real-time FVV） | ⭐⭐ |
| [2025-li-gifstream.md](2025-li-gifstream.md) | 2505.07539 | 2025-05 | **GIFStream**，4D Gaussian feature stream | ⭐ |
| [2025-wang-p4dgs.md](2025-wang-p4dgs.md) | 2510.10030 | 2025-10 | **P-4DGS**，**90× compression**（predictive 4DGS） | ⭐ |
| [2025-zheng-4dgcpro.md](2025-zheng-4dgcpro.md) | 2509.17513 | 2025-09 | **4DGCPro**，4DGS mobile streaming（abstract 级） | ⭐ |
| [2025-liu-4dgrt.md](2025-liu-4dgrt.md) | 2509.10759 | 2025-09 | 4DGRT，4DGS Ray Tracing（NTU+Intel） | ⭐ |

---

## E. 3DGS 静态加速 / 通用加速（3 篇）

| paper | arxiv id | year | 一句话 | 评 |
|---|---|---|---|---|
| [2024-navaneet-compact3d.md](2024-navaneet-compact3d.md) | 2312.08826 | 2023-12 | Compact3D，ECCV 2024 | ⭐ |
| [2023-fan-lightgaussian.md](2023-fan-lightgaussian.md) | 2311.17245 | 2023-11 | LightGaussian，NeurIPS 2024 Spotlight | ⭐ |
| [2025-huang-seele.md](2025-huang-seele.md) | 2503.05168 | 2025-03 | SEELE（SJTU） | ⭐ |
| [2026-zhang-geta3dgs.md](2026-zhang-geta3dgs.md) | 2605.02086 | 2026-05 | **GETA-3DGS**，joint structured pruning + quantization | ⭐⭐ |

---

## F. Survey / Roadmap（写作参考，1 篇）

| paper | arxiv id | year | 一句话 | 评 |
|---|---|---|---|---|
| [2025-youn-success-gs.md](2025-youn-success-gs.md) | 2512.07197 | 2025-12 | SUCCESS-GS survey，Parameter/Restructuring 二分法（Chung-Ang+Kyung Hee, 37 页） | ⭐⭐ |
| (内部 [docs/04-trends-2026H1.md](../../04-trends-2026H1.md)) | — | 2026-07 | 本项目自有趋势分析 | ⭐⭐⭐ |

---

## 总数与对照组

```
- **33 篇 paper notes ↔ 33 个本地 PDF**（一一对应，无遗漏）
- **约 525 MB 总计**（`.pdfs/`）
- **2023**：4 篇
- **2024 H1**：5 篇
- **2024 H2**：4 篇
- **2025 H1**：7 篇
- **2025 H2**：6 篇
- **2026 H1**：7 篇
```

**重点提示**: 25 H2 ~ 26 H1 = **强加速期**（13 / 33 = 39% 的论文集中这 12 月内）

---

## ⚠️ 已知空白（待补 paper notes）

下面是 README / §02 / §04 提到但**还没写独立 paper note** 的（虽然 PDF 已在 `.pdfs/` 或尚未下）：

- **动静态分离专门派**: Drivable 3DGS（2503.15882）/ SVG4D（2505.02957）/ ZAWoR（2506.23514）— abstract 已在 §01 §6 中引用，但**未单独建 paper note**
- **3DGS 加速派**: EffiGaussian++（2505.14919）/ HiP-GS（2503.17903）/ GO-VAE（2504.15644）/ MP-GS（2601.07918）/ Neo mobile 实测 / GaussianStream（2510.16862）
- **Survey**: Deep Review（2504.19053）/ Pipeline Survey（2507.19122）/ LoWiS（2504.09080）

→ **这是下一轮调研该补的方向**（用户应该明示 PR 优先级）

---

## 重新下载某个 PDF

```bash
cd .pdfs
curl -sL --max-time 90 -o <arxiv-id>.pdf https://arxiv.org/pdf/<arxiv-id>
```

如要给新加的 paper note 配 PDF，**用纯 arxiv id 命名**（如 `2603.11531.pdf`），不用易读名；**不要 commit**（已在 `.gitignore` 排除整个 `.pdfs/` 目录）。
