# 2026-veicht-zipsplat · ZipSplat: Fewer Gaussians, Better Splats

> **相关性**：**⭐⭐ 派系 4（流式）+ 派系 1（训练期压缩）有间接价值**（arXiv 2026-06-12）—— 核心数字：**DL3DV 6v 62K Gaussians**（vs 像素对齐 baseline 393K = **6× 更少**），**+2.1 dB over best pose-free baseline**（YoNoSplat）；**RealEstate10K +1.2 dB**；**TTO → 28.99 dB PSNR @ 6v**（Table 1 直引）。**Mobile relevance 间接**（token-based compact scene is mobile-friendly），**未做 mobile GPU 实测**。

> **⚠ 重要区分**：这是 **Feed-forward 3DGS**（不是 4DGS，也不是 per-scene optimization 3DGS）。**Feed-forward 路线 = 给定几张图像一次性 forward pass 重建 3D scene**，不需 minutes-hours 的 per-scene training。**对 4DGS 适用性**：token-based decoupled-from-pixel-grid 思路理论上对 4DGS canonical-space 可借鉴。

## 0.5 元数据

- **venue**: arxiv pre-print (2026-06)
- **arxiv-id**: 2606.05102
- **s2-id**: （v2 用 Semantic Scholar API 补全）
- **homepage**: （无）
- **github**: （无）
- **status**: under review
- **收录日期**: 2026-07-08
- **收录来源**: arxiv scan + 1-hop 引用规则
- **1-hop 引用**: （v2 补全，见 §11 1-hop 关系图）
- **评级**: ⭐

- **survey_section**: 6
## 一句话问题

Feed-forward 3DGS methods 的 inductive bias = **Gaussian 与 input pixel 一一对应**（"tied to input pixels"）—— **Gaussian 预算由 2D camera resolution 决定，而非 3D scene complexity**（"a flat wall and a richly textured object thus produce equally many Gaussians despite very different geometric needs"）。**如何 decouple Gaussian placement from pixel grid，在 fewer Gaussians 下实现更高 quality**？

## 链接

- arXiv：<https://arxiv.org/abs/2606.05102>（v2 2026-06-12）
- **项目页**：<https://veichta.com/zipsplat>（PDF 第 1 页 abstract 直引）
- GitHub：not found in PDF header（项目页应是入口）
- PDF：已下 `.pdfs/2606.05102.pdf`（24 页）
- 会议：not found in abstract

## 年份 / 作者 / 机构（PDF 头部实测）

- **年份**：2026（v2 2026-06-12）
- **第一作者**：**Alexander Veicht¹**
- **通讯作者**：**Sunghwan Hong ⋆¹**
- **其他作者**：Dániel Baráth¹, Marc Pollefeys¹˒²
- **机构**（PDF 头部直引）：
  1. **ETH Zürich**（苏黎世联邦理工）
  2. **Microsoft**

## 方法核心（abstract + PDF §1 直引）

### Token-Based Feed-Forward Architecture（核心创新）

> "a token-based feed-forward model that **decouples Gaussian placement from the pixel grid**"
> "A **multi-view backbone** extracts dense visual tokens, and **k-means clustering** compresses them into a compact set of **scene tokens**. **Cross- and self-attention refine these tokens**, and a **lightweight MLP decodes** each into a group of Gaussians with **unconstrained 3D positions**."

### 三大 pipeline components（abstract 直引）

1. **Multi-view backbone** → dense visual tokens
2. **k-means clustering** → scene tokens（压缩比可调）
3. **Cross-/Self-attention + Lightweight MLP** → each scene token → group of Gaussians with unconstrained 3D positions

### 关键特性

- **Clustering applied at inference**（"a single trained model spans the quality–efficiency curve **without retraining**"）—— **通过 inference 阶段调 cluster 数调整压缩比**
- **No ground-truth poses / intrinsics needed**（"ZipSplat operates without ground-truth poses or intrinsics"）
- **TTO（Test-Time Optimization）**：可选 fine-tune 进一步提升 PSNR

### Pixel-Gaussian Coupling 的三大 Inefficiencies（PDF §1 直引）

1. Flat wall vs textured object **同 Gaussian 容量**（resolution-bound 而非 complexity-bound）
2. **Overlapping views 冗余**
3. [第三个 efficiency problem 在 PDF §1 后续]

## 关键数字（PDF Table 1 直引）

### DL3DV（Table 1 直引，6v/12v/24v = 6/12/24 input views）

| 方法 | P | K | 6v #Gs | 6v PSNR↑ | 6v SSIM↑ | 6v LPIPS↓ | 24v #Gs | 24v PSNR↑ |
|---|---|---|---|---|---|---|---|---|
| MVSplat | ✓ | ✓ | 393K | 22.66 | 0.760 | 0.173 | 1.6M | 19.98 |
| DepthSplat | ✓ | ✓ | 393K | 23.42 | 0.797 | 0.136 | 1.6M | 20.09 |
| DA3 | ✓ | ✓ | 1.5M | 23.99 | 0.805 | 0.158 | 6.1M | 21.70 |
| **ZipSplat** | ✓ | ✓ | **62K** | **25.34** | **0.810** | **0.169** | **249K** | **24.23** |
| **ZipSplat + TTO** | ✓ | ✓ | **62K** | **28.99** | **0.892** | **0.106** | **249K** | **30.03** |
| NoPoSplat | ✓ | – | 393K | 22.77 | 0.743 | 0.179 | 1.6M | 17.86 |
| AnySplat | – | – | 951K | 21.70 | 0.725 | 0.187 | 3.2M | 20.74 |
| C3G | – | – | 2K | 18.70 | 0.492 | 0.409 | 2K | 15.17 |
| YoNoSplat | – | – | 301K | 24.10 | 0.783 | 0.160 | – | – |

### 关键比值（PDF Table 1 直引）

> - **DL3DV 6v**：ZipSplat 62K vs MVSplat 393K = **6.3× 更少 Gaussians**
> - **DL3DV 6v**：ZipSplat 25.34 dB vs MVSplat 22.66 dB = **+2.68 dB over MVSplat**；vs NoPoSplat 22.77 = **+2.57 dB**；vs YoNoSplat 24.10 = **+1.24 dB over best pose-free YoNoSplat**
> - **DL3DV 6v + TTO**：28.99 dB（vs ZipSplat base 25.34 = **+3.65 dB**）
> - abstract 提 **"+2.1 dB over best pose-free baseline"** = 大致 YoNoSplat / 24 view 对比

### Training/Resolution Setup（PDF §4 直引）
- Resolution: **252×252**（"mixture of RealEstate10K [50] and DL3DV [20] with N∈[2, 24], at 252×252"，PDF 第 8-9 页直引）
- Optimizer: AdamW, lr=3×10⁻⁴, weight decay 0.05
- Fine-tuning 0.1× base rate

### abstract 直引
- "**∼6× fewer Gaussians than pixel-aligned methods**"
- "**surpassing the best pose-free baseline by 2.1 dB and 1.2 dB PSNR, respectively** [DL3DV / RE10K]"
- "**generalizes zero-shot to Mip-NeRF360 and ScanNet++**"

## 与本调研主线的关系

### ⭐ 派系 4（流式）+ 派系 1（训练期压缩）— 间接命中

| 维度 | ZipSplat | CodecSplat（派系 4） | 4DGCPro（派系 4） |
|---|---|---|---|
| 压缩比 | **6× fewer Gaussians**（62K vs 393K）| 100-600× size | 不直接 |
| 4D 适配 | ❌ static 3DGS | ❌ static | ✅ 4DGS |
| Mobile relevance | **token-based compact scene, mobile-friendly** | streaming/transmission focus | not mobile-evaluated |
| Training speed | Feed-forward（秒级） | Feed-forward（秒级） | hours |

> **关键洞察**：**ZipSplat 和 CodecSplat 都是 feed-forward 静态 3DGS 路线**，**与本项目 M0 一次训练多次播放的特性契合度较低**（本项目用 4DGS 动态场景）—— 但 token-based decoupled-from-pixel-grid 思路**对 4DGS canonical-space tokenization 有借鉴价值**。

### 对项目目标的具体承诺 / 不可承诺

- **承诺 1（方法学，间接）**：**Clustering-based compression at inference** 提供了 "scene complexity rather than resolution" 的视角 —— 对 4DGS canonical-space compression（**派系 4 流式编码**）理论上可借鉴：`[推测]`
- **承诺 2（数据，间接）**：**Table 1 详细对比 MVSplat / DepthSplat / DA3 / NoPoSplat / AnySplat / C3G / YoNoSplat** —— 是 **feed-forward 3DGS benchmark**，对本项目调研方法学有价值
- **不可承诺 1**：**未做 mobile GPU benchmark**（abstract 未提 mobile）；**252×252 resolution** 比 mobile-typical resolution 还低，`[推测]` 不是面向移动端设计的
- **不可承诺 2**：**4DGS 适配性未做实验**

### ⭐ 派系 2（动静态分离）/ 派系 3（移动端）
- **不直接命中**：无 4DGS / mobile GPU 数据

## 我未找到 / 提请下游注意

- **训练 compute / GPU 类型**：PDF 头部未明示 training hardware（"需 PDF §4 implementation details 核"）
- **Inference FPS**：Table 1 未给 inference FPS
- **Mobile GPU benchmark**：abstract 仅 generic "compact" mention，**未给 mobile FPS / VRAM**
- **4DGS 适配**：abstract / §1-§3 未做 4DGS 实验
- **GitHub link**：项目页有，**但 abstract 未直接给 repo URL**
- **会议**：abstract 无 venue，**arXiv preprint**
- **TTO 训练时**：abstract 提 "**+TTO**" → 28.99 dB，**但 TTO 训练时间 / 收敛性未在 abstract 给**

[abstract 直引] [PDF §1 直引] [PDF Table 1 直引] [推测] [调研深度：PDF §1 + Page 9 Table 1 + Page 9-10 §4 partial]
