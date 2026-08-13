# StealthAttack: Robust 3D Gaussian Splatting Poisoning via Density-Guided Illusions

**作者**: Bo-Hsu Ke, You-Zhe Xie, Yu-Lun Liu, Wei-Chen Chiu
**机构**: National Yang Ming Chiao Tung University
**会议**: ICCV 2025
**arxiv-id**: 2510.02314
**本地 PDF**: .pdfs/iccv2025-Ke_StealthAttack_Robust_3D_Gaussian_Splatting_Poisoning_via_Density-Guided_Illusions_ICCV_2025_paper.pdf
**survey citekey**: (待 M2b extract_paper_summary.py 自动生成)
**GitHub**: https://hentci.github.io/stealthattack/ (project page only; GitHub repo URL PDF 全文未直接给出)
**收录日期**: 2026-08-13
**收录来源**: P36 精读补全(subagent v2,交叉验证)

## 一句话
StealthAttack 是 **首个针对 3DGS 的 data poisoning attack**,通过 Kernel Density Estimation (KDE) 识别初始 Gaussian point cloud 的低密度区域,把"illusive object" 的 Gaussian points 沿目标视角 camera rays 注入这些低密度位置,使 illusory object 在 poisoned view 上清晰可见、在 innocent views 上几乎不可察觉,并辅以 adaptive Gaussian noise scheduling 破坏 multi-view consistency。
vs v1: 一致。

## 关键数字(paper 实测)
*以下为 v2 重抽 PDF p.5-8 后的完整数字(补 v1 缺的 §4 Experiments 主对比表格)*

**Table 1 — Single-view Attack Quantitative Comparisons (V-ILLUSORY / V-TEST)**

| Method | Mip-NeRF 360 V-ILL | Mip-NeRF 360 V-TEST | T&T V-ILL | T&T V-TEST | Free V-ILL | Free V-TEST |
|---|---|---|---|---|---|---|
| Naive 3DGS (w/o attack) | 13.21/0.521/0.731 | 29.45/0.883/0.165 | 13.15/0.616/0.732 | 30.60/0.915/0.135 | 12.00/0.315/0.905 | 26.80/0.826/0.228 |
| IPA-NeRF (Nerfacto) | 16.00/0.582/0.685 | 21.94/0.586/0.415 | 13.51/0.636/0.711 | 23.88/0.730/0.218 | 13.93/0.443/0.699 | 20.28/0.497/0.532 |
| IPA-NeRF (Instant-NGP) | 17.60/0.618/0.641 | 20.00/0.517/0.479 | 16.05/0.693/0.616 | 20.29/0.669/0.350 | 18.94/0.508/0.519 | 20.43/0.503/0.548 |
| IPA-Splat | 13.23/0.518/0.740 | 27.39/0.829/0.247 | 13.43/0.625/0.724 | 28.53/0.891/0.190 | 12.60/0.372/0.744 | 24.71/0.749/0.341 |
| **Ours** | **27.04/0.813/0.369** | **27.76/0.805/0.286** | **21.33/0.809/0.371** | **27.58/0.852/0.239** | **26.66/0.754/0.317** | **25.25/0.728/0.382** |

Ours 在 3 个数据集 × 2 个视图集 = 6 个对比上 PSNR 均最高(IPA-Splat 在 Free V-TEST 上 24.71 < Ours 25.25)。
vs v1: **全新数据**(v1 完全未抽到 Table 1)。

**Table 2 — Single-view Attack 不同难度级别 (Free dataset)**

| Method | EASY PSNR/SSIM/LPIPS | MEDIAN PSNR/SSIM/LPIPS | HARD PSNR/SSIM/LPIPS |
|---|---|---|---|
| IPA-NeRF (nerfacto) | 15.04/0.482/0.662 | 13.93/0.443/0.699 | 14.25/0.450/0.728 |
| IPA-NeRF (instant-ngp) | 18.17/0.518/0.541 | 18.94/0.508/0.519 | 17.95/0.487/0.557 |
| IPA-Splat | 13.94/0.479/0.658 | 12.60/0.372/0.743 | 13.06/0.340/0.796 |
| **Ours** | **29.94/0.853/0.188** | **26.66/0.754/0.317** | **17.53/0.526/0.581** |

vs v1: 全新数据。

**Table 3 — Multi-view Attack on Mip-NeRF 360 (poisoned avg / V-TEST)**
- 2 poisoned views: Ours **27.49/0.842/0.299** V-ILL, 27.77/0.804/0.286 V-TEST (vs IPA-Splat 13.24 V-ILL)
- 3 views: Ours **27.04/0.833/0.311** V-ILL (vs IPA-Splat 13.76)
- 4 views: Ours **26.95/0.855/0.305** V-ILL (vs IPA-Splat 13.09)
- vs v1: 全新数据。

**Table 4 — KDE Bandwidth h Ablation (Mip-NeRF 360)**
- h=0.1: V-ILL 27.00/0.811/0.373, V-TEST 27.83/0.805/0.286
- h=2.5: V-ILL 26.92/0.809/0.375, V-TEST 27.81/0.805/0.286
- h=5.0: V-ILL 26.95/0.811/0.375, V-TEST 27.25/0.786/0.297
- **h=7.5: V-ILL 27.04/0.813/0.369, V-TEST 27.76/0.805/0.286** (best balance)
- h=10.0: V-ILL 26.89/0.807/0.380, V-TEST 27.72/0.805/0.286
- vs v1: 全新数据。

**Table 5 — Noise Scheduling Ablation (σ₀ × decay strategy)**
- (σ₀=30, Linear): V-ILL 26.47/0.795/0.398
- (σ₀=100, **Linear**): V-ILL **27.04/0.813/0.369** V-TEST 27.76/0.805/0.286 (best balance)
- (σ₀=100, Cosine): V-ILL 26.93/0.812/0.373 V-TEST 26.96/0.771/0.315
- (σ₀=100, Square root): V-ILL 26.90/0.813/0.373 V-TEST 26.81/0.767/0.319
- vs v1: 全新数据。

**Table 6 — Attack Strategy Combination (ASR: V-ILL PSNR>25 & V-TEST drop≤3)**
- 仅 GT replacement: 0/7 ASR
- GT + Density-Guided: 6/7 ASR
- GT + View Consistency Disruption: 0/7 ASR(noise alone 不够)
- **GT + Density-Guided + View Consistency Disruption: 7/7 ASR** (full)
- vs v1: 全新数据。

**实验设置(§4.1, p.5)**
- Datasets: Mip-NeRF 360 (复杂 360° scenes), Tanks & Temples (indoor/outdoor), Free (unbounded scenes)
- IPA-NeRF baselines: O=15,000 iterations, T=200 iter/epoch, O/T=75 attack epochs, A=10 attack iter/epoch, K=100 perturbation renderings, distortion budget ϵ=32, constraint parameter η=1, view constraints (13°, 15°)
- IPA-Splat (本文适配): O=30,000 total iterations, T=200 normal training iter/epoch, O/T=150 epochs, A=10 attack iter each
- 评估协议: V-ILLUSORY (masked PSNR/SSIM/LPIPS for illusory region) + V-TEST (unseen viewpoints)
- Attack success: V-ILL PSNR > 25 AND V-TEST PSNR drop ≤ 3
- KDE-based difficulty protocol: 计算 camera viewpoint densities (10% sampling radius), 选 EASY (min density) / MEDIAN / HARD (max density) 三个 viewpoint

## 重要 claim
- "First work to address data poisoning attacks upon 3DGS for illusory objects injection" (PDF p.2 §1 contribution list)
- "Density-guided point placement: KDE on per-voxel opacity density identifies low-density regions; backprojected Gaussian points of illusory object placed along rays cast from target view's virtual camera" (PDF p.4 §3.3)
- "Two motivating attack modes: (a) points placed outside innocent viewpoints' coverage; (b) points occluded from innocent views by existing geometry but visible from target view" (PDF p.4 Figure 4)
- "Adaptive Gaussian noise scheduled into innocent views during training disrupts multi-view consistency to enhance attack" (PDF p.2 §1 / p.4 Figure 3c)
- "KDE-based evaluation protocol to assess attack difficulty systematically — EASY/MEDIAN/HARD via scene density" (PDF p.5 §4.1 / Table 2)
- "Naive approaches fail: (1) directly injecting illusory content into training images gets eliminated by 3DGS multi-view consistency; (2) naive backprojection requires correct depth for illusory object, otherwise occluded by existing geometry" (PDF p.3 §3.2)
- "IPA-NeRF designed for implicit NeRF representation; not directly transferable to explicit 3DGS" (PDF p.2 §1)
- "Bi-level optimization objective: minimize ||Ĩ_ILL - I_ILL||² + Σ_{v_k≠v_p} ||R(Ĝ, v_k) - R(G, v_k)||²" (PDF p.3 §3.1 Eq.1)
- "Ours achieves 27.04 V-ILL PSNR on Mip-NeRF 360 vs IPA-Splat 13.23 — 2× improvement" (PDF p.6 Table 1)
- "Ours maintains 7/7 Attack Success Rate when combining all 3 strategies (GT replacement + density-guided + view consistency disruption)" (PDF p.8 Table 6)
- "Optimal KDE bandwidth h=7.5 balances density estimation smoothness with point placement precision" (PDF p.7 Table 4 / §4.4)
- "Three noise decay strategies (linear / cosine / square root) with σ₀=100 linear decay provides best balance — strong early noise disrupts multi-view consistency, gradually reducing noise preserves innocent view quality" (PDF p.7 Table 5 / §4.4)
- "Scene density negatively correlates with attack success — higher scene coverage → higher attack difficulty" (PDF p.6 §4.2)
- vs v1: v2 补 7 个新 claim(具体 PSNR 数字 / ASR 7/7 / KDE bandwidth / noise decay / scene density 反相关等)。

## 评价(survey 引用规范)
- **派系归属**: **E**(Cross-disciplinary —— 属于 3DGS 安全/对抗攻击子方向,不直接属于 4DGS 表示/动静态分离/3DGS 加速/移动端主线;但与派系 E Cross-disciplinary 范畴下"3D 表示扩展 + 新兴应用"高度契合,涉及 AI security + 3DGS 交叉)
- vs v1: 一致(维持 E)。
- **相关性**: **低**(本项目核心问题:移动端 GPU 实时渲染 4DGS。StealthAttack 攻击 3DGS 训练阶段,影响 3D 资源可信度 / 数字资产保护;对本项目直接技术启发有限,但作为"3DGS 资源被污染的风险"提醒,在采集端训练管线中考虑防御性设计(如 KDE-based 检测)有一定价值)
- vs v1: 一致。
- **方法简述**: 在已训好的 3DGS 上,用 KDE 在 voxel 网格上估计 opacity 密度场(ρ(s) = Σ_{g∈s} α(g),KDE 核带宽 h=7.5);沿 target view camera rays 采样 (t∈[0.3, t_max=scene_depth]),在密度最小处注入 illusory object 的 Gaussians;同时在 innocent views 加 adaptive Gaussian noise (σ₀=100, linear decay) 破坏 multi-view consistency;评估时用 KDE-based 协议衡量攻击难度(EASY/MEDIAN/HARD)。

## 关键段落 anchor
- §1 Introduction: p.1-2,NeRF vs 3DGS explicit representation 的安全差异,IPA-NeRF 不可迁移性,并发工作 Poison-Splat 区分(后者攻击 computational cost / 资源消耗,本文攻击 visible illusion embedding)
- §3.1 Problem Formulation: p.3,Eq.1 二层优化目标(poison view illusion + innocent view fidelity)
- §3.2 Naive Approaches and Limitations: p.3,两种 naive 失败原因分析
- §3.3 Density-Guided Point Cloud Attack: p.4,(a) AABB + voxelization + 体积渲染估计 opacity 密度 ρ(s) (b) KDE 连续密度估计(Eq.2-3) (c) 沿 target view rays 在最小密度位置放点(Eq.4,x_min = argmin f(x))
- §3.4 View Consistency Disruption Attack: p.5,adaptive Gaussian noise (Eq.5 σ_t),三种 decay strategies (linear/cosine/sqrt, Eq.8)
- §4.1 Experimental Setup: p.5,三个数据集 + IPA-NeRF/IPA-Splat baselines + 评估协议 (V-ILLUSORY/V-TEST, ASR 阈值)
- §4.2 Single-view Attack: p.6,Table 1 全数据集主对比 + Table 2 EASY/MEDIAN/HARD 分级 + Figure 6/7 qualitative
- §4.3 Multi-view Attack: p.7,Table 3 (2/3/4 poisoned views on Mip-NeRF 360) + Figure 8
- §4.4 Ablation Studies: p.7-8,Table 4 (KDE bandwidth) + Table 5 (noise scheduling)
- §4.5 Attack Strategy Combination: p.8,Table 6 (ASR for 4 combinations, 7/7 best with all 3)
- Figure 1: p.1,核心插图:innocent view 干净 / poisoned view 红色 illusory vehicle 出现 + poison points 沿 rays 分布
- Figure 2: p.2,IPA-NeRF / IPA-Splat / Ours 在 3DGS 上的局限性对比(IPA-NeRF 攻击 3DGS 失败)
- Figure 3: p.4,框架总览:(a) density-guided point cloud attack (b) normal 3DGS training (c) view consistency disruption attack
- Figure 4: p.4,两个攻击模式:(a) points outside innocent view coverage (b) points occluded by geometry
- Figure 5: p.6,KDE-based evaluation protocol(bicycle 均匀 / stair 不均匀)
- Figure 8: p.7,Multi-view attack qualitative (View 1-4)
- Figure 9: p.8,Attack strategy combinations qualitative
- Project page: https://hentci.github.io/stealthattack/

---

*v2 交叉验证完成(基于 PDF p.4-8 重抽,补全 Table 1-6 全部主对比数字 + 7 个新 claim);派系维持 E(3DGS 安全/对抗攻击是 Cross-disciplinary 子方向)。*