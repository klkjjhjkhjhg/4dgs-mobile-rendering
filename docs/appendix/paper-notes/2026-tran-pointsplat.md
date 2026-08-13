# PointSplat: Efficient Geometry-Driven Pruning and Transformer Refinement for 3D Gaussian Splatting

## 0. 基本信息
- 作者: Anh Thuan Tran, Jana Košecká
- 单位: Department of Computer Science, George Mason University (GMU)
- 年份: 2026 (CVPR 2026 Workshop, 3DMV)
- 会议: CVPR 2026 Workshop on 3D Vision Across Modalities (CVPRW)
- arxiv-id: 2604.09903 (04 编号段位，对应 2026-04 batch)
- GitHub: https://github.com/anhthuan1999/pointsplat
- 项目主页: github.com/anhthuan1999/pointsplat (无独立 homepage)
- 代码许可: 未在 PDF 中声明 (待核实)
- 资助: GMU Office of Research Computing + NSF Award 2018631

## 0.5 元数据
- venue: CVPR 2026 Workshop (3DMV — 3D Vision across Modalities)
- arxiv-id: 2604.09903
- s2-id: (未查询 — cron 批次)
- homepage: https://github.com/anhthuan1999/pointsplat
- github: anhthuan1999/pointsplat
- status: 收录
- 收录日期: 2026-08-10
- 收录来源: arxiv_4dgs_scan (cron)
- 评级: T2 (3DGS 静态压缩 + 几何驱动的 reuse-aware 剪枝)
- survey_section: 5
- faction: C (3DGS 加速 — 静态剪枝 + transformer refinement)

## 1. 一句话总结
PointSplat 提出一个 3D 几何驱动的 prune-and-refine 框架：先用一个仅基于 opacity+volume 的 2D 图像无关剪枝分数从pretrained 3DGS 中挑选 K 个 Gaussians，再用 Dual-Branch Encoder 把几何特征 (position/scale/rotation) 与外观特征 (opacity + MLP 压缩后的 SH) 经位置编码加权后喂给 Point Transformer V3 refine，从而在 50%/30%/10% 极端稀疏下保持 ScanNet++ 与 Replica 上的竞争性 PSNR/SSIM 且无需 per-scene 微调。

## 2. 摘要 (核心 3 段)

**问题**: 3DGS 单场景可膨胀到 millions of Gaussians，存储/渲染开销巨大。现有剪枝方法 (LightGaussian [8], PUP-3DGS [13], Mini-Splatting [10], Speedy-Splat [12]) 存在两大痼疾：(1) 剪枝分数依赖 2D 图像 + ray-pixel intersection → 计算昂贵；(2) 剪枝后需要 per-scene fine-tune → 部署时无法快速复用；纯 Transformer refinement (SplatFormer [6]) 又有 feature imbalance — SH 系数在 L=3 时达 48 维/通道，远超 position/scale/rotation/opacity，导致外观主导几何特征。

**方法**: PointSplat 桥接 "image-driven pruning" 与 "transformer-only refinement" 两条原本分离的路线，由两部分组成：
1. **Geometry-Driven Pruning Score** — score_i = λ_α · ν(α_i) + (1−λ_α) · ν((4/3)π·sx·sy·sz)，即 z-score 归一化的 opacity + Gaussian 体积加权，**完全没有 2D 图像或 ray casting**。Top-K 选择 → 获得空间覆盖好、视觉贡献高的稀疏子集。
2. **Dual-Branch Encoder** — 几何分支 f^(p) = concat(μ, q, s) 与外观分支 f^(a) = concat(α, φ(γ)) 各自经过 MLP ϕ_p/ϕ_a + 位置编码 δ = ψ(μ)，再用 softmax(ϕ_a(f^(a)) + δ) 作为 attention weight 与几何特征点乘 → 抑制 SH 主导地位。Refined 特征再经 Point Transformer V3 (5-stage hierarchy, block 数 (2,2,2,4,2)) + residual heads 输出 → 跳过 per-scene 优化直接 rasterize 渲染。

**结果**: 在 ScanNet++ (5 scenes) 与 Replica (3 scenes) 上，10% 稀疏度时 PointSplat 仍把 PSNR 维持在 23.46 / 29.81 dB，远好于 SplatFormer (10.62 / 8.37)；50% 稀疏度达到 29.52 / 35.98 dB，逼近 dense 3DGS (29.73 / 39.40) 且 **FPS 反而更高** (50%@390.51 FPS vs dense@207.41 FPS，因剪掉了大低-opacity "floaters" 减少 overdraw)。10%@621.53 FPS vs PUP-3DGS@579.98 FPS / LightGaussian@356.04 FPS。无需 per-scene 优化，λ_α = 0.3 跨数据集稳定。A100 80GB，10k iter Adam。

## 3. 派系分类
- **C (3DGS 静态加速)**: 主。PointSplat 完全针对 **3DGS 静态压缩** — 几何驱动剪枝 + transformer refinement 把百万级 Gaussians 瘦身到 10–50%，且渲染 FPS 提升。无 4D / 时序 / motion 维度。
- 相关: D (移动端) 沾边 — 论文明确提及 "real-time deployment on edge devices / resource-constrained devices in AR/VR and robotics" (结论段、p.2)。FPS 提升 (50%@390 FPS, 10%@621 FPS) 与"无需 per-scene 优化"对 mobile port 高度友好。
- 不属于 A (4DGS)，无任何时空维度；不属于 B (训练加速) — 本文关注推理而非训练 budget；不算 E (cross-disciplinary)，方法本身是 3DGS + Point Transformer V3 的直接组合，无跨域迁移。
- 顶部热点: 公开 PDF 是 CVF Open Access 版本，明确写在 footer: "This CVPR Workshop paper is the Open Access version, provided by the Computer Vision Foundation."

**结论**: 主派系 **C**。

## 4. 方法

### 4.1 整体架构 (prune-and-refine pipeline)
输入 → pretrained 3DGS (Splattfacto from Nerfstudio) → (a) Geometry-Driven Pruning Score → top-K Gaussians → (b) Dual-Branch Encoder (geometry + appearance 分支 + 位置编码) → Point Transformer V3 → separate output heads (position + appearance) → residual update → 用修改后的 Gaussians 直接 rasterize (不需要 gradient-based per-scene fine-tune)。架构图见 Figure 2 (p.4)。

### 4.2 Geometry-Driven Pruning Score (Eq. 3)

$$\text{score}_i = \lambda_\alpha \cdot \nu(\alpha_i) + (1-\lambda_\alpha) \cdot \nu\left(\tfrac{4}{3}\pi s_x s_y s_z\right)$$

- **ν(·)**: z-score 标准化 (在全部 N Gaussians 上独立做)
- **λ_α ∈ [0,1]**: opacity vs volume 平衡系数，**固定 0.3** (跨数据集，不调优)
- 排序后取 top-K，K = G% × N (G ∈ {50, 30, 10})
- **关键优势**: 不需要图像、相机参数、ray-pixel intersection — 纯 3D intrinsic attributes

副作用：相比 LightGaussian / PUP-3DGS 保留的"体积大但 opacity 低"的 floaters，PointSplat 倾向选 **小体积 + 高 opacity** 的 Gaussians (median log10(Vol) ≈ −10, median opacity ≈ 0.5, Figure 4 p.7)，rasterization overdraw 降低 → **FPS 反而提升**。

### 4.3 Dual-Branch Encoder (Eqs. 4–6)

两条平行分支 + 位置编码 + soft attention 融合：

$$f_i^{(p)} = \text{concat}(\mu_i, q_i, s_i) \quad \text{(position+quat+scale, 几何)}$$
$$f_i^{(a)} = \text{concat}(\alpha_i, \phi(\gamma_i)) \quad \text{(opacity + MLP 压缩的 SH, 外观)}$$
$$\delta_i = \psi(\mu_i) \quad \text{(位置编码，仅用 3D 坐标)}$$
$$f_i = \sigma(\phi_a(f_i^{(a)}) + \delta_i) \odot (\phi_p(f_i^{(p)}) + \delta_i)$$

- ϕ_p, ϕ_a: 各自独立的 MLP (含 BN + ReLU)
- ψ: 位置编码模块，**只用 μ_i，不用 s/q** — 避免混淆物理 3D 位置与内在属性
- σ(·): softmax → 把外观特征转成 attention weight
- ⊙: 点乘 → 用 appearance-derived attention 加权 geometric features

**核心解决**: SplatFormer [6] 把所有 Gaussian 参数 concat 成 1 个向量喂 PTv3，SH 维度 (L=3 时 48 dim) 主导其他 6D 几何特征 → 学习失衡。PointSplat 把二者分离 + 重加权，让 transformer 看到 balanced 几何-外观表示。

### 4.4 3D Transformer Network

- Backbone: Point Transformer V3 (Wu et al. CVPR 2024) [28]
- 5-stage hierarchical，transformer blocks/stage = (2, 2, 2, 4, 2)
- 局部 attention 保留细粒度结构
- Separate output heads → residual update (Eqs. 7–8):
  $$f_i'^{(p)}, f_i'^{(a)} = PT(f_i)$$
  $$f_i^{(p)} \leftarrow f_i^{(p)} + f_i'^{(p)}, \quad f_i^{(a)} \leftarrow f_i^{(a)} + f_i'^{(a)}$$
- **关键 multi-scene 训练**: 在每个 scene 随机选 2 张图 (类似 pixelSplat [2], MVSplat [5])，但跨 scene 训练 → 学到跨场景的几何先验 (floor、wall 等) → 部署时无需 retraining

### 4.5 训练配置
- 平台: NVIDIA A100 80GB
- 优化: Adam, 10k iter, lr=1e-5, 6k iter 时 ×0.1
- Loss: L = L1 + λ_LPIPS · L_LPIPS, λ_LPIPS = 0.1 (遵循 [6])
- 每次 refinement: **仅 2 张图 per scene** (极轻量)
- 固定 λ_α = 0.3

## 5. 实验

### 5.1 数据集
- **ScanNet++** [Yeshwanth ICCV 2023] [30]: 5 test scenes，high-fidelity 室内 3D，10% 图像做测试
- **Replica** [Straub 2019] [23]: 3 test scenes (沿用 NICE-SLAM [34] 设定)，10% 图像做测试
- 90% 图像训练 pretrained 3DGS (Splatfacto from Nerfstudio [24])

### 5.2 基线
- **Scene-Specific / Image-Driven**: LightGaussian [8], PUP-3DGS [13]
- **Geometry-Driven**: SplatFormer [6] (单一对照)
- **Dense reference**: 3DGS (Kerbl SIGGRAPH 2023) [14]

### 5.3 评测指标
- PSNR↑ / SSIM↑ / LPIPS↓ (standard)
- Efficiency: FPS, #G, Size (MB)
- 评估的稀疏度: G ∈ {50%, 30%, 10%}

### 5.4 Ablation 维度
- λ_α 权重 (5 值: 0.1/0.3/0.5/0.7/0.9)
- Dual-Branch Encoder 5 变体 (I baseline, II geom only, III +PE, IV no PE, V full)

## 6. 性能数字 (PDF 页码标)

### Main Table 1 — ScanNet++ & Replica (p.6)

按 G% 分组，每组列 PSNR / SSIM / LPIPS：
- **100% (Dense, 参考)**: 3DGS — ScanNet++ 29.73 / 0.925 / 0.165; Replica 39.40 / 0.974 / 0.122 [p.6]
- **50% Scene-Specific / Image-Driven**:
  - LightGaussian: 30.23 / 0.929 / 0.171 (ScanNet++), 39.78 / 0.974 / 0.125 (Replica)
  - PUP-3DGS: 31.35 / 0.937 / 0.159, 39.67 / 0.973 / 0.121
- **50% Geometry-Driven**:
  - SplatFormer: 21.27 / 0.857 / 0.348, 30.79 / 0.927 / 0.233
  - **PointSplat*** (prune only): 28.81 / 0.923 / 0.266, 33.97 / 0.956 / 0.213
  - PointSplat* + SplatFormer: 29.03 / 0.924 / 0.264, 34.63 / 0.952 / 0.192
  - **PointSplat (full)**: 29.52 / 0.928 / 0.258, 35.98 / 0.958 / 0.191
- **30% Geometry-Driven**:
  - SplatFormer: 11.66 / 0.691 / 0.509, 29.14 / 0.903 / 0.263
  - **PointSplat**: 27.70 / 0.911 / 0.287, 34.46 / 0.947 / 0.208
- **10% Geometry-Driven**:
  - SplatFormer: 10.62 / 0.691 / 0.569, 8.37 / 0.388 / 0.677 (崩溃)
  - **PointSplat**: 23.46 / 0.855 / 0.374, 29.81 / 0.902 / 0.276

**关键发现**: 10% 稀疏时 PointSplat vs SplatFormer 在 ScanNet++ 上 PSNR 提升 **+12.84 dB** (23.46 vs 10.62)，Replica 上 **+21.44 dB** (29.81 vs 8.37) — 极端稀疏场景下 PointSplat 的 prune+refine 组合压倒性胜出。

### Efficiency — Table 2 (p.8)

| G | Method | #G | FPS | Size(MB) |
|----|---|---|---|---|
| 100% | 3DGS (Dense) | 588K | 207.41 | 145.92 |
| 50% | LightGaussian | 294K | 213.30 | 72.96 |
| 50% | PUP-3DGS | 294K | 278.26 | 72.96 |
| 50% | **PointSplat** | 294K | **390.51** | 72.96 |
| 30% | LightGaussian | 176K | 253.42 | 43.78 |
| 30% | PUP-3DGS | 176K | 352.71 | 43.78 |
| 30% | **PointSplat** | 176K | **440.56** | 43.78 |
| 10% | LightGaussian | 59K | 356.04 | 14.58 |
| 10% | PUP-3DGS | 59K | 579.98 | 14.58 |
| 10% | **PointSplat** | 59K | **621.53** | 14.58 |

**核心观察**: 同一 Gaussian 数量下，PointSplat 的 FPS **一直最高** — 因为剪枝偏向小+高 opacity，减少 overdraw。50% 稀疏时 FPS 甚至高于 dense 3DGS (390.51 vs 207.41)，10% 稀疏时 621.53 FPS。

### Ablation λ_α — Table 3 (p.8)
- λ_α=0.1 → PointSplat ScanNet++ 21.72 / Replica 28.23 (over-volume)
- **λ_α=0.3** → ScanNet++ 23.46 / Replica 29.81 (optimal)
- λ_α=0.5 → ScanNet++ 22.72 / Replica 27.71
- λ_α=0.7 → ScanNet++ 20.10 / Replica 27.39
- λ_α=0.9 → ScanNet++ 10.66 / Replica 26.58 (over-opacity, ScanNet++ 崩溃)

### Ablation Dual-Branch Encoder — Table 4 (p.8)
- I (prune only): 21.87 / 0.836 / 0.377
- II (geom f^(p)): 22.61 / 0.848 / 0.384
- III (geom + PE): 22.76 / 0.847 / 0.385
- IV (geom + appearance, no PE): 22.65 / 0.846 / 0.388
- **V (geom + appearance + PE, full)**: 23.46 / 0.855 / 0.374

实验在 10% 稀疏度。Full model PSNR 提升 **+1.59 dB** vs baseline prune-only。

### 渲染质量提升原因 (Section 4.1, p.7)
- 仅剪枝 → 几何破碎、纹理模糊 (Figure 1, 3)
- 仅 PT refinement (SplatFormer) → feature imbalance → 外观主导
- **PointSplat: 先 prune 掉冗余浮点 → 再用 balanced encoder refine 残留核心 → 几何边沿清晰 + 感知质量稳**

## 7. 评估

**亮点**:
- **图像无关剪枝**: 第一个完全脱 2D 图像的 Gaussian 重要性评分 — 部署时不需要 test-time 图像，对 edge device 友好
- **无需 per-scene 优化**: 跨场景训练 transformer refinement，可即时部署，是真正的 "compact and expressive representation"
- **FPS 反而提升**: 50% 稀疏时 390.51 FPS vs dense 207.41 — 罕见的"剪枝不慢反快"案例 (因避免大低-opacity floaters 的 overdraw)
- **feature imbalance 解决**: Dual-Branch + 位置编码 + soft attention 是优雅的 feature-balance 设计
- **极端稀疏鲁棒**: 10% 稀疏时 PSNR 仍 23.46 / 29.81，远好于 SplatFormer 崩溃到 10.62 / 8.37
- **density-distribution 可视化** (Figure 4): 清晰展示 PointSplat 选高 opacity + 小体积 vs 其它方法保留 floaters

**短板**:
- **仅室内数据集**: ScanNet++ 与 Replica 都是 indoor；作者在 Limitation (p.8) 明确承认 "Extending to complex, unbounded outdoor scenes remains an open challenge"
- **refinement 仍需 2 张图像 per scene** (与 SplatFormer / pixelSplat 一致), 不能做到完全 0 数据依赖
- **作者自承**: Discrete 评分 λ_α 的极值 (0.1/0.9) 在 ScanNet++ 上 PSNR 跌到 21.72 / 10.66，**对超稀疏 + 室内结构性差的场景不太稳**
- **文档不足**: 8 页正文 + 2 页 references，无单独 appendix，许多决定(为何 Block 数 2/2/2/4/2, MLP 维度)未解释
- **没在 dynamic 场景验证**: 论文完全静态 indoor NVS 设定，无 4D / motion 维度
- **没做 mobile / edge GPU 评测**: 虽宣称对 AR/VR/robotics 友好，但所有数据在 A100 80GB 上获得，没测 Adreno / Mali / Jetson

**对我们的相关性**:
- **高** — 正好命中我们核心动机之一: 不依赖 per-scene 优化、可在部署时立即压缩、不需要 2D 图像做剪枝决策，对 mobile port 极其友好
- 10% 稀疏 (59K Gaussians, 14.58 MB) + 621 FPS 的组合在桌面 GPU 上是目标值，移动端 (Adreno 830) 可能需要再降稀疏度到 5% 或量化
- **借鉴价值**: Dual-Branch Encoder 的 feature-balance 思想可迁移到未来 4DGS 静态 backbone 的轻量化
- **风险**: PTv3 在 Adreno 上的可行度未知 — 局部 attention 仍是密集矩阵运算

## 8. 引用 (核心)
- [ref 14] Kerbl SIGGRAPH 2023 — 3DGS 原论文, cite at p.1, p.2, p.3, p.5, p.6
- [ref 8] Fan NeurIPS 2024 — LightGaussian (image-driven pruning baseline)
- [ref 13] Hanson CVPR 2025 — PUP-3DGS (sensitivity-based pruning baseline)
- [ref 6] Chen ICLR 2025 — SplatFormer (closest prior: PointTransformerV3 for GS refinement)
- [ref 10] Fang ECCV 2024 — Mini-Splatting (constrained Gaussian count)
- [ref 12] Hanson CVPR 2025 — Speedy-Splat (fast rasterization kernels, complementary)
- [ref 18] Lee CVPR 2024 — Compact 3DGS (codebook-based grouping)
- [ref 28] Wu CVPR 2024 — Point Transformer V3 (backbone)
- [ref 32] Zhao ICCV 2021 — Point Transformer (V1)
- [ref 27] Wu NeurIPS 2022 — Point Transformer V2
- [ref 30] Yeshwanth ICCV 2023 — ScanNet++ dataset
- [ref 23] Straub 2019 — Replica dataset
- [ref 24] Tancik SIGGRAPH 2023 — Nerfstudio / Splatfacto
- [ref 34] Zhu CVPR 2022 — NICE-SLAM (Replica setup)
- [ref 2] Charatan CVPR 2024 — pixelSplat (2-image-per-scene protocol)
- [ref 5] Chen ECCV 2024 — MVSplat (2-image-per-scene protocol)
- [ref 7] Di Sario 2025 — GoDe (LoD)
- [ref 16] Kulhanek NeurIPS 2025 — LODGE
- [ref 22] Shi 3DV 2025 — LapisGS
- [ref 35] Zoomers WACV 2025 — PRoGS

## 9. Insight

**Insight #1 — 图像相关的剪枝决策是部署时被低估的瓶颈**。LightGaussian/PUP-3DGS/Speedy-Splat 等都需要 2D 测试图像 + ray-pixel intersection 计算分数，这意味着：(1) 部署时必须有 test-time 图像，(2) 重新打分耗算力，(3) 难以做 generalizable pruning。PointSplat 用 opacity × volume 的 z-score 加权直接绕过 2D 信号，**部署时不需要任何图像**。这对我们 mobile port 的启发: 若我们做动态场景的边缘部署，可以考虑用同样思路做 motion-aware pruning 的 3D-only 评分。

**Insight #2 — "剪枝 + transformer refinement" 是 feature compression 的新范式**。PointSplat 揭示了一条与 "LoD streaming" (PRoGS, LapisGS, LODGE) 完全不同的高效化路线: 不构建多 level 渲染 pyramid，而是把 over-parameterized 3DGS 一次性瘦身后用 multi-scene 训练的网络 refine 缺失结构。**优点**: 单一模型即时部署，不需要 LoD 训练 pipeline；**缺点**: 仍需对全场景做一次 forward pass。Mobile 端在算力受限且 LoD 切换成本高时，PointSplat 思路更直接。

**Insight #3 — feature imbalance 是 3DGS + Transformer 的隐藏陷阱**。SplatFormer 直接 concat 所有 Gaussian 属性，SH 48 dim 主导 6D 几何特征。PointSplat 的 Dual-Branch + 位置编码 + soft attention 把 "balance" 形式化为 attention weight，是几何-外观融合的通用模板。我们如果将来想用 PointNet++ 或 PTv3 优化 4DGS 的 Gaussian 集合，**必须考虑 SH / appearance 维度与几何维度的 imbalance 处理** — 不加干预会导致几何特征被淹没。

**Insight #4 — "剪枝使 FPS 上升" 是反直觉但关键的现象**。PointSplat 50% 稀疏时 390.51 FPS vs dense 207.41 FPS。原因是剪掉了大半低-opacity "floaters"（覆盖很多像素但几乎看不见），splatting overdraw 显著下降。这给了我们一个 portable 启示: **mobile 3DGS 的首要优化不是减小 #G，而是去掉 floaters**。即使保留 80% Gaussians，去除 floaters 就能显著提速。

**Insight #5 — 跨场景训练的 Two-Image Trick**。PointSplat 与 pixelSplat / MVSplat 一样，每个 scene 训练时只用 2 张随机图 (而非 100% 全集)，但能跨场景学到几何先验。这在数据稀缺场景 (如小型工程现场) 极具价值。Mobile 端采集和标注都贵，**借鉴这种 "极低数据量 + 跨场景 transformer" 范式，可显著降低采集成本**。

## 11. 1-hop 关系图 (5 篇示范)

**核心 1-hop 关系图**:

| 节点 | 关系类型 | 上游/下游 |
|------|---------|-----------|
| **3DGS [Kerbl SIGGRAPH 2023]** | pretrained input (PointSplat 起点) | upstream |
| **LightGaussian [Fan NeurIPS 2024]** | baseline (image-driven pruning) | concurrent |
| **PUP-3DGS [Hanson CVPR 2025]** | baseline (sensitivity-based pruning) | concurrent |
| **SplatFormer [Chen ICLR 2025]** | closest prior (PTv3 refine, PointSplat 解决其 feature imbalance) | upstream + concurrent |
| **Point Transformer V3 [Wu CVPR 2024]** | backbone (5-stage hierarchy) | upstream |

**未在 INDEX 的 1-hop 候选** (1-hop rule: 命中即停):
- Mini-Splatting, Speedy-Splat, Compact-3DGS, LSM, pixelSplat, MVSplat, MVSGaussian, GoDe, LODGE, LapisGS, PRoGS — 均需单独 paper notes
