# FilterGS: Traversal-Free Parallel Filtering and Adaptive Shrinking for Large-Scale LoD 3D Gaussian Splatting

## 0. 基本信息
- 作者: Yixian Wang, Haolin Yu, Jiadong Tang, Yu Gao, Xihan Wang, Yufeng Yue, Yi Yang† († corresponding)
- 单位: Beijing Institute of Technology (ININ Lab)
- 年份: 2026 (arXiv v1: 25 Mar 2026)
- 会议: arXiv preprint (CVPR 2026 submission per project context — 文中未直接声明 venue)
- arxiv-id: 2603.23891
- GitHub: https://github.com/xenon-w/FilterGS
- 项目主页: 同上 (无独立 homepage)
- 代码许可: 未声明 (待核实)

## 0.5 元数据
- venue: arXiv preprint (CVPR 2026 candidate per task context)
- arxiv-id: 2603.23891
- s2-id: (未查询 — cron 批次)
- homepage: https://github.com/xenon-w/FilterGS
- github: xenon-w/FilterGS
- status: 收录
- 收录日期: 2026-08-10
- 收录来源: arxiv_4dgs_scan (cron)
- 评级: T1 (核心 3DGS 大场景渲染加速 + LoD 树结构关键瓶颈)
- survey_section: 5
- faction: C (3DGS acceleration, large-scale)

## 1. 一句话总结
FilterGS 针对大场景 LoD-3DGS 渲染中两个核心瓶颈——**层级串行遍历**(占 >60% 渲染时间) 和 **冗余 Gaussian-tile K-V pairs**——提出 **(a) Traversal-Free Parallel Filtering** (R&L Filter + Ancestor Filter 解耦树深度依赖) 和 **(b) GTC-guided Adaptive Shrinking** (基于 Gaussian-to-Tile Contribution 度量的场景自适应 GTC→τ 映射),在 6 个大场景上达成 ~300 FPS 同时保持 LoD 顶级重建质量。

## 2. 摘要 (核心 3 段)

**问题**: 大场景 3DGS 渲染存在两个独立但叠加的瓶颈:
1. **串行层级遍历低效**: LoD-3DGS (Hierarchical-GS, OctreeGS, FLoD, LoG 等) 依赖逐层 (level-by-level) traversal 选取当前帧适用的高斯,层间 kernel launch + synchronization 累计开销可达总渲染时间 **>60%**;LoG 在 L=5 时 filter 时间 (3.6 ms) 是 FilterGS 平行滤波 (0.93 ms) 的 3.6 倍。
2. **冗余 Gaussian-Tile K-V pairs**: LoD 多层结构在 rasterization 前生成"海量 Gaussian 与 tile 配对",经测量 **>70% 对最终像素贡献可忽略 (KPC<0.01)**,但仍走完整 sort + α-blending 流水线。FlashGS 的固定阈值 τ=1/255 在大场景下不够激进,learning-based shrinking 在 LoD 树中存在层切换 artifacts 和过拟合。

**方法**: FilterGS 两部件解耦设计:
1. **Parallel Filtering (R&L + Ancestor Filter)**: 在统一 CUDA kernel 中对所有 in-frustum Gaussians (数量 N) 同步执行两步——
   - **R&L Filter**: 投影 2D 协方差 Σ_2D → eigenvalue σ → 像素半径 R_2D = 3σ;R_2D ≤ τ_R (默认 3) 的节点保留;**叶子节点全豁免** (避免空洞)。
   - **Ancestor Filter**: 预计算每个节点 N_{i,j} 的 ancestor path AP_{i,j} (从直接 parent 到 root 的序号序列);只要有 ancestor 通过 R&L,所有 descendant (含作为 leaf 暂留者) 全部 cull。
   - 时间复杂度: T_serial = Σ_ℓ[T_calc(n_ℓ) + T_synch] → **T_parallel = T_synch + T_calc(N)** (与树深度 L **解耦**),fully exploits GPU SIMD。
2. **GTC-Guided Adaptive Shrinking**: 三层聚合度量——
   - **KPC (Key-value Pair Contribution)**: `K_{g_k}^{t_i} = Σ_{j=1}^{B_x B_y} α_{ij} T_{ij}`,即 Gaussian 在 tile 中的有效像素贡献。
   - **Per-tile GTC**: `G_i = (1/n_gs) Σ K_{g_j}^{t_i}` (tile 内平均 KPC)。
   - **Per-view/Per-dataset GTC**: `Ḡ_v = (1/n_tile) Σ G_j` → `Ḡ = (1/N) Σ Ḡ_v`。
   - **Shrinking threshold**: `τ = λ_G · Ḡ⁻¹` (λ_G=0.2 默认),即 Ḡ 低(高拥塞) → τ 高 → 激进 shrink → 减少 K-V pair 数量。给定 2D Gaussian 中心 α_0,半径 r = √(2σ_max² ln(α_0/τ)),替代 FlashGS 的固定 τ=1/255。

**结果**: 在 MatrixCity Block Small (2.7 km², 5620 图像) + GauUScene (College/Residence/Modern-Building) + UrbanScene (Residence/Sci-art) 6 个 1+ km² 大场景上,FilterGS **平均 ~300 FPS** (Residence-U 372 / College-G 290 / Sci-Art 234 / Block-Small 297 / Residence-G 212 / Modern-Building 354),相比 LoG 提升 **200%+**,相比 H3DGS 提升 **~300%**;**filter time tf < 1.2 ms** (vs LoG 8.5–14.2 ms, 降 90%)。PSNR 与 top-LoD 同档 (平均 25-27 dB),SSIM/LPIPS 接近,quality 损失 <1% PSNR 换取 20% FPS。训练 100–300k iter on A100 40G,evaluation on RTX 4090,1080p。

## 3. 派系分类
- **C (3DGS acceleration)**: 主。FilterGS 是 3DGS 大场景渲染 acceleration 的代表性工作,核心 KPI 是 FPS + filter time 下降。
- 相关: **D (mobile/edge)** 边缘沾边 — 文中 Related Work 明确引用 LODGE [Kulhanek 2025] (LoD + mobile)。但 FilterGS evaluation 单独在 RTX 4090,无 mobile 数据。
- 相关: **A (4DGS representation)** 沾边有限 — LoD 树结构属于静态大场景 Gaussian 表示,但无 dynamic / temporal 成分。
- 不属于派系 B (training acceleration, 训练时改) — FilterGS 改动完全在 inference rendering pipeline。

**结论**: 主派系 **C**。

## 4. 方法

### 4.1 整体架构 (3-stage pipeline)
(a) LoD-GS Tree 训练 (遵循 FLoD/LoG 递归构造,parent 旋转 R(q_v) + 各向异性 scale s_v,children 继承 orientation/color/opacity,缩放 γ<1)。
(b) Pre-rendering pass: 全训练视角过一遍 3DGS 标准 pipeline,计算 **GTC Ḡ** → 导出 **shrinking threshold τ = λ_G · Ḡ⁻¹** (一次预计算,后续 inference 复用)。
(c) 正式 rendering: 投影 → Parallel Filter (R&L + Ancestor) → AABB 阶段按 τ shrink → 减少 K-V pairs → sort + α-blending 输出。

### 4.2 Traversal-Free Parallel Filtering

**R&L Filter**:
- 2D 协方差 Σ_2D → eigenvalue σ → R_2D = 3σ (3σ 等价 99.7% Gaussian 覆盖)。
- 阈值 τ_R=3 (pixel radius, 默认);τ_R 越小 → 保留更高频细节 but 越多 Gaussians。
- **Leaf 豁免**: 整枝 Gaussians 全部 R_2D > τ_R 时,强制保留 leaf 节点 1 个 → 防空洞。

**Ancestor Filter**:
- 预计算 AP_{i,j} 序列 (需要 ~20% 额外 memory,作者称 trivial)。
- Top-down culling: 任意内部节点 N_{i*,j*} 通过 R&L 后,所有 descendant N_{i,j} (N_{i*,j*} ∈ AP_{i,j}) cull。
- 保证每枝最多保留 1 个合适 level node,避免多 level 同时 rasterize 同一 branch。

**Serial vs Parallel 时间复杂度**:
```
T_serial = Σ_{ℓ=0}^{L-1} [T_calc(n_ℓ) + T_synch]   # L 层串行
T_parallel = T_synch + T_calc(N)                    # 与 L 解耦
```
- **Depth Decoupling**: cost 仅随 N (in-frustum 总数) 缩放,不随 L。
- **Maximized Concurrency**: 一次性处理所有 level,完全利用 GPU SIMD / memory coalescing。
- 1.5M Gaussians 远超 RTX 4090 单 batch 0.26M 上限 → parallel filter 仍能 full utilization。

### 4.3 Scene-Adaptive Gaussian Shrinking

**KPC (Key-value Pair Contribution)** (Eq. 5):
$$K_{g_k}^{t_i} = \sum_{j=1}^{B_x B_y} \alpha_{ij} T_{ij}$$
每 Gaussian-tile pair 的"有效像素贡献"，KPC < 0.01 视为冗余。

**Per-tile GTC** (Eq. 6):
$$G_i = \frac{1}{n_{gs}} \sum_{j=1}^{n_{gs}} K_{g_j}^{t_i}$$
低 G_i = tile 内 Gaussian 拥塞 (over-clustering/冗余)。

**Per-view GTC** (Eq. 7) + Per-dataset GTC (Eq. 8):
$$\bar{G}_v = \frac{1}{n_{tile}} \sum_{j=1}^{n_{tile}} G_j, \quad \bar{G} = \frac{1}{N} \sum_{j=1}^{N} \bar{G}_v$$

**Adaptive Shrinking**:
$$r = \sqrt{2\sigma_{max}^2 \ln(\alpha_0/\tau)}, \quad \tau = \lambda_G \cdot \bar{G}^{-1}$$
- Ḡ 低 → τ 高 → r 小 → 激进 shrink → 减少 K-V pair。
- **区别于 FlashGS**: FlashGS 用固定 τ=1/255,大场景不够激进;learning-based shrinking (per-Gaussian 训系数) 在 LoD 树上层切换 artifacts + overfitting。
- **GTC 是 universal scene-aware 度量**: low Ḡ = 拥塞需激进;high Ḡ = 真实低透明度区 (如树叶/栅栏) 不能动。

### 4.4 训练与实现
- 数据集: 100–300k iter (按图像数),A100 40G 训练,RTX 4090 evaluation。
- λ_G = 0.2 (表 6 lambda sweep 验证 [0.03, 0.2] 区间为佳)。
- 1080p rendering。
- ancestor path 预计算 ~20% 额外 memory;总模型 size 1.61 GB (Residence-U) – 6.33 GB (Residence-G)。
- 完整方法开源: https://github.com/xenon-w/FilterGS

## 5. 实验

### 5.1 数据集 (6 大场景,all 1+ km²)
- **MatrixCity [Li 2023, ICCV]** Block Small: drone-captured, 5620 图像, 2.7 km²
- **GauUScene [Xiong 2024, arXiv] v2**: College, Residence, Modern-Building (real-world)
- **UrbanScene3D [Lin 2022, ECCV]**: Residence, Sci-art (real-world)
- Camera poses via COLMAP

### 5.2 基线
- **3DGS** [Kerbl 2023, TOG]: vanilla baseline
- **H3DGS (Hierarchical-GS)** [Kerbl 2024, TOG]: continuous LoD 首发
- **FLoD** [Seo 2024, arXiv]: flexible LoD
- **LoG** [Shuai 2024]: discrete LoD tree (GitHub: zju3dv/LoG)
- **OctreeGS** [Ren 2024, arXiv]: Octree-structured LoD
- 另在 Related Work 提及: LODGE (mobile), FlashGS, Scaffold-GS, Mini-Splatting, SpeedySplat, TC-GS, Potamoi, GS-Cache 等

### 5.3 评测指标
- 标准: PSNR↑ / SSIM↑ / LPIPS↓
- 效率: **tf (filter time, ms)** + FPS (cumulative all-frames average)
- 数量: NP (生成的 K-V pair 总数) — 衡量 pair-based redundancy

## 6. 性能数字 (PDF 页码标)

### 主表 Table 1, PDF page 6 (6 大场景)

**MatrixCity Block Small [12]**:
- 3DGS: 25.42 / 0.743 / 0.446 / – / 58 FPS
- H3DGS: 25.73 / 0.756 / 0.440 / 5.51 ms / 83 FPS
- LoG: 26.52 / 0.770 / 0.414 / 10.46 ms / 77 FPS
- OctreeGS: 26.43 / 0.771 / 0.417 / 5.13 ms / 125 FPS
- FLoD: 25.06 / 0.732 / 0.461 / 3.04 ms / 245 FPS
- **FilterGS**: 26.31 / 0.763 / 0.433 / **1.14 ms** / **372 FPS** [p.6]

**UrbanScene Sci-Art [15]**:
- 3DGS: 22.35 / 0.717 / 0.311 / – / 61 FPS
- LoG: 23.27 / 0.737 / 0.305 / 11.6 ms / 67 FPS
- **FilterGS**: 23.07 / 0.749 / 0.308 / **1.01 ms** / **234 FPS** [p.6]

**UrbanScene Residence [15]**:
- 3DGS: 21.92 / 0.767 / 0.298 / – / 62 FPS
- LoG: 22.7 / 0.812 / 0.267 / 11.33 ms / 66 FPS
- **FilterGS**: 22.13 / 0.786 / 0.283 / **0.93 ms** / **297 FPS** [p.6]

**GauUScene College [32]**:
- 3DGS: 24.21 / 0.697 / 0.341 / – / 58 FPS
- LoG: 25.9 / 0.757 / 0.282 / 11.97 ms / 72 FPS
- **FilterGS**: 25.69 / 0.748 / 0.288 / **1.05 ms** / **290 FPS** [p.6]

**GauUScene Residence [32]**:
- 3DGS: 24.15 / 0.746 / 0.250 / – / 42 FPS
- LoG: 25.09 / 0.781 / 0.223 / 14.19 ms / 57 FPS
- **FilterGS**: 25.31 / 0.789 / 0.219 / **1.81 ms** / **212 FPS** [p.6]

**GauUScene Modern-Building [32]**:
- 3DGS: 25.79 / 0.733 / 0.324 / – / 54 FPS
- LoG: 27.35 / 0.814 / 0.270 / 8.51 ms / 81 FPS
- **FilterGS**: 27.04 / 0.810 / 0.273 / **1.04 ms** / **354 FPS** [p.6]

### Ablation Table 2 — Rendering Time Breakdown on Residence [15], PDF page 7
分阶段 (T_calc, T_synch, T_prepr, T_sort, T_alpha, T_total, FPS):
- (–) Shrink (–) Filter: 3.59 / 7.72 / 0.20 / 1.04 / 2.58 / 15.13 ms / 66 FPS [p.7]
- (✓) Shrink (–) Filter: 3.59 / 7.80 / 0.27 / 0.61 / 1.69 / 13.96 ms / 72 FPS [p.7]
- (–) Shrink (✓) Parallel Filter: 0.52 / 0.41 / 0.19 / 1.01 / 2.64 / 4.77 ms / 210 FPS [p.7]
- **(✓) Shrink (✓) Parallel Filter**: 0.52 / 0.40 / 0.26 / 0.57 / 1.62 / **3.37 ms** / **297 FPS** [p.7]
- Parallel Filter 单独 → 218% FPS 提升;S_combined → 350%。

### Ablation Table 3 — Rendering Quality on College/Modern-Building [32], PDF page 7
**Filter 选出的 Gaussian 集合与 serial traversal 完全一致** (PSNR/SSIM/NP 一致):
- College / Modern: 25.90 / 0.752 / 3.25M;27.35 / 0.813 / 2.13M [p.7]
- 加 shrink: 25.69 / 0.748 / 1.56M;27.04 / 0.810 / 1.12M (NP 减 52%,PSNR-0.21) [p.7]
- 说明: Parallel filter **零质量损失**。

### 不同 Shrinking 对比 (College + Modern-Building, Fig. 5, p.7)
- 3DGS + 3σ: 24.21 / 58 FPS / 7.99M NP;p.7
- 3DGS + flashGS (τ=1/255): 24.21 / 61 FPS / 7.98M NP;几乎无收益
- 3DGS + FilterGS (λ_G=0.2): 24.07 / 72 FPS / 6.20M NP
- FilterGS + 3σ: 25.90 / 241 FPS / 3.25M NP
- FilterGS + flashGS: 25.90 / 246 FPS / 3.24M NP
- **FilterGS + λ_G=0.2**: 25.69 / **290 FPS** / **1.56M NP** → 又消 75% 冗余 K-V pair

### λ_G Sensitivity (Fig. 6 + Fig. 7, p.8)
- Block [12]: λ_G 0.02–0.30, PSNR 26.40–26.52 (差 0.12 dB), FPS 311–385 (差 24%);推荐 0.2 区间→1% PSNR 换 20% FPS
- Residence [32]: λ_G 0.02–0.43, PSNR 25.10–25.57 (差 0.47 dB), FPS 153–233 (差 52%)
- λ_G=0.2 时,FilterGS 多减少 Residence [15] K-V pair 中 KPC<0.05 的 >40% (Fig. 6b)

### Quality 退化细节 (Fig. 7, p.8)
- High-frequency 区域 (建筑立面/树叶)几乎无损 (high-KPC Gaussian 保留)。
- Low-frequency 区域 (公路/沙地) 大 λ_G 时 tile 边界渐显 → smooth blending 受损 (acceptable trade-off)。

## 7. 评估

**亮点**:
- **filter time 下降 90%+**+ **FPS 提升 200–350%** — 设计哲学非常直接击中 LoD-3DGS 核心瓶颈
- **Parallel filtering 与 L 解耦** — 工程洞察力强,理论上 scalability 极好
- **GTC 度量 universal**: 同一公式适用 tile/view/dataset 三层聚合,概念优雅
- **Adaptive vs Fixed threshold**: 论证了 FlashGS 固定 τ=1/255 大场景不够,learning-based 在 LoD 树过拟合
- **拆 X 验证**: Filter 单独 → 选 Gaussian 集合与 serial 完全一致 (Table 3 关键证据)
- **不做 NP trade-off**: shrinking 消 75% K-V pair 但保留 >80% high-KPC pair (visual-critical)

**短板**:
- **未在 mobile / edge GPU 评测** — 论文明确 cite LODGE (mobile LoD) 但只在 RTX 4090 单卡 eval,对我们 D 派系难以直接引用
- **Recursion 树结构 = depth-dependent memory precompute** — ancestor path 预计算需要 ~20% extra memory,在显存受限 (mobile 12MB L2) 场景需重新设计
- **未在 dynamic 4DGS 数据集 (D-NeRF / Plenoptic Video) 验证** — FilterGS 假设静态 LoD 树,4DGS deformation 场景需扩展
- **2D projection-based filter** — 依赖 view frustum 内 N 总数;超大规模场景 (10+ km²) in-frustum N 可能破 M**, 内存带宽可能成为新瓶颈
- **FPS 提升主要来自 filter 阶段,sort/α-blending 仍是瓶颈** — 论文未深入研究 sort 优化

**对我们的相关性**:
- **中高**。FilterGS 是大场景 LoD-3DGS 渲染的代表加速,与 mobile 在"LOD 多分辨率" 思路上同源 (LODGE 也用 LoD + mobile),但具体实现 (CUDA unified kernel, RTX 4090 假设) 不能直接 port 到 Adreno。
- **可借鉴设计**:
  - "Depth Decoupling" 思路 — mobile GPU 也可以把 L 层串行摊平,但需避免单 pass 内存爆炸。
  - GTC-based adaptive shrinking — τ 与场景拥塞程度反相关,这种"度量驱动自适应"思路对 mobile 很有用 (异构场景 fragment 负载差大)。
  - KPC (有效像素贡献) — 是非常合理的 mobile-friendly 度量,纯算术,不需要训练。
- **不能直接借鉴**:
  - Ancestor path 预计算 (~20% memory) — mobile VRAM 紧张可能要 on-the-fly 建树。
  - Filter 阶段单 pass 处理 1.5M Gaussians — 超 mobile GPU 内存预算,需 chunk-by-chunk。

## 8. 引用 (核心)
- [ref 8] Kerbl 2023, TOG — 3DGS 原论文 (cite at p.1, p.2, p.3, p.6)
- [ref 9] Kerbl 2024, TOG — Hierarchical-GS / H3DGS (cite at p.2, p.6)
- [ref 21] Ren 2024, arXiv — OctreeGS (cite at p.2, p.6)
- [ref 23] Seo 2024, arXiv — FLoD (cite at p.2, p.3, p.4, p.6)
- [ref 24] Shuai 2024 — LoG (zju3dv/LoG) (cite at p.2, p.3, p.4, p.6)
- [ref 3] Feng 2025, CVPR — FlashGS (fixed-threshold shrinking) (cite at p.1, p.2, p.3)
- [ref 10] Kulhanek 2025, arXiv — LODGE (mobile LoD) (cite at p.2)
- [ref 12] Li 2023, ICCV — MatrixCity dataset (cite at p.6, p.8)
- [ref 15] Lin 2022, ECCV — UrbanScene3D dataset (cite at p.6, p.7, p.8)
- [ref 32] Xiong 2024, arXiv — GauUScene v2 dataset (cite at p.6, p.7, p.8)
- [ref 31] Wei 2025, ICCAD — No-redundancy No-stall streaming (cite at p.2, p.3)
- [ref 36] Ye 2024, NeurIPS — 3DGS learned fragment pruning (cite at p.2, p.3)
- [ref 19] Lu 2024, CVPR — Scaffold-GS (cite at p.2)
- [ref 6] Hanson 2025, CVPR — Speedy-Splat (cite at p.2)
- [ref 13] Liao 2025, SIGGRAPH Asia — TC-GS (tensor cores) (cite at p.2)
- [ref 4] Feng 2024, TACO — Potamoi (cite at p.2)
- [ref 27] Tao 2025, arXiv — GS-Cache (cite at p.2)
- [ref 2] Fang 2024, ECCV — Mini-Splatting (cite at p.2)
- [ref 38] Zhang 2025, CVPR — GaussianSpa (cite at p.2)
- [ref 22] Schonberger 2016, CVPR — COLMAP (cite at p.6)
- [ref 30] Wang 2004 — SSIM (cite at p.6)
- [ref 37] Zhang 2018, CVPR — LPIPS (cite at p.6)

## 9. Insight

**Insight #1 — Depth Decoupling 是 LoD 渲染的核心 scalability 杠杆**。FilterGS 的 T_parallel = T_synch + T_calc(N) 与 L 解耦,让大场景 + 更深 LoD 树(L=10+) 而 filter time 不增长。这种"打破树深度依赖"思路对 mobile 尤其重要:mobile GPU kernel launch overhead 远大于 desktop,层间 synchronization 在移动 SoC 上是双重浪费 (compute + scheduling)。我们的 mobile port 应优先考虑 flatten L 层 traversal,即便牺牲一些 redundancy-reduction。

**Insight #2 — "度量驱动自适应" 是 universal 加速哲学**。GTC 度量场景拥塞→ τ 自适应→ shrinking 激进程度自适应。这套"measure → decide → act" 范式移植到 mobile:fragment shader 工作负载不均 (foreground vs sky tile 差 10×)→ 可类似地以 GTC 灵感测 tile 拥塞 → 动态调整 fragment 早期 z-test 或 simplified SH evaluation。避免一味的"用最坏情况预算"。

**Insight #3 — KPC (Key-value Pair Contribution) 是 mobile-friendly 的关键创新**。KPC = Σ α·T,纯算术 + transmittance 直接复用,**无需训练**。FlashGS 的固定阈值 vs FilterGS 的 GTC-driven 阈值,本质区别是 "全局一个阈值" vs "tile/scene 自适应阈值"。Mobile GPU 极度敏感于 per-tile 工作负载不均 (tile 名义上 16×16 pixel,但 in-frustum Gaussian 数 1 vs 100 差距巨大),KPC 类先验有助于 tile-level load balancing。

**Insight #4 — Pre-rendered GTC 是免费的全局信息**。FilterGS 在 inference 前预计算全数据集 GTC Ḡ,作为 constant 用于所有后续帧。这种 "preprocess once, use many times" 模式对 mobile 友好 (preprocess 一次性 offloaded to server / cloud),但不同场景切换时需重算。Mobile port 应考虑:是否能把 GTC 改为滑动窗口在线更新,权衡 precision vs recompute cost。

**Insight #5 — Filter 内部功能性验证 (Table 3) 是方法论亮点**。作者主动证明 Parallel Filter 选出的 Gaussian 集合与 Serial Traversal **完全相同** (PSNR/SSIM/NP 一致),说明优化是 "无信息损失" 的纯算法加速。这种严谨性是 paper 应有标准 — 我们的 mobile port 工作也要做"baseline-equal-output" 验证,避免被 reviewer 质疑 "加速但悄悄降质"。

## 11. 1-hop 关系图 (5 篇示范)

**核心 1-hop 关系图**:
- 节点 | 关系类型 | 上游/下游
- **LoG [Shuai 2024]** | direct comparison baseline;main rival on filter time / FPS (cite at p.2, p.3, p.4, p.6) | concurrent
- **H3DGS / Hierarchical-GS [Kerbl 2024, TOG]** | direct comparison baseline;first continuous LoD (cite at p.2, p.6) | concurrent
- **FLoD [Seo 2024, arXiv]** | direct comparison baseline;flexible LoD paradigm (cite at p.2, p.3, p.4, p.6) | concurrent
- **OctreeGS [Ren 2024, arXiv]** | direct comparison baseline;Octree-structured LoD (cite at p.2, p.6) | concurrent
- **FlashGS [Feng 2025, CVPR]** | methodological predecessor;fixed-threshold shrinking (cite at p.1, p.2, p.3) | upstream
- **LODGE [Kulhanek 2025, arXiv]** | methodological predecessor;mobile LoD (cite at p.2) | upstream inspiration

**未在 INDEX 的 1-hop 候选** (1-hop rule: 命中即停):
- SpeedySplat, TC-GS, Potamoi, GS-Cache, Mini-Splatting, GaussianSpa, Scaffold-GS, MatrixCity, UrbanScene3D, GauUScene v2, COLMAP, SSIM, LPIPS — 见其他 paper notes / datasets
