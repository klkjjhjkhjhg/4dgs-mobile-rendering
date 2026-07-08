# 2026-li-vedal · VEDAL: Variational Error-Driven Asynchronous Learning for 3D Gaussian Splatting Pruning

> **相关性**：**⭐⭐ 派系 1（训练期压缩）** —— arXiv 2026-06-01；核心数字：**5.2× compression + 0.31 dB PSNR drop + 185 FPS**（abstract 直引）；**Mip-NeRF 360 VEDAL = 0.63M Gaussians, 141 MB, 185 FPS, 27.17 dB**（PDF Table 1 直引）。**Variational free-energy minimization + 异步 pruning + KL sparsity prior** 形式化（区别于 LightGaussian 的 heuristic score 和 PUP 3D-GS 的 sync batch）。**abstract 显式提 "memory-constrained devices" 作为 motivation**，**但无 on-device 实测**。

> **⚠ 重要区分**：这是 **3DGS（静态）** pruning 工作，**不是 4DGS**。**对 4DGS 适用性**：variational 框架 + 异步 pruning + KL sparsity prior 都是**模型无关**的，可直接套到 4DGS canonical-space Gaussians 上。**对本项目 M3 spike 阶段有方法学价值**。

## 一句话问题

现有 3DGS pruning 方法用 **heuristic importance score**（快但次优）或 **synchronous batch update**（一致但慢），**如何在 closed-form variational 框架下，做到 prediction-error gating + 异步更新，且数学可证 retention-error 对应**？

## 链接

- arXiv：<https://arxiv.org/abs/2606.02346>（v1 2026-06-01）
- 项目页：not found in abstract
- GitHub：not found in PDF
- PDF：已下 `.pdfs/2606.02346.pdf`（11 页）
- 会议：not found in abstract（arXiv preprint）

## 年份 / 作者 / 机构（PDF 头部实测）

- **年份**：2026（v1 2026-06-01）
- **第一作者**：**Aoduo Li**
- **机构**（PDF 头部）：
  1. **Nanjing University of Science and Technology（南京理工大学）**——School of Computer Science and Engineering
  2. The Hong Kong Polytechnic University（PolyU）

## 方法核心（PDF §3 直引）

### §3.1 Variational Free-Energy Formulation

- 把 pruning 当作**贝叶斯变量选择问题**：每个 Gaussian 的 retention 概率 `r_i ∈ {0, 1}` 由 Bernoulli head 预测
- 目标：maximize **ELBO = log p(D) - KL[q(r) ‖ p(r)]**（evidence lower bound）
- 关键：KL 散度 prior 强制 sparsity（"sparsity-inducing KL prior"）

### §3.2 Asynchronous Prediction-Error Gating

- **不等所有 batch 收敛**：每个 Gaussian 的 retention 决策**独立 trigger**（"asynchronous, convergence-conditional"）
- 触发条件：prediction error 超过阈值
- **好处**：训练时间更短（不需要等所有 primitive 同步更新）

### §3.3 Closed-Form Correspondence

- 论文证明：**retention probability 与 prediction error 是 1-to-1 对应**（"closed-form retention-error correspondence proven"）
- **意义**：剪枝有数学保证，不会"剪错 Gaussian"

## 关键数字（PDF Table 1 直引 + abstract 直引）

| 方法 | #G (Mip-360) | Storage | FPS | PSNR (Mip-360) |
|---|---|---|---|---|
| 3DGS (vanilla) | 3.25M | 734 MB | 148 | 27.48 dB |
| LightGaussian | — | — | — | (heuristic, worse) |
| Compact3D | — | — | — | (VQ, worse) |
| Mini-Splatting | — | — | — | (densification, worse) |
| PUP 3D-GS | 0.68M | 153 MB | 192 | (sync batch) |
| MaskGaussian | — | — | — | (sync, fail some) |
| **VEDAL (Ours)** | **0.63M** | **141 MB** | **185** | **27.17 dB** |

> **abstract 直引**："**5.2× compression with only 0.31 dB PSNR drop; real-time rendering at 185 FPS**; consistent gains over pruning baselines on Mip-NeRF 360, Tanks&Temples, Deep Blending."
>
> **paired t-test p=0.03** 显著（PDF Table 1 footnote 直引）

## 与本调研主线的关系

### 派系归属：**派系 1（训练期压缩）**

- **派系 1 排名更新**：VEDAL 替代 LightGaussian 作为"variational 形式化"基线候选。**与 4DGS-1K（41.7× 压缩）派系 1 #1 不冲突**——4DGS-1K 是 4DGS 专用，VEDAL 是 3DGS 通用 framework
- **M3 spike 应用**：如果做 4DGS pruning 的 spike，**直接套 VEDAL 的 ELBO + KL prior 到 4DGS canonical Gaussians 上**是合理起点

### 对项目目标的具体承诺

- **无法直接承诺 4DGS 性能**：VEDAL 是 3DGS 静态，**4DGS + VEDAL variational 框架** 实验 = 本项目要做的工程实现
- **静态 3DGS 验证 VEDAL 性能 = 185 FPS @ 141 MB**（Mip-360），**与 Flux-GS 147 FPS @ 2.1 MB 对比**：VEDAL 压缩率（5.2×）< Flux-GS（~13× 相对 3DGS）但**有 closed-form 保证**

### 我未找到 / 提请下游注意

- **VEDAL 训练时间 vs 3DGS baseline**：abstract 未给，**Mip-360 训 0.63M Gaussians = ? h**（`[未在 abstract 拿到]`）
- **VEDAL 的 mobile on-device 实测**：abstract 仅以 "memory-constrained devices" 提 motivation，**未给 Snap 8 Gen 3 / Jetson Orin 等实测**
- **VEDAL 的开源代码**：PDF 未给 GitHub 链接，**本项目 fork 可行性 = 待定**

## 我的 commit 节奏

本文是 33 + 1 (Flux-GS) + 7 (subagent) 之外**新加的第 42 篇**。配套 INDEX.md 派系 E（3DGS 通用压缩）加 1 行。
