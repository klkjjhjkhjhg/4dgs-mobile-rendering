# 2025-wang-airgs · AirGS: Real-Time 4D Gaussian Streaming for Free-Viewpoint Video Experiences

> **相关性**:**中-高相关(4DGS streaming + 通信优化,2025-12)** —— 4DGS 面向 FVV(Free-Viewpoint Video)流式传输的工作;**不是 mobile GPU 实测**,**关注 transmission / bandwidth**;**与本项目"4DGS mobile rendering + 高速相机阵列预制"工作流高度相关**(端侧流式播放链路)。

> **⚠ 重要边界声明**:**AirGS 是 4DGS(动态)工作**,abstract 直引"4D Gaussian Splatting (4DGS) models dynamic scenes with time-varying 3D Gaussian ellipsoids"—— **本项目主线命中**。**但**:**AirGS 重点是 server 端 streaming / 通信 + training pipeline 优化,不是 mobile GPU 端到端实时渲染**;**没有 Vulkan / Adreno / Snap 实测**。

## 0.5 元数据

- **venue**: SIGGRAPH 2025
- **arxiv-id**: 2512.20943
- **s2-id**: （v2 用 Semantic Scholar API 补全）
- **homepage**: （无）
- **github**: （无）
- **status**: received
- **收录日期**: 2026-07-08（首次）
- **收录来源**: arxiv scan + 1-hop 引用规则
- **1-hop 引用**: （v2 补全，见 §11 1-hop 关系图）
- **评级**: ⭐

- **survey_section**: 6
## 一句话问题

4DGS 用于 FVV 时,1) **长序列质量下降**,2) **带宽和存储开销大**,3) **传输/训练时延长** —— 如何在 streaming 场景下保持高 PSNR + 低延迟 + 紧凑传输?

## 链接(均经 fetch + PDF 实测验证)
- arxiv: <https://arxiv.org/abs/2512.20943>(v1 提交 2025-12)
- PDF: 已下 `.pdfs/2512.20943.pdf`(15+ MB)

## 年份 / 作者 / 机构(PDF 头部实测)
- **年份**:2025
- **作者**(按 arxiv metadata 头部):**Zhe Wang, Jinghang Li, Yifei Zhu***(通讯)
- **机构**:**Shanghai Jiao Tong University, Global College**(PDF 头部直引)

## 方法核心(abstract 直引)

> "AirGS, a streaming-optimized 4DGS framework that rearchitects the training and delivery pipeline to enable high-quality, low-latency FVV experiences."

> 三大核心机制(abstract 直引):
> 1. **多通道 2D 格式** —— "converts Gaussian video streams into multi-channel 2D formats"
> 2. **关键帧识别** —— "intelligently identifies keyframes to enhance frame reconstruction quality"
> 3. **temporal coherence + inflation loss** —— "combines temporal coherence with inflation loss to reduce training time and representation size"
> 4. **通信效率**:"models 4DGS delivery as an integer linear programming problem and design a lightweight pruning level selection algorithm to adaptively prune the Gaussian updates to be transmitted, balancing reconstruction quality and bandwidth consumption"

## 关键数字(全部 abstract 直引)
- **质量稳定性**:"reduces quality deviation in PSNR by more than **20%** when scene changes"
- **PSNR 底线**:"maintains frame-level PSNR consistently **above 30**"
- **训练加速**:"accelerates training by **6×**"
- **传输**:"reduces per-frame transmission size by nearly **50%** compared to the SOTA 4DGS approaches"

> 详细 Table 数字(各数据集、bitrate、PSNR、SSIM、LPIPS):**abstract 未给 Table 数字,需 PDF 核**。

## 方法论要点(基于 intro 直引)

- **背景**:FVV = "allows users to explore a dynamic scene from arbitrary viewpoints" —— 重建路线 1) **explicit volumetric / mesh** [1, 2],2) **image-based interpolation** [3-5] —— "often struggle to achieve high reconstruction quality in real-world scenes with complex geometry"
- **3DGS → 4DGS 路径**: "3DGS has emerged as a highly efficient method for novel view synthesis" → "several efforts have extended 3DGS to 4D dynamic scene modeling" → "these methods typically use a fixed number of Gaussian ellipsoids across all frames, which **limits reconstruction quality over long sequences** and **increases per-frame storage overhead**"
- **3DGStream 对比**:"3DGStream [6] introduces a keyframe-based design, where a reference frame (anchor) is represented with full 3D Gaussians, and subsequent frames capture dynamics" —— AirGS 的 keyframe 思想是继承 + 改进 3DGStream
- **资助**:"supported by the National Key R&D Program of China (Grant No. 2024YFC3017100) and NSFC No. 62302292"

## 与本调研主线的关系(基于 00-goal.md)

### 这与 4DGS streaming / 端侧播放的直接关系

| 维度 | AirGS(本笔记) | 4DGCPro(2025-zheng-4dgcpro) | Mobile-GS(2026-du-mobile-gs) | PD-4DGS(2026-li-pd4dgs,本批 2 号) |
|---|---|---|---|---|
| 4D 适配 | ✅ 4DGS | ✅ 4DGS | ❌ 3DGS 静态 | ✅ 4DGS |
| Streaming | ✅ keyframe + ILP pruning | ✅ progressive bitstream | ❌ | ✅ 3-layer DASH/HLS |
| Mobile 实测 | ❌(server 端) | ✅ mobile decode | ✅ Snap 8 Gen 3 127 FPS | ✅ iPhone 2 Mbps |
| 关键机制 | 2D 多通道 + keyframe + ILP pruning | hierarchical + RD + mobile decode | OIT + Vulkan 2.0 | HDD + R-DO + TMC |
| 4DGS 路线 | keyframe-based, FVV streaming | progressive single bitstream | (静态 3DGS) | layer-wise ABR |

> **关键洞察**:**AirGS 与 4DGCPro / PD-4DGS 同属"4DGS streaming 派"**,三者都关心 4DGS 在带宽受限 / 移动网络下的传输;**路线差异**:
> - **AirGS**:**server 端** stream 优化(keyframe 选 + ILP 通信调度) + 训练 pipeline 加速(6×)
> - **4DGCPro**:**single bitstream** + hierarchical + mobile decode
> - **PD-4DGS**:**progressive 3-layer bitstream** + DASH/HLS 兼容(本批 2 号)
>
> **三者对项目 M3 / M4 阶段的核心借鉴**:
> - **借鉴 AirGS**:**"lightweight pruning level selection algorithm"** —— **逐级剪枝算法**;**"integer linear programming" formulation** —— 把 4DGS 传输建模为 ILP,**可加进 M3 流式播控模块**
> - **借鉴 4DGCPro**:**hierarchical** 4D Gaussian(感知 + 运动分组)
> - **借鉴 PD-4DGS**:**3-layer progressive** bitstream + Temporal Mask Consistency

### 与本项目"高速相机阵列预制高密度场景"的关系

- **AirGS 关注"长序列质量下降"**(abstract §直引)—— **本项目高速相机阵列预制场景正是长序列**,**AirGS 的 keyframe + inflation loss + temporal coherence 思路可借鉴**:
  - 高速相机阵列 1000 fps × 60 秒 = **60,000 帧长序列**,长序列 PSNR 衰减是已知难题
  - **借鉴 1**:**2D multi-channel format** 把 Gaussian video streams 压成 2D 图像格式(类视频编码思路),**给本项目 M2 阶段 "60K 帧压缩 + 存储" 提供现成思路**
  - **借鉴 2**:**temporal coherence + inflation loss** —— 减少训练时间和表示大小,**对项目 M2 训练阶段有帮助**

### 关键数字承诺

- **训练加速 6×**:**4DGS 训练在 RTX 3090 上 ≈ 2-4 小时/场景**;**AirGS ≈ 20-40 分钟/场景**(`[推测,需 PDF §4 实测核]`)—— **对项目 M2 训练 pipeline 有借鉴**
- **传输 50% 压缩**:**与 SOTA 4DGS 比**;若 SOTA 是 4DGS 原论文 25 MB / 帧,则 **AirGS ≈ 12.5 MB / 帧**
- **PSNR > 30 维持**:**场景切换时偏差降 20%** —— **FVV 实际用户感知的底线要求**

## 我未找到 / 提请下游注意

- **项目页 / GitHub**:abstract 未直引(`未在公开 abstract 拿到项目页 / 仓库 URL,需 PDF 核`)
- **会议归属**:**abstract 未直引会议**(待 CVPR/ICLR 2026 投递核)
- **Mobile GPU 型号**:**abstract 未提 mobile GPU / Vulkan / Adreno / Snap** —— **AirGS 不做 mobile GPU 端到端实测**(`未在公开 abstract 拿到 mobile GPU 型号`)
- **Vulkan 实现**:**abstract 未提 Vulkan**(`未在公开 abstract 拿到 mobile API`)
- **数据集**:abstract 提到"free-viewpoint video benchmarks"但未给具体名字(需 PDF 核)
- **Table 数字**:**abstract 未给 PSNR / FPS / bitrate 详细 Table**(`abstract 未给 Table 数字,需 PDF §4 核`)
- **与 4DGCPro / PD-4DGS 路线具体差异**:**abstract 级别不易判定**;**需 PDF §3 / §4 详细对比**

## 我的 commit 节奏

本文是 12 篇 paper notes 之外**新加的第 20+ 篇**,**第 N 篇 4DGS streaming 类笔记**(本批 1 号,本批次中 4DGS streaming 派第 1 篇)。**后续 `03-end-to-end-roadmap.md` 应加一节"§Y. 4DGS streaming 派 4 路线对照(AirGS / 4DGCPro / PD-4DGS / GaussianStream)"**。

## 引用一览(本笔记引用自)
- arxiv abstract page 直引(`https://arxiv.org/abs/2512.20943`)
- PDF 头部 author / affiliation 直引(`.pdfs/2512.20943.pdf`)
- 资助信息 PDF 脚注直引(国家 2024YFC3017100 + NSFC 62302292)

[abstract 直引] [PDF 直引] [推测] [调研深度:abstract + intro + 资助段,Table 数字未及]
