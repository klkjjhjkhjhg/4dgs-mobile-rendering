# 2026-thomas-gausslite · GaussLite: Online Task-Conditioned 3D Gaussian Splatting for Real-Time Robotic Mapping

> **相关性**：**⭐⭐⭐ 派系 3（移动端 / 端侧）** —— arXiv 2026-06-29；**MIT AeroAstro 团队**（Jonathan P. How 是 MIT 知名 robotics 教授）；核心数字：**4 Hz real-time on resource-constrained hardware, +2.72 dB ROI PSNR on Replica, +2.23 dB on real hardware**（abstract 直引）；**multi-agent fusion shares only 7.08% of map**（PDF 直引）。**GaussLite 是首篇显式"task-conditioned 3DGS for robotics"的工作**——LLM 解析 natural-language task → 分配 Gaussian 到 ROI 区域。

> **⚠ 重要区分**：这是 **3DGS（静态）** + **SLAM** 工作，**不是 4DGS**。**对 4DGS 适用性**：task-conditioned density allocation 可扩展到 4DGS time-ROI 分配；**对 dynamic SLAM 路线有方法学价值**。**4 Hz 实时性是机器人端侧 mobile-grade 指标**——证明 3DGS-based SLAM 可在低算力硬件上跑。

## 0.5 元数据

- **venue**: arxiv pre-print (2026-04)
- **arxiv-id**: 2606.30809
- **s2-id**: （v2 用 Semantic Scholar API 补全）
- **homepage**: （无）
- **github**: （无）
- **status**: under review
- **收录日期**: 2026-07-08
- **收录来源**: arxiv scan + 1-hop 引用规则
- **1-hop 引用**: （v2 补全，见 §11 1-hop 关系图）
- **评级**: ⭐

## 一句话问题

3DGS SLAM 系统**对所有 Gaussians 一视同仁（uniform density）**，**但机器人任务只关心场景中一部分**（e.g. "fetch the cup on the table"）—— 浪费算力。**如何在 task-conditioned 方式下分配 Gaussian 密度 + 多机器人 map 融合 + 4 Hz 实时**？

## 链接

- arXiv：<https://arxiv.org/abs/2606.30809>（v1 2026-06-29）
- 项目页：not found in abstract
- GitHub：not found in PDF
- PDF：已下 `.pdfs/2606.30809.pdf`
- 会议：not found in abstract（arXiv preprint）

## 年份 / 作者 / 机构（PDF 头部实测）

- **年份**：2026（v1 2026-06-29）
- **第一作者**：**Annika Thomas**
- **通讯作者**：**Jonathan P. How**（MIT AeroAstro 教授，知名 robotics researcher）
- **机构**：**Massachusetts Institute of Technology（MIT）** —— Department of Aeronautics and Astronautics（AeroAstro）

> **MIT + Jonathan P. How 团队背书** —— 这篇工作有可能被 robotics 顶会接收（RSS / ICRA / IROS）

## 方法核心（PDF §3 直引）

### §3.1 Task-Conditioned Density Allocation

- **LLM 解析 natural-language task**（e.g. "navigate to red chair"）→ open-vocabulary detector + segmenter
- 生成 per-pixel **relevance mask**（只在 task 相关区域分配高密度 Gaussian）
- 在 training 阶段：**relevance-driven seeding + gradient scaling**——非 ROI 区域 Gaussian 数量被压低

### §3.2 Multi-Agent Map Fusion

- 多机器人协作场景：每个 agent 维护**自己的 per-voxel submap**
- Fusion：只在两 agent 都有 ROI 的 voxel 做 merge，**只共享 7.08% 的 map 数据**（PDF 直引）
- **结果**：**+3.42 dB PSNR over concatenation baseline**

### §3.3 Resource-Constrained Deployment

- **≤1M Gaussian budget** 硬约束
- **≤0.5 s / frame** latency 上限
- 实测 **4 Hz on real hardware**（`resource-constrained hardware`，**abstract 未明示具体平台**，`[推测]` 是 Jetson Orin / 嵌入式 GPU）

## 关键数字（PDF Table I 直引 + abstract 直引）

| 方法 | Replica avg PSNR↑ | SSIM↑ | LPIPS↓ | 备注 |
|---|---|---|---|---|
| SplaTAM | 28.56 | 0.821 | 0.230 | 静态 baseline |
| MonoGS | 26.10 | 0.815 | 0.287 | 静态 baseline |
| Gaussian-SLAM | 26.62 | 0.823 | 0.303 | 静态 baseline |
| **GaussLite (Ours)** | **29.81** | **0.835** | **0.230** | **+1.25 dB over SplaTAM** |

> **abstract 直引**："4 Hz real-time mapping on resource-constrained hardware; **+2.72 dB ROI PSNR on Replica, +2.23 dB ROI PSNR on real hardware** (indoor/outdoor); multi-agent fusion **+3.42 dB PSNR while only sharing ~7.08% of map**."

## 与本调研主线的关系

### 派系归属：**派系 3（移动端）** 主，**派系 1（训练期压缩）** 辅

- **派系 3 应用**：**4 Hz 实时性证明 3DGS-based SLAM 可在低算力硬件上跑**——本项目 M3 spike 阶段如果做端到端 4DGS SLAM，**GaussLite 的 task-conditioned 思路可移植**
- **派系 1 应用**：≤1M Gaussian budget 强约束 + 实时 pruning —— 4DGS temporal dimension 必然让 Gaussian 数量爆炸，**GaussLite 的 task-conditioned density 是潜在解法**

### 对项目目标的具体承诺

- **4 Hz 实时性 vs 本项目 60 FPS 目标**：差距 15×。**但 GaussLite 是 3DGS + SLAM，4 Hz 包含 mapping + tracking + rendering 全流程**；本项目 4DGS 60 FPS 是 rendering-only，**实际 M5 demo 端到端可能也是 4-10 Hz 量级**（`[推测]`）
- **MIT AeroAstro + Jonathan P. How 背书**：意味着这篇工作的方法学**有 robotics 顶会 RSS/ICRA 接收潜力**——本项目引用可加强学术深度

### 我未找到 / 提请下游注意

- **GaussLite 跑的硬件平台**：abstract 只说 "resource-constrained hardware"，**未明示 Snap 8 Gen 3 / Jetson Orin / 其他**（`[未在 abstract 拿到]`）
- **GaussLite 的开源代码**：PDF 未给 GitHub 链接
- **4DGS 扩展**：task-conditioned 在 4DGS 场景下**task 可能包含时间维度**（e.g. "predict trajectory of pedestrian 5s ahead"）—— 概念可移植但 abstract 未做

## 我的 commit 节奏

本文是 33 + 1 (Flux-GS) + 8 (subagent) 之外**新加的第 43 篇**。配套 INDEX.md 派系 C（渲染加速 / 移动端）加 1 行。
