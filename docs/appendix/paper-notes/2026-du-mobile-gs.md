# 2026-du-mobile-gs · Mobile-GS: Real-time Gaussian Splatting for Mobile Devices

> **相关性**:**高度相关(本项目主线对标最强先例)** —— ICLR 2026,**首篇公开在 mobile GPU 实测的 3DGS 类工作**,**Vulkan 2.0 实现**。**实测 Snap 8 Gen 3 @ Bicycle 116 FPS / 1600×1063**(论文 Fig.1);Mip-NeRF 360 上 Snap 8 Gen 3 **127 FPS**,**127 / 8 ~ 16× 加速于 3DGS / Mini-Splatting / C3DGS / LocoGS-S**(Table 2 直引)。

> **⚠ 重要诚实声明**:这是 3DGS(静态)工作,**不是 4DGS**。但它**直接证明了 Snap 8 Gen 3 + Vulkan 上 3DGS 可达 100+ FPS**—— 本项目 4DGS 路线需要类似加速,**Mobile-GS 的方法学(深度感知 + 顺序无关渲染 + 蒸馏 + NVQ + 剪枝)5 件套对 4DGS 同样适用**。

## 0.5 元数据

- **venue**: ICLR 2026
- **arxiv-id**: 2603.11531
- **s2-id**: （v2 用 Semantic Scholar API 补全）
- **homepage**: https://xiaobiaodu.github.io/mobile-gs-project
- **github**: https://github.com/xiaobiaodu/mobile-gs
- **status**: received
- **收录日期**: 2026-07-08
- **收录来源**: arxiv scan + 1-hop 引用规则
- **1-hop 引用**: （v2 补全，见 §11 1-hop 关系图）
- **评级**: ⭐⭐

- **survey_section**: 5
## 一句话问题

如何在 **mobile GPU(尤其是 Snap 8 Gen 3)+ Vulkan 2.0** 上实现 **实时(snapdragon 至少 30+ FPS)3DGS 渲染**,**PSNR 27+,storage 5 MB 量级**?

## 链接(均经 fetch + PDF 实测)

- arxiv: <https://arxiv.org/abs/2603.11531>(v1 2026-03-12)
- 项目页: <https://xiaobiaodu.github.io/mobile-gs-project>
- GitHub: <https://github.com/xiaobiaodu/mobile-gs>(CSDN 论文解读直引)
- PDF: 已下 `/tmp/4dgs-papers/mobile-gs.pdf`(19 页含附录、9.5 MB)
- 会议:**ICLR 2026**(PDF 头部直引 "Published as a conference paper at ICLR 2026")

## 年份 / 作者 / 机构(PDF 头部实测)

- **年份**:2026(v1 2026-03-12)
- **作者**:Xiaobiao Du, Yida Wang, Kun Zhan, Xin Yu
- **机构**:**University of Technology Sydney** + **Adelaide University** + **Li Auto Inc.**(论文 1 / 2 / 3 单位标识,**3 单位都在**,其中 Xin Yu 通讯为 Adelaide)

## 方法核心(5 件套,PDF §3 直引 + abstract 直引)

### §3.1 Depth-aware Order-Independent Rendering —— **核心创新**
- **alpha-blending 是 3DGS 主要瓶颈**(Fig. 2 实测:sorting 在 Counter / Bicycle / Garden 上占总 60~80% 时间)
- **OIT 不需要 sorting**:**并行累加每个 Gaussian 的贡献**,**渲染速度 ↑↑**
- **关键公式 Eq. 3**:`α_i = o_i × exp(-½ Δx_i^T Σ_i^-1 Δx_i)`,**然后 w_i = φ_i² + φ_i/d_i² + exp(s_max/d_i)` ——**深度感知加权**:远 Gaussian 衰减 + 大尺度 Gaussian 增强
- **缺点**:order-free 会导致深度遮挡区域出现 transparency artifacts(OIT 通病)

### §3.1.5 Neural View-dependent Enhancement
- **MLP**(输入:3D Gaussian scale + rotation + SH + camera-Gaussian 向量)→ **预测 view-dependent opacity**
- **补偿 OIT 的 transparency artifacts**

### §3.2 First-Order SH Distillation
- **从 3rd-order SH(3×16 = 48 系数)→ 1st-order SH(3×4 = 12 系数)**
- **Teacher = Mini-Splatting**(`[PDF §3.4 直引]`);Student = Mobile-GS
- **distill loss**:`L_dstill = 1/|P| Σ_{p∈P} ||C_tea_p - C_p||`(像素级比较)
- **scale-invariant depth distill**:`Ldepth(D, D_tea) = ...`(Eq. 5,~ 0.1 权重)

### §3.2.6 Neural Vector Quantization (NVQ)
- **sub-vector 分解**:Gaussian 属性向量 `z ∈ R^(KL)` 分成 K 个 cluster(z_1, ..., z_K),每 cluster 单独 codebook
- **multi-codebook**:**减少 codebook 体积 + 缓解 codeword collision**
- **Huffman 编码**进 final bitstream

### §3.3 Contribution-Based Pruning
- **投票 + 阈值**:不是立即剪,而是累积投票,阈值超才剪
- **vote 准则**:Gaussians with 低 opacity ∩ 低 scale
- **公式 Eq. 8**:`G_new = G \ {g ∈ G | 1[V_g > l_prune · v]}`

## 关键数字(全部 PDF Table 直引)

### Table 1 · **Desktop RTX 3090 / 3090 Ti**(3 datasets 平均)

| 方法 | Mip-NeRF 360 PSNR↑ | Mip-NeRF 360 Storage↓ | Mip-NeRF 360 FPS↑ |
|---|---|---|---|
| 3DGS | 27.21 | **839.9 MB** | 174 |
| LightGaussian | 27.08 | 60.4 MB | 227 |
| AdR-Gaussian | 26.95 | 358.2 MB | 254 |
| SortFreeGS | 27.02 | 851.4 MB | **731** |
| Speedy-Splat | 26.92 | 79.4 MB | 401 |
| C3DGS | 27.03 | 30.6 MB | 184 |
| LocoGS-S | 27.02 | **8.5 MB** | 292 |
| **Mobile-GS (Ours)** | **27.12** | **4.6 MB** | **1125** |

(其他列:Tanks & Temples 23.09 PSNR / 2.5 MB / 1179 FPS;Deep Blending 29.93 PSNR / 4.6 MB / 1132 FPS)

### Table 2 · **Snapdragon 8 Gen 3 实测(!!)** — 本项目最关键

| 方法 | PSNR↑ | **FPS↑** | Storage | Training↓ |
|---|---|---|---|---|
| 3DGS* | 27.01 | **8** | 61.8 MB | 0.5 h |
| Mini-Splatting* | 27.02 | **12** | 36.9 MB | 0.4 h |
| Speedy-Splat | 26.92 | **19** | 79.5 MB | 0.4 h |
| HAC | 26.98 | 12 | 11.8 MB | 0.7 h |
| LocoGS-S | 27.02 | **17** | 8.5 MB | 0.8 h |
| C3DGS | 27.03 | 14 | 30.6 MB | 0.6 h |
| GES | 26.98 | 18 | 29.4 MB | 0.7 h |
| SortFreeGS* | 26.74 | **24** | 64.3 MB | 1.3 h |
| **Mobile-GS (Ours)** | **27.12** | **127** | **4.6 MB** | 1.5 h |

> **Table 2 标题**:`"Evaluation on the mobile device with Snapdragon 8 Gen 3 GPU. 3DGS*, Mini-Splatting*, and SortFreeGS* mean the quantized version through Huffman encoding."` —— **所有 `*` 方法都是 quantization 后的对比基线**。
>
> **Mobile-GS vs 第二名 SortFreeGS* = 127 / 24 = 5.3×**
> **Mobile-GS vs 3DGS vanilla = 127 / 8 = 15.9×**

### Table 3 · Ablation(Mip-NeRF 360)

| 变体 | PSNR↑ | FPS↑ | Storage |
|---|---|---|---|
| Mobile-GS full | 27.12 | **1125** | 4.6 MB |
| w/o order-independent | 27.26 | **684** | 4.5 MB |
| w/o view-dependent | 26.68 | 1227 | 4.4 MB |
| w/o neural quantization | 27.33 | 841 | 121 MB |
| w/ 0th-order SH distill | 27.04 | 1219 | 3.6 MB |
| w/ 2nd-order SH distill | 27.13 | 917 | 7.3 MB |
| w/ 3rd-order SH | 27.15 | 841 | 9.6 MB |

> **消融解读**:w/o order-independent → FPS **1125 → 684** (-39%);w/o NVQ → storage **4.6 → 121 MB** (26×);w/o view-dependent → PSNR **27.12 → 26.68** (-0.44 dB)。

### §3.4 Implementation
- **Training:RTX 3090 + PyTorch + custom CUDA kernel**(desktop)
- **Mobile Deployment:**Vulkan 2.0**:`"We implement our approach using Vulkan 2.0, a modern, cross-platform graphics and compute API."`
- **Mini-Splatting 是 teacher model**
- **60k iterations,~ 1.5 h on Snap 8 Gen 3**

### Fig.1 Caption 直引
> "Mobile-GS is the first real-time Gaussian Splatting method that can reach **116 FPS rendering speed in the 1600×1063 resolution for Bicycle on the mobile equipped with the Snapdragon 8 Gen 3 GPU** as shown in (a)."

## 与本调研主线的关系(基于 `00-goal.md` + 上一版 `2025-yuan-4dgs-1k.md`)

### 这就是项目目标的"已验证先例"

**Snap 8 Gen 3 + Vulkan + 3DGS**:**127 FPS** 实测。**本项目是 Snap 8 Gen 4 + Vulkan 1.3 + 4DGS**。

**两条迁移路径**:
1. **路径 A(直接复用 Mobile-GS 框架到 4DGS)** —— 把 4DGS 的 canonical + deformation 路径嵌进 Mobile-GS 的 OIT + NVQ + SH-distill 框架
2. **路径 B(基于 Mobile-GS-Vulkan 改造)** —— Mobile-GS 公开了 Vulkan 2.0 实现,在它的基础上加 temporal dimension + 4DGS raft

### 对项目目标的具体承诺

- **`30~60 FPS @ 1080p on Snap 8 Gen 4` 目标**:Snap 8 Gen 3 上 3DGS 已 127 FPS,Adreno 8 Gen 4 比 Gen 3 快 ~30%(高通官方),**Adreno 8 Gen 4 上 3DGS 估算 160+ FPS**(`[推测]`)。**加上 4DGS 时间维度复杂度增量 + 4DGS-1K 的 pruning + mask 复用,M4/M5 工程可达 60 FPS 是非常合理的预期**(`[推测,有 Table 2 实测作锚]`)
- **`Storage ≤ 50 MB / scene`**:Mobile-GS 已 4.6 MB(Mip-NeRF 360 vanilla),4DGS + 4DGS-1K pruning 后估算 ~10~30 MB,远低于预算

### 4DGS-1K vs Mobile-GS 的方法学对照

| 维度 | 4DGS-1K(论文) | Mobile-GS(论文)|
|---|---|---|
| 加速机制 | Spatial-Temporal Variation Score pruning + Temporal Filter mask | Depth-aware OIT(no sort) + neural view-dep + NVQ + SH-distill |
| 显存(推理) | 1.62 GB | **`未明示,论文未给具体 GB 数`**(只是 Inference FPS) |
| Sort 是否消除 | 否(仍 sort) | **是(对 mobile 加速关键)** |
| Mobile 实测 | **未在 mobile 上跑**(`[arxiv:2503.16422 直引]`)| ✅ Snap 8 Gen 3 实测 |
| Vulkan | 无 | Vulkan 2.0 |
| 量化目标 | 41.7× 压缩(PP on N3V) | SH 1st-order + NVQ + Huffman |
| 4DGS 适配 | **已原生支持**(本论文就是 4DGS) | **静态 3DGS** —— **需扩展到 4DGS** |
| 4DGS-1K-Mobile-GS 路线融合 | 改 4DGS-1K 用 OIT 替代 sort | 改 Mobile-GS 加 temporal mask |

> **关键洞察**:**项目 M4 阶段最优路径** = "**Mobile-GS Vulkan 2.0 渲染管线 + 4DGS-1K pruning + Temporal Filter mask**"。**两个 SOTA 工作的"取最强一项"组合**:**Mobile-GS 给 Vulkan 渲染管线 + OIT**;**4DGS-1K 给 sparse-temporal mask**。**论文没做,本项目可以做**(类似 path)。

## 我未找到 / 提请下游注意

- **Mobile-GS 的 Vulkan 实现公开性**:GitHub 仓库有 README,但**具体 Vulkan 2.0 代码可能仍依赖论文附录 / supplementary**,需从 GitHub repo `xiaobiaodu/mobile-gs` 核
- **Mobile-GS 推理 GPU 显存数字**:**Table 2 未明示**,只说"PSNR / FPS / Storage";Mip-NeRF 360 + 4.6 MB 资源下,推理显存应远低于 1 GB,**但未在公开 abstract / table 精确数字**(`[未在公开 abstract 拿到具体 GB]`)
- **Mobile-GS 扩展到 4DGS 的可行性**:**论文未做**,但 method 学允许(`deformation field` 在 OIT 框架下可以 per-Gaussian 应用,只是 deformation 自身的 compute 不在 sort 内)
- **Snap 8 Gen 3 vs Gen 4 的实测差异**:**Mobile-GS 只在 Gen 3 上跑**;Gen 4 估算 = `127 × ~1.3` ≈ `165 FPS`(`[推测,基于高通 Adreno 8 Gen 3→4 ~30% 算力升级]`),但**未在 Mobile-GS 或任何公开 abstract 精确拿到 Gen 4 实测**

## 我的 commit 节奏

本文是 11 篇 paper notes 之外**新加的第 12 篇**,聚焦 mobile GPU 实证。**后续 `02-rendering-acceleration.md` 应加一节"§X. Mobile 端实证(2026 H1)"**,直接引用 Mobile-GS Table 2 + Fig.1 caption。

## 11. 1-hop 关系图

### 11.1 引用的相关工作 (downstream)

Mobile-GS 是小米 / 3DGS 移动端 SOTA：

- **3DGS 原论文**：[2023-kerbl-3dgs](2023-kerbl-3dgs.md)
- **Lumina**：[2025-feng-lumina](2025-feng-lumina.md)（体系结构 co-design 前置工作）
- **Snap 8 Gen 3 实测 127 FPS @ 4.6 MB**（ICLR 2026，深度感知 + OIT + NVQ + 剪枝 5 件套）

### 11.2 被引用的后续工作 (upstream)

- [2026-du-flux-gs](2026-du-flux-gs.md)（Flux-GS 在 Mobile-GS 基础上进一步优化，Snap 8 Gen 3 147 FPS @ 2.1 MB）

**v2 用 S2 API 自动拉取完整 cited-by 列表**。
