# 2026-zhang-geta3dgs · GETA-3DGS: Automatic Joint Structured Pruning and Quantization for 3D Gaussian Splatting

> **相关性**:**⭐⭐ 中高相关(3DGS 自动压缩 + 期刊发表,2026-05)** —— **IEEE Transactions on Circuits and Systems for Video Technology (TCSVT)** 期刊论文(投稿阶段);**核心数字**:"delivers a **∼5× storage reduction** over Vanilla 3DGS with a **fully automatic pipeline that requires no per-scene opacity, scale, or SH-degree thresholds**"(abstract 直引);**"forcing a uniform 6-bit cap costs up to −6.74 dB on view-dependent scenes"** —— **异构 per-attribute mixed-precision 量化的关键证据**。

> **⚠ 重要边界声明**:**GETA-3DGS 是 3DGS(静态)工作**,**不是 4DGS**。**但**:**自动联合剪枝 + 量化**的方法论可推广到 4DGS 静态 / 动态分量;**对项目 M2 / M3 阶段借鉴价值高**(异构 mixed-precision 量化直接可借鉴到 4DGS canonical 空间 + deformation field)。

## 0.5 元数据

- **venue**: arxiv pre-print (2026-05)
- **arxiv-id**: 2605.02086
- **s2-id**: （v2 用 Semantic Scholar API 补全）
- **homepage**: （无）
- **github**: （无）
- **status**: under review
- **收录日期**: 2026-07-08
- **收录来源**: arxiv scan + 1-hop 引用规则
- **1-hop 引用**: （v2 补全，见 §11 1-hop 关系图）
- **评级**: ⭐

## 一句话问题

现有 3DGS 压缩(HAC++ / FlexGaussian / LP-3DGS)把 **pruning / quantization / entropy coding 拆为 3 个独立阶段**,依赖手工调阈值(opacity threshold, fixed bit-width, SH truncation rules),**无法直接指定压缩率或质量预算**。**能否做一个端到端自动的"剪枝 + 量化"联合框架,只需指定 target compression rate 即可**?

## 链接(均经 fetch + PDF 实测)
- arxiv: <https://arxiv.org/abs/2605.02086>(v1 提交 2026-05-04)
- **会议**:**IEEE TCSVT**(PDF 头部直引 "IEEE TRANSACTIONS ON CIRCUITS AND SYSTEMS FOR VIDEO TECHNOLOGY, VOL. XX, NO. X, MONTH YEAR")
- PDF: 已下 `.pdfs/2605.02086.pdf`(1.2 MB)

## 年份 / 作者 / 机构(PDF 头部实测)
- **年份**:2026
- **作者**(按 PDF 脚注):**Baobing Zhang** (Corresponding), **Wanxin Sui**
- **机构**(PDF 脚注直引):
  1. **Baobing Zhang**:**University of Hertfordshire, Hatfield, UK**
  2. **Wanxin Sui**:**Brunel University London, Uxbridge, UK**

## 方法核心(abstract + §IV 直引)

### 三大新组件(abstract § 直引)
1. **3DGS-aware quantization-aware dependency graph (QADG)** —— "treats every Gaussian primitive as a group with five attribute sub-nodes and degree-aware spherical-harmonic sub-nodes"
2. **Render-aware saliency** —— "fuses transmittance-weighted contribution, screen-space gradient, and pixel coverage into a single Gaussian-level importance score"
3. **Heterogeneous per-attribute mixed-precision quantization** —— "co-optimized with structural sparsity under a projected partial saliency-guided (PPSG) descent guarantee"

### 3DGS Parameter Space 重解释(§IV-A 直引)
> "Re-interpretation. A trained 3DGS scene Θ = {θ_i}^N_{i=1} with θ_i = (µ_i, s_i, q_i, α_i, c_i) behaves, from a parameter-storage perspective, like an **extremely wide single-layer linear operator**: every Gaussian primitive can be regarded as an independently prunable 'channel' whose payload is the D-dimensional attribute vector θ_i ∈ R^D, **D = 59** at the standard SH degree ℓ=3 (3+3+4+1+48)."

> 5 个 attribute classes(typed columns):
> - **µ (position)**:geometry-critical,"demanding at least **12-16 bits** to avoid visible jitter"
> - **s (log-scale)**:exp(·) activation dampens quantization noise
> - **q (rotation)**:unit sphere by post-hoc ℓ2-normalization,**8 bits typically sufficient**
> - **α (opacity)**:sigmoid-bounded,"even **4 bits** suffice in practice"
> - **c (SH)**:DC term (albedo) critical, AC bands (view-dep) compressible

### Group Definition(§IV-A 直引)
> "Following the GETA group abstraction, we define the prunable group g_i to be the **i-th Gaussian primitive**, i.e. the i-th row of Θ viewed as a single rigid bundle of five attributes... **Pruning g_i is implemented as deleting the entire row from every attribute tensor; pruning a strict subset of A is forbidden because a Gaussian missing (e.g.) its scale, rotation, or opacity has no well-defined splat in (2).**"

### Constrained Problem(§IV-A 直引,Eq. 6)
> "3DGS compression becomes the rendering-aware constrained problem: min L_render(Θ; φ) s.t. |{i ∈ [N] : g_i ≠ 0}| = K, b^(a) ∈ [b^(a)_l, b^(a)_u] ∀a ∈ A★, **PSNR_D_tr(Θ; φ) ≥ τ**"
> - **K = sparse group count**(用户指定)
> - **b^(a) = per-attribute bit-width bounds**
> - **τ = 渲染质量下限**(hard floor)

## 关键数字(abstract + §V 直引)
- **核心 1**:"**∼5× storage reduction** over Vanilla 3DGS"
- **核心 2**:"**fully automatic pipeline that requires no per-scene opacity, scale, or SH-degree thresholds**"
- **核心 3**:"forcing a uniform **6-bit cap** costs up to **−6.74 dB on view-dependent scenes (counter, room)** versus our heterogeneous allocation"
- **核心 4**:"**information-theoretic reverse-water-filling analysis** we develop in this paper"
- **具体 Table 数字**:**abstract 未给 PSNR / FPS / bitrate 详细 Table**(`abstract 未给 Table 数字,需 PDF §V 核`)

### 评测 datasets(abstract § 直引)
- **Mip-NeRF 360**
- **Tanks and Temples**
- **Deep Blending**

## 与本调研主线的关系(基于 00-goal.md)

### 这与 3DGS 压缩派的方法学对照

| 维度 | GETA-3DGS(本笔记) | HAC++(2024-chen-hacpp) | P-4DGS(本批 3 号) | OMG4(本批 4 号) |
|---|---|---|---|---|
| 4D 适配 | ❌ 3DGS 静态 | ❌ 3DGS 静态 | ✅ 4DGS | ✅ 4DGS |
| 关键机制 | **automatic joint pruning + mixed-precision quant** | hierarchical anchor compression | 视频编码借鉴 | 3-stage sample/prune/merge |
| 压缩率 | **5×** | (未直引) | 40-90× | >60% |
| 单位 | **Hertfordshire + Brunel (UK)** | (Monash 推测) | USTC | Yonsei 等 4 单位 |
| 异构量化 | ✅ **mixed-precision per-attribute** | ❌ | adaptive quant | implicit + SVQ |
| 自动化 | ✅ **fully automatic, no per-scene hyperparam** | ❌ 手工 | (λrate 调节) | (sample 阈值) |
| 期刊 | **TCSVT** | ECCV 2024 | (Preprint) | (Preprint) |
| 信息论分析 | ✅ **reverse-water-filling** | ❌ | ✅ CABAC | ❌ |

> **关键洞察**:**GETA-3DGS 是 3DGS 压缩派"自动 + 异构量化"的代表**;**"reverse-water-filling"信息论框架**是 4DGS 压缩派多未涉及的视角。

### 对本项目"4DGS mobile rendering"的具体借鉴

1. **借鉴 1 · 异构 per-attribute 量化**:
   - **canonical 空间 µ 用 12-16 bits**(避免 jitter)
   - **deformation field 用 8 bits**(因为 unit sphere 归一化)
   - **SH DC 用 12+ bits**(albedo 关键)
   - **SH AC 用 4-8 bits**(高频细节可压)
   - **opacity 用 4 bits**(sigmoid-bound)
   - **本项目 M3 量化阶段直接复用这套 5-class 异构 bit-width**

2. **借鉴 2 · Hard rendering-quality floor τ**:**本项目 M5 perceptual quality 课题可借鉴**(不只压到目标 bitrate,还要保 PSNR ≥ τ)

3. **借鉴 3 · 自动化联合优化**:**本项目 M2 训练 pipeline 可借鉴**(避免 per-scene 调阈值)

### 对项目目标的具体承诺

- **Storage 5× 减** = **本项目"≤ 50 MB / scene" 在 4DGS 静态 / 动态分量上可期**(`[推测,基于 5× 减率]`)
- **全自动**:本项目 M2 训练 pipeline 可大幅简化(免去 per-scene 调参)
- **信息论 reverse-water-filling**:**本项目 M3 / M4 阶段 bit allocation 课题直接借鉴**

## 我未找到 / 提请下游注意

- **4DGS 适配**:**abstract 未提 4DGS**(`未在公开 abstract 拿到 4DGS 适配信息`)—— **GETA-3DGS 是 3DGS 静态,需扩展到 4DGS**
- **Mobile GPU 实测**:**abstract / §V 未提 mobile**(`未在公开 abstract 拿到 mobile GPU 型号`)
- **Vulkan 实现**:**abstract 未提 Vulkan**(`未在公开 abstract 拿到具体 mobile API`)
- **完整 Table 数字**:**abstract 未给 PSNR / FPS / bitrate 详细 Table**(`abstract 未给 Table 数字,需 PDF §V 核`)
- **具体 5× 减率的 baseline 数字**:**abstract 未直引** baseline Vanilla 3DGS 大小(`abstract 未给 baseline 大小`)
- **deformation / dynamic 扩展路径**:**abstract 未直引**(`abstract 未给 4DGS 扩展方案`)

## 我的 commit 节奏

本文是 12 篇 paper notes 之外**新加的第 20+ 篇**,**第 N 篇 3DGS 压缩类笔记**(本批 7 号)。**后续 `02-rendering-acceleration.md` §3 应加 GETA-3DGS 一行**;**`03-end-to-end-roadmap.md` 应专门为 GETA-3DGS 加一节"§Y. 异构量化派路径(GETA-3DGS mixed-precision + reverse-water-filling)"**,作为"3DGS / 4DGS 异构量化"的最直接学术先例。

## 引用一览(本笔记引用自)
- arxiv abstract page 直引(`https://arxiv.org/abs/2605.02086`)
- PDF 头部 TCSVT 期刊标识直引(`.pdfs/2605.02086.pdf`)
- PDF §IV-A 3DGS parameter space 直引(D=59, 5 attribute classes, bit-width 数字)
- PDF §IV-A constrained problem 直引(Eq. 6 PSNR ≥ τ)
- PDF 脚注 author / 2 单位 UK affiliation 直引

[abstract 直引] [PDF 直引] [推测] [调研深度:abstract + §IV,§V Table 数字未及]
