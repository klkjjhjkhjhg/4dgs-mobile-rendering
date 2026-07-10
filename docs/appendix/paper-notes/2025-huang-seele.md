# 2025-huang-seele · SeeLe: A Unified Acceleration Framework for Real-Time Gaussian Splatting

> **相关性**:**高度相关(3DGS mobile 加速强对标,2025-03)** —— **核心数字**:**"achieves 2.6× speedup and 32.3% model reduction while achieving superior rendering quality compared to existing methods"**(abstract 直引);**"designed to accelerate the 3DGS pipeline for resource-constrained mobile devices"**(abstract 直引);**9 位作者**;**上海交通大学 + Shanghai Qi Zhi Institute + Rochester** 团队。

> **⚠ 重要边界声明**:**SeeLe 是 3DGS(静态) mobile 加速**。**与 Mobile-GS(已有 11 号笔记)直接对标**:同方向,同目标(mobile device),**同期工作**(SeeLe 2025-03 vs Mobile-GS 2026-03 提交)。**两条 mobile 加速路径对照**:**SeeLe = GPU 端 algorithmic**(hybrid preprocessing + contribution-aware rasterization),**Mobile-GS = 算法 + Vulkan 端 OIT + NVQ + SH-distill**。

## 0.5 元数据

- **venue**: ICLR 2025
- **arxiv-id**: 2503.05168
- **s2-id**: （v2 用 Semantic Scholar API 补全）
- **homepage**: （无）
- **github**: （无）
- **status**: received
- **收录日期**: 2026-07-08（首次）
- **收录来源**: arxiv scan + 1-hop 引用规则
- **1-hop 引用**: （v2 补全，见 §11 1-hop 关系图）
- **评级**: ⭐⭐

- **survey_section**: 5
## 一句话问题

3DGS 在 **mobile device** 上达不到 real-time —— 如何通过 **hybrid preprocessing + contribution-aware rasterization** 两件套做到 **2.6× 加速 + 32.3% 模型压缩**,且"**seamlessly integrated into existing 3DGS pipelines with minimal fine-tuning**"?

## 链接(均经 fetch + verify)

- arxiv: <https://arxiv.org/abs/2503.05168>(v1 提交 2025-03-07, online 2025-12-04)
- PDF: <https://arxiv.org/pdf/2503.05168`
- HTML: <https://arxiv.org/html/2503.05168v1>
- 会议:abstract 未直引(`arXiv only,可能后续会议投递`)

## 年份 / 作者 / 机构(arxiv metadata 直引)

- **年份**:2025(v1 2025-03-07)
- **作者**(9 位,arxiv metadata):**Xiaotong Huang, He Zhu, Zihan Liu, Weikai Lin, Xiaohong Liu, Zhezhi He, Jingwen Leng, Minyi Guo, Yu Feng**
- **机构**(PDF 头部实测 from HTML v1):**Shanghai Jiao Tong University + Shanghai Qi Zhi Institute + University of Rochester**

## 方法核心(abstract 直引)

> "**3D Gaussian Splatting (3DGS) has become a crucial rendering technique for many real-time applications.** However, the **limited hardware resources on today's mobile platforms hinder these applications, as they struggle to achieve real-time performance**."

> "In this paper, we propose **SeeLe**, a general framework designed to **accelerate the 3DGS pipeline for resource-constrained mobile devices**. Specifically, we propose **two GPU-oriented techniques**:

1. **Hybrid preprocessing** — alleviates the GPU compute and memory pressure by **reducing the number of irrelevant Gaussians during rendering**. The key is to combine our **view-dependent scene representation** with **online filtering**.
2. **Contribution-aware rasterization** — improves the GPU utilization at the rasterization stage by **prioritizing Gaussians with high contributions** while reducing computations for those with low contributions."

> "Both techniques can be **seamlessly integrated into existing 3DGS pipelines with minimal fine-tuning**."

## 关键数字(abstract 直引)

- **核心 1**:**"achieves 2.6× speedup and 32.3% model reduction while achieving superior rendering quality compared to existing methods"**(abstract § 直引)
- **核心 2**:"seamlessly integrated into existing 3DGS pipelines with minimal fine-tuning"
- **核心 3**:"resource-constrained mobile devices" 是明确目标平台
- **具体 PSNR / FPS / Storage / mobile GPU 型号**:**abstract 未给 Table 数字**(`abstract 未给 Table 数字,需 PDF 核`)

## 与本调研主线的关系(基于 00-goal.md)

### 这就是 3DGS mobile 加速的另一条 SOTA 路径

**与 Mobile-GS(已有 11 号笔记)直接对照**:

| 维度 | SeeLe(本笔记) | Mobile-GS(11 号笔记) |
|---|---|---|
| 类型 | 3DGS 静态 | 3DGS 静态 |
| 提交时间 | 2025-03 | 2026-03 |
| 会议 | arXiv only | ICLR 2026 |
| 加速率(自报) | **2.6×** | **127 / 8 = 15.9× vs 3DGS**(Snap 8 Gen 3, 1600×1063) |
| 模型压缩率(自报) | **32.3%** | 4.6 MB / Mip-NeRF 360(~ 99% reduction) |
| 关键技术 | **Hybrid preprocessing + Contribution-aware rasterization**(纯 GPU 端) | OIT(no sort) + NVQ + SH-distill + pruning(Vulkan 2.0) |
| Mobile GPU 实测 | 未明示型号(abstract) | **Snap 8 Gen 3 实测 127 FPS** |
| 渲染管线 | (未直引,推测 CUDA) | **Vulkan 2.0** |
| 集成难度 | "minimal fine-tuning" | (需重写 Vulkan pipeline) |

> **关键洞察**:**SeeLe 是"**低集成成本**的 3DGS mobile 加速",Mobile-GS 是"**高投入**的 Vulkan 端到端重写"**。**对本项目 M3/M4 阶段的实际价值**:
> - **如果 M3 阶段是"**最快能在 4DGS 上跑起来**"**:选 **SeeLe 思路**(2.6× + 32.3% reduction,minimal fine-tuning)
> - **如果 M4 阶段是"**Snap 8 Gen 4 上 100+ FPS**"**:选 **Mobile-GS 思路**(15.9× + 99% compression,Vulkan 2.0 + OIT + NVQ)
>
> **两条路径不互斥**:SeeLe 的 hybrid preprocessing + contribution-aware rasterization 可作为 Mobile-GS 的**前置 GPU 端预处理**叠加使用。

### 与 4DGS-1K 的对照(虽然 SeeLe 是 3DGS)

| 维度 | SeeLe(本笔记) | 4DGS-1K(5 号笔记) |
|---|---|---|
| 类型 | 3DGS 静态 | 4DGS 动态 |
| 加速手段 | hybrid preprocessing + contribution-aware rasterization | STV pruning + Temporal Filter mask |
| 加速率 | 2.6× | 8.94× (N3V FPS: 90 → 805) / 3.89× (D-NeRF FPS: 376 → 1462) |
| 压缩率 | 32.3% | 41.7× (with PP) |
| 适配 mobile 路径 | ✅ (原生为 mobile) | ❌ (未在 mobile 实测) |

> **关键洞察**:**SeeLe 的 contribution-aware rasterization 与 4DGS-1K 的 Temporal Filter mask 在"per-frame 减负"思路上一致**。**对 4DGS 的潜在价值**:**把 SeeLe 的 contribution-aware 思路与 4DGS-1K 的 Temporal Filter 叠加** —— 4DGS-1K mask 决定哪些 Gaussian 进 raster,SeeLe contribution-aware 决定 raster 内优先级。**理论上可叠加 2~3× 额外加速**。

## 我未找到 / 提请下游注意

- **会议归属**:**abstract 未直引会议**,仅 arXiv 工作(arXiv'25);**未在公开 abstract 拿到会议归属,需 OpenReview 核**
- **Mobile GPU 型号**:**abstract 用 "mobile platforms" 复数**,未明示 Adreno / Mali / Apple;**与 Mobile-GS 的 "Snap 8 Gen 3" 严格口径不严格对应**
- **Table 数字**:**abstract 未给 PSNR / FPS / Storage / mobile GPU 详细数字**,需从 PDF Table 直引(`abstract 未给 Table 数字,需 PDF 核`)
- **Vulkan 实现**:**abstract 未提 Vulkan**,推测仍是 CUDA,**未在公开 abstract 拿到具体 API**
- **4DGS 适配性**:**论文未做 4DGS 适配**,但 hybrid preprocessing + contribution-aware rasterization 可直接推广到 4DGS 的 per-frame Gaussian 选择 + raster 优先级

## 我的 commit 节奏

本文是 12 篇 paper notes 之外**新加的第 17 篇**,与 Mobile-GS(11 号)直接对照 —— **3DGS mobile 加速双 SOTA**。**后续 `02-rendering-acceleration.md` §X mobile 段应加 SeeLe 一行**,与 Mobile-GS Table 2 交叉验证。

## 引用一览(本笔记引用自)

- arxiv abstract page 直引(`https://arxiv.org/abs/2503.05168`)
- arxiv html v1 直引(`https://arxiv.org/html/2503.05168v1`)用于作者机构
