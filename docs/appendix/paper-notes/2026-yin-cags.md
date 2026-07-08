# 2026-yin-cags · CAGS: Color-Adaptive Volumetric Video Streaming with Dynamic 3D Gaussian Splatting

> **相关性**:**⭐⭐⭐ 高度相关(Volumetric Video streaming + 3DGS LoD + Siggraph 2026)** —— **SIGGRAPH 2026 Conference Paper**(PDF 头部直引 "SIGGRAPH Conference Papers '26, July 19-23, 2026, Los Angeles, CA, USA");**核心创新 Color-Adaptive LoD + Scalable VQ + Post-Render Perspective Alignment(PRPA)**;**N3DV 3 个视频实测**;**multi-author 跨 4 国 9 单位**。

> **⚠ 重要边界声明**:**CAGS 是 3DGS-based VV streaming 系统**(不是 4DGS 原生)—— abstract 直引 "3DGS-based FVV methods"。**但**:**动态场景(N3DV)** + **server-client 架构** + **LoD streaming** —— **与本项目"高速相机阵列预制 + 端侧流式播放"工作流强相关**。

## 0.5 元数据

- **venue**: arxiv pre-print (2026-05)
- **arxiv-id**: 2605.09279
- **s2-id**: （v2 用 Semantic Scholar API 补全）
- **homepage**: （无）
- **github**: （无）
- **status**: under review
- **收录日期**: 2026-07-08
- **收录来源**: arxiv scan + 1-hop 引用规则
- **1-hop 引用**: （v2 补全，见 §11 1-hop 关系图）
- **评级**: ⭐

## 一句话问题

Volumetric Video(VV)streaming 现有 3DGS 方案存在 1) **LoD-based 质量下降明显**(density-based LoD 在 Gaussian 上不适用),2) **aggressive attribute compression 导致 color distortion**。**如何做"color-adaptive" 自适应 streaming,在 aggressive 量化下保持视觉质量**?

## 链接(均经 fetch + PDF 实测)
- arxiv: <https://arxiv.org/abs/2605.09279>(v1 提交 2026-05-09)
- PDF: 已下 `.pdfs/2605.09279.pdf`(41 MB)
- **会议**:**SIGGRAPH 2026 Conference Paper**(PDF 头部直引)

## 年份 / 作者 / 机构(PDF 头部实测)
- **年份**:2026
- **作者**(9 位,PDF 头部直引):**Daheng Yin, Yili Jin, Jianxin Shi, Isaac Ding, Miao Zhang, Fangxin Wang, Zhaowu Huang, Cong Zhang, Jiangchuan Liu*, Fang Dong**
- **机构**(PDF 头部直引,9 单位):
  1. **Simon Fraser University (SFU, 加拿大)**
  2. **Jiangxing Intelligence Inc.(江兴智能,中国深圳)**
  3. **McGill University (加拿大)**
  4. **Nankai University (南开大学,中国天津)**
  5. **The Chinese University of Hong Kong, Shenzhen (CUHK-SZ)**
  6. **Fuzhou University (福州大学)**
  7. **Southeast University (东南大学)**

## 方法核心(abstract + §4 直引)

### 三大关键发现(abstract § 直引)
> "Our preliminary studies reveal that **aggressive attribute compression primarily causes color distortion**, which can be **effectively corrected in the rendered image using a reference image**."

> "Existing Levels of Detail (LoD) methods based on **density are not well-suited to Gaussian representations**, leading to **visible gaps and severe quality degradation**."

### Color-Adaptive Scheme 三件套(abstract + §4 直引)
1. **Vector Quantization (VQ) for LoD** —— "uses vector quantization (VQ) to establish LoDs"
2. **Reference image color correction** —— "correct color distortions with low-resolution reference images"
3. **Lightweight restoration network** —— "adapt a lightweight SRResNet for restoration by modifying its input layer to support three settings: 1) color restoration from the distorted image, 2) super-resolution from the reference image, 3) example-based restoration from both images"

### CAGS 系统架构(§4 + Fig. 3 直引)
- **Offline**:**Scalable VQ** 建立 LoD → **Tiling** → **Draco lossless compression**
- **Online**:
  - **Server**:**viewport prediction** + **Adaptive FoV** + **3D tiles** + **Reference image rendering**(高 quality layer)
  - **Client**:**tile rendering** + **PRPA(Post-Render Perspective Alignment)** + **lightweight color restoration**

### Scalable Vector Quantization (SVQ)(§4.1)
- **AHC(Agglomerative Hierarchical Clustering)问题**:"AHC involves computing pairwise distances in each iteration, which is computationally prohibitive for Gaussian representations that typically contain **>100k Gaussians per frame**"
- **SVQ 解决**:"integrates the efficiency of KMeans clustering with the hierarchical structure of AHC, with an index assignment strategy to build a scalable codebook"
- **Codebook 4 层**:**L0(base)+ L1/L2/L3(enhancement)** = **可扩展多质量层**(类 4DGCPro / PD-4DGS 的 layer 设计思路)

### PRPA(§4.2)
> "PRPA aligns the reference image in three steps: ❶ unprojects client-view pixels using the depth map, ❷ reprojects them into the reference view, and ❸ samples the corresponding colors to produce an aligned image."

## 关键数字(§3.2 + Fig. 4 直引)

### 三视频 5 配置 PSNR(图 4,直引配置)
> "Configs 1–5 correspond to KMeans VQ settings where **scales are quantized to 8/10/12/14/16 bits**; **rotation and SH are quantized to 4/7/10/13/16 bits**; and **opacity is fixed at 4 bits**."

- **video: coffee_martini** PSNR ≈ 25-35 dB,Size ≈ 4-10 MB(图 4 left)
- **video: cook_spinach** PSNR ≈ 30-40 dB,Size ≈ 2-4 MB(图 4 mid)
- **video: cut_roasted_beef** PSNR ≈ 25-35 dB,Size ≈ 2-6 MB(图 4 right)

### 三大 insight(§3.2 直引)
> "example-based color restoration consistently achieves better visual quality than single-image color restoration and super-resolution. The results indicate that **aggressive VQ mainly damages color while preserving much of the scene structure**. Hence, example-based color restoration leverages preserved structural details to achieve more accurate and visually appealing results."

> "Moreover, when severe distortion makes the distorted image less trustworthy, example-based restoration relies more on the reference image and resembles super-resolution results. Thus, **super-resolution defines the lower bound of example-based restoration**."

## 与本调研主线的关系(基于 00-goal.md)

### 这与 3DGS / 4DGS streaming 派的方法学对照

| 维度 | CAGS(本笔记) | AirGS(本批 1 号) | 4DGCPro(19 号) | PD-4DGS(本批 2 号) | Mobile-GS(11 号) |
|---|---|---|---|---|---|
| 4D 适配 | (3DGS-based, N3DV 动态视频) | ✅ 4DGS | ✅ 4DGS | ✅ 4DGS | ❌ 3DGS 静态 |
| 会议 | **SIGGRAPH 2026** | (未直引) | (未直引) | (未直引) | ICLR 2026 |
| LoD | ✅ **Scalable VQ 4-layer** | keyframe | hierarchical | 3-layer HDD | ❌ |
| Streaming | ✅ server-client + viewport + FoV | ✅ server-client | ✅ single bitstream | ✅ DASH/HLS | ❌ |
| 颜色恢复 | ✅ **example-based + SRResNet** | ❌ | ❌ | TMC regulariser | ❌ |
| 单位 | **SFU + 8 others (9 单位)** | SJTU | SJTU | Qilu | UTS |
| Mobile GPU 实测 | ❌(N3DV desktop) | ❌(server 端) | ✅ mobile decode | ✅ iPhone 2 Mbps | ✅ Snap 8 Gen 3 127 FPS |

> **关键洞察**:**CAGS 是 VV streaming 派"color-adaptive LoD"路线的代表**;**与本项目"高速相机阵列预制 + 端侧流式播放"工作流直接相关**:
> - **CAGS 的 "viewport prediction + Adaptive FoV"** = **本项目 M3 阶段视口预测 / 自适应视野借鉴**
> - **CAGS 的 "Scalable VQ 4-layer"** = **本项目 M3 阶段 bitstream 多层设计借鉴**(类 4DGCPro / PD-4DGS)
> - **CAGS 的 "example-based color restoration"** = **本项目 M5 perceptual quality 课题借鉴**(低分辨率参考图 + 高频修复)

### 对本项目目标的具体承诺

- **CAGS 的 "color distortion 可用 reference image 修复"** = **本项目 M3 阶段可借鉴"低质量 base layer + 高质量 reference image"双流式策略**
- **CAGS 的 "viewport prediction + Adaptive FoV"** = **本项目 M4 阶段 6-DoF FVV 应用场景直接借鉴**
- **CAGS 的 SRResNet-based restoration** = **本项目 M5 阶段实时 perceptual quality 修复直接借鉴**(轻量 SR 网络可跑在 mobile GPU)

## 我未找到 / 提请下游注意

- **Mobile GPU 型号**:**abstract / §4 未提 mobile GPU / Adreno / Snap / Apple**(`未在公开 abstract 拿到 mobile GPU 型号`)—— **CAGS 不做 mobile GPU 端到端实测**
- **Vulkan 实现**:**abstract 未提 Vulkan**(`未在公开 abstract 拿到具体 mobile API`)
- **iPhone / Android client 端实测**:**未在 abstract / §3 拿到**(`未在公开 abstract 拿到 client 端实测数据`)—— **推测是 desktop / server 端为主**
- **PRPA 误差**:**未在 abstract 拿到具体 PRPA alignment 误差数字**(`未在公开 abstract 拿到 PRPA 误差分布`)
- **Server 渲染参考图的具体 GPU 型号**:**未在 abstract 拿到**(`未在公开 abstract 拿到 server GPU`)

## 我的 commit 节奏

本文是 12 篇 paper notes 之外**新加的第 20+ 篇**,**第 N 篇 VV streaming 类笔记**(本批 6 号)。**后续 `02-rendering-acceleration.md` §3 应加 CAGS 一行**;**`03-end-to-end-roadmap.md` 应专门为 CAGS 加一节"§Y. VV streaming color-adaptive 路径(CAGS PRPA + SVQ + example-based restoration)"**,作为"3DGS / 4DGS volumetric video streaming"的最直接学术先例。

## 引用一览(本笔记引用自)
- arxiv abstract page 直引(`https://arxiv.org/abs/2605.09279`)
- PDF 头部 9 作者 + 9 单位 affiliation 直引(`.pdfs/2605.09279.pdf`)
- PDF SIGGRAPH 2026 会议标识直引("SIGGRAPH Conference Papers '26, July 19-23, 2026, Los Angeles, CA, USA")
- PDF §3.2 测量 insight 直引(三视频 5 配置 PSNR)
- PDF §4.1 SVQ 直引(KMeans + AHC + 4-layer codebook)
- PDF §4.2 PRPA 直引(3 步对齐)
- PDF Fig. 3 / Fig. 4 / Fig. 5 caption 直引(CAGS pipeline / PSNR 对比 / SVQ 4-layer)

[abstract 直引] [PDF 直引] [推测] [调研深度:abstract + §3.2 + §4 + Fig.3/4/5,§5 evaluation 数字未及]
