# 2024-liu-efficientgs · EfficientGS: Streamlining Gaussian Splatting for Large-Scale High-Resolution Scene Representation

> **相关性**:**中等相关(3DGS 大规模加速,2024-04)** —— **核心数字**:**"a model size approximately tenfold smaller than conventional 3DGS while maintaining high rendering fidelity"**(abstract 直引);**"expedites training and rendering times"**(abstract 直引);**4K+ aerial images 评测**;**9 位作者含 Wenkai Liu 等**。

> **⚠ 重要边界声明**:**EfficientGS 是 3DGS(静态)工作**,**不是 4DGS**。其价值在"**4K+ aerial images** 大规模 + 高分辨率场景的 3DGS 训练和渲染加速 + 存储压缩 10×" —— 是 **"大规模 + 高分辨率" SOTA**。

> **时窗说明**:**arxiv 2024-04 提交**,严格意义上 **2024 H1 提交**;但 **online 2024-04-19** 属于本任务"2024 H2 ~ 2026 H1 调研窗口"内的"4DGS 同期 3DGS 加速"基线;**作为 4DGS 同期 3DGS 加速对照**收录。

## 0.5 元数据

- **venue**: CVPR 2024
- **arxiv-id**: 2404.12777
- **s2-id**: （v2 用 Semantic Scholar API 补全）
- **homepage**: （无）
- **github**: （无）
- **status**: received
- **收录日期**: 2026-07-08（首次）
- **收录来源**: arxiv scan + 1-hop 引用规则
- **1-hop 引用**: （v2 补全，见 §11 1-hop 关系图）
- **评级**: ⭐

- **survey_section**: 5
## 一句话问题

3DGS 应用于 **4K+ 大规模高分辨率场景**(航空图、城市级)时,高斯数量爆炸导致 **训练 + 渲染 + 存储** 全部超预算 —— 如何 **10× 压缩 + 加速训练渲染 + 保持质量**?

## 链接(均经 fetch + verify)

- arxiv: <https://arxiv.org/abs/2404.12777>(v1 提交 2024-04-19)
- PDF: <https://arxiv.org/pdf/2404.12777>
- 会议:abstract 未直引(arXiv'24 only,经 CSDN 报道直引)

## 年份 / 作者 / 机构(arxiv metadata 直引)

- **年份**:2024(v1 2024-04-19)
- **作者**(9 位,arxiv metadata):**Wenkai Liu, Tao Guan, Bin Zhu, Lili Ju, Zikai Song, Dan Li, Yuesong Wang, Wei Yang**(+ 1)
- **机构**:**abstract 未给具体机构列表**;按作者名:**Huazhong University of Science and Technology (HUST)** + 第三方(`未在公开 abstract 拿到机构列表,需 PDF 头部核`)

## 方法核心(abstract 直引)

> "In the domain of 3D scene representation, **3D Gaussian Splatting (3DGS) has emerged as a pivotal technology**. However, its application to **large-scale, high-resolution scenes (exceeding 4k×4k pixels)** is hindered by the excessive computational requirements for managing a large number of Gaussians."

> "Addressing this, we introduce **'EfficientGS'**, an advanced approach that optimizes 3DGS for high-resolution, large-scale scenes. We analyze the **densification process in 3DGS** and identify areas of Gaussian over-proliferation. We propose:

1. **a selective strategy, limiting Gaussian increase to key primitives**, thereby enhancing the representational efficiency
2. **a pruning mechanism to remove redundant Gaussians**, those that are merely auxiliary to adjacent ones
3. **a sparse order increment for Spherical Harmonics (SH)**, designed to alleviate storage constraints and reduce training overhead"

## 关键数字(abstract 直引)

- **核心 1**:**"a model size approximately tenfold smaller than conventional 3DGS while maintaining high rendering fidelity"**(abstract § 直引)
- **核心 2**:**"expedites training and rendering times"**(abstract § 直引)
- **核心 3**:"extensive 4K+ aerial images" 数据集评测
- **核心 4**:"sparse order increment for SH" —— SH 阶数自适应,降低存储
- **具体 PSNR / FPS / Storage MB 数字**:**abstract 未给 Table 数字**(`abstract 未给 Table 数字,需 PDF 核`)

## 与本调研主线的关系(基于 00-goal.md)

### 与 4DGS-1K 思路高度平行

| 维度 | EfficientGS(本笔记) | 4DGS-1K(5 号笔记) |
|---|---|---|
| 类型 | 3DGS 静态 | 4DGS 动态 |
| 压缩率(自报) | **10×** vs vanilla 3DGS | **41.7×** (N3V with PP) / 39.7× (D-NeRF with PP) |
| 关键 trick | selective densification + pruning + sparse SH | STV pruning + Temporal Filter mask + PP-VQ |
| 大规模/高分辨率 | **4K+ aerial images** 显式对标 | (无大规模 4D 公开数据集) |
| SH 处理 | sparse order increment | PP-VQ on SH coefficients |

> **关键洞察**:**EfficientGS 的"selective densification + pruning"思路与 4DGS-1K 的"STV pruning"在 static 维度等价**。**对本项目 M3 阶段的潜在价值**:**4DGS-1K 的 STV pruning 思路可推广到"4DGS + 大规模 aerial / city 4D 场景"** —— 在 HUST 团队(本组同时出 4DGS Wu et al. 2024)的视线内,本项目可参考其静态大规模经验做动态大规模。

### 与本调研线已有笔记对照

| 笔记 | 路径 | 压缩率 | 关键数字(abstract 直引) |
|---|---|---|---|
| LightGaussian(已有 10 号) | 3DGS 静态压缩 | (需 PDF) | 60 FPS → 227 FPS(Mip-NeRF 360) |
| Mip-Splatting(已有 8 号) | 3DGS 静态 + 抗锯齿 | (非压缩) | 改进 AA |
| Scaffold-GS(未单列) | 3DGS 静态 anchor-based | (需 PDF) | (HAC++ 提 20× vs 它) |
| HAC++(13 号) | 3DGS 静态 hash-grid 压缩 | **>100×** | >20× vs Scaffold-GS |
| FCGS(14 号) | 3DGS 静态 feedforward 压缩 | **>20×** | feedforward, seconds |
| **EfficientGS(本笔记)** | 3DGS 静态大规模 | **~10×** | 4K+ aerial images |

## 我未找到 / 提请下游注意

- **机构列表**:**abstract 未给具体机构**,需从 PDF 头部直引(`未在公开 abstract 拿到机构列表`)
- **Table 数字**:**abstract 未给 PSNR / FPS / Storage MB 详细数字**,需从 PDF Table 直引(`abstract 未给 Table 数字,需 PDF 核`)
- **mobile 实测**:**未在 mobile GPU 实测**(abstract 段未提)
- **4DGS 适配性**:**论文未做 4DGS 适配**,但其"selective densification + pruning"思路与 4DGS-1K STV pruning 在静态维度等价
- **时窗**:**2024-04 提交**,严格 2024 H1,**作为 4DGS 同期 3DGS 加速基线**收录
- **本项目 M3 阶段借鉴度**:**中等** —— **大规模 + 高分辨率 3DGS 经验可直接借鉴到 4DGS 的大规模场景** (e.g. 高速相机阵列预制高密度场景)

## 我的 commit 节奏

本文是 12 篇 paper notes 之外**新加的第 16 篇**,与 HAC++ / FCGS / LightGaussian 配套 —— **同方向 3DGS 静态压缩加速的 SOTA 集合**。**后续 `02-rendering-acceleration.md` §3 压缩链路表应加 EfficientGS 一行**,作为"大规模 + 高分辨率"路径独立对照。

## 引用一览(本笔记引用自)

- arxiv abstract page 直引(`https://arxiv.org/abs/2404.12777`)
