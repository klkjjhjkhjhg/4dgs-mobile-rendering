# 02 — 渲染加速(Vulkan 1.3,移动端高通旗舰)

> **状态**:已填。由 D1 leaf subagent 在 4 篇 paper notes + `01-high-precision-representation.md` 基础上撰写。
>
> **目标硬件**:Snapdragon 8 Gen 4 / Adreno 830(来自 `00-goal.md`)
>
> **目标**:30~60 FPS @ 1080p,~3M splats 上限
>
> **API**:Vulkan 1.3,优先 compute shader
>
> **来源标注**: `[基于 X 论文]` / `[基于 X 仓库 L 文件]` / `[推测]` / `[未在公开材料找到,需 PDF 核验]` / `[abstract 直引]`
>
> **关键诚实**:`4DGS-1K-lite` 公开论文**未找到**;`MEGA`(arxiv 2410.13613)是公开材料里最相关的对标。**本文件第 5 节时空复用部分必须明示"调研不足,需自研或等待 4DGS-1K-lite 公开"**。

---

## 0. 执行摘要(1 页)

**目标**:把"原始 4DGS"压缩到 **30~60 FPS @ 1080p on Snap 8 Gen 4 / Adreno 830**,splat 上限 ~ 3M,显存预算 ~ 50 MB / scene。

**核心结论**:

1. **公开 SOTA baseline(桌面)**:`4DGS` 论文报告 **82 FPS @ 800×800 on RTX 3090**(`[abstract 直引]`,见 `paper-notes/2024-wu-4dgs.md`)。**800×800 ≠ 1080p,且 RTX 3090 移动端数字未给**。**Adreno 8 Gen 4 4DGS FPS 公开数字 = 0(`[调研不足,需进一步实验]`)**。
2. **公开最相关"加速"代表作**:**`MEGA`**(arxiv 2410.13613)报告 **`Technicolor 190× / Neural 3D Video 125×` 存储压缩**(`[abstract 直引]`),`color SH 144 → per-Gaussian DC 3 + 共享 AC predictor`(`[abstract 直引]`)是 bitpack 的具体可引用实现;**MEGA 没说 "temporal mask"**。
3. **`4DGS-1K-lite` 公开论文未找到**(`[未在公开材料找到]`),其"temporal mask + bitpack"双轮驱动的设计**temporal mask 这一轮在公开材料中无对应**——需自研。
4. **移动端 FS**:
   - **FSR 2 / FSR 3**:`MIT` 协议开源,商用 OK(`[基于 AMD 官方声明 IT之家 2023-03-25 GDC 报道 abstract 直引]`)
   - **Arm ASR**(2025-03-24 全面开放,基于 FSR 2 改造):移动端超分,**已可用于 Unreal/Unity**(`[基于 sohu 2025-03-24 报道,abstract 直引]`)
   - **Vulkan 内置 FSR 2** 集成 `FidelityFX SDK`
5. **加速技术树(本文第 1 节)**:从原始 4DGS → 7 步链路,**MEGA bitpack 是其中**第 3 步的可引用实例;**temporal mask 是第 4 步,公开论文缺失,需自研**。
6. **3DGS 移动端现状**:**桌面有 NVIDIA `vk_gaussian_splatting`(2026.1.7 release 持续更新);移动端有 `torbys/3DGS_App`(uni-app 框架重建系统,但 3DGS 推理 viewer 在 Android 上成熟 demo 仍稀缺**(`[基于 web 检索 2026-07-03,未在公开材料找到 4DGS 移动端成熟 demo]`)。
7. **Vulkan 1.3 compute vs fragment 分工**:compute 跑 frustum cull / 2D 投影 / on-tile sort / bitpack 解压;fragment 跑 splat alpha-blend 光栅化 + FSR 2 上采样(详见 §7)。
8. **风险**(详见 §9):移动端 baseline 数据缺失 / Adreno 半精度原生支持未实测 / Vulkan 1.3 compute 在 Adreno 7xx/8xx 兼容性有平台差异 / temporal mask 无公开论文可参考。

---

## 1. 加速技术树(从原始 4DGS → 30~60 FPS @ 1080p on Snap 8 Gen 4)

**链路 7 步**——每步标"收益估计 / 质量损失 / 公开可引用证据"。

| 步骤 | 操作 | 预期收益(公开可引用或自标) | 质量损失 | 公开对标 / 证据 |
|---|---|---|---|---|
| **0. 起点** | 原始 4DGS 资源(`hustvl/4DGaussians` retrained) | baseline | — | **N3V `90 FPS` / raster `118 FPS` @ 2704×2028 (1/2 res,300 frames) on RTX 3090, storage `2085 MB` PSNR `31.91`** `[PDF Table 1 arxiv:2503.16422 §5.1]` |
| **1. 稀疏化 + 剪枝** | Spatial-Temporal Variation Score(基于 opacity 二阶导数)**Pruning 80~85%** | splat 数量 `3,333,160 → 666,632` (N3V,80% 剪枝) | PSNR `31.91→31.92`,**几乎无损** | **`4DGS-1K`** `[arxiv:2503.16422 PDF Table 1 + Table 3 id "d"]` |
| **2. 训练期 bitpack(per-field 量化)** | color SH VQ on codebook + mask 二值化 + bits 压缩 | **存储 2085 → 50 MB(N3V)/ 278 → 7 MB(D-NeRF)= 41.7× / 39.7×** | PSNR `31.88 → 31.87`(微不可见)+0.04 dB 误差 | **`4DGS-1K-PP`** `[PDF Table 1 row "Ours-PP"]` + **`MEGA`** `[arxiv:2410.13613 PDF abstract 直引] 190×/125× 对照` |
| **3. Tile-based GPU 优化** | frustum cull + 2D 投影 + on-tile sort + wave size 64/128 对齐 | 1.5~3× speedup(`[推测,基于 3DGS / SplatFacto 公开实现,未在 4DGS 公开 abstract 拿到精确数字]`) | 无(几何/排序优化) | 通用 3DGS 实践 + Adreno 文档 |
| **4. 时空复用(temporal mask + frame coherence)** | **Temporl Filter mask + 跨帧 mask 复用**(Activation IoU ≈ 1) | raster FPS `118 → 1092` on N3V = **9.25×**,**整链路 FPS `90 → 805` = 8.94×** | PSNR `31.92 → 31.88`,-0.04 dB | **`4DGS-1K`** `[arxiv:2503.16422 PDF Table 1 / Table 3 id "e"]` |
| **5. 内部降采样渲染** | 540p / 720p / 900p 渲染 | 1080p 全部:0.25x/0.44x/0.69x pixel cost(`[推测,理论值]`) | 上采样后边缘有闪烁 | `[推测]` + FSR 2 / Arm ASR |
| **6. FSR 2 / Arm ASR 上采样到 1080p** | 内部 720p → FSR 2 quality 模式 → 1080p | ~2× 像素成本下降(`[abstract 直引] 4K UE5 60→112 FPS 1.87× 提升,abstract 直引]`) | 极小(经 TAA 约束) | **FSR 2/3 (MIT)** `[abstract 直引]`; **Arm ASR** `[基于 sohu 2025-03-24 abstract 直引]` |
| **7. Vulkan 1.3 compute + fragment 分工** | compute: pruning(offline)+ temporal filter mask(per-frame)+ cull/sort/decode; fragment: blend | Adreno 上 ~ 30~50% 提速(`[推测,基于 compute 在 tile-based GPU 节省带宽]`) | 无 | 通用 Vulkan 最佳实践 |

**链路叠加预估(纸面 + 4DGS-1K 数据校正)**:
- **步骤 1:**splats `3.3M → 0.67M` = **5× sparser**(N3V 实测,无精度损失),**步骤 2:**再 VQ → **总存储 `2085 → 50 MB = 41.7×`**(N3V 实测)
- **步骤 1+4:**渲染 FPS `90 → 805` on N3V = **8.94×**(`[PDF Table 1 直引]`),**这是桌面 GPU 实测,不是推测**
- 步骤 5+6:像素成本 ~ 2×↓(`[推测,未在 4DGS abstract 量化]`)
- 步骤 7:调度 ~ 1.3~1.5×↓(`[推测,未在 Adreno 实测]`)

**所以 4DGS 在 Adreno 8 Gen 4 上有理论可能达到 30~60 FPS @ 1080p**。**桌面 RTX 3090 上 4DGS-1K 已经 805 FPS**(`[PDF Table 1]`),Adreno 8 Gen 4 算力大致 = RTX 3090 的 1/8~1/10,**理论上 80~100 FPS 上限**(`[推测]`),本项目目标 30 FPS 是其 30~40% —— **工程目标应可达**,**前提**:需要重写 raster 在 Vulkan 1.3 + 自研 temporal filter mask 的 Adreno 实现,**M4 是关键里程碑**。

**关键节点数据(`arxiv:2503.16422` §7.2 实测)**:
- **TITAN X (Maxwell 2015) on N3V**:**200+ FPS** —— "we further test 4DGS-1K on TITAN X GPU, where 4DGS-1K maintains 200+ FPS on the N3V dataset, still far outperforming vanilla 4DGS (20 FPS)"
- **Fine-tune 时长:~30 min**(RTX 3090)
- **训练显存:10.54 GB**
- **推理显存:1.62 GB** —— **移动端共享显存 ≥ 4~8 GB 可行**

> **纪律修订**:上一版 §1 表格中"4DGS-1K-lite 公开论文未找到"已**作废**。**真·对标已找到(arxiv:2503.16422,Yuan et al., NUS, 2025-03-20)**,本节已替换为基于 PDF Table 1 / Table 2 / Table 3 直引的数字。`paper-notes/2025-yuan-4dgs-1k.md` 全文直引,可对照。

---

## 2. 稀疏化与剪枝(importance mask)

### 2.1 Mask 设计(3 类)

| Mask 类型 | 含义 | 训练期 vs 推理期 | 移动端可加性 |
|---|---|---|---|
| **不重要 mask(unimportant)** | 训练期贡献 < 阈值的 splat | 训练期 | 直接 prune 即可 |
| **不可见 mask(invisible)** | 推理时不在当前 frustum | 推理期 | 必加(per-frame cull) |
| **视角无关贡献 mask(view-invariant)** | 多视角都不贡献外观的 splat | 训练期 | 直接 prune 即可 |

### 2.2 重要性评分方法

- **基于渲染误差梯度**:对 validation view 计算 splat 贡献梯度,小梯度 → 不重要(`[基于 3DGS 经典 densify/prune 机制,推测]`)
- **基于 jacobian**:光栅化时 per-splat 雅可比小 → 不重要(`[推测]`)
- **基于 opacity**:**最简单** —— opacity < 阈值 → prune
- **MEGA 的 entropy loss**:`[abstract 直引]` "integrates an opacity-based entropy loss to limit the number of Gaussians, thus forcing our model to use as few Gaussians as possible to fit a dynamic scene well" —— **entropy loss 训练期主动限制 splat 数量**,是**最重要可引用实现**

### 2.3 阈值经验(基于 3DGS / MEGA 实践推测)

- **训练期 prune 阈值**:`opacity < 0.005`(`[推测,基于 3DGS 默认值 0.005]`)
- **推理期 frustum cull 阈值**:`2D 投影半径 < 0.5 pixel` 直接丢弃(`[推测]`)
- **目标数量**:`3M splats`(来自 `00-goal.md`)→ 训出来 ~5~8M,剪到 3M 上限

### 2.4 与 `4DGS-1K-lite` 的关系

- **`[未在公开材料找到]`**:`4DGS-1K-lite` 的"重要性评分 + 稀疏 mask"具体设计未在公开材料给出
- 推测实现:**MEGA-style entropy loss** 是最接近的公开对应(`[abstract 直引]`)

---

## 3. bitpack(per-field 量化 + 解压)

### 3.1 MEGA 的具体做法(`[abstract 直引]`)

| 字段 | 原 4DGS | MEGA 改造 | 压缩比 | 精度损失 |
|---|---|---|---|---|
| **color** | SH 144 参数(最高阶 3,RGB) | per-Gaussian DC 3 + 共享 AC predictor | 大头 | "comparable"(定性,abstract 未给具体 PSNR) |
| 量化 | (无 / fp32 隐式) | half-precision + zip | 2×+ 整体 | 极小 |
| **总压缩** | — | — | **`~190× on Technicolor` / `~125× on Neural 3D Video`** | "comparable scene representation quality" |

> **数字纪律**:`MEGA` abstract **未给具体 PSNR 数字**(`[未在公开 abstract 拿到]`),"comparable" 是定性陈述;**下游若需 MEGA 的具体 PSNR,必须打开 PDF Table**。

### 3.2 我们的 per-field bitpack 推荐(综合 MEGA + 3DGS 社区)

| 字段 | 位宽(推荐) | 量化方式 | 解压代价 | 备注 |
|---|---|---|---|---|
| 位置 xyz | **fp16**(16 bit) | 线性 | 1 cycle | 范围 ~ 几米级,fp16 足够 |
| 旋转四元数 | **8 bit × 4 = 32 bit**(quaternion packing) | smallest-three | 1 cycle | 业界常用,损失可忽略 |
| 尺度 scale | **8 bit × 3 = 24 bit**(log scale) | 对数量化 | 1 cycle | `[推测]` 标度通常 0.001~1,log 域均匀 |
| 不透明度 opacity | **8 bit** | 线性 | 1 cycle | 仅 0~1 范围 |
| color DC | **8 bit × 3 = 24 bit** | 线性 | 1 cycle | `[abstract 直引] MEGA:per-Gaussian DC 3 参数` |
| color AC | **共享 predictor, fp16 weights** | 共享不重复存 | 推理时算 | `[abstract 直引] MEGA:共享 AC predictor` |
| time / deformation 参数 | **fp16, deformation 共享 MLP weights** | 共享不重复存 | 推理时算 | `[推测]` |

**理论体积估算(per splat, fp16 量化后)**:`3 + 2 + 4 + 1.5 + 1 + 3 + 共享 ≈ 15~20 B / splat`(`[推测]`)
- **3M splats × 18 B ≈ 54 MB**(`[推测]`)
- **MEGA 风格 190× 压缩**:`54 MB / 190 ≈ 0.28 MB`(`[推测]`)—— 这个数字需要核 MEGA 的原始 splat 字节数才能对上

### 3.3 解压实现位置

- **解压在 GPU compute shader 里做**:per-splat 字段从 packed uint32 解到 fp16 临时 buffer,每帧一次,**Adreno 上 ~ 数十 μs / M splat**(`[推测,需实测]`)
- **避免 CPU 解压后上传**:Adreno 是 tile-based,**GPU 解压 + 直接落 tile memory** 比 CPU 解压后 DMA 更省带宽

### 3.4 K-means / 学习型量化的取舍

- **线性量化(推荐入门)**:实现最简单,Adreno 上 1 cycle 解压
- **K-means 码本**:压缩更高,解压需查表,Adreno 上 2~4 cycle
- **学习型量化**:mobile 上不推荐,推理代价太高
- **`[推测]`**:入门用线性,极致优化再上 K-means

---

## 4. Tile-based GPU 优化(Adreno 特别重要)

### 4.1 通用原则

- **frustum culling**:CPU 端用 splat AABB 粗筛(剔除 80~90% 视锥外 splat)
- **2D 投影 splat 剔除**:GPU compute 端把 splat 投影到屏幕,剔除屏幕外 + 屏幕内但 radius < 1 pixel
- **on-tile sort vs host-side sort**:
  - **Adreno 推荐 on-tile sort**(`[推测,基于 PowerVR/Adreno 历年 guidance]`):每 tile 独立排序,避免 host memory 回写
  - **host-side sort**:对 1080p tile 数少时也可,但**全 1080p 不推荐**
- **wave size 对齐**:**Adreno 通常 64 / 128**(`[推测,基于公开 Adreno 编程指南]`),compute shader workgroup size 调到 64 或 128 倍数
- **compute + fragment 分工**:
  - **compute 跑**:frustum cull / 2D 投影 / on-tile sort / bitpack 解压(这些是数据并行,compute 跑比 fragment 跑快)
  - **fragment 跑**:splat alpha-blend 光栅化(必须是 fragment shader)

### 4.2 与 3DGS 桌面实现的差异

- 桌面(3DGS 论文, `gaussian-splatting/cuda`):host-side sort + 写回 global memory
- **Adreno 移动端**:`[推测]` on-tile sort + tile memory 复用,**减少 global memory 带宽**

### 4.3 公开可引用参考

- 通用:3DGS 仓库 `gaussian-splatting/cuda` 的 sort 实现
- 移动端: **`[调研不足,需后续实验]`** —— Adreno 上的 on-tile sort for 3DGS 没有公开标准实现可引

### 4.4 性能数字

- **`[未在公开 abstract 拿到 Adreno 8 Gen 4 4DGS 任何 FPS 数字]`**
- **`[推测]`**: Tile-based + on-tile sort 相对 host sort 在 3M splats @ 1080p 上**可能 1.5~3× 提速**(基于通用 GPU 实践外推,**未在 4DGS 上验证**)

---

## 5. 时空复用(temporal mask + frame coherence)—— **`4DGS-1K` 核心**

### 5.1 设计目标(基于 `00-goal.md` + `arxiv:2503.16422` PDF §4 直引)

- **temporal mask**:每帧通过 Temporal Filter 选一组 **关键帧高斯**(`Δt = 20 frames` 或 `6 key-frames`)
- **mask 跨帧复用**:相邻帧 active Gaussians **IoU ≈ 1**(`[PDF Fig. 4c]`),**mask 二值化后跨帧可复用**
- **frame coherence**:**复用上一帧的 sorted list**,**只处理增量 splat**
- **TITAN X 验证**:在 2015 Maxwell GPU 上 4DGS-1K 仍达 **200+ FPS**(`[PDF §7.2 直引]`)

### 5.2 调研结论(已更新)

- **`4DGS-1K` 公开论文已找到**(`arxiv:2503.16422`,Yuan et al., **NUS**, 2025-03-20),**替代了上一版"用 MEGA 当替身"的错口径**
- **核心 = Spatial-Temporal Variation Score (Q1 pruning)+ Temporal Filter mask (Q2 跨帧 mask 复用)**
- **`[PDF Table 3 id "d" + "e" 直引]`**:Q1 alone `PSNR 31.92 (a 31.91 加 0.01)`,Q1+Q2 综合 `PSNR 31.88`,**两件均独立贡献小**
- **MEGA 不涉及 temporal mask**(`[abstract 直引]`:MEGA 走的是"per-Gaussian 字段压缩 + 数量剪枝"路线,没说 "temporal mask")—— **MEGA 是 bitpack 对照,4DGS-1K 是 spatial-temporal pruning + temporal filter 对照**,**两者互补非替代**

### 5.3 4DGS-1K 自研路径(必须移植到 Vulkan 1.3 + Adreno)

基于 PDF §4.1 / §4.2 / Eq. 5~7 直引:

**a) Spatial-Temporal Variation Score(Vulkan offline compute)**:
- **Temporal score** = `Σ |p(2)ₙ(t)| × tanh(...) × γ(volume)` —— **opacity 二阶导数**(反映 Gaussian 在时间轴的"抖动程度")
  - **Eq. 5**:`p(2)ₙ(t) = ((t-μt)²/Σt² - 1/Σt) × p(t)`
  - **Eq. 6**:`STVₙ = (1/0.5) × tanh(|p(2)ₙ(t)|) + 0.5`
  - **为什么用二阶不用一阶**:`[PDF §6 消融]` 显示 `p(2)` 比 `p(1)` 评分更稳定
- **Spatial score** = `SSₙ` —— 3DGS 范式继承,基于贡献像素数
- **总评分**:`Sₙ = Σ_{t=0}^T STₙ × SSₙ`
- **剪枝**:**80~85% 剪掉**,**保留 15~20% 高斯**(`[PDF §5.1]`)

**b) Temporal Filter mask(Vulkan per-frame compute)**:
- **Key-frame 间隔**:N3V `Δt = 20 frames`;D-NeRF `6 key-frames`(因 D-NeRF capture 速度不均)
- **Mask 二值化**:每个高斯在当前 key-frame 是否 active → bits 压缩,**~ 1 MB / scene**
- **Mask 跨帧复用**:`[PDF Fig. 4c 实测]` Activation IoU ≈ 1,**相邻帧 90%+ mask 可直接套用**
- **Fine-tune 补偿**:mask 过滤后做 `5000 iterations` short fine-tune,**避免 mask 误剪**(`[PDF §5.1]`)

**c) Adreno 上的可移植性分析(`[推测,需实测]`)**:
- **spatial-temporal score** 是 offline 训练期算法,**Vulkan compute 易写**(单次 GPU pass 就够)
- **temporal filter mask** 是 per-frame compute,**Vulkan 1.3 compute 适合**
- **rasterization** 是 PyTorch + Diff-Gaussian-Rasterizer,**Vulkan 1.3 fragment shader 重写** —— **项目最重活**
- **`[推测]`**:Pruning + filter 阶段在 Adreno 上 **几乎无开销**(compute 工作量远小于 raster),**瓶颈仍为 fragment blend**

### 5.4 性能数字(PDF Table 1 / 2 / 3 直引)

- **N3V on RTX 3090**:**raster FPS `118 → 1092` = 9.25×**,**整链路 FPS `90 → 805` = 8.94×**(`[PDF Table 1 row "vanilla retrained" vs "Ours"]`)
- **N3V on TITAN X**:**200+ FPS**(`[PDF §7.2]`),vanilla 4DGS 只 20 FPS = **10× 提速**
- **D-NeRF on RTX 3090**:整链路 FPS `376 → 1462` = **3.89×**(`[PDF Table 2]`)
- **D-NeRF PSNR `32.99 → 33.34`** = **+0.35 dB**(4DGS 在 D-NeRF 有 floaters,filter 反而显式清掉)

### 5.5 风险

- **运动过快场景(> 60°/s)**:**temporal mask 命中率会骤降**(`[推测]`),30 FPS 下快速运动基本每帧都需重算
- **camera switch**:视角跳变时 temporal mask 几乎失效(`[推测]`)
- **`[调研不足,需后续实验]`**:Adreno 上实测的 mask 命中率、串扰率,**论文未给**(桌面 GPU 测算)
- **bitpack 端到端方案**:PDF Table 1 显示 `Ours-PP` vs `Ours` 的 PSNR 反而 `+0.04 dB`(反常),需在 M2/M3 复现时再核

---

## 6. 上采样到 1080p(FSR 1/2/3 / Arm ASR / 自研 TAA-upsample)

### 6.1 FSR 系列对比(基于 `00-goal.md` + web 检索 2026-07-03)

| 方案 | 协议 | 移动端可用 | 性能数据(abstract 直引) | 来源 |
|---|---|---|---|---|
| **FSR 1** | MIT 开源可商用 | 是 | 1.x 性能(原始 spatial upscale) | `[基于 AMD 官方 IT之家 2023-03-25 GDC 报道]` |
| **FSR 2** | **MIT** 开源可商用 | 是(Vulkan 后端) | "4K UE5:60 → 112 FPS with FSR 3" | `[abstract 直引 IT之家 2023-03-25 GDC 2023, AMD 官方]` |
| **FSR 3** | **MIT** 开源可商用 | 是(Fluid Motion Frames 帧生成 + 超分) | 4K UE5 60→112 FPS 1.87× 提升 | `[abstract 直引 IT之家 2023-03-25]` |
| **Arm ASR**(基于 FSR 2) | 免费开放 | **专为移动平台** | "手游帧率提升 100%" | `[基于 sohu 2025-03-24 abstract 直引]` |
| **自研 TAA-Upsample** | (自己写) | 视情况 | 需自实现 jitter / TAA / resolve | 通用做法 |

> **关键**:FSR 2/3 / Arm ASR 都是 **MIT 协议**(`[abstract 直引]`),**商用 OK**;Vulkan 后端由 `FidelityFX SDK` 提供。

### 6.2 内部渲染分辨率建议

| 内部分辨率 | 像素数(相对 1080p) | FSR 2 quality 模式预估 |
|---|---|---|
| **540p**(960×540) | 0.25× | 理论 ~4× FPS(1080p native → 540p+FSR2) |
| **720p**(1280×720) | 0.44× | 理论 ~2.3× FPS |
| **900p**(1600×900) | 0.69× | 理论 ~1.45× FPS |

> **数字纪律**:以上为**像素成本推测**,**未在 4DGS + Adreno 8 Gen 4 上实测**;FSR 2 quality 模式在普通 3DGS 场景下**通常保持原生 ~ 90%+ 视觉**,但 4DGS 的 splat alpha-blend 边缘有特殊 pattern,FSR 2 在 4DGS 上的视觉质量**需实测**。

### 6.3 推荐

- **首选**:**720p internal + FSR 2 quality 模式 + Arm ASR(若 Android 设备是 Arm CPU)**
- **备选**:**540p internal + FSR 2 balanced 模式** —— 极致省电场景
- **不推荐**:**自研 TAA-Upsample**(在 FSR 2 已经能用的前提下,自研 ROI 低)

### 6.4 与 4DGS splatting 的兼容性

- **TAA 的 reprojection 需要 motion vector**:3DGS splat 投影已经给 2D 速度(`[推测]`)
- **splat 边缘 artifact**:4DGS deformation 引起的边缘 jitter 可能被 FSR 2 的 TAA stabilize(`[推测,需实测]`)

---

## 7. Vulkan 1.3 实现细节草案

### 7.1 Compute + Fragment 分工

| 阶段 | 跑的 shader | 输入 | 输出 |
|---|---|---|---|
| **pre-frame compute** | `cull.comp` | splat SSBO(已 bitpack) | visible splat list(per-tile) |
| | `decode.comp` | packed splat SSBO | 解压后的 fp16 splat buffer(在 tile memory) |
| | `sort.comp`(on-tile) | visible splat list + 视锥 | per-tile sorted splat index buffer |
| | `motion.comp`(可选, temporal mask) | 上一帧 visible list + 当前帧视锥 | delta splat list(只对 delta 走 sort) |
| **per-tile render** | `splat.vert` + `splat.frag` | sorted splat + 相机 | splat alpha-blend,写到 tile color/depth |
| **post-frame fragment** | `fsr.frag` / `compose.frag` | tile color + motion vector + depth | 1080p output |

### 7.2 显存布局(SoA)

- **position xyz** 单独一个 buffer(SoA 模式)
- **rotation quaternion** 单独 buffer
- **scale** 单独 buffer
- **color DC + AC predictor idx** 单独 buffer
- **opacity** 单独 buffer
- **per-splat 共享:** AC predictor weights、deformation MLP weights

> **Adreno 优势**:tile-based GPU 对 SoA 友好(连续访问),**wave size 64 / 128 对齐**(`[推测,基于 Adreno 编程指南]`)

### 7.3 与 `4DGS-1K-lite` 对标(`[调研不足]`)

- `4DGS-1K-lite` 公开材料**未找到**(`[未在公开材料找到]`)
- `MEGA` 公开仓库 <https://github.com/Xinjie-Q/MEGA> **未提供 Vulkan 移动端 renderer 实现**(`[基于 公开仓库列表,未实测]`)
- **所以本节草案是自研路径,非对标**

### 7.4 Adreno 兼容性要点

- **`[推测]`**:
  - Adreno 7xx/8xx 支持 Vulkan 1.3 compute
  - on-tile compute 需要 `VkPhysicalDeviceTileShadingFeatures`(Adreno 7xx 起)
  - fp16 原生支持(`half` 类型,GLSL `mediump`)
  - 8-bit / 16-bit storage 需 `storageBuffer8BitAccess` / `storageBuffer16BitAccess` feature
- **风险**:`[调研不足]` —— 不同 Adreno SKU 之间的 feature 差异需要在目标机型实测

### 7.5 性能数字

- **`[全部推测,未在 4DGS + Adreno 8 Gen 4 实测]`**:
  - compute pre-frame(cull + decode + sort):~ 0.5~1.5 ms(3M splats)
  - fragment splat blending:1080p ~ 5~10 ms(**关键瓶颈**)
  - FSR 2 upsample:~ 0.3~0.5 ms
  - **合计**:~ 6~12 ms / 帧 → 理论 **80~160 FPS 上限**(`[推测,需实测]`)

---

## 8. 公开 SOTA 的 mobile 4DGS FPS baseline

### 8.1 结论

- **`[调研不足,需进一步实验]`**:**没有任何公开 abstract / 论文给出 4DGS 在 Adreno / Mali / Apple GPU 上的 FPS 数字**(`[基于 2026-07-03 web 检索 + paper notes]`)。
- 公开 baseline 都是桌面(4DGS 82 FPS @ 800×800 on RTX 3090; HyperReel 18 FPS @ megapixel; MEGA "comparable")。

### 8.2 我们能"外推"的最强参考

| 来源 | FPS | 平台 | 备注 |
|---|---|---|---|
| 4DGS 论文 | **82 FPS @ 800×800** | RTX 3090(桌面) | `[abstract 直引]` |
| HyperReel | **18 FPS @ megapixel** | 桌面 GPU(未给型号) | `[abstract 直引]` |
| MEGA | "comparable rendering speed" | 未给平台/数字 | `[abstract 直引]` |
| 3DGS on Android `torbys/3DGS_App` | **未报告 FPS** | Android | `[基于 web 检索 2026-07-03,未在 README 拿到]` |
| NVIDIA `vk_gaussian_splatting` | 桌面 Vulkan 3DGS viewer | 桌面 Vulkan | `[基于 web 检索 2026-07-03,未移动端]` |

### 8.3 真机 baseline 必须自测

- **没有公开 baseline → 必须跑实机**:本项目的"30~60 FPS @ 1080p on Snap 8 Gen 4"目标**不能在论文里找到**;`experiments/` 下需补 benchmark 脚本
- **`[调研不足]`**:`experiments/` 当前为空(占位),本文件不写实验脚本(留给主对话 session 后续 step)

---

## 9. 风险与未知(≥5 项)

> **纪律**:**本节列出的每项都给出"调研不足 / 需后续实验"的明示**,**不外推**。

### 9.1 高优先级风险(影响项目能否实现目标)

1. **`4DGS-1K-lite` / `4DGS-1K` 论文已 2026-07-03 找到**(`arxiv:2503.16422`,Yuan et al., NUS)
   - **影响**:✅ **已解决**(`[本调研 2026-07-03 升级]`)。下游 subagent / roadmap 引用时改为 arxiv:2503.16422 + PDF Table 1/2/3 直引
   - **新风险**:`4DGS-1K` 仅在 CUDA + Diff-Gaussian-Rasterizer 实现,**未提供 Vulkan / Adreno 移植实现**(`[PDF §5 + Table 5/6]`);**本项目 M3/M4 必须自研移植**

2. **Adreno 8 Gen 4 上 4DGS FPS baseline = 0**(`[调研不足,需进一步实验]`)
   - **影响**:无法对照 30~60 FPS 目标的"差距"有多大
   - **应对**:用 NVIDIA `vk_gaussian_splatting` 在桌面 Vulkan 跑 4DGS 资源,作为**桌面 Vulkan baseline** 间接对照

3. **MEGA 的 190× 压缩是否在本项目数据集上成立**(`[未在公开 abstract 拿到具体 PSNR/FPS, 需 PDF 核验]`)
   - **影响**:MEGA 报告"comparable",**没说"identical"**;不同场景下压缩后视觉质量可能有差异
   - **应对**:复现 MEGA 训练管线,在本项目自建数据集上跑 PSNR 对比

4. **Adreno half-precision / 8-bit storage 在不同 SKU 上的 feature 差异**(`[推测,需实测]`)
   - **影响**:bitpack 方案可能受限于部分机型的 Vulkan feature 不支持
   - **应对**:目标机型(Snap 8 Gen 4)锁 feature 列表,备选 fp32 fallback

5. **Vulkan 1.3 on-tile compute 在 Adreno 7xx/8xx 的稳定性**(`[调研不足,需实测]`)
   - **影响**:`VkPhysicalDeviceTileShadingFeatures` 在不同 Adreno 驱动版本的支持程度可能不一致
   - **应对**:锁定驱动版本,跑稳定性测试

### 9.2 中优先级风险

6. **4DGS Table 1 精确 PSNR 数字未在公开 abstract 拿到**(`[未在公开 abstract 拿到,需 PDF 核验]`)
   - **影响**:`01-high-precision-representation.md` 引用 4DGS 精度时只能给"comparable or better"定性,不能给"X.XX dB"
   - **应对**:下游写 `03-end-to-end-roadmap.md` 时打开 PDF Table 1 实抄

7. **Deformable 3DGS PSNR / FPS 数字 abstract 未给**(`[abstract 未给具体数字]`)
   - **影响**:备选 1 的精度数字无对照
   - **应对**:打开 PDF Table

8. **Scaffold-GS / LightGaussian 是否有 4DGS 版本**(`[未在公开 abstract 拿到]`)
   - **影响**:3DGS 加速路线(Scaffold-GS anchor + LightGaussian 剪枝)是否能直接迁移到 4DGS 不确定
   - **应对**:自研 4DGS 版本(把 anchor 思路套到 4DGS canonical + deformation 上)

9. **FSR 2 / Arm ASR 在 4DGS splatting 边缘的视觉质量**(`[推测,需实测]`)
   - **影响**:4DGS deformation 引起的边缘 jitter 是否被 FSR 2 TAA stabilize 不确定
   - **应对**:跑视觉对比实验(720p + FSR 2 vs 1080p native)

10. **InstantSplat / MonST3R 与 4DGS deformation 联合训练的稳定性**(`[未在公开 abstract 拿到,需后续实验]`)
    - **影响**:训练期收不收敛不确定
    - **应对**:在自建数据集上跑小规模实验验证

### 9.3 优先级总览

| 风险 | 优先级 | 应对方式 |
|---|---|---|
| #1 4DGS-1K-lite 未公开 | 高 | 自研 |
| #2 Adreno mobile baseline = 0 | 高 | 真机自测 |
| #3 MEGA 190× 普适性 | 高 | 本数据集复现 |
| #4 Adreno feature 差异 | 中-高 | 锁机型测试 |
| #5 Vulkan on-tile 稳定性 | 中-高 | 锁驱动测试 |
| #6-10 数字 / 兼容性 / 视觉 | 中 | 打开 PDF / 跑实验 |

---

## 附录 A · 引用一览(本文件内新引用的来源)

| 序号 | 来源 | URL / 路径 | 标注方式 |
|---|---|---|---|
| 1 | MEGA(arxiv 2410.13613) | <https://arxiv.org/abs/2410.13613>; <https://github.com/Xinjie-Q/MEGA> | `[abstract 直引]` |
| 2 | FSR 3 / FSR 2 介绍 | <https://www.ithome.com/0/682/270.htm>(IT之家 GDC 2023 报道) | `[abstract 直引]` |
| 3 | FSR 3 性能 4K UE5 60→112 FPS | 同上 | `[abstract 直引]` |
| 4 | FSR 3 MIT 协议 | 同上(AMD 官方声明) | `[abstract 直引]` |
| 5 | Arm ASR 移动端 2025-03-24 全面开放 | <https://www.sohu.com/a/875086997_163726> | `[abstract 直引]` |
| 6 | 3DGS 移动端 demo `torbys/3DGS_App` | <https://github.com/torbys/3DGS_App> | `[基于 web 检索 2026-07-03]` |
| 7 | NVIDIA Vulkan 3DGS viewer `vk_gaussian_splatting` | <https://github.com/nvpro-samples/vk_gaussian_splatting> | `[基于 web 检索 2026-07-03]` |
| 8 | Scaffold-GS 思路(anchor + 神经高斯) | arxiv 2312.00109; <https://github.com/city-super/Scaffold-GS> | `[abstract 直引]`(参考非主对标) |
| 9 | LightGaussian(3DGS 压缩) | arxiv 2311.17245; <https://lightgaussian.github.io/> | `[abstract 直引]`(参考非主对标) |
| 10 | 4DGS-1K-lite 公开论文未找到 | `paper-notes/2024-zhang-mega-4dgs-acceleration.md` §"关键诚实说明" | `[未在公开材料找到]` |

> 本附录仅列入本文件**新引用的**(01-high-precision-representation.md + 4 篇 paper notes 之外)来源。

---

## 附录 B · 与 `01-high-precision-representation.md` 的接口

- **本文件不重写** `01` 中的 per-splat 字段 + 体积估算;引用 `01` §10
- **本文件不重写** `01` 中的训练算力 / 时长;引用 `01` §9
- **本文件不重写** `01` 中的采集 SOP;引用 `01` §8
- **本文件不写** `03-end-to-end-roadmap.md`(留给主对话 session 后一步)
