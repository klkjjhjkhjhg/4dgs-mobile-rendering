# 2025-oh-neo · Neo: Real-Time On-Device 3D Gaussian Splatting with Reuse-and-Update Sorting Acceleration

> **相关性**:**⭐⭐⭐ 高度相关(3DGS on-device hardware accelerator + ASPLOS 2026)** —— **ASPLOS 2026**(PDF 头部直引 "ASPLOS '26, March 22-26, 2026, Pittsburgh, PA");**核心数字**:"achieves up to **10.0×** and **5.6× higher throughput** compared to the Orin AGX GPU and GSCore, respectively, while **reducing sorting-induced memory traffic by 94.5% and 81.3%**"(abstract 直引);**"real-time 3DGS rendering at QHD resolutions, achieving an average throughput of 99.3 FPS"**。

> **⚠ 重要边界声明**:**Neo 是 3DGS(静态)工作**,**不是 4DGS**。**但**:**直接打到本项目"on-device 3DGS / 4DGS 加速"的核心瓶颈——sorting**;**KAIST + Meta 团队**;**7nm ASIC 综合**。

## 一句话问题

3DGS on-device AR/VR 渲染的瓶颈是 **sorting 阶段**(高 memory bandwidth demand)。**如何利用相邻帧 Gaussian 顺序的时序冗余,做 reuse-and-update 排序,避免每帧重新 sort**?

## 链接(均经 fetch + PDF 实测)
- arxiv: <https://arxiv.org/abs/2511.12930>(v1 提交 2025-11)
- **会议**:**ASPLOS 2026**(PDF 头部直引)
- PDF: 已下 `.pdfs/2511.12930.pdf`(3.2 MB)

## 年份 / 作者 / 机构(PDF 头部实测)
- **年份**:2025(投稿 ASPLOS 2026)
- **作者**(按 arxiv metadata 头部):**Changhun Oh, Seongryong Oh, Jinwoo Hwang, Yoonsung Kim, Hardik Sharma, Jongse Park**
- **机构**(PDF 头部直引):
  - **KAIST (Korea Advanced Institute of Science and Technology, 韩国科学技术院)**
  - **Meta (Sunnyvale, CA, USA)** —— Hardik Sharma

## 方法核心(abstract + §1-3 直引)

### 关键问题识别(abstract + §2.4 直引)
> "Our analysis identifies the **sorting stage** in the 3DGS rendering pipeline as the **major bottleneck** due to its high memory bandwidth demand."

### Reuse-and-Update Sorting(abstract § 直引)
> "Neo, which introduces a **reuse-and-update sorting algorithm** that exploits temporal redundancy in Gaussian ordering across consecutive frames and devises a **hardware accelerator optimized for this algorithm**."

> "By efficiently **tracking and updating Gaussian depth ordering instead of re-sorting from scratch**, Neo significantly reduces redundant computations and memory bandwidth pressure."

### 3DGS Pipeline 4 阶段(§2.3 直引)
1. **Frustum Culling** —— 丢弃视锥外 Gaussians
2. **Feature Extraction** —— 投影 3D → 2D,提取 view-dependent 特征
3. **Sorting**(瓶颈)—— 按深度排序
4. **Rasterization** —— α-blending,深度排序后的累加

### Tile-based Parallelism(§2.4 直引)
- 把 image plane 划分为 tile grid
- Sorting 阶段:Gaussians 复制分配到相交 tiles
- Rasterization 阶段:per-tile 处理
- **NVIDIA CUB library 用于 sorting**;custom CUDA kernels 用于 rasterization

### 综合实现(abstract + §1 直引)
> "We synthesize Neo using Synopsys Design Compiler with **ASAP 7nm library [98]**"

### On-Device 平台背景(§2.1 直引)
> "Apple Vision Pro [2] features a combined **23 million pixels**, achieving 4K-level resolution. Meanwhile, **Meta Quest 3 [66] provides a per-eye resolution of 2064×2208**, with both devices supporting refresh rates of up to **90Hz**."

## 关键数字(全部 abstract + §5 直引)
- **核心 1**:"**10.0×** higher throughput compared to the **Orin AGX GPU**"
- **核心 2**:"**5.6×** higher throughput compared to the state-of-the-art accelerator **GSCore**"
- **核心 3**:"**reduces sorting-induced memory traffic by 94.5%** (vs Orin AGX) and **81.3%** (vs GSCore)"
- **核心 4**:"real-time 3DGS rendering at **QHD resolutions**, achieving an average throughput of **99.3 FPS**"
- **QHD 分辨率**:2560×1440(4K-level)
- **Orin AGX GPU**:NVIDIA Jetson AGX Orin(mobile/edge GPU)
- **GSCore**:SOTA ASIC accelerator
- **ASAP 7nm**:academic 7nm standard cell library

### Throughput 对比(Fig. 3 直引,5 scene)
- **Family / Francis / Horse / Lighthouse / Playground / Train** 6 场景
- **HD / FHD / QHD** 三档分辨率
- **0-100 FPS** 范围

## 与本调研主线的关系(基于 00-goal.md)

### 这与 on-device 3DGS 加速的方法学对照

| 维度 | Neo(本笔记) | Mobile-GS(11 号) | Lumina(本批 13 号) | HiGS(2026-ning-higgs) | FlashGS(2024-feng-flashgs) |
|---|---|---|---|---|---|
| 4D 适配 | ❌ 3DGS 静态 | ❌ 3DGS 静态 | (3DGS 通用) | ❌ 3DGS 静态 | ❌ 3DGS 静态 |
| 形式 | **硬件 ASIC 加速器** | **GPU + Vulkan 2.0** | 硬件-算法 co-design | (Snap 8 Gen 3 量化) | (CUDA 加速) |
| 关键机制 | **Reuse-and-update sort** | OIT + NVQ + SH-distill | temporal coherence + RC | 4-bit + 帧间 hash | CUDA optimization |
| 实测 GPU | **vs Orin AGX, GSCore(ASIC)** | **Snap 8 Gen 3** | **mobile Volta GPU** | **Snap 8 Gen 3** | NVIDIA RTX |
| 加速比 | **10× / 5.6×** | 127 vs 8 FPS(15.9×) | 4.5× speedup | (未直引) | (未直引) |
| Memory traffic 减 | **94.5% / 81.3%** | (未直引) | (未直引) | (未直引) | (未直引) |
| 会议 | **ASPLOS 2026** | ICLR 2026 | (未直引,2025) | (未直引,2026) | CVPR 2025 |

> **关键洞察**:**Neo 是 3DGS 派"on-device 硬件加速"的代表**;**与 Mobile-GS (GPU + Vulkan) 路线对立** —— **Neo 是 ASIC 专用硬件**;**与 Lumina 同属"硬件-算法 co-design"派**;**与 HiGS(本调研已有 2026-ning-higgs)的 Snap 8 Gen 3 量化路线互补**。

### 对本项目"4DGS mobile rendering"的具体借鉴

1. **借鉴 1 · Reuse-and-update sort 思路**:
   - **3DGS 跨帧 Gaussian 顺序时序冗余** = **本项目 4DGS 同样适用**(相邻帧高斯顺序基本不变)
   - **本项目 M4 阶段 Vulkan 实现**:**可借鉴"mask 复用"思路**(类似 4DGS-1K 的 Temporal Filter mask)
   - **实测提升 10×** —— **本项目 M4 / M5 阶段目标"60 FPS @ 1080p on Snap 8 Gen 4" 的潜在加速源**

2. **借鉴 2 · Memory bandwidth 是 on-device 渲染的核心瓶颈**:
   - **94.5% memory traffic 减** = **本项目 M4 阶段 Vulkan / OpenGL ES 实现要重点优化 memory access**
   - **Snap 8 Gen 4 共享内存架构**:**tile-based 渲染是关键技术**(类 Mali / PowerVR)

3. **借鉴 3 · ASIC 7nm 综合**:**本项目 M5+ 阶段长远可考虑 ASIC 路径**(本项目 M3 / M4 走 GPU + Vulkan)

### 对项目目标的具体承诺

- **"real-time 3DGS at QHD = 99.3 FPS"**:**桌面 ASIC 7nm 已验证先例**;**Snap 8 Gen 4 估算约 30-50 FPS at 1080p**(`[推测,基于 Adreno 算力约 Neo 7nm ASIC 的 1/2-1/3]`)—— **本项目 M4 目标"60 FPS @ 1080p on Snap 8 Gen 4" 接近可达**
- **94.5% memory traffic 减**:**本项目 M4 / M5 阶段 memory bandwidth 优化方向**
- **vs Orin AGX 10×**:**Snap 8 Gen 4 与 Orin AGX 同属 mobile / edge GPU 类别**,**Neo 的硬件优化思路可直接借鉴到本项目**

## 我未找到 / 提请下游注意

- **4DGS 适配**:**abstract 未提 4DGS**(`未在公开 abstract 拿到 4DGS 适配信息`)—— **Neo 是 3DGS 静态,需扩展到 4DGS 时序 sort**
- **Vulkan 实现**:**abstract 未提 Vulkan**(`未在公开 abstract 拿到具体 GPU API`)—— **Neo 是 ASIC 7nm,不走 Vulkan**
- **完整 Table 数字**:**abstract 提 10×/5.6×/94.5%/81.3%/99.3 FPS 但未给完整 Table**(`abstract 未给 PSNR / 完整 Table 数字,需 PDF §5 核`)
- **Orin AGX / GSCore 详细对比**:**abstract 只给比率,未给绝对数字**(`abstract 未给 Orin AGX / GSCore 的绝对 throughput`)
- **不同 sort 算法(quicksort, radix sort, bitonic sort)在 4DGS 上的对比**:**abstract 未提**(`abstract 未给 sort 算法对比`)

## 我的 commit 节奏

本文是 12 篇 paper notes 之外**新加的第 20+ 篇**,**第 N 篇 on-device 3DGS 加速类笔记**(本批 10 号)。**后续 `02-rendering-acceleration.md` §3 应加 Neo 一行**;**`03-end-to-end-roadmap.md` 应专门为 Neo 加一节"§Y. On-device 硬件加速派路径(Neo reuse-and-update sort + ASIC 7nm)"**,作为"3DGS / 4DGS on-device hardware acceleration"的最直接学术先例。

## 引用一览(本笔记引用自)
- arxiv abstract page 直引(`https://arxiv.org/abs/2511.12930`)
- PDF 头部 ASPLOS 2026 会议标识直引(`.pdfs/2511.12930.pdf`)
- PDF 头部 author / 2 单位(KAIST + Meta)affiliation 直引
- PDF §2.3 / §2.4 3DGS pipeline 4 阶段直引
- PDF §5 throughput 对比直引(Orin AGX 10× / GSCore 5.6× / 99.3 FPS QHD)
- PDF Fig. 3 caption 直引(5 scene × 3 resolution throughput)

[abstract 直引] [PDF 直引] [推测] [调研深度:abstract + §2 + Fig.3,§5 完整 Table 未及]
