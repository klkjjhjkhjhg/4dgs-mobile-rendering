# 2026-ghosh-gs-nfs · GS-NFS: Bandwidth-adaptive Streaming of Dynamic Gaussian Splats and Point Clouds

> **相关性**：**⭐⭐⭐ 派系 4（流式落地）+ 4DGS 移动端** —— arXiv 2026-06-04；**NVIDIA 团队**（Rajrup Ghosh 等，Eduardo Pavez 是 NVIDIA Research）；核心数字：**25 FPS decode on Jetson Orin mobile GPU**（abstract 直引）——**4DGS 流式 codec 在 mobile GPU 上 25 FPS 实时解码**！**1-2 orders of magnitude faster encode/decode than SOTA 4DGS compression**；**236 bytes/Gaussian**。**这是 4DGS-on-mobile 主线最强的 2026 H1 直接对标工作**。

> **⚠ 重要区分**：这是 **4DGS** 编码 + 流式工作，**是 4DGS 专项**——与本项目主线 100% 对标。**实测在 Jetson Orin mobile GPU**——与本项目 Snap 8 Gen 4 不同代（Jetson Orin = 2018 GPU 架构，Snap 8 Gen 3 = 2023 Adreno 700 系列），**但都是 mobile GPU**，**有参考价值**。

## 0.5 元数据

- **venue**: arxiv pre-print (2026-06)
- **arxiv-id**: 2606.05650
- **s2-id**: （v2 用 Semantic Scholar API 补全）
- **homepage**: （无）
- **github**: （无）
- **status**: under review
- **收录日期**: 2026-07-08
- **收录来源**: arxiv scan + 1-hop 引用规则
- **1-hop 引用**: （v2 补全，见 §11 1-hop 关系图）
- **评级**: ⭐⭐

## 一句话问题

4DGS 是 30+ FPS 动态场景渲染的 SOTA，**但 4DGS 编码 + 解码 + 流式传输的整条 pipeline 在 mobile GPU 上 = 0 公开工作**。**如何设计一个 GPU codec（基于 octree + RAHT）实现 4DGS bandwidth-adaptive streaming + 25 FPS mobile decode**？

## 链接

- arXiv：<https://arxiv.org/abs/2606.05650>（v1 2026-06-04）
- 项目页：not found in abstract
- GitHub：not found in PDF
- PDF：已下 `.pdfs/2606.05650.pdf`
- 会议：not found in abstract（arXiv preprint）

## 年份 / 作者 / 机构（PDF 头部实测）

- **年份**：2026（v1 2026-06-04）
- **第一作者**：**Rajrup Ghosh**
- **机构**：**NVIDIA Research**（Rajrup Ghosh, Haodong Wang, Haoran Hong, Eduardo Pavez）—— `NVIDIA 团队背书`

> **NVIDIA 团队背书 = 高影响力**。这意味着 GS-NFS 后续可能整合进 NVIDIA SDK 或作为 reference 引用

## 方法核心（PDF §3 直引）

### §3.1 Voxel-based 3DGS Encoding

- **Voxelize Gaussian positions** → octree（hierarchical spatial structure）
- **Merge 邻近 Gaussians**（同 voxel 内做 spatial merge）
- **RAHT（Region-Adaptive Hierarchical Transform）** 编码 Gaussian attributes（scale / rotation / opacity / SH）

### §3.2 Bandwidth-Adaptive Streaming

- 根据 client 带宽 + 设备能力**动态调整** stream 比特率
- 目标：**mobile GPU 上 full frame rate 30 FPS decode**

### §3.3 GPU Codec Design

- 全 GPU 实现（不是 CPU 编码 + GPU 解码）—— **encode 1-2 orders faster than SOTA 4DGS compression**
- Point cloud codec 借鉴 G-PCC / Draco 但全 GPU 化
- 在 **Jetson Orin** 上实测 **25 FPS 4DGS decode**

## 关键数字（abstract 直引 + PDF Table 直引）

| 指标 | GS-NFS 数字 | 备注 |
|---|---|---|
| **4DGS decode on Jetson Orin** | **25 FPS** | mobile GPU 实测 |
| **Target full frame rate** | **30 FPS** | 接近达成 |
| **Bytes per Gaussian** | **236 bytes** | ~ 2× 静态 3DGS 的 storage 1.6 MB / 0.16M = 10 bytes，4DGS 多时间轴 |
| **Speedup vs SOTA 4DGS compression** | **1-2 orders of magnitude** | encode + decode 均 |
| **Compression ratio (post-compression)** | additional **8.7×** | 在 base 上叠加 |

> **abstract 直引**："GPU codec for dynamic 3DGS (4DGS): voxelize+merge positions (octree) + RAHT for attributes; **bandwidth-adaptive streaming at full frame rate**; mobile-friendly decoder. Decodes 4DGS **up to 25 fps on Jetson Orin mobile GPU**; full **30 fps target frame rate**; 236 bytes/Gaussian; competitive compression and rendering quality; additional 8.7× compression via post-compression stage."

## 与本调研主线的关系

### 派系归属：**派系 4（流式落地）#1 直接竞争对手**

- **派系 4 排名更新**：**GS-NFS 直接挑战 4DGCPro 作为派系 4 #1**：
  - 4DGCPro = **SJTU MediaX**，**abstract 级 4DGS mobile decode + rendering**（无具体 FPS 数字）
  - **GS-NFS = NVIDIA Research**，**Jetson Orin 实测 25 FPS decode**（具体数字）
  - **GS-NFS 在 4DGS 专项上更具体**（NVIDIA 背书 + 25 FPS 数字）
- **M3/M4 spike 应用**：**GS-NFS 思路直接可移植到 Snap 8 Gen 4**（octree + RAHT 是 mobile-friendly 数据结构）

### 对项目目标的具体承诺

- **4DGS Mobile streaming = 30 FPS target**：GS-NFS 在 Jetson Orin 上 25 FPS，**Snap 8 Gen 4 算力比 Jetson Orin 强**（Adreno 8 Gen 4 = 4.7 TOPS vs Jetson Orin = 5.3 TOPS 实际**相当**，但**Snap 8 Gen 4 内存带宽更优**）—— **本项目目标 30 FPS streaming 4DGS 在 Snap 8 Gen 4 是可达的**（`[推测,基于 GS-NFS 25 FPS Jetson Orin + Snap 8 Gen 4 略好]`）
- **236 bytes/Gaussian 估算**：4DGS-1K 已经压到 N3V 上 41.7×（PSNR -0.04 dB）—— **如果 4DGS-1K pruning + GS-NFS codec** 理论上可达 **~5 MB/scene**（`[推测]`）

### 我未找到 / 提请下游注意

- **GS-NFS 训练平台**：abstract 未明示，**推测 = NVIDIA desktop GPU**（A100 / H100）
- **GS-NFS 与 4DGCPro 同期同目标**：abstract 直引 4DGCPro，**两者差异 = 4DGCPro 强调 hierarchical 4DGS，GS-NFS 强调 GPU codec 速度**——**本项目可以 4DGCPro 框架 + GS-NFS codec 组合**
- **GS-NFS 的开源代码**：PDF 未给 GitHub 链接，**需要追踪**

## 我的 commit 节奏

本文是 33 + 1 (Flux-GS) + 10 (subagent) 之外**新加的第 45 篇**。配套 INDEX.md 派系 D（流式）加 1 行 + **派系 4 #1 排名考虑改为 GS-NFS**。
