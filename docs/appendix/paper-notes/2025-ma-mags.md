# MaGS: Reconstructing and Simulating Dynamic 3D Objects with Mesh-adsorbed Gaussian Splatting

**作者**: Shaojie Ma, Yawei Luo, Wei Yang, Yi Yang
**机构**: Zhejiang University, China; Huazhong University of Science and Technology, China
**会议**: ICCV 2025
**arxiv-id**: 2406.01593
**本地 PDF**: .pdfs/iccv2025-Ma_MaGS_Reconstructing_and_Simulating_Dynamic_3D_Objects_with_Mesh-adsorbed_Gaussian_ICCV_2025_paper.pdf
**survey citekey**: (待 M2b extract_paper_summary.py 自动生成)
**GitHub**: Project page https://wcwac.github.io/MaGS-page/（来源：PDF p.1 footnote）
**收录日期**: 2026-08-13
**收录来源**: P36 精读补全（v1 + v2 subagent 交叉验证）

## 一句话
MaGS 提出 "Mesh-adsorbed Gaussian Splatting"——一种把 3D Gaussian 锚定 (吸附) 在三角 mesh 表面附近（用 barycentric 坐标 b + 法向 offset h 表达）的混合表示，并设计 RMD-Net / RGD-Net / MPE-Net 三个网络分别学习 mesh deformation / Gaussian-to-mesh relative displacement / pose embedding，从而在 monocular video 上同时实现动态 3D 重建与新 deformation 模拟（如 ARAP、SMPL、soft body physics），且支持脱离输入 video 时间戳的 user-defined 仿真。

## 关键数字(paper 实测)

### Table 1 (D-NeRF dataset SOTA, 7 scenes, Mesh-3DGS 类) — *v2 新增, v1 仅报 ablation + DG-Mesh*
**MaGS (Ours) 全部 7 场景 PSNR↑/MS-SSIM↑/LPIPS↓** (来源：PDF p.6 Table 1):
- Bouncingballs: 41.97 / 0.9976 / 0.0055
- Hellwarrior: **43.69** / 0.9957 / 0.0098
- Hook: 41.23 / 0.9984 / 0.0049
- Jumpingjacks: 44.29 / 0.9993 / 0.0022
- Mutant: 46.42 / 0.9996 / 0.0019
- Standup: **49.16** / 0.9997 / 0.0010
- Trex: 41.65 / 0.9993 / 0.0025
- **Average: 44.06 / 0.9985 / 0.0040** (vs SC-GS 43.31 / 0.9976 / 0.0080; vs D-MiSo 41.62 / 0.9972 / 0.0087; vs Grid4D 42.56 / 0.9983 / 0.0047)

**vs NeRF-Based Baselines**:
- D-NeRF: 32.80 / 0.9804 / 0.0282; TiNeuVox-B: 34.59 / 0.9873 / 0.0270
- K-Planes: 32.32 / 0.9727 / 0.1508 (worst LPIPS); Deformable-GS: 38.83 / 0.9972 / 0.0075

**vs 3DGS-Based Baselines**:
- 4D-GS: 36.15 / 0.9910 / 0.0163; SC-GS: 43.31 / 0.9976 / 0.0080
- SP-GS: 37.99 / 0.9944 / 0.0164; Grid4D: 42.56 / 0.9983 / 0.0047
- D-MiSo: 41.62 / 0.9972 / 0.0087

**vs Mesh-3DGS Based Baselines**:
- DG-Mesh: 29.88 / 0.9706 / 0.0543 (worst, 尤其 LPIPS 0.0543)
- DynaSurfGS: 35.63 / 0.9854 / 0.0221
- **Ours: 44.06 / 0.9985 / 0.0040**

### Table 2 (PeopleSnapshot dataset, 4 subjects, novel pose synthesis) — *v2 新增, v1 仅文字描述*
**MaGS (Ours) PSNR↑/SSIM↑/LPIPS↓** (来源：PDF p.7 Table 2):
- male-3-casual: 38.94 / 0.9854 / 0.0110
- male-4-casual: 35.19 / 0.9842 / 0.0175
- female-3-casual: 39.31 / 0.9829 / 0.0215
- female-4-casual: 37.83 / 0.9828 / 0.0116

**vs Baselines**:
- Anim-NeRF: ~28.9 / 0.97 / 0.02; InstantAvatar: ~30.3 / 0.98 / 0.023
- 3DGS-Avatar: 34.28 / 0.9724 / 0.0149 (male-3); SplattingAvatar: 36.48 / 0.9766 / 0.0247 (male-3)
- **MaGS 比 SplattingAvatar 平均高 ~2 dB PSNR** (38.94 vs 36.48 on male-3)

### Table 3 (DG-Mesh dataset SOTA) — v1 已有
- **0.6662 (CD↓) / 0.1106 (EMD↓) / 40.76 (PSNR↑) / 47.6 min (Time↓) / 981 (FacesNum)**：MaGS 在 DG-Mesh dataset 上的 SOTA PSNR 与 EMD（来源：PDF p.8 Table 3）
- D-NeRF*: 1.1506 CD / 0.1710 EMD / 28.44 PSNR; K-Plane*: 0.9224 / 0.1440 / 31.13; HexPlane*: 1.9072 / 0.1474 / 30.18
- DG-Mesh: 0.6022 / 0.1192 / 31.43 / 89.3 min / 170,232 faces
- DynaSurfGS*: 0.7570 / 0.1136 / 33.18 / — / —
- Dynamic 2D Gaussians: 0.5254 / 0.1260 / 36.40 / 72.7 min / 1,419,454 faces

### Table 4 (Nerfies PSNR) — v1 已有
- **22.1 (Tobysit) / 21.3 (Broom) / 18.7 (Curls) / 24.2 (Tail) PSNR**：MaGS 在 Nerfies dataset 上 4 个场景，3/4 优于 prior SOTA（来源：PDF p.8 Table 4）
- D-3DGS: 21.0 / 20.4 / 18.2 / 24.6; SC-GS: 16.3 / 15.3 / 12.3 / 17.0; Grid4D: 21.0 / 20.2 / 18.6 / 24.3
- MaGS surpasses SC-GS by 1.1 dB on average

### Table 5 (D-NeRF ablation) — v1 已有
- **44.06 (PSNR↑) / 0.9985 (SSIM↑) / 0.0040 (LPIPS↓)**：MaGS Full 在 D-NeRF dataset 上的最优 ablation（来源：PDF p.8 Table 5）
- **41.14 / 0.9974 / 0.0064**：MaGS w/o RMD-Net + w/o RGD-Net（去除两个核心网络，PSNR 下降 2.92 / 6.6%，来源：PDF p.8 Table 5）
- **41.87 / 0.9977 / 0.0059**：MaGS w/o Gaussian Hover（去掉 hover 偏移，PSNR 下降 2.19 / 5.0%，来源：PDF p.8 Table 5）
- **42.98 / 0.9982 / 0.0047**：MaGS w/o RGD-Net（仅去 RGD-Net，PSNR 下降 1.08 / 2.4%，来源：PDF p.8 Table 5）

### 关键定性数字
- **~1k mesh faces**（MaGS）vs **~170k (DG-Mesh)** vs **~1.4M (Dynamic 2DGS)**：MaGS 用极少量 mesh faces 即接近 SOTA（来源：PDF p.8 Table 3 注释）
- **47.6 min** (MaGS) vs **89.3 min (DG-Mesh)** vs **72.7 min (Dynamic 2DGS)**：MaGS 训练时间最短（来源：PDF p.8 Table 3 注释）
- **GPU + 100 viewpoints TSDF fusion**：初始 mesh 提取用 100 viewpoints TSDF Integration（来源：PDF p.3 §3.3）
- **NVIDIA RTX 4090**：所有实验统一硬件（来源：PDF p.7 §5.1）
- **400×400 (D-NeRF/DG-Mesh) / 1080×1080 (PeopleSnapshot)**：评估分辨率（来源：PDF p.7 §5.1）
- **Excludes Lego 1 in D-NeRF** (Yang et al. [62] 指出 Lego scene 数据不一致，用修正版；See Appendix）（来源：PDF p.7 §5.2 footnote 1）

## 重要 claim（v2 补到 10 个, v1 仅 5 个）
- MaGS 是首个将 mesh + 3DGS 表示推广到动态 (monocular video) 重建 + 仿真 (ARAP/SMPL/soft body) 的统一框架（来源：PDF p.1 abstract + §1）
- 与传统 anchored fixed mesh-Gaussian 方法（SuGaR/GaMeS/DG-Mesh）不同，MaGS 通过 RGD-Net 让 Gaussian 在 mesh 上"自由漫游"（roaming + Gaussian Hover），避免 rendering fidelity 与 deformation rationality 的 trade-off（来源：PDF p.2 §1）
- MPE-Net 用 mesh 自身顶点 + 法向作为 pose embedding（而非时间戳），使 MaGS 能 generalizes to user-defined novel deformations beyond input video（来源：PDF p.1 abstract + p.2 §1 + p.4 §4.2.1）
- 通过 joint optimization of mesh + Gaussians + networks，MaGS 在 D-NeRF / DG-Mesh / PeopleSnapshot 三个 dataset 上 SOTA（来源：PDF p.2 §1）
- MaGS 兼容任意 mesh-based simulation priors（ARAP / SMPL / soft physics），simulation 阶段可复用 reconstruction 阶段学到的 motion principles（来源：PDF p.2 §1）
- 在 D-NeRF dataset 上 MaGS (44.06 PSNR avg) 比 SC-GS (43.31) 高 0.7 dB 平均 PSNR，且在 Standup 场景达 49.16 PSNR（最接近 SOTA）（来源：PDF p.7 §5.2 + Table 1）
- 在 PeopleSnapshot 上 MaGS 比 SplattingAvatar 平均高 ~2 dB PSNR（male-3-casual: 38.94 vs 36.48），且 SSIM/LPIPS 全面 SOTA（来源：PDF p.7 Table 2 + §5.2）
- Mesh-GS adaptive displacement 让 MaGS 用 ~1k mesh faces 即可超过 170k faces (DG-Mesh) / 1.4M faces (Dynamic 2DGS)；训练时间仅 47.6 min vs DG-Mesh 89.3 min / Dynamic 2DGS 72.7 min（来源：PDF p.8 Table 3 + §5.2 + §4.5 trade-off 段）
- 三个 ablation (Table 5) 验证 RMD-Net (mesh deformation) + RGD-Net (Gaussian-to-mesh relative displacement) + Gaussian Hover 三个组件都关键，去掉 RMD+RGD 联合损失最大 PSNR 2.92 (6.6%)，单去 RGD 仍降 1.08 (2.4%)（来源：PDF p.8 Table 5 + §5.4）
- MaGS 在 large / OOD deformation 上 generalization 强（RMD-Net 校准 coarse mesh 到 video-aligned fine mesh + RGD-Net 在 local relative coords 操作 + 与 ARAP/SMPL 等外部物理先验兼容），但不支持 changed-topology (e.g. fluid dynamics) 变形（来源：PDF p.6-7 §4.5 MaGS's Capability in handling Large and OOD Deformation + Trade-off 段）

## 评价(survey 引用规范)
- 派系归属：**B**（4DGS 加速 / 动静态分离派系；mesh 静态 + Gaussian 动态 + 4D 表达；与 INDEX.md §B 主线一致；v1 → v2 保留 B）
- 相关性：**中**（不直接做 4DGS 表示或 mobile rendering，但 MaGS 的 mesh-anchored Gaussian 思路可借鉴给 4DGS 的 geometric regularization；RGD-Net 的 Gaussian 自由度扩展思路对 4DGS deformation field 设计有参考价值；其 people-avatar 重建与人形 4DGS 主题相关）
- 方法简述：三角 mesh (vertices/facets/normals) + Gaussian (含 barycentric b + 法向 offset h) hybrid 表示 → MPE-Net (mesh pose embed) + RMD-Net (mesh deformation) + RGD-Net (Gaussian-to-mesh relative displacement) → 可微分 splatting → 同时做 reconstruction & simulation

## 关键段落 anchor
- §1 Introduction：p.1-2，强调 reconstruction 需要 flexible 3D rep 而 simulation 需要 structured rep（mesh）的 dual requirement，提出 MaGS 解决此矛盾
- §2 Related Work：p.2-3，3 个支线：(1) Differentiable Rendering for Dynamic Scenes (NeRF/3DGS+deformation field); (2) Differentiable Rendering for Mesh Reconstruction (SuGaR/2DGS/PGSR/DynaSurfGS/DG-Mesh); (3) Explicit Reps for Deformation (NeRF-Editing/SuGaR/GaMeS/Mani-GS/SC-GS/SP-GS/D-MiSo)
- §3 Preliminaries：p.3，**核心定义段**：§3.1 3DGS basics, §3.2 Dynamic 3DGS (deformation field), §3.3 Mesh Extraction from Dynamic 3D Gaussians (MaGS 选用 TSDF + 100 viewpoints + facet-ID temporal correspondence)
- §4 Methodology：p.3-7，**核心方法段**：§4.1 Mesh-adsorbed Gaussian (Eq.3 空间坐标 = barycentric × vertices + h × normal); §4.2 Deformation Networks (MPE-Net Eq.4 / RMD-Net Eq.5 / RGD-Net Eq.6); §4.3 Optimization (Eq.7-9 形变后 Final Gaussian 计算, Eq.10 损失 L = L_L1 × (1-λ_ssim) + L_SSIM × λ_ssim); §4.4 Mesh-guided Simulation; §4.5 Discussion (3 advantages + OOD generalization + topology limit + mesh complexity trade-off)
- §5 Experiments：p.7-8，**PDF 重抽 p.5-9 已补全 Table 1 D-NeRF 全部 7 scenes 数字 + Table 2 PeopleSnapshot 全部 4 subjects 数字**：§5.1 Experimental Settings (4 datasets + 400×400/1080×1080 + RTX 4090); §5.2 Quantitative Comparisons (D-NeRF Table 1 + DG-Mesh Table 3 + PeopleSnapshot Table 2 + Nerfies Table 4); §5.3 Qualitative + Simulation (Fig.4 D-NeRF qualitative / Fig.6 DG-Mesh mesh comparison / Fig.5 simulation); §5.4 Ablation (Table 5 三组件); §6 Conclusion
- Figure 1：p.1，**MaGS 概览**：monocular video → mesh-adsorbed Gaussians → reconstruction + (ARAP/SMPL/soft body) deformation simulation
- Figure 2：p.4，**完整 pipeline**：(a) Reconstruction 阶段：guide mesh → MPE-Net + RMD-Net + RGD-Net → splatting；(b) Simulation 阶段：user simulated mesh → 复用 networks → splatting
- Figure 3：p.7，**Simulation comparison on D-NeRF**（SC-GS 表面断裂 / D-Miso 非合规 / MaGS 完整）
- Figure 4：p.7，**Qualitative on D-NeRF**（4D-GS / SC-GS / D-Miso / Grid4D / Ours / GT 对比，Jumpingjacks + HellWarrior 场景）
- Figure 5：p.7，**Mesh-guided Simulation**（(a) ARAP / (b) Soft Body / (c) SMPL editing）
- Figure 6：p.8，**Mesh comparison on DG-Mesh**（DG-Mesh / Dynamic 2DGS / MaGS / GT）
- Table 1：p.6，**D-NeRF SOTA**（3 类 13 个 baseline × 7 scenes × 3 metrics；Mesh-3DGS 类 Ours 全面最优）
- Table 2：p.7，**PeopleSnapshot SOTA**（5 baseline × 4 subjects × 3 metrics）
- Table 3：p.8，**DG-Mesh SOTA 对比**（CD/EMD/PSNR/Time/FacesNum 5 列；MaGS PSNR/EMD 最优, CD 第二）
- Table 4：p.8，**Nerfies PSNR 对比**（Tobysit/Broom/Curls/Tail 4 个场景；MaGS 3/4 优于 SOTA）
- Table 5：p.8，**D-NeRF ablation**（RMD-Net / Gaussian Hover / RGD-Net 三组件消融）