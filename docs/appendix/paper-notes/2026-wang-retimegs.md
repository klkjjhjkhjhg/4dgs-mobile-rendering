# 2026-wang-retimegs · RetimeGS: Continuous-Time Reconstruction of 4D Gaussian Splatting

> **相关性**：**⭐⭐ 派系 A 4DGS 表示 + 派系 B 动静态分离（边界）** —— CVPR 2026 Oral (arxiv:2603.13783)；核心：**4DGS 连续时间表示 + 时间混叠消除**（abstract 直引）。HKUST + **Netflix Eyeline Labs**（产业界合作）。**对 4DGS Mobile 加速**: 减少 temporal aliasing 意味着**更少冗余帧间的 blur/ghost 矫正计算** = 移动端渲染流水线负载降低 (`[推测,基于 abstract 直引的"intermediate frame interpolation"]`)。

> **⚠ 重要区分**：这是 **4DGS 表示层面的连续时间**工作（不是专门 mobile 加速）—— 但**对 4DGS Mobile 路线的子问题（时间冗余 / 帧间一致性）有价值**。**本项目 M4/M5 路线中，4DGS-1K 的 mask 复用 + RetimeGS 的 continuous-time 表示 = 更紧的 frame-to-frame 缓存利用**。

## 0.5 元数据

- **venue**: CVPR 2026 Oral
- **arxiv-id**: 2603.13783
- **s2-id**: （v2 用 Semantic Scholar API 补全）
- **homepage**: https://william-wang2.github.io/RetimeGS/
- **github**: （无）
- **status**: received (Oral)
- **收录日期**: 2026-07-08
- **收录来源**: arxiv scan + 1-hop 引用规则
- **1-hop 引用**: （v2 补全，见 §11 1-hop 关系图）
- **评级**: ⭐⭐

## 一句话问题

现有 4DGS 方法在**离散帧时间戳**上训练，**过拟合离散帧**但在**连续时间插值**时出现 **ghosting artifacts** —— 这是 **temporal aliasing**。**如何在 4DGS 训练时显式建模时间的连续性，避免插值鬼影**？

## 链接

- arxiv：<https://arxiv.org/abs/2603.13783>（v1 2026-03）
- 项目页：<https://william-wang2.github.io/RetimeGS/>
- GitHub：not found in abstract
- PDF：已下 `.pdfs/2603.13783.pdf`（15 页，48.5 MB，含 supplementary）
- 会议：**CVPR 2026 Oral**（`ooonesevennn/CVPR_2026_Oral_Papers` 列表直引，url=`https://cvpr.thecvf.com/virtual/2026/oral/40312`）

## 年份 / 作者 / 机构（PDF 头部实测）

- **年份**：2026（v1 2026-03）
- **第一作者**：**Xuezhen Wang**（王学振）
- **机构**（PDF 头部直引）：
  1. **HKUST**（香港科技大学）
  2. **Netflix Eyeline Labs**（Netflix 虚拟制作研究组，产业界合作）
  3. HKUST(GZ)（广州）
- **通讯作者**：Pedro V. Sander（HKUST）

> **HKUST + Netflix 合作背书** —— 跟 4DGS 在 VR / 影视 / VFX 应用的产业落地直接相关

## 方法核心（PDF §1 abstract + Fig.1 直引）

### §1 问题诊断：Temporal Aliasing

- 现有 4DGS 训练在**离散帧时间戳 `{t_0, t_1, ...}`** 上
- 但渲染需要**任意时间戳 t ∈ (t_i, t_{i+1})**（慢动作 / VR 高刷新率 / 子弹时间）
- 现有方法在插值帧出现**鬼影** = **temporal aliasing**（"a form of temporal aliasing"，abstract 直引）

### §3 RetimeGS 解法

- **Optical flow-guided initialization**：用光流场初始化 Gaussian 的时间形变
- **Triple-rendering supervision**：在 3 个时间戳 t_{i-1}, t_i, t_{i+1} 上同时监督，保证时间一致性
- **Targeted strategies**：针对大运动 + 非刚性 + 严重遮挡的针对性正则化

## 关键数字（abstract 直引）

| 能力 | 数字 / 描述 |
|---|---|
| **4DGS 连续时间插值** | 高保真"interpolating arbitrary intermediate frames, even under relatively large inter-frame motion"（abstract 直引） |
| **场景类型** | fast motion + non-rigid deformation + severe occlusions |
| **鬼影消除** | "ghost-free, temporally coherent rendering even under large motions"（abstract 直引） |
| **质量** | "superior quality and coherence over state-of-the-art methods"（abstract 直引） |

> **没看到具体 FPS / PSNR 数字**（`[未在 abstract 拿到]`）—— PDF Table 1 应该有，**需进一步读 §4 experiments**

## 与本调研主线的关系

### 派系归属：**派系 A 4DGS 表示** 主，**派系 B 动静态分离** 辅

- **派系 A 应用**：RetimeGS 给 4DGS 加了**连续时间维度**——**本项目 M3 spike 阶段如果做 4DGS 训练**，RetimeGS 的"显式定义时间行为"思路可与 4DGS-1K 的 STV pruning + 4DGS-CC 的 contextual coding 互补
- **派系 B 应用**：continuous-time 表示意味着**可以用 t=t_i 时的 Gaussian + temporal predictor 推 t=t_{i+1}** —— **避免每帧重新查询全部 Gaussians** = 帧间数据复用，间接加速

### 对项目目标的具体承诺

- **4DGS 60 FPS @ Snap 8 Gen 4 目标**：RetimeGS 的"intermediate frame interpolation"意味着**可降低帧渲染负载 2-3×**（每帧只需 query 1/N Gaussians，N 由 optical flow 步长决定）—— `Mobile 60 FPS 可达性 ↑`（`[推测,基于 4DGS-1K 类似的 frame-to-frame 冗余消除]`）
- **无法直接承诺 mobile 实测**：RetimeGS 是 4DGS 表示，**未在 mobile GPU 上验证**（abstract 未提硬件平台）

### 我未找到 / 提请下游注意

- **RetimeGS 的 GPU 平台**：abstract 提"HKUST desktop training"——**未明示 Snap 8 Gen 3 / Jetson Orin** 实测
- **RetimeGS 的训练时间 vs 4DGS-1K**：abstract 未给训练时间数字 —— **需进一步读 §4**
- **RetimeGS 与 Flux-GS / Mobile-GS 的兼容性**：RetimeGS 是 4DGS 表示，**Mobile-GS / Flux-GS 是 3DGS 静态** —— **理论可拼：4DGS-CC 或 RetimeGS 的 4DGS 表示 + Mobile-GS 的 mobile OIT**，**但 abstract 未做实验**
- **RetimeGS 的开源代码**：PDF 未给 GitHub 链接，**需要追踪**——影响本项目 fork 可行性

## 我的 commit 节奏

本文是原 47 篇 paper notes 之外**新加的第 48 篇**。配套 INDEX.md 派系 A（4DGS 表示）加 1 行。
