# 2026-hong-ploymerge · PolyMerge: Compressing 3D Gaussian Splats with Polytope Coverings for Provably Safe Resource-Constrained Navigation

> **相关性**：**⭐⭐⭐ 派系 3（移动端/edge）+ 派系 1（训练期压缩）双命中**（IEEE RA-L 2026，PDF 直引）—— 核心数字：**从 SaferSplat 626.7 MB → PolyMerge 39.4 MB @ Garden scene**（~16× 压缩）；**Crazyflie 无人机 on-board CBF real-time 路径规划**；abstract 直引"**runs on-board drone compute with severe onboard compute constraints**"；**5 polytope counts tested in hardware (10/30/50/100/150)** —— **唯一在本批 13 篇中明确"on-board drone"实测的 paper**。

> **⚠ 重要区分**：这是 **3DGS（静态）→ polytope 几何抽象**工作，**不是 4DGS**，**不是为了渲染**。**PolyMerge 目标不是渲染而是 collision avoidance** —— 把 3DGS 转成 **凸多面体覆盖**，用于 CBF-based safe navigation。**对本项目 4DGS mobile rendering 不直接命中渲染管线**，但其 **"3DGS → 紧凑几何抽象"** 思路对派系 1（训练期压缩）**有借鉴价值**。

## 0.5 元数据

- **venue**: arxiv pre-print (2026-05)
- **arxiv-id**: 2606.16232
- **s2-id**: （v2 用 Semantic Scholar API 补全）
- **homepage**: （无）
- **github**: （无）
- **status**: under review
- **收录日期**: 2026-07-08
- **收录来源**: arxiv scan + 1-hop 引用规则
- **1-hop 引用**: （v2 补全，见 §11 1-hop 关系图）
- **评级**: ⭐

## 一句话问题

3DGS radiance field 适合 photorealistic 重建，但 **memory-heavy（hundreds of thousands to millions Gaussians，MB-GB 级）**，**远超 mobile platforms**（"mobile platforms typically on the order of kilobytes for small drones such as Crazyflies"）—— abstract 直引。**如何在保持 provable obstacle over-approximation 的前提下，把 3DGS 模型压缩到 drone on-board 内存容量，且支持实时 CBF safe planning**？

## 链接

- arXiv：<https://arxiv.org/abs/2606.16232>（v1 2026-06-15，cs.RO）
- **项目页**：<https://athlon76.github.io/PolyMerge-website/>（PDF 第 1 页 abstract 直引）
- GitHub：项目页应有（abstract 直引"for our code and videos, visit https://athlon76.github.io/PolyMerge-website/"）
- PDF：已下 `.pdfs/2606.16232.pdf`（8 页）
- **会议**：**IEEE Robotics and Automation Letters（RA-L），Preprint version accepted April 2026**（PDF 第 1 页直引）

## 年份 / 作者 / 机构（PDF 头部实测）

- **年份**：2026（Preprint version accepted April 2026）
- **第一作者**：**Jihoon Hong¹**
- **其他作者**：Chih-Yuan Chiu¹, Sara Fridovich-Keil¹, **Glen Chou¹**
- **机构**（PDF 第 1 页 footnote 直引）：
  1. **Georgia Institute of Technology（佐治亚理工学院）**

## 方法核心（PDF §II + §III 直引）

### §II.A PolyMerge 三大阶段（PDF §I 直引 + Fig.1）

1. **Extract volumetric occupancy grid** —— 识别 input 3DGS scene 中所有 occupied regions
2. **Compute covering set of convex polytopes** —— **polytopes union 包含所有 occupied space**
3. **Iterative merging** —— **反复用 convex hull 替换一对 convex polytopes**（merging）

### §II.B CBF-based Safe Control（abstract + §I 直引）

- 集成 **Control Barrier Functions (CBFs)** 来 plan collision-free paths
- **Crazyflie drone microcontroller** 上 **实时** computing + following safe trajectories
- **Custom firmware**：CLF nominal controller + CBF safety filter

### §III Hardware & Compute Constraints（PDF §I 直引）

- "**on-board a Crazyflie drone with severe onboard compute constraints**"（abstract 直引）
- "**mobile platforms, typically on the order of kilobytes for small drones**"（PDF §I 直引）
- "outperforming baselines **in speed** while **guaranteeing safety**"（abstract 直引）

### 关键算法：覆盖 + 合并多面体（PDF §III 直引）

> "PolyMerge first extracts a volumetric occupancy grid to ensure all obstacles in the input scene are considered occupied. It then computes a covering set of convex polytopes which contains all occupied space. Finally, PolyMerge performs iterative merging by repeatedly replacing pairs of convex polytopes with their convex hull"（PDF §I 直引）

- **Provable over-approximation**：polytopes union ⊇ all obstacles（safety guarantee）
- **Polytope count tunes trade-off**：fewer polytopes = lower compute + more conservative navigation

## 关键数字（PDF Table I + Table II 直引）

### PDF Table I 直引 · Memory Comparison @ 9 Mip-NeRF 360 scenes

| 场景 | SaferSplat Size (MB) | SuGaR+CoACD Hulls | SuGaR+CoACD Size (MB) | **PolyMerge Hulls** | **PolyMerge Size (MB)** |
|---|---|---|---|---|---|
| Bicycle | 671.1 | 3,296 | 13.5 | 3,296 | 60.7 |
| Flowers | 692.0 | 2,624 | 10.6 | 2,624 | 49.8 |
| Garden | **718.7** | 1,006 | 4.2 | 1,006 | **20.1** |
| Stump | 659.8 | 2,458 | 10.7 | 2,458 | 67.3 |
| Treehill | 644.2 | 2,681 | 10.7 | 2,681 | 58.8 |
| Room | 473.6 | 454 | 1.8 | 454 | 8.5 |
| Counter | 640.3 | 1,367 | 5.6 | 1,367 | 10.6 |
| Kitchen | 612.5 | 901 | 3.8 | 901 | 17.4 |
| **Bonsai** | 626.7 | 2,080 | 8.5 | 2,080 | **39.4** |

> **关键比值**：
> - PolyMerge/Bonsai **39.4 MB vs SaferSplat 626.7 MB = 16× 压缩**
> - **但 PolyMerge vs SuGaR+CoACD 同 hull 数**：PolyMerge 占内存更大（"its polytopes are composed of **more half-planes**"，PDF 第 6 页直引）
> - "across all scenes, **up to 10× reduction** in memory footprint when convex polytopes, rather than ellipsoids, are stored"（PDF 第 6 页直引）

### PDF Table II 直引 · Hardware Drone Trajectory Statistics

| Number of Convex Hulls | 10 | 30 | 50 | 100 | 150 |
|---|---|---|---|---|---|
| Success Rate | 0.7 | 0.8 | **1.0** | 0.8 | 0.9 |
| Min Obstacle Distance | 0.268 | 0.253 | **0.098** | 0.117 | 0.097 |

> **关键观察**：50 hulls 给出 best balance（success 1.0 + min obstacle 0.098）；更多 hull = 更 tight（少 obstacle 距离）但 compute cost 增加

### abstract 直引
- "**runs on-board drone compute with severe onboard compute constraints**"
- "**outperforming baselines in speed while guaranteeing safety**"
- "memory and compute-intensive → prevents on-board deployment"（motivation）

## 与本调研主线的关系

### ⭐⭐⭐ 派系 3（移动端/edge）+ 派系 1（训练期压缩）— 双命中（最特殊的命中）

| 维度 | PolyMerge | Pocket-SLAM | GaussLite（4D 移动 SLAM） |
|---|---|---|---|
| 4D 适配 | ❌ static polytope | ❌（但 SLAM）| ❌（但 4 Hz real-time）|
| **移动 GPU 实测** | ✅ **Crazyflie drone** | ✅ drones/AV | ✅ resource-constrained robot |
| 压缩比 | **~10-16×**（3DGS → polytope）| 61.3% peak memory | ≤1M Gaussian budget |
| 实时性 | ✅ CBF real-time | ❌（SLAM only） | ✅ 4 Hz |
| 路径规划 | ✅ **drone + safety filter** | ❌ | ❌ |

### 对项目目标的具体承诺 / 不可承诺

- **承诺 1（强，路径不同）**：**"3DGS → 紧凑几何抽象"路径** 已经成功在 **Crazyflie ~kB memory** 上部署 —— **证明 3DGS 派生 representation 在 on-board drone 上可行**，**间接为本项目 M4 端侧 4DGS 部署背书**
- **承诺 2（强）**：**Polytope + CBF safety filter** 思路对 **4DGS 移动端 + 移动机器人 perception path** 有方法学价值：`[推测]` 本项目调研边缘端不只"渲染 viewer"还应包括 "**on-board 避障 / SLAM**"
- **不可承诺 1**：**PolyMerge 不做渲染**，**对本项目 4DGS rendering pipeline 无直接加速贡献**
- **不可承诺 2**：**测试平台 Crazyflie microcontroller（极低算力）** ≠ **Snap 8 Gen 4（手机 GPU）** —— 不可直接外推到 mobile phone GPU 目标
- **不可承诺 3**：**3DGS 静态 polytope abstraction ≠ 4DGS canonical-space Gaussians**

### ⭐ 派系 2（动静态分离）/ 派系 4（流式）
- **不直接命中**

## 我未找到 / 提请下游注意

- **CBF planning 频率（control loop Hz）**：PDF 提"configure the drone to run the controller at different time-step frequencies for different values of n"，**未直接 Hz 数字**
- **Memory 实时分配 / Polytope 选择算法**：PDF §III 提 cover selection，未给具体选择算法公式
- **GPU 类型**：**无 GPU**（Crazyflie microcontroller）—— **完全 CPU-based, real-time**
- **PSNR 渲染质量**：PolyMerge 不渲染，**无 PSNR 数字**
- **4DGS 适配**：未做 4DGS polytope abstraction 实验
- **Crazyflie model / EKF / Vicon motion-capture setup**：详细配置需 PDF §V.A 完整核

[abstract 直引] [PDF §I-III 直引] [PDF Table I 直引] [PDF Table II 直引] [推测] [调研深度：PDF §I-§III + Page 6-8 Table I/II]
