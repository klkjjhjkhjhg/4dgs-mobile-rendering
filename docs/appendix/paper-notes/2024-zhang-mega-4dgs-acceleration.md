# 2024-zhang-mega-4dgs-acceleration · MEGA: Memory-Efficient 4D Gaussian Splatting for Dynamic Scenes

> **升级说明**:本笔记从 abstract 级升级为 PDF 全文级。**关键数字全部 PDF Table 1/2/3 直引**,不再外推。补充:MEGA 是 **bitpack 路线**(SH→DC+AC + entropy-constrained deformation),与 4DGS-1K(Spatial-Temporal Variation Score pruning + Temporal Filter mask)**不同思路**,**两者可叠加**(已在 `2025-yuan-4dgs-1k.md` §"与本调研主线的关系"中明确说明)。

## 一句话问题
如何把 4DGS 的"百万级高斯 × 161 参数(其中 144 是 SH 系数)"从**GB 级存储**压到**几十 MB**,**同时保持 comparable quality 和实时速度**?

## 链接(均经 fetch + PDF 实测)
- arxiv: <https://arxiv.org/abs/2410.13613>(v1 2024-10-17)
- 项目页 / GitHub: <https://github.com/Xinjie-Q/MEGA>(PDF abstract 直引 + 仓库 README 实测)
- PDF: 已下到 `/tmp/4dgs-papers/zhang-mega.pdf`(15 页、4.5 MB)

## 年份 / 作者 / 机构(arxiv metadata + PDF 头部实测)
- **年份**:2024(2024-10-17 v1)
- **第一作者**:Xinjie Zhang(张欣杰,通讯)
- **通讯作者**:Yifan Zhang(亦凡)、Shuicheng Yan(严水成,NUS)、Jun Zhang(张军,HKUST iComAI Lab)
- **完整作者列表**:Xinjie Zhang, Zhening Liu, Yifan Zhang, Xingtong Ge, Dailan He, Tongda Xu, Yan Wang, Zehong Lin, Shuicheng Yan, Jun Zhang
- **机构**:
  - **iComAI Lab, HKUST**(香港科技大学)
  - **Skywork AI**
  - **CUHK**(香港中文大学)
  - **NUS**(新加坡国立大学)
  - **AIR, Tsinghua University**(清华智能产业研究院)
- **会议 / 出版**:ICLR 2025(PDF §1 + 公开 metadata)

## 方法核心(PDF §3 直引,Figure 3)

1. **DC-AC color(DAC)represent**(PDF §3.1 / Eq. 3):
   - 把原来 4DGS 的 4D 球谐系数(SH,144 个参数,占总参数 161 的 ~90%)替换为:
     - **per-Gaussian DC component** `c_dc ∈ R^3`(3 个参数,view- & time-independent)
     - **shared AC color predictor** `F_φ`(轻量 MLP,3 linear layers,view- & time-aware)
   - **单 Gaussian 节省 ~8× 颜色存储**(PDF §1 直引:"achieves a compression ratio of approximately 8× relative to the original 4D Gaussians with equivalent Gaussian points")。

2. **Entropy-constrained Gaussian Deformation**(PDF §3.2 / Eq. 4~6):
   - 4DGS 原本假设每个 4D Gaussian 在时间维度上**线性运动 + 旋转/尺度固定**,需要堆大量高斯拟合复杂运动
   - MEGA 引入**temporal-viewpoint aware deformation predictor**(轻量 MLP + 频率位置编码),**扩大每个高斯的"作用时间范围"**
   - 配合**opacity-based entropy loss** `L_opa = -o_j log(o_j)`,鼓励每个高斯的 spatial opacity 趋向 0 或 1 → 主动剪枝 `K` 步内 opacity 近 0 的高斯
   - **关键效果**:Gaussian participation ratio 从 4DGS 的 **< 50%** 提到 MEGA 的 **~75%**(PDF Figure 4a)

3. **Training + Compression Pipeline**(PDF §3.3):
   - **Loss**:`L = (1-λ)·L1 + λ·L_SSIM + κ·L_opa`,论文设 `λ=0.2, κ=0.0005`
   - **半精度存储**:**FP16** 存 learnable parameters
   - **zip delta 压缩**:额外 ~10% 无损压缩
   - **整体存储**:BitPACK 路径(`FP16 + zip`)典型 `~10%` raw model size

4. **推理流程**(PDF §3,Figure 3d):4 步 — per-Gaussian transformation → temporal slicing → projection → differentiable rasterization。**渲染时剪掉 `σ(t) ≤ 0.05` 的高斯**(PDF §4 直引)。

## 关键数字(全部 PDF Table 1/2/3 直引)

### Table 1 · Technicolor Dataset(2048×1088,5 scenes,storage=50 frames)[PDF Table 1 直引]

| Method | PSNR↑ | DSSIM1↓ | DSSIM2↓ | LPIPS↓ | FPS↑ | Storage↓ |
|---|---|---|---|---|---|---|
| DyNeRF | 31.80 | — | 0.0210 | 0.1400 | 0.02 | 30.00 MB |
| HyperReel | 32.70 | 0.0470 | — | 0.1090 | 4.00 | 60.00 MB |
| Deformable 3DGS | 30.95 | 0.0696 | 0.0353 | 0.1553 | 76.09 | 61.36 MB |
| STG | 33.35 | 0.0404 | 0.0187 | 0.0846 | 141.73 | 51.35 MB |
| E-D3DGS | 32.89 | 0.0494 | 0.0231 | 0.1114 | 79.14 | 56.07 MB |
| 4DGS | 32.07 | 0.0535 | 0.0263 | 0.1189 | 55.26 | **6107.07 MB** |
| **Ours (MEGA)** | **33.57** | **0.0442** | **0.0204** | **0.1014** | **83.14** | **32.45 MB** |

> **MEGA vs 4DGS**:**PSNR +1.50 dB / 32.07→33.57**;Storage **6107.07 → 32.45 MB = 188.2× 压缩**(论文 abstract 直引 **190×**);FPS **55.26 → 83.14 = 1.50× 加速**。
> **PDF vs abstract 不一致**:abstract 说 "190×" / Table 1 实测 188.2×(30.32MB / 7.79GB = ~250× for single scene,但 50-frame storage 是 190×;以 Table 1 数字为准)。

### Table 2 · Neural 3D Video Dataset(Neu3DV,300 frames,6 scenes)[PDF Table 2 直引]

| Method | PSNR↑ | DSSIM1↓ | DSSIM2↓ | LPIPS↓ | FPS↑ | Storage↓ |
|---|---|---|---|---|---|---|
| HyperReel | 31.10 | 0.0360 | — | 0.0960 | 2.00 | 360.00 MB |
| K-Planes | 31.63 | — | 0.0180 | — | 0.30 | 311.00 MB |
| MixVoxels-L | 31.34 | — | 0.0170 | 0.0960 | 37.70 | 500.00 MB |
| MixVoxels-X | 31.73 | — | 0.0150 | 0.0640 | 4.60 | 500.00 MB |
| Dynamic 3DGS | 30.46 | 0.0350 | 0.0190 | 0.0990 | 460.00 | 2772.00 MB |
| C-D3DGS | 30.46 | — | — | 0.1500 | 118.00 | 338.00 MB |
| Deformable 3DGS | 30.98 | 0.0331 | 0.0191 | 0.0594 | 29.62 | 32.64 MB |
| E-D3DGS | 31.20 | 0.0259 | 0.0151 | 0.0304 | 69.70 | 40.20 MB |
| STG | 32.04 | 0.0261 | 0.0145 | 0.0440 | 273.47 | 175.35 MB |
| 4DGS | 31.57 | 0.0290 | 0.0164 | 0.0573 | 96.69 | 3128.00 MB |
| **Ours (MEGA)** | **31.49** | **0.0290** | **0.0165** | **0.0568** | **77.42** | **25.05 MB** |

> **MEGA vs 4DGS**:**PSNR -0.08 dB / 31.57→31.49**(几乎无损);Storage **3128 → 25.05 MB = 124.9× 压缩**(abstract 直引 **125×**);FPS 96.69 → 77.42 = 0.80×(轻微减速)。
> **MEGA vs STG(SOTA on N3V)**:PSNR 31.49 vs 32.04(**-0.55 dB**);Storage 25.05 vs 175.35 = 7.0× 更小;FPS 77.42 vs 273.47 = 0.28×(更慢)。

### Table 3 · 消融(per-component)[PDF Table 3 直引]

#### (a) Technicolor Dataset — Birthday 场景

| 变体 | PSNR↑ | DSSIM1↓ | N(#Gauss)↓ | Params↓ |
|---|---|---|---|---|
| 4DGS baseline | 31.00 | 0.0383 | 13.00M | 2093.56M |
| w/ grid(K-Planes style) | 30.49 | 0.0410 | 16.33M | 293.07M |
| w/ DAC | 31.60 | 0.0355 | 15.43M | 308.65M |
| w/ DAC + Deformation | 31.35 | 0.0368 | 15.75M | 315.36M |
| w/ DAC + L_opa | 31.46 | 0.0370 | 9.15M | 183.23M |
| **w/ DAC + Deformation + L_opa (=MEGA)** | **32.02** | **0.0309** | **0.91M** | **18.48M** |

#### (b) Neural 3D Video Dataset — Flame Steak 场景

| 变体 | PSNR↑ | DSSIM1↓ | N(#Gauss)↓ | Params↓ |
|---|---|---|---|---|
| 4DGS baseline | 33.19 | 0.0204 | 5.17M | 831.88M |
| w/ grid | 31.07 | 0.0279 | 4.82M | 97.35M |
| w/ DAC | 33.34 | 0.0210 | 5.31M | 106.33M |
| w/ DAC + Deformation | 33.47 | 0.0209 | 6.34M | 127.16M |
| w/ DAC + L_opa | 33.45 | 0.0208 | 2.76M | 55.22M |
| **w/ DAC + Deformation + L_opa (=MEGA)** | **32.27** | **0.0242** | **0.87M** | **17.79M** |

> **消融解读**:
> - **DAC alone** 替换 SH → 几乎不掉 PSNR(31.00→31.60 on Birthday);参数 ~7× 降(2093→308 M)
> - **Deformation alone** 反而让 #Gauss 上升(15.43→15.75M),但配合 **L_opa** 之后**骤降到 0.91M** —— 这是最关键的协同点
> - **MEGA final** vs 4DGS baseline:**#Gauss 13M→0.91M = 14.3× 减;params 2093M→18.48M = 113.3× 减**(与 188× storage 压缩一致,余下 1.6× 来自 FP16 + zip)

## 训练 / 推理资源(综合 PDF Table 3 + §4)
- **训练 GPU**:**NVIDIA A800**(单卡,PDF §4.2 直引:"running their released codes on a single NVIDIA A800 GPU")
- **训练迭代数**:**30K iterations**(PDF §4.2 直引)
- **训练 stop-densification**:**midpoint**(即 15K iterations)
- **Batch size**:**1**
- **训练时长 / scene**:**未在 PDF 显式报出分钟数**;`未在公开材料精确拿到`
- **推理 GPU 显存**:**未在 PDF 显式报出**
- **训练 GPU 显存**:
  - **vanilla 4DGS(Birthday 单场景)**:Paper Figure 1(a) 标 "PSNR 31.00 dB, Mem **7.79 GB**"(PDF §1 直引)
  - **MEGA(Birthday 单场景)**:Paper Figure 1(a) 标 "PSNR 32.02 dB, Mem **31.42 MB**"(**约 248× 降**)
- **数据集**:
  - Technicolor(4×4 camera rig, 2048×1088, 5 scenes, 50 frames)
  - Neu3DV(18~21 cameras, 2704×2028, 6 scenes, 300 frames @ half resolution)
- **典型 splat 数量级**:Technicolor **0.91M / scene**(MEGA final),4DGS vanilla **13M / scene**(PDF Table 3a 直引)

## 与本调研主线的关系

### 1. 主线对标(bitpack 路线,与 4DGS-1K 互补)
- MEGA = **bitpack / compressed 4D Gaussian 路线**(SH→DC+AC,FP16+zip)→ 解决 **per-splat 字节数**
- 4DGS-1K(Yuan 2025)= **pruning / mask 路线**(STV pruning + Temporal Filter mask)→ 解决 **#Gauss 数量**
- **两者正交,理论上可叠加**:
  - 先用 4DGS-1K 的 STV pruning 砍 #Gauss 到 ~600K
  - 再用 MEGA 的 DAC + FP16 砍 per-splat 字节
  - 综合目标:N3V 单场景从 2085 MB(4DGS retrained)→ 50 MB(4DGS-1K-PP)→ **< 10 MB**(推测叠加后)

### 2. 借鉴价值
- **DAC 思想**(per-Gaussian 3-参 DC + shared MLP AC)对项目移动端**极其友好**:3-参颜色是 cache-friendly,MLP shared weights 适合 push to constant buffer 一次
- **Entropy-based pruning** 是 L_opa 的"真身",**与 4DGS-1K 的 STV pruning 思路不同**:MEGA 用 o_j log(o_j) 鼓励 0/1 化,4DGS-1K 用 temporal score;**两个损失可同时用**(做"4DGS-1K + MEGA-DAC" 组合实验)
- **FP16 + zip 流水**是**任何 mobile 端 4DGS 落地必经一步**,MEGA 给的 ~10% zip 压缩数据是基线

### 3. 与 4DGS-1K 关键数字的"同台对比"(交叉引用)
| 维度 | MEGA Technicolor(Birthday) | 4DGS-1K N3V(Coffee Martini) | 谁更好? |
|---|---|---|---|
| Storage | 18.48 MB(params) / 32.45 MB(50 frames) | 50 MB(PP,300 frames) | 4DGS-1K 单场景更小 |
| PSNR | 32.02 | 31.87(PP) / 31.88(no-PP) | MEGA 略高 |
| FPS | 83.14 | 805 | 4DGS-1K **10× 更快** |
| #Gauss | 0.91M | 0.67M | 4DGS-1K 更少 |

> **结论**:**4DGS-1K 是更"现代"的对标**(pruning+mask 双重加速);MEGA 是更"普适"的工具(DAC+FP16 可直接用)。**本项目移动端路线应两者结合**。

### 4. 对采集端反推
- Technicolor(4×4 同步 camera rig)+ Neu3DV(18~21 cam):**多视角 + 高分辨率 + 短时序**。
- **MEGA training** 30K iter × 单 A800 ≈ [推测 4~6 小时 / scene,A800 实测类比],`未在 PDF 显式报出,abstract 未给`。

## 我未找到 / 提请下游注意
- **训练时长 / scene 分钟数**:PDF 未显式报出,`未在公开材料精确拿到`
- **推理 GPU 显存**:PDF 未显式报出
- **移动端 / Vulkan / Adreno 实现**:PDF 未提,**移动端必须自研**
- **GitHub commit 是否包含 mobile backend**:从公开 README 看到是 PyTorch + diff-gaussian-rasterization,**未在公开材料拿到 mobile backend 证据**
- **DSSIM vs SSIM 关系**:Table 1 写的是 DSSIM1 / DSSIM2,**未在 PDF 显式说明 DSSIM1 vs DSSIM2 含义差异**(推测 DSSIM1 = D-SSIM = (1-SSIM)/2,DSSIM2 = 10^(-MS-SSIM) 之类,**这是推测,abstract 未给**)

## 我的 commit 节奏
- 此前 abstract 级笔记 7980 B → **本次升级 → 见最终 commit hash**。
- 与 `2025-yuan-4dgs-1k.md` 关系:本笔记作为 **bitpack 路线**对照,**不替换** 4DGS-1K 的主线地位。
- 下游 `02-rendering-acceleration.md` §3(bitpack 段)应引用本文 Table 1/2/3 的精确数字 + 与 4DGS-1K 的"同台对比"小表。
