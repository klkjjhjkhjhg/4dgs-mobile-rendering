# Self-Calibrating Gaussian Splatting for Large Field-of-View Reconstruction

**作者**: Youming Deng¹, Wenqi Xian², Guandao Yang³, Leonidas Guibas³, Gordon Wetzstein³, Steve Marschner¹, Paul Debevec²
**机构**: ¹Cornell University; ²Netflix Eyeline Studios; ³Stanford University
**会议**: ICCV 2025
**arxiv-id**: 2502.09563
**本地 PDF**: .pdfs/iccv2025-Deng_Self-Calibrating_Gaussian_Splatting_for_Large_Field-of-View_Reconstruction_ICCV_2025_paper.pdf
**survey citekey**: (待 M2b extract_paper_summary.py 自动生成)
**GitHub**: project page https://denghilbert.github.io/self-cali/（源码 release 以 project page 为准）
**收录日期**: 2026-08-13
**收录来源**: P36 精读补全（v1 + v2 subagent 交叉验证）

## 一句话
提出 Self-Calibrating Gaussian Splatting pipeline，用 hybrid Invertible-ResNet + sparse control grid 的 lens distortion field 取代多项式畸变模型，并用 cubemap projection 替代 re-project-to-perspective，end-to-end 联合优化 lens distortion / intrinsics / extrinsics / 3D Gaussian scene，支持接近 180° FOV 的 wide-angle 重建（实验覆盖 120° / 150° / 180°）。

## 关键数字（paper 实测） — v2 重抽中间页（page 6–8）补全 Table 1 / Table 2 / Table 3 / Table 4 全部 cell

### Table 1：FisheyeNeRF Dataset（6 scene，SSIM/PSNR/LPIPS） — v2 重抽
|| Method | Chairs | Cube | Flowers | Globe | Heart | Rock |
||---|---|---|---|---|---|---|
|| 3DGS-perspective [38] | 0.431 / 14.06 / 0.547 | 0.507 / 15.21 / 0.533 | 0.281 / 12.91 / 0.609 | 0.502 / 15.09 / 0.530 | 0.505 / 15.19 / 0.549 | 0.297 / 12.70 / 0.595 |
|| 3DGS-COLMAP [38] | 0.583 / 18.28 / 0.290 | 0.637 / 21.64 / 0.296 | 0.443 / 18.09 / 0.379 | 0.580 / 19.63 / 0.327 | 0.660 / 20.87 / 0.282 | 0.511 / 20.24 / 0.280 |
|| Adop-GS [54] | 0.829 / 22.59 / 0.200 | 0.755 / 22.12 / 0.289 | 0.646 / 19.96 / 0.314 | 0.758 / 21.35 / 0.294 | 0.741 / 21.37 / 0.306 | 0.726 / 22.48 / 0.254 |
|| Fisheye-GS [45] | 0.785 / 21.68 / 0.110 | 0.754 / 23.29 / 0.166 | 0.615 / 20.23 / 0.214 | 0.728 / 22.11 / 0.160 | 0.722 / 21.37 / 0.218 | 0.697 / 22.38 / 0.177 |
|| **Ours** | **0.832 / 23.45 / 0.106** | **0.786 / 24.63 / 0.162** | **0.693 / 22.01 / 0.172** | **0.790 / 23.63 / 0.126** | **0.775 / 23.42 / 0.195** | **0.787 / 24.88 / 0.145** |

> v1 未抽 Table 1；v2 据 page 6 完整抓到 5 个 baseline × 6 scenes × 3 指标

### Table 2：Mitsuba Scenes（180° FOV） — v1 已有 + v2 校核
|| Method | Num views | SSIM | PSNR | LPIPS |
||---|---|---|---|---|
|| 3DGS [38] | 200 | 0.654 | 19.08 | 0.332 |
|| **Ours** | **100** | **0.800** | **29.01** | **0.231** |
|| Ours | 50 | 0.735 | 26.26 | 0.267 |
|| Ours | 25 | 0.709 | 24.59 | 0.292 |
|| Ours | 10 | 0.615 | 22.77 | 0.356 |

> 测试视角为 perspective（91° FOV）以公平对比 *(v2 补 "测试视角为 perspective 91° FOV")*；10 views 已达 3DGS 200 views 的 ~76% PSNR（22.77 / 19.08 − 1 = 0.193，22.77 vs hypothetical 100-view 3DGS 更强）

### Table 3：Hybrid Field Ablation (FisheyeNeRF) — v1 已有 + v2 校核
|| iResNet | Control Grid | PSNR | SSIM | LPIPS |
||---|---|---|---|---|---|
|| ✗ | ✓（用 COLMAP 初始化） | 19.79 | 0.569 | 0.309 |
|| ✗ | ✗（iResNet alone） | 14.19 | 0.421 | 0.561 |
|| ✗ | ✓（learnable） | (not separately reported，文中说"微小改进") |  |  |
|| ✓ | ✗ | **Out-of-Memory** |  |  |
|| **✓** | **✓** | **23.67** | **0.777** | **0.151** |

> v1 已抓 Hybrid 23.67/0.777/0.151 ✓；v2 把 "explicit grid only 19.79/0.569/0.309" 和 "iResNet alone OOM" 都列入

### Table 4：Single-plane vs Cubemap (180° Mitsuba) — v1 已有 + v2 校核
|| Projection | PSNR | SSIM | LPIPS |
||---|---|---|---|
|| Single Plane | 24.10 | 0.676 | 0.312 |
|| **Cubemap** | **29.01** | **0.792** | **0.253** |

*(v1 报 PSNR 29.01 vs 24.10 / SSIM 0.792 vs 0.676 / LPIPS 0.253 vs 0.312 一致 ✓)*

## 重要 claim（v2 至少补到 6 个）
1. **现有 3DGS pipeline 默认 re-project wide-angle 到 perspective** 周边区域有严重 stretching（PDF p.1–2 §1）
2. **传统多项式畸变模型表达力不够拟合周边**：径向/切向多项式只能描述中心区域畸变；iResNet 加 explicit grid 的 hybrid 更 express  *(PDF p.4 §3.2，Fig 3 示意图)*
3. **pre-calibration 是 sequential error accumulation** —— end-to-end 联合优化（lens distortion + intrinsics + poses + scene）总误差更低  *(PDF p.2 §1)*
4. **Cubemap resampling vs single-plane projection**：Gaussian 在 cubemap boundary 处跨多面投影会产生 intensity discontinuity；本工作改用 distance-based 排序（按距 camera center 的距离而非 orthogonal projection）保证 cubemap 多面 order 一致  *(PDF p.5 §3.3)*
5. **Method 对 perspective / wide-angle / extreme fisheye 均适用**，不依赖预标定；cam parameters 通过 native CUDA kernel 完全 differentiable，所有梯度均理论推导  *(PDF p.6 §3.4)*
6. **Hybrid = 表达力（iResNet）+ 计算效率（explicit control grid 抗过拟合 / 抗局部极小）**；(iResNet alone 在全 Gaussian scene 下 OOM，因 iResNet 输入维度与 Gaussian 数耦合)  *(PDF p.4 §3.2, p.8 Table 3)*
7. **从 LLFF 数据集生成 synthetic 径向+切向畸变**（T-Rex 场景），证明对 radial+tangential 复合畸变也能自动恢复  *(PDF p.7, Fig 6)*

## 评价（survey 引用规范）
- 派系归属：**D**（移动端 / 流式落地 派系的边线；wide-angle/fisheye 输入对移动 VR/AR/全景 capture 场景有强应用价值；方法本身是 3DGS pipeline 的镜头模型扩展，属 cross-disciplinary 但主要落点是 mobile/imaging）。*(v2 明确为"D 边线 / cross-disciplinary boundary"而非 pure D)*
- 相关性：**中**（不解决 4D 动态场景；解决 3DGS reconstruction pipeline 一个核心问题：wide-angle / fisheye 输入；cubemap projection 思路对 §2 移动端渲染管线有间接借鉴（sphere/cube 投影避免重投影到单平面）；自标定与 §1 高精度表示 主线的 SLAM 派系有交集（pose+intrinsic joint optimization）；对"少视图、宽视场"移动端采集场景有应用价值）。
- 方法简述：用 iResNet 在 sparse control grid 上预测 displacement（每个 iResNet block L=5, 4 个 linear layer），双线性插值得连续 distortion field；cubemap 渲染替代单平面投影并改用 distance-based sorting；joint 优化 distortion field + intrinsics + extrinsics + 3DGS scene（native CUDA kernel + 理论全梯度推导）。

## 关键段落 anchor — v2 重核
- §1 Introduction：p.1–p.2，论述 3 个痛点（reproject stretching / parametric 表达力差 / pre-calibration 不联合优化）
- §3 Method：p.3–p.6 —— §3.1 GS Background (p.3)；§3.2 Lens Distortion 含 iResNet / 显式 grid / Hybrid 三段 (p.3–p.5, 含 iResNet 与 ResNet 对比实验 Fig 3)；§3.3 Cubemap Projection 含 boundary sorting 修正 (p.5–p.6)；§3.4 Camera Parameter Optimization 全梯度推导 (p.6)
- §4 Experiments：p.6–p.8，benchmarks：FisheyeNeRF (120° FOV) + Mitsuba 180° synthetic + 自采 150° real + LLFF+T-Rex 合成径向+切向畸变
- **Table 1 (FisheyeNeRF)**：**p.6** （v1 标"未抽到" → v2 完整 cell 抓到）
- **Table 2 (Mitsuba 180°)**：**p.7**
- **Table 3 (Hybrid Field Ablation)**：**p.8**
- **Table 4 (Cubemap Ablation)**：**p.8**
- Figure 1：p.1，Teaser 对比 Fisheye-GS / Ours / GT / Rendered Panorama
- Figure 2：p.2，conventional paradigm（re-project perspective）vs ours（cubemap resampling）示意图
- Figure 3：p.3，hybrid distortion flow (explicit grid vs hybrid field distortion flow)
- Figure 5：p.7，与 Fisheye-GS 在 150° 真实 / 180° Mitsuba 的定性对比
- Project page: https://denghilbert.github.io/self-cali/

**v1 已标 / v2 仍未补的项**：
- GPU / 训练时长 / 数据集分辨率：正文未给，依赖 supplementary
- 是否开源 code：project page https://denghilbert.github.io/self-cali/ 注明 release 情况，v2 未深入爬