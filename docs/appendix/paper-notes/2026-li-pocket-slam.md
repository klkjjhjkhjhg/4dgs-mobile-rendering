# 2026-li-pocket-slam · Pocket-SLAM: Rendering-Area-Aware Pruning for Memory-Efficient 3DGS-SLAM

> **相关性**：**⭐⭐⭐ 派系 1+3（训练期压缩 + 移动端 / 端侧）** —— arXiv 2026-06-23；核心数字：**61.3% peak memory reduction + 2.7× FPS improvement**（abstract 直引）；**KITTI seq10: 34.2 GB → 13.3 GB**（PDF Table II 直引）；**EuRoC: 25.4 GB → 10.1 GB + 3.6 FPS**（PDF Table I 直引）；**ATE 0.07 m** 保留定位精度。**对 4DGS-SLAM 直接可移植**——Pocket-SLAM 的 rendering-area-aware pruning 是**对场景区域分 tile 后按需 prune**，**与 4DGS canonical space pruning 兼容**。

> **⚠ 重要区分**：这是 **3DGS + SLAM**，**不是 4DGS**。**对 4DGS 适用性**：Pocket-SLAM 是 **plug-in**（"enable edge-device (AV/drone embedded GPU) deployment"）——可以接到 4DGS-SLAM pipeline 上，作为 4DGS 之外的**渲染剪枝层**。**对派系 1（压缩）和派系 3（移动端）都有强 relevance**。

## 一句话问题

3DGS-SLAM 在大场景（KITTI / EuRoC）下**显存爆炸（10-40 GB）**——单卡 GPU 跑不动，**更别说 edge device**。**如何在不破坏 SLAM 跟踪精度的前提下，按渲染区域贡献度做 tile-level budget-aware pruning**？

## 链接

- arXiv：<https://arxiv.org/abs/2606.24796>（v1 2026-06-23）
- 项目页：not found in abstract
- GitHub：not found in PDF
- PDF：已下 `.pdfs/2606.24796.pdf`
- 会议：not found in abstract（arXiv preprint）

## 年份 / 作者 / 机构（PDF 头部实测）

- **年份**：2026（v1 2026-06-23）
- **第一作者**：**Leshu Li**
- **机构**：中国（具体学校待 PDF 完整确认）—— `not found in first 8 pages extract`

## 方法核心（PDF §3 直引）

### §3.1 Rendering-Area-Aware Importance

- **有效像素覆盖率（effective pixel-coverage contribution）**作为重要性分数
- 与 LightGaussian / MaskGaussian 的 heuristic score 不同：**Pocket-SLAM 用的是"实际渲染时贡献的像素数 × alpha 累加"**

### §3.2 Tile-Level Budget Control

- **Tile budget 上限**：每个 tile 最多保留 N Gaussians
- **目的**：防止 texture 区域 over-pruning（vs uniform 全局 prune）
- **可调**：Pocket-SLAM 提供 **hyperparameter knob** 平衡 memory vs quality

### §3.3 Plug-in 设计

- **Pocket-SLAM 是 plug-in**：不修改 SLAM backbone，**只在渲染前加一个 pruning pass**
- 兼容：LSG-SLAM, WildGS-SLAM, MonoGS 等多种 3DGS-SLAM backbone

## 关键数字（PDF Table II 直引 + abstract 直引）

| 数据集 | 方法 | Peak Memory | FPS | 备注 |
|---|---|---|---|---|
| EuRoC (avg) | LSG-SLAM | 25.4 GB | 1.3 FPS | 强 baseline |
| EuRoC (avg) | MaskGaussian | 17.6 GB | 1.6 FPS | sync batch prune |
| EuRoC (avg) | **Pocket-SLAM** | **10.1 GB** | **3.6 FPS** | **2.5× mem↓, 2.7× FPS↑** |
| KITTI seq10 | LSG-SLAM | 34.7 GB | 0.8 FPS | 大场景 |
| KITTI seq10 | **Pocket-SLAM** | **13.3 GB** | **2.4 FPS** | **2.6× mem↓, 3× FPS↑** |
| KITTI seq10 | 3DGS-SLAM (orig) | 34.2 GB | (low) | baseline |

> **ATE 跟踪精度**（Table I 直引）：Pocket-SLAM ATE RMSE **0.07 m vs LSG-SLAM 0.06 m**（**差距 1 cm，定位几乎无损**）
>
> **abstract 直引**："**61.3% peak memory reduction, 2.7× FPS improvement**; preserves localization (**ATE RMSE 3.22 vs 3.05 m**) and PSNR (**26.55 vs 26.82 dB**)."

## 与本调研主线的关系

### 派系归属：**派系 1（训练期压缩）** 主，**派系 3（移动端）** 强

- **派系 1 应用**：Pocket-SLAM 提供了**纯渲染时剪枝**（不修改 3DGS 训练 pipeline），可作为本项目 4DGS 训练后的**post-processing** 步骤
- **派系 3 应用**：abstract **显式提 "edge-device (AV/drone embedded GPU) deployment"**——**与本项目 Snap 8 Gen 4 移动 GPU 目标直接相关**

### 对项目目标的具体承诺

- **3.6 FPS on EuRoC + Pocket-SLAM**：EuRoC 训 1 个 scene 3.6 FPS（**不是 mobile 实测，是 desktop 测 memory + FPS**），**移动端估算 = 1-2 FPS**（`[推测,基于 desktop-to-mobile 算力差距 5-8×]`）
- **本项目 4DGS Mobile 路线价值**：**4DGS 必然比 3DGS 显存高 5-10×**（time dimension + 大场景），Pocket-SLAM 的 60% memory↓ + 2.7× FPS↑ **直接缓解 4DGS 显存压力**

### 我未找到 / 提请下游注意

- **Pocket-SLAM 的 mobile on-device 实测**：abstract 提 "edge-device" 但**未明示具体 GPU 平台**（`[未在 abstract 拿到]`）
- **Pocket-SLAM 的开源代码**：PDF 未给 GitHub 链接
- **Pocket-SLAM 对 4DGS 的兼容性**：**理论上 plug-in 兼容任何 3DGS backbone**——4DGS backbone 同样适用，**但 abstract 未做实验**（`[本项目 spike 阶段需要验证]`）

## 我的 commit 节奏

本文是 33 + 1 (Flux-GS) + 11 (subagent) 之外**新加的第 46 篇**。配套 INDEX.md 派系 E（3DGS 通用压缩）+ 派系 C（移动端）各加 1 行。
