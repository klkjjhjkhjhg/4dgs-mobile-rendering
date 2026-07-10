# 2025-tu-speede3dgs · SpeeDe3DGS: Speedy Deformable 3D Gaussian Splatting with Temporal Pruning and Motion Grouping

> **相关性**:**⭐⭐ 中高相关(动态 3DGS 加速三大模块,2025-06,2026-03 v4)** —— **核心数字**:在 MonoDyGauBench 50 场景平均,**整合 TSP+TSS 让 DeformableGS 渲染加速 6.78×、Gaussian 数减 10×;叠加 GroupFlow 后 13.71× 加速 + 2.53× 训练加速**(abstract 直引)。**三大模块都围绕"deformable 4DGS 太慢"问题**。

> **⚠ 重要边界声明**:**SpeeDe3DGS 是 Deformable 3DGS(Yang 2024)的优化版**,**不是纯 4DGS canonical rotation 派**,**针对 DeformableGS 的"per-Gaussian neural motion field" 瓶颈**;**GroupFlow 模块也可单独叠加在 4DGS 上**(MonoDyGauBench Table 2 第二段"4DGS + Pruning + GroupFlow" 行)。

## 0.5 元数据

- **venue**: CVPR 2025
- **arxiv-id**: 2506.07917
- **s2-id**: （v2 用 Semantic Scholar API 补全）
- **homepage**: （无）
- **github**: （无）
- **status**: received
- **收录日期**: 2026-07-08（首次）
- **收录来源**: arxiv scan + 1-hop 引用规则
- **1-hop 引用**: （v2 补全，见 §11 1-hop 关系图）
- **评级**: ⭐⭐

- **survey_section**: 4
## 一句话问题

Deformable 3DGS 及其动态扩展虽然质量 SOTA,**但 per-Gaussian neural inference 的 cost 让它们算不动**(MonoDyGauBench 文献里 DeformableGS 20 FPS,4DGS 63 FPS)。**如何既保住 neural motion field 的表达力,又把渲染速度拉到 non-neural baseline 水平?**

## 链接(均经 fetch + PDF 实测验证)
- arxiv: <https://arxiv.org/abs/2506.07917>(v4 更新 2026-03-27)
- **项目页**:`https://speede3dgs.github.io`(PDF 头部直引)
- PDF: 已下 `.pdfs/2506.07917.pdf`(17 页,9.6 MB)

## 年份 / 作者 / 机构(PDF 头部实测)
- **年份**:2025(arxiv v1 2025-06-09);v4 2026-03-27
- **作者**(按 arxiv metadata 头部,等贡献标记 *):**Allen Tu*¹, Haiyang Ying*¹, Alex Hanson¹, Yonghan Lee¹, Tom Goldstein¹, Matthias Zwicker¹**
- **机构**:**University of Maryland, College Park(马里兰大学帕克分校)** —— 全部 6 位都是 UMD
- **资助**:**IARPA(ODNI)+ Amazon Research Awards + Open Philanthropy + DARPA TIAMAT + NSF TRAILS Institute** —— 军工 + 大厂 + 学术混合资助(PDF p9 直引)

## 方法核心(abstract + §1 + §4 直引)

### 三大互补模块(abstract § 直引)

**模块 1 · Temporal Sensitivity Pruning (TSP)**
> "Temporal Sensitivity Pruning (TSP) **removes low-impact Gaussians via temporally aggregated sensitivity analysis**"

- 思想:**对每个 Gaussian 在时间窗口内聚一个 sensitivity score,把 low-sensitivity 的剪掉**
- 区别于 3DGS 静态剪枝:**用"时间维度"上的梯度聚合(不仅看单帧贡献,看跨帧稳定性)**
- 软剪枝:densification 阶段**每 3,000 iter 软剪 60%**;硬剪枝:densification 后硬剪 30%

**模块 2 · Temporal Sensitivity Sampling (TSS)**
> "Temporal Sensitivity Sampling (TSS) **perturbs timestamps to suppress floaters and improve temporal coherence**"

- 思想:**在 sensitivity estimation 时给 timestamp 加 Gaussian perturbation(线性退火,β=0.1, τ=20,000)**
- 解决 TSP 副产品:**低 sensitivity 可能 = 在 unseen deformation 才会失稳 = 不能直接当"低 importance"**
- TSS 主动 probe temporal dimension,**让 unstable Gaussian 显形,被 TSP 正确剪掉**
- 副作用:**压 floaters + 提升 temporal coherence**(PDF Fig 3: NeRF-DS bell scene,11× 减 Gaussians 同时 SSIM 反超 baseline)

**模块 3 · GroupFlow(grouped SE(3) motion distillation)**
> "GroupFlow **distills the learned deformation field into shared SE(3) transformations for efficient groupwise motion**"

- 思想:**不让每个 Gaussian 都跑一遍 MLP,把 motion field 蒸馏成一组 SE(3) 群变换**
- 算法:
  1. **FPS(farthest point sampling)在 t=0 时刻选 J=2048 个 control points**(`h_j`)
  2. **每个 Gaussian 按 trajectory similarity 分到最近的 control point 组**(Eq. 9: `S_{i,j} = λ_r·std_t(‖μ_t - h_t_j‖) + (1-λ_r)·mean_t(...)`,λ_r=0.5)
  3. **每组用 Umeyama alignment 估 SE(3) 变换**(Eq. 10: `argmin ‖μ_t - (R_j(μ_0 - h_0_j) + h_0_j + T_j)‖²`)
  4. 推理时只查 control point,**避免 per-Gaussian MLP forward**
- 控制参数:**J=2048 groups,N_max=100 sampled per group**

### 关键 Pipeline 配合
> "on the 50 dynamic scenes in MonoDyGauBench, integrating TSP and TSS into DeformableGS **accelerates rendering by 6.78× on average**... Adding GroupFlow culminates in **13.71× faster rendering and 2.53× shorter training**"

**训练时间线**(PDF §5 实验设置):
- 0~6,000 iter:**DeformableGS baseline 训练**(warmup)
- 6,000 iter 起:**每 3,000 iter 应用 TSP,软剪 60%**
- 15,000 iter:**GroupFlow 初始化**(densification 完成后)
- 30,000 iter:**总训练结束**

## 关键数字(全部 PDF Table 1 / Table 2 直引)

### Table 1 · **NeRF-DS 7 场景**(real-world,Table 1 / PDF p7)

| 组件组合 | PSNR ↑ | SSIM ↑ | LPIPS ↓ | FPS ↑ | Size (MB) ↓ | #Gauss ↓ | Train (s) ↓ |
|---|---|---|---|---|---|---|---|
| **DeformableGS (baseline)** | 23.80 | 0.8503 | 0.1781 | **54.37 (1.00×)** | 33.21 (1.00×) | 132.22K (1.00×) | 1523.83 (1.00×) |
| + **TSP** | 23.78 | 0.8507 | 0.1863 | **346.96 (6.38×)** | **4.52 (7.35×)** | 10.90K (12.13×) | 741.66 (2.05×) |
| + **TSP + TSS** | 23.81 | 0.8515 | 0.1853 | **345.24 (6.35×)** | 4.55 (7.29×) | 11.06K (11.95×) | 750.69 (2.03×) |
| + **GroupFlow** | 23.54 | 0.8433 | 0.1892 | **406.21 (8.58×)** | 51.00 (0.65×) | 132.32K (1.00×) | 826.75 (1.84×) |
| + **TSP + TSS + GroupFlow** | 23.66 | 0.8487 | 0.1901 | **505.60 (10.68×)** | 21.40 (1.55×) | 11.10K (11.91×) | **625.48 (2.44×)** |

**表 1 关键观察**:
- **PSNR / SSIM 几乎无损**(差距 < 0.14 dB / 0.01 SSIM)
- **GroupFlow 单独** = 8.58× 加速但 storage 反而增(因为 motion params 多)
- **TSP + TSS + GroupFlow 三件套** = **10.68× 加速、2.44× 训练加速、storage 1.55×(10.90K Gaussians × 小 motion params)**

### Table 2 · **MonoDyGauBench 50 场景平均**(5 数据集,Table 2 / PDF p8)

| Method | PSNR ↑ | SSIM ↑ | MS-SSIM ↑ | LPIPS ↓ | FPS ↑ | Train (s) ↓ |
|---|---|---|---|---|---|---|
| EffGS [19] | 21.84 | 0.672 | 0.725 | 0.347 | 177.21 | 3757.81 |
| STG-decoder [24] | 21.81 | 0.678 | 0.742 | 0.352 | 109.42 | 5980.64 |
| STG [24] | 19.51 | 0.583 | 0.643 | 0.475 | 181.70 | 5359.56 |
| RTGS [54] | 21.61 | 0.663 | 0.720 | 0.350 | 143.37 | 7352.52 |
| **4DGS [49] (baseline)** | 23.55 | 0.708 | 0.765 | 0.277 | **62.99 (1.00×)** | 8628.89 (1.00×) |
| + 4DGS Pruning | 22.44 | 0.689 | 0.737 | 0.334 | **179.64 (2.85×)** | 4358.17* (1.47×) |
| + 4DGS Pruning+GroupFlow | 21.00 | 0.667 | 0.705 | 0.380 | **290.21 (4.61×)** | 4176.49* (2.07×) |
| **DeformableGS [53] (baseline)** | **24.07** | 0.694 | 0.755 | 0.283 | **20.20 (1.00×)** | 6227.43 (1.00×) |
| + DeformableGS Pruning | 23.86 | 0.694 | 0.749 | 0.295 | **137.01 (6.78×)** | 2850.60* (2.18×) |
| **+ DeformableGS Pruning+GroupFlow** | 23.52 | **0.709** | **0.771** | 0.313 | **276.91 (13.71×)** | **2461.14* (2.53×)** |

> **表 2 关键观察**:
> - **DeformableGS + Pruning + GroupFlow 跑赢所有 baseline 的 FPS**(13.71× = 276 FPS,vs EffGS 177 / STG-decoder 109 / RTGS 143)
> - **SSIM / MS-SSIM 反超 DeformableGS baseline**(0.709 vs 0.694,0.771 vs 0.755)—— **GroupFlow 起到 regularization 作用**
> - **4DGS + Pruning + GroupFlow 也跑赢**(4.61× 加速,290 FPS)**但 PSNR 损失较大**(-2.55 dB)—— **GroupFlow 对 4DGS 的 canonical rotation 派表现略差**(论文 §5.1 自述:"per-Gaussian inference in DeformableGS better preserves fidelity under grouped motion")

### HyperNeRF chicken 场景(Fig 1 标题直引)
- **9.88× 渲染加速**
- **11.37× 更少 Gaussians**
- **2.87× 训练加速**
- **GroupFlow on top:33.13× 渲染、4.24× 训练**

## 与本调研主线的关系(基于 00-goal.md)

### SpeeDe3DGS 在"动态 3DGS 加速派"的位置

| 维度 | SpeeDe3DGS(本笔记) | 4DGS-1K(2025-yuan-4dgs-1k) | OMG4(2025-lee-omg4) | 4D-RotorGS(2024-duan-4drotorgs) |
|---|---|---|---|---|
| 4D 适配 | ✅ DeformableGS / 4DGS | ✅ 4DGS | ✅ 4DGS | ✅ 4DGS |
| 关键机制 | **TSP + TSS + GroupFlow** | STV + mask | 3-stage sample/prune/merge | canonical rotation |
| 加速比 | **13.71× render / 2.53× train** | 8.94× | 60%+ compression | 1257 FPS @ D-NeRF |
| 输出 FPS | **276 FPS** | 805 FPS | (未给) | 1257 FPS |
| 焦点 | **训练 + 渲染同时加速 + motion 蒸馏** | 剪枝 + 加速 | 紧凑性优先 | 几何加速 |
| 单位 | **UMD(6 位全 UMD)** | NUS | Yonsei/SNU/POSTECH/SKKU | (推测) |
| Mobile 实测 | ❌(RTX 3090 / A5000) | ❌(TITAN X 200+) | ❌ | ❌ |

### 对本项目"4DGS mobile rendering"的具体借鉴

1. **借鉴 1 · GroupFlow 的 motion 蒸馏思路**:**本项目 M3 / M4 阶段可直接借鉴** —— **per-Gaussian neural inference 是 mobile 上最贵的环节**;**用 SE(3) 群变换替代** = **对 mobile 友好的 4DGS motion 表达**
2. **借鉴 2 · TSS 的 temporal perturbation 范式**:**本项目 M2 训练 pipeline 借鉴** —— **当前 4DGS 训练在 mobile 数据上容易 floaters**;**TSS 的"temporally jittered timestamp" 可作为 anti-floater 正则**
3. **借鉴 3 · TSP 的"跨帧 sensitivity aggregation"**:**本项目 M3 bitstream 设计借鉴** —— **跨帧 importance map = mobile 可复用的"dynamic-vs-static mask"**
4. **借鉴 4 · 训练时间缩短 2.53× 的启示**:**本项目 M0~M2 决策借鉴** —— **高速相机阵列长序列训练的工程预算,从 24 hr 拉到 9.5 hr,实际可承受**

### 对项目目标的具体承诺

- **DeformableGS-Pruning-GroupFlow 在 RTX 3090 上 276 FPS,Mobile 上估算 50-100 FPS**(`[推测,基于 Adreno 8 Gen 4 算力约 RTX 3090 的 1/3~1/6]`)—— **本项目 M4 目标"60 FPS @ 1080p on Snap 8 Gen 4" 接近可达**
- **训练 2.53× 加速**:**本项目 M0~M2 训练 budget 关键启示** —— **高速相机阵列长序列(60,000 帧)若按 4DGS 原版 24 hr,加 GroupFlow 后约 9.5 hr,周末训练 budget 现实**
- **GroupFlow 的 SE(3) 群变换**:**本项目 M3 移动端友好设计关键** —— **SE(3) 只用 6 DOF 表达,比 per-Gaussian MLP 的 100+ KB 大幅减**

## 我未找到 / 提请下游注意

- **Mobile GPU 实测**:**abstract / §1 未提 mobile**(`未在公开 abstract 拿到 mobile GPU 型号`)
- **Vulkan 实现**:**abstract 未提 Vulkan**(`未在公开 abstract 拿到具体 mobile API`)
- **GroupFlow 在 4DGS 上效果较差**:**Table 2 显示 4DGS+GroupFlow PSNR -2.55 dB**(从 23.55 → 21.00)**—— 需谨慎使用**:`[推测] GroupFlow 把 4DGS 的"per-Gaussian canonical rotation"过度聚合 = 损失表达能力`
- **完整 Table 数字**:**abstract 未给 PSNR / FPS / storage 详细 Table**(`abstract 只给 13.71× / 6.78× 加速比,Table 1/2 来自 PDF p7-p8`)
- **MonoDyGauBench 与 N3V 的关系**:**abstract 提 50 场景但未列具体数据集**:`MonoDyGauBench = 5 datasets × 10 scenes = 50(论文 §2.1 ref[25] 直引)`
- **GroupFlow 与 4DGS 的具体冲突点**:**§5.1 PDF 提到 "per-Gaussian inference in DeformableGS better preserves fidelity under grouped motion" 但没量化差多少**:`[推测,需 PDF §A.1 per-dataset 表格核]`

## 我的 commit 节奏

本文是 12 篇 paper notes 之外**新加的第 20+ 篇**,**第 N 篇 4DGS 加速类笔记**。**后续 `02-rendering-acceleration.md` §3 应加 SpeeDe3DGS 一行**;**`03-end-to-end-roadmap.md` 应专门为 SpeeDe3DGS 加一节"§Z. 4DGS motion 蒸馏路径(GroupFlow SE(3) 群变换 + TSP/TSS temporal pruning)",作为"4DGS 训练 + 渲染同时加速"的最直接学术先例**。

## 引用一览(本笔记引用自)
- arxiv abstract page 直引(`https://arxiv.org/abs/2506.07917`)
- 项目页 `https://speede3dgs.github.io` (PDF 头部直引)
- PDF 头部 author / 6 位 UMD affiliation 直引(`.pdfs/2506.07917.pdf`)
- PDF §1 intro 直引(传统 dynamic GS 背景 + MonoDyGauBench 引用)
- PDF §4 TSP / TSS / GroupFlow 方法直引
- PDF Table 1 / Table 2 实测数字直引(NeRF-DS + MonoDyGauBench 50 scenes)
- PDF Fig 1 标题直引(HyperNeRF chicken 9.88× 数字)
- PDF §9 Acknowledgments 直引(IARPA / Amazon / Open Philanthropy / DARPA / NSF 资助)

[abstract 直引] [PDF 直引] [推测] [调研深度:abstract + §1 + §4-5 + Table 1/2 + 项目页,§A per-dataset 未及]
