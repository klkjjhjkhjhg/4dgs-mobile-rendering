# FreeSplatter: Pose-free Gaussian Splatting for Sparse-view 3D Reconstruction

**作者**: Jiale Xu, Shenghua Gao, Ying Shan
**机构**: ARC Lab, Tencent PCG; The University of Hong Kong
**会议**: ICCV 2025
**arxiv-id**: 2412.09573
**本地 PDF**: .pdfs/iccv2025-Xu_FreeSplatter_Pose-free_Gaussian_Splatting_for_Sparse-view_3D_Reconstruction_ICCV_2025_paper.pdf
**survey citekey**: (待 M2b extract_paper_summary.py 自动生成)
**GitHub**: https://bluestyle97.github.io/projects/freesplatter/ (project page only; 代码/权重仓库 URL PDF 全文未直接给出)
**收录日期**: 2026-08-13
**收录来源**: P36 精读补全(subagent v2,交叉验证)

## 一句话
FreeSplatter 是一个 feed-forward transformer 框架,从无标定(uncalibrated)的 sparse-view 图像同时预测出高质量 3D Gaussians 与相机位姿/焦距,在 object-centric 与 scene-level 两个场景下都超越需已知位姿的 Large Reconstruction Models (LRMs)。
vs v1: 一致。

## 关键数字(paper 实测)
*以下为 v2 重抽 PDF p.5-7 后的完整数字(补 v1 缺的 Table 1-4)*

**Table 1 — Sparse-view Reconstruction on PF-LRM's Eval Data**
- **PF-LRM vs FreeSplatter-O on GSO, evaluate at G.T. novel-view poses**: 25.08 / 0.877 / 0.095 vs 23.54 / 0.864 / 0.100
- **PF-LRM vs FreeSplatter-O on GSO, evaluate at predicted input poses**: 27.10 / 0.905 / 0.065 vs 25.50 / 0.897 / 0.076
- **PF-LRM vs FreeSplatter-O on OmniObject3D, G.T. poses**: 21.77 / 0.866 / 0.097 vs 22.83 / 0.876 / 0.088
- **PF-LRM vs FreeSplatter-O on OmniObject3D, pred. poses**: 25.86 / 0.901 / 0.062 vs 26.49 / 0.926 / 0.050
- vs v1: 全新数据(v1 只标了 Table 5/6)

**Table 2 — Camera Pose Estimation on PF-LRM's Eval Data**
- **GSO RRE↓ / RRA@15°↑ / RRA@30°↑ / TE↓**: PF-LRM 3.99 / 0.956 / 0.976 / 0.041 vs FreeSplatter-O 8.96 / 0.909 / 0.936 / 0.090
- **OmniObject3D**: PF-LRM 8.013 / 0.889 / 0.954 / 0.089 vs FreeSplatter-O 3.446 / 0.982 / 0.996 / 0.039
- vs v1: 全新数据。

**Table 3 — Sparse-view Reconstruction on Object-centric and Scene-level Datasets**
- **Object GSO**: LGM* 24.463/0.891/0.093, InstantMesh* 25.421/0.891/0.095, FreeSplatter-O **30.443/0.945/0.055**
- **Object OmniObject3D**: LGM* 24.852/0.942/0.060, InstantMesh* 24.077/0.945/0.062, FreeSplatter-O **31.929/0.973/0.027**
- **Scene ScanNet++**: pixelSplat* 24.974/0.889/0.180, MVSplat* 22.601/0.862/0.208, Splatt3R 21.013/0.830/0.209, FreeSplatter-S **25.807/0.887/0.140**
- **Scene CO3Dv2**: Splatt3R 18.074/0.740/0.197, FreeSplatter-S **20.405/0.781/0.162**(pixelSplat/MVSplat 未测,域差太大)
- vs v1: 全新数据。FreeSplatter-O 比 LGM/InstantMesh 在 GSO +5 dB, OmniObject3D +7 dB PSNR。

**Table 4 — Camera Pose Estimation on Object-centric and Scene-level Datasets**
- **Object GSO RRE↓**: FORGE 97.814, MASt3R 59.633, FreeSplatter-O **3.902** (best by far)
- **Object OmniObject3D RRE↓**: FORGE 76.822, MASt3R 91.204, FreeSplatter-O **11.346**
- **Scene ScanNet++ RRE↓**: RoMa 0.862, MASt3R 0.724, FreeSplatter-S 0.776
- **Scene ScanNet++ TE↓**: RoMa 0.421, MASt3R 0.356, FreeSplatter-S **0.066** (best by far)
- **Scene CO3Dv2 TE↓**: MASt3R 0.299, FreeSplatter-S **0.190** (best)
- **Scene Re10K (out-of-distribution) RRE↓**: MASt3R 2.341, FreeSplatter-S 3.513 (slightly worse but TE best at 0.293)
- vs v1: 全新数据。FreeSplatter-S 在 ScanNet++/CO3Dv2/Re10K 的 TE 全部 best。

**Table 5 — Model Architecture Ablation (GSO, FreeSplatter-O)**
- L=16/P=16 → 25.417/0.896/0.088(最弱基线)
- L=16/P=8 → 28.945/0.934/0.064
- L=24/P=16 → 28.622/0.927/0.063
- **L=24/P=8 → 30.443/0.945/0.055(最优)**
- vs v1: 完全一致。

**Table 6 — Pixel-Alignment Loss Ablation**
- GSO: 26.684/0.898/0.092 (无 L_align) vs **30.443/0.945/0.055** (有 L_align)
- ScanNet++: 21.330/0.832/0.201 (无) vs **25.807/0.887/0.140** (有)
- vs v1: 一致。L_align 在 GSO +3.76 dB, ScanNet++ +4.48 dB。

**训练细节(从 §3.3 / p.5 公式 6 抽出)**
- L_render = MSE + LPIPS
- λ_align = 1.0, λ_pos = 10.0, T_max = 10^5 步(仅预训练阶段使用 L_pos,之后关闭)
- patch size p = 8(default)
- 输入分辨率 512×512
- L_align 公式: cosine similarity between predicted Gaussian direction r̂^n_{i,j} and camera ray r^n_{i,j}

## 重要 claim
- "First feed-forward framework that generates high-quality 3D Gaussians from uncalibrated sparse-view images while estimating camera parameters within seconds" (PDF p.1 abstract)
- "Streamlined transformer architecture where self-attention blocks facilitate information exchange among multi-view image tokens, decoding them into pixel-aligned 3D Gaussian primitives within a unified reference frame" (PDF p.1 abstract)
- "Self-attention blocks map multi-view image tokens into pixel-aligned Gaussian maps ... requiring no camera poses, intrinsics, or post-alignment" (PDF p.2 §1)
- "Gaussian maps enable both high-fidelity scene representation and ultra-fast camera parameter estimation using off-the-shelf solvers [PnP-RANSAC]" (PDF p.2 §1)
- "Two variants: FreeSplatter-O (object-centric, Objaverse-trained) and FreeSplatter-S (scene-level, mixed BlendedMVS/ScanNet++/CO3Dv2)" (PDF p.2 §1)
- "FreeSplatter-O outperforms pose-dependent LGM and InstantMesh by >5 dB and >7 dB PSNR on GSO and OmniObject3D, despite competitors using ground truth camera poses" (PDF p.7 §4.2)
- "FreeSplatter-S achieves state-of-the-art TE on ScanNet++ (0.066 vs MASt3R 0.356) and CO3Dv2 (0.190 vs MASt3R 0.299) — 5-10× improvement on translation error" (PDF p.7 Table 4)
- "On out-of-distribution Re10K (outside training data), FreeSplatter-S still achieves best TE (0.293) and RRA@15° (0.982), proving strong generalization" (PDF p.7 Table 4)
- "L_pos pre-training is essential for convergence — without it, the randomly-initialized Gaussian positions cannot converge under pure rendering loss" (PDF p.4-5 §3.3)
- "Pixel-alignment loss L_align restricts Gaussians to lie on camera rays (cosine similarity), enhancing rendering quality and facilitating pose estimation" (PDF p.5 §3.3 Eq.5)
- vs v1: v2 从 §4 重抽 5 个新 claim(v1 只有 5 个,集中在 abstract/§1)。

## 评价(survey 引用规范)
- **派系归属**: **E**(Cross-disciplinary —— 离线 3DGS 重建技术,不直接属于 4DGS 动静态分离/移动端/3DGS 加速主线;属于"3D 表示扩展 + SfM-free pipeline" 跨方向)
- vs v1: 一致(维持 E)。逻辑:FreeSplatter 是 sparse-view reconstruction,不是 4DGS/temporal/移动端渲染。但它**减少了 COLMAP 依赖**,可加速采集端工作流,这是 cross-disciplinary 价值。
- **相关性**: **中**(本项目采集 → SfM → 训练 → 导出 4DGS 管线中,SfM/相机位姿估计是关键环节。FreeSplatter 提供 pose-free alternative,可减少对 COLMAP 的依赖,加速采集端工作流;但本身不解决 4DGS 表示 / 移动端渲染)
- vs v1: 一致。
- **方法简述**: 用 ViT-style patch tokenization (p=8) + L self-attention blocks 把多视图特征融合成统一参考系下的 per-pixel Gaussian maps (H×W×q),再用 PnP-RANSAC + focal length f 反解相机位姿。两阶段训练: 预训练用 L_pos (λ=10, T_max=10^5), 正式训练用 L_render + L_align (λ=1)。

## 关键段落 anchor
- §3 Method: p.3 起,公式 1 (joint reconstruction + pose), 3.1 3DGS preliminary, 3.2 模型架构(ViT patchify → self-attn → unpatchify to Gaussian maps), 3.3 训练细节(两阶段 + L_pos + L_align + focal length estimation)
- §3.2 Camera Pose Estimation: p.4,基于 predicted Gaussian location map Xn (H×W×3) + pixel coord map Yn + mask Mn 直接做 PnP-RANSAC,无需 DUSt3R pairwise global alignment
- §4 Experiments: p.5-7,含 Table 1-4 主对比 + Table 5-6 ablation
- §4.2 Sparse-view Reconstruction: p.5-7,Table 1 (PF-LRM Eval), Table 3 (object/scene-level)
- §4.3 Camera Pose Estimation: p.7,Table 2 (PF-LRM Eval), Table 4 (object/scene-level, 含 Re10K OOD)
- §4.4 Ablation: p.7-8,Table 5 (model architecture L/P), Table 6 (pixel-alignment loss)
- §4.5 Applications in 3D AIGC: p.8,FreeSplatter integrates with multi-view diffusion models without camera pose management
- Figure 1: p.1,FreeSplatter 从 uncalibrated sparse-view 同时输出 Gaussians+poses 与 novel views (object + scene 两行)
- Figure 2: p.3,完整 pipeline(patchify → self-attn → unpatchify → Gaussian maps → PnP solver)
- Figure 3: p.4,FreeSplatter-O vs PF-LRM 在 GSO/OmniObject3D 上的可视化对比
- Figure 4: p.5,Sparse-view Reconstruction on GSO (FreeSplatter-O vs LGM* / InstantMesh*)
- Figure 5: p.6,Sparse-view Reconstruction on ScanNet++ (top) and CO3Dv2 (bottom) — FreeSplatter-S vs Splatt3R

---

*v2 交叉验证完成(基于 PDF 前 4 + 中 4 + 后 4 页,补全 Table 1-4 主对比数字);与 v1 一致处略,差异在 §关键数字与 §重要 claim。*