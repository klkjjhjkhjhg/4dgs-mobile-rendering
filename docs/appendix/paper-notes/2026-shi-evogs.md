# 2026-shi-evogs · EvoGS: Constructing Continuous-Layered Gaussian Splatting with Evolution Tree for Scalable 3D Streaming

> **相关性**：**⭐⭐ 派系 1+4（流式落地 + 训练期压缩）** —— arXiv 2026-06-05；核心数字：**2.4× payload 缩减 + 5.5× VRAM 缩减 + 65%→25% splat redundancy 降低**（abstract 直引）。Mip-360 L1 EvoGS **302 MB stored / 200 MB VRAM vs LapisGS 561/561 MB**（PDF Table 1 直引）；**4 个 LOD level continuous smooth transition**（EvoGS 唯一）。对**派系 4（流式）**有方法学价值（continuous progressive 优于 discrete），**对派系 1（压缩）**有 8.7× post-compression 增益。**无 on-device mobile 实测**。

> **⚠ 重要区分**：这是 **3DGS（静态）** streaming 工作，**不是 4DGS**。**对 4DGS 适用性**：continuous-layered Evolution Tree 在概念上可直接扩展到 4DGS 的时间维度（加一层 time axis），但 abstract 未做实验。**本项目 M4/M5 路线中，4DGS streaming 的 progressive 传输可借鉴 Evolution Tree 的 parent-child 关系**。

## 一句话问题

现有 3DGS streaming 方法用 **discrete LOD layers**（每个 LOD 独立训练一个 splat set），**layer 之间 splat 冗余 65%+，且 layer transition 不平滑**。**如何在保持 layer-wise 渐进式传输的同时，让 layer 间有连续的质量过渡 + 大幅降低存储**？

## 链接

- arXiv：<https://arxiv.org/abs/2606.07179>（v1 2026-06-05）
- 项目页：not found in abstract
- GitHub：not found in PDF
- PDF：已下 `.pdfs/2606.07179.pdf`
- 会议：not found in abstract（arXiv preprint）

## 年份 / 作者 / 机构（PDF 头部实测）

- **年份**：2026（v1 2026-06-05）
- **第一作者**：**Yuang Shi**（施远 / 史远）
- **机构**（PDF 头部）：
  1. National University of Singapore（NUS）
  2. Singapore University of Technology and Design（SUTD）
  3. CNRS, IRIT, Université de Toulouse（法国图卢兹）
  4. CNRS @ Singapore（CFAR/Smart Systems Institute）

## 方法核心（PDF §3 直引）

### §3.1 Evolution Tree（核心数据结构）

- 用 **wavelet-inspired parent-child** 结构：**child splat 是 parent 的"修正量"**（不是独立的 splat）
- 渲染时：取最高 LOD 的 child 后累加所有 ancestor 的 base 即可
- 相比 discrete layer：**总 splat 数 = 4 个 LOD layer 的 child 之和 + 1 个 root**，**层间无冗余**

### §3.2 Continuous Quality Transition

- Discrete LOD：跳到 L1 时整个场景从 264 MB → 561 MB（重构整个 set），**PSNR 跳变**
- Evolution Tree：parent-child 是 smooth correction，**L0 → L1 时质量渐进提升**，**SSIM 0.89→0.91 连续**（abstract 直引）

### §3.3 Post-compression（PDF Table 1 后部）

- Evolution Tree 给出 base 320 MB（Mip-360 L1）
- 再跑 8.7× standard compression codec（V-PCC / G-PCC / Draco）→ **最终 36 MB**
- **vs LapisGS 561 MB → 64 MB**（同样 post-compression 后）

## 关键数字（PDF Table 1 直引 + abstract 直引）

| 场景 / LOD | 方法 | Storage (MB) | VRAM (MB) | 备注 |
|---|---|---|---|---|
| Mip-360 L0 | LapisGS | 264 | 264 | |
| Mip-360 L0 | **EvoGS** | 125 | — | Evolution Tree base |
| Mip-360 L1 | LapisGS | 561 | 561 | |
| Mip-360 L1 | **EvoGS** | **302** | **200** | 2.4× payload↓, 5.5× VRAM↓ |
| Mip-360 L2 | LapisGS | 643 | 643 | |
| Mip-360 L2 | **EvoGS** | 285 | — | |
| Mip-360 L3 | LapisGS | 822 | 822 | |
| Mip-360 L3 | **EvoGS** | 353 | — | |
| Blender L0 | LapisGS | 264 | 264 | |
| Blender L0 | **EvoGS** | 21.25 | 15.14 | **12× payload↓, 17× VRAM↓** |

> **abstract 直引**："EvoGS significantly reduces transmission payload up to **2.4×** and GPU VRAM footprint up to **5.5×**, while eliminating **splat redundancy from >65% to <25%**."

## 与本调研主线的关系

### 派系归属：**派系 4（流式）** 主，**派系 1（压缩）** 辅

- **派系 4 应用**：Evolution Tree 概念可直接扩展到 **4DGS time-axis**：root 是 time-agnostic 静态 splat，children 是 time-dependent motion correction。**M4/M5 工程实现价值高**——但需要重新设计 time 维度的 stratified sampling 策略。
- **派系 1 应用**：post-compression 8.7× 增益叠加在 4DGS-1K 41.7× 压缩上，**理论可叠加 360× 压缩**（`[推测]`）—— 但前提是 4DGS-1K 也能跑 Evolution Tree 类似的 progressive structure。

### 对项目目标的具体承诺

- **`4DGCPro` 路线对比**：4DGCPro (派系 4 #1) 用 hierarchical 4DGS + single bitstream progressive streaming；**EvoGS 的 Evolution Tree 提供了更精细的 layer 设计** —— 本项目可以"4DGCPro 的 hierarchical + EvoGS 的 continuous layering"组合
- **无法直接承诺**：M4 demo 的 1.7s 启动时间（PD-4DGS 数据）—— EvoGS 仍以 desktop 训练 + 4 个 LOD 切换为前提，**未在 mobile 实测**

### 我未找到 / 提请下游注意

- **Evolution Tree 的训练时间**：abstract 未给，**Mip-360 L1 训 320 MB 训练代价 = ? h**（`[未在 abstract 拿到]`）
- **4DGS time-axis 扩展可行性**：未在 abstract 提到；本项目 M3 spike 阶段如果尝试，需要自己设计 time-stratified sampling
- **mobile on-device 实测**：EvoGS 测试平台是 desktop GPU，**Snap 8 Gen 3 / Jetson Orin 等 mobile GPU 实测 = 0**
- **开源情况**：GitHub 链接未在 PDF 给出，**需要追踪**——可能影响本项目 fork 可行性

## 我的 commit 节奏

本文是 33 + 1 (Flux-GS) + 6 (subagent 写的 6 篇) 之外**新加的第 41 篇**。配套 INDEX.md 派系 D（流式）加 1 行。
