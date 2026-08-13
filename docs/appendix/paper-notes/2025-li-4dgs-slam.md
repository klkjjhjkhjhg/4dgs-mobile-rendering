# 2025-li-4dgs-slam · 4D Gaussian Splatting SLAM

> **这是 2025-10 ICCV 2025 的 4DGS-SLAM 系统**(Yanyan Li 等, 杭电+TUM+浙大+Google)。
> **关键差异**:与同期动态 SLAM 系统(MonoGS / SplaTAM / SC-GS / Gaussian-SLAM)**不是"加速"路线**,而是**"显式建模 4D 动态场景"路线** —— 把动态高斯独立于静态高斯,用 sparse control points + MLP 学习形变场 + 2D 光流渲染监督。

## 0.5 元数据

- **venue**: ICCV 2025
- **arxiv-id**: (PDF 未给 arxiv-id 直引; GitHub 仓库公开了 `yanyan-li/4DGS-SLAM`)
- **s2-id**: (待补)
- **homepage / GitHub**: https://github.com/yanyan-li/4DGS-SLAM
- **status**: received
- **收录日期**: 2026-08-13
- **收录来源**: ICCV 2025 整批扫描补缺(此 PDF 在 .pdfs/ 但无对应 note)
- **1-hop 引用**: (待 v2 补)
- **评级**: ⭐⭐
- **survey_section**: 3

## 一句话问题

如何在 SLAM 跟踪 + 建图的同时,**显式建模动态场景的 4D Gaussian 表示**,既保证 tracking 鲁棒性(高动态),又能做高质量动态场景 view synthesis?

## 链接(均经 fetch + PDF 实测验证)
- ICCV 2025 收录:PDF 头部"ICCV 2025"标识
- GitHub: https://github.com/yanyan-li/4DGS-SLAM(PDF abstract 直引)
- PDF: 已下到 `.pdfs/iccv2025-Li_4D_Gaussian_Splatting_SLAM_ICCV_2025_paper.pdf`(10 页)
- arxiv-id:**未在 PDF 显式报出**;项目页提到但 PDF abstract 字段缺失。**未在公开材料拿到 arxiv-id**

## 年份 / 作者 / 机构(PDF §1 + 头部实测)
- **年份**:2025(ICCV 2025)
- **作者**(5 位):**Yanyan Li** (李岩岩, 共同一作)、**Youxu Fang**、Zunjie Zhu† (通讯)、Kunyi Li、Yong Ding、**Federico Tombari**(TUM + Google)
- **机构**:
  1. **Hangzhou Dianzi University**(杭州电子科技大学)
  2. **Technical University of Munich**(慕尼黑工业大学)
  3. **Zhejiang University**(浙江大学)
  4. **Google**

## 方法核心(PDF §3 直引)

1. **Motion mask 生成 + 动静 Gaussian 分离**:
   - 输入 = RGB-D 序列 + 预生成 motion mask
   - **每个 Gaussian 分配 dy 属性**(0=static, 1=dynamic)
   - 静态 Gaussian 用纯 3DGS 表示(只参与 tracking 约束)
   - 动态 Gaussian 用 **sparse control points + MLP(Ψ)** 建模 transformation field

2. **Transformation Field(动态 Gaussian 的形变场)**:
   - **sparse control points** 沿动态 Gaussian 空间分布布置(类似 4DGS-1K 的 STV pruning 思路,但用途相反——**不是剪枝而是形变锚点**)
   - **MLP Ψ** 输入 control points + 时间戳,输出 transformation(translation + rotation)
   - **ARAP loss**(As-Rigid-As-Possible)约束形变的"局部刚度",防止不规则形变

3. **2D Optical Flow Rendering(本工作核心创新)**:
   - 传统 4DGS-SLAM 只用 photometric + geometric 约束
   - 本工作额外:**用动态 GS 渲染 2D 光流图**(在相邻帧间),与预训练光流模型输出做 loss
   - 强制 4D Gaussian 的"运动模式"跟物理光流一致
   - **无需显式 motion segmentation 后期处理**

4. **Joint Optimization**:
   - **Photometric L1(C(p))** + **Geometric L1(D(p))** + **D-SSIM** + **ARAP loss** + **Iso loss**(L_iso 惩罚 ellipsoid 拉伸)
   - 1500 iter color refinement,Loss = `0.2·D-SSIM + 0.8·L1(C) + 0.1·L1(D) + w1·arap + w2·E_iso`

5. **Online Mapping + Tracking**:
   - **Tracking**:基于静态 Gaussian 做 photometric + geometric pose estimation
   - **Mapping**:每帧选 5 个 overlap keyframe 重建当前可见区,2 个 global keyframe 防止遗忘

## 关键数字(全部 PDF Table 1/2/3/4 直引)

### Table 2 · TUM RGB-D Dataset · View Synthesis PSNR / SSIM / LPIPS

| Method | Metric | sit st | sit xyz | sit rpy | walk st | walk xyz | walk rpy | Avg. |
|---|---|---|---|---|---|---|---|---|
| MonoGS[30] | PSNR↑ | 19.95 | 23.92 | 16.99 | 16.47 | 14.02 | 15.12 | 17.74 |
| Gaussian-SLAM[50] | PSNR↑ | 18.57 | 19.22 | 16.75 | 14.91 | 14.67 | 14.5 | 16.43 |
| SplaTAM[21] | PSNR↑ | 24.12 | 22.07 | 19.97 | 16.70 | 17.03 | 16.54 | 19.40 |
| SC-GS[18] | PSNR↑ | 27.01 | 21.45 | 18.93 | 20.99 | 19.89 | 16.44 | 20.78 |
| **Ours** | PSNR↑ | **27.68** | **24.37** | **20.71** | **22.99** | **19.83** | **19.22** | **22.46** |

> **4D-GS SLAM vs SOTA(SplaTAM)**:TUM-Avg PSNR **+3.06 dB**(19.40→22.46);LPIPS **0.241→0.228**(5% 改善);**SSIM 0.757→0.786**(3.8% 改善)

### Table 3 · BONN RGB-D Dataset · View Synthesis

| Method | Metric | ballon | ballon2 | ps_track | ps_track2 | sync | sync2 | p_no_box | p_no_box2 | p_no_box3 | Avg. |
|---|---|---|---|---|---|---|---|---|---|---|---|
| MonoGS | PSNR↑ | 21.35 | 20.22 | 20.53 | 20.09 | 22.03 | 20.55 | 20.76 | 19.38 | 24.81 | 21.06 |
| Gaussian-SLAM | PSNR↑ | 20.45 | 18.55 | 19.60 | 19.09 | 21.04 | 21.35 | 19.99 | 20.35 | 21.22 | 20.18 |
| SplaTAM | PSNR↑ | 19.65 | 17.67 | 18.30 | 15.57 | 19.33 | 19.67 | 20.81 | 21.69 | 21.41 | 19.34 |
| SC-GS | PSNR↑ | 22.3 | 21.38 | – | – | 23.62 | 22.74 | 20.60 | 21.55 | 19.24 | 21.63 |
| **Ours** | PSNR↑ | **25.90** | **22.71** | **21.78** | **20.65** | **23.25** | **25.42** | **23.14** | **24.28** | **25.88** | **23.66** |

> **4D-GS SLAM vs SOTA**:BONN-Avg PSNR **+2.03 dB**(21.63→23.66)

### Table 1 · BONN · Trajectory ATE [cm]↓

| Method | Avg ATE↓ |
|---|---|
| RoDyn-SLAM[20] | 7.9 |
| MonoGS[30] | 33.1 |
| Gaussian-SLAM[50] | 84.3 |
| SplaTAM[21] | 56.8 |
| **Ours** | **3.6** |

> **4D-GS SLAM vs NeRF-based RoDyn-SLAM**:**2.2× 更准**(7.9→3.6 cm);**vs 3DGS-SLAM 系**:**9.2× 更准**(33.1→3.6 cm)

### Table 4 · TUM · Trajectory ATE [cm]↓

| Method | Avg ATE↓ |
|---|---|
| RoDyn-SLAM[20] | 5.1 |
| MonoGS[30] | 15.8 |
| Gaussian-SLAM[50] | 72.4 |
| SplaTAM[21] | 62.2 |
| **Ours** | **1.8** |

> **TUM ATE 1.8 cm**:**3DGS-SLAM 系最佳**;比 RoDyn-SLAM **2.8× 更准**

## 训练 / 推理资源(综合 PDF §4.2 + §4.3)
- **训练设备**:PDF §4.2 未显式报出 GPU 型号;**未在公开材料拿到**
- **训练时长**:**未在 PDF 显式报出**;**未在公开材料精确拿到**
- **推理 FPS**:**未在 PDF 显式报出**;**未在公开材料精确拿到**
- **训练迭代数**:**1500 iterations color refinement**(PDF §4.3 直引)
- **数据集**:
  - **TUM RGB-D**[41] —— 6 sequences(sit st / sit xyz / sit rpy / walk st / walk xyz / walk rpy)
  - **BONN RGB-D Dynamic**[34] —— 9 sequences(balloon / ps_track / sync / p_no_box 等)

## 与本调研主线的关系

### 1. 主线对标(动静态分离 4DGS 范式, 跟 4DGS-1K 不同)
- **4DGS-1K**(Yuan 2025)= **pruning 路线**(STV pruning 砍 #Gauss 数量)——解决 per-frame 冗余
- **4DGS-SLAM**(Li 2025)= **显式 4D 动态表示路线**(control points + MLP 学形变)——解决"动态 SLAM 同时建模动态"
- **两者不冲突,可叠加**:
  - 4DGS-SLAM 提供 tracking 鲁棒性 + 动态场景表示
  - 4DGS-1K 在 4DGS-SLAM 输出的 #Gauss 上做 STV pruning 进一步压缩
  - **但本文作者未做此组合实验**,需下游评估

### 2. 借鉴价值
- **Optical Flow Rendering 监督是本工作**最大创新**:把 2D 光流作为 4D Gaussian 形变场的显式约束,**大幅提升高动态场景 view synthesis + tracking**
- **Sparse control points + MLP Ψ 范式**对项目移动端**可能友好**:control points 数 < dynamic Gauss 1-2 个数量级,MLP Ψ 可在 GPU shared memory 常驻
- **ARAP loss** 是借鉴价值,约束 dynamic Gaussian 形变的"局部刚度"——本项目做 deformable 4DGS 时可考虑

### 3. 不可作为移动端最终方案
- **论文未给移动端 FPS / 显存**:**未在公开材料拿到**
- **RGB-D 输入依赖**:本项目目标是 monocular / few-camera,**跟 4DGS-SLAM 假设不匹配**
- **Tracking + Mapping 双系统架构**:对工程落地复杂度高,**反例基准**

### 4. 对采集端反推(00-goal.md §"必须覆盖")
- TUM RGB-D(手持相机)+ BONN RGB-D(handheld + 动态物体):**monocular RGB-D + 已知 dynamic masks**
- **采集时需配合运动目标检测**(YOLO / Mask R-CNN 之类)生成 motion mask——**不是端到端**,需要预训练检测器

## 我未找到 / 提请下游注意
- **arxiv-id**:PDF 未给;**未在公开材料拿到**
- **训练 GPU 型号**:**未在 PDF §4.2 显式报出**;**未在公开材料精确拿到**
- **训练时长 / scene 分钟数**:**未在 PDF 显式报出**
- **推理 FPS / 显存**:**未在 PDF 显式报出**
- **移动端 / Vulkan / Adreno 数字**:**未在 PDF 找到**
- **GitHub commit 周期 + 是否包含 mobile backend**:从仓库 `yanyan-li/4DGS-SLAM` 看是 PyTorch + diff-gaussian-rasterization 系,**未在公开材料拿到 mobile backend 证据**
- **Optical flow 预训练模型选型**:**未在 PDF §3.3 明确**(推测 RAFT / FlowNet 之类,**这是推测,abstract 未给**)
- **运行时 #Gauss 数量级**:**未在 PDF 显式报出**

## 我的 commit 节奏
- 首次收录 → 本次 PDF 全文级核验 + 关键数字直引
- 下游同步:`02-rendering-acceleration.md` §3 (动静态分离 4DGS 范式段) 引用本文 optical flow rendering 创新
