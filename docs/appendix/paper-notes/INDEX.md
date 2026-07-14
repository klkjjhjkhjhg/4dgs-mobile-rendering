# Paper Notes 索引（按主线分组）

> **本地 PDF stash**: `/.pdfs/`（仓库根目录，**不进 git**，见 `.gitignore`）
> **命名约定**: 大部分用纯 arxiv id（`<arxiv-id>.pdf`），4 篇"早期下"的用易读命名（`4DGS-1K.pdf` / `wu-4dgs.pdf` 等）
> **总计**: **59 篇 paper notes ↔ 59 个本地 PDF**（截至 2026-07-13，含本批 1 篇 MVFusion-GS，v5.44 删 2017-simon-handkeypoint 早于 3DGS 提出 2023-08, 不在调研范围）
> **标记**: ⭐⭐⭐ = 本项目直接对标 / ⭐⭐ = 高相关 / ⭐ = 参考
> **本批扩展（25 H2 ~ 26 H1）**: 14 篇 — `Flux-GS` (ECCV 2026) + 13 篇 2026 H1 arxiv (3DGS 加速 / 压缩 / mobile / streaming 派系)
> **本批触发**: 用户用 GitHub 链接 `https://github.com/xiaobiaodu/Flux-GS` 作为入口，扩到同期 13 篇相关工作
> **本批 2（2026-07-08 ECCV/CVPR 专扫）**: 2 篇 CVPR 2026 Oral — `RetimeGS` (4DGS continuous-time, HKUST+Netflix) + `GaussianFluent` (3DGS 物理模拟, PKU+BIGAI)。**ECCV 2026 接收名单尚未公开（9 月会议，arXiv+web 搜索 4 来源无数据）**；CVPR 2026 Poster 全名单非常稀疏（amusi 3DGS 段仅 3 篇），本项目相关核心（Mobile-GS / Flux-GS / Flow4DGS-SLAM / RAP / FastGS / Topology-Aware）已在前批 commit 覆盖。
> **本批 4（2026-07-13 arxiv 扫描）**: 1 篇 TIER 1 4DGS — `MVFusion-GS` (Tsinghua + UT Dallas + UESTC, 2026-07-02 arxiv)。**Motion-Variance Guided Refinement + MotionFormer Temporal Attention 双模块 plug-in DeGauss**，Neu3D +0.55 dB PSNR 同时 42% 动态 Gaussian 压缩。无 mobile 评测。22 篇新候选已分类 TIER 1/2/3（cron 预算只收 TIER 1）。

---

## A. 4DGS 表示（高精度表示主线，13 篇）

| paper | arxiv id | year | 一句话 | 评 |
|---|---|---|---|---|
| [2024-wu-4dgs.md](2024-wu-4dgs.md) | 2310.08528 | 2023-10 | 4DGS 原论文，canonical + deformation field | ⭐⭐⭐ |
| [2023-yang-deformable-3dgs.md](2023-yang-deformable-3dgs.md) | 2309.13101 | 2023-09 | Deformable 3DGS，canonical anchor + per-frame deformation（NeRF 系起源） | ⭐⭐⭐ |
| [2025-yuan-4dgs-1k.md](2025-yuan-4dgs-1k.md) | 2503.16422 | 2025-03 | **本项目直接对标**，STV 评分 + temporal mask（动静态分离的隐式版本） | ⭐⭐⭐ |
| [2023-attal-hyperreel.md](2023-attal-hyperreel.md) | 2301.02238 | 2023-01 | HyperReel，关键帧 + 光流 warp（NeRF-style 4D） | ⭐⭐ |
| [2024-zhang-mega-4dgs-acceleration.md](2024-zhang-mega-4dgs-acceleration.md) | 2410.13613 | 2024-10 | MEGA，buffer-A/B 残差编码（结构化分离） | ⭐⭐ |
| [2024-duan-4drotorgs.md](2024-duan-4drotorgs.md) | 2402.03307 | 2024-02 | 4D-RotorGS，**canonical rotation** (arxiv-id corrected from prior 2402.03306 which is a math paper by Perrotin)，D-NeRF 1257 FPS（动静态分离的另一变体） | ⭐ |
| [2024-li-spacetime-gaussians.md](2024-li-spacetime-gaussians.md) | 2312.16812 | 2023-12 | Spacetime Gaussians，geometry-aware KNN 时空网格 | ⭐ |
| [2025-shi-sparse4dgs.md](2025-shi-sparse4dgs.md) | 2511.07122 | 2025-11 | Sparse4DGS，稀疏化 + 4DGS 加速 | ⭐ |
| [2025-liu-4dgrt.md](2025-liu-4dgrt.md) | 2509.10759 | 2025-09 | 4DGRT，4DGS Ray Tracing（NTU+Intel） | ⭐ |
| [2026-wang-retimegs.md](2026-wang-retimegs.md) | 2603.13783 | 2026-03 | **RetimeGS** (CVPR 2026 Oral, HKUST+Netflix)，4DGS continuous-time 表示，**消除 temporal aliasing + ghost-free frame interpolation** | ⭐⭐⭐ |
| [2026-huang-gaussianfluent.md](2026-huang-gaussianfluent.md) | 2601.09265 | 2026-01 | **GaussianFluent** (CVPR 2026 Oral, PKU+BIGAI)，3DGS + MPM 物理模拟（elastic / fracture / slicing）+ 混合材质 | ⭐⭐ |
| [2026-song-l2d2-gs.md](2026-song-l2d2-gs.md) | 2606.29374 | 2026-06 | **L2D2-GS** (小米+北大联合)，feedforward 4DGS 动态场景重建 + 自监督 densification policy（**对作者 heliangliang@xiaomi.com 有合作背景**） | ⭐⭐⭐ |
| [2026-hu-mvfusion-gs.md](2026-hu-mvfusion-gs.md) | 2607.01578 | 2026-07 | **MVFusion-GS** (Tsinghua + UT Dallas + UESTC)，plug-in DeGauss with Motion-Variance guided refinement + MotionFormer Temporal Attention 双机制，Neu3D 32.07 dB (+0.55 vs DeGauss) + 42% 动态 Gaussian 压缩 (56,533 → 32,985) | ⭐⭐ |

---

## B. 4DGS 加速 / 动静态分离（25-26 主线之三，7 篇）

| paper | arxiv id | year | 一句话 | 评 |
|---|---|---|---|---|
| [2026-liao-sharptimegs.md](2026-liao-sharptimegs.md) | 2602.02989 | 2026-02 | **SharpTimeGS**，lifespan modulation 时间/动态分层（隐式动静态分离） | ⭐⭐ |
| [2025-lee-omg4.md](2025-lee-omg4.md) | 2510.03857 | 2025-10 | **OMG4**，minimal 4DGS，imperceptible 时间部分剪枝 | ⭐⭐ |
| [2026-yin-cags.md](2026-yin-cags.md) | 2605.09279 | 2026-05 | **CAGS**，色彩自适应的动静态分层 streaming | ⭐ |
| [2025-tu-speede3dgs.md](2025-tu-speede3dgs.md) | 2506.07917 | 2025-06 | **SpeeDe3DGS**，temporal pruning + motion compensation（UMD, 13.71×） | ⭐⭐ |
| [2025-chen-4dgscc.md](2025-chen-4dgscc.md) | 2504.18925 | 2025-04 | **4DGS-CC**，contextual coding framework | ⭐⭐ |
| [2026-li-pd4dgs.md](2026-li-pd4dgs.md) | 2605.11427 | 2026-05 | **PD-4DGS**，progressive decomposition + R-DO（TMC 一致性） | ⭐⭐ |
| [2026-ren-cubifygs.md](2026-ren-cubifygs.md) | 2606.28720 | 2026-06 | **CubifyGS**，object-level asset + rigid rearrangement lifelong dynamic scene（**>40× faster than WildGS-SLAM**） | ⭐ |

---

## C. 渲染加速（pipeline 级，含 3DGS + 4DGS，12 篇）

| paper | arxiv id | year | 一句话 | 评 |
|---|---|---|---|---|
| [2026-du-flux-gs.md](2026-du-flux-gs.md) | 2606.30017 | 2026-06 | **Flux-GS** (ECCV 2026)，Mobile-GS 团队继任作，**Snap 8 Gen 3 147 FPS @ 2.1 MB**（Indoor） | ⭐⭐⭐ |
| [2026-du-mobile-gs.md](2026-du-mobile-gs.md) | 2603.11531 | 2026-03 | **Mobile-GS**，Snap 8 Gen 3 上 127 FPS（**Vulkan 2.0**） | ⭐⭐⭐ |
| [2025-feng-lumina.md](2025-feng-lumina.md) | 2506.05682 | 2025-06 | **Lumina: Real-Time Mobile Neural Rendering**，SJTU+Rochester，**4.5× speedup + 5.3× energy** | ⭐⭐⭐ |
| [2025-oh-neo.md](2025-oh-neo.md) | 2511.12930 | 2025-11 | **Neo: On-Device 3DGS** with **Reuse-and-Update Sorting Accelerator** | ⭐⭐⭐ |
| [2026-thomas-gausslite.md](2026-thomas-gausslite.md) | 2606.30809 | 2026-06 | **GaussLite** (MIT AeroAstro)，**4 Hz real-time on resource-constrained hardware** + task-conditioned density | ⭐⭐ |
| [2026-li-pocket-slam.md](2026-li-pocket-slam.md) | 2606.24796 | 2026-06 | **Pocket-SLAM**，3DGS-SLAM **60% memory↓ + 2.7× FPS↑**（KITTI seq10 34.2→13.3 GB） | ⭐⭐ |
| [2026-gong-dict-3dgs.md](2026-gong-dict-3dgs.md) | 2605.30396 | 2026-05 | **Smaller-Faster-3DGS** (Linköping)，post-training dictionary learning，**3.95×/3.10×/4.55× comp** + 23-25% FPS↑ | ⭐⭐ |
| [2024-yu-mip-splatting.md](2024-yu-mip-splatting.md) | 2311.16493 | 2023-11 | Mip-Splatting，CVPR 2024 best student（尺度修正） | ⭐⭐ |
| [2024-feng-flashgs.md](2024-feng-flashgs.md) | 2408.07967 | 2024-08 | FlashGS，CVPR 2025 | ⭐⭐ |
| [2024-liu-efficientgs.md](2024-liu-efficientgs.md) | 2404.12777 | 2024-04 | EfficientGS | ⭐ |
| [2024-chen-fcgs.md](2024-chen-fcgs.md) | 2410.08017 | 2024-10 | FCGS，Monash U（频率压缩） | ⭐ |
| [2024-chen-hacpp.md](2024-chen-hacpp.md) | 2501.12255 | 2025-01 | HAC++，ECCV 2024（hierarchical anchor compression） | ⭐ |
| [2026-poirier-ginter-gray.md](2026-poirier-ginter-gray.md) | 2606.30869 | 2026-06 | **GRay** (ACM CGIT 2026, U. Laval + Inria)，3DGS ray tracing **4× vs 3DGRT, 248 FPS**（桌面 RTX 唯一平台） | ⭐⭐ |
| [2026-zhou-temporalgs.md](2026-zhou-temporalgs.md) | 2607.03390 | 2026-07 | **TemporalGS** (McGill + Waterloo + Toronto)，**首个 training-free plug-and-play** 3DGS 加速，**up to 1.48×**，作者未来工作明示"develop a 4DGS counterpart" | ⭐⭐ |

---

## D. 流式 streaming / 移动端落地（10 篇）

| paper | arxiv id | year | 一句话 | 评 |
|---|---|---|---|---|
| [2026-ghosh-gs-nfs.md](2026-ghosh-gs-nfs.md) | 2606.05650 | 2026-06 | **GS-NFS** (NVIDIA Research)，**4DGS 25 FPS decode on Jetson Orin mobile GPU** | ⭐⭐⭐ |
| [2025-wang-airgs.md](2025-wang-airgs.md) | 2512.20943 | 2025-12 | **AirGS**，4DGS streaming + ILP pruning（**6× 训练加速** + 50% transmission） | ⭐⭐ |
| [2025-zheng-4dgcpro.md](2025-zheng-4dgcpro.md) | 2509.17513 | 2025-09 | **4DGCPro**，4DGS mobile streaming（abstract 级） | ⭐⭐ |
| [2026-li-pd4dgs.md](2026-li-pd4dgs.md) | 2605.11427 | 2026-05 | **PD-4DGS**（同时见派系 B），**iPhone 2 Mbps 移动网络 1.7s 启动**，progressive decomposition + R-DO | ⭐⭐ |
| [2025-ke-streamstgs.md](2025-ke-streamstgs.md) | 2511.06046 | 2025-11 | **StreamSTGS**，streaming spatial-temporal grids（real-time FVV） | ⭐⭐ |
| [2026-shi-evogs.md](2026-shi-evogs.md) | 2606.07179 | 2026-06 | **EvoGS**，continuous-layered Evolution Tree，**2.4× payload↓, 5.5× VRAM↓, redundancy 65%→25%** | ⭐⭐ |
| [2026-veicht-zipsplat.md](2026-veicht-zipsplat.md) | 2606.05102 | 2026-06 | **ZipSplat** (ETH/Microsoft)，feed-forward 3DGS，**6× fewer Gaussians** + token-based scene | ⭐⭐ |
| [2026-yu-codecsplat.md](2026-yu-codecsplat.md) | 2605.25563 | 2026-05 | **CodecSplat** (PKU)，ultra-compact latent coding，**20-108 KiB/scene** | ⭐ |
| [2025-li-gifstream.md](2025-li-gifstream.md) | 2505.07539 | 2025-05 | **GIFStream**，4D Gaussian feature stream | ⭐ |
| [2025-wang-p4dgs.md](2025-wang-p4dgs.md) | 2510.10030 | 2025-10 | **P-4DGS**，**90× compression**（predictive 4DGS） | ⭐ |
| [2025-liu-4dgrt.md](2025-liu-4dgrt.md) | 2509.10759 | 2025-09 | 4DGRT，4DGS Ray Tracing（NTU+Intel） | ⭐ |

---

## E. 3DGS 静态加速 / 通用加速（8 篇）

| paper | arxiv id | year | 一句话 | 评 |
|---|---|---|---|---|
| [2023-kerbl-3dgs.md](2023-kerbl-3dgs.md) | 2308.04079 | 2023-08 | **3DGS 原论文**（INRIA, SIGGRAPH 2023 Best Paper），3D Gaussian Splatting for Real-Time Radiance Field Rendering | ⭐⭐⭐ |
| [2023-navaneet-compact3d.md](2023-navaneet-compact3d.md) | 2312.08826 | 2023-12 | Compact3D，ECCV 2024 | ⭐ |
| [2023-fan-lightgaussian.md](2023-fan-lightgaussian.md) | 2311.17245 | 2023-11 | LightGaussian，NeurIPS 2024 Spotlight | ⭐ |
| [2025-huang-seele.md](2025-huang-seele.md) | 2503.05168 | 2025-03 | SEELE（SJTU） | ⭐ |
| [2026-zhang-geta3dgs.md](2026-zhang-geta3dgs.md) | 2605.02086 | 2026-05 | **GETA-3DGS**，joint structured pruning + quantization | ⭐⭐ |
| [2026-li-vedal.md](2026-li-vedal.md) | 2606.02346 | 2026-06 | **VEDAL** (NUST+PolyU)，variational free-energy pruning，**5.2× comp, 0.31 dB PSNR drop, 185 FPS** | ⭐⭐ |
| [2026-chen-refine.md](2026-chen-refine.md) | 2606.09074 | 2026-06 | **REFINE** (西工大)，**3,000× pruning compute↓ + ~20× device-latency speedup**（Hessian-field 解析） | ⭐⭐ |
| [2026-zhao-ace-gs.md](2026-zhao-ace-gs.md) | 2606.21244 | 2026-06 | **ACE-GS** (单作者)，momentum consistency + statistical sensitivity，**4.5× 训练加速 + 745 FPS** | ⭐⭐ |
| [2026-zhao-mmgs.md](2026-zhao-mmgs.md) | 2605.19304 | 2026-05 | **MMGS** (CQU)，multi-view ranking + optimal transport，**10× comp, 10× 训练加速** | ⭐⭐ |
| [2026-mousa-provablepruning.md](2026-mousa-provablepruning.md) | 2607.02721 | 2026-07 | **Provable Pruning** (Univ. of Haifa)，**首个 3DGS 可证明 coreset theorem**，resolution-dependent importance score（理论意义大于工程加速比） | ⭐⭐ |
| [2026-hong-ploymerge.md](2026-hong-polymerge.md) | 2606.16232 | 2026-06 | **PolyMerge** (UC Berkeley)，polytope coverings + Crazyflie drone on-board CBF | ⭐⭐ |

> *注：PolyMerge 文件路径为 `2026-hong-polymerge.md`（修正拼写，之前为 `ploymerge`）*

---

## F. Survey / Roadmap（写作参考，1 篇）

| paper | arxiv id | year | 一句话 | 评 |
|---|---|---|---|---|
| [2025-youn-success-gs.md](2025-youn-success-gs.md) | 2512.07197 | 2025-12 | SUCCESS-GS survey，Parameter/Restructuring 二分法（Chung-Ang+Kyung Hee, 37 页） | ⭐⭐ |
| (内部 [docs/04-trends-2026H1.md](../../04-trends-2026H1.md)) | — | 2026-07 | 本项目自有趋势分析 | ⭐⭐⭐ |

---

## 总数与对照组

```
- **54 篇 paper notes ↔ 54 个本地 PDF**（一一对应，无遗漏）
- **约 790 MB 总计**（`.pdfs/`，截至 2026-07-08）
- **2023**：4 篇
- **2024 H1**：5 篇
- **2024 H2**：4 篇
- **2025 H1**：7 篇
- **2025 H2**：6 篇
- **2026 H1**：27 篇  ←  本批 3 (2026-07-09 cron) 加 4 篇 (mousa / poirier / song / zhou)
```
- 合计 54 + 6 + 1 = **61 篇** 已编 INDEX（v5.43 增 MVFusion-GS 后含 60 paper notes + INDEX.md = 61 .md）
- A. 4DGS 表示（13 篇）  ←  本批 4 加 1 (hu-mvfusion-gs, plug-in DeGauss)
- B. 4DGS 加速 / 动静态分离（7 篇）
- C. 渲染加速 / 移动端（14 篇）  ←  本批 3 加 2 (poirier-gray / zhou-temporalgs)
- D. 流式 streaming / 移动端落地（11 篇）  ←  本批 3 加 1 (mousa-provablepruning, 部署理论)
- E. 3DGS 静态加速 / 通用（9 篇）  ←  补 3DGS 原论文 (2023-kerbl-3dgs) + navaneet 命名修正
- F. Survey / Roadmap（1 篇）
- **合计 61 篇**

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

## G. 4DGS 前身 / 数据集 / 相关工作（6 篇）  ←  v5.42 补全 survey.bib cite key, v5.44 删 2017-simon-handkeypoint（17 年早于 3DGS 提出, 不属 4DGS 调研范围）

| paper | arxiv id | year | 一句话 | 评 |
|---|---|---|---|---|
| [2023-kerbl-3dgs.md](2023-kerbl-3dgs.md) | 2308.04079 | 2023-08 | 3DGS 原论文, SIGGRAPH 2023 Best Paper (INRIA) | ⭐⭐⭐ |
| [2023-navaneet-compact3d.md](2023-navaneet-compact3d.md) | 2311.18159 | 2023-11 | CompGS/Compact3D, residual VQ, 15× reduction + 200+ FPS (UMBC) | ⭐⭐ |
| [2021-pumarola-dnerf.md](2021-pumarola-dnerf.md) | 2011.13961 | 2020-11 | D-NeRF, monocular dynamic NeRF (UB+ETH) | ⭐⭐ |
| [2021-park-nerfies.md](2021-park-nerfies.md) | 2011.12948 | 2020-11 | Nerfies, deformable NeRF (Google+UW) | ⭐⭐ |
| [2021-park-hypernerf.md](2021-park-hypernerf.md) | 2106.13228 | 2021-06 | HyperNeRF, topology-varying + vrig dataset (Google) | ⭐⭐ |
| [2022-gao-dycheck.md](2022-gao-dycheck.md) | 2210.13445 | 2022-10 | DyCheck iPhone dataset, 5 scenes (UCB+FAIR+Google) | ⭐⭐ |
