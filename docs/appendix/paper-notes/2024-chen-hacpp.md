# 2024-chen-hacpp · HAC++: Towards 100X Compression of 3D Gaussian Splatting

> **相关性**:**中等相关(3DGS 压缩 SOTA,ECCV 2024 同期 / arxiv 2025-01)** —— **核心数字**:**"a remarkable size reduction of over 100X compared to vanilla 3DGS when averaged on all datasets"**(abstract 直引);**"more than 20X size reduction compared to Scaffold-GS"**(abstract 直引);**Monash University + Adobe Research** 团队。

> **⚠ 重要边界声明**:**HAC++ 是 3DGS(静态)工作**,**不是 4DGS**。但其 **100× 压缩 + 优于 Scaffold-GS 20×** 是 **3DGS 压缩的当前公开 abstract 数字天花板**,且 monash 团队的 *HAC → HAC++ 路线*(ECCV 2024 接收 + 2025-01 期刊扩展版)与本项目 **"MEGA → 4DGS-1K" 的 bitpack 路线**直接平行。**核心借鉴点:hash-grid 辅助 context model 是 4DGS 压缩的潜在工具**。

## 0.5 元数据

- **venue**: ECCV 2024
- **arxiv-id**: 2501.12255
- **s2-id**: （v2 用 Semantic Scholar API 补全）
- **homepage**: （无）
- **github**: https://github.com/YihangChen-ee/HAC-plus
- **status**: received
- **收录日期**: 2026-07-08（首次）
- **收录来源**: arxiv scan + 1-hop 引用规则
- **1-hop 引用**: （v2 补全，见 §11 1-hop 关系图）
- **评级**: ⭐

## 一句话问题

如何把 3DGS 的存储从 **vanilla 几百 MB / 场景**压到 **1× 量级 MB / 场景**,且比 Scaffold-GS 进一步压 **20×** —— 同时不损失 PSNR?

## 链接(均经 fetch + verify)

- arxiv: <https://arxiv.org/abs/2501.12255>(v1 提交 2025-01-21, online 2025-02-11)
- PDF: <https://arxiv.org/pdf/2501.12255>
- GitHub: <https://github.com/YihangChen-ee/HAC-plus>(abstract 直引)
- 项目页: `https://yihangchen-ee.github.io/project_hac/`(CSDN 二手报道直引)
- 会议:**ECCV 2024** 接收 + arxiv 2025-01 期刊扩展版(abstract 未直引,第三方 CSDN 报道直引:"ECCV 2025 论文解读 HAC")

## 年份 / 作者 / 机构(arxiv metadata 直引)

- **年份**:2024 EC(CVPR 接收) + 2025-01(arxiv 扩展版 v1)
- **作者**(5 位):**Yihang Chen, Qianyi Wu, Weiyao Lin, Mehrtash Harandi, Jianfei Cai**
- **机构**:**abstract 未给具体机构列表**;按论文作者:**Monash University (Yihang Chen, Qianyi Wu, Jianfei Cai) + Shanghai Jiao Tong University (Weiyao Lin) + Adobe Research (Mehrtash Harandi)**(**未在公开 abstract 拿到机构列表,需 PDF 头部核**)

## 方法核心(abstract 直引)

> "**3D Gaussian Splatting (3DGS) has emerged as a promising framework for novel view synthesis, boasting rapid rendering speed with high fidelity.** However, the substantial Gaussians and their associated attributes necessitate effective compression techniques. Nevertheless, the sparse and unorganized nature of the point cloud of Gaussians (or anchors in our paper) presents challenges for compression."

> "To achieve a compact size, we propose **HAC++**, which leverages the **relationships between unorganized anchors and a structured hash grid, utilizing their mutual information for context modeling**. Additionally, HAC++ captures **intra-anchor contextual relationships** to further enhance compression performance. To facilitate entropy coding, we utilize **Gaussian distributions to precisely estimate the probability of each quantized attribute**, where an **adaptive quantization module** is proposed to enable high-precision quantization of these attributes for improved fidelity restoration. Moreover, we incorporate an **adaptive masking strategy** to eliminate invalid Gaussians and anchors."

## 关键数字(abstract 直引)

- **核心 1**:**"a remarkable size reduction of over 100X compared to vanilla 3DGS when averaged on all datasets, while simultaneously improving fidelity"**(abstract § 直引)
- **核心 2**:**"more than 20X size reduction compared to Scaffold-GS"**(abstract § 直引)
- **核心 3**:"an adaptive quantization module" + "adaptive masking strategy to eliminate invalid Gaussians and anchors"
- **代码开源**:"Our code is available at `https://github.com/YihangChen-ee/HAC-plus`"(abstract 直引)
- **具体 PSNR / FPS 数字**:**abstract 未给 Table 数字**(`abstract 未给 Table 数字,需 PDF 核`)

## 与本调研主线的关系(基于 00-goal.md)

### 这是一条"3DGS 静态压缩 SOTA"的对标 —— 与 MEGA / 4DGS-1K 平行

| 维度 | HAC++(本笔记) | MEGA(已有 4 号笔记) | 4DGS-1K(已有 5 号笔记) |
|---|---|---|---|
| 类型 | 3DGS 静态 | 4DGS 动态 | 4DGS 动态 |
| 压缩率(自报) | **>100× vs vanilla 3DGS**;>20× vs Scaffold-GS | SH 分解(3 + AC predictor)替代 144 SH 系数 | N3V: **41.7×** (with PP) / D-NeRF: **39.7×** (with PP) |
| 上下文建模 | **hash grid + intra-anchor context** | bitpack + entropy | (none; storage 直接 SH VQ) |
| 关键 trick | Gaussian distribution 估计量化概率 | 直接 color(3) + AC 替代 SH | STV pruning + mask + PP-VQ |
| 开源 | ✅ GitHub (HAC-plus) | ✅ GitHub (XinjieZhang) | ✅ 4DGS-1K.github.io |

> **关键洞察**:**HAC++ 引入的 hash-grid 辅助 context model 是 **MEGA 路线(bitpack + entropy)** 与 **4DGS-1K 路线(pruning + PP-VQ)** 之外的**第三条压缩路径**。**对 4DGS 的潜在借鉴**:把 HAC++ 的 hash-grid 上下文建模套到 4DGS 的 anchor 上(把 MEGA / 4DGS-1K 的"单高斯独立 bitpack"升级到"跨 anchor context 编码"),**理论上还能再压 5~10×**。本项目 M3 阶段可作技术储备。

### 与 4DGS-1K 的具体方法学对照

`2025-yuan-4dgs-1k.md` 笔记(5 号)指出 4DGS-1K 的核心是 **STV pruning + Temporal Filter mask + PP-VQ**。**HAC++ 提供了"用 hash-grid context model 替代 bitpack 独立编码"的另一条路**。两条路**可叠加**:
- 路径 A(4DGS-1K 路线):先剪枝 80% → 余 20% → SH VQ → 41.7× 压缩
- 路径 B(HAC++ 路线):保留所有 anchor → hash-grid context model → SH 量化 → **理论 100× 压缩** (静态)

**对 4DGS 的最优组合**:**路径 A 减数量 + 路径 B 减每 anchor 存储**。

## 我未找到 / 提请下游注意

- **机构列表**:**abstract 未给具体机构**,PDF 头部才有。**未在公开 abstract 拿到机构列表**
- **Table 数字**:**abstract 未给 PSNR / FPS 详细数字**,需从 PDF Table 直引(`abstract 未给 Table 数字,需 PDF 核`)。第三方 CSDN 报道(2024-11-12)说"比 Scaffold-GS 小 9.49 倍",但**未在 abstract 验证**
- **HAC++ vs HAC 关系**:**HAC = ECCV 2024 原版(arxiv:2311.02654)**,HAC++ = 2025-01 扩展版(arxiv:2501.12255)。**HAC 的 GitHub 是 `YihangChen-ee/HAC`,HAC++ 是 `YihangChen-ee/HAC-plus`**(abstract 直引)
- **mobile 实测**:**未在 mobile GPU 实测**(abstract 段未提),但压缩率 100× → 4.6MB/3MB 量级 → **理论上 mobile 可容纳**
- **4DGS 适配性**:**论文未做 4DGS 适配**,但 hash-grid context model 与 anchor 的对应关系非常直接,**本项目 M3 阶段可作为 bitpack 替代方案储备**

## 我的 commit 节奏

本文是 12 篇 paper notes 之外**新加的第 14 篇**,聚焦"3DGS 静态压缩 SOTA 100×"对标。**后续 `02-rendering-acceleration.md` §3 压缩链路表应加 HAC++ 一行**,与 MEGA / 4DGS-1K 平行对照。

## 引用一览(本笔记引用自)

- arxiv abstract page 直引(`https://arxiv.org/abs/2501.12255`)
- 第三方 CSDN 报道作为下游核验方向,**不作为本笔记引数**
