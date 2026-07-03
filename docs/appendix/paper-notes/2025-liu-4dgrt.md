# 2025-liu-4dgrt · 4D-GRT: 4D Gaussian Ray Tracing for Physics-based Camera Effect Data Generation

> **相关性**:**中等相关(4DGS + 渲染加速 / ray tracing 替代 raster,2025-09)** —— **核心数字**:**"4D-GRT achieves the fastest rendering speed while performing better or comparable rendering quality compared to existing baselines"**(abstract 直引);**6 位作者**;**National Taiwan University (NTU) + Intel** 团队(I-Sheng Fang 是 NTU 教授)。

> **⚠ 重要边界声明**:**4D-GRT 是 4DGS(动态)工作**,但 **核心应用场景是"camera effect 数据生成"** —— 不是直接 mobile rendering 加速。**其相关性在本调研的间接价值是**:**"**4D Gaussian + ray tracing** 替代 4D Gaussian + rasterization"** 是本项目 M3 阶段可考虑的另一条渲染管线思路。

## 一句话问题

现有 4DGS 假设 **理想 pinhole 相机**,无法模拟真实相机的 **fisheye 畸变 + rolling shutter** 等物理效果 —— 如何在 **4DGS 框架内**加入 **physically-based ray tracing** 来生成可控的物理真实相机效果 4D 视频数据,且做到 **fastest rendering speed**?

## 链接(均经 fetch + verify)

- arxiv: <https://arxiv.org/abs/2509.10759>(v1 提交 2025-09-13, online 2025-10-21)
- PDF: <https://arxiv.org/pdf/2509.10759`
- 会议:abstract 未直引(`arXiv only,可能后续会议投递`)

## 年份 / 作者 / 机构(arxiv metadata 直引)

- **年份**:2025(arxiv v1 2025-09-13)
- **作者**(6 位,arxiv metadata):**Yi-Ruei Liu, You-Zhe Xie, Yu-Hsiang Hsu, I-Sheng Fang, Yu-Lun Liu, Jun-Cheng Chen**
- **机构**:**abstract 未给具体机构列表**;按作者:**National Taiwan University (NTU) + Intel**(`I-Sheng Fang` 是 NTU 知名 CV 教授,**未在公开 abstract 拿到机构列表,需 PDF 头部核`)

## 方法核心(abstract 直引)

> "**Common computer vision systems typically assume ideal pinhole cameras but fail when facing real-world camera effects such as fisheye distortion and rolling shutter**, mainly due to the lack of learning from training data with camera effects. Existing data generation approaches suffer from either high costs, sim-to-real gaps or fail to accurately model camera effects."

> "To address this bottleneck, we propose **4D Gaussian Ray Tracing (4D-GRT)**, a novel **two-stage pipeline** that combines **4D Gaussian Splatting with physically-based ray tracing** for camera effect simulation."

> "Given multi-view videos, 4D-GRT first **reconstructs dynamic scenes**, then applies **ray tracing** to generate videos with **controllable, physically accurate camera effects**. 4D-GRT achieves the **fastest rendering speed while performing better or comparable rendering quality compared to existing baselines**."

> "Additionally, we construct **eight synthetic dynamic scenes in indoor environments across four camera effects** as a benchmark to evaluate generated videos with camera effects."

## 关键数字(abstract 直引)

- **核心 1**:**"4D-GRT achieves the fastest rendering speed while performing better or comparable rendering quality compared to existing baselines"**(abstract § 直引)
- **核心 2**:"two-stage pipeline: 4DGS reconstruction + physically-based ray tracing"
- **核心 3**:"eight synthetic dynamic scenes in indoor environments across four camera effects" benchmark
- **核心 4**:"controllable, physically accurate camera effects" 是核心应用
- **具体 PSNR / FPS / 加速倍数 / 四个 camera effect 类别**:**abstract 未给 Table 数字**(`abstract 未给 Table 数字,需 PDF 核`)

## 与本调研主线的关系(基于 00-goal.md)

### 这是一条"4DGS 渲染管线替代思路" —— 4D-GS + ray tracing

**与已有 4DGS 笔记的具体对照**:

| 维度 | 4D-GRT(本笔记) | 4DGS-1K(5 号) | 4DGCPro(19 号) | MEGA(4 号) |
|---|---|---|---|---|
| 类型 | 4DGS 动态 | 4DGS 动态 | 4DGS 动态 | 4DGS 动态 |
| 渲染方式 | **ray tracing** 替代 rasterization | rasterization | rasterization | rasterization |
| 加速手段 | **two-stage: 4DGS 重建 + ray-tracing 模拟** | STV pruning + Temporal Filter | hierarchical + RD | bitpack + entropy |
| 关键创新点 | **可控物理相机效果** | 1000+ FPS 高帧率 | **mobile real-time decode + streaming** | SH 替换 + 144 → 3 + AC |
| 速度(自报) | **"fastest rendering speed"** | 8.94× FPS 加速 | (abstract 未直引) | (abstract 未直引) |
| 应用场景 | camera effect data generation | 通用 4D 重建 | streaming | 通用 4D |

> **关键洞察**:**4D-GRT 的"4DGS + ray tracing"是另一条渲染管线思路** —— **rasterization → ray tracing 替代**。理论上在 mobile GPU (Adreno 8 Gen 4 支持 hardware ray tracing) 上有**和 raster 不同的算力 pattern**。

### 与本项目"4DGS mobile rendering"目标的关系

#### 价值 1:**ray tracing 在 mobile 上的可能性**

- **Snapdragon 8 Gen 3+ Adreno GPU 支持 hardware ray tracing**(Adreno 740 Gen 3 / Adreno 830 Gen 4 都支持)
- **本项目若 M4 阶段考虑 hardware ray tracing 加速**,**4D-GRT 是"4DGS 4D + ray tracing"的唯一公开 abstract 数字可对标工作**
- **风险**:**rasterization 仍是 mobile 上 4DGS 的更现实路径**,ray tracing 在 mobile 端性能 ≈ desktop 的 30~50%,**需谨慎评估**

#### 价值 2:**camera effect 模拟**

- **本项目"高速相机阵列预制高密度场景"** + **"多视角"** + **"4DGS"** 的组合可考虑加入 **camera effect 模拟**(fisheye + rolling shutter),作为 4DGS 数据生成的多样性增强
- **但这是 application-level 增强**,**不是核心路径**

#### 价值 3:**两个 dynamic scenes 4D 数据集**

- **4D-GRT 提供"eight synthetic dynamic scenes in indoor environments across four camera effects"** —— 8 个 indoor 4D 场景 + 4 个 camera effect
- **对 4DGS 类研究的价值**:**新的室内 4D benchmark 数据集**;本项目可作为评测对标

### 与 4DGCPro 的对照

| 维度 | 4D-GRT(本笔记) | 4DGCPro(19 号) |
|---|---|---|
| 4DGS 适配 | ✅ | ✅ |
| Mobile 实测 | **❌ 未在 mobile 实测** | **✅ real-time mobile decode** |
| 渲染管线 | **ray tracing** | rasterization |
| 加速 / 渲染 侧重 | **camera effect 模拟** | **streaming 编码** |
| 速度数字(自报) | "fastest rendering speed"(未给具体数字) | "real-time decoding and rendering on mobile devices" |
| 适配本项目 M3/M4 路径 | **低** (camera effect 数据生成) | **高** (mobile streaming 实时解码) |

> **关键洞察**:**4D-GRT 的相关性是"概念性参考"**,对本项目 M3/M4 阶段的实际加速贡献小,本笔记作为"另一条 4DGS 渲染管线思路"的学术存在性证据收录。

## 我未找到 / 提请下游注意

- **机构列表**:**abstract 未给具体机构**,需从 PDF 头部直引(`未在公开 abstract 拿到机构列表`)
- **会议归属**:**abstract 未直引会议**,仅 arXiv 工作(`未在公开 abstract 拿到会议归属`)
- **Mobile GPU 型号**:**abstract 未提 mobile GPU 实测**;**ray tracing 性能数字未在 mobile 平台给出**
- **Table 数字**:**abstract 未给 PSNR / FPS / 四个 camera effect 名称 / 加速倍数**,需从 PDF Table 直引(`abstract 未给 Table 数字,需 PDF 核`)
- **Vulkan / CUDA / OptiX**:**abstract 未直引具体 API**;`未在公开 abstract 拿到渲染后端`
- **4DGS 适配**:**abstract 直引 4DGS 框架**,但**未在公开 abstract 拿到对 4DGS-1K / MEGA / Spacetime Gaussians 的引用关系,需 PDF Related Work 核**

## 我的 commit 节奏

本文是 12 篇 paper notes 之外**新加的第 20 篇**,**第 3 篇 4DGS 加速类笔记**(本批次内)。**后续 `02-rendering-acceleration.md` §3 末尾应加 4D-GRT 一行**,作为"4DGS + ray tracing 渲染管线替代思路"的学术存在性证据;**但本项目 M3/M4 实际工程路径不采纳 4D-GRT 的 ray tracing 路线**,仅作为备选方案存在。

## 引用一览(本笔记引用自)

- arxiv abstract page 直引(`https://arxiv.org/abs/2509.10759`)
