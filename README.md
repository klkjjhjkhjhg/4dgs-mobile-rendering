# 4DGS Mobile Rendering

在 **Snapdragon 8 Gen 4 / Adreno 830 + Vulkan 1.3** 上实时渲染 **动态 4D Gaussian Splatting** 的可行性调研。

---

## 一句话定位

> 4DGS 在桌面 RTX 3090 已有 **1000+ FPS** 实测 (arxiv:2503.16422, NUS 2025-03)。
> 在 **Snapdragon 8 Gen 3** 的 3DGS 已有 **127 FPS** 实测 (arxiv:2603.11531, ICLR 2026)。
> 25 H2 ~ 26 H1 新增 **4DGS 加速 mobile 落地工作** (Lumina / Neo / AirGS / StreamSTGS / CAGS),**首次有 mobile-side 实测证据**。
> **Adreno 8 Gen 4 上 4DGS @ 1080p / 60 FPS 应可达** (`[推测,基于上述 4 个 SOTA 锚点 + 推算]`)。
> 详细风险与 baseline 见 `docs/04-trends-2026H1.md`。

---

## 怎么读这份调研（按时间预算分流）

| 你有几分钟 | 读 |
|---|---|
| **30 秒** | 这页首屏（上面"一句话定位"） |
| **3 分钟** | 本文档 §"现状与趋势表格" + §"产品落地问题"（足以下判断 go/no-go） |
| **30 分钟** | 加 [`docs/00-goal.md`](docs/00-goal.md) + [`docs/04-trends-2026H1.md`](docs/04-trends-2026H1.md) |
| **2 小时** | 全套 docs: 01 / 02 / 03 / paper-notes 重点 5 篇 |

---

## 仓库是什么 · 不是什么

| ✅ 是 | ❌ 不是 |
|---|---|
| 两块调研 + 路线图 + 33 篇 paper notes | 实机 demo / 代码实现 |
| 列出现有公开 SOTA，每条数字标 `[PDF 直引]` 或 `[推测]` | 拍胸脯保证 mobile 4DGS 一定跑得动 |
| 明确指出"未在公开材料找到 / 调研不足"处 | 凭印象补全缺失数字 |

---

## 仓库结构

```
docs/
├─ 00-goal.md                                 调研目标 spec（硬约束 / 必覆盖 / 产出要求）
├─ 01-high-precision-representation.md       第一块调研：离线高精度 4DGS 表示（含 §6 动静态分离专章）
├─ 02-rendering-acceleration.md               第二块调研：渲染加速（Vulkan 1.3 移动端，含末尾综述节）
├─ 03-end-to-end-roadmap.md                   整合路线图（M0 ~ M6）
├─ 04-trends-2026H1.md                        2025 H2 ~ 2026 H1 趋势单文件总结
└─ appendix/
   ├─ paper-notes/   33 篇核心论文笔记（按主线分组 A~F）
   ├─ collection-sop.md       采集 SOP 指针（详见 01- §8）
   └─ vulkan-impl-notes.md    Vulkan 1.3 实现笔记指针（详见 02- §7）
```

`.pdfs/`（git ignore）—— 33 个本地 PDF，不上传，给 offline 阅读 / 重跑抽取用。

---

## §术语速查（30 条，速查表，更全版见各 paper note）

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

---

## §调研结论（3 条决断）

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

## §现状与趋势

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
3. **Mobile streaming 实测报告涌现** —— AirGS / StreamSTGS / CAGS 是首批 4DGS on-device streaming 实测报告
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

## §Paper Notes 库（33 篇，按主线分组见 [`docs/appendix/paper-notes/INDEX.md`](docs/appendix/paper-notes/INDEX.md)）

**6 大组，全部 paper notes 都已 PDF 全文级验证**（arxiv API 反查 + 本地 PDF /Title 字段直引）：
- **A. 4DGS 表示**（9 篇）
- **B. 4DGS 加速 / 动静态分离**（6 篇）
- **C. 渲染加速**（8 篇）
- **D. 流式 streaming / 移动端落地**（6 篇）
- **E. 3DGS 静态加速**（4 篇）
- **F. Survey**（1 篇）

> **本批扩展（25 H2 ~ 26 H1）**: 14 篇新 paper notes（验证完成）

---

## §现状与关键风险

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

## §调研纪律（贯穿全文）

- **`绝不瞎编历史`**：`facts/discovery/never-fabricate-history` 红线，不据 CSDN / 二手综述转写为已验证数字
- 每条结论标 `[abstract 直引]` / `[PDF Table X 直引]` / `[基于 X 论文]` / `[推测]` / `[未在公开材料找到,需 PDF 核验]` / `[调研不足,需进一步实验]`
- 仓库 visibility：`private`；不写真名 / 个人邮箱 / token / 私人 key
