# 2026-yu-codecsplat · CodecSplat: Ultra-Compact Latent Coding for Feed-Forward 3D Gaussian Splatting

> **相关性**：**⭐⭐ 派系 4（流式）+ 派系 1（训练期压缩）命中**（arXiv 2026-05-25）—— 核心数字：**DL3DV 20-107.77 KiB/scene @ 23.56-26.36 dB PSNR**；**RealEstate10K 3.37-12.51 KiB/scene @ 24.76-27.05 dB**；codec encode **0.267s** / decode **0.273s**（PDF Table 2 直引）；**比压缩 FF 生成的 Gaussians 还小 ~一个数量级**（abstract 直引）；**Mobile relevance 弱**（streaming/transmission focus，**未做 mobile GPU 实测**）。

> **⚠ 重要区分**：这是 **Feed-forward 3DGS（静态）** 工作，不是 4DGS。**对 4DGS 适用性**：**intermediate 2D Gaussian-generation feature latent coding** 思路理论上可扩展到 4DGS 中间 latent 特征，但 abstract 未做 4DGS 实验。**对派系 4（流式）价值最高**：**kB-level scene bitstream** + **controllable rate-distortion** 与本项目 M2 训练→流式播放 pipeline 强契合。

## 0.5 元数据

- **venue**: arxiv pre-print (2026-06)
- **arxiv-id**: 2605.25563
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

FF3DGS 给定 sparse context views 在单次 forward pass 内重建 3D scene，但**生成后的 Gaussians 是 irregular representation，对压缩不友好**。**如何把 coding bottleneck 移到 feed-forward 内部（before 2D-to-3D Gaussian mapping），实现 kB-level scene bitstream + 可控 RD trade-off**？

## 链接

- arXiv：<https://arxiv.org/abs/2605.25563>（v1 2026-05-25，cs.CV，"Preprint"）
- GitHub：not found in PDF header
- 项目页：not found in PDF header
- PDF：已下 `.pdfs/2605.25563.pdf`（12 页）
- 会议：not found in abstract

## 年份 / 作者 / 机构（PDF 头部实测）

- **年份**：2026（v1 2026-05-25）
- **第一作者**：**Pengpeng Yu¹˒³**（余鹏鹏，PDF 头部直引）
- **通讯作者**：**Jing Wang³†**, **Yulan Guo¹˒³†**（双通讯）
- **机构**（PDF 头部直引）：
  1. **Sun Yat-sen University（中山大学）** —— 中国广州
  2. **Peking University（北京大学）** —— 中国北京
  3. **Pengcheng Laboratory（鹏城实验室）** —— 中国深圳
  - 邮箱：`yupp5@mail2.sysu.edu.cn`

## 方法核心（PDF §3 + abstract 直引）

### 关键创新：把 Coding Bottleneck 移到 Feed-Forward 内部

> "By placing the coding bottleneck **before 2D-to-3D Gaussian construction**, CodecSplat allows compression and feed-forward Gaussian generation to operate on the **same compact intermediate representation**."（PDF 第 8 页直引）

- **传统路线的问题**：现有 3DGS 压缩（per-scene）→ 操作于最终 irregular 3D Gaussians，**spatial locality and cross-view redundancy 在 structured-to-irregular 转换时已丢失**
- **CodecSplat 解法**：**编码 intermediate 2D Gaussian-generation feature** → 编码 2D grid latent features，保留 structured 2D 信息（depth-guided, multi-view refined）

### 三大 pipeline component（abstract + PDF §3 直引）

1. **Encoder**：multi-view depth + feature extraction → depth-guided multi-view feature refinement → **entropy-coded latent bitstream**
2. **Bitstream**：entropy-coded 2D grid feature，**KB-level per scene**
3. **Decoder**：entropy-decode → predict depth + Gaussian attributes via lightweight heads → map pixel-aligned predictions to 3D space

### Rate-Distortion Trade-off（abstract 直引）

- 通过调节 **λ ∈ {16, 32, 64, 128, 256, 512, 1024}** 控制 bitrate vs quality
- **DL3DV**（PDF Table 1 直引）：λ=16 给出 **20.00 KiB/scene @ 23.56 dB**，λ=1024 给出 **107.77 KiB/scene @ 26.36 dB**
- **RE10K**（PDF Table 1 直引）：**3.37 KiB/scene @ 24.76 dB**（λ=16）→ **12.51 KiB/scene @ 27.05 dB**（λ=1024）

## 关键数字（PDF Table 1 / Table 2 直引 + abstract 直引）

### PDF Table 1 直引 · DL3DV vs Baselines

| 方法 | Bytes/scene ↓ | PSNR↑ | SSIM↑ | LPIPS↓ |
|---|---|---|---|---|
| DepthSplat→PNG | 11.66 MiB | 24.94 | 0.848 | 0.128 |
| DepthSplat→SOGS | 11.48 MiB | 24.94 | 0.848 | 0.128 |
| DepthSplat→FCGS | 12.08 MiB | 24.93 | 0.847 | 0.129 |
| ReSplat→PNG | 0.84 MiB | 22.75 | 0.843 | 0.172 |
| ReSplat→SOGS | 0.86 MiB | 28.36 | 0.894 | 0.120 |
| ReSplat→FCGS | 1.39 MiB | 28.72 | 0.897 | 0.113 |
| **CodecSplat λ=16** | **20.00 KiB** | **23.56** | 0.768 | 0.267 |
| **CodecSplat λ=256** | 76.56 KiB | 26.14 | [n/a] | [n/a] |
| **CodecSplat λ=1024** | **107.77 KiB** | **26.36** | [n/a] | [n/a] |

> **比压缩 FF 生成 Gaussians 还小 ~一个数量级**（abstract 直引）：
> - vs DepthSplat→SOGS **11.48 MiB**: 76.56 KiB = **149× 缩小**
> - vs ReSplat→FCGS 1.39 MiB: 107.77 KiB = **13× 缩小**

### PDF Table 2 直引 · Timing（DL3DV）

| 方法 | GS Gen. (s) ↓ | Compress (s) ↓ | Decompress (s) ↓ |
|---|---|---|---|
| DepthSplat→SOGS | 0.155 | **69.768** | 0.452 |
| DepthSplat→FCGS | 0.155 | 4.470 | 3.790 |
| ReSplat→SOGS | 0.282 | 16.114 | 0.024 |
| ReSplat→FCGS | 0.282 | 0.762 | 0.969 |
| **CodecSplat** | **0.124** | **0.267** | **0.273** |

> **关键观察**：CodecSplat 是 **唯一 codec encode+decode 都 < 0.3s 的方法**（SOGS encode 16-70s，慢 ~60-260×）

### abstract 直引
- "**20.00-107.77 KiB and 3.37-12.51 KiB per scene, respectively**"
- "**23.56-26.36 dB and 24.76-27.05 dB PSNR, respectively**"
- "**roughly one order of magnitude smaller** than compressing feed-forward generated Gaussian primitives"
- "**preserving controllable rate–distortion behavior**"

## 与本调研主线的关系

### ⭐⭐ 派系 4（流式）— 直接命中（与 ZipSplat 同思路）

| 维度 | CodecSplat | ZipSplat（派系 4） | 4DGCPro（派系 4 4DGS 对比） |
|---|---|---|---|
| Bytes/scene | **20-108 KiB** | 62K Gaussians（bytes 视 attribute 维度） | 4DGS specific |
| 4DGS 适配 | ❌ static | ❌ static | ✅ |
| Codec encode | **0.267s** | n/a | depends |
| Codec decode | **0.273s** | n/a | depends |
| Mobile relevance | 弱（streaming focus） | 弱 | 不直接 |

### 对项目目标的具体承诺 / 不可承诺

- **承诺 1（强）**：**Coding bottleneck inside pipeline + structured intermediate feature** = 对 4DGS 端到端流式 pipeline **M2 训练→M4 端侧播放** 有重要启发 —— **应把 4DGS 训练流程中的 intermediate latent 也编码**
- **承诺 2（强）**：**Rate-distortion controllable + KB-level bitstream** = **派系 4（流式）核心交付物**：`[推测]` 本项目 M4 端侧需要 ~100 KiB/scene 级别 bitstream，CodecSplat 已证明可行
- **承诺 3（方法学）**：**与 ZipSplat 同源思路**（feed-forward + intermediate feature compression）—— **两条都是"对 pipeline 内部表示做压缩"**
- **不可承诺 1**：**Mobile GPU benchmark 缺失** —— **未给 mobile GPU FPS / VRAM**
- **不可承诺 2**：**FPS rendering 实测**：Table 2 只给 codec encode/decode 时间，**未给 rendering FPS**
- **不可承诺 3**：**未做 4DGS 实验** —— **3DGS feed-forward 路线 ≠ 4DGS，方法学可借鉴但需重做**

### ⭐ 派系 1（训练期压缩）/ 派系 2（动静态分离）/ 派系 3（移动端）
- **派系 1 间接**：FF3DGS 输出 → kB codec，与"训练后压缩"互补
- **派系 2/3 不直接命中**

## 我未找到 / 提请下游注意

- **Mobile GPU benchmark**：abstract 仅"compact for transmission"，**未给 mobile GPU 型号 / FPS**
- **Inference rendering FPS**：Table 2 只列 codec 时序，**rendering 时序未单独 benchmark**
- **4DGS 适配**：abstract / §1-§3 全程未做 4DGS 实验
- **GitHub / 项目页**：PDF 头部无直链
- **会议**：abstract "Preprint"，**arXiv preprint 状态**
- **DL3DV / RE10K 详细 PSNR（每 λ）**：[Table 1 给出部分，需 PDF Page 8-9 完整核]
- **训练 hardware**：abstract / Table 2 未明示（`[推测]` 是 datacenter GPU）

[abstract 直引] [PDF §3 直引] [PDF Table 1 直引] [PDF Table 2 直引] [推测] [调研深度：PDF §1-§3 + Page 7-8 Table 1/2]
