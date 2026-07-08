# 2026-zhao-ace-gs · ACE-GS: Acing the Trade-off with Accurate, Compact and Efficient 3D Gaussian Splatting

> **相关性**：**⭐⭐ 训练期压缩 + ultra-fast reconstruction**（arXiv 2026-06-19，PDF 直引）—— **核心数字**：Mip-NeRF 360 上 **3DGS 24m43s → ACE-GS 5m30s**（**~4.5× 训练加速**），**FPS 241.8 → 745.6**（**3.1×**），**PSNR 27.54 → 28.10**（**+0.56 dB**）；Tanks & Temples 上 **12m50s → 3m01s（4.3×）**、**FPS 313 → 863.9**；abstract 提 **"up to 3.7× training acceleration against Speedy-Splat"** + **"3 to 5 minutes to converge, peak PSNR improvement up to 0.89 dB"**。**对派系 1（训练期压缩）**直接命中 + **派系 3（移动端）有间接 motivation**（abstract 提"virtual reality and digital twins"）。

> **⚠ 重要区分**：这是 **3DGS（静态）** 工作，不是 4DGS。**但其方法学（momentum-consistency densification + statistical sensitivity sparsification + frequency-domain residual compensation）对 4DGS canonical-space 剪枝有借鉴价值**。**未做 4DGS / mobile GPU 实测**。

## 0.5 元数据

- **venue**: arxiv pre-print (2026-03)
- **arxiv-id**: 2606.21244
- **s2-id**: （v2 用 Semantic Scholar API 补全）
- **homepage**: （无）
- **github**: （无）
- **status**: under review
- **收录日期**: 2026-07-08
- **收录来源**: arxiv scan + 1-hop 引用规则
- **1-hop 引用**: （v2 补全，见 §11 1-hop 关系图）
- **评级**: ⭐

## 一句话问题

现有 3DGS 加速框架为追求快速收敛往往 **aggressive pruning primitives → 高频细节严重丢失**。**如何在保持 ultra-fast 训练速度（3-5 min）的同时，保留甚至超越原始 3DGS 的 PSNR**？

## 链接

- arXiv：<https://arxiv.org/abs/2606.21244>（v1 2026-06-19，cs.CV）
- GitHub：not found in PDF header（abstract 无直链）
- 项目页：not found in PDF header
- PDF：已下 `.pdfs/2606.21244.pdf`（17 页）
- 会议：not found in abstract（arXiv preprint）

## 年份 / 作者 / 机构（PDF 头部实测）

- **年份**：2026（v1 2026-06-19）
- **第一作者**：**Jijian Zhao（赵集坚）¹**
- **机构**（PDF 头部直引）：
  1. **Huazhong University of Science and Technology（华中科技大学）** —— Wuhan, China
  - 联系邮箱：`jijianzhao28@gmail.com`（PDF 头部）

## 方法核心（PDF §3 + abstract 直引）

### §3 三大 synergistic 模块（abstract 直引）

> "a **progressive optimization framework** tailored for accurate, compressed, and efficient scene representation. We realize that **precise primitive management** is the key"

1. **Momentum consistency-guided densification**（PDF §4.2 直引）
2. **Statistical sensitivity-driven sparsification**
3. **Cross-dimensional residual frequency compensation**

### §4.2 Momentum Consistency-Guided Densification（核心创新 1）

- **动机**：standard gradient-based strategy 在 **non-manifold regions 创建 floating artifacts**（PDF 第 7 页直引）
- **解法**：historical motion trends > single-step gradient snapshots
- **momentum latent variable**（PDF 第 7 页 Eq. 4 直引）：
  `m_t = γ · m_{t-1} + (1 - γ) · ∇_p L_t`
- **Momentum consistency score Ψ_i**（PDF 第 7 页 Eq. 5 直引）：
  `Ψ_i = (m_t · ∇_p L_t) / (‖m_t‖ · ‖∇_p L_t‖ + ε)` — **cosine similarity 衡量当前梯度 vs 累积动量方向一致性**
- **Dynamic densification trigger**（PDF 第 7 页 Eq. 6 直引）：
  `I_densify = (‖∇L‖ > τ_grad) ∧ (Ψ_i > Ψ̄)` — **只在 primitive consistency 高于 population mean 时 densify**
- **Scene-adaptive**（无需 manual hyperparameter search）

### §4.3 (推测：紧跟) Statistical Sensitivity-Driven Sparsification

- PDF §4.3 内容：[未在抽象 abstract 拿到具体公式，需 PDF §4.3 核]
- abstract 提："deploy a statistical sensitivity-driven sparsification mechanism to **precisely prune redundant primitives, yielding a further compressed footprint**"

### §4.4 (推测：紧跟) Cross-Dimensional Residual Frequency Compensation

- abstract 直引："introduce a cross-dimensional residual frequency compensation scheme that **explicitly back-injects high-frequency error energy into primitive attributes, perfectly restoring sharp geometric details**"
- 意义：**三维 spatial-domain 难以拟合的高频纹理，用 frequency-domain 残差回注** — "spectral analysis: ACE-GS maintains higher energy density in high-frequency bands, aligning closely with Ground Truth"（PDF Fig. 2b 直引）

## 关键数字（PDF Table 1 直引 + abstract 直引）

### PDF Table 1（Page 9）直引 · 三数据集全对比

**Mip-NeRF 360**（PDF Table 1 直引）：

| 方法 | SSIM↑ | PSNR↑ | LPIPS↓ | Time↓ | FPS↑ |
|---|---|---|---|---|---|
| 3DGS | 0.813 | 27.54 | 0.221 | 24m43s | 241.8 |
| LightGaussian | 0.801 | 27.03 | 0.245 | 36m43s | 345.8 |
| Compact3DGS | 0.798 | 27.01 | 0.247 | 28m06s | 331.0 |
| Scaffold-GS | 0.812 | 27.76 | 0.226 | 20m57s | 460.5 |
| Speedy-Splat | 0.782 | 26.89 | 0.295 | 14m47s | 1720.9 |
| **ACE-GS (Ours)** | **0.821** | **28.10** | **0.215** | **5m30s** | **745.6** |

**Tanks & Temples**（PDF Table 1 直引）：

| 方法 | SSIM↑ | PSNR↑ | LPIPS↓ | Time↓ | FPS↑ |
|---|---|---|---|---|---|
| 3DGS | 0.853 | 23.74 | 0.169 | 12m50s | 313.0 |
| LightGaussian | 0.837 | 23.49 | 0.197 | 22m30s | 580.7 |
| Compact3DGS | 0.833 | 23.36 | 0.200 | 15m22s | 464.0 |
| Scaffold-GS | 0.854 | 24.13 | 0.174 | 11m26s | 704.9 |
| Speedy-Splat | 0.820 | 23.47 | 0.240 | 6m48s | 2216.0 |
| **ACE-GS** | **0.860** | **24.63** | **0.171** | **3m01s** | **863.9** |

**Deep Blending**（PDF Table 1 直引）：

| 方法 | SSIM↑ | PSNR↑ | LPIPS↓ | Time↓ | FPS↑ |
|---|---|---|---|---|---|
| 3DGS | 0.907 | 29.77 | 0.238 | 21m58s | 268.0 |
| ACE-GS | **0.912** | **30.33** | **0.237** | **3m00s** | **1108.4** |

### abstract 直引
- "up to **3.7× training acceleration against Speedy-Splat**"（Speedy-Splat 是 aggressive-pruning 路线）
- "**3 to 5 minutes to converge**"
- "**peak PSNR improvement of up to 0.89 dB over the original 3DGS**"
- Room scene（Mip-360）："**ACE-GS achieves a superior reconstruction quality of 32.51 dB**"（PDF Fig. 2a 直引）

## 与本调研主线的关系

### ⭐⭐ 派系 1（训练期压缩）— 直接命中

| 维度 | ACE-GS | Flux-GS（派系 3 首选） | 4DGS-1K |
|---|---|---|---|
| 训练时间 | **5m30s on Mip-360** | 11 min (Indoor) | 中等 |
| FPS | **745.6**（Mip-360）| 147 on Snap 8 Gen 3 | 1000+ FPS @ N3V |
| PSNR vs 3DGS | **+0.56 dB** | -0.19 dB | ~相同 |
| Mobile GPU 实测 | ❌ | ✅ Snap 8 Gen 3 | ❌ |

- **承诺**：**momentum-consistency densification + frequency-domain residual compensation** 都是**派系 1 方法学**——**对 4DGS canonical-space pruning 有借鉴价值**
- **不可承诺**：**未做 mobile GPU 实测**，`[推测]` 745.6 FPS 在 desktop RTX 4090（`[推测]`）;**Snap 8 Gen 4 上 745.6 × (Adreno 8 Gen 4 / RTX 4090) 约 100-200 FPS** = 与 Flux-GS 量级相当 —— **但 abstract 未给 mobile 数据**

### ⭐ 派系 3（移动端渲染管线）
- **间接 motivation**："virtual reality and digital twins"（abstract 直引）
- **不可承诺**：**target = desktop GPU ultra-fast reconstruction**（5 min 训练），与"端侧实时渲染"目标不同

### ⭐ 派系 2（动静态分离）/ 派系 4（流式）
- **不直接命中**：3DGS 静态，无 4DGS / streaming 适配

## 我未找到 / 提请下游注意

- **Sparsification § + Frequency compensation § 公式细节**：仅有 abstract 一句话总述，**§4.3 + §4.4 具体公式需 PDF §4.3-§4.4 核**
- **Mobile GPU benchmark**：abstract / Table 1 均未给 mobile GPU 型号（**`[推测]` 是 desktop GPU benchmark**）
- **GPU 显存数字**：abstract / Table 1 未给具体 VRAM
- **Dataset 内场景数**：abstract 提"Mip-NeRF 360, Tanks & Temples, Deep Blending"，但未给 scene-level breakdown
- **GitHub / 项目页**：PDF 头部仅作者邮箱，**无 GitHub / project link 直引**
- **4DGS 适配性**：未做 4DGS 实验，**仅方法学层面与 per-Gaussian 属性 compatible**（`[推测]`）
- **会议**：abstract 无 venue 信息，**arXiv preprint 状态**

[abstract 直引] [PDF §3 直引] [PDF Table 1 直引] [推测] [调研深度：PDF §1-§4.2 + Page 9 Table 1]
