# Layered 4D-Rotor Gaussian Splatting: A Compressed Representation for Long Dynamic Scenes

## 0. 基本信息
- 作者: Hanjie Xu*, Yuanxing Duan*, Qiyu Dai*, Ge Li†, Baoquan Chen†, He Wang† (* equal contribution, † corresponding)
- 单位: Peking University (PKU) + Galbot
- 年份: 2026 (CVPR 2026)
- 会议: CVPR 2026 (openaccess, p.1 watermark: "This CVPR paper is the Open Access version, provided by the Computer Vision Foundation")
- 论文 ID: arxiv-id 未在本 PDF 提供 (CVPR openaccess PDF)；主页发布于 ACM SIGGRAPH 2024 之前的 4D-Rotor GS 系列工作
- GitHub: 未在 PDF 显式给出 (PDF 仅含 project page)
- 项目主页: https://m1sak1-mei.github.io/layered-4d-rotor/
- 代码许可: 未声明 (待核实)

## 0.5 元数据
- venue: CVPR 2026 (openaccess)
- arxiv-id: 未在 PDF 提供
- s2-id: (未查询 — cron 批次)
- homepage: https://m1sak1-mei.github.io/layered-4d-rotor/
- github: (PDF 未给出 — 待补)
- status: 收录
- 收录日期: 2026-08-10
- 收录来源: cvpr_openaccess (cron)
- 评级: T1 (核心 4DGS 压缩 + 实时渲染)
- survey_section: 4
- faction: A 兼 C (4DGS 表示 + 推理加速; 强 mobile 端口价值)

## 1. 一句话总结
L4DRotorGS 在 4D-Rotor Gaussian 基础上引入 **layer-bucket 层级时间结构 + Triple-buffer 训练框架 + 三件套压缩 (FCQ/Layered/RCQ)**，把原本 >500 MB / <10s 的 4DGS 推到 8.8 MB / 30 min 训练 / 661 FPS 的实用水准（RTX 3090），压缩率最高 22.3×，是少数同时实现"长视频 + 高压缩 + 实时"四项指标的工作。

## 2. 摘要 (核心 3 段)

**问题**: 现有 4DGS 动态重建 (Deformable4DGS, 4D-Rotor GS, RealTime4DGS) 在短片段 (<10 s) 上视觉质量极佳，但长视频场景下高斯数量爆炸 → 存储 >500 MB、GPU VRAM 紧张、训练/渲染不可持续；TGH 虽尝试层级时间结构但无法做到 <1 MB/s 带宽（无法上移动/带宽受限场景）。

**方法**: 提出 L4DRotorGS = 表示 + 训练 + 压缩 的统一框架。三大贡献：
1. **Layered 4D Gaussian 表示** — 沿 TGH 思路按 temporal extent τ 分层，但额外把每层切成 left/right temporal buckets（允许 Gaussian 跨 bucket 边界），令层内时间一致性更利于压缩；层数 L = ⌈log₂ n⌉+1（n=帧数）。
2. **Triple-buffer 训练框架** — GPU 双缓冲 + CPU bucket 缓冲，结合自适应密度控制，最小化 CPU↔GPU 传输（4DGS/TGH 训练瓶颈）；引入 **Dynamic-Aware Rotor Learning Rate (DARLR)**：对 temporal extent τ 大的静态 4D Gaussian 施更小的 rotor-temporal 学习率，避免长视频上静态区域失稳。
3. **三件套压缩**:
   - **Factorized Covariance Quantization (FCQ)**: scale 拆成 (scale factor, normalized scale) → SQ + VQ；rotor 拆成 (spatial, temporal) → 独立 VQ → 解码端按 spacetime 重建合并；解决直接 VQ 4D cov 量化在 10⁰–10¹⁰ 跨幅下不可行的问题。
   - **Layered Compression**: 跨层分布差异大的属性 (scale factor, normalized scale, rotor spatial, rotor temporal) 逐层独立 codebook；分布跨层稳定的 (SH, opacity) 用 global VQ/SQ；合并尾层稀疏层进一步省存储。
   - **Residual Codebook Quantization (RCQ)**: 每层内按 bucket-block 局部 VQ + 轻量 residual codebook 补偿，避免给每 block 单独维护 codebook 的存储开销；Layer 0 排除（短时变化小受益少）。

**结果**: N3DV 数据集（6 场景，19–21 cam, 10s, 1352×1014）上 Ours 32.23 PSNR / 180.7 MB / 351 FPS（RTX 3090）；Ours Large 32.06 PSNR / 13.8 MB / 662 FPS（13.1× 压缩）；Ours Small 31.84 PSNR / 8.8 MB / 661 FPS（20.5× 压缩，bitrate <1 MB/s）。SelfCap (6 场景，1–10 min, 4K, 60 FPS) 上 Ours 24.64 PSNR / 928.8 MB / 854 FPS；Large 24.49 PSNR / 48.4 MB / 1190 FPS；Small 24.41 PSNR / 41.8 MB / 1194 FPS（19.1× 压缩）。N3DV 训练 30 min / 2 GB VRAM peak。

## 3. 派系分类
- **A (4DGS representation)**: 主。L4DRotorGS 是 4DGS 表示层改进（layer-bucket 时空结构 + 4D-Rotor 几何）。
- **C (3DGS / 4DGS 推理加速)**: 强沾边。Triple-buffer 训练框架 + DARLR 训练策略让单 GPU 30 min 训完；CUDA 渲染器 662 FPS 是核心卖点。
- **B (4DGS 压缩)**: 核心。FCQ + Layered + RCQ 三件套把 4DGS 压到 1/20 存储。
- **D (移动端)**: 高度相关。bitrate <1 MB/s + 2 GB VRAM peak + 661 FPS 都是为 mobile / edge 部署设计，但作者没在 mobile GPU 上实测。
- **E (cross-disciplinary)**: 沾边 — VQ/SQ/codebook 量化借鉴传统 compression (image/video codec) 的多层残差字典思路。

**结论**: 主派系 **A + B + C**。对 D (mobile) 派系有 **强借鉴价值**（架构特性匹配移动端，但需自做 port）。

## 4. 方法

### 4.1 整体架构
L4DRotorGS = 表示层 (Layer-Bucket) + 训练层 (Triple-buffer + DARLR) + 压缩层 (FCQ + Layered + RCQ) 三段式。流水线：训练 4D-Rotor GS → layer/bucket 划分 → 自适应剪枝/稠化 → 编码端三件套压缩 → 解码端按 timestamp 拉取 neighbor buckets 渲染。

### 4.2 Layer-Bucket 表示 (Sec. 3.2)

每 4D Gaussian 中心 μ₄D = (μx, μy, μz, μt) 与 4D 协方差 Σ₄D = R₄D · S₄D · S₄Dᵀ · R₄Dᵀ。给定时间 t 切片得 3D Gaussian via 公式 (3)；可见性门控 λ(t−μt)² > 16 直接剔除（temporal extent τ = 2√(16/λ)）。

**Layer 划分**: τ 大的 → 高层（slow varying，跨长时间段）；τ 小的 → 低层（瞬态）。L = ⌈log₂ n⌉+1。
**Bucket 划分**: 每层再按时间轴切 left/right buckets，允许 Gaussian 跨 bucket 边界（用 mean time μt + τ 判定归属），避免 TGH 那种硬切导致边界 Gaussian 被压到低层的问题。
**渲染时**: 仅加载 timestamp t 当前 bucket + immediate neighbors（每层少量 buckets），大幅降 VRAM。

### 4.3 Triple-Buffer 训练框架 (Sec. 3.2.2)

每 iteration:
1. 采样训练图像 + timestamp t
2. GPU buffer 更新 —
   - 自适应密度控制 (pruning + densification, 每步)
   - 从 CPU bucket buffer 把可见 4D Gaussian 加载到 GPU render buffer
   - 长时间未用的 Gaussian offload 回 CPU
3. 前后向 + 优化

GPU 双缓冲隐藏 CPU↔GPU 异步传输开销。**DARLR (Dynamic-Aware Rotor Learning Rate)**: temporal extent τ 大的 static 4D Gaussian → 较小 rotor-temporal 学习率；否则长视频训练中静态区域会被 temporal rotor 漂移产生"伪动态"伪影。

### 4.4 三件套压缩 (Sec. 3.3)

#### 4.4.1 Factorized Covariance Quantization (FCQ)
直接 VQ 4D 协方差失败（spatial/temporal scale 跨 10⁻³–10³，二次放大到 >10 个数量级，远超 VQ 精度）。分解：
- **Scale**: 4D scale → (scale factor) + (normalized scale)，前者 SQ (Scalar Quantization, 8-bit pre-activation 避免动态范围)，后者 VQ
- **Rotor**: 8D 4D rotor → spatial (4D) + temporal (4D) 独立 VQ → 解码时合并归一化
- 重要性权重：渲染所有训练图像，pixel contribution（backprop 梯度）= 量化权重

#### 4.4.2 Layered Compression
跨层分布差异大的属性（scale factor, normalized scale, rotor spatial, rotor temporal）→ 逐层独立 codebook（解决 shared codebook 因跨层方差大导致量化误差大病）；跨层分布稳定的（SH, opacity）→ global VQ/SQ（省 codebook 存储）；尾层稀疏层合并；opacity 在 sigmoid 激活后 SQ（值域 [0,1] 天然适 SQ）。

#### 4.4.3 Residual Codebook Quantization (RCQ)
每个 layer 内部 further 分 bucket-block；每 block 用 block-specific codebook（VQ），但 block codebook 与 global layer codebook 之差用一个**轻量 residual codebook** 表示（避免给每个 block 单独维护 codebook 的存储开销）。解码：global[i] + residual[j] → block-specific entry → Gaussian 索引。Layer 0 排除 RCQ（短时变化小，受益少）。

### 4.5 实现细节 (Sec. 3.4)
- 全 C++/CUDA 实现 — 训练 / 压缩 / 渲染一体化
- N3DV 单 RTX 3090：训练 30 min / peak 2 GB VRAM / 压缩 4 min / 推理 660 FPS
- 60s 序列 (3600 帧) 端到端：>20× 压缩 + >900 FPS（RTX 5090）

## 5. 实验

### 5.1 数据集
- **N3DV** [Li 2022, CVPR]: 6 动态场景，19–21 同步相机，1352×1014 分辨率，10s 持续，平均 300 帧
- **SelfCap** [Xu TOG 2024, TGH 同一作者]: 6 场景（bicycle repairing, yoga 等大动作），60 FPS @ 4K，18–22 cam，1–10 min 长时

### 5.2 基线
NeRF-based: DyNeRF, StreamRF, HyperReel, NeRFPlayer, K-Planes, MixVoxels
Gaussian-based: Deformable4DGS, RealTime4DGS, MEGA, STG, Ex4DGS, TGH

### 5.3 评测指标
PSNR↑ / SSIM↑ / LPIPS↓ + Training Time + FPS + Storage（MB）+ bitrate (MB/s)

## 6. 性能数字 (PDF 页码标)

### N3DV Dataset — Table 1, PDF page 6 (RTX 3090)
- DyNeRF: 29.58 PSNR / — / 0.08 LPIPS / 1344 h / 0.015 FPS / 28 MB [p.6]
- StreamRF: 28.16 / 0.85 / 0.31 / 1.3h / 8.50 / 24 MB [p.6]
- HyperReel: 30.36 / 0.92 / 0.17 / 9h / 2.00 / 360 MB [p.6]
- NeRFPlayer: 30.69 / — / 0.11 / 6h / 0.05 / — [p.6]
- K-Planes: 30.73 / 0.93 / 0.07 / 3.2h / 0.10 / 309 MB [p.6]
- MixVoxels: 30.85 / 0.96 / 0.21 / 1.5h / 16.70 / 508 MB [p.6]
- Deformable4DGS: 28.42 / 0.92 / 0.17 / 1.2h / 39.93 / 147 MB [p.6]
- RealTime4DGS: 31.57 / 0.97 / 0.16 / 8h / 72.80 / **3128 MB** [p.6]
- MEGA: 31.49 / 0.97 / 0.057‡ / — / 77.42 / 25.05 MB [p.6]
- STG: 32.05 / 0.95 / 0.14 / 1.3h / 140 / 200 MB [p.6]
- Ex4DGS: 32.11 / 0.94 / 0.14 / 0.6h / 120.6 / 115 MB [p.6]
- TGH† (Flame Salmon only): 29.44 / 0.945 / 0.214 / 2.1h / 550 / 90 MB [p.6]
- **Ours (uncompressed)**: **32.23** / 0.941 / 0.153 / 0.5h / 351.12 / 180.7 MB [p.6]
- **Ours Large**: 32.06 / 0.939 / 0.153 / 0.6h* / **661.93** / 13.8 MB (13.1× 压缩) [p.6]
- **Ours Small**: 31.84 / 0.937 / 0.156 / 0.6h* / 660.79 / **8.8 MB** (20.5× 压缩, bitrate <1 MB/s) [p.6]

### SelfCap Dataset — Table 2, PDF page 8 (RTX 5090)
- Ours: 24.64 PSNR / 854.21 FPS / 7.2h 训练 / 928.8 MB [p.8]
- Ours Large: 24.49 / 1190.15 / 7.9h / 48.4 MB [p.8]
- Ours Small: 24.41 / 1193.50 / 7.9h / 41.8 MB (19.1× 压缩) [p.8]

### 不同视频时长 — Table 3, PDF page 8 (SelfCap Bike scene)
PSNR/Storage:
- 1 min: 26.45 / 578.4 MB (Ours); 26.26 / 29.5 MB (Large); 26.17 / 27.2 MB (Small) [p.8]
- 2.5 min: 26.29 / 1519.0 MB; 26.16 / 55.6 MB; 26.05 / 49.0 MB [p.8]
- 5 min: 28.58 / 1151.1 MB; 28.25 / 56.3 MB; 27.81 / 51.8 MB [p.8]
- 10 min: 24.90 / 1787.1 MB; 24.73 / 92.9 MB; 24.70 / 87.4 MB [p.8]
- 5 min PSNR 异常高 (28.58) — 作者未解释，可能是数据分布因素

### 压缩组件 Ablation — Table 4, PDF page 8 (N3DV Flame Salmon)
- (a) Cov4D VQ: 11.35 PSNR / 29.03 MB [p.8]
- (b) + FCQ: 22.09 / 16.22 MB [p.8]
- (c) + Layer Structure: 28.90 / 15.93 MB [p.8]
- (d) + RCQ: 28.92 / 16.73 MB [p.8]
- 关键洞察: FCQ 是最大跳跃 (+10.74 dB, 11.35→22.09)；Layered 是第二大跳跃 (+6.81 dB, 22.09→28.90)；RCQ +0.02 dB 微调（成本敏感时可省）

### RCQ Codebook Size Ablation — Table 5, PDF page 8
- 64: 28.919 PSNR / 16.740 MB [p.8]
- 128: 28.919 / 16.734 MB [p.8]
- 256: 28.922 / 16.733 MB [p.8]
- 512: 28.923 / 16.734 MB [p.8]
- 1024: 28.921 / 16.733 MB [p.8]
- 结论：RCQ 对 codebook size 极不敏感（64→1024 几乎不变），可大胆用小 codebook

### 训练效率 (正文 Sec. 3.4)
- N3DV 训练: ~30 min 单卡 RTX 3090 / peak 2 GB VRAM / 压缩 4 min / 推理 660 FPS [p.5]
- 60s 3600 帧: >20× 压缩 + >900 FPS (RTX 5090) [p.2]

### DARLR 视觉对比 — Fig. 7, PDF page 6
- w/o DARLR: 静态区域过平滑、丢失高频纹理
- w/ DARLR: 保留细节

## 7. 评估

**亮点**:
- **实用参数全表**: 8.8 MB / 661 FPS / 0.6h 训练 / 2 GB VRAM peak — 把 4DGS 从实验室 demo 推到生产可用
- **三件套压缩互相补充**: FCQ 解维度灾难、Layered 解跨层方差、RCQ 在小成本下再压；每件 ablation 都有清晰增益
- **C++/CUDA 全栈自研**: 训练/压缩/渲染统一底层，不像很多工作依赖 PyTorch 调度
- **bitrate <1 MB/s**: 明确 mobile / streaming 部署目标，应用驱动清晰
- **SelfCap 真正长视频**: 1–10 min 4K 60 FPS，跟 N3DV 互补（短 vs 长）
- **Triple-buffer 框架**: 解决 4DGS 训练中 CPU↔GPU 传输瓶颈，普适到其他 high-Gaussian-count 训练
- **DARLR**: 静态区域训练稳定性的"小补丁"，但非常重要 — 没它长视频不能训

**短板**:
- **压缩是 offline** — 文中明确 "compression is still time-consuming, does not support online training" (p.8 Sec. 5)；限制 streaming capture 场景
- **TGH baseline 仅在 Flame Salmon 场景评估**（Table 1 footnote †），其他场景对比缺
- **没在 mobile GPU (Adreno/Mali) 实测** — 8.8 MB + 661 FPS 是 RTX 3090/5090 数字；移动端 Adreno 830 算力差 10–20×，66 FPS 都不一定够
- **SH global VQ 跨层共享** — 跨场景复用 codebook 没说，可能需要 per-scene codebook（牺牲一些好处）
- **开源情况不明** — PDF 全文未给 GitHub 链接（只给 project page），对复现不友好
- **5 min PSNR 异常高** (28.58 vs 1 min 26.45) — 数据本身因素，论文未解释
- **Deformable4DGS baseline 仅 28.42 PSNR** — 应该是 4DGS 原论文数值，与其他 baseline 跨 baseline 公平度需注意

**对我们的相关性 (mobile 4DGS)**:
- **高**。L4DRotorGS 的所有设计目标（低存储、低 VRAM、高 FPS、bitrate <1 MB/s）都和 mobile 部署诉求高度重叠
- **Triple-buffer 思想可直接移植** — 移动端 NPU/GPU 内存更小，bucket selective loading 是必走之路
- **C++/CUDA 渲染器代码可参考** — 4DGS 渲染 shader 部分设计
- **DARLR 训练策略** 可借鉴到 mobile 端训练 pipeline（虽然 mobile 多用 server-side 训练，但不影响 inference 时这些模型的兼容性）
- **风险**: 作者未在 mobile GPU 上跑；bitrate <1 MB/s 是移动网传输的目标，但端侧推理 FPS 是需要我们补的实验

## 8. 引用 (核心)
- [ref 4] Duan 2024 — 4D-Rotor Gaussian Splatting (ACM SIGGRAPH 2024), 本工作的直接基础, cite at p.2, p.3
- [ref 34] Xu 2024 — Temporal Gaussian Hierarchy (TGH, TOG 2024), 本工作直接借鉴并改进的层级结构, cite at p.2, p.3, p.5, p.6
- [ref 14] Kerbl 2023 — 3DGS 原论文 (SIGGRAPH/TOG 2023), cite at p.3
- [ref 17] Li 2022 — N3DV dataset, cite at p.1, p.2, p.5, p.6
- [ref 23] Niedermayr 2024 — C3DGS (借鉴 FCQ 思路), cite at p.5
- [ref 11] Hu 2025 — 4DGC (rate-aware 4DGS compression), cite at p.3
- [ref 12] Javed 2024 — TC3DGS (temporal compression), cite at p.3
- [ref 13] Jiang 2024 — HiFi4G (non-rigid tracking + dual-map), cite at p.3
- [ref 20] Liu 2025 — Light4GS (hierarchical context model), cite at p.3
- [ref 37] Yuan 2025 — 4DGS-1K (1000+ FPS 4DGS), cite at p.3
- [ref 9] Girish 2024 — QUEEN (quantized streaming), cite at p.3
- [ref 33] Wu 2023 — Deformable 3DGS (Deformable4DGS), cite at p.3, p.6
- [ref 36] Yang 2024 — RealTime4DGS (ICLR), cite at p.2, p.3, p.6
- [ref 38] Zhang 2024 — MEGA (memory-efficient 4DGS), cite at p.6
- [ref 19] Li 2024 — STG (spacetime Gaussian feature splatting), cite at p.6
- [ref 15] Lee 2024 — Ex4DGS (fully explicit dynamic GS), cite at p.6
- [ref 1] Attal 2023 — HyperReel, cite at p.2, p.6
- [ref 16] Li 2022 — StreamRF, cite at p.2, p.6
- [ref 28] Song 2023 — NeRFPlayer, cite at p.2, p.6
- [ref 6] Fridovich-Keil 2023 — K-Planes, cite at p.2, p.6
- [ref 31] Wang 2023 — MixVoxels, cite at p.2, p.6
- [ref 22] Mildenhall 2020 — NeRF 原论文, cite at p.2

## 9. Insight

**Insight #1 — 4DGS 走向实用的"三件套"配方逐渐清晰**: L4DRotorGS 给出 (Layered Structure + Quantization + Online-friendly CUDA) 的标准组合。Mobile 端部署 4DGS 不需要自己发明整套压缩 palette，参考这个配方即可。这给我们一个 system design blueprint: 不要从零开始，要把 4DGS 当成"高维度图像"，走传统 image/video codec 的"分层 + 量化 + 残差"路线。

**Insight #2 — Triple-buffer 训练范式被低估**。4DGS 高斯数爆炸后，CPU↔GPU 传输是训练瓶颈（不仅是 VRAM）。L4DRotorGS 把 GPU 双缓冲 + 异步 bucket loading 抽象出来，这种设计原则对移动端训练/tuning 同样有效（移动端 NPU/GPU 共享内存但不共享 cache，bucket-aware loading 仍能省带宽）。当我们的 mobile port 想做 on-device fine-tuning 时，Triple-buffer 思想直接借鉴。

**Insight #3 — FCQ 分解是"维度灾难"的通用解法**。当 Gaussian 维度（4D、6D、未来可能 8D）跨数个数量级时，整体 VQ 必然失败。L4DRotorGS 的 factorize 思路 (scale factor + normalized scale, rotor spatial + temporal) 给了我们一个通用范式：先按物理意义分层归一化，再分别量化。我们未来做 6DGS / hash-grid 4DGS 压缩时，可以套同样模板。

**Insight #4 — 压缩 vs 质量 trade-off 的"甜蜜点"已探明**。Our Large (13.1×, -0.17 dB) vs Our Small (20.5×, -0.39 dB) 的差距很小但存储差距 35%，说明在 13–20× 区间压缩边际收益递减。对 mobile 端存储预算分析时有指导意义：超过 20× 投入产出比急速下降，应停在 15–20× 区间。

**Insight #5 — DARLR 揭示了 4D-Rotor GS 的"伪动态"问题**。这是 L4DRotorGS 训练稳定性的关键：static 4D Gaussian 的 temporal rotor 分量若用同学习率，长视频训练会因数值累积漂移让静态区域产生"伪动态"伪影。Mobile 端即使不做 fine-tuning，importing 这些被 DARLR 稳定训练好的模型也能避免静态区域抖动。其他 4DGS 工作（4DGS 原论文、RealTime4DGS）没专门处理这个问题，可能是它们在长视频上表现差的隐藏原因。

**Insight #6 — bitrate <1 MB/s 是 mobile 传输侧的硬指标**。8.8 MB / 10 min = 0.88 MB/s，刚好压在 1 MB/s 以下 — 这是 mobile / streaming 实际部署的带宽预算上限。意味着 4DGS 终于"能下到手机上"了（虽然还要看端侧解码 FPS，但这篇文章没给）。这是行业拐点：4DGS 从"学术 demo"过渡到"工程可用"的标志事件。

## 11. 1-hop 关系图 (5 篇示范)

**核心 1-hop 关系图**:

- 节点 | 关系类型 | 上游/下游
- **4D-Rotor Gaussian Splatting [Duan SIGGRAPH 2024]** | 本工作的直接基础（基线 + 几何表示） | upstream
- **TGH (Temporal Gaussian Hierarchy) [Xu TOG 2024]** | 借鉴并改进的层级结构（layer-bucket = TGH + cross-boundary） | upstream
- **C3DGS (Compressed 3DGS) [Niedermayr CVPR 2024]** | 借鉴 FCQ 量化思路（factorize 后 VQ） | upstream
- **3DGS [Kerbl SIGGRAPH 2023]** | 更底层基础 (cite at p.3) | upstream
- **SelfCap [Xu TOG 2024 / TGH 同期]** | 同时使用 TGH 团队自家数据集 (1–10 min 长视频) | parallel concurrent

**未在 INDEX 的 1-hop 候选** (1-hop rule: 命中即停):
- 4DGC, TC3DGS, HiFi4G, Light4GS, QUEEN, 4DGS-1K — 其他 4DGS 压缩工作，需在 1-hop rule 下核对
- MEGA, STG, Ex4DGS, RealTime4DGS, Deformable4DGS — 实验对比 baseline (Table 1)
- HyperReel, StreamRF, MixVoxels, K-Planes, NeRFPlayer, DyNeRF — NeRF-based baseline
- N3DV [Li CVPR 2022] — 主数据集之一
