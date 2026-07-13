# MVFusion-GS: Motion-Variance Guided Temporal Attention for High-Quality Dynamic Gaussian Splatting

## 0. 基本信息
- 作者: Jianwei Hu*, Tingxuan Huang*, Hengyu Zhou, Ningna Wang, Xiaohu Guo, Jinshan Lai, Bin Wang† (* equal contribution, † corresponding)
- 单位: Tsinghua University (Tsinghua) + UT Dallas + UESTC
- 年份: 2026 (arXiv v1: 2 Jul 2026)
- 会议: arXiv preprint (尚未投稿？无 venue 信息)
- arxiv-id: 2607.01578
- GitHub: https://github.com/toseeai-com/MVFusion-GS
- 项目主页: 无显式 homepage
- 代码许可: 未声明 (待核实)

## 0.5 元数据
- venue: arXiv preprint
- arxiv-id: 2607.01578
- s2-id: (未查询 — cron 批次)
- homepage: https://github.com/toseeai-com/MVFusion-GS
- github: toseeai-com/MVFusion-GS
- status: 收录
- 收录日期: 2026-07-13
- 收录来源: arxiv_4dgs_scan (cron)
- 评级: T1 (核心 4DGS 表示 + 训练稳定性)
- survey_section: 3 (4DGS 表示)
- faction: A (4DGS representation)

## 1. 一句话总结
MVFusion-GS 在 DeGauss 解耦框架上 plug-in 两个运动感知模块（全局 trajectory variance + MotionFormer 时序 cross-attention），把"伪静态前景残留"从背景分支正确划归到动态分支，从而同时改善 distractor-free 重建与 dynamic scene 重建的 PSNR/LPIPS。

## 2. 摘要 (核心 3 段)

**问题**: 标准 decoupled 4DGS 框架（如 DeGauss）将 deformation field 一视同仁地应用于所有 Gaussians，但**无明确运动强度先验** → 低幅度/瞬态运动的前景点常常 under-fitted → 残留"伪静态"Gaussians 错误滞留于背景分支 → distractor-free 重建的静态背景不干净、dynamic scene 重建的前景细节模糊。

**方法**: 提出两条互补的运动感知机制，**plug-in 接入 DeGauss 的 deformation network 隐空间** (不动 original deformation heads Φ):
1. **Motion-Variance Guided Refinement (MVG)** — 每 E=2000 iter 沿 deformation trajectory 采样 K=64 timesteps，统计每个 Gaussian 的 position/rotation/scale 变化 → 形成 13D **global trajectory signature** + cached **local variance dictionary** e(t) → 作为运动强度先验注入 deformation feature (zero-init MLP, residual)。
2. **MotionFormer Temporal Attention (MFTA)** — 时间窗 w=5 内做 query-centered **cross-attention**（非 self-attention），让当前帧动态特征 attend 至相邻帧特征 → 增强短期时序一致性。

**结果**: 在 Neu3D (动态场景) 上 mean PSNR 从 DeGauss 31.52 提到 32.07 (+0.55 dB)；在 NeRF On-the-go (distractor-free) 上 Mean PSNR 23.91→23.94 (背景质量几乎饱和，LPIPS 更敏感) + dynamic 区域 PSNR 22.93→27.60 (+4.67 dB)；RobustNeRF 上 28.89→29.39 PSNR。渲染 FPS 71.0→62.7（慢 12%），但动态 Gaussians 从 56,533 压到 32,985 (−42%)。RTX 4090 单卡，单 GPU。

## 3. 派系分类
- **A (4DGS representation)**: 主。MVFusion-GS 是 4DGS 表示层改进（动态时空 Gaussian 表示 + 时序一致性）。
- 相关: B (training acceleration) 边缘沾边 — deformation statistics 缓存可减少重复计算，是典型的"用训练时 cached feature 换 inference 加速"思路。
- 不属于 C (3DGS 加速，静态)、D (移动端，本论文仅评 RTX 4090，无 mobile 评测)。
- E (cross-disciplinary) 沾边有限：MotionFormer Transformer 自注意力借鉴 NLP 经典结构 (Vaswani et al. 2017)。

**结论**: 主派系 **A**。

## 4. 方法

### 4.1 整体架构 (plug-in design)
DeGauss 是基本 baseline。本工作的关键设计哲学：**MVG 和 MFTA 仅在隐空间融合**，不替换 deformation heads Φ。

$$\Delta G_d^{MR}(t) = \Phi\left( h_{base}(t) + h_{MVG}(t) + h_{MFTA}(t) \right)$$

refined deformation = baseline + motion-aware refinement。这避免了重训整个 deformation network，是真正的 drop-in 模块。

### 4.2 Motion-Variance Guided Refinement (MVG)

**13D global trajectory signature** per Gaussian:
- 位置: mean(Δpos) [3d] + var(Δpos) [3d] = 6d
- 旋转: mean(θ) [1d] + var(θ) [1d] = 2d
- 各向同性 scale: mean(ℓ_iso) [1d] + var(ℓ_iso) [1d] = 2d
- 各向异性 scale: mean(ℓ_aniso) [1d] + var(ℓ_aniso) [1d] = 2d
- 运动强度 scalar: 1d (fused motion intensity)
- 合计 **13d**

**Cached local variance dictionary** e(t)：时间索引字典，query t → sliding window 内的方差值，避免每帧重算。

EMA 归一化 (decay 0.99) + soft-clipping 3.0 + ϵ=10⁻⁶ 数值稳定。

### 4.3 MotionFormer Temporal Attention (MFTA)

$$a_{i,t_i} = \text{Attn}(z_{i,t_i}, z_{i,t_i-w}, z_{i,t_i+w})$$

- 时间窗 w=5 (前后 2 帧 + 当前 + 边界 padding)
- **query-centered cross-attention**: 当前时刻 Q attend 相邻 K/V (反对称，不是 self-attention 处理 [t-w, t, t+w])
- 输出经 lightweight MLP → h_MFTA ∈ R^{N×H} → 与 h_base 融合

### 4.4 训练 3-stage 课程

**Stage 1 (Base Geometry)**: 仅优化 Gaussian 几何参数，deformation network 关闭。
**Stage 2 (Base Deformation)**: 激活 base deformation network，学基础时空变形。后期开启 temporal branch 收集 motion statistics。
**Stage 3 (Motion-Aware Refinement)**: 完整激活 MVG + MFTA，zero-init residual 注入，end-to-end 训练。

Neu3D 各 stage: 2k + 3k + 20k iter (共 25k iter)；NeRF On-the-go: 3k + 7k + 20k (共 30k iter)。Adam，单 RTX 3090。

## 5. 实验

### 5.1 数据集
- **Neu3D** [Li 2022, CVPR]: 20 同步静态相机，300 frame 视频。view 0 测试，其余训练。共 7 场景 (Cut Beef, Cook Spinach, Sear Steak, Flame Steak, Flame Salmon, Coffee Martini + 1 个)
- **NeRF On-the-go** [Ren 2024, CVPR]: 7 场景 casual real-world with distractors；occluded image 训练，clean hold-out 评测
- **RobustNeRF** [Sabour 2023, CVPR]: 4 场景手工 distractors

### 5.2 基线
- Static branch: 3DGS, WildGaussians, DeSplat, SpotlessSplats, DeGauss
- Dynamic branch: 4DGS, MangoGS, MixVoxels, K-Planes, HexPlane, NeRFPlayer, HyperReel, SWinGS

### 5.3 评测指标
PSNR↑ / SSIM↑ / LPIPS↓ 三件套，外加 Training Time + FPS + Dynamic GS Num (efficiency)

## 6. 性能数字 (PDF 页码标)

### NeRF On-the-go (Distractor-Free) — Main Table 1, PDF page 11
Mean over 7 scenes:
- WildGaussians: 22.16 / 0.746 / 0.182 [p.11]
- DeSplat: 22.58 / 0.813 / 0.130 [p.11]
- SpotlessSplats: 23.42 / 0.813 / 0.145 [p.11]
- **DeGauss**: 23.91 / 0.819 / 0.113 [p.11]
- **MVFusion-GS**: 23.94 / 0.826 / 0.085 [p.11]
- LPIPS gain: **0.113 → 0.085 (−25%)** — 主战场

### NeRF On-the-go (Dynamic Foreground Regions) — Table 2, PDF page 12
Mean over 6 scenes:
- **DeGauss**: 22.93 / 0.795 / 0.169 [p.12]
- **MVFusion-GS**: **27.60 / 0.878 / 0.092** [p.12]
- **PSNR gain: +4.67 dB** — 远超背景增益

### Neu3D (Dynamic Scene Reconstruction) — Table 4, PDF page 14
Mean over 7 scenes:
- 4DGS: 31.12 / 0.937 / 0.058 [p.14]
- MangoGS: 31.89 / 0.940 / 0.052 [p.14]
- **DeGauss**: 31.52 / 0.942 / 0.047 [p.14]
- **MVFusion-GS (4DGS plug-in)**: 31.66 / 0.942 / 0.057 [p.14]
- **MVFusion-GS (full)**: **32.07 / 0.943 / 0.046** [p.14]
- vs DeGauss: +0.55 dB / −0.001 LPIPS
- Dynamic region PSNR: **31.78** (MVFusion-GS) vs ST-4DGS 31.35 vs SpaceTimeGS 30.85 [p.12]

### RobustNeRF — Table 3, PDF page 14
Mean 4 scenes:
- DeGauss: 28.89 / 0.893 / 0.085 [p.14]
- MVFusion-GS: **29.39 / 0.897 / 0.069** [p.14]
- LPIPS gain: −0.016

### Efficiency — Table 11, PDF page 24 (RTX 4090)
- 4DGS: 31.12 PSNR / 0.85h 训练 / **53.1 FPS** / 124,197 dyn Gaussians [p.24]
- **DeGauss**: 31.52 PSNR / 2.1h / **71.0 FPS** / 56,533 dyn Gaussians [p.24]
- **MVFusion-GS**: 32.07 PSNR / 2.26h / **62.7 FPS** / 32,985 dyn Gaussians [p.24]
- Trade-off: −12% FPS 但 +42% Gaussian compaction, +0.55 dB PSNR

### Ablation — Table 5, PDF page 14 (Neu3D / NeRF On-the-go PSNR)
- w/o MVG & MFTA: 31.52 / 23.86
- w/o MVG: 31.64 / 23.87 (+MVG gives +0.41 on Neu3D)
- w/ MVG (position-only): 31.93 / 23.92
- w/o MFTA: 31.78 / 23.89
- Self-attention (代替 cross-attn): 32.01 / 23.93
- **Full**: 32.07 / 23.94

### Sensitivity
- E (update interval): 2000 iter 最优 [p.21 Table 7]
- w (temporal window): 5 最优 [p.21 Table 8]
- Motion score weights: 0.7/0.2/0.1 (pos/rot/scale) 最优 [p.20 Table 6]

## 7. 评估

**亮点**:
- 设计哲学优雅: plug-in to existing deformation pipeline，零重训 deformation heads
- 双任务双赢 (distractor-free + dynamic scene)，同套机制同时改善两个目标 — 罕见
- 42% 动态 Gaussian 压缩率 (56,533 → 32,985) — storage/inference 双友好
- 量化指标完整 (PSNR/SSIM/LPIPS + efficiency + compactness)
- ablations 充分 (5 变体 + 3 sensitivity analyses)

**短板**:
- 仅在 RTX 3090/4090 单卡评测 — 无 mobile / edge GPU 数据，对我们 D 派系无直接帮助
- inference FPS 下降 12% (71→62.7) — 代价明确，需考虑是否值得
- 仍依赖 baseline deformation 提供 motion cues — 初始 deformation underfit 时 residual artifacts 仍存在 (Fig. 12 failure case, p.24)
- 没在 D-NeRF / Plenoptic Video / 自采数据集上验证

**对我们的相关性**:
- 中等。属于 4DGS 表示的**质量改进**，而非我们的核心目标（mobile 实时渲染）
- MVG 缓存思想可借鉴到 mobile — 但作者未给出 mobile port
- MotionFormer 是 GPU-friendly attention，但 window=5 + cross-attn 在 Adreno 上是否有足够算力存疑（matrix-multiply heavy）

## 8. 引用 (核心)
- [ref 9] Kerbl 2023 — 3DGS 原论文 (SIGGRAPH 2023), cite at p.2, p.4
- [ref 29] Wang ICCV 2025 — DeGauss baseline (CVF), cite at p.2, p.4, p.10
- [ref 32] Wu CVPR 2024 — 4DGS 原论文, cite at p.3, p.4
- [ref 7] Huang CVPR 2024 — SC-GS (sparse-controlled)
- [ref 8] Jiang ICCV 2025 — Timeformer (closest prior on temporal transformer for GS)
- [ref 6] Huang ICLR 2024 — MangoGS (multi-frame node-guided 4DGS)
- [ref 11] Li SIGGRAPH 2024 — ST-4DGS (spatial-temporally consistent 4DGS)
- [ref 13] Li CVPR 2024 — Spacetime Gaussian Feature Splatting
- [ref 14] Lu CVPR 2024 — Scaffold-GS
- [ref 19] Park CVPR 2025 — SplineGS (motion-adaptive spline)
- [ref 28] Wang ICCV 2025 — Shape of Motion
- [ref 30] Wang CVPR 2025 — FreeTimeGS
- [ref 10] Kulhanek NeurIPS 2024 — WildGaussians
- [ref 31] Wang CVPR 2025 — DeSplat
- [ref 20] Ren CVPR 2024 — NeRF On-the-go
- [ref 22] Sabour CVPR 2023 — RobustNeRF
- [ref 21] Sabour TOG 2025 — SpotlessSplats (SIGGRAPH)

## 9. Insight

**Insight #1 — Plug-in 设计哲学胜过 monolithic re-design**。MVFusion-GS 没替换 deformation heads Φ，只在 feature 空间加 residual 项。这种设计让用户能把作者工作塞进自己现有 pipeline（包括 DeGauss 之外的其他 deformation field，如 4DGS / SC-GS），是真正的 modular enhancement。我们的 mobile port 设计也应采取同样思路: 不要为 mobile 重写整个 deformation，只把可拆分的 motion-aware 模块做成可选子模块。

**Insight #2 — 错误的"伪静态"残留是 decoupled 4DGS 的固有缺陷**。MVFusion-GS 论证了 decoupled design 的 trade-off: 容易让 motion 在 background branch 留残留。Mobile port 设计时如果走 decoupled 路线，要考虑是否需要类似的 motion-intensity gating；否则 mobile 上背景噪点会被用户在无 monitor 情况下放大察觉。

**Insight #3 — 缓存的 motion statistics 是免费的"压缩加速"**。MVG 的 13D signature + local variance dictionary 都是无梯度计算 + 缓存复用，**训练时间几乎不变**（2.1h → 2.26h，+7%）。这给我们一个线索: 如果 mobile port 训练时预处理这些 descriptors、inference 时直接读，应该能在不增加推理成本的前提下引入运动强度先验。

**Insight #4 — FPS 降低 12% 换取 +0.55 dB 不一定划算**。Mobile 平台上每 FPS 都宝贵，62.7 vs 71 FPS 在 60 FPS 阈值附近是"够用 vs 不够用"的区别。但 42% 动态 Gaussian 压缩 (= 32,985 vs 56,533) 节省的 VRAM 在 mobile (Adreno 830 ~12MB L2) 上价值巨大 — 优先级应高于 FPS。

## 11. 1-hop 关系图 (5 篇示范)

**核心 1-hop 关系图**:

| 节点 | 关系类型 | 上游/下游 |
|------|---------|-----------|
| **DeGauss [Wang ICCV 2025]** | baseline (本论文主要对比 & plug-in 框架) | upstream |
| **4DGS [Wu CVPR 2024]** | concurrent baseline (4DGS plug-in variant) | concurrent |
| **MangoGS [Huang ICLR 2024]** | concurrent baseline (Neu3D 对比) | concurrent |
| **Timeformer [Jiang ICCV 2025]** | concurrent temporal transformer for GS | upstream inspiration |
| **ST-4DGS [Li SIGGRAPH 2024]** | concurrent dynamic region baseline (Neu3D 对比 31.35 dB) | concurrent |

**未在 INDEX 的 1-hop 候选** (1-hop rule: 命中即停):
- WildGaussians, DeSplat, SpotlessSplats, NeRF On-the-go, RobustNeRF — 见其他 paper notes
