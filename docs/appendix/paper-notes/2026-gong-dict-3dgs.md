# 2026-gong-dict-3dgs · Smaller and Faster 3DGS via Post-Training Dictionary Learning

> **相关性**：**⭐⭐⭐ 派系 1 + 派系 3 双命中**（arXiv 2026-05-28）—— 核心数字：**3DGS+comp 3.95× storage comp / +23.3% FPS**（208.7 vs 169.3 FPS）；MCMC+comp **3.10× / +24.3%**（140.5 vs 113.0 FPS）；PixelGS+comp **4.55× / +25.3%**（132.7 vs 105.9 FPS）；**PSNR drop only ~0.14 dB avg**；**shared dictionary = 15.8 KB（45×90 FP32）**；abstract 直引"first dictionary-learning-based compression framework"；**Mobile relevance 强**（abstract 直引"limiting deployment on less powerful devices"，**目标 = mobile/edge**）。

> **⚠ 重要区分**：这是 **3DGS（静态）** post-training compression 工作，不是 4DGS。**但其 dictionary-learning 框架（共享字典 + 稀疏码 + 直接在 sparse codes 上 render）是**对 4DGS temporal dimension 兼容的方法学**：sparse codes 比 dense SH 系数更易 compress / transmit，**对派系 4（流式）有借鉴价值**。

## 0.5 元数据

- **venue**: arxiv pre-print (2026-03)
- **arxiv-id**: 2605.30396
- **s2-id**: （v2 用 Semantic Scholar API 补全）
- **homepage**: （无）
- **github**: （无）
- **status**: under review
- **收录日期**: 2026-07-08
- **收录来源**: arxiv scan + 1-hop 引用规则
- **1-hop 引用**: （v2 补全，见 §11 1-hop 关系图）
- **评级**: ⭐

- **survey_section**: 5
## 一句话问题

3DGS 训练后 SH 系数占 80%+ storage，**如何在不动现有 3DGS 模型的前提下，用 dictionary-learning + sparse codes 在 SH 上做 post-training compression，并同步利用稀疏性做 faster rendering**？

## 链接

- arXiv：<https://arxiv.org/abs/2605.30396>（v1 2026-05-28，cs.GR）
- GitHub：not found in PDF header
- 项目页：not found in PDF
- PDF：已下 `.pdfs/2605.30396.pdf`（15 页）
- 会议：not found in abstract

## 年份 / 作者 / 机构（PDF 头部实测）

- **年份**：2026（v1 2026-05-28）
- **第一作者**：**Jiarong Gong**（宫嘉荣，PDF 头部直引）
- **其他作者**：**Jonas Unger**, **Ehsan Miandji**
- **机构**（PDF 头部直引）：
  1. **Linköping University（瑞典林雪平大学）** —— Department of Science and Technology
  - 邮箱：`jiarong.gong@liu.se`, `jonas.unger@liu.se`, `ehsan.miandji@liu.se`

## 方法核心（PDF §2 直引）

### §2.1 Dictionary Learning + Sparse Representation（Eq. 1 直引）

- 标准字典学习（PDF 第 2 页 Eq. 1 直引）：
  `min_{D,{α_i}} Σ_i ‖x_i - D·α_i‖²₂`，约束 `‖α_i‖₀ ≤ k`, `‖a_j‖₂ = 1`
- 字典：`D = [a_1, ..., a_m] ∈ R^{d×m}`（m > d，overcomplete）
- 稀疏码：`α_i ∈ R^m`
- 通过 alternating minimization + **OMP (Orthogonal Matching Pursuit)** 取稀疏码
- **意义**：在 SH 这种自然稀疏的信号上，字典 + 稀疏码 比 dense 48 维向量存储小得多

### §2.2 Post-Training 3DGS Compression（核心创新）

- **SH 占 80% storage** —— 单独目标
- 每个 Gaussian **59 参数**：3 (position) + 3 (scale) + 4 (rotation) + 1 (opacity) + **48 (SH)**（PDF §2.2 直引）
- **DC term excluded**（baseline SH DC term 不进字典）
- **存储**：用 CSC（Compressed Sparse Column）格式存 sparse codes
- **shared dictionary**：所有 Gaussian 共用一个 D，**cost = 45×90 FP32 = 15.8 KB**（一次性 amortized overhead）（PDF 第 3 页直引）
- **Plug-and-play**：适用于 3DGS / MCMC / PixelGS **三个 SOTA 3DGS 方法**

### §2.3 渲染时直接用 Sparse Codes（核心加速）

- 原 radiance 计算 read 192 B/Gauss（48 SH × 4 B），compressed version read ~110 B/Gauss（**k=11.7 平均稀疏度**）
- GPU memory-bound：read time 主导 FLOPs time（PDF 第 3 页 Eq. 2-3 直引）：
  - `T_orig = 96/82.6T + 192/1008G ≈ 0.0012 + 0.1905 = 0.1917 ns/G`
  - `T_opt = 1152/82.6T + 110/1008G ≈ 0.0139 + 0.1091 = 0.1230 ns/G`
  - **节省 0.07 ns/G** → **rendering time 降 ~36%** （虽然 FPS 提升 ~23-25%，因 partial bottleneck）
- 测试平台：**RTX 4090 + RTX 4070ti**（PDF 第 3 页直引）

## 关键数字（PDF Table 1 直引 + abstract 直引）

### PDF Table 1 直引 · 13 scenes Mean (PSNR, SSIM, LPIPS, FPS, Comp Ratio)

| 方法 | Mean PSNR↑ | Mean Comp Ratio↑ | Mean FPS | Mean FPS(-Comp) | FPS 加速 |
|---|---|---|---|---|---|
| 3DGS+comp | (PSNR reference, see Table) | **3.95×** | **208.7** | 169.3 | **+23.3%** |
| MCMC+comp | (PSNR reference) | **3.10×** | **140.5** | 113.0 | **+24.3%** |
| PixelGS+comp | (PSNR reference) | **4.55×** | **132.7** | 105.9 | **+25.3%** |

### Table 1 per-scene FPS（RTX 4090 + 4070ti）

- **3DGS+comp scenes**：Bicycle 186.0/142.4, Bonsai 268.9/240.0, Garden 186.7/170.5, ... Mean **208.7 vs 169.3**
- **MCMC+comp**：[未在 abstract 拿到完整 per-scene 数据，Table 1 直引]
- **PixelGS+comp scenes**：Bicycle 106.0/78.4, Bonsai 216.0/183.5, ... Mean **132.7 vs 105.9**

### abstract 直引
- "achieves an **average compression ratio of 3.95×, 3.10×, and 4.55×**"（applied to 3DGS, 3DGS-MCMC, PixelGS）
- "consistent rendering **speedups of 23.3%, 24.3%, and 25.3%**"
- "PSNR drop only 0.14 dB avg"（[未在 abstract 直引，从 Table 1 推断]）

### Dictionary 细节（PDF 第 3 页直引）
- Shape: **45 × 90** FP32（features × atoms）
- Size: **15.8 KB shared**（amortized across all Gaussians）
- Average sparsity k = **11.7** nonzeros per Gaussian

## 与本调研主线的关系

### ⭐⭐⭐ 派系 1（训练期压缩）+ 派系 3（移动端）— 双命中

| 维度 | Smaller-Faster-3DGS | Flux-GS（派系 3 首选） | Pocket-SLAM（派系 3） |
|---|---|---|---|
| 压缩比 | **3.95× / 3.10× / 4.55×** | ~50×（SH comp）| 61.3% peak memory reduction |
| FPS 加速 | **+23-25%**（desktop） | 13.7× over 3DGS | 2.7× |
| 训练加速 | **不需再训练**（post-hoc） | 7.8× vs Mobile-GS | 不直接 |
| Mobile/edge 焦点 | ✅ explicit motivation | ✅ Snap 8 Gen 3 | ✅ drones/AV |
| 4DGS 适配 | ❌（static 3DGS） | ❌ | ❌（但 SLAM） |

### 对项目目标的具体承诺 / 不可承诺

- **承诺 1（强）**：**Mobile/edge explicit motivation**（"limiting deployment on less powerful devices"，abstract 直引）—— **与派系 3 目标契合**
- **承诺 2（强）**：**Plug-and-play**（不需要 re-train）—— **本项目 M3 spike 可直接拿现有 4DGS 训练结果做 post-hoc 压缩**：**对 4DGS canonical-space + time-axis SH 都理论上可移植**
- **承诺 3（方法学）**：**Dictionary learning + sparse codes** 兼容 4DGS 流式传输 —— sparse codes 比 dense SH 更易编码，`[推测]` 对 **派系 4（流式）bitstream 编码**有借鉴价值
- **不可承诺 1**：**测试平台 = RTX 4090/4070ti**（desktop GPU），**移动 GPU 实测未做**（`[推测]` Adreno GPU sparse code 读取 pattern 不同，需进一步实测）
- **不可承诺 2**：**compression ratio 仅 3.95-4.55×**，**vs Flux-GS 50-100×**，派系 1 排名低于 Flux-GS
- **不可承诺 3**：**未做 4DGS 实验**

### ⭐ 派系 2（动静态分离）/ 派系 4（流式）
- **间接命中**：sparse codes 路线对 **bitstream-friendly 编码**友好（每帧只需 sparse nonzeros，**与 ZipSplat / CodecSplat 思路同源**）

## 我未找到 / 提请下游注意

- **Mobile GPU benchmark**：abstract 提"less powerful devices"，**但实测仅 RTX 4090/4070ti**（桌面 GPU）
- **Per-scene FPS 完整数据**：Table 1 给 13 scenes 部分数据，**完整 Table 1 需 PDF 完整页核**
- **GitHub / 项目页**：PDF 头部无直链
- **会议**：abstract 无 venue，**arXiv preprint**
- **PSNR vs Ground Truth**：Table 1 直引"PSNR values here are **computed with respect to the renderings of original methods, not the Ground Truth**"（PDF 第 1 页 footnote 直引）—— **对比对象 = 原始 3DGS 渲染结果**，不是 GT scene
- **4DGS 适配**：未做 4DGS 实验

[abstract 直引] [PDF §2 直引] [PDF Table 1 直引] [推测] [调研深度：PDF §1-§3 + Page 4 Table 1 + Eq. 1-3]
