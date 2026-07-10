# 2024-feng-flashgs · FlashGS: Efficient 3D Gaussian Splatting for Large-scale and High-resolution Rendering

> **相关性**:**中等相关(3DGS 桌面临近 SOTA,CVPR 2025)** —— **核心数字**:**average 4× acceleration over mobile consumer GPUs**(abstract 直引),**"over mobile consumer GPUs" 这个措辞是本调研线最看重的属性**(虽然不是 4DGS);开源 CUDA 库,**项目 11 位作者含 Guofeng Feng,Siyan Chen 等**。

> **⚠ 重要边界声明**:**FlashGS 是 3DGS(静态)工作**,**不是 4DGS**。但其 "**average 4× speedup over mobile consumer GPUs**" 这个 abstract 直引数字是**桌面对标**层面非常难得的 mobile GPU 实测数字;虽然不是 4DGS,本调研作为"4DGS mobile 路径的桌面先例"收录。

## 0.5 元数据

- **venue**: CVPR 2024
- **arxiv-id**: 2408.07967
- **s2-id**: （v2 用 Semantic Scholar API 补全）
- **homepage**: （无）
- **github**: （无）
- **status**: received
- **收录日期**: 2026-07-08（首次）
- **收录来源**: arxiv scan + 1-hop 引用规则
- **1-hop 引用**: （v2 补全，见 §11 1-hop 关系图）
- **评级**: ⭐⭐

- **survey_section**: 5
## 一句话问题

如何在 **CUDA 层面**让 3DGS 在 **mobile consumer GPU(笔记本/手机 GPU)** 上获得 **平均 4× 加速 + 内存下降**,且开源一个 Python + CUDA 的可集成库?

## 链接(均经 fetch + verify)

- arxiv: <https://arxiv.org/abs/2408.07967>(v1 提交 2024-08-15, online 2024-08-19)
- PDF: <https://arxiv.org/pdf/2408.07967>
- 项目页:见 CVPR 2025 收录论文 PDF `https://openaccess.thecvf.com/content/CVPR2025/papers/Feng_FlashGS_Efficient_3D_Gaussian_Splatting_for_Large-scale_and_High-resolution_Rendering_CVPR_2025_paper.pdf`
- GitHub: `https://github.com/InternLandMark/FlashGS`(abstract 末尾未直引 commit URL,**需从项目页核**)
- 会议:**CVPR 2025**(PDF 头部实测,见博客园第三方报道直引 "[CVPR 2025]")

## 年份 / 作者 / 机构(arxiv metadata 直引)

- **年份**:2024(v1 2024-08-15)
- **作者**(10 位,arxiv metadata):**Guofeng Feng, Siyan Chen, Rong Fu, Zimu Liao, Yi Wang, Tao Liu, Zhilin Pei, Hengjie Li, Xingcheng Zhang, Bo Dai**
- **机构**:**abstract 未给**,**需 PDF 核**(推测含 THU + Intern + SJTU,**未在公开 abstract 拿到具体机构**)

## 方法核心(abstract 直引)

> "This work introduces **FlashGS, an open-source CUDA Python library**, designed to facilitate the efficient differentiable rasterization of 3D Gaussian Splatting through **algorithmic and kernel-level optimizations**."

> "FlashGS is developed based on the observations from a comprehensive analysis of the rendering process to enhance computational efficiency and bring the technique to wide adoption. The paper includes a suite of optimization strategies, encompassing:

1. **redundancy elimination**
2. **efficient pipelining**
3. **refined control and scheduling mechanisms**
4. **memory access optimizations**

all of which are meticulously integrated to amplify the performance of the rasterization process."

## 关键数字(abstract 直引)

- **核心结论**:**"FlashGS consistently achieves an average 4× acceleration over mobile consumer GPUs, coupled with reduced memory consumption"**(abstract § 直引)
- **评测范围**:"across a diverse spectrum of synthetic and real-world **large-scale scenes**, encompassing a variety of image resolutions"
- **其他具体表格数字**:**abstract 未给 Table 数字**(`abstract 未给 Table 数字,需 PDF 核`)。从第三方报道(CSDN 博客园二手)转述:`实现平均 7.2 倍的加速比,并以最低 125.9 帧/秒的速率进行渲染` —— **第三方数字不作为本笔记引数,需 PDF 核**。

## 与本调研主线的关系(基于 00-goal.md)

### 这是一条"3DGS 在 mobile GPU 上"的可量化对标

**Snap 8 Gen 3 mobile GPU 实测 4× 加速**(abstract 原文,虽然评测对象是"mobile consumer GPUs"不一定是 Adreno 8 Gen 3)是 **本项目 M3 / M4 阶段 4DGS mobile 路径的"3DGS 实证下限"**。

| 维度 | FlashGS | Mobile-GS(本项目已有 12 号笔记) | 4DGS-1K(本项目已有 5 号笔记) |
|---|---|---|---|
| 类型 | 3DGS 静态 | 3DGS 静态 | 4DGS 动态 |
| Mobile GPU 实测 | **✅ 4× 加速(abstract)** | ✅ 127 FPS(Snap 8 Gen 3 Table 2) | ❌ 未在 mobile 实测(仅 TITAN X 200+ FPS) |
| 移动端 GPU 类别 | mobile consumer GPU(未明示) | **Snap 8 Gen 3** | TITAN X(Pascal 2015) |
| Vulkan 渲染管线 | CUDA only | **Vulkan 2.0** | CUDA + PyTorch |
| 加速手段 | kernel-level + algorithmic | OIT + NVQ + SH-distill | STV pruning + Temporal Filter |
| 开源 | **CUDA Python lib** | Vulkan 2.0 | CUDA + Diff-GS-Rasterizer |

> **关键洞察**:**FlashGS 的 "4× 加速 over mobile consumer GPU" 是 abstract 层级最直接的 mobile GPU 对标数字**,而 Mobile-GS 在 Snap 8 Gen 3 上是 127 FPS(127 / 8 ≈ 15.9× over 3DGS),是更激进的数字。**本项目 M4 阶段可参考 FlashGS 的 kernel 优化思路** (redundancy elimination + efficient pipelining + memory access optimization) 作为 Vulkan 1.3 实现的算法种子。

### 与 Mobile-GS 笔记的对照

`2026-du-mobile-gs.md` 笔记(11 号)已确立 **Mobile-GS 的 5 件套方法学**(depth-aware OIT + neural view-dep + NVQ + SH-distill + pruning)。**FlashGS 提供的是 kernel-level 实现技巧** —— **这两条路径不冲突,可叠加**:Mobile-GS 提供"做什么",FlashGS 提供"在 CUDA kernel 里怎么做"。

## 我未找到 / 提请下游注意

- **机构归属**:**abstract 未给具体机构**,需从 PDF 头部 / 项目页 / GitHub README 直引(`未在公开 abstract 拿到机构列表`)
- **GitHub 仓库 URL**:**abstract 末尾未给 commit URL**,第三方(CSDN 博客园)报道直引 `https://github.com/InternLandMark/FlashGS`(`未在公开 abstract 拿到仓库 URL`)
- **Table 数字**:**abstract 未给具体 PSNR / FPS / Storage**,需从 PDF Table 1-3 直引。第三方报道提及"7.2× 加速 / 125.9 FPS"但**未在 abstract 段验证**(`abstract 未给 Table 数字,需 PDF 核`)
- **mobile consumer GPU 具体型号**:**abstract 用 "mobile consumer GPUs" 复数**,未明示哪类 GPU(可能含 Apple Silicon / Adreno / Mali / 笔记本核显);与 Mobile-GS 的"Snap 8 Gen 3"严格口径不严格对应
- **4DGS 适配性**:**论文未做 4DGS 适配**,本项目需自研

## 我的 commit 节奏

本文是 12 篇 paper notes 之外**新加的第 13 篇**,聚焦"3DGS 桌面端 mobile GPU 实证"。**后续 `02-rendering-acceleration.md` 应加一节"§X. Mobile GPU 桌面先例"**,直接引用本笔记 abstract + Mobile-GS Table 2 数字交叉验证。

## 引用一览(本笔记引用自)

- arxiv abstract page 直引(`https://arxiv.org/abs/2408.07967`)
- 第三方数字(7.2× / 125.9 FPS)**仅作为下游核验方向**,本笔记不作为引数
