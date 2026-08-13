# MotionScale: Reconstructing Appearance, Geometry, and Motion of Dynamic Scenes with Scalable 4D Gaussian Splatting

## 0. 基本信息
- 作者: Haoran Zhou, Gim Hee Lee
- 单位: Department of Computer Science, National University of Singapore (NUS)
- 年份: 2026 (arXiv v1: 31 Mar 2026)
- 会议: arXiv preprint (未注明 venue)
- arxiv-id: 2603.29296
- GitHub: 未在 PDF 中显式给出
- 项目主页: https://hrzhou2.github.io/motion-scale-web/
- 代码许可: 未声明 (待核实)

## 0.5 元数据
- venue: arXiv preprint
- arxiv-id: 2603.29296
- s2-id: (未查询 — cron 批次)
- homepage: https://hrzhou2.github.io/motion-scale-web/
- github: (未在 PDF 中给出)
- status: 收录
- 收录日期: 2026-08-10
- 收录来源: paper note 抽取批次
- 评级: T1 (scalable 4DGS 表示 + cluster-centric motion field + 长时间序一致性)
- survey_section: 3
- faction: A (4DGS representation)

## 1. 一句话总结
MotionScale 提出 cluster-centric motion field（按 Gaussian 聚类共享 SE(3) 全局变换 + 多 basis 局部精修），并通过 progressive optimization（背景扩展 + 三阶段前景传播）把单目视频重建扩到长序列与大场景，在 DAVIS/DyCheck/NVIDIA 上同时刷新渲染质量与 3D tracking 精度。

## 2. 摘要 (核心 3 段)

**问题**: 现存 4DGS 重建方法在两种场景下失败：(1) **Under-constrained geometry** — 监督主要来自 view-dependent appearance，缺乏强 3D 结构约束；(2) **Accumulated temporal drift** — motion models 依赖 2D tracking priors，缺少 3D 感知，长序列累积误差导致几何坍塌与轨迹不一致。

**方法**: MotionScale 三个核心设计：
1. **Scalable Motion Field**: 把 dynamic Gaussians 按 canonical frame K-means 聚类成 K 个 cluster；每个 cluster 共享一个 SE(3) **global transformation** + B 个 fine-grained basis transformations；Gaussian 通过可学习系数 ∑w_b=1 加权 blend basis → 既表达局部非刚性变形、又保持几乎常数计算开销。
2. **Adaptive Control**: 仿 3DGS densification，对 motion-inconsistent cluster 做 split/cull；Stage 3 用 HDBSCAN + Agglomerative Clustering 判定子组质心距离是否超阈值，触发时复制参数初始化两个新 cluster。
3. **Progressive Optimization**: 增量加入 T_new 新帧，先做 background extension（采样新可见区域 + joint pose refinement + shadow Gaussians），再做 foreground propagation 的三阶段：Initial Alignment（单向 tracking loss）/ Short-term Consistency（双向 loss）/ Long-term Refinement（跨全序列 + 联合优化 + ARAP 正则）。

**结果**: DyCheck NVS PSNR 17.98（vs Shape-of-Motion 16.72, +1.26 dB）；NVIDIA NVS PSNR 26.75（vs SoM 23.37, +3.38 dB）；DyCheck 3D tracking EPE 0.070（vs SoM 0.082, −14.6%）。Ablation 验证 Global Bases 退化到 16.70 PSNR，w/o Adaptive 17.21，w/o Shadow 16.26 — 全部组件都有显著贡献。

## 3. 派系分类
- **A (4DGS representation)**: 主。MotionScale 直接改进 4DGS 的 motion field 表示（cluster-centric SE(3) + basis blending），并把动态场景重建 pipeline 整体推到大场景长序列。
- 相关: B (training acceleration) 沾边 — progressive optimization 本身是 incremental training；adaptive control 类似 3DGS densification 的轻量化重制。
- 不属于 C (3DGS 静态加速)、D (mobile / edge，本论文仅评 RTX 4090，无 mobile 数据)。
- E (cross-disciplinary) 沾边：深度借鉴 K-means / HDBSCAN / Agglomerative / Procrustes / ARAP 这些经典 geometry processing 工具。

**结论**: 主派系 **A**。

## 4. 方法

### 4.1 整体架构 (canonical 3DGS + motion field)
基础是 3DGS [Kerbl SIGGRAPH 2023]：canonical Gaussians g⁰ᵢ = {μ⁰ᵢ, R⁰ᵢ, sᵢ, oᵢ, cᵢ}。动态场景通过 time-dependent motion field 把每个 canonical Gaussian 映射到时间 t 的状态。

### 4.2 Scalable Motion Field (cluster-centric)

**Partition**: K disjoint clusters {Cₖ}ᴷₖ₌₁ from K-means on canonical-frame 3D points (Sec. 3.3)。

**Hierarchical motion model per cluster**:
- **Global transformation** Gᵗₖ = [Rᵗₖ,ᵍ | tᵗₖ,ᵍ] ∈ SE(3)：整个 cluster 的刚性运动。
- **Local bases** Bᵗₖ = {(rᵗₖ,ᵦ, tᵗₖ,ᵦ)}ᴮᵦ₌₁：rᵗₖ,ᵦ 是 6D 连续旋转 [Zhou 2019]，tᵗₖ,ᵦ ∈ R³。
- **Per-Gaussian coefficient** wᵢ ∈ Rᴮ，约束 ∑wᵢ,ᵦ = 1。

**Blending equation** (Eq. 2–3):
```
Rᵗᵢ,ℓ = R(Σ wᵢ,ᵦ · rᵗₖ,ᵦ)
tᵗᵢ,ℓ = Σ wᵢ,ᵦ · tᵗₖ,ᵦ
μᵗᵢ = Rᵗₖ,ᵍ(Rᵗᵢ,ℓ μ⁰ᵢ + tᵗᵢ,ℓ) + tᵗₖ,ᵍ
Rᵗᵢ = Rᵗₖ,ᵍ Rᵗᵢ,ℓ R⁰ᵢ
```

**Scalability**: 单 Gaussian 仅受一个 cluster 影响 → cluster 数增加时单 Gaussian 计算几乎常数；每个 cluster 仅维护 (B+1) 个 SE(3)，memory 与总 Gaussian 数解耦。

### 4.3 Adaptive Control (split/cull)
- 在 Stage 3 触发，**HDBSCAN** on per-cluster 3D trajectories → density-based sub-clusters。
- **Agglomerative Clustering** 找到两个候选组 → 算质心距离 vs 阈值。
- 超阈值 → split；新 cluster 复制原参数初始化（保持拆分瞬间 motion state 一致）。
- 体积过小的 cluster → cull (删 Gaussian + 删 motion entry + 紧凑化索引)。

### 4.4 Progressive Optimization (核心)
**Priors**：π3 [Wang 2025] 提供 monocular depth + camera pose；SAM2 [Ravi 2024] 提供 foreground mask；CoTracker3 [Karaev ICCV 2025] 在 mask 内采样密集 grid 做 2D point tracks。

**Initialization** (Sec. 3.3)：
- Background：back-project depth maps → initial 3DGS point cloud。
- Foreground：sample 3D trajectories from (2D tracks, depth) → K-means → cluster init。
- Global transformations init via **Procrustes**；local bases 设为 identity。

**Background extension** (per batch of T_new frames)：
- Project existing background Gaussians → 标记未覆盖像素 → 用 monocular depth 初始化新 Gaussians。
- Targeted photometric loss on new frames。
- **Joint pose refinement** via end-to-end gradient on camera extrinsics（替代 SLAM / BA）。

**Foreground propagation — 3 stages** (Fig. 2(b))：
1. **Initial Alignment**：单向 tracking loss（已优化帧 t → 新帧 t′）；仅优化新帧 motion bases，其他参数冻结。
2. **Short-term Consistency**：双向 tracking loss over arbitrary (t, t′) in propagation window；梯度回流到旧帧。
3. **Long-term Refinement**：sample (t, t′) over entire sequence → global supervision + photometric (RGB) loss + **ARAP regularization** + 联合 Gaussian densification。

**Tracking loss** (Eq. 4–6)：
```
X_{t→t′}(p) = Σ μᵗ′ᵢ αΠ(1−α)   ← alpha-blend 3D positions
L_track = mean || Û_{t→t′}(p) − U_{t→t′}(p) ||
L_depth = mean || D̂_{t→t′}(p) − D_{t′}(U_{t→t′}(p)) ||
```

### 4.5 Shadow Gaussians (Sec. 3.3 末尾 + Sec. 4.5)
- 背景中的专用 shadow Gaussians，与动态 motion field 耦合（跟物体一起移动）。
- **故意不加 geometric / motion supervision**（阴影 3D 几何差、mask 时间不一致）→ 仅靠 RGB loss + segmentation constraint（防止与前景重叠）。
- 起点：starting frames 的粗 shadow mask → 随 background propagation 联合精修。

## 5. 实验

### 5.1 数据集
- **DAVIS** [Perazzi CVPR 2016]: 单目 casual 视频 + 复杂非刚性运动 + 自由相机运动；用于定性 dynamic scene reconstruction。
- **DyCheck** [Gao NeurIPS 2022]: 14 个真实动态场景，2 同步静态相机 + LiDAR 深度；sparse keypoint annotations (5–15 per seq) for long-term 3D tracking。
- **NVIDIA Dynamic Scenes** [Yoon CVPR 2020]: 标定多视角、人体 + 物体活动。
- 注: **未用 Neu3D / Plenoptic Video / D-NeRF**（与 MVFusion-GS 不同）。

### 5.2 基线
- 4D NeRF: T-NeRF, HyperNeRF, DynIBaR
- 4DGS: Deformable-GS, 4D Gaussians (Wu), Dynamic GM, 4D-Fly, Shape-of-Motion, GFlow, SplineGS
- Tracking: CoTracker / CoTracker3 + DA, TAPIR + DA, DELTA, SpatialTracker, DynMF

### 5.3 评测指标
- **NVS**: PSNR↑ / SSIM↑ / LPIPS↓
- **3D Tracking**: EPE↓ + δ⁰·⁰⁵₃D↑ + δ⁰·¹⁰₃D↑ (5cm / 10cm thresholds)
- **2D Tracking**: AJ↑ + ⟨δavg⟩↑ + OA↑ (Average Jaccard / position accuracy / Occlusion Accuracy)

## 6. 性能数字 (PDF 页码标)

### DyCheck + NVIDIA NVS — Table 1, PDF page 6
- T-NeRF: 15.60 / 0.55 / 0.55 | 20.76 / 0.59 / 0.17
- HyperNeRF: 15.99 / 0.59 / 0.51 | 20.05 / 0.57 / 0.18
- DynIBaR: 13.41 / 0.48 / 0.55 | — [p.6]
- Deformable-GS: 11.92 / 0.49 / 0.66 | —
- 4D Gaussians: 13.11 / 0.39 / 0.73 | 17.69 / 0.48 / 0.38
- Dynamic GM: 15.79 / 0.59 / 0.44 | 22.36 / 0.66 / 0.15
- 4D-Fly: 17.03 / 0.60 / 0.37 | 22.52 / 0.69 / 0.14
- Shape-of-Motion: 16.72 / 0.63 / 0.45 | 23.37 / 0.75 / 0.10
- **MotionScale**: **17.98 / 0.70 / 0.40 | 26.75 / 0.78 / 0.07** [p.6]
- vs SoM DyCheck: +1.26 dB PSNR, −0.05 LPIPS
- vs SoM NVIDIA: +3.38 dB PSNR, −0.03 LPIPS

### DyCheck Tracking — Table 2, PDF page 7
- HyperNeRF: 0.182 / 28.4 / 45.8 | 10.1 / 19.3 / 52.0
- DynIBaR: 0.252 / 11.4 / 24.6 | 5.4 / 8.7 / 37.7
- Deformable-GS: 0.151 / 33.4 / 55.3 | 14.0 / 20.9 / 63.9
- DynMF: 0.188 / 22.9 / 53.8 | 5.5 / 9.5 / 60.5
- CoTracker+DA: 0.202 / 34.3 / 57.9 | 24.1 / 33.9 / 73.0
- TAPIR+DA: 0.114 / 38.1 / 63.2 | 27.8 / 41.5 / 67.4
- DELTA: 0.159 / 32.5 / 55.3 | 24.7 / 34.1 / 68.9
- SpatialTracker: 0.125 / 37.7 / 63.9 | 24.9 / 36.9 / 73.5
- Shape-of-Motion: 0.082 / 43.0 / 73.3 | 34.4 / 47.0 / 86.6
- **MotionScale**: **0.070 / 47.0 / 76.4 | 37.7 / 50.6 / 87.4** [p.7]
- vs SoM: −14.6% EPE, +4.0 / +3.1 δ-thresholds, +3.3 AJ, +3.6 δavg, +0.8 OA

### Ablations (DyCheck) — Table 3, PDF page 8
- Full: 17.98 / 0.70 / 0.40 | 37.7 / 50.6 / 87.4
- Global Bases (替换 cluster-centric 为全局共享 bases，类似 SoM): 16.70 / 0.63 / 0.45 | 34.2 / 46.6 / 86.1 [p.8]
- w/o Adaptive Control: 17.21 / 0.67 / 0.42 | 34.9 / 47.0 / 86.6 [p.8]
- w/o Pose Refinement: 17.45 / 0.67 / 0.41 | — [p.8]
- **w/o Shadow: 16.26 / 0.60 / 0.50** | — [p.8]  ← 最大单组件 drop（−1.72 dB）
- w/o FG Propagation: 16.97 / 0.64 / 0.42 | 34.4 / 46.9 / 86.4 [p.8]

### Visual Ablations — Fig. 4, PDF page 8
- w/o Pose Ref: 锐利纹理模糊（红框）[p.8 Fig. 4 top]
- w/o Shadow: 地面 transient lighting 无法重建，前景过膨胀 + ghosting [p.8 Fig. 4 bottom]

### Efficiency
- **未提供 FPS / 训练时间 / 动态 Gaussian 数量数字**（paper 未报告效率指标；这是对比 MVFusion-GS 时的盲区）

## 7. 评估

**亮点**:
- **Cluster-centric motion field 是结构化创新**：每个 cluster 共享 SE(3) + basis blending，同时获得全局刚性与局部非刚性表达能力，弥补了 SoM "fixed global bases" 过度平滑的缺陷（Ablation: 16.70 → 17.98 PSNR）
- **Progressive optimization 把短序列扩到任意长**：通过 background extension + 三阶段 foreground propagation，规避了 full-batch 优化在长序列上的 temporal drift 与 instability
- **Shadow Gaussians 显式建模 transient lighting**：避免 foreground Gaussians 越界去拟合阴影导致的 geometric dilation 与 ghosting
- **3D tracking 突破**：EPE 0.070 显著低于 SpatialTracker 0.125 和 SoM 0.082，证明 cluster motion field 提供了 3D-aware trajectory supervision
- **多视角 + 单目通用**：NVIDIA 多视角 + DAVIS 单目 + DyCheck 单目多视角都用一套方法

**短板**:
- **效率数据缺失**：未报 FPS / 训练时间 / 内存占用 / Gaussian 数量。对照 MVFusion-GS 那种细致 efficiency 表，本论文对"是否 scalable"的论据偏弱（仅在 qualitative 上声称）
- **未在 mobile / edge GPU 评测**：单卡 RTX 4090，对 D 派系无直接价值
- **依赖 2D tracking prior**：pipeline 上游是 CoTracker3 — 2D tracks 出错时 motion field 也跟着错（但通过 3-stage refinement 部分缓解）
- **数据集偏少**：DAVIS / DyCheck / NVIDIA 都偏 monocular-in-the-wild，缺 Plenoptic Video / iPhone Dataset / Neu3D 等标定数据集上的对比
- **Joint pose refinement 描述偏弱**：仅说 "end-to-end gradient on extrinsics"，没说 reparam / Lie algebra，reproducibility 受影响
- **HDBSCAN + Agglomerative 双层聚类**：split 阈值未给具体数值（在 supplementary 中）

**对我们的相关性**:
- **中等偏低**：属于 4DGS 表示的高质量改进，但论文未触及 mobile / edge GPU / quantization / compression 等我们关心的维度
- **Progressive optimization 思想可借鉴**：把训练拆成 stage 1/2/3 与 BG/FG 解耦，是 mobile pipeline 设计（先 BG 后 FG 的 warm-start）的好范式
- **Cluster-centric motion field 在 mobile 上的隐患**：每个 cluster 维护 (B+1) × SE(3) 参数 + Gaussian per-cluster blending → memory 与 cache locality 比 vanilla 4DGS 差；需要做 cluster 数量 budget 控制
- **Shadow Gaussians 是 "feature engineering" 思路**：在 mobile 上值得保留（语义清晰、shadow-only 无几何监督 → 推理便宜），但占内存

## 8. 引用 (核心)
- [ref 18] Kerbl 2023 — 3DGS 原论文 (ACM TOG / SIGGRAPH 2023)
- [ref 49] Wu CVPR 2024 — 4D Gaussians (real-time dynamic scene rendering)
- [ref 43] Wang ICCV 2025 — Shape-of-Motion (4D reconstruction from single video, 主要对比 baseline)
- [ref 46] Wang AAAI 2025 — GFlow (recovering 4D world from monocular video, 主要对比 baseline)
- [ref 47] Wang 2025 — π3 (permutation-equivariant visual geometry, 提供 depth + pose prior)
- [ref 16] Karaev ICCV 2025 — CoTracker3 (point tracking prior)
- [ref 36] Ravi 2024 — SAM2 (foreground mask)
- [ref 52] Yang NeurIPS 2024 — Depth Anything V2
- [ref 12] Huang CVPR 2024 — SC-GS (sparse-controlled 3DGS for editable dynamic scenes)
- [ref 48] Wu CVPR 2025 — 4D-Fly (fast 4D reconstruction)
- [ref 28] Park CVPR 2025 — SplineGS (motion-adaptive spline 4DGS)
- [ref 22] Li CVPR 2023 — DynIBaR
- [ref 10] Gao NeurIPS 2022 — DyCheck
- [ref 55] Yoon CVPR 2020 — NVIDIA Dynamic Scenes
- [ref 31] Perazzi CVPR 2016 — DAVIS
- [ref 50] Xiao CVPR 2024 — SpatialTracker (3D-aware tracking)
- [ref 5] Doersch ICCV 2023 — TAPIR
- [ref 15] Karaev ECCV 2024 — CoTracker
- [ref 58] Zhou CVPR 2019 — 6D continuous rotation representation

## 9. Insight

**Insight #1 — Cluster-centric motion field 是 "局部共享参数" 的成功案例**。每个 Gaussian 仍受全局 cluster 绑定，但 cluster 内通过可学习 basis blending 表达非刚性。这比"每 Gaussian 独立 deformation"（如 4DGS / Deformable-GS 的朴素做法）参数效率高，比"全局共享 basis"（如 SoM）表达力强。对 mobile port 的启发：**先 group 后 per-Gaussian blend** 的设计可在显存与表达力之间找到甜点。

**Insight #2 — Progressive optimization 是 "数据并行 + 时间串行" 的解耦**。背景是 spatial extension（独立于时间），前景是 temporal propagation（依赖时间）；两者通过 joint pose refinement + shadow Gaussians 耦合。这种解耦让每个 stage 训练目标清晰、可单独 checkpoint — 移动端做 cloud offload + on-device refinement 时可直接对应 "BG server / FG device" 的分工。

**Insight #3 — Shadow Gaussians 的设计哲学值得借鉴**。作者明确指出 "shadow 无 3D 几何 / mask 时间不一致" → 故意只用 RGB loss + segmentation constraint 监督。这是承认物理先验的不完备性后，**用最小监督 + 强解耦** 的工程哲学。Mobile 渲染里"质量瓶颈往往不在几何而在瞬态效应（阴影、反射、散焦）"，可借鉴这种"为每个瞬态分配专门 primitives"的思路。

**Insight #4 — 论文对 scalability 的论证偏弱**。标题强调 "Scalable"，但只给 quality 表，没有 efficiency 表（FPS / memory / Gaussian count / training time）。强烈怀疑 cluster + adaptive control 在长序列上 Gaussian 数与训练时间是 super-linear 的，但作者未量化。对我们 D 派系的可移植性需要重新实验验证，而非照搬论断。

**Insight #5 — HDBSCAN + Agglomerative 的双层聚类是 "承认 split 信号噪声大" 的稳健做法**。直接看 cluster motion variance 容易被噪声触发；先用 density-based 找候选子结构，再用 hierarchical 找 bipartition + 阈值化，能减少 split 抖动。对 mobile 上的 online adaptive control 是好参考。

**Insight #6 — Joint pose refinement 是 "用 photometric loss 替代 SLAM" 的极简替代**。作者明确说不做 SLAM / BA，直接 gradient on extrinsics。在小漂移校正场景下够用，但长序列累积 drift 仍存在 — 这是为什么需要 Stage 3 Long-term Refinement 来 rescue 的根本原因。Mobile 上无 SLAM 后端时，这条设计哲学直接适用。

## 11. 1-hop 关系图 (5 篇示范)

**核心 1-hop 关系图**:

| 节点 | 关系类型 | 上游/下游 |
|------|---------|-----------|
| **Shape-of-Motion [Wang ICCV 2025]** | 主要对比 baseline + Abla "Global Bases" 直接对齐 | concurrent |
| **GFlow [Wang AAAI 2025]** | 主要对比 baseline (DAVIS 定性) | concurrent |
| **4D-Fly [Wu CVPR 2025]** | NeuIPS 2024 / CVPR 2025 fast 4D recon baseline | concurrent |
| **π3 [Wang 2025]** | upstream prior (depth + camera pose) | upstream |
| **CoTracker3 [Karaev ICCV 2025]** | upstream prior (point tracking) | upstream |

**未在 INDEX 的 1-hop 候选** (1-hop rule: 命中即停):
- Deformable-GS, 4D Gaussians, Dynamic GM, SplineGS, DynIBaR, HyperNeRF — 见其他 paper notes
- SpatialTracker, TAPIR, CoTracker, DELTA — tracking SOTA 系列
- Depth Anything V2, MoGe, VGGT, DUST3R — 2D foundation model 系列
- SAM2 — segmentation prior
