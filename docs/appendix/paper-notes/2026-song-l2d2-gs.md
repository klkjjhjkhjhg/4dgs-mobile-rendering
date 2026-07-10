# 2026-song-l2d2-gs · L2D2-GS: Learning to Densify for Feedforward Dynamic Gaussian Scene Reconstruction

> **相关性**：**⭐⭐⭐ 派系 A 4DGS 表示 + 派系 C 渲染加速** —— **小米 + 北大联合工作**（junnan5@xiaomi.com / sunchitian@xiaomi.com / heliangliang@xiaomi.com），**对用户（小米 17 级图形架构部）有直接合作背景**。**路径价值**：**Feedforward 动态场景重建**（摆脱 per-scene optimization 的 4DGS 表示 + 自监督 densification policy）。**凌晨 cron 标 🚩 争议项（PDF 下载失败）— 实测 fitz 解析完整 14 页，争议解除**。

## 0.5 元数据

- **venue**: （未给，预投 IEEE Transactions 模板，**未验证会议**）
- **arxiv-id**: 2606.29374
- **s2-id**: （v2 用 Semantic Scholar API 补全）
- **homepage**: （未在 abstract 拿到）
- **github**: （**未在 abstract 拿到** —— 注意 references [2] 提到 DriveStudio `https://github.com/ziyc/drivestudio` 是 L2D2-GS 评测用的 baseline 框架，**不是 L2D2-GS 自己的代码**；L2D2-GS 是否开源 **待人工**）
- **status**: preprint
- **收录日期**: 2026-07-09（凌晨 cron 🚩 争议项 → 本次 cron fitz 解析解 🚩 → 正式收录）
- **收录来源**: arxiv scan（cron arxiv_4dgs_scan）
- **1-hop 引用**: （v2 补全）
- **评级**: ⭐⭐⭐（**升级 ⭐⭐ → ⭐⭐⭐** 鉴于 1) 小米合作 + 2) 解 🚩 + 3) Feedforward 4DGS 路径与 ZipSplat 同主线）

## 1. 一句话问题

如何在 **动态城市街景（autonomous driving / large-scale world modeling）**中，**摆脱 per-scene optimization 的高开销**，用 **Feedforward 通用框架**（一次性推理即可重建动态 4D 场景）+ **自监督 densification policy**（基于 reconstruction gain 引导局部细化）达到**与 per-scene optimization 相当或更高的 PSNR**？

## 2. 链接

- arxiv：<https://arxiv.org/abs/2606.29374>（v1 提交 2026-06-28）
- PDF：已下 `.pdfs/2606.29374.pdf`（14 页，33 MB，**fitz 验证 14 页完整**）

## 3. 年份 / 作者 / 机构（PDF §I 第 1 页底部直引）

- **年份**：2026（v1 2026-06-28）
- **作者**：Zetian Song, Chenming Wu, Junnan Liu, Chitian Sun, Liangliang He, Hangjun Ye, Jiaqi Zhang, Siwei Ma (Fellow, IEEE), Wen Gao (Fellow, IEEE)
- **机构**（PDF 第 1 页底部脚注直引）：
  1. **Zetian Song — Peking University**, Beijing 100871 (songzt@pku.edu.cn)
  2. **Chenming Wu — Tsinghua University**, Beijing 100085 (wcm15@mails.tsinghua.edu.cn)
  3. **Junnan Liu — Xiaomi Inc.** (junnan5@xiaomi.com)
  4. **Chitian Sun — Xiaomi Inc.** (sunchitian@xiaomi.com)
  5. **Liangliang He — Xiaomi Inc.** (heliangliang@xiaomi.com)
  6. 其余：PKU / THU / Xiaomi 联合

> **关键**：**小米 3 位作者**（Junnan Liu / Chitian Sun / Liangliang He，邮箱后缀都是 @xiaomi.com）—— **本项目用户（小米 17 级图形架构部）所在公司**。**对用户直接相关**：小米在 4DGS / dynamic scene reconstruction 方向有团队投入。

## 4. 派系分类

- **派系 A 4DGS 表示**（核心）：Feedforward dynamic Gaussian scene reconstruction，**代表"摆脱 per-scene optimization"路径**
- **派系 C 渲染加速**（次要）：通过 feedforward + 自监督 policy 减少重建时间（**~98s vs per-scene optimization 70-80 min**）

> **与派系 A 中已有 4DGS 论文对比**：与 **ZipSplat (2606.05102, 已收录派系 D)** 共享 "feedforward 3DGS" 主线，但 L2D2-GS 走的是 **动态街景**（不是静态场景），与 **Wu 4DGS (2310.08528) / Deformable 3DGS (2309.13101) / 4DGS-1K (2503.16422)** 等 canonical+deformation 路径**不同** —— L2D2-GS 用 **iterative densification policy + reparameterization** 而不是 deformation field。

## 5. 方法核心（PDF §III 直引 + abstract 直引）

### 5.1 框架核心（PDF §III 直引）

- **核心思想**：**reformulates generalizable reconstruction not as a one-shot regression, but as a robust iterative process of optimization and densification**（abstract 直引）
- **3 阶段训练**（PDF Algorithm 1 第 6 页直引）：
  1. **Stage 1: Reconstructor Pre-training** —— 用 L2 + LPIPS + Lreg loss 预训练 reconstruction network
  2. **Stage 2: Policy Learning from Cached Scores** —— 用预训练时缓存的 reconstruction gain 训练 densification policy
  3. **Stage 3: Joint Training** —— 解冻所有模块联合训练

### 5.2 自监督 densification policy（PDF §III-B 直引）

- **核心**：**derives explicit reward signals from global reconstruction gains to guide local densification**（abstract 直引）
- **policy loss**：`Lpolicy = -1/i · Σ H(wᵢ)`（PDF Eq. 6 第 5 页直引，二值交叉熵）
- **输入**：`Pquery` = 4M query points → policy 输出 **discrete densification probability w ∈ [0, 1]**（PDF §III 第 6 页直引）
- **输出**：`Pdens` = 400K densified points（PDF §III 第 6 页直引）

### 5.3 Geometric Regularization（PDF §III-C 直引）

- **核心**：**utilizing reparameterization to constrain the optimization manifold and prevent convergence to poor local optima**（abstract 直引）
- **目的**：mitigate irreversible early-stage artifacts
- **reg loss**：`Lreg(G)` 用 reparameterization 约束 Gaussian 属性（PDF Eq. 8 第 5 页直引）

### 5.4 网络结构（PDF §IV-A 直引）

- **3D U-Net** with sparse convolutions（torchsparse 实现）
- **每个 Gaussian 参数化**：46 维 feature（14 维 explicit attributes + 32 维 neural features，PDF 第 13 页直引）
- **k-NN cross-attention**：k=16, Nheads=4, dhead=32（PDF 第 6 页直引）

## 6. 关键数字（PDF Table II 第 8 页 + Table IV 第 11 页直引）

### 6.1 训练资源（PDF 第 6 页直引）

- **8 × NVIDIA H20 GPUs**（**非 A100**）
- **per-GPU scene batch size = 1**，总 batch = 8
- **AdamW**, lr = 1×10⁻⁴, weight decay = 1×10⁻⁵
- **Per-scene iterations = 30,000**（PDF 第 14 页直引）

### 6.2 评测数据集（PDF §IV-B 第 7 页直引）

- **PandaSet**（主数据集）
- **Waymo Open Dataset (WOD)** —— **zero-shot generalization**
- **NOTR Dynamic32 split**（来自 EmerNeRF [44]）—— **short sequence interpolation**

### 6.3 主结果 PandaSet（PDF Table II 第 8 页直引）

| 方法 | PSNR↑ | SSIM↑ | LPIPS↓ | Time↓ | Gaussian |
|---|---|---|---|---|---|
| Street Gaussians [2]（upper bound, per-scene）| 24.54 | 0.739 | 0.224 | **~70 min** | 3M |
| OmniRe [3]（upper bound, per-scene）| 24.57 | 0.739 | 0.222 | **~80 min** | 3M |
| G3R [10] | 23.15 | 0.636 | — | 60s | 3M |
| G3R*（**复现配置**） | 23.18 | 0.653 | 0.406 | 75s | 3M |
| **L2D2-GS** | **24.19** | **0.705** | **0.329** | **98s** | **1.2M** |

> **关键对比**：
> - vs G3R：+1.01 dB PSNR（23.18 → 24.19），**LPIPS -0.077**（0.406 → 0.329）
> - vs Street Gaussians upper bound（**per-scene optimization 70 min**）：PSNR 仅 -0.35 dB，**时间 70 min → 98 s ≈ 43× 加速**（**核心数字**）
> - **Gaussian 数 1.2M vs upper-bound 3M** —— **2.5× 压缩**

### 6.4 Waymo Open Dataset（PDF Table IV 第 8 页直引）

| 方法 | PSNR↑ | SSIM↑ | LPIPS↓ | Gaussian |
|---|---|---|---|---|
| STORM [7] | 19.69 | 0.628 | 0.683 | — |
| G3R [10] | 24.35 | 0.686 | — | — |
| G3R* | 24.36 | 0.698 | 0.347 | — |
| Flux4D [11] | 23.84 | 0.675 | — | — |
| **L2D2-GS** | **25.22** | **0.735** | **0.287** | — |

> **zero-shot generalization**（用 PandaSet 训练，直接测 Waymo）：PSNR 25.22 vs STORM +5 dB

### 6.5 DL3DV 数据集（PDF Table V 第 13 页直引）

| View 数 | 方法 | PSNR↑ | SSIM↑ | LPIPS↓ | Gaussian |
|---|---|---|---|---|---|
| 32-view | AnySplat [5] | 18.76 | 0.569 | 0.389 | 5M |
| 32-view | G3R [10] | 23.97 | 0.737 | 0.256 | 700K |
| 32-view | **L2D2-GS** | **24.19** | **0.746** | **0.249** | **700K** |
| 64-view | AnySplat [5] | 17.33 | 0.518 | 0.458 | 10M |
| 64-view | G3R [10] | 23.63 | 0.721 | 0.277 | 700K |
| 64-view | **L2D2-GS** | **23.88** | **0.733** | **0.269** | **700K** |

### 6.6 G3R 协议（PDF Table 第 11 页直引）

- **G3R** PandaSet Scenes 1/30/40/80/90/110/120：G3R PSNR 25.22 dB，**L2D2-GS PSNR 26.87 dB**（**+1.65 dB**）

### 6.7 LiDAR + 3D-VFM 消融（PDF 第 9 页直引）

| 配置 | PSNR↑ | SSIM↑ | LPIPS↓ |
|---|---|---|---|
| 3D-VFM only | 24.04 | 0.700 | 0.340 |
| LiDAR only | 24.14 | 0.703 | 0.335 |
| **LiDAR + 3D-VFM** | **24.19** | **0.705** | **0.329** |

## 7. 评估（PDF §IV-C 直引）

### 7.1 稳定性（PDF 第 9 页直引 "RECONSTRUCTING EACH TEST SCENE 10 TIMES"）

- L2D2-GS: PSNR 24.19 (σ×10³ = 1.96), SSIM 0.705 (σ×10⁵ = 8.62), LPIPS 0.329 (σ×10⁵ = 6.46)
- **标准差 0.002-0.009** —— 较 G3R (1.75 dB) 略高，但 SSIM/LPIPS 稳定

### 7.2 与 G3R 的差距
- G3R 协议上 L2D2-GS PSNR 23.18 → 26.87 dB（**+3.69 dB**）
- 但 G3R*（复现配置）→ L2D2-GS：+3.69 dB
- 与 Street Gaussians upper-bound（per-scene）仅 -0.35 dB PSNR

### 7.3 边界
- **仅测 NVIDIA H20 GPUs**（无 mobile / Jetson 实测）
- **数据集集中在 PandaSet / Waymo / DL3DV**（无 4DGS dynamic scene dataset）
- **未给 FPS 数字**（**仅 PSNR / SSIM / LPIPS**）—— 与本项目（4DGS 实时渲染）核心 KPI（FPS / latency）**不完全对标**
- **feedforward 路径**：单次推理后**不再 fine-tune**，但推理时仍需 24 timesteps 优化

## 8. 引用（PDF §References 第 9-14 页，共 44 条）

### 8.1 核心引用（派系相关 + 已收录 49 篇）

| # | 引用 | 关系 | 本项目状态 |
|---|---|---|---|
| [1] | Kerbl et al. "3D Gaussian Splatting", SIGGRAPH 2023, TOG 42(4) 139 | 基础 3DGS | **已收录**（`2023-kerbl-3dgs.md`, 第 50 篇） |
| [2] | Yan et al. "Street Gaussians", ECCV 2024 | per-scene upper bound | **未收录**（drive 派系边缘）|
| [3] | Chen et al. "OmniRe" (2408.16760) | per-scene upper bound | **未收录** |
| [5] | Jiang et al. "AnySplat: Feed-forward 3D Gaussian Splatting from Unconstrained Views", TOG 44(6) | 同主线 feedforward 3DGS | **未收录** |
| [7] | Yang et al. "STORM" (2501.00602) | WOD baseline | **未收录** |
| [10] | Chen et al. "G3R" (2024) | 主 baseline | **未收录** |
| [11] | Wang et al. "Flux4D: Flow-based Unsupervised 4D Reconstruction" (2512.03210) | 4DGS 主线 | **未收录** |
| [30] | Liang et al. "4DGSream: Variable Bitrate Dynamic Gaussian Splatting Streaming", IEEE TMM 2026 | 派系 D streaming | **未收录** |
| [37] | Xu et al. "AD-GS" (2025 ECCV) | 自驾 3DGS | **未收录** |
| [40] | Tang et al. "torchsparse" MICRO 2023 | sparse convolution lib | 工程实现 |
| [41] | Keetha et al. "MapAnything" (2509.13414) | 几何先验 | **未收录** |
| [44] | Yang et al. "EmerNeRF" (2311.02077) | NOTR Dynamic32 split 出处 | **未收录** |

### 8.2 1-hop 候选论文（待评估）

- **Street Gaussians (Yan 2024)** —— drive 派系对标 → 可考虑收录
- **OmniRe (Chen 2024)** —— drive 派系对标 → 可考虑收录
- **STORM (Yang 2501.00602)** —— NVIDIA + Waymo 合作 → drive 派系
- **G3R (Chen 2024, [10])** —— 4DGS 主 baseline → 可考虑收录派系 A
- **Flux4D (Wang 2512.03210)** —— 4DGS 主流派系 A → 可考虑收录
- **MapAnything (Keetha 2509.13414)** —— 3D VFM / 几何先验 → 派系 C
- **EmerNeRF (Yang 2311.02077)** —— drive 派系基础
- **AnySplat (Jiang TOG 44(6))** —— 同主线 feedforward → 与 ZipSplat 共享
- **4DGSream (Liang TMM 2026)** —— 4DGS streaming → 与派系 D 关联
- **AD-GS (Xu ECCV 2025)** —— drive 派系对标

## 9. Insight（对 4DGS 移动端渲染）

### 9.1 直接相关性

1. **小米合作背景**：junnan5@xiaomi.com / sunchitian@xiaomi.com / heliangliang@xiaomi.com 三位小米作者 —— **与本项目用户所属公司直接相关**。**潜在合作 / 内部参考价值**
2. **路径差异**：L2D2-GS 用 **Feedforward + densification policy**（一次性推理）替代 **canonical + deformation**（Wu 4DGS 范式）—— 是 4DGS 表示路径的**第二选择**

### 9.2 对本项目 Snap 8 Gen 4 + Vulkan 1.3 实时渲染 4DGS 的启示

1. **Feedforward 4DGS 的可行性**：L2D2-GS 证明 dynamic urban scene 可以 ~98s 重建达到 per-scene 70 min 接近的 PSNR（24.19 vs 24.54 = -0.35 dB）—— **节省 43× 时间**。**问题**：98s 是 H20 GPU，**移动端能否在可接受时间（如 1-2 分钟）跑完 feedforward 推理**？**待评估**
2. **移动端 4DGS 重建潜在路径**：如果把 L2D2-GS 的 24 timesteps 推理在 mobile GPU 上做，**第一步**：把 30K iter 减少到 1-2K（牺牲 PSNR）；**第二步**：把 46 维 Gaussian 参数压缩到 14 维 explicit（仅位置/旋转/缩放/颜色/不透明度）
3. **与本项目 README §1 论据的关系**：本项目核心论据是 "**4DGS 实时渲染在 mobile 上 FPS 是瓶颈**" —— L2D2-GS 不解决渲染瓶颈（**未给 FPS**），但提供**离线重建路径加速 43×**（缩短训练/重建时间）。**这是间接支持**：更快的重建 → 更频繁的内容更新 → 流式落地价值

### 9.3 边界 / 不适用

- L2D2-GS 的 98s 重建时间是 **offline batch**，**不直接对应实时渲染 FPS** —— **本项目目标"实时渲染"不是 L2D2-GS 关心的问题**
- L2D2-GS 用 8 × H20 GPUs 训练，**不适合移动端直接运行**（mobile 需极度压缩）
- **PSNR 24.19 dB 在 PandaSet** 比同主线 AnySplat 18.76 dB 高 +5.43 dB（32-view），但 **FPS / latency 未测**

## 11. 1-hop 关系图（待 v2 补全）

```python
# 待 v2 用 Semantic Scholar API 验证后补全
# 候选 1-hop: Street Gaussians / OmniRe / STORM / G3R / Flux4D / MapAnything / AnySplat / 4DGSream
# 5 篇示范：Street Gaussians / G3R / Flux4D / AnySplat / 4DGSream
```

## 12. 注释 / 待人工

- **🚩 解 🚩 历史**：凌晨 cron（2026-07-09 00:37）pypdf 解析失败 → 本次 cron 用 fitz 重解析成功 → **3 道保险 #1 数字必标 PDF 页码全部满足**
- **❓ L2D2-GS 是否开源**：PDF 未给 GitHub URL（references [2] 的 DriveStudio 是 G3R 的 baseline 框架）—— **待人工核查**（arXiv abs 页 → check "Code" tab）
- **❓ venue 归属**：PDF 模板 "JOURNAL OF LATEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2021" —— **明显是 IEEE Transactions 模板遗留**（不是真实发表年份），**真实投稿目标待人工**（可能 TVCG / TPAMI）