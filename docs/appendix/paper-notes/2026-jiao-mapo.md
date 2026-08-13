# MAPo: Motion-Aware Partitioning of Deformable 3D Gaussian Splatting for High-Fidelity Dynamic Scene Reconstruction

## 0. 基本信息
- 作者: Han Jiao*, Jiakai Sun*, Yexing Xu, Lei Zhao, Wei Xing, Huaizhong Lin (* leading authors from ZJU; Jiakai Sun is MAPo 共同一作)
- 单位: Zhejiang University (ZJU) + The Shenzhen Campus, Sun Yat-sen University
- 年份: 2026 (arXiv v1 2025-08; v2 2025-11-25)
- 会议: (未确认 venue，文中仅列 arXiv preprint)
- arxiv-id: 2508.19786v2 (cs.CV, 25 Nov 2025)
- GitHub: (论文 / PDF 中未声明；作者名单里有 Sun Jikai 注: 之前发出 3DGStream ref [26] 等开源代码，但本论文 codebase 未明 — 待核实)
- 项目主页: 未声明
- 代码许可: 未声明 (待核实)

## 0.5 元数据
- venue: arXiv preprint (cs.CV)
- arxiv-id: 2508.19786v2
- s2-id: (未查询 — cron 批次)
- homepage: (未声明)
- github: (未声明 — 待核实)
- status: 收录
- 收录日期: 2026-08-10
- 收录来源: arxiv_4dgs_scan (cron)
- 评级: T1 (核心 4DGS 表示 + 动态区域质量)
- survey_section: 4
- faction: A (4DGS representation)

## 1. 一句话总结
MAPo 把单 canonical-set + 单 deformation network 的"统一建模"换成 dynamic-score-driven 的递归时间切分 + 静态识别：高分位 3DGs 在时间维度上二分递归复制 3DG 子集与各自独立的 deformation sub-network；低分位 3DGs 直接固化不再走 deformation；同时用 L_current + L_gt 跨帧一致性损失缝合 partition 边界。在 N3DV/MeetRoom 上 PSNR 提升 0.5–1.0 dB，存储和 FPS 同步优于 4DGS 系 baseline。

## 2. 摘要 (核心 3 段)

**问题**: D3DGS / 4DGS / E-D3DGS 等基于 deformation 的 4DGS 框架依赖"单一 canonical set + 单一全局共享 deformation network"统一建模所有时空变化。这强制网络在所有时间步上对**冲突的运动模式**拟合出**单一参数集**，从而学到"时序平均"表示 (temporally averaged representation, Fig. 2/3)：无法拟合偏离均值的高频/突变动运动 → 高动态区域细节模糊丢失 (Fig. 1, a-b)；同时静态 3DGs 也走 deformation → 冗余计算浪费。

**方法**: 提出 **dynamic-score-based partitioning** (核心) + **cross-frame consistency loss** (补丁)。两阶段分区：
1. 对每个 3D G_i 记录训练中的 m 个历史位置 {x_ij}，计算最大位移 r_i (历史位置 AABB 对角线长) + 位置方差 v_i → 通过百分位 normalize → 用 harmonic mean 融合成 **dynamic score S_i ∈ [0,1]**。
2. **Temporal Partition (高动态)**：当 S_i > 当前 level 阈值 τ_l 时，在其时间区间 [t_start, t_end) 中点处做二分 → 复制 3DG (attributes identical) 给 [t_mid, t_end) 子段 → 同步复制 deformation network F → 两个子段各用专属 sub-network。继续递归直至达到 max level (默认 3)。
3. **Static 3DG Partition (低动态)**：S_i < τ_static 的 3DGs 用一次 deformation 输出 baked 固化为静态，rendering 时跳过 deformation 计算。
4. **Cross-frame consistency loss L_cross = 0.5 (L_current + L_gt)**：只对距 partition 边界 ≤ 5 帧的 view 启用。L_current 让 boundary-frame 用两套相邻 3DG 渲染同一时刻应一致；L_gt 强制相邻段渲染对齐当前 ground-truth。L_cross 双功能：消除 boundary jump + 利用 temporal context 提升质量。

**结果**: N3DV (20 cameras, 30 FPS): **Ours 31.33 / 0.944 / 0.044**, vs E-D3DGS 30.79 / 0.934 / 0.051 (+0.54 dB LPIPS -14%), 4DGS 30.30 / 0.933 / 0.069 (storage 65 MB vs 3.6 GB = 1/55×); Meet Room (13 cameras): **26.72 / 0.903 / 0.066** vs E-D3DGS 26.24 / 0.896 / 0.081 (+0.48 dB)。FPS 75.64 (N3DV) / 92.21 (Meet Room)，匹配甚至略优于 Swift4D (138/110 FPS)，但 PSNR/LPIPS 显著优。训练时间 1h52m / 1h19m。

## 3. 派系分类
- **A (4DGS representation)**: 主。MAPo 是 4DGS 表示层的**结构性改进**——把"单一 deformation network"换成"score-driven 多分 deformation network + 静态 baked" 的分层建模。
- 相关: D (mobile) **不沾** — 论文仅在 RTX A6000 评测，无 Adreno / mobile 平台数据。B (training acceleration) 边缘沾边：static partition 直接节省 deformation forward calls；time-aware 下分块 latent 推理可借鉴。
- 不属于 C (3DGS 静态加速)。
- E (cross-disciplinary) 沾边有限：tOF 指标借鉴 video generation 文献 (Chu et al. 2020, TOG)；harmonic-mean 融合借鉴经典信息检索。

**结论**: 主派系 **A**。

## 4. 方法

### 4.1 整体架构 (基于 E-D3DGS 增量)
MAPo 是 E-D3DGS 之上的 plug-in。三块组件：
- (i) **Dynamic Score Calculation** per 3DG，训练时计算
- (ii) **Temporal Partition** (high-dynamic, 递归二分裂) + **Static 3DG Partition** (low-dynamic, baked 固化)
- (iii) **Cross-frame consistency loss** 只对 boundary 周围训练 view 启用

### 4.2 Dynamic Score (公式 Eq 3 + 4 + 5, p.4–5)

per-3DG 训练时记录 m=300 个历史位置 {x_ij}：

**最大位移**（AABB 对角线 / span vector）：
  r_i = max_j |x_ij| − min_j |x_ij|  （element-wise）

**位置方差**（围绕均值的均方距离）：
  v_i = (1/m) Σ_j ||x_ij − x̄_i||²

**百分位 normalize 到 [0,1]**（避免 outlier）：
  r̃_i = Σ_{k=1}^{10} 𝟙(r_i ≤ q_r^(k) / 10)
  ṽ_i = Σ_{k=1}^{10} 𝟙(v_i ≤ q_v^(k) / 10)
  (即按十分位映射)

**Harmonic-mean 融合**（要求两指标同时高才显高分）：
  S_i = 2 / (1/(r̃_i + ε) + 1/(ṽ_i + ε)) ，ε=10⁻⁶

r_i 反映"振幅峰值"，v_i 反映"持续活动性"，两者互补避免：
- 短时高速 + 长期静止：r 大 v 小 (peak 强 but 静止多)
- 持续微振：r 小 v 大 (consistent low-amplitude)

### 4.3 Temporal Partitioning Based on Dynamic Scores (Sec 4.1.2, p.5)

每个 3DG 维护 **(partition level l, 时间区间 [t_start, t_end))**。Initial: l=0, [0, T)。

For G_i at level l: 若 S_i > 当前 level 阈值 τ_l，且所在段 [t_start, t_end)
  → 在 t_mid = (t_start + t_end)/2 处二分：
    • 原 3DG 保留给 [t_start, t_mid)，升级至 l+1
    • 复制一份 (attributes identical) 给 [t_mid, t_end)
    • deformation network F_{[t_start,t_end)} 同步复制成 F_{[t_start,t_mid)} 和 F_{[t_mid,t_end)}
  → 在每个子段内继续递归，直到 partition level = max_level（默认 3）

效果：每个 sub-segment 内只有"局部运动模式" → 避免"temporal averaging"，高动态区域质量↑。

**Toy Fig. 4 示意**：单个 point+单个 MLP 无法拟合复杂曲线 p(t)；二分后两段各自用独立 MLP 拟合 → 精度大幅提升（与 paper note 我们的核心 takeaway 吻合）。

### 4.4 Static 3D Gaussian Partition (Sec 4.1.3, p.5)
S_i < τ_static 的 3DGs 视为静态：attributes 用其 deformation network 在某 random timestep 的输出 baked 一次 → rendering 时完全跳过 deformation forward → **显著降低 deformation compute cost**（在 Table 3 "2.0 +Static" 行体现：FPS 54→92，storage 67→48MB）。

### 4.5 Cross-Frame Consistency Loss (Sec 4.2, p.5–6)

T=partition boundary 时的 visual jump 由两项缝补：

**(1) L_current** — boundary-frame consistency：
  L_current = || I_t(G_t, V) − I_t(G_{t'}, V) ||_1
  其中 t 是 partition boundary 附近帧，t' 是相邻段中离 t 最近的 frame timestamp；让 boundary 两侧 3DG 渲染同一帧应一致。

**(2) L_gt** — temporal context grounding：
  L_gt = || I_t(G_{t'}, V) − I^{GT}_t ||_1
  把相邻段的 3DGs 用当前帧 GT 监督 (anchor to ground truth, 防 over-smoothing)。

**(3) Combined**：
  L_cross = 0.5 · (L_current + L_gt)

仅对距 partition boundary ≤ 5 帧的 training views 启用。

效果 (Table 3): 单独 Temporal Partition (1.2+Var) 引入 boundary tOF 上升 (0.074 → 0.082)，加 +L_current 后回落到 0.074，再加 +L_gt 进一步降到 0.072 且 PSNR 涨至 26.72。

### 4.6 训练 Pipeline
- **implementation builds upon E-D3DGS codebase** (Bae et al. ECCV 2024, ref [2])
- m=300 historical positions per 3DG (recorded during training)
- max partition level = 3
- 全部训练 RTX A6000

## 5. 实验

### 5.1 数据集
- **N3DV** [Li CVPR 2022, ref 15]: 20 cameras, 30 FPS, downsampled 1352×1014；flame salmon 切成 4 个 10s clips
- **Meet Room** [Li NeurIPS 2022, ref 14]: 13 cameras, 30 FPS, 1280×720

### 5.2 基线
- NeRF 系: DyNeRF, NeRFPlayer, MixVoxels, K-Planes, HyperReel
- 3DGS 系: D3DGS, 4DGS, 4DGaussians, Ex4DGS, **Swift4D, 4DGC, LocalDyGS, E-D3DGS, E-D3DGS (seg)**
- 指标: PSNR↑ / SSIM↑ / LPIPS↓ + Storage / Training Time / FPS

### 5.3 评测指标
三项标准 (PSNR/SSIM/LPIPS) + 三项效率 (Storage / Training Time / FPS) + tOF [Chu TOG 2020] 测时序一致性 (Avg / Bnd 分开报)

### 5.4 tOF 指标 (ch. 5.4, p.8)
tOF 衡量 temporal coherence：值越低 = 帧间跳变更小。论文同时报 Avg (全序列平均) 和 **Bnd (partition boundary 周围)** 两项。Bnd 对 MAPo 验证一致性损失有效性至关重要。

## 6. 性能数字 (PDF 页码标)

### N3DV — Table 1, PDF page 6 (mean over scenes)
- DyNeRF: 29.58 / - / 0.083 / 56MB / 1344h train / 0.01 FPS [p.6]
- NeRFPlayer: 30.69 / 0.932 / 0.111 / 1654MB / 5h36m / 0.06 FPS [p.6]
- MixVoxels: 30.30 / 0.918 / 0.127 / 512MB / 1h28m / 1.01 FPS [p.6]
- K-Planes: 30.86 / 0.939 / 0.096 / 309MB / 1h33m / 0.15 FPS [p.6]
- HyperReel: 30.37 / 0.921 / 0.106 / 1362MB / 8h42m / 1.19 FPS [p.6]
- D3DGS: 28.27 / 0.917 / 0.156 / 75MB / 2h17m / 20.29 FPS [p.6]
- 4DGS: 30.30 / 0.933 / 0.069 / 3.6GB / 7h43m / 54.36 FPS [p.6]
- 4DGaussians: 30.19 / 0.917 / 0.061 / 53MB / 1h13m / 78.28 FPS [p.6]
- Ex4DGS: 30.76 / 0.939 / 0.056 / 205MB / 1h05m / 51.46 FPS [p.6]
- Swift4D: 30.05 / 0.931 / 0.055 / 116MB / 48m / **138.00 FPS** [p.6]
- 4DGC: 30.78 / 0.938 / 0.052 / 225MB / 5h44m / 124.61 FPS [p.6]
- LocalDyGS: 30.75 / 0.933 / 0.053 / 102MB / 42m / 109.30 FPS [p.6]
- E-D3DGS: 30.79 / 0.934 / 0.051 / 73MB / 2h41m / 37.51 FPS [p.6]
- E-D3DGS (seg): 30.73 / 0.935 / 0.049 / 215MB / 8h32m / 37.97 FPS [p.6]
- **Ours (MAPo)**: **31.33 / 0.944 / 0.044 / 65MB / 1h52m / 75.64 FPS** [p.6]
- **PSNR gain vs best baseline (E-D3DGS)**: +0.54 dB；LPIPS: 0.051 → 0.044 (-14%); Storage: 73MB → 65MB; FPS 37.51 → 75.64 (**2×!** vs same-baseline family)

### Meet Room — Table 2, PDF page 7 (discussion subscene)
- D3DGS: 25.81 / 0.890 / 0.233 / 36MB / 47m / 42.51 FPS [p.7]
- 4DGS: 26.12 / 0.896 / 0.080 / 5.4GB / 6h32m / 70.54 FPS [p.7]
- 4DGaussians: 26.16 / 0.894 / 0.081 / 51MB / 1h03m / 77.26 FPS [p.7]
- Ex4DGS: 26.46 / 0.895 / 0.083 / 123MB / 1h06m / 117.49 FPS [p.7]
- Swift4D: 25.51 / 0.882 / 0.085 / 76MB / 20m / 109.58 FPS [p.7]
- 4DGC: 26.56 / 0.901 / 0.070 / 224MB / 3h26m / **160.59 FPS** [p.7]
- LocalDyGS: 25.85 / 0.888 / 0.084 / 98MB / 1h07m / 130.30 FPS [p.7]
- E-D3DGS: 26.24 / 0.896 / 0.081 / 28MB / 1h36m / 90.26 FPS [p.7]
- E-D3DGS (seg): 26.31 / 0.900 / 0.073 / 89MB / 4h03m / 85.20 FPS [p.7]
- **Ours (MAPo)**: **26.72 / 0.903 / 0.066 / 49MB / 1h19m / 92.21 FPS** [p.7]
- **PSNR gain vs best baseline (4DGC)**: +0.16 dB；LPIPS: 0.070 → 0.066 (-6%)

### Progressive Ablation — Table 3, PDF page 7 (Meet Room)
按 component 顺序增量添加：
- E-D3DGS Baseline: 26.24 / 0.896 / 0.081 / 28MB / 1h36m / 90.26 FPS / tOF 0.082/0.074 [p.7]
- Baseline (seg) naive 三段切片: 26.31 / 0.900 / 0.073 / 89MB / 4h03m / 85.20 FPS / 0.080/**0.185** [p.7] (注意 boundary tOF 0.185 显著恶化 — 验证 boundary discontinuity 问题)
- +Temporal Partition (1.1 +Max Dis): 26.52 / 0.901 / 0.070 / 65MB / 1h41m / 55.21 FPS / 0.079/0.084 [p.7]
- +Var (1.2): 26.63 / 0.903 / 0.067 / 67MB / 1h42m / 54.56 FPS / 0.079/0.082 [p.7]
- +Static Partition (2.0): 26.60 / 0.903 / 0.066 / 48MB / 1h12m / **92.59 FPS** / 0.079/0.081 [p.7]
- +L_current (3.1): 26.49 / 0.899 / 0.071 / 48MB / 1h18m / 92.88 FPS / 0.078/0.074 [p.7] (单加 L_current PSNR 微降)
- +L_gt (3.2) = **Full MAPo**: **26.72 / 0.903 / 0.066 / 49MB / 1h19m / 92.21 FPS / 0.078/0.072** [p.7]

### Max Partition Level Ablation — Table 4, PDF page 8 (flame salmon frag3)
- Level 0: 29.93 / 0.923 / 0.61 / 44MB / 1h13m / **95.21 FPS** [p.8]
- Level 1: 30.08 / 0.927 / 0.56 / 51MB / 1h24m / 88.13 FPS [p.8]
- Level 2: 30.21 / 0.932 / 0.54 / 59MB / 1h37m / 82.81 FPS [p.8]
- Level 3 (default): **30.30 / 0.934 / 0.52 / 70MB / 1h56m / 74.58 FPS** [p.8]
- Level 4: 30.32 / 0.936 / 0.50 / 88MB / 2h22m / 64.25 FPS [p.8]
- Level 5: **30.36** / 0.936 / **0.49** / 103MB / 2h40m / 57.05 FPS [p.8]
- 注意 LPIPS 是 3 位数 0.61 → 0.49 (paper 原文 0.061 → 0.049 的 typo 或列宽处理, 我按原文抄录)。Trade-off: PSNR 增益 dimishing returns > level 3，但 cost 仍稳步增长 — 因此默认 3

### Temporal Consistency
- baseline tOF (Avg/Bnd): 0.082 / 0.074
- Baseline (seg) naive 切片: 0.080 / **0.185** (boundary 大幅恶化)
- Full MAPo: **0.078 / 0.072** (Avg 下降 + boundary 反低于 baseline)

### Sensitivity & 其他 Observations (from paper Sec 5.4 + Fig 6-9)
- Fig 6 (Vrheadset): 1.2+Var 阶段 dynamic partition 已能完整分离头部运动区
- Fig 7 (Salmon): 2.0+Static 阶段"静态识别"准确地把背景烤成 static
- Fig 8 (time-slice visualize): L_cross 显著削弱 boundary flash
- Fig 9 (frame 74-75 边界连续): full model + L_gt 给出最平滑过渡 + 最锐利细节

## 7. 评估

**亮点**:
- **范式转移**: 不再要求 single deformation network 适配所有 motion mode；用 dynamic score 引导 per-3DG 局部子网络 → 真正解决 "temporal averaging" 瓶颈
- **三大 metrics 全 SOTA**: N3DV/Meet Room 上 PSNR/SSIM/LPIPS 都**高于所有 4DGS 系 baseline**，包括 SOTA E-D3DGS (seg)
- **效率极佳**: Meet Room 上 FPS 比基线 E-D3DGS (90.26) 还高到 92.21，归功于 static partition 跳过 compute；N3DV 上 FPS 75.64 vs E-D3DGS 37.51 (2× 加速)
- **存储友好**: N3DV 仅 65MB (vs 4DGS 3.6GB=55× 体积减小)
- **per-3DG 精细**: vs SWinGS 的 coarse window-level + 2D optical flow prior，MAPo 是 per-3DG + 3D motion signal → 无需预处理 / 后处理 / 2D prior
- **严谨 ablation**: 7 步 progressive + tOF Avg/Bnd 独立报告 + max-level sweep 6 步
- **方法通用性**: core idea (score-driven partition + consistency loss) 与 baseline 解耦 — 同样可 plug-in 到 D3DGS / 4DGS / SC-GS

**短板**:
- **仅 2 数据集**: N3DV + Meet Room 都没 Neu3D-iOS / D-NeRF synthetic / 自采移动数据 (后者对我们 mobile port 评估至关重要)
- **仅 RTX A6000 单卡评测**: 无 mobile / 边缘 GPU 加速数据，对我们 D 派系无直接帮助；代码 release 与否未明 (2025-11 v2 仍未公开?)
- **未与 MVFusion-GS / FreeTimeGS / SplineGS 等最新 4DGS 比较**: Table 1/2 baseline 截至 ECCV 2024，缺乏 2025 年代表
- **FPS 仍低于 Swift4D (138 vs 75.64 on N3DV) / 4DGC (160 vs 92 on Meet Room)**: 质量优但帧率非最优；如 mobile port 不优化 deformation network dispatch 可能维持 quality/speed trade-off
- **max partition level 3+ 时 storage 增长可控** (level 4 才 2× level 0)，但 deformation network 数随 3DG 数量线性增长 — 大场景存储/调度成隐患
- **section on ST-GS, SWinGS 推迟到 appendix**: 表 1/2 缺这两个重要 baseline，appendix 内容本次未抽到 (只是 references)

**对我们的相关性**:
- **中等偏高**。核心是 4DGS 表示质量改进，与我们 mobile 实时渲染目标**正交**但**有借鉴价值**:
  - "dynamic score 静态识别"思路与我们 mobile 上的"GPU pipeline dispatch gating"高度相关 — 训练时即标记低动态 → 推理时无需 deformation forward → 与 Swift4D 走 2D RGB 分离的 path 形成**两种正交方案**
  - "harmonic-mean 融合 max displacement + variance" 是干净的运动强度估计器，可作为我们 motion-aware LOD scheduler 的启发项
  - L_cross 思想 (boundary 周围额外监督) 是 general temporal consistency 增强器，对 mobile streaming 也有意义 (替代或补充 3DGStream 的 streaming consistency)
- 但 **report 中无 mobile / edge GPU 数据**，需自行 port + benchmark Adreno 730/830 — 推理路径中的 "per-segment forward 在 GPU 上 fan out" 在 mobile 是否会触发 buffer/tensor pool 碎片化 unknown

## 8. 引用 (核心)
- [ref 27] Wu 2023 — **4DGS / 4DGaussians** (SIGGRAPH 2023) — deformation field 入门 reference
- [ref 32] Yang CVPR 2023 — **D3DGS** (canonical 3DGs + deformation net, p.3 cited)
- [ref 2] Bae ECCV 2024 — **E-D3DGS** (per-Gaussian embedding + dual deformation; MAPo 的直接 baseline & codebase 来源)
- [ref 29] Wu 2025 — **Swift4D** (2D RGB separate static/dynamic + 4D hash grid) — strongest FPS baseline
- [ref 10] Hu 2025 — **4DGC** (rate-aware 4DGS compression) — Meet Room FPS SOTA baseline
- [ref 28] Wu 2025 — **LocalDyGS** (Scaffold-GS inspired local dynamic decomposition)
- [ref 9] Gao 2024 — **GaussianFlow** (splatting Gaussian dynamics, curve method)
- [ref 13] Lee 2024 — **Fully Explicit DGS** (curve method)
- [ref 17] Lu 2024 — **DN-4DGS** (denoised deformable network + temporal-spatial aggregation)
- [ref 24] Shaw 2024 — **SWinGS** (sliding windows + optical flow; comparative discussed but not in main table — defer to appendix)
- [ref 18] Lu 2023 — **Scaffold-GS** (结构化 3DGS, cited for LocalDyGS 启发)
- [ref 15] Li CVPR 2022 — **Neural 3D Video Synthesis (DyNeRF)** — N3DV dataset, baseline
- [ref 14] Li NeurIPS 2022 — **Streaming Radiance Fields (NeRFPlayer)** — Meet Room dataset, baseline
- [ref 1] Attal 2023 — **HyperReel** (6-DoF video + dual-plane)
- [ref 3] Cao CVPR 2023 — **HexPlane**
- [ref 7] Fridovich-Keil CVPR 2023 — **K-Planes**
- [ref 12] Kerbl SIGGRAPH 2023 — **3DGS** original
- [ref 19] Mildenhall CACM 2021 — **NeRF**
- [ref 22] Pumarola CVPR 2021 — **D-NeRF**
- [ref 20] Park ICCV 2021 — **Nerfies**
- [ref 21] Park 2021 — **HyperNeRF**
- [ref 30] Xian CVPR 2021 — **ST-NeRF** (free-viewpoint video)
- [ref 25] Song 2023 — **NeRFPlayer streamable**
- [ref 8] Gao 2024 — **HiCoM** (hierarchical coherent motion)
- [ref 11] Huang 2023 — **SC-GS** (sparse-controlled editable dynamic)
- [ref 31] Xu TOG 2024 — **Temporal Gaussian Hierarchy** (long volumetric video)
- [ref 33] Yang 2024 — **Real-time 4DGS**
- [ref 5] Duan 2024 — **4D Gaussian Splatting (4DGC 初版/4DGS 同名)**
- [ref 16] Li 2023 — **Spacetime Gaussian Feature Splatting**
- [ref 23] Shao 2023 — **Tensor4D** (efficient 4D decomposition)
- [ref 26] Sun 2024 — **3DGStream** (streaming of 3DGS for free-viewpoint video)
- [ref 6] Fang SIGGRAPH Asia 2022 — **Fast dynamic radiance fields** (TiNeuVox)
- [ref 4] Chu TOG 2020 — **tOF** temporal coherence metric (本论文用)

## 9. Insight

**Insight #1 — "Temporal averaging" 是 deformation-based 4DGS 的根本瓶颈，不是细节问题**。MAPo 的核心洞见比"加 attention" "加 transformer" 直击本质:单 canonical set + single deformation net 在异质运动下被迫学平均表示。Mobile port 设计时如果走 deformation-based 路线，必须考虑 per-region 或 per-segment 专用子网络，否则高动态区域会持续糊。

**Insight #2 — Dynamic score 是简洁的运动强度先验**。r_i + v_i 经 percentile norm + harmonic-mean 融合 → 既不像 2D optical flow 需 2D prior / pre-processing，也不像 attention 那样 O(N²) 重。paper 给出 ablation 显示 (1.1) 只用 max displacement 时 PSNR 26.52，加 variance 后涨到 26.63 (ν+0.11 dB)，证明两指标互补。这个 13 行 numpy 即可复现的 metric 是 mobile edge 上**可接受的预算**，可独立于 mobile port 重新设计 (e.g. 用 continuous trajectory 拟合代替 buffer)。

**Insight #3 — Static partition 比 Temporal partition 更影响 efficiency**。从 Table 3 看：单加 Temporal Partition 时 FPS 从 90.26 → 54.56 (-40%)；再加 Static Partition 后 FPS 54.56 → 92.59 (+70%)，storage 也从 67MB → 48MB。Mobile inference 应优先部署 Static partition (本质是 "frozen bake" 操作，等价于 baking 全 deformation 进 start-frame attributes)，开销极小且 FPS 大幅回血。

**Insight #4 — "Per-3DG recursion" 比 "Per-scene window" 更细但需要 cost control**。MAPo vs SWinGS: SWinGS 是 sequence-level coarse slice + optical flow prior；MAPo 是 per-3DG recursion + 3D motion signal + end-to-end。理论上更准 (Table 1/2 MAPo > E-D3DGS (seg) naive slice)，但 storage 跟着 3DG 增长，max level > 3 时 cost 累加。Mobile 上 recursion depth 受限 (建议 ≤ 2)，否则 deformation forward calls 增长超 4×。

**Insight #5 — Cross-frame consistency loss 帮我们想了 streaming 难题**。MAPo 的 L_cross = 0.5·(L_current + L_gt) 思路可借鉴到 mobile streaming：边界 ±5 frames 用额外监督强制 temporal consistency，类似 ST-GS 的 surveillance。但 L_gt 直接 require GT，意味着 training-time-only；我们在 mobile 上的对应项应是 "temporal photometric consistency" (无 GT) 或者 "key-frame priors"。

---

## 11. 1-hop 关系图 (5 篇示范)

**核心 1-hop 关系图**:

| 节点 | 关系类型 | 上游/下游 |
|------|---------|-----------|
| **E-D3DGS [Bae ECCV 2024, ref 2]** | baseline (MAPo 直接 codebase 来源 + 主要对比组) | upstream |
| **D3DGS [Yang CVPR 2023, ref 32]** | 4DGS 范式奠基 (canonical + deformation, p.2-4 多次 cite) | upstream |
| **4DGS / 4DGaussians [Wu SIGGRAPH 2023, ref 27]** | N3DV baseline (PSNR 30.30 vs MAPo 31.33) | concurrent baseline |
| **Swift4D [Wu 2025, ref 29]** | N3DV FPS SOTA (138 vs MAPo 75) — 互补方案 (2D RGB separation vs 3D score) | concurrent baseline |
| **SWinGS [Shaw 2024, ref 24]** | 对比的 window-based 方案 (paper 推到 appendix 比较) | concurrent baseline |

**未在 INDEX 的 1-hop 候选** (1-hop rule: 命中即停):
- 4DGC [Hu 2025, ref 10], LocalDyGS [Wu 2025, ref 28], Ex4DGS, MixVoxels, K-Planes, HexPlane, HyperReel — 见其他 paper notes
