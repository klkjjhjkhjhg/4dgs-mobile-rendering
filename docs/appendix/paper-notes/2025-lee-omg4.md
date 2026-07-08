# 2025-lee-omg4 · OMG4: Optimized Minimal 4D Gaussian Splatting

> **相关性**:**⭐⭐ 中高相关(4DGS 多阶段压缩,2025-10)** —— **核心数字**:"reducing model sizes by **over 60%** while maintaining reconstruction quality"(abstract 直引);**3-stage progressive pipeline**:Gaussian Sampling → Gaussian Pruning → Gaussian Merging + implicit appearance compression + generalized Sub-Vector Quantization (SVQ)。

> **⚠ 重要边界声明**:**OMG4 是 4DGS(动态)工作**,abstract 直引 —— **本项目主线命中**。**关键创新是把 3DGS 的 sample / prune / merge 范式系统化搬到 4DGS**;**多作者跨 4 单位(Yonsei / SNU / POSTECH / Sungkyunkwan)**,韩国 4DGS 派系。

## 0.5 元数据

- **venue**: arxiv pre-print (2025-10)
- **arxiv-id**: 2510.03857
- **s2-id**: （v2 用 Semantic Scholar API 补全）
- **homepage**: （无）
- **github**: （无）
- **status**: under review
- **收录日期**: 2026-07-08（首次）
- **收录来源**: arxiv scan + 1-hop 引用规则
- **1-hop 引用**: （v2 补全，见 §11 1-hop 关系图）
- **评级**: ⭐⭐

## 一句话问题

4DGS 用数百万 Gaussian 拟合动态,存储开销巨大(单 Gaussian + 时间属性 = 巨大 footprint)。**能否用 3 阶段 progressive 压缩(Sample → Prune → Merge)+ 属性压缩 + SVQ,既降 60% 体积又保持质量**?

## 链接(均经 fetch + PDF 实测)
- arxiv: <https://arxiv.org/abs/2510.03857>(v1 提交 2025-10-04)
- 项目页 / GitHub: <https://minshirley.github.io/OMG4/>(abstract 直引)
- PDF: 已下 `.pdfs/2510.03857.pdf`(11.7 MB)

## 年份 / 作者 / 机构(PDF 头部实测)
- **年份**:2025
- **作者**(按 arxiv metadata 头部):Minseo Lee*, Byeonghyeon Lee*, Lucas Yunkyu Lee, Eunsoo Lee, Sangmin Kim, Seunghyeon Song, Joo Chan Lee, Jong Hwan Ko, Jaesik Park, Eunbyung Park†
- **机构**(PDF 头部直引):
  - **Yonsei University**(Minseo Lee, Byeonghyeon Lee, Eunbyung Park)
  - **Seoul National University**(Lucas Yunkyu Lee, Sangmin Kim, Jaesik Park)
  - **POSTECH**(Lucas Yunkyu Lee)
  - **Sungkyunkwan University**(Eunsoo Lee, Seunghyeon Song, Joo Chan Lee, Jong Hwan Ko)

## 方法核心(abstract + Fig. 1 + §1 直引)

### 3-Stage Progressive Compression Pipeline(abstract + Fig. 1 caption 直引)

> "OMG4(Optimized Minimal 4D Gaussian Splatting), a framework that constructs a compact set of salient Gaussians capable of faithfully representing 4D Gaussian models. Our method progressively prunes Gaussians in three stages:"

1. **Gaussian Sampling**:**identify primitives critical to reconstruction fidelity**
2. **Gaussian Pruning**:**remove redundancies**
3. **Gaussian Merging**:**fuse primitives with similar characteristics**

> Fig. 1 caption:"The overall OMG4 pipeline and performance comparison. OMG4 is a multi-stage 4DGS compression framework, progressively identifying important Gaussians (Gaussian Sampling), pruning unnecessary Gaussians (Gaussian Pruning), and merging similar Gaussians (Gaussian Merging), followed by attribute compression. The rate-distortion curve shows that OMG4 achieved significant improvements over recent state-of-the-art methods (**larger circles indicate higher FPS**)."

### 属性压缩(abstract + §3 直引)
- **Implicit appearance compression** —— 把 appearance 编码为隐式表示
- **Sub-Vector Quantization (SVQ)** —— "generalize Sub-Vector Quantization (SVQ) to 4D representations, further reducing storage while preserving quality"

### 4DGS 两种范式(§1 直引)
> "Modeling the dynamic scenes using Gaussian primitives has evolved in two directions."
> - **Deformation-based methods**:"employ a canonical set of 3D Gaussians and learns a deformation field that predicts per-primitive displacement and maps canonical primitives to each time step (Wu et al., 2024; Yang et al., 2023)."
> - **Spacetime-as-volume methods**:"treats the space-time as a single volume and optimizes a set of 4D Gaussian primitives, extending 3D Gaussians to the time axis for temporally varying appearance (Yang et al., 2024)."

### 关键问题(§1 直引)
> "current 4D Gaussian representations often carry a substantial computational cost and memory footprint. The number of primitives can grow to millions (e.g., **Real-Time4DGS (Yang et al., 2024) produces millions of 4D Gaussians, consuming over a gigabyte of memory**), with each primitive carrying high-dimensional attributes that evolve over time."

## 关键数字(abstract 直引 + Fig. 1 RD 曲线描述)
- **核心 1**:"reducing model sizes by **over 60%** while maintaining reconstruction quality"
- **核心 2**:"significantly outperforms recent state-of-the-art methods"
- **具体 Table 数字**:**abstract 未给 PSNR / FPS / bitrate 详细 Table 数字**(`abstract 未给 Table 数字,需 PDF 核`)

## 与本调研主线的关系(基于 00-goal.md)

### 4DGS 压缩派的方法学对照

| 维度 | OMG4(本笔记) | P-4DGS(本批 3 号) | 4DGS-1K(5 号) | 4DGS-CC(本批 5 号) |
|---|---|---|---|---|
| 4D 适配 | ✅ 4DGS | ✅ | ✅ | ✅ |
| 关键机制 | **3-stage: sample + prune + merge** | 视频编码借鉴: anchor + entropy | STV + mask | NVCC + VQCC |
| 压缩率 | **>60%** | 40-90× | 41.7×(PP) | **12×** |
| 属性压缩 | **implicit appearance + SVQ** | adaptive quant + context | VQ(PP) | **VQCC** |
| 项目页 | ✅ **有** | ❌ | ❌ | ❌ |
| 单位 | Yonsei + SNU + POSTECH + Sungkyunkwan | USTC | NUS | Beihang + Newcastle + Futurewei + HKU |

> **关键洞察**:**OMG4 与 4DGS-CC 思路最接近**(都是"剪枝 + VQ 派")—— 但 OMG4 把剪枝拆成 3 阶段(sample → prune → merge),更系统;**与 4DGS-1K 思路互补**(4DGS-1K 是 STV 评分 + mask 复用;OMG4 是 sample / prune / merge 渐进);**与 P-4DGS 思路对立**(P-4DGS 借鉴视频编码;OMG4 借鉴 3DGS 范式)。

### 对本项目"4DGS mobile rendering"的具体借鉴

1. **借鉴 1 · 3-stage sample-prune-merge 流水线**:**本项目 M2 训练 pipeline 可直接复用**:
   - **Sample** = 关键 Gaussian 识别(类似 4DGS-1K 的 STV 评分)
   - **Prune** = 冗余 Gaussian 移除(类似 4DGS-1K 的剪枝)
   - **Merge** = 相似 Gaussian 融合(OMG4 独有创新)—— **本项目 M2 可借鉴**
2. **借鉴 2 · Generalized SVQ to 4D**:**本项目 M3 量化阶段直接借鉴**(sub-vector quantization 是 Mobile-GS NVQ 的同类思路)
3. **借鉴 3 · Implicit appearance compression**:**本项目 M2 / M3 阶段可借鉴**(appearance 用 MLP 隐式编码)

### 对项目目标的具体承诺

- **Storage 减 60%**:**意味着本项目 M3 目标"≤ 50 MB / scene"可期**(`[推测,基于 abstract 数字 60% 减率]`)—— **若 4DGS vanilla 100 MB,OMG4 后 40 MB,达到本项目预算**
- **质量保持**:**"maintaining reconstruction quality"**(abstract § 直引)—— **本项目 M5 perceptual quality 目标不妥协**

## 我未找到 / 提请下游注意

- **会议归属**:**abstract 未直引会议**(`未在公开 abstract 拿到会议归属`)—— **arXiv only**
- **Mobile GPU 实测**:**abstract / intro 未提 mobile**(`未在公开 abstract 拿到 mobile GPU 型号`)—— **OMG4 不做 mobile GPU 端到端**
- **Vulkan 实现**:**abstract 未提 Vulkan**(`未在公开 abstract 拿到 mobile API`)
- **完整 Table 数字**:**abstract 未给 PSNR / FPS / bitrate 详细 Table**(`abstract 未给 Table 数字`)
- **每阶段压缩率细分**:**abstract 未直引** sample / prune / merge 各阶段贡献(`abstract 未给分阶段数字`)
- **SVQ 推广到 4D 的具体算法**:**abstract 未直引**(`abstract 未给 SVQ-4D 算法细节,需 PDF §3 核`)

## 我的 commit 节奏

本文是 12 篇 paper notes 之外**新加的第 20+ 篇**,**第 N 篇 4DGS 压缩类笔记**(本批 4 号)。**后续 `02-rendering-acceleration.md` §3 应加 OMG4 一行**;**`03-end-to-end-roadmap.md` 应专门为 OMG4 加一节"§Y. 4DGS 3-stage 压缩路径(OMG4 sample / prune / merge)"**,作为"4DGS 借鉴 3DGS 渐进压缩范式"的最直接学术先例。

## 引用一览(本笔记引用自)
- arxiv abstract page 直引(`https://arxiv.org/abs/2510.03857`)
- 项目页 `https://minshirley.github.io/OMG4/` (abstract 直引)
- PDF Fig. 1 caption 直引(`.pdfs/2510.03857.pdf`)
- PDF §1 intro 直引(4DGS 两种范式段 + 关键问题段)
- PDF 头部 author / 4 单位 affiliation 直引

[abstract 直引] [PDF 直引] [推测] [调研深度:abstract + Fig.1 + §1,Table 数字未及]
