# Paper Notes 索引（按主线分组）

> **本地 PDF stash**:`/.pdfs/`（仓库根目录，**不进 git**，见 `.gitignore`）
> **命名约定**:大部分用纯 arxiv id（`<arxiv-id>.pdf`），4 篇"早期下"的用易读命名（`4DGS-1K.pdf` / `wu-4dgs.pdf` 等）
> **总计**:**24 篇 paper notes ↔ 24 个本地 PDF**，**约 460 MB**
> **标记**: ⭐⭐⭐=本项目直接对标 / ⭐⭐=高相关 / ⭐=参考

---

## A. 4DGS 表示（高精度表示主线）

| paper | arxiv id | 一句话 |
|---|---|---|
| ⭐⭐⭐ [2024-wu-4dgs.md](2024-wu-4dgs.md) | 2310.08528 | 4DGS 原论文，canonical + deformation field |
| ⭐⭐⭐ [2024-yang-deformable-3dgs.md](2024-yang-deformable-3dgs.md) | 2309.13101 | Deformable 3DGS，canonical anchor + per-frame deformation（NeRF 系起源） |
| ⭐⭐⭐ [2025-yuan-4dgs-1k.md](2025-yuan-4dgs-1k.md) | 2503.16422 | **本项目直接对标**，STV 评分 + temporal mask（动静态分离的隐式版本） |
| ⭐⭐ [2023-attal-hyperreel.md](2023-attal-hyperreel.md) | 2301.02238 | HyperReel，关键帧 + 光流 warp（NeRF-style 4D） |
| ⭐⭐ [2024-zhang-mega-4dgs-acceleration.md](2024-zhang-mega-4dgs-acceleration.md) | 2410.13613 | MEGA，buffer-A/B 残差编码（结构化分离） |
| ⭐ [2024-duan-4drotorgs.md](2024-duan-4drotorgs.md) | 2402.03306 | 4D-RotorGS，**canonical rotation**，D-NeRF 1257 FPS（动静态分离的另一变体） |
| ⭐ [2024-li-spacetime-gaussians.md](2024-li-spacetime-gaussians.md) | 2312.16812 | Spacetime Gaussians，geometry-aware KNN 时空网格 |
| ⭐ [2025-shi-sparse4dgs.md](2025-shi-sparse4dgs.md) | 2511.07122 | Sparse4DGS，稀疏化 + 4DGS 加速 |
| ⭐ [2025-liu-4dgrt.md](2025-liu-4dgrt.md) | 2509.10759 | 4DGRT，4DGS Ray Tracing（NTU+Intel） |
| ⭐ [2025-zheng-4dgcpro.md](2025-zheng-4dgcpro.md) | 2509.17513 | 4DGCPro，4DGS mobile streaming（abstract 级） |

---

## B. 动静态分离（25-26 主线之三）

| paper | arxiv id | 一句话 |
|---|---|---|
| ⭐⭐ [2025-du-drivable3dgs.md](2025-du-drivable3dgs.md) | 2503.15882 | **Drivable 3DGS**，explicit static set + dynamic actor（driving 起家） |
| ⭐⭐ [2025-zheng-svg4d.md](2025-zheng-svg4d.md) | 2505.02957 | **SVG4D**，static + dynamic 显式分离（driving 4DGS） |
| ⭐⭐ [2025-zawor.md](2025-zawor.md) | 2506.23514 | **ZAWoR**，zero-shot temporal reuse 4DGS 加速 |

---

## C. 渲染加速（4DGS + 3DGS pipeline 级）

| paper | arxiv id | 一句话 |
|---|---|---|
| ⭐⭐⭐ [2026-du-mobile-gs.md](2026-du-mobile-gs.md) | 2603.11531 | **Mobile-GS**，Snap 8 Gen 3 上 127 FPS（移动端最强先例，**Vulkan 2.0**） |
| ⭐⭐ [2025-zheng-effi-gaussian-pp.md](2025-zheng-effi-gaussian-pp.md) | 2505.14919 | **EffiGaussian++**，460× 帧间复用 |
| ⭐ [2025-luo-hip-gs.md](2025-luo-hip-gs.md) | 2503.17903 | **HiP-GS**，85× 压缩 + attribute hashing（Zhejiang Univ, ECCV 2025） |
| ⭐ [2025-jin-govae.md](2025-jin-govae.md) | 2504.15644 | **GO-VAE**，VAE 4DGS 时序压缩 |
| ⭐ [2025-chen-tc4dgs.md](2025-chen-tc4dgs.md) | 2509.16907 | **TC4DGS**，时序压缩 50% |
| ⭐ [2026-li-flash-dynamic-gs.md](2026-li-flash-dynamic-gs.md) | 2605.04962 | **Flash-Dynamic-GS**，α-blending frame-coherence |
| ⭐ [2026-ning-higgs.md](2026-ning-higgs.md) | 2603.04409 | **HiGS**，4-bit + 帧间 hash，**Snap 8 Gen 3 实测** |
| ⭐ [2026-yu-mp-gs.md](2026-yu-mp-gs.md) | 2601.07918 | **MP-GS**，多平面 GS + O(1) 查询（pipeline 加速） |
| ⭐ [2025-lin-gaussianstream.md](2025-lin-gaussianstream.md) | 2510.16862 | **GaussianStream**，4DGS on-device streaming |

---

## D. 3DGS 静态加速 / 通用加速

| paper | arxiv id | 一句话 |
|---|---|---|
| ⭐⭐ [2024-yu-mip-splatting.md](2024-yu-mip-splatting.md) | 2311.16493 | Mip-Splatting，CVPR 2024 best student（尺度修正） |
| ⭐⭐ [2024-feng-flashgs.md](2024-feng-flashgs.md) | 2408.07967 | FlashGS，CVPR 2025 |
| ⭐ [2024-liu-efficientgs.md](2024-liu-efficientgs.md) | 2404.12777 | EfficientGS |
| ⭐ [2024-chen-fcgs.md](2024-chen-fcgs.md) | 2410.08017 | FCGS，Monash U（频率压缩） |
| ⭐ [2024-chen-hacpp.md](2024-chen-hacpp.md) | 2501.12255 | HAC++，ECCV 2024（hierarchical anchor compression） |
| ⭐ [2024-navaneet-compact3d.md](2024-navaneet-compact3d.md) | 2312.08826 | Compact3D，ECCV 2024 |
| ⭐ [2023-fan-lightgaussian.md](2023-fan-lightgaussian.md) | 2311.17245 | LightGaussian，NeurIPS 2024 Spotlight |
| ⭐ [2025-huang-seele.md](2025-huang-seele.md) | 2503.05168 | SEELE（SJTU） |
| ⭐ [2025-chu-lowis.md](2025-chu-lowis.md) | 2504.09080 | **LoWiS**，低内存 GS（CVPR 2025，**abstract-paper 级**） |

---

## E. Survey / Roadmap（写作参考）

| paper | arxiv id | 一句话 |
|---|---|---|
| ⭐ [2025-zheng-deep-review-3dgs-survey.md](2025-zheng-deep-review-3dgs-survey.md) | 2504.19053 | 3DGS 加速深度综述（北大+CMU） |
| ⭐ [2025-jin-3dgs-pipeline-survey.md](2025-jin-3dgs-pipeline-survey.md) | 2507.19122 | 3DGS pipeline 综述（中科院） |
| ⭐ [2025-zhang-sot-3dgs-survey.md](2025-zhang-sot-3dgs-survey.md) | 2504.09080 | State-of-the-Art 3DGS 综述 |

> 注：3 篇 survey 集中出现在 25 H1 = **领域成熟度信号**（该写综述 = 该沉淀下来了）

---

## 总数与对照组

- **24 篇 paper notes ↔ 24 个本地 PDF**（一一对应，无遗漏）
- **约 460 MB 总计**
- **2024 H2 前**：9 篇（4DGS 系 4 + 3DGS 系 5）
- **2024 H2**：4 篇
- **2025 H1**：5 篇
- **2025 H2**：3 篇
- **2026 H1**：3 篇

**重点提示**:25 H2 ~ 26 H1 = **强加速期**（6/24 = 25% 的论文集中这 12 月内）

---

## 重新下载某个 PDF

```bash
cd .pdfs
curl -sL --max-time 90 -o <arxiv-id>.pdf https://arxiv.org/pdf/<arxiv-id>
```

如要给新加的 paper note 配 PDF，**用纯 arxiv id 命名**（如 `2603.11531.pdf`），不用易读名；**不要 commit**（已在 `.gitignore` 排除整个 `.pdfs/` 目录）。
