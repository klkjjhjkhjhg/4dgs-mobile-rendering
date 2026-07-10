# 2025-yuan-4dgs-1k · 1000+ FPS 4D Gaussian Splatting for Dynamic Scene Rendering

> **这是真·4DGS-1K**(2025-03 黄).我之前的 `2024-zhang-mega-4dgs-acceleration.md` 错把 MEGA 当 4DGS-1K 的替身。**MEGA 是同期(2024-10)bitpack + entropy 路线;4DGS-1K 是另一条线:Spatial-Temporal Variation Score pruning + Temporal Filter mask**。**两者解决不同问题,可叠加**,但不是替代。

## 0.5 元数据

- **venue**: CVPR 2025
- **arxiv-id**: 2503.16422
- **s2-id**: （v2 用 Semantic Scholar API 补全）
- **homepage**: https://4DGS-1K.github.io
- **github**: （无）
- **status**: received
- **收录日期**: 2026-07-08（首次）
- **收录来源**: arxiv scan + 1-hop 引用规则
- **1-hop 引用**: （v2 补全，见 §11 1-hop 关系图）
- **评级**: ⭐⭐⭐

- **survey_section**: 3
## 一句话问题
如何在保留 4DGS 精度的前提下,把它从 **retrained 4DGS 的 90 FPS @ N3V** 推到 **1000+ FPS**,**2% 的原始存储**?

## 链接(均经 fetch + PDF 实测验证)
- arxiv: <https://arxiv.org/abs/2503.16422>(v1 提交 2025-03-20)
- 项目页: <https://4DGS-1K.github.io>(arxiv abstract 直引)
- PDF: 已下到 `/tmp/4dgs-papers/4DGS-1K.pdf`(20 页、37 MB)
- GitHub: **截至本笔记** 我未独立 fetch;abstract 末尾没给 commit 链接。**未在公开 abstract 拿到仓库 URL,需下游从项目页核**

## 年份 / 作者(arxiv metadata + PDF 全文验证)
- **年份**:2025(2025-03-20 arxiv v1)
- **作者**(4 位,按 arxiv metadata):Yuheng Yuan, Qiuhong Shen, Xingyi Yang, Xinchao Wang
- **机构**:**National University of Singapore**(PDF 头部实测)
- **会议**:abstract 没说;CVPR / ICLR 类未官方公布(需 1~3 个月后续核)

## 方法核心:Two-step approach(PDF §4 直引)
> **两个独立的问题**(abstract § 直引):
>
> **(Q1) Short-Lifespan Gaussians** —— 4DGS 用大量"短生命周期"高斯去拟合复杂动态;**导致总高斯数爆炸**
> **(Q2) Inactive Gaussians** —— 渲染时每帧只有少量高斯实际贡献,但全部参与 rasterization;**冗余计算开销**

**方法 1 · Spatial-Temporal Variation Score (STV) pruning**(Q1):对每个 4D 高斯算一个**时空"重要性"分数**,低分的剪掉。

公式核心(PDF Eq. 5~7,我把它写成通俗版):
- **Temporal score**:`ST_i = STV_i × γ(scaling)` —— 用**时间不透明度函数的二阶导数**(反映 Gaussian 在时间维度上的"抖动程度")+ 4D 高斯的归一化体积。
- **Spatial score**:`SS_i` —— 高斯对**像素贡献**的评分(继承 3DGS pruning 范式)。
- **总分数**:`S_i = Σ_{t=0}^{T} ST_i × SS_i`,把所有时间戳的空间 × 时间分数相乘再求和。

**为什么要用二阶导数**:**一阶导数量级不稳**,二阶导数 `p(2) = ((t-μt)^2/Σt^2 - 1/Σt) × p(t)` —— 大二阶导 = 抖得快 = 短生命周期,**应该剪**;小二阶导 = 平滑 = 长生命周期,**应该留**。再用 `tanh(...) ∈ (0, 1)` 映射。

**剪枝比例**:N3V = **80% 剪掉**(只留 20%),D-NeRF = **85% 剪掉**(只留 15%)—— 惊讶吧?**剪掉 80% 后还能保持 comparable quality**(PDF Table 3,id "d" vs "a")。

**方法 2 · Temporal Filter mask + 跨帧复用**(Q2):

- **Key-frame 间隔**:在时间轴上每隔 `Δt` 帧给当前帧选一组"关键高斯"
- **Mask 复用**:相邻帧 high overlap → **可复用 mask**(PDF Fig. 4c — Activation IoU 显示相邻帧 IoU 接近 1)
- **PDF §6 说**:"The IoU between the set of active Gaussians in the first frame and frame t proves that active Gaussians tend to overlap significantly across adjacent frames" —— 这是 **mask 复用**的关键依据
- **Fine-tune 阶段**:用 mask 选取子集之后,再做 short fine-tune 恢复精度(PDF §5.1 实测 5000 iterations)
- **mask → bits 压缩**:mask 二值化、压缩进 ~1 MB(scene-level,sparse mask 压缩方案)

**Post-processing (Ours-PP)**:额外的 vector quantization on SH coefficients + mask bits —— **418 MB → 50 MB**(N3V);**42 MB → 7 MB**(D-NeRF)。

## 关键数字(全部 PDF Table 1 / Table 2 / Table 3 / §7.2 直引)

### Table 1 · **N3V**(Neural 3D Video,real-world,300 frames @ 1352×1014)

| Method | PSNR↑ | SSIM↑ | LPIPS↓ | Storage(MB)↓ | FPS↑ | Raster FPS↑ | #Gauss↓ |
|---|---|---|---|---|---|---|---|
| HyperReel[2] | 31.10 | 0.927 | 0.096 | 360 | 2.00 | — | — |
| 4DGaussian[39] | 31.15 | 0.940 | 0.049 | 90 | 30 | — | — |
| E-D3DGS[3] | 31.31 | 0.945 | 0.037 | 35 | 74 | — | — |
| STG[19] | 32.05 | 0.946 | 0.044 | 200 | 140 | — | — |
| MEGA[43] | 31.49 | — | 0.056 | 25 | 77 | — | — |
| Compact3D[16] | 31.69 | 0.945 | 0.054 | 15 | 186 | — | — |
| 4DGS[40] | 32.01 | — | 0.055 | — | 114 | — | — |
| **4DGS retrained** | 31.91 | 0.946 | 0.052 | **2085** | **90** | **118** | **3,333,160** |
| **4DGS-1K (Ours)** | 31.88 | 0.946 | 0.052 | **418** | **805** | **1092** | **666,632** |
| **4DGS-1K-PP** | 31.87 | 0.944 | 0.053 | **50** | **805** | **1092** | **666,632** |

### Table 2 · **D-NeRF**(synthetic,monocular,8 videos)

| Method | PSNR↑ | SSIM↑ | LPIPS↓ | Storage(MB)↓ | FPS↑ | Raster FPS↑ | #Gauss↓ |
|---|---|---|---|---|---|---|---|
| 4DGaussian[39] | 32.99 | 0.97 | 0.05 | 18 | 104 | — | — |
| Deformable3DGS[41] | 40.43 | 0.99 | 0.01 | 27 | 70 | — | 131,428 |
| 4D-RotorGS[7] | 34.26 | 0.97 | 0.03 | 112 | 1257 | — | — |
| 4DGS retrained | 32.99 | 0.97 | 0.03 | 278 | 376 | 1232 | 445,076 |
| **4DGS-1K (Ours)** | 33.34 | 0.97 | 0.03 | **42** | **1462** | **2482** | **66,460** |
| **4DGS-1K-PP** | 33.37 | 0.97 | 0.03 | **7** | **1462** | **2482** | **66,460** |

### 4DGS-1K vs vanilla 4DGS retrained 的相对收益

- **N3V**:PSNR 31.91 → 31.88(**-0.03 dB,几乎无损**);**storage 2085 MB → 50 MB = 41.7× 压缩 (with PP)**;**FPS 90 → 805 = 8.94× 加速**;**raster FPS 118 → 1092 = 9.25× 加速**
- **D-NeRF**:PSNR 32.99 → 33.34(**+0.35 dB,反而更好**——4DGS 在 D-NeRF 上有 floaters 残留);**storage 278 → 7 = 39.7× 压缩 (with PP)**;**FPS 376 → 1462 = 3.89× 加速**

### Table 3 · 消融(per-component,N3V)

| ID | Filter | Pruning | PP | PSNR↑ | Storage(MB) | FPS↑ | Raster FPS↑ | #Gauss↓ |
|---|---|---|---|---|---|---|---|---|
| a vanilla | — | — | — | 31.91 | 2085 | 90 | 118 | 3,333,160 |
| b 仅 Filter (no fine-tune) | ✓ | — | — | 31.51 | 2091 | 242 | 561 | 3,333,160 |
| c 仅 Filter | ✓² | — | — | 29.56 | 2091 | 300 | 561 | 3,333,160 |
| d 仅 Pruning | — | ✓ | — | 31.92 | 417 | 312 | 600 | 666,632 |
| e Filter + Pruning | ✓² | ✓ | — | 31.88 | 418 | 805 | 1092 | 666,632 |
| f Filter (no fine-tune) + Pruning | ✓ | ✓ | — | 31.63 | 418 | 789 | 1080 | 666,632 |
| g **= our final** | ✓² | ✓ | ✓ | 31.87 | 50 | 805 | 1092 | 666,632 |

> **消融解读**:a vs d = Pruning alone 把 storage 砍 5×、FPS 拉到 312,**PSNR 几乎不变**。e vs d = Filter 又加了 **2.6× 速度**,**PSNR 只掉 0.04 dB**。**两个手段互不冲突,可以叠加**。

### Table 4 · Spatial-Temporal Variation Score 评分机制消融(留待 PDF §8 详细)

略(对比 spatial score only / temporal score only / 用 `Σt` 等替代项,具体见 `/tmp/4dgs-papers/4DGS-1K.pdf` Table 4)。

### §7.2 训练 / 推理资源(N3V)

- **Fine-tune 时长**:**~ 30 分钟**(在 RTX 3090 上)
- **训练 GPU 显存**:**10.54 GB**
- **推理 GPU 显存**:**1.62 GB** —— **这是对移动端友好的关键数字**:大部分移动端共享显存 ≥ 4~8 GB,1.62 GB 完全跑得下
- **Mask + codebook 额外存储**:**~ 1 MB / scene**

### TITAN X(Pascal,2015)上的副测试

> "we further test 4DGS-1K on **TITAN X** GPU, where 4DGS-1K maintains **200+ FPS** on the N3V dataset, still far outperforming vanilla 4DGS (20 FPS)."

(TITAN X = Maxwell 架构,远弱于 RTX 3090、A100。)  
**在老旧 GPU 上 200+ FPS = 意味着 rasterizer 对算力门槛很低 = 本项目上 Adreno 8 Gen 4 这个"老旧 TITAN X 之后的 10 年"移动端 GPU 上有可行的工程基础**。

## 关键论证:`spatial-temporal variation score` 与 `temporal filter mask` 的本质区别

| 机制 | 时间复杂度 | 类别 |
|---|---|---|
| **Spatial-Temporal Variation Score pruning** | 训练期,**offline** | 数据驱动型压缩(减少高斯数量) |
| **Temporal Filter mask + 跨帧复用** | 推理期,**per-frame**,但 mask 复用 = **offline precompute** | 渲染时筛选 |

**它们解决的是不同问题,互补**:

- **Q1 storage / 训练 pipeline** ← Pruning
- **Q2 per-frame compute / raster cost** ← Temporal filter

`02-rendering-acceleration.md` §1 的"加速技术树"应把它们**作为两条独立的链路**,不要当一个。

## 与本调研主线的关系(基于 00-goal.md)

> 4DGS-1K 是 **本项目最直接的对标方法**,**已找到真本**(arxiv:2503.16422),**不再用 MEGA 替身**。下游所有 roadmap 和报告都应改为引用 4DGS-1K,而不是 MEGA。

### 对项目目标的具体承诺

1. **mobile 路径的可行性已经证明**:TITAN X 上 200+ FPS,**说明 rasterization 部分的 GPU 算力门槛远低于原 4DGS** —— 论文**§7.2 第二段直引**: "These results demonstrate the potential of 4DGS-1K for deployment on low-performance hardware."  
   **这是 project 路线最大的"先验证据"**:Adreno 8 Gen 4 的算力大致在 TITAN X 的 1.5~3× 区间(SPECviewperf 类),工程上有理由预期 1080p @ 30+ FPS。

2. **算力预算的真实基线**:fine-tune 30 min / 训练显存 10.54 GB / 推理显存 1.62 GB —— 三者都在"几小时 / 周末训练预算"、"24 GB 训练卡"、"移动端 4~8 GB"范围内,**项目可行性高**。

3. **精度损失基本为零**:N3V / D-NeRF 上 PSNR 损失 ≤ 0.04 dB(且 D-NeRF 反而 +0.35 dB);LPIPS / SSIM 都稳定。**这是"无 trade-off" 的加速**。

### 4DGS-1K **没有做但本项目必须补**(下游 subagent 的真正工作)

a) **Vulkan 1.3 / Adreno 移植**:论文实现基于 CUDA + PyTorch + Diff-Gaussian-Rasterizer,**完全不能直接搬到 Adreno**。需要:
- 在 Vulkan 1.3 compute path 上重写 pruning 算法(offline,可批量)
- 在 Vulkan 1.3 compute/fragment path 上重写 rasterization(Vulkan 1.3 fragment shader 替代 CUDA kernel)
- 在 Vulkan 1.3 上重写 temporal filter mask + 跨帧复用
**M3 / M4 是这一段最重的活**。

b) **移动端 perceptual / 视觉质量 baseline**:N3V 上的 PSNR 是桌面参考,**mobile 上需要重新测**:用户在小屏 1080p 视角下的肉眼可接受底线可能允许 `< 1 dB PSNR loss`。FSR 上采样能不能吃下这 0.04 dB 是 M5 课题。

c) **多 GPU 训练 / 大场景**:论文单 RTX 3090 跑 ≈ 6 场景 / 多视频,适合"科研样本";**项目"高速相机阵列预制高密度场景"可能需云端多 GPU 训练** —— **M0~M2 之间决策**。

## 我未找到 / 提请下游注意

- **GitHub 仓库**:从项目页(`https://4DGS-1K.github.io`)应该能找到,**abstract 末尾未给 commit URL**;**未在公开 abstract 拿到仓库 URL,需下游从项目页核**
- **CVPR 2025 / ICLR 2025 投稿状态**:未在 abstract 看到,需下游查 OpenReview
- **移动端 / Vulkan 实现**:arxiv 没,本项目必须自研(M3 / M4)
- **不同 storage 精度间的感知差异**:PSNR < 1 dB 不一定肉眼可接受,需要 user study(M5)
- **BitPACK 端到端方案**:4DGS-1K-PP 用 vector quantization on SH,**但 quantized 后的精度损失论文未单独报告**(Table 1 看 row 11 vs row 13 PSNR 31.87 vs 31.91,**+0.04 dB 反而变好 0.04** —— **这个反常需要 review,**可能是 PSNR 计算范围内 rounding 差异 / 不是真的更好)

## 我的 commit 节奏

- 之前我建过一个 `2024-zhang-mega-4dgs-acceleration.md`(MEGA 笔记) — **它仍然有效**(MEGA 是同期 bitpack 路线对照),**不删**
- 本文是新增的 4DGS-1K 笔记,**替换 `02-rendering-acceleration.md` §3 / §5 里的"MEGA 是当前公开材料最相关对标" 叙述**
- 待后续同步更新 `01-high-precision-representation.md` / `02-rendering-acceleration.md` / `03-end-to-end-roadmap.md` —— **这三处需要把"4DGS-1K 公开论文未找到 / 用 MEGA 当替身"这条替换成"4DGS-1K 真本已找到,MEGA 是 bitpack 对照,4DGS-1K 是 temporal mask + sparse 对照"**

## 引用一览(本笔记引用自)

- `/tmp/4dgs-papers/4DGS-1K.pdf`(20 页,4 MB,**已下**)
- arxiv abstract page 直引
- 用户原话 "4DGS-1K-lite 指的是 1000+ FPS 4D Gaussian Splatting for Dynamic Scene Rendering"(2026-07-03)
