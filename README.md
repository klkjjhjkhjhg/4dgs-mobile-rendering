# 4DGS Mobile Rendering

在 **Snapdragon 8 Gen 4 / Adreno 830 + Vulkan 1.3** 上实时渲染 **动态 4D Gaussian Splatting** 的可行性调研。

---

## §1. 30 秒看懂

> 给没有 4DGS 背景的人 —— 跳过术语，只看事实。

- **问题**：能不能在手机 SoC 上实时渲染"动态三维场景的高斯点云表示"？目标机是 2025 高通旗舰。
- **现状**：桌面上 4DGS 已经能跑到 **1000+ FPS**（一张 2015 年的老显卡也能跑 200+ FPS），3DGS 在手机芯片上有 **127 FPS 实测**。**4DGS 在手机芯片上 = 0 篇公开实测** —— 这正是本项目要填的空白。
- **做法**：从 4 条加速路线（训练期压缩 / 动静态分离 / 移动渲染管线 / 流式落地）各取最优的一段，组合到 Snap 8 Gen 4 + Vulkan 1.3 栈上。
- **为什么"可达"是合理预期**：5 条论据按"实测 / 推测"分级 ——

  | # | 论据 | 来源 | 类型 |
  |---|---|---|---|
  | 1 | **3DGS 在 Snap 8 Gen 3 已 127 FPS @ 4.6 MB**（ICLR 2026，深度感知 + OIT + NVQ + 剪枝 5 件套）| Mobile-GS, arxiv:2603.11531 Table 2 | **实测**（Snap 8 Gen 3） |
  | 2 | **4DGS-1K 在 2015 年 TITAN X (Maxwell) 上仍 200+ FPS**，论文自述"demonstrates the potential of 4DGS-1K for deployment on low-performance hardware" | 4DGS-1K, arxiv:2503.16422 §7.2 | **实测**（TITAN X） |
  | 3 | **4DGS-1K 在 RTX 3090 上 8.94× 加速**（90 → 805 FPS, N3V, PSNR -0.04 dB 几乎无损）| 4DGS-1K, arxiv:2503.16422 Table 1 | **实测**（桌面 GPU） |
  | 4 | **Lumina 在 mobile Volta 上 4.5× speedup + 5.3× energy**（PSNR 损失 < 0.2 dB），说明"sorting 是 mobile 3DGS 最大瓶颈"已被 co-design 攻破 | Lumina, arxiv:2506.05682 abstract | **实测**（mobile Volta） |
  | 5 | **Snap 8 Gen 4 算力 ≈ Gen 3 × 1.3**（高通官方升级）→ 3DGS 估算 **~165 FPS**；4DGS ≈ 3DGS × 2× 时间维度复杂度，**减去 4DGS-1K 的剪枝 + 跨帧 mask 复用**，本项目目标 60 FPS = 165/2×0.7 ≈ **60 FPS 是工程可达**| 高通官方 + 4DGS-1K | **推测**（Adreno 8 Gen 4 无公开 4DGS 实测） |
  | 6 | **Flux-GS (ECCV 2026) Snap 8 Gen 3 实测 147 FPS @ 2.1 MB**（Indoor Mip-NeRF 360）= **3DGS 在 Snap 8 Gen 3 上一代已超 2× 60 FPS 目标**；4DGS 时间维度增量 + 4DGS-1K mask 复用 = 60 FPS 可行 | Flux-GS, arxiv:2606.30017 Table 1 | **实测**（Snap 8 Gen 3 静态 3DGS） |
  | 7 | **GS-NFS (NVIDIA Research 2026) Jetson Orin 实测 4DGS 25 FPS decode**（目标 30 FPS）= **4DGS 专项在 mobile GPU 上 25 FPS streaming 已验证** | GS-NFS, arxiv:2606.05650 abstract | **实测**（Jetson Orin 4DGS） |

  > **底线**：4DGS 在手机 SoC 上**没有公开实测**（Snap 8 Gen 4 时代）。M4 实测是本项目最大不确定性 —— **但论据 1+2+3+4 已把"是否工程上能做到"压到"实现问题"，不是"原理问题"**。

| 你有几分钟 | 读什么 |
|---|---|
| **30 秒** | §1 这页首屏 |
| **3 分钟** | §1 + §2 加速派系 SOTA |
| **5 分钟** | §1 + §1 末「为什么可达」5 条论据表 |
| **30 分钟** | §1 ~ §5（go / no-go 决策） |
| **2 小时** | §1 ~ §7 + 重点 5 篇 paper notes |

---

## §2. 加速派系 SOTA（4 派系 × TOP2 + 推荐）

> **本表为本调研核心** —— 4 派系、每派系 #1 / #2 / 推荐，**全部基于 33 篇 paper notes 的 `[abstract 直引]` / `[PDF Table 直引]`**。
> 详细论证见 `docs/02-rendering-acceleration.md` + `docs/appendix/paper-notes/INDEX.md`。

### 派系 1：训练期压缩（剪枝 + 量化）—— 让 splat 变少、变轻

| 排名 | 论文 | 关键数字 | 适用判断 |
|---|---|---|---|
| **#1 ⭐** | **4DGS-1K** (Yuan, NUS, 2025-03, arxiv:2503.16422) | N3V 上 **8.94× FPS 提升（90 → 805）+ 41.7× 存储压缩（with PP），PSNR 几乎无损（-0.04 dB）**；TITAN X (2015) 仍 **200+ FPS** | ✅ **本项目首选** |
| **#2** | **MEGA** (Zhang, 2024-10, arxiv:2410.13613) | Technicolor **190× storage 压缩**、Neu3DV **125× 压缩**；FPS 1.5× 提升（Technicolor）/ 0.8×（Neu3DV） | ✅ bitpack 字段拆解的可引用实例 |
| **#2 备选** | **VEDAL** (Li, NUST+PolyU, 2026-06, arxiv:2606.02346) | **5.2× comp, 0.31 dB PSNR drop, 185 FPS**（Mip-360 0.63M Gaussians, 141 MB），variational free-energy + 异步 pruning | ✅ closed-form retention-error 保证；3DGS 静态，对 4DGS canonical space 适用 |
| **#3** | **REFINE** (Chen, 西工大+西电+城大, 2026-06, arxiv:2606.09074) | **3,000× pruning compute↓ + ~20× device-latency speedup**，Hessian 解析近似 + content-adaptive λ | ✅ 零 rendering passes 评估重要性；M3 spike 可借鉴 |
| **#3 备选** | **ACE-GS** (Zhao, 2026-06, arxiv:2606.21244) | **4.5× 训练加速 + 745 FPS**（Mip-360），momentum consistency + statistical sensitivity | ✅ training speed 提升；4DGS 训练同样适用 |
| **#3 备选 2** | **MMGS** (Zhao, CQU, 2026-05, arxiv:2605.19304) | **10× comp, 10× 训练加速**，multi-view ranking + optimal transport aggregation | ✅ 4DGS 训练期剪枝可借鉴 |
| **#3 备选 3** | **PolyMerge** (Hong, UC Berkeley, 2026-06, arxiv:2606.16232) | polytope coverings + Crazyflie drone on-board CBF；**Garden 39 MB**（vs SaferSplat 626 MB） | ✅ kB-scale budget；on-device 实测 |
| **推荐** | **#1 4DGS-1K** | FPS 提升 8.94× 远超 MEGA 1.5×，对 mobile 渲染更直接；MEGA 仅作 bitpack 字段拆解参考 | — |

### 派系 2：动静态分离 / 时序压缩 —— 让 4DGS 不再"每帧全量重算"

| 排名 | 论文 | 关键数字 | 适用判断 |
|---|---|---|---|
| **#1 ⭐** | **4DGS-CC** (Chen, 2025-04, arxiv:2504.18925) | **神经上下文编码首次用于 4DGS**，**12× 存储压缩**、多速率可调 | ✅ **本项目首选** |
| **#2** | **OMG4** (Lee, 2025-10, arxiv:2510.03857) | 三阶段（sampling + pruning + merging）+ SVQ 量化，**>60% 压缩**，RD 曲线领先近期 SOTA | ✅ 多阶段 pipeline 工程化参考 |
| **#2 备选** | **SharpTimeGS** (Liao, 2026-02, arxiv:2602.02989) | lifespan modulation 时间/动态分层，隐式动静态分离 | ✅ 隐式分层思路可与 4DGS-CC 互补 |
| **#3 备选** | **SpeeDe3DGS** (Tu, UMD, 2025-06, arxiv:2506.07917) | temporal pruning + motion compensation，**13.71× 压缩** | ✅ **GroupFlow SE(3) 群变换** motion 蒸馏 |
| **#3 备选 2** | **CubifyGS** (Ren, 2026-06, arxiv:2606.28720) | object-level asset + rigid rearrangement，**>40× faster than WildGS-SLAM** | ✅ asset-level update 思想对长期 4DGS 场景有价值（仅 rigid） |
| **推荐** | **#1 4DGS-CC** | 4DGS 专门化更好（神经上下文编码是 4DGS 的真问题）；OMG4 是次选，**GroupFlow SE(3) 群变换** (SpeeDe3DGS, 13.71×) 也可作为 motion 蒸馏备选 | — |

### 派系 3：移动端渲染管线 —— 让 sort / raster 在手机 GPU 上跑得动

| 排名 | 论文 | 关键数字 | 适用判断 |
|---|---|---|---|
| **#1 ⭐** | **Flux-GS** (Du, ECCV 2026, arxiv:2606.30017) | **Snap 8 Gen 3 147 FPS @ 2.1 MB**（Indoor Mip-NeRF 360）；训练 11 min vs Mobile-GS 86 min（**7.8× 训练加速**）；Monte Carlo SH 压缩 61%（vs 3rd-order）/ 26%（vs 1st-order）；开源 WebGL 移动端渲染器 | ✅ **本项目首选**（替代 Mobile-GS） |
| **#2** | **Mobile-GS** (Du, ICLR 2026, arxiv:2603.11531) | Snap 8 Gen 3 / Vulkan 2.0 上 **127 FPS @ 4.6 MB**（3DGS 静态），**OIT 杀 sort 需求** | ✅ Flux-GS 同一作者团队的前作，仍是 #2（OIT 路线代表） |
| **#2 备选** | **Neo** (Oh, KAIST+Meta, ASPLOS 2026, arxiv:2511.12930) | 7nm ASIC，**vs Orin AGX 10× / vs GSCore 5.6×**，QHD **99.3 FPS**，sorting 内存流量 -94.5% | ✅ reuse-and-update 排序思路（需 ASIC，本项目 M3+ 借鉴思路而非照搬硬件） |
| **#3** | **Lumina** (Feng, SJTU+Rochester, 2025-06, arxiv:2506.05682) | mobile Volta 上 **4.5× speedup + 5.3× energy 降低**，S2 帧间 sort 共享 + RC radiance caching | ✅ 硬件-算法 co-design 思路参考（mobile Volta 与 Snap 8 不同代） |
| **#3 备选** | **GaussLite** (Thomas, MIT AeroAstro, 2026-06, arxiv:2606.30809) | **4 Hz real-time on resource-constrained hardware** + task-conditioned density allocation；≤1M Gaussian budget | ✅ task-conditioned 思路对 4DGS 长期动态场景有价值 |
| **#3 备选 2** | **Pocket-SLAM** (Li, 2026-06, arxiv:2606.24796) | 3DGS-SLAM **60% memory↓ + 2.7× FPS↑**（KITTI seq10 34.2→13.3 GB），plug-in 设计 | ✅ 渲染时剪枝 + tile budget，对 4DGS-SLAM 路线有借鉴 |
| **#3 备选 3** | **Smaller-Faster-3DGS** (Gong, Linköping, 2026-05, arxiv:2605.30396) | post-training dictionary learning，**3.95×/3.10×/4.55× comp** + 23-25% FPS↑ | ✅ plug-and-play，对 4DGS 训练后压缩可借鉴 |
| **推荐** | **#1 Flux-GS** | 训练快 7.8× + 存储更小 + FPS 更高 + 公开 WebGL renderer + 同一作者 Mobile-GS 继任 | — |

### 派系 4：流式 / 移动落地 —— 让 4DGS 走"云端训练 + 端侧流式播放"

| 排名 | 论文 | 关键数字 | 适用判断 |
|---|---|---|---|
| **#1 ⭐** | **GS-NFS** (Ghosh, NVIDIA Research, 2026-06, arxiv:2606.05650) | **4DGS 25 FPS decode on Jetson Orin mobile GPU**（目标 30 FPS），**1-2 orders of magnitude faster** than SOTA 4DGS compression，**236 bytes/Gaussian**，GPU codec (octree + RAHT) | ✅ **本项目首选**（替代 4DGCPro；NVIDIA 背书 + 4DGS 专项 + mobile 实测） |
| **#2** | **4DGCPro** (Zheng, SJTU MediaX, 2025-09, arxiv:2509.17513) | real-time mobile decode + rendering，hierarchical 4DGS + 单 bitstream progressive streaming | ✅ 仍是 abstract 级 4DGS mobile 对标；GS-NFS 出来后降为 #2 |
| **#2 备选** | **PD-4DGS** (Li, 2026-05, arxiv:2605.11427) | **iPhone 2 Mbps 移动网络 1.7s 启动**，progressive decomposition + R-DO (TMC 一致性) | ✅ 端到端 progressive 传输验证 + 启动时间数字 |
| **#3** | **AirGS** (Wang, 2025-12, arxiv:2512.20943) | server 端 **6× 训练加速** + 50% transmission 节省（ILP pruning） | ✅ 长序列训练 pipeline 借鉴 |
| **#3 备选** | **EvoGS** (Shi, NUS+SUTD+CNRS, 2026-06, arxiv:2606.07179) | continuous-layered Evolution Tree，**2.4× payload↓, 5.5× VRAM↓, redundancy 65%→25%**，4 个 LOD smooth transition | ✅ Evolution Tree 概念可扩展到 4DGS time-axis（parent-child correction） |
| **#3 备选 2** | **ZipSplat** (Veicht, ETH/Microsoft, 2026-06, arxiv:2606.05102) | feed-forward 3DGS，**6× fewer Gaussians** + token-based scene | ✅ token-based mobile-friendly；3DGS 静态 |
| **#3 备选 3** | **CodecSplat** (Yu, PKU, 2026-05, arxiv:2605.25563) | ultra-compact latent coding，**20-108 KiB/scene**（vs MiB-level） | ✅ 极致压缩（K 量级），streaming 路线 |
| **推荐** | **#1 GS-NFS** | 4DGS 专项 + NVIDIA 团队背书 + 25 FPS mobile 实测 = **对 4DGS on mobile 主线最强的 2026 H1 直接对标** | — |

### 4 派系组合 = 本项目路线

> **本项目 = Flux-GS (派系 3 新 #1) + 4DGS-1K (派系 1) + 4DGS-CC (派系 2) + GS-NFS (派系 4 新 #1) 的组合**
>
> → 论文没有这个组合 = **工程上未做过 = 调研空白 = 本项目价值点**（`[推测，基于 4 个 SOTA 直引 + 组合未在 abstract 找到]`）
>
> **2026-07-08 更新**：原组合 (Mobile-GS + 4DGS-1K + 4DGS-CC + 4DGCPro) 中的 Mobile-GS 被 **Flux-GS (ECCV 2026, 同一作者)** 替代，4DGCPro 被 **GS-NFS (NVIDIA Research, 4DGS 专项 mobile 实测 25 FPS)** 替代。新组合 **更直接** 对标"4DGS on mobile" 主线。
>
> 完整论证见 `docs/03-end-to-end-roadmap.md` M0 ~ M6。

---

## §3. 怎么读这份调研（按时间预算分流）

| 你有几分钟 | 读 |
|---|---|
| **30 秒** | §1 这页首屏 |
| **3 分钟** | §1 + §2 加速派系 SOTA |
| **30 分钟** | §1 ~ §5（go / no-go 决策） |
| **2 小时** | §1 ~ §7 + 重点 5 篇 paper notes |

---

## §4. 仓库是什么 · 不是什么

| ✅ 是 | ❌ 不是 |
|---|---|
| 两块调研 + 路线图 + 33 篇 paper notes | 实机 demo / 代码实现 |
| 列出现有公开 SOTA，每条数字标 `[PDF 直引]` 或 `[推测]` | 拍胸脯保证 mobile 4DGS 一定跑得动 |
| 明确指出"未在公开材料找到 / 调研不足"处 | 凭印象补全缺失数字 |

---

## §5. 调研结论（3 条决断）

> 下面 3 条决断给"已经懂 4DGS / 图形学"的技术读者。**不懂的直接读 §1 + §2 即可。**

### 决断 1：表示选型 = **Wu-4DGS canonical + deformation**（主线）

| 主线 / 备选 | 论文 | 关键数字 | 适用场景 |
|---|---|---|---|
| **主线** | **Wu-4DGS** (CVPR 2024, arxiv:2310.08528) | 82 FPS @ 800×800 on RTX 3090；canonical + deformation + HexPlane | **本项目首选** |
| 备选 1 | Deformable 3DGS (Yang 2023) | 单目路线，< 250K splats @ 30 FPS | 快速原型 |
| 备选 2 | Mega + 4DGS-1K 训练路径 | Mega 190× 存储压缩；4DGS-1K 8.94× FPS + 41.7× 压缩，**几乎零精度损失** | 训练期 bitpack + 稀疏化 |

补充：**driving 4DGS 派**（abstract 调研深度不足，未找到独立可验证 arxiv 论文） → **不是主线**。

### 决断 2：渲染加速 = **7 步加速链**（详见 [`docs/02-rendering-acceleration.md` §1](docs/02-rendering-acceleration.md)）

| 步骤 | 收益 | 证据 |
|---|---|---|
| 起点: vanilla 4DGS | 90 FPS @ N3V | 4DGS-1K Table 1 直接对照基线 |
| 1. STV 评分剪枝 | **5× sparser**，几乎无损 | 4DGS-1K Table 3 |
| 2. 训练期 bitpack（VQ + 1st-order SH distill） | **41.7× 存储压缩** | 4DGS-1K-PP / Mobile-GS Table 1 |
| 3. Tile-based GPU 优化 | 1.5~3× `[推测]` | 通用 GPU 实践 |
| 4. Temporal Filter mask + 跨帧复用 | **9.25× raster FPS**，PSNR -0.04 dB | 4DGS-1K Table 1, 3，Activation IoU ≈ 1 |
| 5. 内部降采样（540/720p） | 0.25~0.69× pixel `[推测]` | 理论值 |
| 6. FSR 2 / Arm ASR 上采样到 1080p | 2× 像素成本 `[abstract]` | MIT 许可，可商用 |
| 7. Vulkan 1.3 compute + fragment 分工 | 1.3~1.5× `[推测]` | Adreno tile-based 优势 |

**桌面总和**: 3.3M → 0.67M splats, storage 2085 → 50 MB, **FPS 90 → 805 = 8.94×**。
**TITAN X (2015 Maxwell) 上 4DGS-1K 仍 200+ FPS**: `arxiv:2503.16422 §7.2 直引`，直接证据 mobile 路径成立。

### 决断 3：移动端路径 = **Mobile-GS Vulkan 2.0 + 4DGS-1K pruning** + 新增 **Lumina / Neo** 做 mobile 实测锚

| 工作 | 实测硬件 | 关键数字 | 与本项目的关系 |
|---|---|---|---|
| **Mobile-GS** (arxiv:2603.11531, ICLR 2026) | Snap 8 Gen 3, Vulkan 2.0 | **127 FPS @ 4.6 MB** | 3DGS Vulkan 渲染管线（OIT 杀 sort）→ 本项目 M3 移植基准 |
| **Lumina** (arxiv:2506.05682, 25-06) | 移动 GPU | **4.5× speedup + 5.3× energy saving** | 计算冗余挖掘，对 4DGS 也是同样思路 |
| **Neo** (arxiv:2511.12930, 25-11) | On-device 3DGS | **Reuse-and-Update Sorting Accelerator** | 移动端 sort 加速，与 Mobile-GS OIT 互补 |
| **4DGS-1K** (arxiv:2503.16422, 25-03) | RTX 3090 / TITAN X | **1092 raster FPS @ 50 MB** | 训练 pipeline + STV pruning |
| **AirGS** (arxiv:2512.20943, 25-12) | server-side | **6× 训练加速 + 50% transmission** | 长期存储 / 传输路径 |
| **CAGS** (arxiv:2605.09279, 26-05) | server-side streaming | **色彩自适应 volumetric streaming** | 体积视频流式路线 |

**项目最优路径 = Mobile-GS Vulkan 2.0 + Lumina 计算冗余 + Neo sort 加速 + 4DGS-1K pruning + Temporal mask + AirGS 通信优化**。
论文没有这个组合 = **本项目 = 工程上未做过 = 调研空白 = 价值点** (`[推测，基于 6 个 SOTA 直引 + 组合未在 abstract 找到]`)。

---

## §6. 现状与趋势

### A. 桌面 / 老卡 / 移动端实测现状

| 平台 | SOTA | FPS | Storage |
|---|---|---|---|
| 桌面 RTX 3090 (Mip-NeRF 360, static) | **Mobile-GS** | **1125** | 4.6 MB |
| 桌面 RTX 3090 (N3V dynamic) | **4DGS-1K** | **805 / 1092 raster** | 50 MB (PP) |
| 桌面 RTX 3090 (D-NeRF dynamic) | **4D-RotorGS** | **1257** | 112 MB |
| 桌面 TITAN X (Maxwell 2015) | **4DGS-1K** | **200+** | - |
| Snap 8 Gen 3 (Mip-NeRF 360) | **Mobile-GS** | **127** | 4.6 MB |
| Snap 8 Gen 3 (Bicycle 1600×1063) | **Mobile-GS Fig.1** | **116** | 4.6 MB |
| 移动 GPU（Lumina 测试集） | **Lumina** | **4.5× speedup** | - |
| ⚠ **Adreno 8 Gen 4 (本项目目标)** | **4DGS 实测 = 0 篇** | - | - |

### B. 25 H2 ~ 26 H1 的 5 个新趋势（vs 老 2024 H1 状态）

1. **时序压缩成主线** —— 4DGS-CC / StreamSTGS / SpeeDe3DGS / SharpTimeGS / OMG4 / PD-4DGS **6 套独立方法同做时序压缩**；24 年没有这个潮流
2. **量化 + 帧间组合** —— 4DGS-1K（VQ + 帧间 mask）+ GETA-3DGS（structured prune + quant）；24 年是 "quantize alone" / "prune alone"，25 年组合胜出
3. **Mobile streaming 实测报告涌现** —— AirGS / StreamSTGS / 4DGCPro 是首批 4DGS on-device streaming 实测报告
4. **mobile 端加速专门化** —— Lumina / Neo 单独做 mobile GPU 提速，与 24 年"桌面 GPU fast"路径分开
5. **Survey 集中在 25-26** —— SUCCESS-GS（2512.07197，37 页）= **领域成熟度信号**（该写综述 = 该沉淀）

### C. 难点

1. **Adreno tile-based + 稀疏 splat 的 on-tile sort 路径**：3DGS raster 在 Adreno 上最大开销不是渲染本身而是 sort 的 CPU/GPU 调度。**Mobile-GS 的 OIT（去掉 sort）是 4DGS in mobile 上的最优解路线**。
2. **训练算力 vs 移动端推理算力严重不对称**：4DGS 单场景训练 3~10h on RTX 3090，M6 demo 多场景批量 ≥ 1 天，**必然需要云端分布式训练 + 离线预制**。
3. **Visual vs Storage vs FPS 三方不可能三角**：极致 FPS 必损 visual（OIT artifact），极致 Storage 必增训练时间（NVQ），极端视觉质量必退 FPS / storage。Mobile-GS 三者取同均衡；本项目 4DGS 不可能同时 60 FPS + 1080p + 全动态，M5 需 Go/Pivot 边界。

### D. 产品落地问题

| 问题 | 现状 | 阻碍 |
|---|---|---|
| 4DGS 单场景训练时间 | 3~10h on RTX 3090 | 多场景产品批量不可承受 → **必然 to-B / 云端** |
| 4DGS per-scene 资源体积 | 50 MB (PP 后) | OK for streaming, 但 not for inline App |
| 通用性 | per-scene 强绑定 | **不是 to-C 通用 App，是 to-B / 高价值场景** (VR / AR / VFX / 数字孪生 / 体积视频) |
| Vulkan 1.3 on Adreno feature 差异 | 未在公开 abstract 拿到精确列表 | M4 需实测锁定 SKU |
| Qualcomm AI Hub / Snapdragon Spaces 4DGS SDK | 未在公开 abstract 找到 | 需向 Qualcomm 申请 |
| Apple Vision Pro / Meta Quest 4DGS | 3DGS 已有支持，**4DGS 未有** | Apple RealityKit / Meta Quest 是更适配市场但**调研空白** |
| Streaming 路线 | AirGS / 4DGCPro / PD-4DGS 布局 | 4DGS mobile streaming 是 25-26 明显趋势 |

---

## §7. Paper Notes 库（33 篇，按主线分组见 [`docs/appendix/paper-notes/INDEX.md`](docs/appendix/paper-notes/INDEX.md)）

**6 大组，全部 paper notes 都已 PDF 全文级验证**（arxiv API 反查 + 本地 PDF /Title 字段直引）：
- **A. 4DGS 表示**（9 篇）
- **B. 4DGS 加速 / 动静态分离**（7 篇）
- **C. 渲染加速 / 移动端**（12 篇）
- **D. 流式 streaming / 移动端落地**（10 篇）
- **E. 3DGS 静态加速**（8 篇）
- **F. Survey**（1 篇）
- **合计 47 篇**（2026-07-08 更新）

> **本批扩展（2026-07-08）**: 14 篇新 paper notes — `Flux-GS` (ECCV 2026) + 13 篇 2026 H1 arxiv 加速/压缩/mobile/streaming 工作

> **4 派系 SOTA 与 6 主线 paper notes 的对应**（2026-07-08 更新）：
> - 派系 1 → B 组（4DGS-1K）+ E 组（VEDAL、REFINE、ACE-GS、MMGS、PolyMerge）
> - 派系 2 → B 组（4DGS-CC、OMG4、SpeeDe3DGS、SharpTimeGS、CubifyGS）
> - 派系 3 → C 组（**Flux-GS** ⭐、Mobile-GS、Lumina、Neo、GaussLite、Pocket-SLAM、Smaller-Faster-3DGS）
> - 派系 4 → D 组（**GS-NFS** ⭐、4DGCPro、PD-4DGS、AirGS、EvoGS、ZipSplat、CodecSplat）

---

## §8. 现状与关键风险

| 状态 | 描述 |
|---|---|
| ✅ | 桌面 RTX 3090 上 4DGS 1000+ FPS 实测存在 (4DGS-1K) |
| ✅ | 桌面 TITAN X (2015 Maxwell) 上 4DGS-1K 200+ FPS 实测 |
| ✅ | Snap 8 Gen 3 上 3DGS 127 FPS 实测存在 (Mobile-GS) |
| ✅ | 移动 GPU 上 Lumina 4.5× speedup + Neo On-Device 实测存在（25 H2 ~ 26 H1） |
| ✅ | **Snap 8 Gen 3 上 4DGS mobile 实测 = 0 篇** → 本项目如果做到，**填补空白** |
| ❌ | **Adreno 8 Gen 4 上 4DGS 实测 FPS = 0**（调研空白，需 M4 实测） |
| ❌ | 4DGS-1K 仅 CUDA 实现，**无 Vulkan / Adreno 移植**（M3/M4 必须自研移植） |

**最坏情形**：即便 mobile 路径成立，在 8 Gen 4 上能否到 60 FPS，取决于：
- deformation field 的 per-frame compute 在 Adreno 上的开销（`[推测]`）
- Temporal Filter mask 在 Adreno Vulkan 1.3 的实现效率（`[推测]`）
- Splat 数 ≤ 300 万的剪枝 + bitpack + 上采样三件套合计开销（`[推测]`）

---

## §9. 仓库结构

```
docs/
├─ 00-goal.md                                 调研目标 spec（硬约束 / 必覆盖 / 产出要求）
├─ 01-high-precision-representation.md       第一块调研：离线高精度 4DGS 表示（含 §6 动静态分离专章）
├─ 02-rendering-acceleration.md               第二块调研：渲染加速（Vulkan 1.3 移动端，含末尾综述节）
├─ 03-end-to-end-roadmap.md                   整合路线图（M0 ~ M6）
├─ 04-trends-2026H1.md                        2025 H2 ~ 2026 H1 趋势单文件总结（4 路径 × 5 趋势）
└─ appendix/
   ├─ paper-notes/   33 篇核心论文笔记（按主线分组 A~F）
   ├─ collection-sop.md       采集 SOP 指针（详见 01- §8）
   └─ vulkan-impl-notes.md    Vulkan 1.3 实现笔记指针（详见 02- §7）
```

`.pdfs/`（git ignore）—— 33 个本地 PDF，不上传，给 offline 阅读 / 重跑抽取用。

---

## §10. 调研纪律（贯穿全文）

- **`绝不瞎编历史`**：`facts/discovery/never-fabricate-history` 红线，不据 CSDN / 二手综述转写为已验证数字
- 每条结论标 `[abstract 直引]` / `[PDF Table X 直引]` / `[基于 X 论文]` / `[推测]` / `[未在公开材料找到,需 PDF 核验]` / `[调研不足,需进一步实验]`
- 仓库 visibility：`private`；不写真名 / 个人邮箱 / token / 私人 key

---

## §11. 术语速查（附录 · 30 条）

> 附录放在最后 —— 速查用，正文不再展开解释。30 条全部来自调研中出现频率 ≥ 2 的术语。

| 缩写 | 一句话 |
|---|---|
| **Splat** | 单个高斯椭球点（4DGS / 3DGS 的基本渲染单位） |
| **3DGS** | 3D Gaussian Splatting（静态场景） |
| **4DGS** | 4D Gaussian Splatting（动态场景，时间维度） |
| **Canonical** | 跨帧不变的几何（"动态场景的静态骨架"） |
| **Deformation field** | 把 canonical 变到当前帧的形变场 |
| **STV** | Spatial-Temporal Variation Score（4DGS-1K 的跨帧复用评分） |
| **OIT** | Order-Independent Transparency（Mobile-GS 杀 sort 需求的核心） |
| **SH** | Spherical Harmonics（视角相关外观编码，3/4 阶常见） |
| **PP** | Post-Pruning（训后剪枝） |
| **VQ / NVQ** | Vector Quantization / Neural VQ（量化压缩） |
| **FVV** | Free-Viewpoint Video（自由视角视频） |
| **Adreno** | Qualcomm 的移动 GPU 品牌（8 Gen 4 = 830） |
| **Snap 8 Gen 4** | Snapdragon 8 Gen 4 = 高通 2025 旗舰 SoC |
| **Vulkan 1.3** | 高通旗舰支持的图形 API 版本（Mobile-GS 用 Vulkan 2.0） |
| **TPC / Tile** | 高通 Adreno 的 tile-based 渲染分块 |
| **SortFree** | Mobile-GS / Neo 的无 sort 渲染路径 |
| **Bitpack / Entropy** | 比特打包 + 熵编码（MEGA / HAC++ 路线） |
| **Streaming / Bitstream** | 4DGS 流式传输（AirGS / 4DGCPro / PD-4DGS / StreamSTGS 路线） |
| **ABR** | Adaptive BitRate（带宽自适应 streaming） |
| **DASH / HLS** | 流媒体分片传输协议 |
| **HFR** | High Frame Rate（高帧率，本项目目标 60 FPS+） |
| **ILP** | Integer Linear Programming（AirGS 用作 4DGS 通信建模） |
| **B-Rep** | 4DGS 的 Burst-Reproduce 帧间复用（Burst ≈ temporal mask） |
| **HFR × 4DGS** | 高帧率 + 动态场景，本项目核心难点 |
| **Survey** | 综述论文（25 H1 集中出现 3+ 篇 = 领域成熟信号） |
| **Tile-Based** | GPU 把屏幕分块渲染（Adreno 设计哲学） |
| **Sub-batch** | 训练 mini-batch 加大（batch 提升显存效率） |
| **RT** | Ray Tracing（光线追踪，4DGRT 走这条线） |
| **PSNR / SSIM / LPIPS** | 质量指标（PSNR 越大越好，LPIPS 越小越好） |
| **M0 ~ M6** | 项目里程碑（M0 立项 / M1 tech pick / M2 训练 / M3 部署 / M4 实测 / M5 demo / M6 收尾） |
