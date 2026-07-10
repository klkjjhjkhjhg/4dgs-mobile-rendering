# 2025-chen-4dgscc · 4DGS-CC: A Contextual Coding Framework for 4D Gaussian Splatting Data Compression

> **相关性**:**⭐⭐ 中高相关(4DGS 数据压缩 + 神经上下文编码,2025-04)** —— **核心数字**:"achieves an average storage reduction of approximately **12×** while maintaining rendering fidelity compared to our baseline 4DGS approach"(abstract 直引);**"first work to apply neural contextual coding techniques to the compression of Gaussian Splatting based dynamic scene representations"** —— **首次把神经上下文编码(NCC)用于 4DGS**。

> **⚠ 重要边界声明**:**4DGS-CC 是 4DGS(动态)工作**,**本项目主线命中**。**核心创新是 NVCC(Neural Voxel Contextual Coding) + VQCC(Vector Quantization Contextual Coding)双模块**,把信息论上下文模型借鉴到 4DGS 压缩。

## 0.5 元数据

- **venue**: CVPR 2025
- **arxiv-id**: 2504.18925
- **s2-id**: （v2 用 Semantic Scholar API 补全）
- **homepage**: （无）
- **github**: （无）
- **status**: received
- **收录日期**: 2026-07-08（首次）
- **收录来源**: arxiv scan + 1-hop 引用规则
- **1-hop 引用**: （v2 补全，见 §11 1-hop 关系图）
- **评级**: ⭐⭐

- **survey_section**: 4
## 一句话问题

4DGS 重建动态场景存储开销大(动态 deformation 4D neural voxels + canonical 3DGS)。**能否借鉴神经上下文编码(NCC,已在 NeRF / 3DGS 静态场景验证)到 4DGS 动态场景,实现 12× 压缩同时保持 SOTA 渲染质量**?

## 链接(均经 fetch + PDF 实测)
- arxiv: <https://arxiv.org/abs/2504.18925>(v1 提交 2025-04-26)
- PDF: 已下 `.pdfs/2504.18925.pdf`(1.4 MB)

## 年份 / 作者 / 机构(PDF 头部实测)
- **年份**:2025
- **作者**(按 arxiv metadata 头部):Zicong Chen¹, Zhenghao Chen², Wei Jiang³, Wei Wang³, Lei Liu⁴, Dong Xu⁴
- **机构**(PDF 头部直引):
  1. **Beihang University (北京航空航天大学)**
  2. **The University of Newcastle, Australia**
  3. **Futurewei Technologies Inc (华为子公司)**
  4. **The University of Hong Kong (HKU)**

## 方法核心(abstract + §3 直引)

### 4DGS 分解(§3.2 直引)
> "We first decompose the dynamic scene into two primary components: **Canonical Gaussians** and a **Gaussians deformation field (i.e., 4D neural voxels)**, each of which will be compressed separately."

### 双压缩模块(abstract 直引)
1. **NVCC (Neural Voxel Contextual Coding)** —— 用于 4D neural voxels 压缩:
   - "Decompose 4D neural voxels into distinct quantized features by separating the temporal and spatial dimensions"
   - "Leverage the previously compressed features from the temporal and spatial dimensions as priors and apply NVCC to generate the spatiotemporal context"
2. **VQCC (Vector Quantization Contextual Coding)** —— 用于 canonical 3DGS 压缩:
   - "Employ a codebook to store spherical harmonics information from canonical 3DGS as quantized vectors"
   - "Losslessly compressed by using VQCC with the auxiliary learned hyperpriors for contextual coding"

### 4DGS-CC 整体框架(abstract 直引)
> "By integrating NVCC and VQCC, our contextual coding framework, 4DGS-CC, enables **multi-rate 4DGS data compression tailored to specific storage requirements**."

### Hybrid Lossy-Lossless 方案(§3.2 直引)
- **X(位置)**:16 bits 量化,lossless 存
- **s, r, α(scaling, rotation, opacity)**:8 bits 量化,lossless 存
- **C(spherical harmonics)**:**VQ → indices + codebook**;**indices run-length coding 压缩**;**codebook Y 用 VQCC 压缩(learned hyper-prior)**
- **4D Neural Voxels**:**Hexplane 量化 + NVCC(lossless)**

### 信息论基础(§3.1 直引)
> "the cross entropy H(q, p) = E_Ā~q [-log(p(Ā))] serves as a practical lower bound on the storage cost for losslessly compressing Ā. Here, p(Ā) denotes the estimated probability distribution of Ā, while q(Ā), represents its true distribution. By refining p(Ā) to more closely approximate q(Ā), we can reduce H(q, p), and consequently lower the storage cost."

## 关键数字(abstract + §4 直引)
- **核心**:"achieves an average storage reduction of approximately **12×** while maintaining rendering fidelity"
- **三大 benchmark**:"Extensive experiments on three 4DGS data compression benchmarks"
- **具体 Table 数字**:**abstract 未给 PSNR / FPS / bitrate 详细 Table**(`abstract 未给 Table 数字,需 PDF §4 核`)

## 与本调研主线的关系(基于 00-goal.md)

### 4DGS 压缩派方法学对照

| 维度 | 4DGS-CC(本笔记) | P-4DGS(本批 3 号) | OMG4(本批 4 号) | 4DGS-1K(5 号) |
|---|---|---|---|---|
| 4D 适配 | ✅ 4DGS | ✅ | ✅ | ✅ |
| 关键机制 | **NVCC + VQCC(神经上下文编码)** | 视频编码借鉴: anchor + entropy | sample / prune / merge + SVQ | STV + mask |
| 压缩率 | **12×** | 40-90× | >60% | 41.7×(PP) |
| 单位 | **Beihang + Newcastle + Huawei + HKU** | USTC | Yonsei 等 4 单位 | NUS |
| 上下文编码 | ✅ **NCC 范式(信息论)** | ✅ CABAC 类 | ❌ | ❌ |
| 多速率 | ✅ **multi-rate tailored** | (λrate 调节) | ❌ | (PP only) |

> **关键洞察**:**4DGS-CC 是 4DGS 压缩派"信息论派"的代表** —— **NCC(神经上下文编码)是从 NeRF / 3DGS 静态场景迁移到 4DGS 动态场景的首次系统化尝试**;**与 P-4DGS 的"视频编码借鉴"和 OMG4 的"3DGS 渐进范式"形成三大方法论对比**。

### 对本项目"4DGS mobile rendering"的具体借鉴

1. **借鉴 1 · VQCC**:**本项目 M3 量化阶段直接借鉴**(VQ + 上下文编码)
2. **借鉴 2 · NVCC**:**本项目 M3 bitstream 压缩借鉴**(空间 + 时间 priors)
3. **借鉴 3 · Multi-rate tailored compression**:**本项目 M3 / M4 阶段"60 FPS @ 1080p on Snap 8 Gen 4"对应不同码率,可借鉴多速率**

### 对项目目标的具体承诺

- **Storage 12× 减** = **本项目"≤ 50 MB / scene" 可期**(`[推测,基于 12× 减率]`)—— **若 4DGS baseline 100 MB,4DGS-CC 后 ≈ 8 MB,远低于预算**
- **多速率**:**本项目 M4 阶段不同 GPU 算力 + 不同网络条件可借鉴**
- **4 作者 4 单位跨国合作**:**Beihang + Newcastle + Huawei + HKU** —— **方法学可信度较高**

## 我未找到 / 提请下游注意

- **项目页 / GitHub**:**abstract 未直引**(`未在公开 abstract 拿到项目页 URL`)
- **会议归属**:**abstract 未直引会议**(`未在公开 abstract 拿到会议归属`)
- **Mobile GPU 实测**:**abstract / intro 未提 mobile**(`未在公开 abstract 拿到 mobile GPU 型号`)
- **Vulkan 实现**:**abstract 未提 Vulkan**(`未在公开 abstract 拿到 mobile API`)
- **完整 Table 数字**:**abstract 未给 PSNR / FPS / bitrate 详细 Table**(`abstract 未给 Table 数字,需 PDF §4 核`)
- **与其他压缩方法的具体对比**:**abstract 级别不易判定**(只说"3 benchmarks 全面 SOTA")
- **SaRO-GS 验证**:"we also build upon the latest method SaRO-GS [52]" —— **§3.2 直引**

## 我的 commit 节奏

本文是 12 篇 paper notes 之外**新加的第 20+ 篇**,**第 N 篇 4DGS 压缩类笔记**(本批 5 号)。**后续 `02-rendering-acceleration.md` §3 应加 4DGS-CC 一行**;**`03-end-to-end-roadmap.md` 应专门为 4DGS-CC 加一节"§Y. 4DGS 信息论派压缩路径(4DGS-CC NVCC + VQCC)"**,作为"4DGS 借鉴神经上下文编码"的最直接学术先例。

## 引用一览(本笔记引用自)
- arxiv abstract page 直引(`https://arxiv.org/abs/2504.18925`)
- PDF 头部 author / 4 单位 affiliation 直引(`.pdfs/2504.18925.pdf`)
- PDF §3.1 / §3.2 直引(decomposition + lossy/lossless + NCC 信息论)
- PDF Fig. 2 / Fig. 3 caption 直引(VQCC / NVCC 框架)

[abstract 直引] [PDF 直引] [推测] [调研深度:abstract + §3,§4 Table 数字未及]
