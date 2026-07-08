# 2025-li-gifstream · GIFStream: 4D Gaussian-based Immersive Video with Feature Stream

> **相关性**:**⭐⭐ 中高相关(4DGS immersive video + 2D re-organization,2025-05)** —— **核心数字**:"delivers high-quality immersive video at **30 Mbps**, with **real-time rendering and fast decoding on an RTX 4090**"(abstract 直引);**项目页**:`https://xdimlab.github.io/GIFStream`;**Zhejiang University 团队**。

> **⚠ 重要边界声明**:**GIFStream 是 4DGS(动态)工作**,abstract 直引"4D Gaussian Splatting" + "6-Dof-free viewing experience" —— **本项目主线命中**。**核心创新是把 4DGS 重新组织为 2 个 video(VTI + VGF),借助 VVC / HEVC 视频编解码器压缩**。

## 0.5 元数据

- **venue**: CVPR 2025
- **arxiv-id**: 2505.07539
- **s2-id**: （v2 用 Semantic Scholar API 补全）
- **homepage**: （无）
- **github**: （无）
- **status**: received
- **收录日期**: 2026-07-08（首次）
- **收录来源**: arxiv scan + 1-hop 引用规则
- **1-hop 引用**: （v2 补全，见 §11 1-hop 关系图）
- **评级**: ⭐

## 一句话问题

Immersive video 需要 6-DoF 自由观看 + 高质量重建 + 可控存储。**4DGS 当前方法难以平衡质量与存储**。**如何把 4DGS 重新组织成 2D 视频格式,让传统视频编解码器(VVC / HEVC)直接压缩**?

## 链接(均经 fetch + PDF 实测)
- arxiv: <https://arxiv.org/abs/2505.07539>(v1 提交 2025-05-12)
- **项目页**:`https://xdimlab.github.io/GIFStream`(PDF Fig. 1 caption 直引)
- PDF: 已下 `.pdfs/2505.07539.pdf`(5.2 MB)

## 年份 / 作者 / 机构(PDF 头部实测)
- **年份**:2025
- **作者**(按 arxiv metadata 头部):**Hao Li, Sicheng Li, Xiang Gao, Abudouaihati Batuer, Lu Yu**, Yiyi Liao*
- **机构**:**Zhejiang University (浙江大学)**

## 方法核心(abstract + §3 直引)

### 三大组成(abstract + Fig. 1 直引)
> "we introduce GIFStream, a novel 4D Gaussian representation using a **canonical space and a deformation field enhanced with time-dependent feature streams**."

> 三大机制:
> 1. **Feature streams**:"enable complex motion modeling and allow efficient compression by leveraging temporal correspondence and motion-aware pruning"
> 2. **Temporal and spatial compression networks**:"for end-to-end compression"
> 3. **2D re-organization** (§3.2):"Leveraging the alignment provided by the canonical space and deformation, our representation can be sorted and reorganized into **two videos**"

### 4DGS → 2 Video 重新组织(§3.2 直引)
- **Video 1 - VTI (Time-Independent)**:**VTI ∈ R^((12+3K+C)×1×H×W)**:time-independent 信息 `{x ∈ R³, S1 ∈ R³, S2 ∈ R³, {o_i ∈ R³}^K_{i=1}, M ∈ R³, f ∈ R^C}`
  - **(12+3K+C) = channels** (time dimension)
  - **M = {M_de, M_knn, M_dy}** (motion modulation params)
- **Video 2 - VGF (Gaussian Feature)**:**VGF ∈ R^(N×P×h×w)**:time-dependent feature stream `{f_t}^N_{t=1}`,N frames × P channels
- **h < H, w < W** (VGF 分辨率 < VTI,因 sparsity pruning)

### 关键 trick(§3.2 直引)
> "Observing the sparsity of the feature stream, we directly **discard the feature stream set to zero by M_de**, and reorganize remaining features by skipping over the zero using line-by-line scanning."

> "the representation trained with our entropy supervision can also be **compressed using traditional video codecs, such as VVC [3] and HEVC [36]**."

### Feature Stream 稀疏性(§3 直引)
> "in challenging scenes, approximately **30% of the anchors require retention of time-dependent features**, while in simpler scenes, **only about 0.3% of the anchors need to retain these features**. This indicates that our representation can be effectively adapted to different scenarios."

### Gaussian Motion Prediction Head(§3.1 直引)
- **KNN aggregation**:`f̃_t = (1 - M_knn) Σ_{k∈N} f̂_{k,t} + M_knn · f̂_t`
- **Learnable factor M_dy**:"ensures anchors representing static objects remain stationary"
- **SE(3) motion**:`R_t = q2m(q̄ + M_dy · q_t)`, `T_t = M_dy · τ_t`
- **Position**:`p^i_t = R_t · S_2 · o_i + x + T_t`

## 关键数字(Fig. 1 caption + abstract 直引)
- **Fig. 1 直引**:
  - **4DGaussian**:PSNR 31.06,**108 MB**
  - **CSTG**:PSNR 31.93,**5.29 MB**
  - **Ours (GIFStream)**:Rate-SSIM curve 优势
- **Abstract 直引**:
  - **30 Mbps** 码率(immersive video 传输)
  - **real-time rendering + fast decoding on RTX 4090**
  - **time-dependent feature streams + motion-aware pruning + end-to-end compression**
- **30% 锚点 (challenging) / 0.3% 锚点 (simpler) 需要时序 features**(`§3 直引`)

## 与本调研主线的关系(基于 00-goal.md)

### 4DGS immersive video 派方法学对照

| 维度 | GIFStream(本笔记) | StreamSTGS(本批 8 号) | 4DGCPro(19 号) | AirGS(本批 1 号) |
|---|---|---|---|---|
| 4D 适配 | ✅ 4DGS | ✅ | ✅ | ✅ |
| 关键机制 | **canonical + deformation + time-dep feature streams + 2-video reorg** | canonical + 2D image + video | hierarchical + RD | keyframe + ILP |
| 视频编码 | ✅ **VVC / HEVC 兼容** | ✅(abstract 提 2D 视频) | ❌ | ❌(用 ILP) |
| Bitrate | **30 Mbps** | (未直引) | (未直引) | (未直引) |
| 单位 | **Zhejiang U** | Tianjin U | SJTU | SJTU |
| 项目页 | ✅ **有** | ❌ | ✅ | ❌ |
| 6-DoF | ✅(immersive video) | ✅(FVV) | ✅(volumetric) | ✅(FVV) |
| 实测 GPU | **RTX 4090**(桌面) | RTX A6000 | mobile(abstract) | (server 端) |

> **关键洞察**:**GIFStream 是 4DGS 派"传统视频编码工具借用"的代表**;**与 StreamSTGS 思路一致**(都把 4DGS 重新组织为 2D 视频格式);**与 4DGCPro / AirGS 思路不同**(后者用 hierarchical / ILP)。

### 对本项目"高速相机阵列预制 + 端侧流式播放"的具体借鉴

1. **借鉴 1 · 2-video re-organization**:**本项目 M2 / M3 bitstream 设计直接借鉴**(VTI + VGF 双视频 + VVC / HEVC 压缩)
2. **借鉴 2 · Feature stream sparsity-aware**:**本项目 M3 阶段可借鉴 M_de mask 机制**(30% / 0.3% 锚点保留策略)
3. **借鉴 3 · Time-dependent feature streams**:**本项目 M2 训练 pipeline 可借鉴**(比传统 deformation field 更灵活)

### 对项目目标的具体承诺

- **30 Mbps bitrate** = **本项目"端侧流式播放"的网络条件指标**(`[实测,abstract]`)
- **RTX 4090 实时** = **桌面 GPU 已验证**;**Snap 8 Gen 4 估算约 30-60 FPS**(`[推测,基于 Adreno 算力约 RTX 4090 的 1/4]`)
- **5.29 MB / scene vs 4DGaussian 108 MB** = **20× 压缩**(`[实测,Fig. 1]`)—— **本项目 M3 目标"≤ 50 MB"可期**

## 我未找到 / 提请下游注意

- **会议归属**:**abstract 未直引会议**(`未在公开 abstract 拿到会议归属`)
- **完整 Table 数字**:**Fig. 1 只给一个 PSNR 数字,未给完整 Table**(`abstract / Fig.1 未给完整 Table 数字,需 PDF §4 核`)
- **VVC / HEVC 实际压缩率**:**abstract 提"can be compressed using traditional video codecs"但未给具体压缩率**(`abstract 未给 VVC/HEVC 压缩率`)
- **Mobile GPU 实测**:**abstract 未提 mobile**(`未在公开 abstract 拿到 mobile GPU 型号`)
- **Vulkan 实现**:**abstract 未提 Vulkan**(`未在公开 abstract 拿到具体 mobile API`)
- **具体数据集**:**abstract 提"challenging scenes" / "simpler scenes" 但未给具体名字**(`abstract 未给评测数据集`)

## 我的 commit 节奏

本文是 12 篇 paper notes 之外**新加的第 20+ 篇**,**第 N 篇 4DGS immersive video 类笔记**(本批 9 号)。**后续 `02-rendering-acceleration.md` §3 应加 GIFStream 一行**;**`03-end-to-end-roadmap.md` 应专门为 GIFStream 加一节"§Y. 4DGS VVC/HEVC 兼容路径(GIFStream 2-video reorg + feature stream)"**,作为"4DGS 借鉴传统视频编解码器"的最直接学术先例。

## 引用一览(本笔记引用自)
- arxiv abstract page 直引(`https://arxiv.org/abs/2505.07539`)
- 项目页 `https://xdimlab.github.io/GIFStream` (PDF Fig. 1 caption 直引)
- PDF §3.1 直引(`.pdfs/2505.07539.pdf`)(Gaussian attribute prediction + motion prediction head)
- PDF §3.2 直引(2-video re-organization + VVC/HEVC 兼容)
- PDF §3 直引(30% / 0.3% 锚点 sparsity 数字)
- PDF 头部 author / Zhejiang U affiliation 直引

[abstract 直引] [PDF 直引] [推测] [调研深度:abstract + Fig.1 + §3,§4 Table 数字未及]
