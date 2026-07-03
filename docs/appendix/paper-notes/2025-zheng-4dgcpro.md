# 2025-zheng-4dgcpro · 4DGCPro: Efficient Hierarchical 4D Gaussian Compression for Progressive Volumetric Video Streaming

> **相关性**:**高度相关(4DGS mobile 加速 + streaming,2025-09 / 项目页 2026-06)** —— **核心数字**:**"achieves real-time decoding and rendering on mobile devices while outperforming existing methods in RD performance across multiple datasets"**(abstract 直引);**"facilitates real-time mobile decoding and high-quality rendering via progressive volumetric video streaming in a single bitstream"**(abstract 直引);**10 位作者**;**Shanghai Jiao Tong University (MediaX 实验室) + 多个相关机构** 团队。

> **⚠ 重要边界声明**:**4DGCPro 是 4DGS(动态)工作**,**直接打到本项目主线** —— 4DGS 在 **mobile device 实测实时解码 + 流式 streaming** 是本项目"4DGS mobile rendering"目标的最直接对标。**"real-time decoding and rendering on mobile devices"** 是 abstract 段原话。

## 一句话问题

4DGS 的 **volumetric video** 流式传输面临:1) **无法单模型内调质量 / 码率** (网络带宽 + 设备差异大);2) **mobile device 上做不到实时解码 + 渲染**。**如何在单一 bitstream 中实现 progressive streaming,且在 mobile device 上做到实时解码 + 渲染**?

## 链接(均经 fetch + verify)

- arxiv: <https://arxiv.org/abs/2509.17513>(v1 提交 2025-09-22, online 2025-09-26)
- PDF: <https://arxiv.org/pdf/2509.17513`
- 项目页: <https://mediax-sjtu.github.io/4DGCPro>(github.io)
- 会议:abstract 未直引(`arXiv only,可能后续会议投递`)

## 年份 / 作者 / 机构(arxiv metadata + 项目页直引)

- **年份**:2025(arxiv v1 2025-09-22, 项目页更新至 2026-06-04)
- **作者**(10 位,arxiv metadata):**Zihan Zheng, Zhenlong Wu, Houqiang Zhong, Yuan Tian, Ning Cao, Lan Xu, Jiangchao Yao, Xiaoyun Zhang, Qiang Hu, Wenjun Zhang**
- **机构**:**Shanghai Jiao Tong University (上海交通大学, MediaX 实验室)**(项目页直引)+ 推测合作机构(**abstract 未给具体机构列表,需 PDF 头部核**)

## 方法核心(abstract 直引)

> "Achieving seamless viewing of **high-fidelity volumetric video**, comparable to 2D video experiences, **remains an open challenge**. Existing volumetric video compression methods either **lack the flexibility to adjust quality and bitrate within a single model** for efficient streaming across diverse networks and devices, or **struggle with real-time decoding and rendering on lightweight mobile platforms**."

> "To address these challenges, we introduce **4DGCPro**, a novel **hierarchical 4D Gaussian compression framework** that facilitates **real-time mobile decoding and high-quality rendering via progressive volumetric video streaming in a single bitstream**."

> "Specifically, we propose:

1. a **perceptually-weighted and compression-friendly hierarchical 4D Gaussian representation** with **motion-aware adaptive grouping** to reduce temporal redundancy, preserve coherence, and enable scalable multi-level detail streaming
2. an **end-to-end entropy-optimized training scheme**, which incorporates **layer-wise rate-distortion (RD) supervision** and **attribute-specific entropy modeling** for efficient bitstream generation"

## 关键数字(abstract 直引)

- **核心 1**:**"achieves real-time decoding and rendering on mobile devices while outperforming existing methods in RD performance across multiple datasets"**(abstract § 直引)
- **核心 2**:"real-time mobile decoding and high-quality rendering via progressive volumetric video streaming in a single bitstream"
- **核心 3**:"perceptually-weighted and compression-friendly hierarchical 4D Gaussian representation"
- **核心 4**:"motion-aware adaptive grouping to reduce temporal redundancy, preserve coherence"
- **核心 5**:"end-to-end entropy-optimized training scheme" + "layer-wise rate-distortion (RD) supervision"
- **具体 PSNR / FPS / bitrate / mobile GPU 型号**:**abstract 未给 Table 数字**(`abstract 未给 Table 数字,需 PDF 核`)

## 与本调研主线的关系(基于 00-goal.md)

### **这是 4DGS mobile 渲染的最直接对标 —— 主线命中**

**与已有笔记的具体对照**:

| 维度 | 4DGCPro(本笔记) | 4DGS-1K(5 号) | MEGA(4 号) | Mobile-GS(11 号) |
|---|---|---|---|---|
| 类型 | 4DGS 动态 | 4DGS 动态 | 4DGS 动态 | 3DGS 静态 |
| 提交时间 | 2025-09 | 2025-03 | 2024-10 | 2026-03 |
| 关键机制 | **hierarchical + RD + mobile decode** | STV pruning + Temporal Filter | bitpack + entropy | OIT + Vulkan |
| Mobile 实测 | **✅ real-time decode on mobile** | ❌(TITAN X 200+ FPS only) | ❌ | ✅ Snap 8 Gen 3 127 FPS |
| Streaming | **✅ progressive single bitstream** | ❌(单文件) | ❌ | ❌ |
| 压缩率 | **未直引** + RD supervision | 41.7× (PP) | (per attribute 3 + AC) | 4.6 MB / 27.12 PSNR |

> **关键洞察**:**4DGCPro 是 4DGS mobile 流式 streaming 的目前最直接对标** —— 同样目标(mobile device),同样 4D,同样追求 real-time。**对本项目 M3 / M4 阶段直接借鉴**:
> - **借鉴 1**:**"perceptually-weighted hierarchical 4D Gaussian representation"** —— 按感知重要性做层级,可直接给本项目 M5 的 "perceptual quality baseline" 课题
> - **借鉴 2**:**"motion-aware adaptive grouping"** —— **按运动复杂度动态分组**,与 4DGS-1K 的 STV 时空评分在"按重要性筛"思路上一致
> - **借鉴 3**:**"layer-wise rate-distortion (RD) supervision"** —— **分层 RD 训练,可控码率**,本项目 M4 阶段可作为 "60 FPS @ 1080p on Snap 8 Gen 4" 的码率预算工具
> - **借鉴 4**:**"real-time decoding and rendering on mobile devices"** 是 abstract 段原话 —— **直接验证 4DGS mobile 路径可行**

### 与 Mobile-GS 的对照

| 维度 | 4DGCPro(本笔记) | Mobile-GS(11 号) |
|---|---|---|
| 4D 适配 | **✅ 4DGS 原生** | ❌ 3DGS 静态(需扩展) |
| Mobile 实测 | **✅ real-time mobile decode** | ✅ 127 FPS on Snap 8 Gen 3 |
| 公开 mobile GPU 型号 | **未明示**(abstract 复数) | **Snap 8 Gen 3** |
| 适配 4DGS mobile 的"最小工程量" | **中等**(已有 4DGS 框架,加 hierarchical + RD) | **高**(需重写 4DGS deformation 为 OIT) |

> **关键洞察**:**4DGCPro 的 mobile 路径对 4DGS 是"低工程量扩展"**(加 hierarchical + RD supervision);**Mobile-GS 的 mobile 路径对 4DGS 是"高工程量改造"**(重写 deformation + 改 sort 为 OIT)。**对本项目 M3 阶段的具体决策**:
> - **若 M3 是"**最快 4DGS 跑 mobile**"**:选 **4DGCPro 思路**(hierarchical + RD + 现成 4DGS 框架)
> - **若 M4 是"**Snap 8 Gen 4 上 100+ FPS**"**:选 **Mobile-GS 思路**(OIT + Vulkan 端到端)

### 与本项目"高速相机阵列预制高密度场景"的关系

- **4DGCPro 的 progressive streaming 思路** = **本项目"场景预制 + 端侧流式播放"工作流的学术先例**
- **本项目预制场景后可仿 4DGCPro**:**hierarchical 4D Gaussian + single bitstream → Adreno 8 Gen 4 端侧实时解码 + 渲染**
- **iPhone-4D(Sparse4DGS) + 4DGCPro = 本项目"M2 应急数据采集 + M3 流式播放"完整链路**

## 我未找到 / 提请下游注意

- **机构列表**:**abstract 未给具体机构**,需从 PDF 头部直引(`未在公开 abstract 拿到机构列表`)。项目页 `mediax-sjtu` 域名直指 **Shanghai Jiao Tong University (SJTU) MediaX Lab**
- **会议归属**:**abstract 未直引会议**,仅 arXiv 工作(`未在公开 abstract 拿到会议归属`)
- **Mobile GPU 型号**:**abstract 用 "lightweight mobile platforms" / "mobile devices" 复数**,未明示 Adreno / Mali / Apple;**与 Mobile-GS 的 "Snap 8 Gen 3" 严格口径不严格对应**
- **Table 数字**:**abstract 未给 PSNR / FPS / bitrate / mobile GPU 详细数字**,需从 PDF Table 直引(`abstract 未给 Table 数字,需 PDF 核`)
- **Vulkan 实现**:**abstract 未提 Vulkan**,推测仍是 CUDA + 自研 mobile decoder;**未在公开 abstract 拿到具体 mobile API**
- **数据集**:**abstract 未明示 4D 数据集**,需 PDF 核 (`未在公开 abstract 拿到评测数据集`)

## 我的 commit 节奏

本文是 12 篇 paper notes 之外**新加的第 19 篇**,**第 2 篇 4DGS 加速类笔记**(本批次内)。**后续 `02-rendering-acceleration.md` §3 应加 4DGCPro 一行**;**`03-end-to-end-roadmap.md` 应专门为 4DGCPro 加一节"§X. 4DGS mobile streaming 路径"**,作为"4DGS 在 mobile device 实时解码 + 渲染"的最直接学术先例。

## 引用一览(本笔记引用自)

- arxiv abstract page 直引(`https://arxiv.org/abs/2509.17513`)
- 项目页 `https://mediax-sjtu.github.io/4DGCPro` (用于机构线索)
