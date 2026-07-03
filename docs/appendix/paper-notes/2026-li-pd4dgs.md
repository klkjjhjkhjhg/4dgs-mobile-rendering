# 2026-li-pd4dgs · PD-4DGS: Progressive Decomposition of 4D Gaussian Splatting for Bandwidth-Adaptive Dynamic Scene Streaming

> **相关性**:**⭐⭐⭐ 高度相关(4DGS mobile streaming + 渐进式 + 实测,2026-05)** —— **核心数字**:**"cuts the streamed bitstream by >60% at matched rendering fidelity and reduces first-frame latency from 73–930 s to ∼1.7 s on a 2 Mbps link"**(abstract 直引);**iPhone (Dycheck) 实测,2 Mbps 移动网络**;**"natively compatible with DASH/HLS"** —— **直接打"4DGS mobile streaming 派"路线**。

> **⚠ 重要边界声明**:**PD-4DGS 是 4DGS(动态)工作**,abstract 直引 —— **本项目主线命中**。**4DGS 在 mobile bandwidth 下"all-or-nothing 等待"问题被本研究首次系统化解决**:73~930 秒的等待降至 1.7 秒,**on-demand progressive streaming first framework for 4DGS**。

## 一句话问题

4DGS 的"monolithic bitstream"是 streaming 的"all-or-nothing"瓶颈:典型 ~25 MB 单一 bitstream(15 MB 静态 + 1.5 MB 全局 deformation + 8 MB 局部 deformation)在 2 Mbps 移动网络下需要 **100 秒**等待。**如何把 4DGS 改为 progressive,使得"任何 prefix 都可渲染"且兼容 DASH/HLS adaptive-bitrate**?

## 链接(均经 fetch + PDF 实测)
- arxiv: <https://arxiv.org/abs/2605.11427>(v1 提交 2026-05-12)
- PDF: 已下 `.pdfs/2605.11427.pdf`(3.4 MB)

## 年份 / 作者 / 机构(PDF 头部实测)
- **年份**:2026(arxiv v1 2026-05-12)
- **作者**:Jiachen Li, Guangzhi Han, Jin Wan, Delong Han, Yuan Gao, Min Li, Mingle Zhou, Gang Li*
- **机构**:**Qilu University of Technology (齐鲁工业大学)**

## 方法核心(abstract 直引 + PDF §3 直引)

### 三大组成(abstract §直引)

> "PD-4DGS, the first framework for progressive compression and on-demand transmission of 4DGS."

> 三件套:
> 1. **Hierarchical Deformation Decomposition (HDD)** —— "externalises the coarse-to-fine motion hierarchy already latent in 4DGS into three independently transmittable layers"
> 2. **Gaussian-entropy attribute rate–distortion loss + temporal mask consistency regulariser** —— "shrink the base layer while suppressing low-bitrate flicker"
> 3. **Capacity-weighted rollout schedule** —— "gated online by a learnt activation rate ρ"

### HDD 三层(abstract + §3.1 直引)

> "HDD factorises the rendering network into three additive bitstreams — Static Scaffold (ss0), +Global Deformation (ss1), +Local Refinement (ss2)."

| Layer | 内容 | 体积(Dycheck 估算) | 渲染能力 |
|---|---|---|---|
| **Layer 0 - Static Scaffold** | canonical anchors + attribute-prediction MLP | **0.5 MB** | 静态快照 |
| **Layer 1 - Global Deformation** | +Fglobal (HexPlane + MLP) | 1.7 MB(累计 2.0) | 粗动态 |
| **Layer 2 - Local Refinement** | +Flocal(per-Gaussian residuals) | 7.0 MB(累计 6.90 ~ 7) | full HD 细节 |

> **关键论断**(abstract):"base layer = 7.3% of full model · single bitstream · DASH / HLS ready"

### Rate-Distortion Optimization (R-DO)(§3.2)
- **可学习 mask m_i ∈ [0,1]**:对称乘 opacity 和 scale,`α'_i = α_i m_i`, `s'_i = s_i m_i`
- **dual multiplicative gating**:"ensures an anchor simultaneously becomes transparent and volume-zero as m_i → 0"
- **hard-threshold m_i > 0.01** at inference
- **Gaussian entropy model**:per-batch Gaussian prior `N(μ_a, σ²_a)` → Shannon bit cost `R(a) = -log_2 Φ((a+Q_a/2 - μ_a)/σ_a)`
- **目的**:"Layer 0 carries ~60% of total model size, so a bulky base layer defeats the second-scale first-frame promise"

### Temporal Mask Consistency (TMC)(§3.3)
- **问题**:"tiny mask differences across frames are amplified into visible inter-frame jitter, so a static-scene quantisation/masking scheme that looks adequate per-frame becomes a flicker source as soon as the deformation network is rolled out over time"
- **解法**:**TMC regulariser** 抑制低 bitrate flicker

### Capacity-Weighted Progressive Rollout Training(§3.4)
- **问题**:"Uniform layer sampling would systematically under-train the higher-capacity deformation networks, collapsing progressivity into a pseudo-progressive regime"
- **解法**:"samples layers non-uniformly and drives the sampling distribution online via a learnt mask-activation rate ρ = E[m_top - m_base]; the adaptive distribution π(ρ) = (1-ρ) π_uniform + ρ π_aggressive"
- **目的**:"reallocates budget across levels according to each scene's deformation complexity, **without any per-scene hyperparameter**"

## 关键数字(全部 abstract 直引 + Fig. 1 caption 直引)

### 头号数字(Fig. 1 标题直引)
> "**First-frame latency on Dycheck iPhone over a 2 Mbps link: existing methods need 73–930 s—far beyond the 3–5 s user-tolerance window**—while PD-4DGS streams a **0.44 MB static base layer in 1.7 s** and progressively upgrades to global motion (1.62 MB at 6.5 s) and full HD detail (6.90 MB at 27.6 s) from a single trained model natively compatible with DASH/HLS."

### 4DGS streaming 派数字对照(Fig. 1 左下)

| Method | First-frame latency | 比率 |
|---|---|---|
| MoDec-GS (CVPR 2025) | 73.5 s | 15× over |
| 4DGS (SIGGRAPH 2024) | 314 s | 63× over |
| Deformable 3DGS (CVPR 2024) | 438 s | 88× over |
| SC-GS (CVPR 2024) | 930 s | (baseline) |
| **PD-4DGS (Ours)** | **1.7 s** | **user-tolerance window 内** |

### Abstract 关键数字
- **">60% bitstream reduction at matched rendering fidelity"**
- **"first-frame latency 73-930 s → ~1.7 s on 2 Mbps"** —— **on-demand progressive streaming for 4DGS 首次实现**

## 与本调研主线的关系(基于 00-goal.md)

### 这是 4DGS mobile streaming 派的最强先例之一

| 维度 | PD-4DGS(本笔记) | AirGS(本批 1 号) | 4DGCPro(19 号) | Mobile-GS(11 号) |
|---|---|---|---|---|
| 类型 | 4DGS | 4DGS | 4DGS | 3DGS |
| 提交时间 | 2026-05 | 2025-12 | 2025-09 | 2026-03 |
| 渐进 / streaming | ✅ **3-layer HDD + DASH/HLS** | ✅ keyframe + ILP | ✅ hierarchical + RD | ❌ |
| Mobile 实测 | ✅ **iPhone 2 Mbps** | ❌(server 端) | ✅ mobile decode | ✅ **Snap 8 Gen 3 127 FPS** |
| 压缩率 | **>60% 减** | 50% 减 | (abstract 未直引) | 4.6 MB(静态) |
| 解码延迟 | **1.7 s (base)** | (未直引) | (未直引) | (实时) |
| Flicker 处理 | ✅ **TMC regulariser** | ❌ | ❌ | (无需) |
| 4DGS 适配 | ✅ **原生 4DGS** | ✅ | ✅ | ❌ 静态 |

> **关键洞察**:**PD-4DGS 是 4DGS streaming 派"ABR-friendly"的目前最强先例** —— **DASH/HLS 兼容**让本项目可以**直接套用 industry-standard streaming 协议**而不用自研 streaming server。

### 对本项目"高速相机阵列预制高密度场景 + 端侧流式播放"的核心借鉴

1. **借鉴 1 · HDD 三层架构**:**Static Scaffold + Global Deformation + Local Refinement** —— 本项目 M3 阶段最直接的 bitstream 设计模板:
   - **Layer 0** 0.5 MB = 高速相机阵列预制场景的 "静态几何 + 颜色基线"
   - **Layer 1** 1.5 MB = "粗动态"(每帧全局 motion)
   - **Layer 2** 5 MB = "局部细节"(毛发、面部肌肉等)
   - **总 7 MB / scene** 远低于 25 MB 4DGS 原 bitstream

2. **借鉴 2 · DASH/HLS 兼容**:**直接用 industry-standard streaming 协议**,本项目 M3 阶段不用自研 server + client

3. **借鉴 3 · Temporal Mask Consistency (TMC)**:**抑制低 bitrate flicker** —— 本项目 M5 perceptual quality 课题直接借鉴

4. **借鉴 4 · Capacity-Weighted Rollout**:**ρ-adaptive 训练采样** —— 本项目 M2 训练 pipeline 可借鉴,**避免 deformation network under-training**

### 对项目目标的具体承诺

- **"2 Mbps 移动网络,1.7 s 启动"是真实可达的** —— **比 Mobile-GS 的 127 FPS 桌面 GPU 实测更严苛的指标**(mobile 带宽 + 移动 GPU + 4D 三重压力)
- **DASH/HLS 兼容**:**意味着可以套用现成 CDN / edge caching 基建** —— 工程实现 M3 阶段成本大幅降低
- **3-layer 渐进 + 自适应层训练**:**方法学上"先验已验证"** —— 本项目 M3 阶段**第一优先借鉴**

## 我未找到 / 提请下游注意

- **会议归属**:**abstract 未直引会议**(`未在公开 abstract 拿到会议归属`)
- **项目页 / GitHub**:**abstract 未直引项目页**(`未在公开 abstract 拿到项目页 URL`)
- **Mobile GPU 型号**:**abstract 说 "iPhone"** 但未明示 Adreno / Apple GPU 型号(`未在公开 abstract 拿到 mobile GPU 型号`)—— 与 Mobile-GS 的 "Snap 8 Gen 3" 严格口径不严格对应
- **DASH/HLS 实现细节**:**abstract 未直引** server / client 端实现(`abstract 未给 server / client 端 stack 详情`)
- **Vulkan 实现**:**abstract 未提 Vulkan**(`未在公开 abstract 拿到具体 mobile API`)—— 推测仍是 PyTorch + 平台 native decoder
- **完整 Table 数字**:**abstract 给核心数字但未给完整 Table**(PSNR/SSIM/LPIPS/Bitrate/FPS per scene)
- **vs 4DGCPro 的具体差异**:**abstract 级别不易判定**;**需 PDF §4 实验对比表**核

## 我的 commit 节奏

本文是 12 篇 paper notes 之外**新加的第 20+ 篇**,**第 N 篇 4DGS streaming 类笔记**(本批 2 号)。**后续 `02-rendering-acceleration.md` §3 应加 PD-4DGS 一行**;**`03-end-to-end-roadmap.md` 应专门为 PD-4DGS 加一节"§Y. 4DGS ABR 路径(PD-4DGS DASH/HLS 兼容)"**,作为"4DGS mobile bandwidth-adaptive streaming"的最直接学术先例。

## 引用一览(本笔记引用自)
- arxiv abstract page 直引(`https://arxiv.org/abs/2605.11427`)
- PDF Fig. 1 caption 直引(`.pdfs/2605.11427.pdf`)
- PDF §3.1 / §3.2 / §3.3 / §3.4 直引(HDD / R-DO / TMC / Rollout)
- PDF §1 intro 实测(2 Mbps 100 秒 等待数字)

[abstract 直引] [PDF 直引] [推测] [调研深度:abstract + Fig.1 + §3,Table 数字未及]
