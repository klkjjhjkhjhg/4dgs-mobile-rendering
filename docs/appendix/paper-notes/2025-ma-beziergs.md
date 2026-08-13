# BézierGS: Dynamic Urban Scene Reconstruction with Bézier Curve Gaussian Splatting

**作者**: Zipei Ma, Junzhe Jiang, Yurui Chen, Li Zhang
**机构**: School of Data Science, Fudan University; Shanghai Innovation Institute
**会议**: ICCV 2025
**arxiv-id**: 2506.22099
**本地 PDF**: .pdfs/iccv2025-Ma_BezierGS_Dynamic_Urban_Scene_Reconstruction_with_Bezier_Curve_Gaussian_Splatting_ICCV_2025_paper.pdf
**survey citekey**: (待 M2b extract_paper_summary.py 自动生成)
**GitHub**: https://github.com/fudan-zvg/BezierGS
**收录日期**: 2026-08-13
**收录来源**: P36 精读补全(subagent v2,交叉验证)

## 一句话
BézierGS 用 **learnable Bézier curves** 显式建模动态 Gaussian 的运动轨迹,无需精确的 3D bounding box 标注,可在 Waymo Open Dataset 与 nuPlan benchmark 上同时做动静态分解与 novel view synthesis,显著超越 PVG / Street Gaussians / OmniRe / DeformableGS。
vs v1: 一致。

## 关键数字(paper 实测)
*以下为 v2 重抽 PDF p.6-8 后的完整数字(补 v1 缺的 Table 1 baseline 行绝对值)*

**Table 1 — Comparison to SOTA on Waymo & nuPlan (Image Recon + Novel View)**

Waymo Image Reconstruction (PSNR↑ / SSIM↑ / LPIPS↓ / Dyn-PSNR↑):
- DeformableGS: 32.34 / 0.923 / 0.086 / 27.39
- HUGS: 31.58 / 0.904 / 0.094 / 25.78
- Street Gaussians: 32.18 / 0.918 / 0.090 / 28.64
- OmniRe: 32.32 / 0.923 / 0.084 / 28.36
- PVG: 32.61 / 0.901 / 0.159 / 29.32
- **BézierGS: 33.98 / 0.934 / 0.077 / 32.39** (best on PSNR,SSIM,LPIPS,Dyn-PSNR)

Waymo Novel View Synthesis:
- DeformableGS 29.52 / 0.889 / 0.100 / 24.66
- HUGS 29.34 / 0.865 / 0.110 / 23.84
- Street Gaussians 28.92 / 0.877 / 0.110 / 25.54
- OmniRe 29.41 / 0.884 / 0.101 / 25.85
- PVG 29.64 / 0.864 / 0.179 / 24.46
- **BézierGS 31.51 / 0.903 / 0.092 / 28.51**
- delta vs SOTA: **+1.87 dB PSNR / +0.014 SSIM / -8.00% LPIPS / +2.66 dB Dyn-PSNR**

nuPlan Image Reconstruction:
- DeformableGS 28.10 / 0.880 / 0.143 / 22.64
- HUGS 24.16 / 0.768 / 0.274 / 20.39
- Street Gaussians 26.05 / 0.813 / 0.180 / 22.19
- OmniRe 26.72 / 0.845 / 0.165 / 24.28
- PVG 29.08 / 0.869 / 0.170 / 21.94
- **BézierGS 30.74 / 0.896 / 0.122 / 27.13** (best on all 4)

nuPlan Novel View Synthesis:
- DeformableGS 26.20 / 0.824 / 0.159 / 21.37
- HUGS 23.77 / 0.744 / 0.280 / 20.15
- Street Gaussians 25.76 / 0.788 / 0.185 / 22.03
- OmniRe 26.01 / 0.819 / 0.173 / 23.90
- PVG 26.38 / 0.772 / 0.222 / 19.69
- **BézierGS 29.42 / 0.860 / 0.133 / 25.12** (best on all 4)
- delta vs SOTA: **+3.04 dB PSNR / +0.036 SSIM / -16.35% LPIPS / +1.22 dB Dyn-PSNR**
- vs v1: 全新数据(v1 只引用了 delta)。v2 给出所有 baseline 完整行。

**Table 2 — Ablation Study for novel view synthesis on Waymo**
- (a) w/o L_icc: 30.83 / 0.900 / 0.096 / 26.15
- (b) w/o L_dr: 30.99 / 0.891 / 0.099 / 28.07
- (c) w/o L_v: 31.40 / 0.901 / 0.094 / 28.29
- (d) w/o time-to-Bézier: 31.36 / 0.899 / 0.094 / 27.97
- (e) w/ MLP trajectory (DeformableGS-style): **29.58 / 0.898 / 0.087 / 24.78** (-1.93 dB vs full)
- (f) w/ sinusoidal trajectory (PVG-style): **29.65 / 0.877 / 0.099 / 26.27** (-1.86 dB vs full)
- **BézierGS (full): 31.51 / 0.903 / 0.092 / 28.51**
- vs v1: 完全一致。

**训练细节(从 §4.1 p.6 抽出)**
- 使用 cubic Bézier curve (n = 3)
- 单卡 NVIDIA RTX A6000, 30,000 iterations
- Loss coefficients: λ_r=0.2, λ_d=1.0, λ_sky_o=0.05, λ_icc=0.01, λ_dr=0.1, λ_v=1.0
- Waymo: 12 sequences (selected by Street Gaussians / PVG); nuPlan: 6 sequences (partitioned by NAVSIM)
- Frame rate 10 Hz; every 4th image as test, rest as training
- Dyn-PSNR: PSNR within ground-truth 3D bbox projected onto 2D image plane

## 重要 claim
- "First explicit dynamic trajectory representation using learnable Bézier curves that does not depend on the accuracy of manual object annotations" (PDF p.2 abstract)
- "Dynamic Gaussian trajectory: μ(τ,g) = δ(t) + γ(t,g), where t = f(τ,g) ∈ [0,1] with Bernstein basis controlled by n+1 control points" (PDF p.4 §3.2 Eq.7)
- "Bounding-box based methods [21,31,38,41,52] represent a special case of BézierGS — where offset is constant over time in object coordinate system; piecewise Bézier can represent long trajectories (higher-level alternative to PVG's periodic vibration)" (PDF p.5 §3.2)
- "Inter-curve consistency loss L_icc = ||δ(t) − (||p_0||+||p_n||)/2||_1 enforces trajectory consistency among Gaussians of same object, eliminating floaters" (PDF p.5 §3.3 Eq.10)
- "Dynamic rendering loss L_dr = L_rgb^dyn + L_o^dyn masks dynamic regions via projected bboxes + Grounded-SAM, supervising dynamic Gaussians' rendering separately" (PDF p.5 §3.3 Eq.13)
- "Velocity loss L_v = ||V_G^dyn · (1 − M^dyn)||_2 prevents dynamic Gaussians from drifting into static regions" (PDF p.6 §3.3 Eq.18)
- "Time-to-Bézier mapping t = f(τ,g) (per-object) handles non-uniform motion velocity, especially valuable for highly complex trajectories" (PDF p.4 §3.2 + p.8 §4.3)
- "Sky rendered as high-resolution cube map C = C_G + (1 − O_G) ⊙ C_sky, with sky-opacity loss L_O^sky = −Σ M_sky · log(1 − O_G) using Grounded-SAM mask" (PDF p.5 §3.2 + §3.3 Eq.8)
- "BézierGS can automatically correct pose errors of bounding boxes — this is why it outperforms box-based methods (Street Gaussians, OmniRe, HUGS) significantly on nuPlan where annotations are suboptimal" (PDF p.7-8 §4.2)
- "DeformableGS cannot separate dynamic objects; PVG fails to separate static/dynamic; Street Gaussians/OmniRe blur around dynamic elements — BézierGS achieves clean separation" (PDF p.7 §4.2 / Figure 4)
- vs v1: v2 补 5 个新 claim(velocity loss / sky / box-correction / comparison flaws / time-to-Bézier 详细作用)。

## 评价(survey 引用规范)
- **派系归属**: **B**(4DGS 加速 / 动静态分离 —— 显式动静态分解 + 自监督 trajectory,核心贡献是"无需 bounding box annotation 的动态 4DGS 表示",可直接归到动静态分离 + 4DGS 表示派系 B)
- vs v1: **维持派系 B**。**关键判断**:BézierGS 核心是 explicit dynamic trajectory + 动静态分离 → 派系 B(4DGS acceleration / 动静态分离)。虽然它的表示形式(Bézier curve trajectory)与"派系 A 4DGS 表示"有交叉,但论文主标题是 "Dynamic Urban Scene Reconstruction" 且实验聚焦"static + dynamic decomposition",本质是动静态分离问题,因此 v2 维持 v1 派系 B 判断(拒绝 v1 自身的"次要:派系 A"备注,统一为 B)。
- **相关性**: **高**(动态场景表示 + 动静态分离是本项目核心问题之一。BézierGS 的 explicit trajectory + time-to-Bézier mapping + inter-curve consistency 思路对本项目 4DGS 表示路线有直接启发;动静态分离也契合移动端可只渲染静态或动态子集的需求)
- vs v1: 一致。
- **方法简述**: 静态背景用普通 3DGS,动态前景把每个 Gaussian 的轨迹 μ(τ,g) 分解为 object-center γ(t,g) + offset δ(t),两者都用 learnable cubic Bézier curves (n=3) + per-object time-to-Bézier 映射 t=f(τ,g) 建模;并用 grouped inter-curve consistency loss L_icc + dynamic rendering loss L_dr + velocity loss L_v 三类约束确保一致性;天空用 cube map 渲染 + Grounded-SAM mask 监督。

## 关键段落 anchor
- §1 Introduction: p.1-2,问题动机(自动驾驶场景重建需要 large-scale + highly dynamic;现有方法依赖手动 object pose annotation;S3Gaussian 隐式 modeling + PVG 周期性 vibration 均有缺陷)
- §3 Method: p.3 起,3.1 preliminaries(3DGS + Bézier curve 定义 Eq.5-6)、3.2 Bézier curve Gaussian splatting(μ(τ,g) = δ(t) + γ(t,g), t = f(τ,g) Eq.7)、3.3 优化函数(L_icc Eq.10, L_dr Eq.13, L_v Eq.18, sky Eq.8)
- §3.2 Object center + offset decomposition: p.3-4,核心表示:每个 object g 有独立的 control points {p_i^g} 用于 center trajectory,Gaussian 还有 offset control points {p_i} 用于 offset trajectory
- §4.1 Experimental Setup: p.6,Waymo (12 seq) + nuPlan (6 seq) + baselines (DeformableGS / HUGS / Street Gaussians / OmniRe / PVG) + RTX A6000 30k iter + loss coefficients
- §4.2 SOTA Comparison: p.6-8,Table 1 完整 Waymo + nuPlan 主对比 (Image Recon + Novel View)
- §4.3 Ablation: p.8,Table 2 (6 ablations) + Bézier vs MLP vs sinusoidal 轨迹对比
- §5 Conclusion: p.8,BézierGS eliminates manual annotation dependency + enables automatic pose error correction
- Figure 1: p.1,dynamic vehicle 三个时间戳 + trajectory 可视化 + 动态实例移除 demo
- Figure 2: p.3,pipeline(object node + background node + sky node)
- Figure 3: p.4,(a) floaters 现象 (b) inter-curve consistency 修复
- Figure 4: p.7,Waymo qualitative comparison(Ours 比 DeformableGS / Street Gaussians / OmniRe / PVG 都更清晰,特别在动态区域)
- Figure 5: p.8,nuPlan qualitative comparison (Ours 自动校正 bbox pose errors)

---

*v2 交叉验证完成(基于 PDF p.4-8 重抽,补全 Table 1 完整 baseline 行 + 5 个新 claim);派系维持 B(动态 4DGS 表示 + 动静态分离是核心问题,非派系 A 通用 4DGS 表示)。*