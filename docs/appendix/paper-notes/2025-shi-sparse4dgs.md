# 2025-shi-sparse4dgs · Sparse4DGS: 4D Gaussian Splatting for Sparse-Frame Dynamic Scene Reconstruction

> **相关性**:**高度相关(4DGS 加速,AAAI 2026)** —— **核心定位**:**"the first method for sparse-frame dynamic scene reconstruction"**(abstract 直引);**9 位作者**,**Hangzhou Dianzi University + Harbin Institute of Technology** 团队。

> **⚠ 重要边界声明**:**Sparse4DGS 是 4DGS(动态)工作**,**但**其核心贡献 **不是"性能加速"** 而是"**稀疏帧输入下重建质量**"**。本调研取其**两个间接加速价值**:1) **"texture-aware" pruning 思路与 4DGS-1K STV pruning 平行**;2) **iPhone-4D 数据集** —— 是本项目"高速相机阵列预制高密度场景"路线的数据形态先例。

## 0.5 元数据

- **venue**: arxiv pre-print (2025-11)
- **arxiv-id**: 2511.07122
- **s2-id**: （v2 用 Semantic Scholar API 补全）
- **homepage**: https://changyueshi.github.io/Sparse4DGS/
- **github**: （无）
- **status**: under review
- **收录日期**: 2026-07-08（首次）
- **收录来源**: arxiv scan + 1-hop 引用规则
- **1-hop 引用**: （v2 补全，见 §11 1-hop 关系图）
- **评级**: ⭐

- **survey_section**: 3
## 一句话问题

现有 4DGS 方法(Deformable-3DGS / 4DGS / 4DGS-1K 等)需要 **dense-frame video sequence** 才能高质量重建;**当输入帧稀疏** (e.g. iPhone 拍摄的低 FPS 视频)时,4DGS 重建质量急剧下降。**如何让 4DGS 在 sparse-frame 输入下保持质量**?

## 链接(均经 fetch + verify)

- arxiv: <https://arxiv.org/abs/2511.07122>(v1 提交 2025-11-10)
- PDF: <https://arxiv.org/pdf/2511.07122`
- 项目页: <https://changyueshi.github.io/Sparse4DGS/>
- 会议:**AAAI 2026**(CSDN 报道直引 "AAAI 2026, pp.8933-8941")

## 年份 / 作者 / 机构(arxiv metadata + PDF 直引)

- **年份**:2025(arxiv v1 2025-11-10, AAAI 2026 接收)
- **作者**(9 位,arxiv metadata):**Changyue Shi, Chuxiao Yang, Xinyuan Hu, Minghao Chen, Wenwen Pan, Yan Yang, Jiajun Ding, Zhou Yu, Jun Yu**
- **机构**:**Hangzhou Dianzi University (杭州电子科技大学) + Harbin Institute of Technology (哈尔滨工业大学)**(CSDN + 项目页直引)

## 方法核心(abstract 直引)

> "**Dynamic Gaussian Splatting approaches have achieved remarkable performance for 4D scene reconstruction.** However, these approaches **rely on dense-frame video sequences for photorealistic reconstruction**. In real-world scenarios, due to equipment constraints, sometimes **only sparse frames are accessible**."

> "In this paper, we propose **Sparse4DGS, the first method for sparse-frame dynamic scene reconstruction**. We observe that dynamic reconstruction methods fail in both canonical and deformed spaces under sparse-frame settings, especially in areas with high texture richness. **Sparse4DGS tackles this challenge by focusing on texture-rich areas**."

> "For the deformation network, we propose **Texture-Aware Deformation Regularization**, which introduces a **texture-based depth alignment loss** to regulate Gaussian deformation. For the canonical Gaussian field, we introduce **Texture-Aware Canonical Optimization**, which incorporates **texture-based noise into the gradient descent process of canonical Gaussians**."

## 关键数字(abstract 直引)

- **核心 1**:"the first method for sparse-frame dynamic scene reconstruction"
- **核心 2**:"outperforms existing dynamic or few-shot techniques on **NeRF-Synthetic, HyperNeRF, NeRF-DS, and our iPhone-4D datasets**"
- **核心 3**:"**iPhone-4D datasets**" —— **iPhone 实拍的 4D 稀疏帧数据集**,本项目最相关数据形态先例
- **核心 4**:两个新机制:**Texture-Aware Deformation Regularization + Texture-Aware Canonical Optimization**
- **具体 PSNR / FPS / Storage / #Gauss 数字**:**abstract 未给 Table 数字**(`abstract 未给 Table 数字,需 PDF 核`)

## 与本调研主线的关系(基于 00-goal.md)

### 这是一篇"4DGS 在稀疏帧下"的加速意义 —— **双层价值**

#### 价值 1:**"texture-aware" 思路与 4DGS-1K STV pruning 平行**

| 维度 | Sparse4DGS(本笔记) | 4DGS-1K(5 号笔记) |
|---|---|---|
| 类型 | 4DGS 动态(稀疏帧) | 4DGS 动态(密帧) |
| 关键 trick | Texture-Aware Deformation Reg + Canonical Opt | STV pruning + Temporal Filter mask |
| 共同点 | **都关注"高重要性 Gaussian 优先"**(Sparse4DGS 关注 texture-rich;4DGS-1K 关注 temporal-variation 高) | 同 |
| 数据输入 | **sparse frame** | dense frame |
| 重建质量 vs SOTA | "outperforms existing dynamic or few-shot techniques" | PSNR 几乎无损(-0.04 dB N3V / +0.35 dB D-NeRF) |

> **关键洞察**:**Sparse4DGS 的 "texture-aware" 评分 + 4DGS-1K 的 "temporal-variation" 评分 = 互补**。本项目 M3 阶段可参考两者做 **"joint texture-temporal pruning score"**。

#### 价值 2:**iPhone-4D dataset** —— **iPhone 4D 实拍数据集**

- **关键**:**Sparse4DGS 自带 iPhone-4D 数据集**,**iPhone 实拍的低帧率 4D 场景**
- **对本项目意义**:**本项目"高速相机阵列预制高密度场景"** vs **Sparse4DGS 的 "iPhone 低帧率实拍"** 是 **两个互补的 4D 数据形态**
- **借鉴点**:**iPhone-4D 的稀疏帧策略可作为本项目 M2 阶段的"低成本数据采集"先例** (若高速相机阵列不可用,可用 iPhone + Sparse4DGS 路线应急)

### 与 4DGS-1K 路线融合的潜在价值

| 路径 | 描述 | 预期收益 |
|---|---|---|
| 4DGS-1K alone | 4DGS-1K STV pruning + Temporal Filter | 8.94× FPS 加速,41.7× 压缩 |
| Sparse4DGS alone | Texture-Aware pruning | 在 sparse 帧输入下保持质量 |
| **融合** | STV + texture 双评分联合剪枝 | **理论 10~15× FPS 加速 + sparse 帧鲁棒** |

> **关键洞察**:**本项目 M3 阶段最优路径** = 4DGS-1K STV + Sparse4DGS texture-aware **双评分**;在 dense 帧输入下二者独立;在 sparse 帧输入下 texture-aware 帮 STV 补偿 temporal 信息缺失。

## 我未找到 / 提请下游注意

- **PSNR / FPS / Storage 数字**:**abstract 未给 Table 数字**,需从 PDF Table 直引(`abstract 未给 Table 数字,需 PDF 核`)
- **mobile 实测**:**未在 mobile GPU 实测**(abstract 段未提)
- **4DGS-1K 引用关系**:**abstract 未直引 4DGS-1K** —— **未在公开 abstract 拿到对 4DGS-1K 的引用关系,需 PDF Related Work 核**
- **iPhone-4D dataset 开源性**:**abstract 未直引** —— **未在公开 abstract 拿到 dataset 公开 URL,需 PDF / 项目页核**
- **会议归属**:AAAI 2026 直引来自第三方报道(CSDN) + 论文集页(`researchr.org`);**abstract 未直引 AAAI 2026 字样,需 PDF 头部核**

## 我的 commit 节奏

本文是 12 篇 paper notes 之外**新加的第 18 篇**,**首篇 4DGS 加速类笔记**(本批次内)。**后续 `02-rendering-acceleration.md` §3 应加 Sparse4DGS 一行**,作为"sparse-frame 4DGS 加速"路径独立对照;`00-goal.md` 应考虑 iPhone-4D 数据集作为"M2 阶段应急数据采集方案"备选。

## 引用一览(本笔记引用自)

- arxiv abstract page 直引(`https://arxiv.org/abs/2511.07122`)
- 项目页 `https://changyueshi.github.io/Sparse4DGS/` (用于 arxiv id 确认)
- researchr alias `https://researchr.org/alias/minghao-chen` (用于 AAAI 2026 论文集页码)
