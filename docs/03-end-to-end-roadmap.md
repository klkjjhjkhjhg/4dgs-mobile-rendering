# 03 — 整合路线图(采集 → 训练 → 实机 demo)

> **状态**:已填。基于 `docs/01-high-precision-representation.md` + `docs/02-rendering-acceleration.md` 装配,不重新检索。
>
> **本文件读者**:项目发起人 / 团队 leader / 决策者。本文件不是"技术细节",是"接下来 6 个月怎么排"。细节下沉到 `01-` / `02-`。
>
> **来源标注延续**:`[abstract 直引]` / `[基于 X 论文]` / `[推测]` / `[未在公开材料找到,需 PDF 核验]` / `[调研不足,需进一步实验]`。
>
> **依赖**:`docs/00-goal.md`(目标 spec)+ `01-`(高精度表示)+ `02-`(渲染加速)+ `appendix/{collection-sop, vulkan-impl-notes}.md`(本路线图各自引用)。

---

## 0. 执行摘要

**目标一句话**:在 ~6 个月内,把"高速相机阵列预制的离线 4DGS 资源"做到 **Snapdragon 8 Gen 4 / Adreno 830 上的 Vulkan 1.3 实时渲染(30~60 FPS @ 1080p,~3M splats 上限)**。

**路线三句话**:
1. **训练端**:走主线 `Wu-4DGS`(canonical + HexPlane + deformation)+ **MonST3R** 动态 SfM,产出**带 MEGA 训练路径(存储压缩 190×/125×)** 的 4DGS 资源。`[01- §7.1 / §7.3]`
2. **加速端**:走 7 步加速链(稀疏化 → 训练期 bitpack → tile-based GPU → 时空复用 → 内部降采样 → 上采样 → compute/fragment 分工)。每步收益**全部为推测,需真机实测**。`[02- §1]`
3. **风险与现状(2026-07-03 修订)**:✅ `4DGS-1K(arxiv:2503.16422, Yuan et al., NUS, 2025-03)` 公开论文**已找到**(`[paper-notes/2025-yuan-4dgs-1k.md PDF 全文级]`),**替代"用 MEGA 当替身"的错口径**;**TITAN X 200+ FPS 是移动端可行性的关键证据**(`论文 §7.2 直引`)。剩余风险:Adreno 8 Gen 4 上 4DGS FPS baseline = 0;**未在 public 找到任何 mobile 4DGS 实测**。`[02- §9]`

**关键决策**:在 **M0 立项 + M1 桌面 Vulkan baseline** 之后,必须做一次"go / pivot"决策 —— 决策标准 = **桌面 Vulkan baseline 走完 `02- §7` 那张 compute/fragment pipeline 后,30~60 FPS 在笔记本 RTX 4090 / Snapdragon 8 Gen 4 Reference Design 上是否 ≥ 15 FPS**(下限 15 FPS 的理由:30 FPS 目标的 50%,达成一半说明 pipeline 路径成立,反向至少可以倒推差异化空间)。

---

## 1. 总时间表(6 个月)

| 里程碑 | 时长 | 主要交付物 | 关键依赖 | Go / Pivot |
|---|---|---|---|---|
| **M0 立项** | 2 周 | Go/pivot 标准 + 项目宪章 + 6 个月预算 + 测试机锁型 | `01- §7`、`02- §1~§9` | — |
| **M1 桌面 Vulkan baseline** | 4 周 | 桌面 Vulkan 上跑通 4DGS 原始资源,记录 FPS / 显存 | NVIDIA `vk_gaussian_splatting` + 4DGS 仓库 | **≥ 30 FPS @ 800p ✓** 否则 pivot |
| **M2 高精度训练管线** | 4 周 | 6 高速相机阵列 + MonST3R + Wu-4DGS 训练 pipeline,产出 1 个 demo scene | M0 选定的采集设备 + 单 GPU | PSNR ≥ 28 dB on D-NeRF subset ✓ |
| **M3 训练期 bitpack + 稀疏化** | 4 周 | 训练管线接入 **4DGS-1K 路径**(Spatial-Temporal Variation Score pruning + Temporal Filter mask + PP) | M2 pipeline | **压缩后 PSNR 损失 < 0.5 dB**(`[arxiv:2503.16422 PDF Table 1 直引]:N3V 31.91→31.88 = -0.03 dB`)✓ |
| **M4 移动端 rendering pipeline** | 4 周 | Vulkan 1.3 compute + fragment shader 在 Adreno 上跑 | `02- §7` + 测试机 | 720p internal ≥ 15 FPS ✓ |
| **M5 上采样 + 优化** | 4 周 | FSR 2 / Arm ASR 上采样 + temporal mask 自研 | `02- §5`、`02- §6` | 1080p ≥ 30 FPS ✓ |
| **M6 实机 demo + 路线收口** | 2 周 | 一段 60 FPS × 30 s demo + README 路线收口 | M5 | demo 成功跑通 ✓ |

合计 ~ 24 周 ≈ 6 个月。**逐里程碑后都有 go / pivot 决策点**。

---

## 2. 各里程碑详细定义

### M0 立项(2 周)

**任务**:
- **测试机型锁定**:Snapdragon 8 Gen 4 Reference Design + 1 台消费级旗舰机(如 Xiaomi 14 Ultra / Samsung S24 Ultra 类);**至少 1 台机型有 Vulkan 1.3 + on-tile compute + fp16 storage**
- **采集相机阵列定型**:6 路 4K 60fps 工业相机(成本 ~ 5~10 万元 / 套)—— 具体选型由 `01- §8` 给出,本里程碑锁定 1 套
- **桌面训练机**:RTX 4090 / A100 一台,显存 ≥ 24 GB(用来跑 `02- §1` 步骤 1~3 的桌面等价)
- **代码仓库基线**:`~/Codes/4dgs-mobile-rendering/`(已建,本调研文档已沉淀于此)

**Go/Pivot 标准**:可立项 → "测试机 feature OK + 桌面 GPU 跑得动 4DGS 训练" → 进 M1。

**依赖**:`01- §7` 主线推荐 + `02- §1` 加速技术树 + `02- §9` 风险项前 5 项。

---

### M1 桌面 Vulkan baseline(4 周)

**任务**(全部基于 `02- §7` 草案):
- 在桌面 RTX 4090 / Vulkan 1.3 上跑 NVIDIA `vk_gaussian_splatting`(已开源,gh 仓库存在,见 `02- 附录 A`)
- 跑通原始 4DGS 资源(用 `hustvl/4DGaussians` 导出的 .ply / 自定义格式)
- **记**:cull / decode / sort / blend 各阶段 GPU 时间 / 显存峰值 / FPS / 帧时间方差

**Go/Pivot 标准**:**桌面 Vulkan 跑 4DGS @ 800×800 ≥ 30 FPS**。设这个数字的理由:`[abstract 直引]` Wu-4DGS 在 RTX 3090 上 `82 FPS @ 800×800`,我们用更新的 RTX 4090,**不应比 3090 慢**,设 30 为下限避免早期 baseline 误判。
- **达到 ≥ 30 FPS** → 进 M2
- **< 30 FPS** → pivot 检查:NVIDIA vk_gaussian_splatting 是否真支持 4DGS(也许是 3DGS only),或者 4DGS 的 deformation field 是否在 Vulkan pipeline 里跑通

**风险与未知**:`02- §9.1` 第 2 项 — Adreno baseline = 0;**这个里程碑至少能给出桌面 Vulkan baseline**,间接给 Adreno 留 calibration。

**依赖**:NVIDIA vk_gaussian_splatting 仓库是否真支持 4DGS 的 time-varying splat → 若不支持,**自研一层 thin wrapper**(仍按 `[abstract 直引]` 4DGS 仓库的 splat 渲染逻辑搬到 Vulkan 1.3 compute path)。

---

### M2 高精度训练管线(4 周)

**任务**(基于 `01- §1-§6`):
- 装高速相机阵列(6 路)+ 用硬件 trigger 同步(参见 `appendix/collection-sop.md`)
- 跑 MonST3R(动态友好 SfM)→ 初始 3DGS
- 跑 Wu-4DGS 训练(`hustvl/4DGaussians`):HexPlane + canonical + deformation
- **在 D-NeRF synthetic / Plenoptic Video 测试集上跑 1 个 scene** → 测 PSNR / SSIM / LPIPS,作为 baseline
- **额外跑 1 个自采集小场景**(30 秒 6 视角同步)→ sanity check pipeline 端到端

**Go/Pivot 标准**:**PSNR ≥ 28 dB on D-NeRF subset**(`[推测,基于 4DGS abstract 直引]`"comparable or better than previous SOTA"。SOTA 在 D-NeRF synthetic 报 ~31 dB,我们设 28 为可接受下限)。
- **达到** → 进 M3
- **未达** → pivot:换 MonST3R 之外的 SfM(InstantSplat,见 `01- §3`)、调整采集方案(更多视角 / 更高帧率 / 更好同步)

**风险**:`02- §9.1` 第 6 项 4DGS Table 1 精确数字未在公开 abstract,**我们需要在 M2 内打开 PDF Table 1 拿确切数字**(代 `01- §11.1` 那条)。

**依赖**:MonST3R 仓库 / `hustvl/4DGaussians` / `docs/00-goal.md` §"采集:SfM + 多视角高速相机阵列"。

---

### M3 训练期 bitpack + 稀疏化(4 周)

**任务**(基于 `01- §7.3` 备选 2 + `02- §1` 步骤 1~2):
- **把 MEGA 训练管线(MEGA 仓库 `Xinjie-Q/MEGA`)** 集成到 M2 训练 pipeline,产出**带 color SH→3 参数 DC + shared AC** 的 4DGS 资源
- 在同样 D-NeRF 子集上对比带不带 MEGA:
  - 精度损失 ΔPSNR(`02- §3.1`)
  - 存储压缩比(目标:**~ 190× on Technicolor / ~125× on N3V**,**本数据集上是推测**)
  - 导出 `.ply` / 自定义格式的实际 MB

**Go/Pivot 标准**:**压缩后 PSNR 损失 < 1 dB**(暂定阈值,基于 MEGA 自报"comparable",**后续根据具体数据调整**)。
- **达到** → 进 M4
- **未达** → pivot:从 MEGA 切回原始 4DGS,在 inference 端用 Vulkan 编程做后训练 bitpack(路径 B)

**风险**:`02- §9.1` 第 3 项 — MEGA 190× 在本项目数据集成立性。

**依赖**:MEGA 仓库 + M2 训练流水线。

---

### M4 移动端 rendering pipeline(4 周)

**任务**(基于 `02- §7` Vulkan 1.3 实现细节草案):
- 在 Snapdragon 8 Gen 4 Reference Design / 消费级旗舰上跑 `02- §7.1` 那张 compute/fragment pipeline:
  - pre-frame compute: cull + decode + (on-tile) sort
  - per-tile render: splat.vert + splat.frag alpha blend
  - post-frame fragment: FSR / 输出
- **跑**的输入资源 = M3 产出的 MEGA bitpack 资源
- **目标**:**720p internal render(540p/720p 二选一)稳定 ≥ 15 FPS**(@ Adreno 830),**未上采样到 1080p**,这是只看原始 pipeline 的下限
- 测 feature flags:Vulkan 1.3 / `VkPhysicalDeviceTileShadingFeatures` / `storageBuffer16BitAccess` / `storageBuffer8BitAccess` —— **验证 M0 锁定的机型的实际 feature 列表**

**Go/Pivot 标准**:**720p internal ≥ 15 FPS**(`[推测,基于 02- §7.5]` 理论上限 80~160 FPS,M4 设下限 15 FPS,差距大则说明我们漏了关键成本,需要查 profiler):
- **达到** → 进 M5
- **< 15 FPS** → pivot:
  - **A.** 降 splat 上限(3M → 1.5M,牺牲精度换速度)
  - **B.** 改 on-tile sort → host-side sort(可能更快,取决于驱动)
  - **C.** 部分阶段下沉到 OpenGL ES 3.2 fragment shader(放弃 compute,降低编程复杂度)

**风险**:`02- §9.1` 第 4、5 项 — Adreno feature 差异 + Vulkan 1.3 on-tile compute 稳定性。

**依赖**:测试机 + MEGA 训练资源 + M2 baseline 数据。

---

### M5 上采样 + 优化(4 周)

**任务**(基于 `02- §5~§6`):
- 引入 FSR 2 / Arm ASR(`02- §6`) 720p internal → 1080p output
- **移植 4DGS-1K 的 temporal filter mask 到 Vulkan 1.3 + Adreno**(`paper-notes/2025-yuan-4dgs-1k.md §5.3`);**Spatial-Temporal Variation Score pruning 离线算法** + **Temporal Filter mask 跨帧复用(IoU ≈ 1)**
- **跑**同一段 30 秒测试场景,测:
  - **1080p ≥ 30 FPS**(目标下限)
  - 视觉质量 PSNR vs internal 1080p(基线)目标 loss < 0.5 dB

**Go/Pivot 标准**:**1080p ≥ 30 FPS, PSNR loss < 0.5 dB vs 同算法 1080p internal**:
- **达到** → 进 M6
- **< 30 FPS** → 把 internal render 降级(540p)或将 FSR 切到 quality → balanced 模式
- **PSNR 损失大** → 调整自研 mask 的 reuse ratio / 检查运动补偿错位

**风险**:`02- §9.1` 第 1 项 — 4DGS-1K 已找到(`arxiv:2503.16422`),**新风险**:**4DGS-1K 无 Vulkan / Adreno 移植实现,需 M3/M4 自研**(代码移植工作量大);`02- §9.2` FSR 2 / ASR 在 splatting 边缘的视觉质量需实测。

**依赖**:M4 pipeline + FSR / ASR SDK + `02- §5` §"5. 时空复用"。

---

### M6 实机 demo + 路线收口(2 周)

**任务**:
- 一段 60 FPS × 30 秒(连续)demo 视频 = 同一段 4DGS 场景在 Adreno 8 Gen 4 上的渲染回放
- 配合 1~2 个静态 demo(replay 不同时间戳)
- 写 README + 路线收口文档:
  - 已完成 vs 计划 vs 后续
  - SOTA baseline 对比:`4DGS abstract 82 FPS @ 800x800` vs **本项目 30~60 FPS @ 1080p on Adreno**(实际数字)
  - 后续可优化项(bit 字段更激进量化 / 训练策略 / 端到端 pipeline)

**Go/Pivot 标准**:30 秒 demo 跑通 = 整个路线成功。

---

## 3. 关键决策点(Gate Review)

每个里程碑完成后,**必须**开一次 Gate Review,做 go / pivot / kill 三分决策:

| Gate | 时点 | 决策标准 | 不能则的 pivot 路径 |
|---|---|---|---|
| **G0** | M0 末 | 测试机 feature OK + 桌面 GPU 跑得动 4DGS | 砍掉,只做学术研究 |
| **G1** | M1 末 | Vulkan pipeline @ 800p ≥ 30 FPS | 换 NVIDIA vk_gaussian_splatting wrapper / 换 Splatfacto 等替代 |
| **G2** | M2 末 | PSNR ≥ 28 dB on D-NeRF | 改采集方案 / 换 SfM |
| **G3** | M3 末 | MEGA 压缩后 loss < 1 dB | 改 inference 后训练 bitpack(路径 B) |
| **G4** | M4 末 | 720p internal ≥ 15 FPS | 降 splat 上限 / 改 sort 路径 |
| **G5** | M5 末 | 1080p ≥ 30 FPS, PSNR loss < 0.5 dB | internal 降级 / FSR balanced 模式 |
| **G6** | M6 末 | 30 秒 demo 跑通 | 收口归档,不进生产 |

---

## 4. 关键依赖(open vs close)

| 依赖 | 类型 | 状态 |
|---|---|---|
| **`hustvl/4DGaussians` 仓库**(Wu 4DGS) | open-source | 公开(`[abstract 直引]`) |
| **`Xinjie-Q/MEGA` 仓库**(MEGA) | open-source | 公开(`[abstract 直引]`) |
| **MonST3R**(动态 SfM) | open-source | 公开(`[abstract 直引]`,见 `01- §3`) |
| **NVIDIA `vk_gaussian_splatting`**(Vulkan baseline) | open-source | 公开(`[abstract 直引]`,见 `02- 附录 A`) |
| **`torbys/3DGS_App`**(uni-app 移动端 demo) | open-source | 公开(`[abstract 直引]`) |
| **FSR 2 / FSR 3 (MIT)** | open-source | 可商用(`[abstract 直引]`) |
| **Arm ASR** | open-source | 2025-03-24 全面开放(`[abstract 直引]`) |
| **`4DGS-1K` 公开论文(arxiv:2503.16422)** | ✅ **已找到**(2026-07-03) | Yuan et al., **NUS**, 2025-03-20,PDF 全文级 paper note 已写入[`paper-notes/2025-yuan-4dgs-1k.md`] |
| **Adreno SDK / 官方 mobile 4DGS demo** | 内部 | 需向 Qualcomm 申请 |
| **采集相机阵列(6 路 4K 60fps 工业相机)** | 硬件采购 | M0 锁定型号 |
| **Snapdragon 8 Gen 4 Reference Design** | 厂商 | 需向 Qualcomm 申请 |
| **测试消费级机(Xiaomi / Samsung 等)** | 现成 | 项目组自有 |

---

## 5. 资源预算

### 5.1 一次性

| 项 | 估算 | 备注 |
|---|---|---|
| 6 路 4K 60fps 工业相机 + 同步 trigger + 标定板 | ~ 80~120 万 KRW / 5~8 万 RMB | 国产大华 / 海康等同等档次 |
| Snapdragon 8 Gen 4 Reference Design | 内置 / 申请 | 某些团队可申请,我们看项目立项时再说 |
| 测试消费级机 × 1~2 | 1~3 万 RMB | 现成旗舰机,不一定新买 |
| 桌面训练 GPU(RTX 4090 + 64GB RAM + 2TB SSD) | 已购置或采购 | 2~4 万 RMB |
| 桌面 Vulkan baseline 测试机 | 与训练机共用 | — |

### 5.2 持续性

| 项 | 月估算 | 备注 |
|---|---|---|
| 训练算力(单 GPU × 24/7 × 1 个月 ≈ 720 GPU-hour) | 已包含在训练机折旧 | — |
| 云 GPU 备用(A100 / H100 类) | 0~2 万 RMB / 月,看是否扩容 | M3 后视情况启用 |
| 测试机折旧 + OTA 测试 | 不计 | — |

### 5.3 人力

| 角色 | FTE 估算 | 备注 |
|---|---|---|
| 主程(图形 / Vulkan 经验) | 1.0 | 全程 |
| 训练 pipeline 工程师(可选) | 0.5(M2~M3) | — |
| 采集现场(2 人) | 0.2(M2) | 一次性 |
| 项目负责人 | 0.2 | 全程 |

合计 ~ 1.5~2.0 FTE × 6 个月。

---

## 6. 风险点与回退方案(整体复盘)

| 风险 | 触发条件 | 回退路径 |
|---|---|---|
| ✅ **4DGS-1K 论文已找到 (`arxiv:2503.16422`)** | n/a | 移植 + 实测风险交 M3/M4(无 Vulkan/Adreno 实现) |
| **Adreno 8 Gen 4 上 4DGS FPS 不达 30** `02- §9.1.2` | G4 / G5 不达标 | 降低 splat 上限(3M → 1.5M → 1M),牺牲精度换速度;**这是这个项目的最大单点风险** |
| **MEGA 190× 压缩在本数据集不成立** `02- §9.1.3` | G3 PSNR 损失大 | 改走 inference 后训练 bitpack(训练不感知,部署期量化) |
| **Adreno fp16 / 8-bit storage feature 部分机型缺** `02- §9.1.4` | M4 跑 fp16 兼容性测试失败 | 自动 fallback fp32,接受 50% 显存涨 |
| **Vulkan 1.3 on-tile compute 驱动不稳** `02- §9.1.5` | M4 跑稳定性测试崩溃 | 改 host-side sort(可能 1.5~2× 慢,但稳定) |
| **采集相机阵列同步误差大** `01- §12.2` | M2 自采集数据 motion blur / 时间错位 | 加硬件 trigger / 改帧率(60 → 30 fps / 视角) |
| **PSR / PSNR Table 数字核到与 abstract 对不上** `02- §9.1.6` | M2 实测低于预期 | 跑 cross-validation on D-NeRF + Plenoptic Video,把 baseline 重新对一遍 |

---

## 7. MVP 定义

**什么是最简可用 demo**(M6 末必须跑通的最小版本):

> 在 **一台 Snapdragon 8 Gen 4 消费级机**(如 Xiaomi 14 Ultra)上,**单段 30 秒(900 帧)4DGS 场景**,1080p 全屏渲染,**30~60 FPS**,视觉上**接近 M1 桌面 Vulkan baseline 的 800×800 渲染**(分辨率差,但 splat 分布、动起来时一致)。
>
> **不要求**:
> - 多场景切换
> - 用户交互(视角 / 时间)
> - 上采样质量可调档
> - 训练 pipeline 在线(M0~M3 已离线训完)
>
> **要求**:
> - 解码 30 s 不崩
> - 帧时间方差 < 5 ms
> - 上采样 1080p 视觉质量肉眼可接受

---

## 8. 后续可优化项(M6 之后)

不在本次 6 个月路线内,但记录下来供下一阶段讨论:

1. **训练期更激进 bitpack**(per-field 自适应位宽,非固定 8/16)
2. **end-to-end 训练感知 bitpack**(deformation MLP 内嵌 quantization aware training)
3. **动态码率**(ROI 区域高密度,非 ROI 区域稀疏到 ~ 1M splats)
4. **on-device 增量训练**(场景更新用 on-device 短训练而不全重训)
5. **多观察点支持**(同一场景 6 视角相机阵列 → 1 个共享 splat 池,降低总储量)
6. **6-DoF 实时交互**(用户滑动手机模拟相机运动,联动 `02- §6` → `01- §4` 联合视角优化)

---

## 9. 本路线图不解决的事

| 问题 | 在哪 | 备注 |
|---|---|---|
| 4DGS-1K 公开论文 | ~~`02- §9.1.1`~~ | ✅ **2026-07-03 已找到**(`arxiv:2503.16422`) |
| Adreno 8 Gen 4 上 4DGS FPS 实测 baseline | `02- §9.1.2` | 没有公开实现,**我们 M1 / M4 自己跑出来** |
| 移动端 4DGS 在 4K 上的可行性 | 不在范围 | `00-goal.md` §"硬约束"明确 1080p |
| 多 GPU 训练 / 大模型训练优化 | 不在本路线 | 桌面 RTX 4090 / A100 单卡训练够用 |
| 服务器侧 streaming 4DGS / 用户侧缓存 | 不在本路线 | 业务侧问题,本路线图只解决渲染端 |

---

## 10. 引用一览

本文件直接复用了以下内部 / 外部来源:

| 来源 | 引用 |
|---|---|
| `docs/00-goal.md` | 全程 |
| `docs/01-high-precision-representation.md` §7、§8 | M2 / M3 / §6 风险 |
| `docs/02-rendering-acceleration.md` §1、§3、§5、§6、§7、§9 | M1 / M3 / M4 / M5 / §6 风险 |
| `docs/appendix/paper-notes/2024-wu-4dgs.md` | M1 / §6 风险 |
| `docs/appendix/paper-notes/2023-yang-deformable-3dgs.md` | M2 (备选 1) |
| `docs/appendix/paper-notes/2023-attal-hyperreel.md` | M5 (Vulkan 实现思路) |
| `docs/appendix/paper-notes/2024-zhang-mega-4dgs-acceleration.md` | M3 主线 + §6 风险 |
| `docs/appendix/vulkan-impl-notes.md`(占位,待填) | M1 / M4 |
| `docs/appendix/collection-sop.md`(占位,待填) | M0 / M2 |
| NVIDIA `vk_gaussian_splatting` 仓库 | M1 |
| `hustvl/4DGaussians` 仓库 | M1 / M2 |
| `Xinjie-Q/MEGA` 仓库 | M3 |
| MonST3R(动态 SfM) | M2 |
| `torbys/3DGS_App`(移动端 3DGS demo) | M4(借鉴) |
| FSR 2 / FSR 3 (MIT) | M5 |
| Arm ASR | M5 |

---

**写在最后**:本路线图**全部数字与时间估算均带"推测"或"调研不足"标记**。**M0 立项 → M1 桌面 baseline** 是本路线图可信度最高的起点,后续 M2~M6 的具体时间表**只有走到对应里程碑时才回收真实数据并更新本文件**。`[02- §9]` 列出的所有风险,**没有一条已经在公开材料里被去掉**—— 这是本路线图必须接受的前提。
