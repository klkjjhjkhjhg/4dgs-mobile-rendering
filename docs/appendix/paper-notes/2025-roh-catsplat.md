# CATSplat: Context-Aware Transformer with Spatial Guidance for Generalizable 3D Gaussian Splatting from A Single-View Image

**作者**: Wonseok Roh, Hwanhee Jung, Jong Wook Kim, Seunggwan Lee, Innfarn Yoo, Andreas Lugmayr, Seunggeun Chi, Karthik Ramani, Sangpil Kim
**机构**: Korea University; Google; CNAPS.AI Inc.; Purdue University
**会议**: ICCV 2025
**arxiv-id**: 2412.12906v2
**本地 PDF**: .pdfs/iccv2025-Roh_CATSplat_Context-Aware_Transformer_with_Spatial_Guidance_for_Generalizable_3D_Gaussian_ICCV_2025_paper.pdf
**survey citekey**: (待 M2b extract_paper_summary.py 自动生成)
**GitHub**: (未在抽到的 PDF 段落中提及——v1 + v2 PDF 重抽 (p.1-11, 11 页全文) 均未发现 github.com / gitlab 等代码仓 URL; abstract / intro / §4 experiments 均未列代码地址, 标 "未在抽到的 PDF 段落中提及")
**收录日期**: 2026-08-13
**收录来源**: P36 精读补全（v1 + v2 subagent 交叉验证）

## 一句话
CATSplat 提出一个通用 (generalizable) 的单图 3D Gaussian Splatting 重建框架，在传统 generalizable 3DGS 范式（pixel-aligned Gaussian primitives）基础上，引入两个新颖先验——来自 VLM (LLaVA) 的文本上下文先验 (contextual prior) 和来自 2D depth back-projected 3D 点云的空间先验 (spatial prior)——通过多尺度 transformer 的 cross-attention 增强单视图 image features，从而在没有多视图对应的情况下从单张图预测高质量 3D Gaussian 场景。

## 关键数字(paper 实测)

### D-NeRF 风格 SOTA 复现：Table 1 (RE10K NVS, 单视图对比) — *v2 新增, v1 缺*
- **29.09 / 0.907 / 0.094 (PSNR↑/SSIM↑/LPIPS↓)**：CATSplat 在 RE10K n=5 frames 设定（vs Flash3D 28.46/0.899/0.100；vs MVSplat 26.39 / Splatter Image 28.15 / MINE 28.45）— 全表最优 (来源：PDF p.6 Table 1)
- **26.44 / 0.866 / 0.125 (n=10)**：CATSplat vs Flash3D 25.94/0.857/0.133（来源：PDF p.6 Table 1）
- **25.45 / 0.841 / 0.151 (n=Random, ±30 frames)**：CATSplat vs Flash3D 24.93/0.833/0.160（来源：PDF p.6 Table 1）

### Table 2 (RE10K Interpolation vs Extrapolation, 单/双视图) — *v2 新增*
- **25.23 / 0.835 / 0.159 (Interpolation)**：CATSplat 单视图 vs Flash3D 单视图 23.87/0.811/0.185；vs MVSplat 双视图 26.39/0.869/0.128（来源：PDF p.6 Table 2）
- **25.35 / 0.837 / 0.159 (Extrapolation)**：CATSplat 单视图 vs Flash3D 24.10/0.815/0.185；vs MVSplat 23.04/0.813/0.185；CATSplat 在 extrapolation 上超过所有双视图 baseline（来源：PDF p.6 Table 2）

### Table 3 (Cross-dataset generalization) — *v2 新增*
- **RE10K → NYUv2**：CATSplat 25.57/0.781/0.157 vs Flash3D 25.09/0.775/0.182（来源：PDF p.6 Table 3）
- **RE10K → ACID**：CATSplat 24.73/0.739/0.250 vs Flash3D 24.28/0.730/0.263（来源：PDF p.6 Table 3）
- **RE10K → KITTI**：CATSplat 22.43/0.833/0.122 vs Flash3D 21.96/0.826/0.132（来源：PDF p.6 Table 3）

### Table 4 (Ablation on priors) — *v2 新增*
- **Baseline** n=10: 26.04/0.857/0.132；n=Random: 25.02/0.834/0.159（来源：PDF p.7 Table 4）
- **w/ Contextual** n=10: 26.40/0.864/0.127；n=Random: 25.40/0.838/0.153（来源：PDF p.7 Table 4）
- **w/ Spatial** n=10: 26.38/0.864/0.127；n=Random: 25.42/0.837/0.153（来源：PDF p.7 Table 4）
- **CATSplat (combined)** n=10: 26.44/0.866/0.125；n=Random: 25.45/0.841/0.151（来源：PDF p.7 Table 4）

### Table 5 (Pre-trained visual priors vs ours) — *v2 新增*
- **w/ ConvNeXt-B** n=10: 26.15/0.856/0.132（来源：PDF p.7 Table 5）
- **w/ ConvNeXt-L** n=10: 26.17/0.857/0.132（来源：PDF p.7 Table 5）
- **w/ DINOv2-B** n=10: 26.17/0.858/0.131（来源：PDF p.7 Table 5）
- **w/ DINOv2-g** n=10: 26.19/0.859/0.131（来源：PDF p.7 Table 5）
- **w/ Contextual (Ours)** n=10: 26.40/0.864/0.127（来源：PDF p.7 Table 5）— 比所有 DINOv2/ConvNeXt 视觉预强 baseline 提升 +0.21-0.25 PSNR

### Table 6 (Text description format ablation) — *v2 新增*
- **w/ Scene Type** n=10: 26.14/0.859/0.130；**w/ Object List**: 26.23/0.862/0.128；**w/ Extended (paragraph)**: 26.31/0.862/0.128；**w/ Single Sentence (Ours default)**: 26.40/0.864/0.127（来源：PDF p.7 Table 6）— 单句 caption 最优

### Table 7 (Geometric cues ablation) — v1 已有
- **26.04 / 0.857 / 0.132**：Baseline n=10 (来源：PDF p.8 Table 7)
- **26.38 / 0.864 / 0.127**：加入 Point Features (w/ Point Feat.) 在同一 RE10K n=10 设定下（最优 ablation, 来源：PDF p.8 Table 7）
- **25.42 / 0.837 / 0.153**：加入 Point Features 在 n=Random frames 设定（来源：PDF p.8 Table 7）

### Table 8 (User study) — v1 已有
- **88.42% (RE10K) / 91.41% (ACID) preference**：User study 中 CATSplat vs Flash3D 的偏好比例；Flash3D 仅 11.58% / 8.59%（来源：PDF p.8 Table 8）
- **6.04 (RE10K) / 5.27 (ACID) Likert (1-7 scale)**：CATSplat 7-point Likert 评分，Flash3D 仅 4.56 / 4.14（来源：PDF p.8 Table 8）

### 训练设置
- **60 / 20 scenes**：User study 选取 RE10K / ACID 场景数；100 名 Amazon Mechanical Turk 受试者（来源：PDF p.8 §4.4）
- **5 / 10 / Random frames**：RE10K NVS 评估协议（3 个目标 frame 距离；Random 在 ±30 frames 内随机抽样）；Interpolation / Extrapolation 协议沿用 Flash3D / pixelSplat / latentSplat（来源：PDF p.5 §4.1 + p.6 Table 1 caption）
- **RealEstate10K / ACID / KITTI / NYUv2**：4 个评测数据集（来源：PDF p.2 §1 + p.6 实验段）
- **1CA / 2CA / 3CA**：Iterative cross-attention iteration 消融，PSNR 从 25.09 → 25.36 → 25.45（来源：PDF p.7 Fig. 5）

## 重要 claim（v2 补到 8 个, v1 仅 5 个）
- CATSplat 是首个在单视图 generalizable 3DGS 重建中同时引入 VLM 文本上下文先验和 3D 点云空间先验的框架；填补了 pixelSplat / MVSplat（多视图）与 Flash3D（仅 2D depth 单视图）之间的方法论空白（来源：PDF p.1 §1）
- 通过文本先验 (text features from VLM LLaVA)，未见过 (unseen) 的相似场景（如 kitchen）可获得 "shared semantic representation" 作为额外锚点，提升跨场景泛化（来源：PDF p.2 §1）
- 通过把 2D depth map back-project 成 3D 点云 (point cloud) 而非仅用 2D depth grid，能在 cross-attention 中给 image features 提供更 rich 的几何结构（来源：PDF p.4 §3.3）
- Multi-resolution 3 层 transformer 设计，逐层 cross-attend text + point features, 用 ratio γ 保留视觉信息（来源：PDF p.3-4 §3.2 + Fig. 4）
- 在 RE10K + ACID 上 user study 显著优于 Flash3D（88% vs 12% 偏好）（来源：PDF p.8 §4.4 + Table 8）
- 在 RE10K Extrapolation 协议（target frames ≥45 frames away）上，CATSplat 单视图 (25.35 PSNR) 甚至超过所有双视图 baseline (pixelSplat 21.84 / latentSplat 22.62 / MVSplat 23.04)，表明 priors 让单图摆脱短距离视觉约束（来源：PDF p.6 Table 2 + §4.2 extrapolation 段）
- Cross-dataset generalization (RE10K 训练 → NYUv2/ACID/KITTI 测试)：CATSplat 全面优于 Flash3D +0.16 ~ +0.47 PSNR；ACID (outdoor aerial) 与 KITTI (driving) 的显著提升证明 text-prior + point-prior 对 domain gap 鲁棒（来源：PDF p.6 Table 3 + §4.2 cross-dataset 段）
- 对比 pre-trained 视觉预强 (DINOv2-g / ConvNeXt-L) 替换 cross-attention 输入：VLM text + point features (Ours) 比最强 vision-only baseline (DINOv2-g) 在 n=10 上高 +0.21 PSNR (26.40 vs 26.19)，证明 VLM 的语言驱动洞察能补视觉信息纯冗余的局限（来源：PDF p.7 Table 5 + §4.3 Vs. Pre-trained Visual Pre-training 段）
- 单句 text description 比 scene type / object list / extended paragraph 都好，证明过度细节会引入 over-statement 而 single-sentence 提供恰当锚点（来源：PDF p.7 Table 6 + §4.3 段）

## 评价(survey 引用规范)
- 派系归属：**E**（Cross-disciplinary 派系；单视图 generalizable 3DGS 重建涉及 VLM + 单图重建 + 多 prior 跨方向，非 4DGS / 非 dynamic / 非 mobile streaming / 非显式加速；与 INDEX.md §E 主线一致；v1 → v2 保留 E）
- 相关性：**低**（核心创新在 single-view 通用 3DGS，不直接解决 4DGS 调研的 mobile rendering / dynamic scene / SLAM / pose / memory 任何核心问题；但其 generalizable feed-forward 思路可作为 4DGS-SLAM 的 reference-anchor baseline，可借鉴 text-prior 增强 dynamic 4DGS 的 scene understanding）
- 方法简述：单图 → ResNet encoder → multi-resolution 3 层 transformer（cross-attend VLM text features + 3D point cloud features）→ Gaussian decoder 输出 per-pixel 3DGS

## 关键段落 anchor
- §1 Introduction：p.1-2，强调 monocular 3D 重建比 multi-view 更难（无 cross-view correspondences），CATSplat 用两个 priors 弥补单图信息缺失
- §2 Related Work：p.2-3，分 Sparse-view / Single-view / VLMs 三支，pixelSplat + MVSplat + Splatter Image + Flash3D + CLIP/BLIP-2/LLaVA 是核心 reference
- §3 Method：p.3-5，**核心方法段**：§3.1 Overview (transformer pipeline), §3.2 Context-Aware (text cross-attention, Eq.1-2), §3.3 Spatial Guidance (3D point cloud cross-attention, Eq.3-5, ratio γ 在 Eq.5), §3.4 Gaussian Parameters Prediction (depth offset + 3D offset → µ; opacity α / covariance Σ / color c; loss Eq.8 L_total = λ_L1·L1 + λ_ssim·L_ssim + λ_lpips·L_lpips)
- §4 Experiments：p.5-8，**PDF 重抽 p.5-9 已补全 Table 1-6**：§4.1 Experimental Setup (4 datasets + 5-frames/10-frames/Random evaluation + Interpolation/Extrapolation protocols); §4.2 Performance Comparisons SOTA (Table 1 RE10K NVS / Table 2 Interp+Extrap / Table 3 Cross-dataset); §4.3 Ablation (Table 4 priors / Table 5 vs pre-trained vision / Table 6 text format / Fig.5 CA iterations); §4.4 Visual Comparisons + Table 7 (geometric cues ablation) + Table 8 (user study) + §5 Conclusion
- Figure 1：p.1，**Generalizable 3D scene reconstruction pipeline** 概览（input single view → encoder → decoder → 3D Gaussians → novel views）
- Figure 2：p.2，**两个 priors + VLM text description 示例** (e.g. "A kitchen with a white stove...")
- Figure 3：p.3，**CATSplat framework overview** — Image encoder + Point cloud encoder + VLM (frozen) → cross-attention transformer layers → Gaussian decoder
- Figure 4：p.4，**detailed transformer pipeline** — cross-attention(Q from image, K/V from text) 然后 cross-attention(Q from image, K/V from point)，ratio γ 融合
- Figure 5：p.7，**Iterative cross-attention ablation** (1CA / 2CA / 3CA 的 PSNR 25.09 / 25.36 / 25.45)
- Figure 6：p.8，**Qualitative vs Flash3D**（RE10K + ACID 6 个场景对比）
- Table 1：p.6，**RE10K NVS**（6 methods × 3 target frame settings × 3 metrics）
- Table 2：p.6，**RE10K Interpolation + Extrapolation**（5 two-view baselines + 2 single-view）
- Table 3：p.6，**Cross-dataset** (RE10K → NYUv2/ACID/KITTI, CATSplat vs Flash3D)
- Table 4：p.7，**Ablation: priors** (Baseline / w/ Contextual / w/ Spatial / Combined)
- Table 5：p.7，**Ablation: vs pre-trained vision** (ConvNeXt-B/L + DINOv2-B/g vs Ours)
- Table 6：p.7，**Ablation: text format** (Scene Type / Object List / Extended / Single Sent.)
- Table 7：p.8，**Ablation: geometric cues**（Baseline / w/o Depth Conc. / w/ Point Conc. / w/ Depth Feat. / w/ Point Feat.）
- Table 8：p.8，**User study**（RE10K 60 场景 + ACID 20 场景, 100 受试者, 7-point Likert）