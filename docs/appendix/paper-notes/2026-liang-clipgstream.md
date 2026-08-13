# ClipGStream: Clip-Stream Gaussian Splatting for Any Length and Any Motion Multi-View Dynamic Scene Reconstruction

## 0. 基本信息

- **作者**: Jie Liang¹˒²*, Jiahao Wu¹˒²*, Chao Wang²‡, Jiayu Yang², Xiaoyun Zheng², Kaiqiang Xiong¹˒², Zhanke Wang¹, Jinbo Yan¹, Feng Gao³, Ronggang Wang¹˒²˒⁴†
  （*equal contribution，†corresponding author，‡co-corresponding author）[p1 直引]
- **机构**:
  1. Guangdong Provincial Key Laboratory of Ultra High Definition Immersive Media Technology, Shenzhen Graduate School, Peking University
  2. Pengcheng Laboratory
  3. Peking University
  4. MIGU Video Co., Ltd. [p1 直引]
- **年份**: 2026
- **arxiv-id**: 2604.13746v1 [cs.CV], 15 Apr 2026 [p1 侧边栏直引]
- **主页**: https://liangjie1999.github.io/ClipGStreamWeb/ [p1 abstract 末尾直引]
- **GitHub**: 全文未出现代码仓库链接 [PDF 全文核验，未找到]

> ⚠️ **venue 存疑（P36 铁律）**：任务单描述为 "CVPR 2026"，但**本 PDF 全文无任何 CVPR 标记**——无 CVPR 页眉、无 camera-ready 版式、正文/致谢均未提接收信息，首页仅有 arXiv 预印标识。PDF 元数据 creator 为 `WPS 演示`、creationDate `2025-11-13`。
> 因此本 note **按 arXiv pre-print 记录**，venue 字段留待 `cron-paper-upgrade` 上接收名单后再改。

## 0.5 元数据

- **venue**: arXiv pre-print（**非** PDF 可证的 CVPR 2026，见上方警告）
- **arxiv-id**: 2604.13746
- **s2-id**: (待补)
- **本地 PDF**: `.pdfs/2604.13746.pdf`（16.2 MB，11 页）
- **homepage**: https://liangjie1999.github.io/ClipGStreamWeb/
- **status**: PDF 全文核验 ✅（pymupdf 抽取，正文 + 6 张表格 + 66 条 references 完整）
- **收录来源**: 定向指派（subagent A，任务 8）
- **1-hop 引用**: 见 §8
- **survey_section**: 5 (派系 D → 流式落地，对应 Rendering Acceleration 章节)
- **faction**: D
- **评级**: T1
- **收录日期**: 2026-08-10

## 1. 一句话总结

把长多视角动态视频切成若干 clip，**第一个 clip 作为 Reference Clip 训练出锚点 / 静态特征 / 解码器并全程冻结继承**，后续每个 Source Clip 只学「独立的时空场 STF + 残差锚点」，从而在 clip 粒度（而非帧粒度）做流式优化，兼顾 Frame-Stream 的可扩展性与 Clip 方法的时序稳定性。

## 2. 摘要（核心 3 段）

**段 1 · 问题** [abstract + §1 直引]
动态 3D 重建对 VR/MR/XR 沉浸媒体是刚需，但长序列 + 大幅运动仍难。现有动态高斯方法二分：
- **Frame-Stream**（Dynamic3DGS [26]、3DGStream [27]）逐帧优化，可扩展到超长序列，但**帧间抖动 + 误差累积**；
- **Clip**（4DGS [28]、4DGaussian [29]、SpaceTimeGS [30]）对约 300 帧联合优化，局部一致但**显存 / 计算开销大、序列长度受限**。
且两种范式**都难处理大幅 / 快速运动**。

**段 2 · 方法** [abstract + §3 直引]
提出 **Clip-Stream** 混合框架：序列切成 N 个 clip（每 clip M 帧），`Clip₀` 为 Reference Clip，`Clipₙ, n∈[1,N-1]` 为 Source Clip。两条互补策略：
- **Intra-clip 训练策略**：每个 clip 配**独立时空场 STF**建模局部运动；对 Source Clip 用**残差锚点补偿（RAC）**补上新出现 / 大位移的结构。
- **Inter-clip 继承策略**：Source Clip **继承 Reference Clip 的锚点、静态特征、解码器并全部冻结**，保证跨 clip 结构一致。

**段 3 · 结果** [Tab 1-4]
- Long 360（1,400 帧）**PSNR 24.54**，全指标最优，超过所有 Frame-Stream / Clip baseline，甚至超过静态方法在 frame 0 的上界参考（3DGS 24.13）。
- N3DV 5 场景 300 帧 **PSNR 32.53 / 106 FPS / 0.5h 训练 / 98MB**，质量、训练时间、模型体积同时最优。
- flame salmon 1,200 帧 **PSNR 29.40**，LPIPS 0.144 最优。
- VRU (GZ) **PSNR 30.67 / LPIPS 0.137**，动态方法中最优。

## 3. 派系分类（INDEX 同步）

- **派系 B**（4DGS 加速 / 动静态分离）为主 —— 核心机制正是 `f_s`（静态）/ `f_d`（动态）特征解耦 + 静态分支冻结复用，与派系 B 定义高度吻合。
- **兼具派系 D 属性**（移动端 / 流式落地）—— clip 级流式训练、98MB 模型、逐 clip 增量产出，天然贴近流式分发场景。
- 论文自称开辟第三范式 "**Clip-stream methods**"（Tab 1 / Tab 3 中单列一栏），介于 Frame-Stream 与 Clip 之间。
- ⚠️ 派系归属需人工 review 确认（P27 双盲协议）。

## 4. 方法

### 4.1 表示（§3.1 + §3.2.1）

基于 ScaffoldGS [56] 的 anchor 思路，但**锚点属性被大幅精简**：

| | ScaffoldGS [56]（p4） | ClipGStream（p4） |
|---|---|---|
| 位置 | `μ_a ∈ R³` | `μ ∈ R³` |
| 特征 | `f_a ∈ R³²` | `f_s ∈ R⁶⁴`（静态）+ `f_d ∈ R⁶⁴`（动态） |
| 尺度 | `l_a ∈ R³` | 无 |
| offsets | `O_a ∈ R^{k×3}` | 无 |

- 锚点 `A₀` 由 `Clip₀` **全部帧**融合的 COLMAP [57,58] 点云初始化。
- **动态特征来自时空场 STF**：`STF₀` = 4D hash grid `h₀` + fully fused MLP `φ₀`
  `f_{d,0} = φ₀(h₀(μ₀, t))`  … Eq.(4)
- **解码为 Temporal Gaussians** [31]（沿用 LocalDyGS 的 Temporal GS 概念）：
  `G_{t,0} = d([f_{s,0}; f_{d,0}])`  … Eq.(5)
  随后光栅化 + 多视角图像监督。Reference Clip 阶段联合优化 `μ₀`、`f_{s,0}`、`STF₀`、解码器 `d`。

**特征解耦的实证依据**（Fig 3, p4）：单独解码 `f_s` 渲染 → 得到 clip 内全部背景信息（故可跨 clip 共享）；单独解码 `f_d` → 学到控制动态内容可见性的残差信息（故必须 clip-independent）。这是整个继承策略成立的前提。

### 4.2 Intra-clip：残差锚点补偿 RAC（§3.2.1，Fig 4 p4）

继承来的锚点在大运动下位移过大，单靠形变场表达不了 → 补新锚点，但要防冗余增长。**几何感知去重（Dedup）**：

1. `A_n = A₀ ∪ A^r_n = A₀ ∪ Dedup(A^c_n, A₀)`  … Eq.(6)，`A^c_n` 是 `Clip_n` 自己的 COLMAP 锚点
2. **Point → Field**：对每个 `p ∈ A₀` 建球，半径取到 3 近邻（KNN）的平均欧氏距离
   `r = (1/3) Σ_{i=1..3} ‖p_i − p‖₂`  … Eq.(7)
   → 形成"球形覆盖场"，描述 `A₀` 已表达的区域
3. **Field → Residual**：对候选 `q ∈ A^c_n` 算到覆盖面的**有符号距离** SDF（用 Open3D [59]）
   - `SDF(q) > 0`（球外，Fig 4 绿框 q₂）→ 保留为残差锚点
   - `SDF(q) < 0`（球内，Fig 4 红框 q₁）→ 丢弃

### 4.3 Intra-clip：Clip-specific STF（§3.2.1 末）

锚点的动态特征跨 clip 差异大，**共享单个 `STF₀` 会导致后续 clip 覆写先前学到的动态**（§4.4 消融原话）。故每 clip 分配独立时空场 `STF₁ … STF_{N-1}`。

### 4.4 Inter-clip：继承策略（§3.2.2）

Source Clip 训练时**冻结**三样东西：

| 组件 | 状态 | 作用 |
|---|---|---|
| 锚点 `A₀` | 冻结 | 静态结构的稳定参考，防局部重优化 |
| 静态特征 `f_{s,0}` | 冻结 | 跨 clip 背景一致 → 抑制闪烁 |
| 解码器 `d(·)` | 冻结 | 几何/外观属性解码方式一致 |

新增部分可训练：残差锚点 `A^r_1` 及其**可学习残差静态特征** `f^r_{s,1}`，拼接成
`f_{s,1} = [f_{s,0}; f^r_{s,1}]`  … Eq.(9)
`f_{d,1} = φ₁(h₁(μ₁, t))`  … Eq.(10)
`G_{t,1} = d([f_{s,1}; f_{d,1}])`  … Eq.(11)

### 4.5 损失（§3.3）

- 体积正则（促使 Temporal Gaussian 紧凑、只表达局部区域）[56,60]：
  `L_v = Σ_{i=1..M} Prod(s^i_t)`，M = 活跃 Temporal Gaussian 数，`s^i_t` = 第 i 个高斯在 t 时刻的尺度 … Eq.(12)
- 总目标：`L = (1 − λ_SIM)·L₁ + λ_SIM·L_SIM + λ_v·L_v` … Eq.(13)
- ⚠️ `λ_SIM` / `λ_v` **具体取值全文未给** [PDF 核验，未找到]

### 4.6 实现细节（§4.1，p6）

- 所有 MLP 均 **2 层 + ReLU**，输出接 Sigmoid 或归一化
- 静态 / 动态特征维度均 **64**
- Adam [61]，clip 内沿用 3DGS [54] 的学习率调度
- **关键 trick**：学习率调度器在**每个 clip 训练开始时重新初始化**，不继承 Reference Clip 的状态——否则 lr 随训练推进变得过小，妨碍后续 clip 的有效优化

## 5. 实验

### 5.1 数据集（§4.2，p6）

| 数据集 | 规格 | 用途 |
|---|---|---|
| **Long 360** [31,62] | **1,400 帧**，4K，**36 相机 360° 环形**，篮球比赛；cam 0/10/20/30 测试、其余 32 训练，图像 **下采样 2×** | 主战场：高速运动 + 超长序列 |
| **N3DV** [14] | 21 相机，2704×2028，30 FPS；train/test 遵循 [27,38,40] | 标准基准：细粒度运动。5 场景 × 300 帧；另测 flame salmon **1,200 帧** |
| **VRU (GZ)** [39] | 34 相机，1920×1080，25 FPS，真实篮球赛；设置同 Swift4D [39] | 泛化 + 大运动幅度鲁棒性，250 帧 |

### 5.2 Baseline

- **静态**（仅在 frame 0 评测，作为上界参考）：2DGS [23]、3DGS [54]、ScaffoldGS [56]、GOF [21]
- **Frame-Stream**：StreamRF [40]、3DGStream [27]、iFVC [44]、HiCoM [45]、4DGC [64]
- **Clip**：NeRFPlayer [37]、HyperReel [36]、K-Planes [46]、HexPlane [47]、MixVoxels [13]、4DGaussian [29]、RealTimeGS/4DGS [28]、SpaceTimeGS [30]、Swift4D [39]、LocalDyGS [31]、Grid4D [42]、4K4D [65]、ENeRF [66]、Dy3DGS [26]

## 6. 性能数字（**必标 PDF 页码**）

### Tab 1 · Long 360，1,400 帧（**p6**）

| 类别 | 方法 | PSNR ↑ | DSSIM₁ ↓ | DSSIM₂ ↓ | LPIPS ↓ |
|---|---|---|---|---|---|
| 静态(frame 0) | 2DGS [23] | 23.80 | 0.085 | 0.042 | 0.181 |
| 静态(frame 0) | 3DGS [54] | 24.13 | 0.087 | 0.040 | 0.159 |
| 静态(frame 0) | ScaffoldGS [56] | 23.53 | 0.096 | 0.048 | 0.203 |
| Frame-Stream | 3DGStream [27] | 21.94 | 0.105 | 0.053 | 0.200 |
| Frame-Stream | iFVC [44] | 22.35 | 0.101 | 0.050 | 0.192 |
| Clip | 4DGaussian [29] | 22.01 | 0.103 | 0.052 | 0.198 |
| Clip | Swift4D [39] | 23.01 | 0.094 | 0.048 | 0.180 |
| Clip | LocalDyGS [31] | 23.11 | 0.093 | 0.046 | 0.178 |
| **Clip-stream** | **ClipGStream (Ours)** | **24.54** | **0.079** | **0.036** | **0.146** |

> 关键差距：**+1.43 dB vs 最强 Clip 基线 LocalDyGS**，**+2.19 dB vs 最强 Frame-Stream 基线 iFVC**，且**+0.41 dB 超过静态 3DGS 的 frame-0 上界参考**。

### Tab 3 · N3DV，5 场景 × 300 帧（**p6**）

| 方法 | PSNR ↑ | DSSIM₁ ↓ | DSSIM₂ ↓ | FPS ↑ | Time ↓ | Size ↓ |
|---|---|---|---|---|---|---|
| StreamRF [40] | 28.26 | - | - | 10.9 | - | 5310MB |
| 3DGStream [27] | 31.67 | - | - | **215** | 1.0h | 1230MB |
| 4DGC [64] | 31.58 | - | - | - | - | - |
| HiCoM [45] | 31.17 | - | - | - | - | - |
| NeRFPlayer [37] | 30.69 | 0.034 | - | 0.05 | 6.0h | 5130MB |
| HyperReel [36] | 31.10 | 0.036 | - | 2 | - | 360MB |
| K-Planes [46] | 31.63 | - | 0.018 | 0.3 | 5.0h | 311MB |
| HexPlane [47] | 31.70 | - | 0.014 | 0.21 | 12.0h | 240MB |
| MixVoxels [13] | 31.73 | - | 0.015 | 4.6 | - | 500MB |
| 4DGaussian [29] | 31.02 | 0.030 | - | 30 | 0.67h | **90MB** |
| RealTimeGS [28] | 32.01 | - | 0.014 | 114 | 9.0h | >1000MB |
| SpaceTimeGS [30] | 32.05 | 0.026 | 0.014 | 140 | >5h | 200MB |
| LocalDyGS [31] | 32.28 | 0.028 | 0.014 | 105 | 0.58h | 100MB |
| **ClipGStream (Ours)** | **32.53** | **0.024** | **0.012** | 106 | **0.5h** | 98MB |

> **训练时间 0.5h 为全表最快**；FPS 106 排第 4（低于 3DGStream 215 / SpaceTimeGS 140 / RealTimeGS 114）；Size 98MB 排第 2（4DGaussian 90MB 更小）。

### Tab 4 · flame salmon，1,200 帧（**p7**）

| 方法 | PSNR ↑ | SSIM ↑ | LPIPS ↓ |
|---|---|---|---|
| 4DGaussian [29] | 28.89 | **0.952** | 0.196 |
| 4K4D [65] | 21.29 | 0.826 | 0.196 |
| ENeRF [66] | 23.48 | 0.894 | 0.259 |
| 3DGS [54] | 28.61 | 0.949 | 0.210 |
| Dy3DGS [26] | 25.91 | 0.880 | 0.255 |
| LocalDyGS [31] | 28.15 | 0.912 | 0.153 |
| **ClipGStream (Ours)** | **29.40** | 0.917 | **0.144** |

> ⚠️ **SSIM 非最优**：0.917 < 4DGaussian 0.952 / 3DGS 0.949。论文正文对此未作解释。

### Tab 2 · VRU (GZ)，250 帧（**p6**）

| 方法 | PSNR ↑ | SSIM ↑ | LPIPS ↓ |
|---|---|---|---|
| GOF [21] (静态) | 30.39 | 0.949 | 0.141 |
| 2DGS [23] (静态) | **30.78** | 0.949 | 0.187 |
| 3DGS [54] (静态) | 30.50 | 0.949 | 0.171 |
| 4DGaussian [29] | 28.32 | 0.930 | 0.186 |
| SpaceTimeGS [30] | 27.42 | 0.926 | 0.193 |
| LocalDyGS [31] | 30.58 | 0.944 | 0.173 |
| **ClipGStream (Ours)** | 30.67 | 0.946 | **0.137** |

> ⚠️ PSNR 30.67 **未超过静态 2DGS 的 30.78**（静态方法仅在 frame 0 评测，论文明确标为 upper-bound reference）；在动态方法中最优，LPIPS 0.137 为全表最优。

### Tab 5 · 消融：DI / RAC，Long 360（**p8**）

| 配置 | PSNR ↑ | DSIM₁ ↓ | DSIM₂ ↓ | LPIPS ↓ | Δ PSNR |
|---|---|---|---|---|---|
| w/o DI（解码器继承） | 24.34 | 0.081 | 0.038 | 0.152 | −0.20 |
| w/o RAC（残差锚点补偿） | 23.62 | 0.083 | 0.044 | 0.160 | **−0.92** |
| ours | 24.54 | 0.079 | 0.036 | 0.146 | — |

> **RAC 是更关键的模块**（−0.92 dB vs DI 的 −0.20 dB）。

### Tab 6 · 消融：clip 训练策略，Long 360（**p8**）

| 策略 | PSNR ↑ | DSSIM₁ ↓ | DSSIM₂ ↓ | LPIPS ↓ |
|---|---|---|---|---|
| Independent Training（各 clip 完全独立） | 21.85 | 0.142 | 0.068 | 0.316 |
| Shared STF（全序列共享一个 STF） | 23.11 | 0.093 | 0.046 | 0.178 |
| ours | 24.54 | 0.079 | 0.036 | 0.146 |

> **完全独立训练崩得最惨（−2.69 dB）**，原因是各 clip 锚点稀疏化；共享 STF 则是后续 clip 覆写先前动态（−1.43 dB）。
> ⚠️ **数据巧合存疑**：Shared STF 行 `23.11 / 0.093 / 0.046 / 0.178` 与 Tab 1 中 LocalDyGS [31] 行**四个数字完全一致**。可能是复用了 LocalDyGS 结果作为该消融的等价实现，也可能是排版错误——论文未说明 [PDF 核验，正文无解释]。

### 定性 / 稳定性证据

- **Fig 1(b,c) p1**：cross-clip 残差热力图显示闪烁被有效抑制；flame salmon 上同时超越 SOTA 的重建保真度与训练效率
- **Fig 5 p5**：去掉 RAC / AI / 两者，相邻 clip 残差热力图在**静态区域**出现强响应（= 闪烁）；全开则平滑
- **Fig 8 p8**：不继承解码器 → 渲染明显模糊；继承 → 细节清晰
- **Fig 9 p8**：LocalDyGS 在小 M 下时序不稳、大 M 下**直接训不动**；ClipGStream 在长短序列上 PSNR 均更优

## 7. 评估（对本项目 4DGS 移动端渲染的相关性）

**相关性：中等偏上（B+）**，但**不是**移动端方向的直接可用件。

✅ **可用点**
1. **N3DV 98MB / 106 FPS / 0.5h** 这组数字在派系 B 里属第一梯队，且是**同时**拿下质量 + 训练时间 + 体积的少数工作，可作 README 论据表的对照点。
2. **静态/动态特征解耦 + 静态分支全程冻结**——冻结的 `A₀ + f_{s,0} + d` 对移动端意味着**这部分可一次性下发并常驻**，每个 clip 只需增量传输 `STF_n + 残差锚点 + f^r_{s,n}`。这个「一次基座 + 逐 clip 增量」的结构与流式分发天然契合，是本项目最值得借鉴的一点。
3. **clip 粒度而非帧粒度**的流式设计，规避了 Frame-Stream 的误差累积，同时把峰值显存限制在单 clip 内——对端侧内存受限场景是正确的方向。
4. **几何感知去重（球形覆盖场 + SDF）** 是个轻量、可独立复用的锚点增量准则，不依赖本文其余组件。

⚠️ **不可直接用 / 需警惕**
1. **完全没有移动端 / 端侧实验**。FPS 全部在（未指明型号的）桌面 GPU 上测，106 FPS 不能外推到手机。
2. **训练侧工作，非推理侧**。本文优化的是"如何训得稳、训得快"，对**推理时的算力 / 带宽 / 功耗零贡献**——本项目主线是移动端渲染加速，二者只在表示层面交集。
3. **每 clip 一个独立 STF（4D hash grid + MLP）** 是存储隐忧：N 个 clip 就是 N 份 hash grid。Tab 3 的 98MB 是 300 帧 / 少量 clip 的结果，**1,400 帧 Long 360 的模型体积全文未报告** —— 长序列下 size 如何增长是关键未知数，直接影响端侧可行性。
4. abstract 声称 "reduced memory overhead"，但**全文没有任何训练显存 / 峰值内存的测量表**，仅 Tab 3 有模型 Size。该 claim 未被实验支撑 [PDF 核验，未找到对应实验]。

📌 **信息缺口（复现或引用前需补）**
- clip 长度 **M 的具体取值全文未给**；Long 360 的 clip 数 N 也未明说（Fig 9 提到 "LocalDyGS 140 Clips video"，暗示 1400 帧 / 140 clip → M=10，但**未在正文确认**）
- 训练迭代数、GPU 型号、锚点数量规模、`λ_SIM` / `λ_v` 取值 —— 均缺失
- Long 360 的模型体积 / FPS（仅 N3DV 报了效率指标）

## 8. 引用（paper 自己引了什么）

共 **66 条 references**（p9-p11）。骨架依赖：

- **基座表示**：3DGS [54] Kerbl et al.、ScaffoldGS [56] Lu et al.（anchor 范式）、EWA splatting [55] Zwicker et al.
- **最直接的前作**：**LocalDyGS [31]**（Wu et al., arXiv 2507.02363）—— Temporal Gaussians 概念、Long 360 数据集均出自此文，且作者高度重叠（Jiahao Wu、Ronggang Wang 等）。本文可视为 LocalDyGS 的长序列 / clip-stream 扩展。
- **Frame-Stream 对标**：StreamRF [40]、Dynamic3DGS [26]、3DGStream [27]、iFVC [44]、HiCoM [45]、4DGC [64]、Instant Gaussian Stream [18]
- **Clip 对标**：4DGS/RealTimeGS [28]、4DGaussian [29]、SpaceTimeGS [30]、Swift4D [39]、Grid4D [42]、K-Planes [46]、HexPlane [47]、MixVoxels [13,38]
- **形变场系**：D-NeRF [48]、Nerfies [35]、DeformableGS [34]、SC-GS [49]、DynMF [50]、Gaussian-Flow [51,52]、NSFF [53]
- **工具链**：COLMAP [57]、PatchMatch MVS [58]（本组自研）、Open3D [59]（SDF）、Adam [61]
- **数据集**：N3DV [14]、VRU [39]、Long 360 [31,62]（[62] 指向 AVS 组织 https://www.avs.org.cn/）

> **自引密集**：[6][9][10][18][25][31][33][39][44][58] 均为 Ronggang Wang / PKU-SZ 组工作，占比约 15%。

## 9. Insight（**必填**）

1. **"冻结基座 + 增量分支" 是流式落地的正确骨架**。本文最大的可迁移结论不是 clip-stream 本身，而是证明了：动态场景中**静态部分只需学一次**（`f_s` 单独解码即得完整背景，Fig 3），后续全部冻结不但不掉点，反而**是抑制闪烁的必要条件**（Fig 5：去掉 AI 后静态区域残差热力图强响应）。本项目若做移动端流式，应当照抄这个拓扑：基座一次下发 + 每 clip 小增量。
2. **闪烁是"静态区被反复重优化"造成的，不是动态建模不够。** 这是个反直觉但被 Fig 5 直接证实的判断——跨 clip 残差热力图的强响应出现在**静态区域**。任何做 clip 切分的方案，第一优先级应是锁死静态分支，而非加强时序平滑损失。
3. **RAC > DI（0.92 dB vs 0.20 dB，Tab 5）**：大运动场景下，"补新锚点"比"统一解码器"重要得多。若本项目要做移动端裁剪版，DI 可保留（近乎零成本：复用同一个 MLP），RAC 的 KNN + SDF 去重则是每 clip 一次的预处理开销，需评估端侧可行性——但它是不能砍的那个。
4. **学习率调度器每 clip 重置**（§4.1）是个容易忽略但显然必要的工程细节——任何"继承式"增量训练方案都会踩这个坑（继承 lr 状态 → 后续 clip 学不动）。值得记入本项目的增量训练 checklist。
5. **警惕长序列下的存储增长**：每 clip 独立 STF 的设计在质量上是必要的（Tab 6 共享 STF −1.43 dB），但存储随 N 线性增长，而论文**恰好没报告 1,400 帧下的模型体积**。若本项目引用其 98MB 数字，必须注明"300 帧 N3DV 设定"，不能外推到长序列。

## 11. 1-hop 关系图

**向上（本文引用的关键前作）**
```
3DGS [54] ──────────────┐
ScaffoldGS [56] ────────┼──→ ClipGStream
LocalDyGS [31] ─────────┘    （最近前作，同组，
  ├─ Temporal Gaussians       Temporal GS + Long 360
  └─ Long 360 dataset          均继承自此）

对标范式：
  Frame-Stream: StreamRF[40] → Dynamic3DGS[26] → 3DGStream[27] → iFVC[44]/HiCoM[45]/4DGC[64]
  Clip:         K-Planes[46]/HexPlane[47] → 4DGaussian[29]/4DGS[28] → SpaceTimeGS[30]/Swift4D[39]
```

**向下（被引用的后续工作）**
- 暂无 —— 2026-04 预印，尚未观察到引用 [待 s2 补全]

**本项目 note 内横向关联（待建立）**
- `LocalDyGS`（[31]，最直接前作）—— 若库中尚无 note，**建议 1-hop 收录**，优先级高于本文
- `Swift4D` [39]、`3DGStream` [27]、`SpaceTimeGS` [30] —— 常见对标，宜确认 note 齐全

---

## 抽取过程说明（可复核）

- 工具：`pymupdf 1.28.0` / MuPDF 1.29.0，`page.get_text()` 逐页抽取，11 页共 48,995 字符
- 抽取警告：MuPDF 报 `unknown cid font type` / `no XObject subtype specified`——**图注内嵌的矢量文字（Fig 1、Fig 3 的标签）抽出为乱码**，故 Fig 1/Fig 3 的描述依据其**正文 caption**（caption 本身抽取正常），未依赖图内文字
- **正文、全部 6 张表格、66 条 references 抽取完整可读**，本 note 所有数字均逐一比对原文
- 落盘全文备份：`<scratchpad>/paper_8.txt`

---
*本 note 由 subagent A 基于 PDF 全文核验写入（P36 铁律：数字均标 Table 编号 + PDF 页码）。
*⚠️ **venue 与任务单描述不符**：任务单称 CVPR 2026，PDF 实为 arXiv 2604.13746v1 预印，无任何接收标记——已按 PDF 为准记录，请 parent 裁决。
*派系分类（B / 兼 D）待人工 review 确认。
*§7 已标注 4 项信息缺口（M/N 取值、GPU、长序列模型体积、显存 claim 无实验支撑），引用前需注意。
