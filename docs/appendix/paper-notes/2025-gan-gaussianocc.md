# GaussianOcc: Fully Self-supervised and Efficient 3D Occupancy Estimation with Gaussian Splatting

**作者**: Wanshui Gan¹,² (equal contribution), Fang Liu¹ (equal contribution), Hongbin Xu³, Ningkai Mo⁴, Naoto Yokoya¹,² (corresponding)
**机构**: ¹The University of Tokyo; ²RIKEN; ³South China University of Technology; ⁴Shenzhen Institute of Advanced Technology, Chinese Academy of Sciences
**会议**: ICCV 2025
**arxiv-id**: 2408.11447
**本地 PDF**: .pdfs/iccv2025-Gan_GaussianOcc_Fully_Self-supervised_and_Efficient_3D_Occupancy_Estimation_with_Gaussian_ICCV_2025_paper.pdf
**survey citekey**: (待 M2b extract_paper_summary.py 自动生成)
**GitHub**: https://github.com/GANWANSHUI/GaussianOcc.git
**收录日期**: 2026-08-13
**收录来源**: P36 精读补全（subagent v1→v2）

## 一句话
GaussianOcc 提出两阶段 pipeline —— Stage 1 用 GSP（Gaussian Splatting for Projection）模块提供 cross-view scale 监督，使 surround-view 3D occupancy estimation 完全 self-supervised（无需 GT ego 6D pose）；Stage 2 用 GSV（Gaussian Splatting from Voxel space）模块在体素网格顶点直接视作 3D Gaussian 做 splatting 渲染，替代传统 volume rendering 实现训练 2.7× 加速、渲染 5× 加速。 *(vs v1 一致 ✓)*

## 关键数字（paper 实测） — v2 重抽中间页（page 5–7）补全 Table 1 / Table 2 / Table 4–7

### Table 1：3D occupancy on Occ3D-nuScenes (mIoU*) — v2 完整重抽
| Method | GT Occ. | GT Pose | mIoU* | mIoU |
|---|---|---|---|---|
| MonoScene [4] | ✓ | × | 6.33 | 6.06 |
| BEVDet [18] | ✓ | × | 20.03 | 19.38 |
| BEVFormer [28] | ✓ | × | 24.64 | 23.67 |
| OccFormer [56] | ✓ | × | 22.39 | 21.93 |
| TPVFormer [20] | ✓ | × | 28.69 | 27.83 |
| CTF-Occ [40] | ✓ | × | **29.54** | **28.53** |
| RenderOcc [36] | × | × | 24.53 | 23.93 |
| SimpleOcc [11] | × | ✓ | 7.99 | 7.05 |
| SelfOcc [21] | × | ✓ | 10.54 | 9.30 |
| OccNeRF [53] | × | ✓ | 10.81 | 9.54 |
| **GaussianOcc** | × | × | **11.26** | **9.94** |

> v1 报 Stage 2 occupancy "GT pose+VR mIoU* 10.81" 等数据 → v2 校为 **Table 1 是 nuScenes Occ3D 主对比 (mIoU* 11.26 vs OccNeRF 10.81)**，是任务级 cell
> RenderOcc [36] 是 weakly-supervised（无 3D 标签但用 GT depth+semantic）*(v1 漏；v2 补)*

### Table 2：Depth estimation on nuScenes & DDAD — v2 完整重抽
**nuScenes**
| Method | GT Occ | GT Pose | Abs Rel | Sq Rel | RMSE | RMSE log | δ<1.25 | δ<1.25² | δ<1.25³ |
|---|---|---|---|---|---|---|---|---|---|
| FSM [14] | × | × | 0.297 | - | - | - | - | - | - |
| FSM* [14] | × | × | 0.319 | 7.534 | 7.860 | 0.362 | 0.716 | 0.874 | 0.931 |
| SurroundDepth [43] | × | × | 0.280 | 4.401 | 7.467 | 0.364 | 0.661 | 0.844 | 0.917 |
| SA-FSM [49] | × | × | 0.272 | 4.706 | 7.391 | 0.355 | 0.689 | 0.868 | 0.929 |
| VFF [26] | × | × | 0.289 | 5.718 | 7.551 | 0.348 | 0.709 | 0.876 | 0.932 |
| R3D3 [37] | × | × | 0.253 | 4.759 | 7.150 | - | 0.729 | - | - |
| **GaussianOcc ‡ (Stage 1)** | × | × | **0.258** | **5.733** | **7.222** | **0.343** | **0.753** | **0.888** | **0.934** |
| GaussianOcc † (Stage 2 + semi) | × | ✓ | 0.197 | 1.846 | 6.733 | 0.312 | 0.746 | 0.873 | 0.931 |

**DDAD**
| Method | Abs Rel | Sq Rel | RMSE | RMSE log | δ<1.25 | δ<1.25² | δ<1.25³ |
|---|---|---|---|---|---|---|---|
| FSM* [14] | 0.228 | 4.409 | 13.433 | 0.342 | 0.687 | 0.870 | 0.932 |
| VFF [26] | 0.218 | 3.660 | 13.327 | 0.339 | 0.674 | 0.862 | 0.932 |
| SurroundDepth [43] | 0.208 | 3.371 | 12.977 | 0.330 | 0.693 | 0.871 | 0.934 |
| SA-FSM [49] | 0.187 | 3.093 | 12.578 | 0.311 | 0.731 | 0.891 | **0.945** |
| R3D3 [37] | 0.162 | 3.019 | 11.408 | - | **0.811** | - | - |
| **GaussianOcc ‡** | 0.212 | 3.556 | 12.564 | 0.320 | 0.701 | 0.888 | 0.944 |
| **GaussianOcc** (Stage 2 + semi) | 0.228 | 3.854 | 14.326 | 0.357 | 0.660 | 0.853 | 0.922 |

> 注：Ground truth depth range clamp 不同（nuScenes 80m，DDAD 200m） —— (v2 补)
> v1 报 Table 3 "Stage 1 depth estimation nuScenes Abs Rel 0.211 / Sq Rel 3.115 / RMSE 7.131 / δ<1.25 0.762" → v2 校核：Table 4 是 "Pose type 消融" (GT vs One-stage vs [26] vs Ours) 而非 Stage 1 与 GT pose 对比；该数据实为 Table 4 cell (Ours row 用 0.211/3.115/7.131/0.762)。Table 2 中 GaussianOcc ‡ Stage 1 用 0.258/5.733/7.222/0.753 -- **v1 与 v2 不一致**

### Table 4：Pose type for Stage 2 training on depth estimation (nuScenes)
| Pose type | Abs Rel | Sq Rel | RMSE | δ<1.25 |
|---|---|---|---|---|
| GT pose | 0.214 | 3.362 | 7.127 | 0.771 |
| One stage training | 0.946 | 17.008 | 16.397 | 0.103 |
| [26] | 0.235 | 3.592 | 7.295 | 0.750 |
| **Ours** | **0.211** | **3.115** | **7.131** | **0.762** |

> v1 把 Table 3/4 数据放在了 Table 3 caption 下；v2 确认为 Table 4 内容（"Pose type ablation"）

### Table 5：Volume Rendering vs Splatting Rendering (Stage 2 深度，GT pose 设置)
| Render type | Abs Rel | Sq Rel | RMSE | δ<1.25 |
|---|---|---|---|---|
| VR (volume rendering) | 0.215 | 3.508 | 7.113 | 0.775 |
| SR (s = 0.05) | 0.223 | 3.694 | 7.246 | 0.761 |
| SR (s = 0.1) | 0.217 | 3.504 | 7.152 | 0.770 |
| SR (s = 0.15) | 0.217 | 3.406 | 7.204 | 0.763 |
| **SR (s = learnable, sigmoid clamped to 0.12)** | **0.212** | **3.248** | **7.112** | **0.771** |

> s = learnable 是最优；s = 0.05 太小会产生 grainy depth map (paper §4.4); s = 0.1 与 VR 相近
> v1 报 "VR Abs Rel 0.225 vs 0.456" → v2 实际是该表 depth=0.215 vs mIoU 在 Table 6 (GT pose VR / SR 0.225 vs 0.197)；校核 OK

### Table 6：GT pose vs Learned pose × VR vs SR on 3D occupancy (nuScenes)
| Pose type | mIoU* | Abs Rel | Sq Rel | δ<1.25 |
|---|---|---|---|---|
| GT pose (VR) | 10.81 | 0.456 | 12.682 | 0.704 |
| GT pose (SR) | 11.30 | 0.225 | 4.339 | 0.787 |
| Learned pose (VR) | 11.19 | 0.506 | 15.577 | 0.684 |
| Learned pose (SR) | 11.26 | **0.197** | **1.846** | 0.746 |

> v1 报 "GT pose+VR mIoU* 10.81 / GT pose+SR mIoU* 11.30 / Learned pose+VR 11.19 / Learned pose+SR 11.26" 完全一致 ✓

### Table 7：Rendering efficiency
| Render | 180×320 | 240×520 | 360×640 | Training time (h/epoch) |
|---|---|---|---|---|
| VR | ≈0.85s | ≈1.57s | N/A（OOM on A100 40GB） | ≈2.68 |
| SR | ≈0.17s | ≈0.17s | ≈0.17s | ≈1 |

> v1 报 "VR ≈ 0.85s vs SR ≈ 0.17s；360×640 SR ≈ 0.17s VR OOM on A100 40GB；VR ≈ 2.68h/epoch vs SR ≈ 1h/epoch" 完全一致 ✓

## 重要 claim（v2 至少补到 6 个）
1. **首个 surround-view fully self-supervised 3D occupancy estimation**，使用 Gaussian splatting，无需 GT 6D ego pose *(PDF p.1 abstract, p.2 §1)* *(vs v1 一致)*
2. **传统 self-supervised 方法（SimpleOcc, OccNeRF, SelfOcc）依赖 GT ego pose 才能得到 real-world scale**；GSP 利用相邻视场 overlap + mask-out 提供 scale 监督，使整个 pipeline 摆脱对 GT pose 的依赖 *(PDF p.2 §1, p.3–4 §3.2)* *(vs v1 一致)*
3. **Volume rendering 在 occupancy 任务上的采样冗余严重**：OccNeRF 采样 108,735,066 点但优化目标只有 2,160,000 体素顶点 *(PDF p.4 §3.3)*；每 vertex 直接视作 3D Gaussian，optimize 其 semantic + opacity；empty space vertex opacity 学为 0，不贡献几何/语义 *(vs v1 一致)*
4. **两阶段训练必要** (vs v1 没强调)：One-stage 直接用 cross-view loss on rendered depth 会落入 local optimum 无法泛化到 non-overlapping region；Stage 2 必须依赖 Stage 1 已收敛的 6D pose net *(PDF p.7 §4.4)*
5. **GSV "render directly from voxel vertices" 解决了 volume rendering biased sampling 问题**（OccNeRF 仅 25% sample points 用作 semantic map rendering）— Splatting rendering 直接渲染 voxel vertices 取消该 bias *(PDF p.5 §3.3)*
6. **Mask-out strategy 与 Erode 操作对 GSP scale-aware training 至关重要**：naive GS without mask-out 会导致 rendered image 仍来自当前 view 的 sub-optimal；erode 二值 mask 排除 overlap 外区域，refinement 2 epochs 固定 6D pose 减少 overlap edge 伪影 *(PDF p.7 §4.4, Table 3)*
7. **nuScenes depth 仅靠 Stage 2 渲染要优于 Stage 1**，DDAD 反过来：差异来自 perception range（80m vs 200m）*(PDF p.5 §4.3)*
8. **SR scale learnable via Sigmoid clamp 0.12 在 Stage 2 深度最优**（s=learnable Abs Rel 0.212 优于 s=0.1 固定 0.217）*(PDF p.7 Table 5，v1 漏)*

## 评价（survey 引用规范）
- 派系归属：**D**（移动端 / 流式落地 派系的边线；surround-view 自动驾驶是 moving sensor platform；splatter rendering 5× 加速对移动端部署有借鉴）。*(vs v1：派系 D 一致 ✓；v2 明确为 "D 边线" 而非 pure D，因为核心问题域是 3D occupancy 而非 mobile rendering)*
- 相关性：**中-高**（v1 评中 → v2 微调）：不直接解决 4D 动态场景的时序建模；但 **(a)** Gaussian splatting 替代 volume rendering 训练 2.7× / 渲染 5× 加速 — 对 §2 mobile rendering 调研有强借鉴价值（与 Flux-GS / Mobile-GS 派系 3 的 3DGS 加速同方向）；**(b)** self-supervised 6D pose + multi-camera scale-aware — 对 §1 高精度表示 主线的 SLAM 派系有交集；(c) Surround-view 多相机场景本质可视为"动态多视角 4DGS"边界案例。*(vs v1 "中" → v2 评 "中-高"，因 splatter 5× 加速证据强)*
- 方法简述：两阶段 pipeline —— Stage 1 用 New-CRFs (Swin Transformer backbone) U-Net 在 2D grid 预测 Gaussian 属性 (depth/scale/rotation)，通过 cross-view GSP 渲染提供 6D pose net 的 scale 监督（无 GT ego pose）；Stage 2 把 2D feature lift 到 3D voxel grid (256×256×16 upsample 512×512×32)，每 vertex 作为 3D Gaussian 做 splatting 渲染。 *(vs v1：增加 512³ voxel grid 上采样细节)*

## 关键段落 anchor — v2 重核
- §1 Introduction：p.1–p.2，volume rendering 在 occupancy 上的两大局限（依赖 GT ego pose + 108M vs 2.16M 采样冗余）
- §3 Method：p.3–p.5 —— §3.1 Preliminaries (p.3)；§3.2 GSP scale-aware training (p.3–p.4)；§3.3 GSV fast rendering (p.4–p.5)
- §4 Experiments：p.5 起，benchmarks：nuScenes + DDAD，指标：Abs Rel / Sq Rel / RMSE / δ<1.25 (depth) + mIoU / mIoU* (occupancy)
- **Table 1 (Occ3D-nuScenes mIoU 主对比)**：**p.5**（v1 漏页码 / cell 残缺 → v2 完整 11 个 baseline）
- **Table 2 (Depth estimation nuScenes + DDAD)**：**p.6**（v1 漏完整 cell → v2 完整 ~14 baselines × 8 metrics × 2 datasets）
- **Table 3 (Scale-aware depth ablation nuScenes)**：**p.6** (7 rows, ✓/✗/GS loss/Mask/Erode/Refine 组合)
- **Table 4 (Pose type for Stage 2 training)**：**p.7**（v1 误标为 Table 3 → v2 校为 Table 4）
- **Table 5 (VR vs SR scale factor ablation)**：**p.7** （v1 漏 — 5 rows of scale s）
- **Table 6 (Pose × Render type on occupancy)**：**p.7**（v1 已抓到）
- **Table 7 (Rendering efficiency)**：**p.7**（v1 已抓到）
- Figure 1：p.1，问题设定图（surround image + 2D semantic annotation，无 GT occupancy / GT ego pose）
- Figure 2：p.3，两阶段方法 Overview (Stage 1 U-Net 2D Gaussian + 6D pose net; Stage 2 voxel Gaussian splatting)
- Figure 5：p.6，cross-view Gaussian splatting vs bilinear interpolation 合成对比
- GitHub: https://github.com/GANWANSHUI/GaussianOcc.git

---

*v2 在 v1 基础上完成：(1) 重抽 page 5–7 中间页确认 Table 1 / Table 2 / Table 4 / Table 5 完整 cell（v1 漏 Tables 1, 2, 4, 5）；(2) 校核 v1 "Stage 1 depth 0.211/3.115/7.131/0.762" 实为 Table 4 cell 而不是 Table 3，已修正；(3) §重要 claim 由 5 个扩到 8 个（含 one-stage 失败原因、mask-out+erode+refine 必要性、SR learnable scale 优势、nuScenes vs DDAD 现象解释）；(4) 相关性由 "中" 微调到 "中-高"（splatter 5× 加速证据强，对 §2 mobile rendering 主线借鉴价值明确）。*

**v1 已标 / v2 仍未补的项**：
- GPU 型号 + batch size + learning rate：正文未明确
- Stage 1 单 epoch 时间：未给出
- Stage 2 上采样 256³ → 512³ 的内存代价数字：未列出
- DDAD 上无 GT occupancy 导致无 occupancy 表：已确认 paper 不提供
