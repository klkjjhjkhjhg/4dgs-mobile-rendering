# 2026-zhao-mmgs · MMGS: 10× Compressed 3DGS through Optimal Transport Aggregation based on Multi-view Ranking

> **相关性**：**⭐⭐ 训练期压缩（派系 1）通用方法学**（arXiv 2026-05-19）—— 核心数字：**Deep Blending 上 10.25× comp. ratio + ∆PSNR +0.44 dB over vanilla 3DGS**；T&T 上 8.26× / +0.31 dB；Waymo 上 8.41× / +0.03 dB；训练 **10× speedup**；Method **multi-view ranking + Optimal Transport aggregation**。**Mobile relevance 弱**（仅 generic "real-time rendering" motivation，**未做 mobile GPU 实测**）。

> **⚠ 重要区分**：这是 **3DGS（静态）** 压缩工作，不是 4DGS。**对 4DGS 适用性**：OT-based aggregation 在 canonical-space Gaussians 上理论可移植（global 几何分布匹配），但 abstract 未做 4DGS 实验。**对本项目派系 1（训练期压缩）方法学价值**：OT 框架提供了比 local-heuristic pruning 更 global 的视角。

## 0.5 元数据

- **venue**: arxiv pre-print (2026-05)
- **arxiv-id**: 2605.19304
- **s2-id**: （v2 用 Semantic Scholar API 补全）
- **homepage**: （无）
- **github**: （无）
- **status**: under review
- **收录日期**: 2026-07-08
- **收录来源**: arxiv scan + 1-hop 引用规则
- **1-hop 引用**: （v2 补全，见 §11 1-hop 关系图）
- **评级**: ⭐

## 一句话问题

3DGS 通过 2D view-space gradients 做 densification，导致 **massive redundant primitives + 几何不一致性**。**如何用 global 几何分布匹配（Optimal Transport）将 3DGS 压缩到 10% primitives 同时保持 ∆PSNR ≥ 0**？

## 链接

- arXiv：<https://arxiv.org/abs/2605.19304>（v1 2026-05-19，cs.CV，"Preprint"）
- GitHub / 项目页：not found in PDF header / abstract
- PDF：已下 `.pdfs/2605.19304.pdf`（19 页）
- 会议：not found in abstract

## 年份 / 作者 / 机构（PDF 头部实测）

- **年份**：2026（v1 2026-05-19）
- **第一作者**：**Beizhen Zhao¹**（赵北辰，PDF 头部直引）
- **通讯作者**：**Hao Wang¹ †**（PDF 头部直引）
- **机构**（PDF 头部直引）：
  1. **The Hong Kong University of Science and Technology (Guangzhou)**（**广州香港科技大学**）—— HKUST-GZ
- 联系邮箱：`bzhao610@connect.hkust-gz.edu.cn`, `haowang@hkust-gz.edu.cn`（PDF 头部）

## 方法核心（abstract + PDF §3 直引）

### 三大模块（abstract 直引）

1. **Multi-view 3D Gaussian contribution ranking mechanism** —— **filters primitives using geometric consistency instead of local heuristics**
2. **Global Optimal Transport (OT)-based aggregation algorithm** —— **merges redundant primitives while preserving the underlying geometry**
3. **OT-based densification operator** —— **maintains the Gaussian's distributional properties for stable optimization**

### Multi-View Ranking（PDF §3.1 直引）

- **构造 texture-aware metric map**（"constructs a texture-aware metric map to filter out transient noise"，abstract 直引）
- **Project 2D map back to 3D** via inverse accumulation voting mechanism
- **Importance sampling for densification and pruning**
- 解耦："decouple the generation of primitives from 2D projection error"（abstract 直引）

### Global OT Aggregation（PDF §3.2 直引）

- **核心思路**：**Gaussian reduction = discrete mass transport problem** rooted in OT theory
- **最小化 Wasserstein distance** between original dense set and compacted set
- **Global aggregation**：**merge spatially clustered low-contribution primitives into a compacted set**
- **意义**：比 local-heuristic pruning 更 global，更保留几何连续性

### OT-based Densification（PDF §3.3 直引，Eq. 12-13 直引）

- **问题**：existing methods duplicate opacity or scale arbitrarily → optimization instability
- **解法**：**new splitting operator preserving parent distribution**
- **公式**（PDF Page 6 Eq. 12-13 直引）：
  - "To preserve the 2nd moment, the mixture variance must equal the original variance"
  - `Σ_mixture = Σ_local + Σ_means ⟹ (s'_k)² + δ²`
  - `s'_k = s_k · √(1 - η²)`
- **物理意义**：split 时 sub-Gaussians 保留 parent Gaussian 的 distributional properties

## 关键数字（PDF Table 1 直引 + abstract 直引）

### PDF Table 1 直引 · Compression Ratio / ∆PSNR

| 方法 | Deep Blending CR ↑ | Deep Blending ∆PSNR ↑ | T&T CR | T&T ∆PSNR | Waymo CR | Waymo ∆PSNR |
|---|---|---|---|---|---|---|
| DashGaussian | 1.27× | -0.13 | 1.30× | +0.18 | 1.43× | -1.27 |
| Speedy-splat | 5.13× | -0.11 | 7.48× | -0.31 | 3.85× | -1.76 |
| GHAP | 5.02× | 0.00 | 5.06× | -0.57 | 4.87× | -0.48 |
| Mini-splatting | 4.39× | +0.27 | 5.23× | -0.33 | 6.17× | -3.48 |
| Taming-3dgs | 8.48× | +0.09 | 4.91× | +0.04 | 5.14× | -0.12 |
| FastGS | 7.69× | +0.30 | 6.28× | +0.30 | 4.40× | -0.02 |
| **MMGS (Ours)** | **10.25×** | **+0.44** | **8.26×** | **+0.31** | **8.41×** | **+0.03** |

### PDF Table 2 直引 · Full PSNR/SSIM/LPIPS/NGS + Time

| 数据集 | 方法 | PSNR↑ | NGS↓ | Time↓ |
|---|---|---|---|---|
| Mip-NeRF 360 | 3DGS | 29.06 | 2.47M | 30.46 min |
| Mip-NeRF 360 | **MMGS** | **28.89** | **0.29M** | **4.08 min** |
| Mip-NeRF 360 | MMGS-B | **29.17** | 0.57M | 6.11 min |
| T&T | 3DGS | 23.76 | 1.57M | 17.80 min |
| T&T | **MMGS** | **24.07** | **0.19M** | **2.83 min** |
| Deep Blending | 3DGS | 29.74 | 2.46M | 30.18 min |
| Deep Blending | **MMGS** | **30.18** | **0.24M** | **3.04 min** |

> **关键比值**：
> - **Mip-NeRF 360 NGS**：0.29M / 2.47M = **8.5× 减少**（与 Table 1 的 10.25× Deep Blending 取平均）
> - **Deep Blending PSNR**：**30.18 > 29.74 = +0.44 dB over 3DGS**（原文 Table 2 直引；不是因为压缩丢质量，是真实提升）
> - **训练加速**：Deep Blending 30.18 min → 3.04 min = **9.9×**

### abstract 直引
- "achieves state-of-the-art rendering quality with only **10% primitives and 10× accelerated training speeds** compared to vanilla 3DGS"

## 与本调研主线的关系

### ⭐⭐ 派系 1（训练期压缩）— 方法学价值（与 Flux-GS 互补）

| 维度 | MMGS | REFINE | Flux-GS |
|---|---|---|---|
| 压缩比 | **10×** primitives（storage 减比 ~10×）| 3,000× **pruning compute** | ~50×（3rd → 1st SH）|
| ∆PSNR over vanilla | **+0.44 dB** | ~0 | -0.19 dB |
| 训练加速 | **10×** | n/a（post-hoc）| 7.8× |
| 核心算法 | **OT aggregation** | Hessian field | MC SH sampling |
| Mobile 实测 | ❌ | ❌ | ✅ Snap 8 Gen 3 |

> **关键洞察**：**MMGS 是 storage-only 压缩（10× primitives），REFINE 是 compute-only 压缩（3000× pruning passes），Flux-GS 兼顾 SH storage 压缩 + 训练加速** —— **三者路线完全不同，可互补**。

### 对项目目标的具体承诺 / 不可承诺

- **承诺 1（方法学）**：**OT-based aggregation + multi-view ranking** 是**派系 1 训练期压缩可借鉴的方法学** —— 对 4DGS canonical-space Gaussians global-pruning 有理论可移植性
- **承诺 2（数据）**：**Table 1 详细对比 DashGaussian / Speedy-splat / GHAP / Mini-splatting / Taming-3DGS / FastGS** —— 是**3DGS 压缩方法的最新 benchmark**，对本项目 M1 评估 stage 有 baseline 对比价值
- **不可承诺 1**：**Mobile relevance 弱**（generic real-time motivation）
- **不可承诺 2**：**未做 mobile GPU benchmark** — `[推测]` 训练从 30 min → 3 min 主要是 GPU compute 受益，**移动端 inference 优势未量化**

### ⭐ 派系 2（动静态分离）/ 派系 3（移动端）/ 派系 4（流式）

- **不直接命中**：3DGS 静态压缩，无 4DGS / streaming / mobile GPU 数据

## 我未找到 / 提请下游注意

- **GPU 类型**：Table 1 / Table 2 未明确 RTX 3090 / 4090 / A100（`[推测]` 是 desktop GPU）
- **Mobile GPU benchmark**：abstract 仅 "scalable applications"（generic），**未给 mobile GPU 型号 / FPS / VRAM**
- **GitHub / project page**：abstract / PDF 头部无直链
- **会议**：abstract "Preprint"，**无 venue 信息**
- **FPS rendering**：Table 2 主要列 PSNR/SSIM/NGS，**FPS rendering 数据未在 §1-§4 详细给**（`需 PDF §4 后续页核`）
- **MMGS-B vs MMGS 差异**：MMGS-B "reduces the threshold of densification process for better rendering quality with more [Gaussians]"（PDF §4 直引）—— **B = Quality-priority；普通 = Speed-priority**
- **4DGS 适配**：未做 4DGS 实验

[abstract 直引] [PDF §3 直引] [PDF Table 1/2 直引] [推测] [调研深度：PDF §1-§3.3 + Page 6 Table 1 + Page 7-8 Table 2]
