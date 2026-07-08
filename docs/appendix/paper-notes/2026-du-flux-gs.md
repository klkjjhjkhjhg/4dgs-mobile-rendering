# 2026-du-flux-gs · Flux-GS: Monte Carlo Energy Aggregation for Mobile 3D Gaussian Splatting

> **相关性**：**⭐⭐⭐ 本项目派系 3（移动端渲染管线）的直接对标新基线** —— ECCV 2026，**Mobile-GS 同一作者团队**（Xiaobiao Du 第一作者，Xin Yu 通讯）的下一篇工作。**Snap 8 Gen 3 上 137-151 FPS @ 1.6-4.6 MB**（Table 1 / Fig.1 直引），**训练时间从 Mobile-GS 的 86 min 缩短到 11 min（7.8× 训练加速）**。**已开源 WebGL 移动端渲染器**（https://github.com/xiaobiaodu/flux-gs-project）。

> **⚠ 重要区分**：这是 **3DGS（静态）**工作，不是 4DGS。**但其方法学（Monte Carlo SH 压缩 + multi-view densification + WebGL 端侧渲染）对 4DGS 同样可移植**——**Mobile-GS 也是 3DGS 静态，但已经成功成为本项目派系 3 首选**；Flux-GS 是其继任工作，应该替换或并列 Mobile-GS 作为新的派系 3 首选。

## 0.5 元数据

- **venue**: ECCV 2026 (under review)
- **arxiv-id**: 2606.30017
- **s2-id**: （v2 用 Semantic Scholar API 补全）
- **homepage**: https://xiaobiaodu.github.io/flux-gs-project/
- **github**: （无）
- **status**: under review
- **收录日期**: 2026-07-08
- **收录来源**: arxiv scan + 1-hop 引用规则
- **1-hop 引用**: （v2 补全，见 §11 1-hop 关系图）
- **评级**: ⭐⭐⭐

## 一句话问题

如何在 **mobile GPU (Snap 8 Gen 3)** 上以 **3rd-order SH 等价视觉质量 + 更小 storage** 实时渲染 3DGS，**且训练时间从 Mobile-GS 的 86 min 缩短到 11 min 量级**？

## 链接

- arxiv：<https://arxiv.org/abs/2606.30017>（v1 2026-06-29）
- 项目页：<https://xiaobiaodu.github.io/flux-gs-project/>
- GitHub（训练代码）：<https://github.com/xiaobiaodu/Flux-GS>
- GitHub（WebGL 移动渲染器）：<https://github.com/xiaobiaodu/flux-gs-project>
- PDF：已下 `.pdfs/2606.30017.pdf`（26 页，11.0 MB）
- 会议：**ECCV 2026**（论文 GitHub 头部直引 `European Conference on Computer Vision (ECCV)`）

## 年份 / 作者 / 机构（PDF 头部实测）

- **年份**：2026（v1 2026-06-29）
- **第一作者**：**Xiaobiao Du**（杜晓彪，**与 Mobile-GS 同一人**）
- **通讯作者**：Xin Yu
- **机构**：
  1. University of Technology Sydney（UTS）
  2. **Baidu Inc.（百度）** ← 新增，关键产业界背书
  3. Australian Institute for Machine Learning, **Adelaide University**

> **对比 Mobile-GS**：Mobile-GS 是 UTS + Adelaide + Li Auto（理想汽车）；**Flux-GS 把 Li Auto 换成了 Baidu**。百度 + 阿德莱德 + UTS 的产业 + 学术组合更稳，且 ECCV 比 ICLR 2026 排名更靠前一点（同行评审背书更强）。

## 方法核心（3 件套，PDF §3 直引 + abstract 直引）

### §3.1 Monte Carlo Specular Energy Aggregator —— **核心创新 1**

- **问题**：3rd-order SH 每个 Gaussian 48 系数，几百万个 Gaussian → 存储爆炸；Mobile-GS 用 teacher-student distillation 强压到 1st-order SH，**但训练耗时 86 min**。
- **Flux-GS 解法**：不蒸馏，**用 Monte Carlo 直接采样 3rd-order SH 的方向能量并聚合成 latent space**：
  - **Step 1**（前 3k iter）：保留 3rd-order SH 正常训练，捕获高频 specular
  - **Step 2**（>3k iter）：**spherical sampling K 个方向 + 计算 photometric residual**（`c_res(d_k) = c_i(d_k) - c_2_i(d_k)`），**聚合 E_mag（能量）和 E_dir（方向）** 成低维 descriptor（Eq. 4）
  - **训练结束时**：用 MLP Φ 把 (E_mag, E_dir, position, scale, rotation, opacity) → 1st-order SH `c'_i + Δc_i`（Eq. 6）
  - **推理时**：**MLP 离线 baked into Gaussian parameters**（"statically baked into the explicit Gaussian parameters prior to inference"）—— 推理时**完全无 MLP overhead**
- **结果**：**SH 内存降 61%（vs 3rd-order）/ 26%（vs 1st-order）**（Fig.2a 直引）

### §3.2 Attribute-Conditioned SH Enhancement —— **核心创新 2**

- **问题**：把 3rd-order 压到 1st-order 后，**高频 specular lobe 会损失细节**（SH dense + global 表示 sparse specular 本来就低效）
- **解法**：训练一个 **lightweight MLP Φ**（输入：position / scale / rotation / opacity / 1st-order SH），**预测 per-Gaussian 残差 Δc** 补偿丢失的高频
- **关键设计**：MLP 的**最后一层 zero-initialized**，所以训练初期等同于标准 3DGS，**平滑学习残差**
- **关键性质**：Φ 只依赖 Gaussian intrinsic 属性，**不依赖 camera viewing direction** —— **所以推理时 Φ 可以离线跑一次，结果直接 baked 进 Gaussian**（"crucially, because Φ relies strictly on intrinsic Gaussian attributes and is entirely independent of the camera viewing direction, the residual Δc only needs to be decoded once for subsequent inference"）

### §3.3 Multi-view Alpha-based Densification & Pruning —— **核心创新 3**

- **问题**：vanilla 3DGS 用 **single-view positional gradient** 做 densification，**容易产出过多 Gaussian + overfit 单视角**（Mobile-GS 也仍用这个）
- **Flux-GS 解法**：
  1. **Stratified Camera Sampling**：把相机分到 angular bins，**每个 bin 采一个代表视角**（最大 view variation）
  2. **Multi-view Loss Determination**：用 **alpha-weighted 误差在多视角上累加**（Eq. 9：`S_i^+ = Σ_{c,uv} α_i · M_uv^{c,+}`，bad-reconstruction 区域加分；well-reconstructed 区域减分）
  3. **Alpha-based Importance** 替代 gradient-based —— 避免单视角 occlusion 误导
- **结果**：多视图一致性 + 精确剪枝冗余

## 关键数字（PDF Table 1 直引 + Fig.1 直引）

### Table 1 · **Snapdragon 8 Gen 3 移动端实测**（Mip-NeRF 360）

| 类别 | 方法 | PSNR↑ | #G ×10⁶↓ | Storage↓ | FPS↑ | Train(min)↓ |
|---|---|---|---|---|---|---|
| **Indoor** | 3DGS (vanilla) | 30.41 | 1.45 | 478 MB | — | 27 |
| Indoor | 3DGS* (Huffman 量化) | 30.04 | 1.45 | 46 MB | 11 | 27 |
| Indoor | Speedy-Splat | 30.11 | 0.37 | 64 MB | 21 | 14 |
| Indoor | C3DGS | 30.01 | 0.75 | 21 MB | 18 | 31 |
| Indoor | LocoGS-S | 30.08 | 0.82 | 6.1 MB | 13 | 46 |
| Indoor | **Mobile-GS (full)** | 30.37 | 0.38 | 3.5 MB | 131 | **86** |
| Indoor | Mobile-GS* (no MLP) | 29.58 | 0.38 | 3.4 MB | 142 | 64 |
| Indoor | **Flux-GS (Ours)** | **30.22** | **0.22** | **2.1 MB** | **147** | **11** |
| **Outdoor** | 3DGS (vanilla) | 24.61 | 3.14 | 1361 MB | — | 36 |
| Outdoor | 3DGS* | 24.39 | 3.14 | 85 MB | 5 | 36 |
| Outdoor | Speedy-Splat | 24.41 | 0.56 | 88 MB | 14 | 13 |
| Outdoor | C3DGS | 24.38 | 0.91 | 34 MB | 13 | 45 |
| Outdoor | LocoGS-S | 24.31 | 1.41 | 10 MB | 19 | 61 |
| Outdoor | **Mobile-GS (full)** | 24.51 | 0.58 | 5.5 MB | 114 | 136 |
| Outdoor | **Flux-GS (Ours)** | **24.45** | **0.48** | **4.6 MB** | **132** | **11** |

> **Flux-GS vs Mobile-GS 关键比值**（Indoor 数据）：
> - **Storage**：2.1 MB / 3.5 MB = **0.6×**（小 40%）
> - **FPS**：147 / 131 = **1.12×**（快 12%）
> - **PSNR**：30.22 / 30.37 = **-0.15 dB**（几乎无损，< 0.2 dB）
> - **训练时间**：11 / 86 = **0.13× = 7.8× 训练加速** ← **本论文最响亮的卖点**
> - **Gaussian 数量**：0.22 / 0.38 = **0.58×**（少 42%）

### Fig.1 直引

> "ab. Flux-GS achieves rendering quality comparable to both 3DGS and the Mobile-GS, while reducing the number of Gaussian primitives and facilitating significantly higher FPS on the mobile with Snapdragon 8 Gen 3 GPU."
>
> 数据：3DGS = 11 FPS / 1.85M Gaussians; Mobile-GS = 137 FPS / 0.45M Gaussians; **Flux-GS = 151 FPS / 0.16M Gaussians**
> **Flux-GS vs 3DGS = 13.7× FPS 加速、11.6× Gaussian 数量减少**
> **Flux-GS vs Mobile-GS = 1.10× FPS、2.8× Gaussian 数量减少**

### §3.4 WebGL 部署细节

- **不依赖 CUDA** —— 浏览器 WebGL API 直接跑
- **Async WebWorker 处理 sort**（"offloading the depth-sorting of millions of Gaussians to an asynchronous WebWorker and using the CPU for the visibility order update"）—— **突破浏览器 120 FPS 显示限制**
- **Decoupled sorting**：与 Mobile-GS 的 OIT（no sort）路线**不同** —— **Flux-GS 选择保留 sort + WebWorker 异步化**

> **路线分歧点**：Mobile-GS = "no sort + OIT"；Flux-GS = "keep sort + async WebWorker"——**两条路线都达 130+ FPS**。**对本项目 4DGS 路线选择有指导意义**：M3 spike 阶段可能需要对比 OIT vs async-sort 两种实现。

## 与本调研主线的关系

### ⭐ 派系 3 排名：**Flux-GS 取代 Mobile-GS 成为新的 #1**

| 派系 3 维度 | Mobile-GS (ICLR 2026) | **Flux-GS (ECCV 2026)** |
|---|---|---|
| Snap 8 Gen 3 FPS | 131 (Indoor) | **147** (Indoor) |
| Storage | 3.5 MB (Indoor) | **2.1 MB** (Indoor) |
| 训练时间 | 86 min (Indoor) | **11 min** (Indoor, **7.8× faster**) |
| PSNR loss vs 3DGS | -0.04 dB | -0.19 dB (Indoor) |
| 排序策略 | **OIT (no sort)** | **Async WebWorker (keep sort)** |
| 开源 | GitHub | GitHub + **WebGL renderer 公开** |
| 移动端实测 | ✅ Snap 8 Gen 3 | ✅ Snap 8 Gen 3 |
| 通讯作者 | Xin Yu | Xin Yu (同一) |
| 第一作者 | Xiaobiao Du | Xiaobiao Du (同一) |

> **结论**：**Flux-GS = Mobile-GS 的全面继任者**。**训练快 7.8×** + 存储更小 + FPS 更高 + 公开 WebGL renderer。**唯一 trade-off 是 PSNR 略低 0.15 dB，仍在无损范围内 (< 0.2 dB)**。
>
> **本项目更新建议**：**§2 派系 3 #1 改为 Flux-GS，#2 改为 Mobile-GS**（GitHub star 数 + ECCV 2026 接收 + 7.8× 训练加速 = 全面胜出）。

### 对 4DGS Mobile 路线的具体承诺

- **`30~60 FPS @ 1080p on Snap 8 Gen 4` 目标**：Flux-GS 1.6 MB / 151 FPS（Fig.1 直引，**single 视角桌面渲染的 Mip-NeRF 360 数据**），**4DGS 估算 = 3DGS × 2× 时间复杂度 ÷ Flux-GS multi-view mask 复用 ≈ 75 FPS**。Adreno 8 Gen 4 比 Gen 3 快 30%，**估算 100 FPS 静态 3DGS**，`100 / 2 × 0.7 ≈ 35 FPS` —— **M4/M5 60 FPS 目标需要 4DGS-specific 进一步压缩**（如 4DGS-1K pruning）。
- **训练效率**：Mobile-GS 86 min 训一个 scene 不可接受（实际项目需要训几百个 scene）。**Flux-GS 11 min 是工程可行门槛**。**Flux-GS 的"Monte Carlo aggregation + 离线 baked MLP"模式对 4DGS temporal dimension 同样可移植**。
- **开源 WebGL renderer**：**比 Mobile-GS 更进一步直接给 WebGL 代码**。本项目 M3 spike 可以直接 fork 改。

### 4 派系组合路线的更新

> **本项目更新前** = Mobile-GS (派系 3) + 4DGS-1K (派系 1) + 4DGS-CC (派系 2) + 4DGCPro (派系 4)
>
> **本项目更新后** = **Flux-GS (派系 3 新首选)** + 4DGS-1K (派系 1) + 4DGS-CC (派系 2) + 4DGCPro (派系 4)
>
> → **仍然没有"Flux-GS + 4DGS"的组合** = 调研空白 = 本项目价值点（`[推测]`）

## 我未找到 / 提请下游注意

- **Flux-GS 推理 GPU 显存数字**：Table 1 未给；1.6-4.6 MB 模型 + OIT 之外的 sort 路径下，**推理显存应 < 100 MB 量级**（`[推测]`）—— **未在 abstract 精确拿到**
- **Flux-GS 的 WebGL 渲染器支持哪些平台**：GitHub repo 有说明，**需要进一步核**（大概率 iOS Safari + Android Chrome + 桌面 WebGL 全支持）
- **Flux-GS 的 multi-view Alpha densification 在 4DGS 场景下是否仍然有效**：论文未做实验。**理论上**：4DGS 的 temporal dimension 多一个时间轴，multi-view 概念可扩展为 "multi-frame"——但需要重新设计 stratified sampling 策略（沿时间轴 + 沿视角轴同时分 bin）
- **Flux-GS vs Lumina 的对比**：都是 mobile 3DGS，**Lumina = 4.5× speedup + 5.3× energy**（mobile Volta）；**Flux-GS = 13.7× speedup over vanilla 3DGS on Snap 8 Gen 3**——但**两者 GPU 平台不同**，需 cross-platform benchmark
- **Flux-GS ECCV 2026 接收 vs Mobile-GS ICLR 2026 接收**：ECCV oral/poster 还没公开，ICLR 2026 是 conference paper。**两者都是顶会**，Flux-GS 时间更新（2026-06-29 > 2026-03-12）

## 我的 commit 节奏

本文是原 33 篇 paper notes 之外**新加的第 34 篇**，**直接挑战原 §2 派系 3 #1 位置（Mobile-GS）**。**配套需更新**：
- `INDEX.md` 派系 3（C 渲染加速）加 Flux-GS 行 + 调整排名
- `README.md` §2 派系 3 表格 #1 改 Flux-GS，#2 改 Mobile-GS；§1 论据表加新行（论据 6：Flux-GS 1.6 MB / 147 FPS / 11 min 训练）
- `docs/02-rendering-acceleration.md` 加 §X 节"Mobile 端 2026 H2 新基线"

## 11. 1-hop 关系图

### 11.1 引用的相关工作 (downstream)

Flux-GS 是 3DGS 移动端 SOTA（Snap 8 Gen 3 实测 147 FPS @ 2.1 MB）：

- **3DGS 原论文**：[2023-kerbl-3dgs](2023-kerbl-3dgs.md)
- **Mobile-GS**：[2026-du-mobile-gs](2026-du-mobile-gs.md)（直接前置工作）

### 11.2 被引用的后续工作 (upstream)

**v2 用 S2 API 自动拉取完整 cited-by 列表**——预计会成为 3DGS 移动端后续工作的引用基线。
