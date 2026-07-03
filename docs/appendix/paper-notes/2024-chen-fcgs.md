# 2024-chen-fcgs · Fast Feedforward 3D Gaussian Splatting Compression

> **相关性**:**中等相关(3DGS 压缩另一路径,2024-10)** —— **核心数字**:**"compression ratio of over 20X while maintaining fidelity, surpassing most per-scene SOTA optimization-based methods"**(abstract 直引);**"significantly reduces compression time from minutes to seconds"**(abstract 直引);**Monash University 团队**(Yihang Chen, Qianyi Wu 等,**与 HAC++ 同组**)。

> **⚠ 重要边界声明**:**FCGS 是 3DGS(静态)压缩**。其价值在**"feedforward 压缩,把 minutes-level 优化压成 seconds-level"** —— 是 **HAC++ 的速度版**(HAC++ 还是 per-scene optimization,FCGS 是 feedforward)。

## 一句话问题

3DGS 压缩通常需要 **per-scene optimization** (分钟级) —— 如何做到 **feedforward single-pass**(秒级),且 **>20× 压缩率** + 维持 PSNR?

## 链接(均经 fetch + verify)

- arxiv: <https://arxiv.org/abs/2410.08017>(v1 提交 2024-10-10, online 2025-03-12)
- PDF: <https://arxiv.org/pdf/2410.08017>
- GitHub: <https://github.com/YihangChen-ee/FCGS>(abstract 直引)
- 会议:arxiv 2024,abstract 未直引(arXiv'24 标识在 GitHub README)

## 年份 / 作者 / 机构(arxiv metadata 直引)

- **年份**:2024(arxiv v1 2024-10-10)
- **作者**(6 位,arxiv metadata):**Yihang Chen, Qianyi Wu, Mengyao Li, Weiyao Lin, Mehrtash Harandi, Jianfei Cai**
- **机构**:**abstract 未给具体机构列表**;按作者:**Monash University + Shanghai Jiao Tong University + Adobe Research**(**未在公开 abstract 拿到机构列表,需 PDF 头部核**)

## 方法核心(abstract 直引)

> "With **3D Gaussian Splatting (3DGS) advancing real-time and high-fidelity rendering** for novel view synthesis, **storage requirements pose challenges** for their widespread adoption. Although various compression techniques have been proposed, **previous art suffers from a common limitation**: for any existing 3DGS, **per-scene optimization is needed to achieve compression, making the compression sluggish and slow**."

> "To address this issue, we introduce **Fast Compression of 3D Gaussian Splatting (FCGS)**, an **optimization-free model that can compress 3DGS representations rapidly in a single feed-forward pass**, which **significantly reduces compression time from minutes to seconds**."

> "To enhance compression efficiency, we propose:
1. a **multi-path entropy module** that assigns Gaussian attributes to different entropy constraint paths for balance between size and fidelity
2. carefully design both **inter- and intra-Gaussian context models** to remove redundancies among the unstructured Gaussian blobs"

## 关键数字(abstract 直引)

- **核心 1**:**"compression ratio of over 20X while maintaining fidelity, surpassing most per-scene SOTA optimization-based methods"**(abstract § 直引)
- **核心 2**:**"significantly reduces compression time from minutes to seconds"**(abstract § 直引)
- **核心 3**:"optimization-free model that can compress 3DGS representations rapidly in a single feed-forward pass"
- **核心 4**:"inter- and intra-Gaussian context models" —— **与 HAC++ 思路同源**(同团队)
- **代码**:"Our code is available at: `https://github.com/YihangChen-ee/FCGS`"(abstract 直引)
- **具体 PSNR / Storage MB / FPS 数字**:**abstract 未给 Table 数字**(`abstract 未给 Table 数字,需 PDF 核`)

## 与本调研主线的关系(基于 00-goal.md)

### 与 HAC++ 的关系:**同组,功能互补**

| 维度 | FCGS(本笔记) | HAC++(13 号笔记) |
|---|---|---|
| 团队 | Monash + SJTU + Adobe(同 HAC++) | 同 |
| 类型 | 3DGS 静态 | 3DGS 静态 |
| 压缩率(自报) | **>20×** | **>100×** vs vanilla 3DGS, **>20×** vs Scaffold-GS |
| 速度 | **seconds (feedforward)** | minutes (per-scene optimization) |
| 思路 | feedforward + multi-path entropy | per-scene + hash-grid context model |
| 开源 | ✅ FCGS | ✅ HAC-plus |

> **关键洞察**:**HAC++ 压得更狠(100×)但要数分钟,FCGS 压得稍弱(20×)但秒级**。**对 4DGS 的潜在借鉴**:训练后用 HAC++ 路径,实时流式传输场景用 FCGS 路径(快速 re-encode)。

### 与 MEGA / 4DGS-1K 的对照

| 维度 | FCGS | MEGA(4 号) | 4DGS-1K(5 号) |
|---|---|---|---|
| 4DGS 适配 | ❌ 3DGS only | ✅ 4DGS 原生 | ✅ 4DGS 原生 |
| 压缩率 | >20× (3DGS) | SH 3 + AC predictor(替换 144 SH) | N3V: 41.7× / D-NeRF: 39.7× (with PP) |
| 训练时间 | **seconds** | hours(retrained 4DGS) | 30 min fine-tune + 30 min pruning |
| 上下文建模 | inter- + intra-Gaussian | (none) | (none) |

> **关键洞察**:**FCGS 的"inter- + intra-Gaussian context model"思路可移植到 4DGS 的 temporal 维度**:把"跨 Gaussian"升级为"跨 Gaussian + 跨 time"。**本项目 M3 阶段可作为 fast-re-encode 路径储备**。

## 我未找到 / 提请下游注意

- **机构列表**:**abstract 未给具体机构**,需从 PDF 头部直引(`未在公开 abstract 拿到机构列表`)
- **Table 数字**:**abstract 未给 PSNR / Storage MB / FPS 详细数字**,需从 PDF Table 直引(`abstract 未给 Table 数字,需 PDF 核`)
- **mobile 实测**:**未在 mobile GPU 实测**(abstract 段未提),但"seconds-level 压缩"特性意味着**可在 mobile 端 on-device re-encode**
- **4DGS 适配性**:**论文未做 4DGS 适配**,但 inter-Gaussian context 可直接推广到 4DGS 的 inter-frame / inter-anchor context
- **训练/推理资源**:**abstract 未给 GPU 显存 / 训练时间详细数字**(`未在公开 abstract 拿到具体 GB / h`)

## 我的 commit 节奏

本文是 12 篇 paper notes 之外**新加的第 15 篇**,与 HAC++ 配套 —— **同团队 Monash 的 3DGS 压缩 SOTA 两条平行路径**。**后续 `02-rendering-acceleration.md` §3 压缩链路表应加 FCGS 一行**,作为"fast feedforward"路径独立对照。

## 引用一览(本笔记引用自)

- arxiv abstract page 直引(`https://arxiv.org/abs/2410.08017`)
