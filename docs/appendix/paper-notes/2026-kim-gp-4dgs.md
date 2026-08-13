# GP-4DGS: Probabilistic 4D Gaussian Splatting from Monocular Video via Variational Gaussian Processes

## 0. 基本信息
- 作者: Mijeong Kim¹, Jungtaek Kim³, Bohyung Han¹,² (PDF p.1)
- 单位: ¹ECE and ²IPAI, Seoul National University, Korea; ³University of Wisconsin–Madison, USA (PDF p.1)
- 年份: 2026 (arXiv:2604.02915v2, 8 Jul 2026) [PDF p.1]
- 会议: 未在 PDF 披露 (PDF 中无显式 venue 声明；任务提示词标注 CVPR 2026 main)
- arxiv-id: 2604.02915
- GitHub: 未在 PDF 披露
- 项目主页: 未在 PDF 披露
- 代码许可: 未在 PDF 披露

## 0.5 元数据
- venue: CVPR 2026 (main) (per task prompt; 未在 PDF 披露)
- arxiv-id: 2604.02915
- status: 收录
- 收录日期: 2026-08-10
- 收录来源: 人工 (本次 9 篇批)
- 评级: T1 (核心 4DGS 表示；**论文未给 FPS/延迟/显存测量，不涉及渲染加速**)
- survey_section: 3
- faction: A

## 1. 一句话总结
GP-4DGS 是首个把变分高斯过程 (variational Gaussian Processes) 与 4D Gaussian Splatting 结合的概率框架：用 spatio-temporal composite kernel 建模 4D Gaussian primitives 的 deformation field，配合 inducing points 把 O(N³) 降到 O(NM²+M³)，从而同时获得 (i) motion 不确定性量化、(ii) 训练帧外的未来运动外推、(iii) 在 occlusion/sparse-view 区域的 data-adaptive motion priors。

## 2. 摘要 (核心 3 段)

**问题 (PDF §1, p.1-2)**: Dynamic scene reconstruction from monocular videos [PDF p.1]。当前 4DGS 方法 (D-3DGS, 4DGS, STG 等) 把 motion 当成 deterministic optimization 问题，强制套用 polynomial [23]、rigidity [2] 等手工 priors，对所有 primitives 一视同仁 [PDF p.2]。当 primitives 被 occlude 或观察稀疏时，这些 fixed priors 失当；且现有方法缺少 principled uncertainty estimation 与 beyond-training-frame 的 motion extrapolation 机制 [PDF p.2]。

**方法 (PDF §4, p.4-6)**: 三件事：
1. **Probabilistic deformation modeling** (§4.1): 把每个 Gaussian primitive 的 (3D translation + 6D rotation) deformation y∈R^d (d=9) 建模成 multi-output GP。Composite kernel = spatial Matérn (各向异性 ℓ_{s,i,j}, 处理几何 smoothness 与多物体 discontinuity) + temporal Matérn×periodic (捕获 motion periodicity) [PDF p.4, Eq. 10-13]。
2. **Variational GP with inducing points** (§4.2): 选 M≪N 个 inducing points Z={z_m}∈R⁴；spatial xs 通过 Chronos 时间序列特征 + k-means 选 M_spatial [PDF p.5 §4.2]，t uniform 采 M_time；|Z| = M_spatial × M_time [PDF p.11, Eq. B]。ELBO = Σᵢ [E_q[log p(yᵢ|uᵢ)] − KL[q(uᵢ)‖p(uᵢ)]] 联合优化 kernel hyperparams + Z + variational {mᵢ,Sᵢ} [PDF p.5, Eq. 14]。推理 O(M) per query [PDF p.5, Eq. 15-16]。
3. **GP-GS dual optimization** (§4.3): 两 stage 交替 — Stage 1: 用 α-blending 权重 C_k = Σ_I Σ_r ω_k(r) 选 confident subset D_C (C_k > τ_C)，加 Gaussian noise N(0, 0.02)（**PDF p.5 Eq.18 未明示 std vs variance**）正则化训练 GP；Stage 2: 每 N_GP=2000 iter 重训 GP 一次并 cache 预测 μ̄*，用 GP guidance loss L_GP = E[δ(k,t)·‖y(k,t)−μ̄*(k,t)‖²] (δ 为偏差指示器，threshold τ_δ 从 τ_δ,start annealed 到 τ_δ,end) 正则化 GS；总 loss = L_recon + λ_GP L_GP, λ_GP=0.1 [PDF p.5-6, Eq. 17-19]。

**结果 (PDF §5, p.6-8)**: 在 DyCheck (All / SoM 5 / Challenging subset) 上 mPSNR↑ 与 mLPIPS↓ 全面刷 SOTA，mSSIM 与 SoM 在 All (0.65/0.65) 与 Challenging (0.46/0.46) 上打平 [PDF Table 1, p.6]。Challenging subset (reduced viewpoint overlap) 提升最大: SoM 14.56 → GP-4DGS 15.02 mPSNR (+0.46), LPIPS 0.53→0.51 [PDF Table 1, p.6]。Periodic motion extrapolation (last 5 frames withheld): linear 11.55 → GP-4DGS 17.62 PSNR (+6.07 dB) [PDF Table 2, p.7]。Non-periodic 5-frame extrapolation: 15.02 → 15.27 (+0.25) [PDF Table 2, p.7]。Uncertainty quantification (AUSE-MSE, ×10⁻²): Random 9.76 / UA-4DGS 7.60 / GP-4DGS 7.22 (Top 20 frames) [PDF Table 3, p.8]。Inducing-point init 用 Chronos time-series feature 优于 random + velocity KNN (ELBO avg 1.53 vs 1.10 / 1.37) [PDF Table 4, p.8]。

## 3. 派系分类
- **A (4DGS representation)**: 主。GP-4DGS 直接替换/增强 4DGS 的 deformation field，用概率建模替代 deterministic prior，是 4DGS 表示层的根本性改进。
- 沾边: **B (training acceleration)** — variational inducing points + cache-based GP inference 把 O(N³) 降到 O(NM²+M³)，是 scalable training/inference 设计。
- 沾边: **E (cross-disciplinary)** — 把 Gaussian Processes (经典 ML, Rasmussen & Williams 2006 [37]) 引入 4DGS，是概率建模与神经图形的跨界整合；用 Chronos (时间序列基础模型) 做 inducing point initialization [PDF p.11]。
- 不属于: **C (3DGS 加速/静态)** — 本论文核心是 dynamic reconstruction，不针对静态 3DGS。
- 不属于: **D (移动端)** — 论文无任何 mobile / edge GPU 实验，未涉及轻量化。

**结论**: 主派系 **A**。

## 4. 方法

### 4.1 Probabilistic Deformation Modeling (§4.1)
每个 Gaussian primitive 的 deformation y ∈ R^d (d=9: 3D translation + 6D continuous rotation [Zhou 2019]) 用一个 multi-output GP 建模，x=(p,t)∈R⁴ 是 canonical position + time。Composite kernel 显式分离 spatial/temporal 分量 [PDF p.4, Eq. 10]:
- **Spatial Matérn kernel**: 各向异性 scaled distance r_{s,i} = √(2νᵢ·Σⱼ(pⱼ−p'ⱼ)²/ℓ²_{s,i,j})，选 Matérn 而非 RBF 因为能处理 discontinuity (多物体场景) [PDF p.4, Eq. 11]。
- **Temporal kernel = Σⱼ Matérn(pⱼ,p'ⱼ) · periodic(t,t')**: 把 per-axis spatial Matérn 与 periodic kernel 相乘；periodic 形式 k_periodic ∝ exp(−2 sin²(π|t−t'|/τ)/ℓ²) 提供 extrapolation 归纳偏置 [PDF p.4, Eq. 12-13]。

### 4.2 Scalable Variational GP with Inducing Points (§4.2)
- 选 M≪N 个 inducing points 近似 full GP；复杂度 O(NM²+M³) [PDF p.5]。
- **Inducing point 初始化**: spatial 维度用 Chronos 时间序列模型 (per-axis 256-dim embedding，concat → 768-dim F_k) + k-means 选 M_spatial；t 维度在 [0,1] uniform 采 M_time；|Z| = M_spatial × M_time [PDF p.11, Eq. A-B]。
- **ELBO 训练**: 联合优化 kernel hyperparams (length scales / signal variances / periods) + Z + variational posterior q(u_i) = N(m_i, S_i) [PDF p.5, Eq. 14]。
- **推理**: O(M) per query — predictive mean = k*ᵀ K_ZZ⁻¹ m_i，variance = k*_i − k*ᵀ Σ_i k* [PDF p.5, Eq. 15-16]。

### 4.3 GP-GS Optimization Loop (§4.3, Algorithm 1, p.5)
两 stage 交替:
- **Stage 1 — GP Training**: 算 C_k = Σ_I Σ_r ω_k(r) 选 confident subset D_C (threshold τ_C)；输入加 N(0,0.02) Gaussian noise 正则化；ELBO 优化 [PDF p.5-6, Eq. 17-18]。
- **Stage 2 — GS Optimization**: GP 推理 cache μ̄*(k,t)，每 N_GP=2000 iter 刷新一次；GP guidance loss 只惩罚 ‖y−μ̄‖>τ_δ 的 primitives；τ_δ annealed 收紧；λ_GP=0.1 [PDF p.6, Eq. 19]。
- L_recon follows SoM [46]: photometric + D-SSIM + flow + smoothness [PDF p.6]。

### 4.4 Uncertainty Quantification (§4.4)
- Translation: 直接取前 3 维 variance σ̄*。
- Rotation: 6D→matrix 是非线性的，用 Monte Carlo sampling S 次采 deformation → 算 position variance U_{k,t} = Var({p^(s)_{k,t}})，再 α-blend 渲染成 motion uncertainty map Û(r) = Σ_k U_{k,t}·ω_k(r) [PDF p.6, Eq. 20-21]。

### 4.5 Future Motion Extrapolation (§4.5)
直接 query trained GP at x*_f = (p, t_f)，无额外训练或架构改动 [PDF p.6]。配合 periodic kernel 可做长期外推 (cyclic motion)。

## 5. 实验结果

### 5.1 主表 DyCheck (Table 1, PDF p.6)
| Split | Method | mPSNR↑ | mSSIM↑ | mLPIPS↓ |
|-------|--------|--------|--------|---------|
| All | Gaussian Marbles [42] | 15.84 | 0.54 | 0.57 |
| All | SoM [46] | 17.09 | 0.65 | 0.39 |
| All | **GP-4DGS** | **17.38** | **0.65** | **0.37** |
| SoM 5 | SC-GS [23] | 14.13 | 0.48 | 0.49 |
| SoM 5 | D-3DGS [51] | 11.92 | 0.49 | 0.66 |
| SoM 5 | 4DGS [48] | 13.42 | 0.49 | 0.56 |
| SoM 5 | T-NeRF | 15.60 | 0.55 | 0.55 |
| SoM 5 | HyperNeRF [34] | 15.99 | 0.59 | 0.51 |
| SoM 5 | DynIBaR [22] | 13.41 | 0.48 | 0.55 |
| SoM 5 | Gaussian Marbles | 16.03 | 0.54 | 0.58 |
| SoM 5 | SoM | 16.73 | 0.64 | 0.43 |
| SoM 5 | **GP-4DGS** | **16.92** | **0.66** | **0.41** |
| Challenging | Gaussian Marbles | 14.05 | 0.40 | 0.61 |
| Challenging | SoM | 14.56 | 0.46 | 0.53 |
| Challenging | **GP-4DGS** | **15.02** | **0.46** | **0.51** |

提升最显著的是 Challenging subset (reduced viewpoint overlap) — 验证 GP priors 对 sparse observation 区域的 propagation。

### 5.2 Future Motion Extrapolation (Table 2, PDF p.7)
| Method | Periodic 5f | Periodic 15f | Non-periodic 5f | Non-periodic 15f |
|--------|-------------|--------------|-----------------|------------------|
| Linear extrapolation | 11.55 | 8.11 | 15.02 | 11.92 |
| **GP-4DGS** | **17.62** | **16.65** | **15.27** | **13.22** |

PSNR ↑。Periodic +6.07 dB (5f), +8.54 dB (15f); Non-periodic +0.25 dB (5f), +1.30 dB (15f)。

### 5.3 Uncertainty Quantification (Table 3, PDF p.8)
AUSE-MSE ×10⁻² ↓:
| Method | Top 20 | Top 40 | All |
|--------|--------|--------|-----|
| Random | 9.76 | 9.30 | 10.98 |
| UA-4DGS [19] | 7.60 | 8.11 | 8.62 |
| **GP-4DGS** | **7.22** (−0.38) | **8.00** (−0.11) | **8.49** (−0.13) |

AUSE-MSE = reconstruction-error-vs-uncertainty sparsification gap，越小说明 uncertainty 与真实误差对齐越好。

### 5.4 Inducing Point Initialization (Table 4, PDF p.8)
ELBO↑ 平均: Random 1.10 / Velocity KNN 1.37 / Time-series (Chronos+KM) **1.53**。Per-scene 大多胜出 (paper-windmill 0.85/1.12/**1.28**, spin 0.92/1.15/**1.35**, teddy 1.45/1.52/**1.68** 等)，但 apple 场景 ours 1.19 < Velocity KNN 1.21，是少数反例。

### 5.5 GP-GS Optimization Ablation (Table B, PDF p.12, paper-windmill)
| Method | mPSNR↑ | mSSIM↑ | mLPIPS↓ |
|--------|--------|--------|---------|
| Baseline | 19.56 | 0.558 | 0.21 |
| w/o GP-GS optimization | 19.22 | 0.541 | 0.17 |
| w/ GP-GS optimization | **19.88** | **0.560** | 0.19 |

GP-GS 优化 vs 无优化在 paper-windmill 上 +0.66 mPSNR；脱离 joint optimization 反而比 baseline 差 (-0.34)。

### 5.6 Kernel Design Ablation (Table C, PDF p.12)
| Kernel | 5f extrap | 15f extrap | NVS m-PSNR |
|--------|-----------|------------|------------|
| w/o decomposition | 12.61 | 10.6 | 15.0 |
| RBF | 13.8 | 11.1 | 16.4 |
| Matérn | 13.1 | 10.4 | 17.1 |
| Spectral-mixture | 15.7 | 14.1 | 17.5 |
| **Ours (Matérn + periodic)** | **15.9** | **14.2** | 17.3 |

时空分解是 essential：去掉分解后 extrapolation 崩塌到 prior。

### 5.7 数据集
- **DyCheck** [Gao 2022, NeurIPS] — handheld monocular videos, rapid motion, 7 scenes (Apple, Block, Paper-windmill, Spin, Teddy, Space-out, Wheel) [PDF p.6 §5.1]。
- **DAVIS** [Pont-Tuset 2017] — 视频对象分割基准，用 Mega-SAM [Li 2025, CVPR] 估相机位姿，用于 extreme viewpoint shift 评测 [PDF p.6 §5.1, p.7 §5.2]。

### 5.8 评测指标
- 主指标: masked mPSNR↑ / mSSIM↑ / mLPIPS↓ (co-visible region only) [PDF p.6]。
- Uncertainty: AUSE-MSE [PDF p.8]。
- Extrapolation: PSNR on withheld last 5/15 frames [PDF p.7]。
- 训练细节: GP inputs/outputs 归一化，stochastic variational batch size 5000，GP-GS 优化 1000 inner iterations [PDF p.12 §D]。Initial LR 1e-2 (spatial+temporal inducing)，initial length scales ℓ_s=0.001 / ℓ_t=0.002，exp decay 0.95/epoch [PDF p.12 §D]。GPyTorch [Gardner 2018] 实现 [PDF p.6]。

## 6. 相关性评估

**用户评分: 4 分** (核心 4DGS 表示 / 渲染加速)。

**详细分析**:
1. **方法直接对接 4DGS 表示层**：把 deterministic deformation field (polynomial [23], HexPlane [48], MLP [51]) 升级为 probabilistic GP，是 4DGS 表示的范式级改进，理论上可 plug-in 到所有 4DGS baseline。
2. **核心增量三件套** (uncertainty / extrapolation / data-adaptive priors) 全部是 4DGS 此前没有的能力，独家贡献清晰。
3. **Scalability 认真做**：用 inducing points 把 O(N³) 降到 O(NM²+M³)，不是 toy 演示；Chronos + k-means 的 inducing point init 是工程细节上的周到设计 (Table 4 验证)。
4. **Challenging subset 上提升最大** (15.02 vs SoM 14.56)，说明 GP prior 在 occlusion 区域的 propagation 真的有效。
5. **对我们的相关性**:
   - **强相关 (A 派系)**: 与 MVFusion-GS / DeGauss / 4DGS / ST-4DGS 等核心 4DGS 工作同台，需要在 survey 4DGS 表示章节引用并讨论。
   - **强相关 (E 派系)**: 跨 ML 经典方法 (Gaussian Processes) 引入神经图形，是典型的"理论驱动 representation"思路，适合放 survey 跨界章节。
   - **弱相关 (B 派系)**: inducing point + cache 思路有训练加速价值，但非本论文主推。
   - **不相关 (D 派系)**: 论文无 mobile / edge 评测；GP inference (即使 O(M)) 在 mobile 上也难直接 port。但 variability 可借鉴 — uncertainty map 可作为 dynamic region detector 替代品。
6. **缺点**: 
   - 仅在 monocular DyCheck + DAVIS 评测，没在 multi-view Plenoptic Video / Neu3D / 自采数据上验证，泛化性待考。
   - GP inference 虽 O(M)，但 M 仍可能达数千 (M_spatial × M_time)，对 mobile 不友好。
   - λ_GP=0.1, N_GP=2000, τ_δ 调度等超参在 supplementary [PDF p.12 §D] 提及但未深入 sensitivity 分析。

## 7. 关键洞察

1. **从 "fixed deterministic prior" 到 "learned probabilistic prior" 是 4DGS 表示的范式跳跃**。现有 4DGS 用 polynomial / HexPlane / MLP 强制套用一个参数化形式，而 GP-4DGS 让 priors 从 well-observed primitives 自动学到，能 adapt 到 observation pattern。这是 4DGS 与传统 Bayesian ML 的首次严肃整合，比 MVFusion-GS 的 plug-in 残差模块更具结构性。

2. **Spatio-temporal composite kernel 是关键设计**。直接把 (x,y,z,t) 喂 isotropic kernel 会崩塌 — 因为空间几何 smooth、时间却周期性。把它们显式 factorize 后还能用 Chronos 做 semantic-aware inducing point init。Table C 验证 "w/o decomposition" 几乎全失败 [PDF Table C, p.12]。

3. **Uncertainty map 是一种 "free" 的副产品**。GP 后验方差天然提供，不需额外训练。Table 3 显示 GP-4DGS 在 "Top 20/40 高质量帧" 上的 AUSE 比 baseline 更优 — 这意味着 GP 不只在 hard region 有用，在 well-reconstructed region 也能 identify subtle residual errors。这种细粒度 uncertainty 可被用于 downstream task (e.g., active perception, dynamic-static decomposition)。

4. **GP-GS 联合优化是 "self-reinforcing loop"**。Stage 1 训 GP 在 confident data → Stage 2 用 GP 引导 GS 优化 → confident data 增长 → GP 训得更好。Table B (paper-windmill) 显示脱离这个 loop 反而变差 (-0.34 mPSNR)，验证了闭环的必要性。

5. **未来 motion 外推是免费副产品**。无需额外训练或架构改动就能 query GP at t > t_train (Eq. 15)。Periodic motion 上 +6~8 dB (Table 2)，non-periodic 也有 +0.25~1.30 dB。对 robotics / autonomous driving 的 predictive planning 有直接意义 (论文引用了 [28, 31, 35, 50, 52, 54] 等 robotics / driving 场景)。

## 8. 链接
- arxiv: https://arxiv.org/abs/2604.02915
- PDF (本地): .pdfs/2604.02915.pdf

## 9. 笔记出处
- 抽取者: subagent_A (PDF-only)
- 抽取日期: 2026-08-10
- 未二次核字段: 
  - 所有 PSNR / SSIM / LPIPS / AUSE-MSE / ELBO 数字均直接从 PDF Table 1-4 + Table A-C + Table D 抄录，未与 arxiv 公开版对比
  - venue "CVPR 2026 (main)" 来源于任务提示词；PDF 正文未显式声明
  - GitHub / 项目主页 / 代码许可：PDF 全文检索均无披露
  - 作者 affiliation 标注 ¹ECE + ²IPAI + ³Wisconsin 来源于 PDF p.1 header；邮箱地址也在 p.1
  - 所有公式 (Eq. 10-19) 与 kernel 设计的解释均直接来自 PDF §4.1-4.3，未做推算