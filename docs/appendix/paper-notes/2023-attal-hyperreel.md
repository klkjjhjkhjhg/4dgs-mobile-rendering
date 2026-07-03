# 2023-attal-hyperreel · HyperReel: High-Fidelity 6-DoF Video with Ray-Conditioned Sampling

> **升级说明**:本笔记从 abstract 级升级为 PDF 全文级。**关键数字全部 PDF Table 1/2/3 直引**。HyperReel 是 **NeRF-style 6-DoF 视频** 路线(非 3DGS 范式),**本项目不直接采用其渲染路径**;但**"ray-conditioned sample prediction network"**的"稀疏采样"思想是后续 3DGS 加速路线的精神先驱。**NeRF-style 6-DoF 在 §1 引言中也是明确列出的"非 3DGS 路线"对照**。

## 一句话问题
如何在**多视角视频**(4×4 / 18~20 / 46 相机阵列)上同时实现**高质量 6-DoF 视频**、**实时渲染**、**紧凑存储**,**不用 custom CUDA code**?

## 链接(均经 fetch + PDF 实测)
- arxiv: <https://arxiv.org/abs/2301.02238>(v2 2023-05-29;v1 2023-01-06)
- 项目页: <https://hyperreel.github.io>
- GitHub: <https://github.com/facebookresearch/hyperreel>(PDF §B 直引)
- PDF: 已下到 `/tmp/4dgs-papers/attal-hyperreel.pdf`(16 页、30 MB;含补充材料)

## 年份 / 作者 / 机构(arxiv metadata + PDF 头部实测)
- **年份**:2023(CVPR 2023)
- **第一作者**:Benjamin Attal(CMU + Meta Reality Labs)
- **完整作者列表**:Benjamin Attal, Jia-Bin Huang, Christian Richardt, Michael Zollhöfer, Johannes Kopf, Matthew O'Toole, Changil Kim
- **机构**:
  - **Carnegie Mellon University**(1)
  - **University of Maryland**(2)
  - **Reality Labs Research / Meta**(3)
  - **Meta**(4)
- **会议**:CVPR 2023(PDF §1 引用 + 公开 metadata)
- **重要卖点**:**"no custom CUDA code"** —— 全部用 PyTorch 实现,2023 年在 RTX 3090 上跑 18 FPS @ megapixel 分辨率

## 方法核心(PDF §3 直引)

1. **Ray-Conditioned Sample Prediction Network**(PDF §3.1 / Eq. 4~5,Figure 2):
   - 输入是 Plücker coordinates 表示的射线 `(o, ω)`
   - 网络 `E_φ` 输出 N 个 **geometric primitives** `G_1, ..., G_N`(z-planes 或 spherical shells)的参数 + per-sample **displacement offsets** `d_1, ..., d_N`
   - 采样点 `x_k = inter(G_k; o, ω) + d_k` —— **ray 与 primitive 交点 + offset**
   - **核心优势**:同时(1) 加速 volume rendering 和(2) 处理 highly view-dependent appearance(反射、折射)

2. **TensoRF-style Keyframe-Based Dynamic Volume**(PDF §3.2 / Eq. 10~11):
   - 把 TensoRF 扩展为 **"keyframes"** —— 每隔 4 帧设一个 keyframe,中间帧用 **trainable scene flow** 推算
   - 公式:`A(x_k, τ_i) = B_1(f_1(x,y) ⊙ g_1(z, τ_i)) + ...`(3 个 CP 分解,把 time 维度融入 g_1, g_2, g_3)
   - **共 6 个 2D textures**:(x,y)/(x,z)/(y,z)/(x,t)/(y,t)/(z,t) 之类的乘积组合
   - **Memory efficient**:利用 dynamic scene 的 spatio-temporal redundancy

3. **Sample Network 同时建模 view-dependent appearance**(PDF §3.1):
   - Point offsets `(e_1, ..., e_N)` + Tanh 激活 —— 允许 sample points 沿 ray 方向 warped
   - 类似 "canonical frame deformation"(Nerfies / Neural Volumes)
   - **关键 insight**:反射、折射违反 epipolar geometry → sample points 需要 viewpoint-dependent 偏移

4. **训练目标**:L2 + L1 sparsity + TV regularization(同 TensoRF)
5. **Inference**:直接 volume rendering,**无 custom CUDA** —— 纯 PyTorch Eager Mode

## 关键数字(全部 PDF Table 1/2/3 直引)

### Table 1 · Static Scene Comparisons(DoNeRF synthetic)[PDF Table 1 直引]

| Dataset / 分辨率 | Method | PSNR↑ | FPS↑ | Memory↓ |
|---|---|---|---|---|
| DoNeRF 400×400 | R2L(单 sample light field) | 35.5 | — | 23.7 MB |
| DoNeRF 400×400 | **Ours(per-frame)** | **36.7** | **4.0** | **58.8 MB** |
| DoNeRF 800×800(Uniform) | NeRF | 30.9 | 0.3 | 3.8 MB |
| DoNeRF 800×800(Uniform) | Instant NGP | 33.1 | 3.8 | 64.0 MB |
| DoNeRF 800×800(Adaptive) | DoNeRF | 30.8 | 2.1 | 4.1 MB |
| DoNeRF 800×800(Adaptive) | AdaNeRF | 30.9 | 4.7 | 4.1 MB |
| DoNeRF 800×800(Adaptive) | TermiNeRF | 29.8 | 2.1 | 4.1 MB |
| DoNeRF 800×800(Adaptive) | **Ours(per-frame)** | **35.1** | **4.0** | **58.8 MB** |

> **Memory 注意**:HyperReel 报的是 **"MB per frame"**,因为它为每个 frame 维护一个 keyframe volume。**不可直接和 4DGS 的"全场景"storage 数字对比**。

### Table 2 · Dynamic Scene Comparisons[PDF Table 2 直引]

(FPS 都是 **megapixel 分辨率**;Memory 是 **MB per frame**)

#### Technicolor Dataset(2048×1088,5 scenes,50 frames)

| Method | PSNR↑ | SSIM↑ | LPIPS↓ | FPS↑ | Memory↓ |
|---|---|---|---|---|---|
| Neural 3D Video | 31.8 | 0.958 | 0.140 | 0.02 | 0.6 MB |
| **Ours (HyperReel)** | **32.7** | **0.906** | **0.109** | **4.00** | **1.2 MB** |

#### Neural 3D Video Dataset(20 cameras, 2704×2028 → half-res 1352×1014, 6 scenes, 300 frames)

| Method | PSNR↑ | SSIM↑ | LPIPS↓ | FPS↑ | Memory↓ |
|---|---|---|---|---|---|
| Neural 3D Video¹ | 29.6 | 0.961 | 0.083 | 0.02 | 0.1 MB |
| NeRFPlayer | 30.7 | 0.931 | 0.111 | 0.06 | 17.1 MB |
| StreamRF¹ | 28.3 | — | — | 10.90 | 17.7 MB |
| **Ours (HyperReel)** | **31.1** | **0.927** | **0.096** | **2.00** | **1.2 MB** |

(¹ Neural 3D Video / StreamRF 报的是 flame salmon 单场景;StreamRF 没给 SSIM / LPIPS。)

#### Google Immersive Light Field Dataset(46-fisheye camera rig, 7 scenes)

| Method | PSNR↑ | SSIM↑ | LPIPS↓ | FPS↑ | Memory↓ |
|---|---|---|---|---|---|
| NeRFPlayer | 25.8 | 0.848 | 0.196 | 0.12 | 17.1 MB |
| **Ours (HyperReel)** | **28.8** | **0.874** | **0.193** | **4.00** | **1.2 MB** |

> **核心读数**:
> - 在 Technicolor 上,HyperReel **PSNR 比 Neural 3D Video 高 0.9 dB**;**FPS 4.00 vs 0.02 = 200× 加速**;memory **2×** 增加
> - 在 Neural 3D Video Dataset 上,**PSNR 比 NeRFPlayer 高 0.4 dB**;**FPS 2.00 vs 0.06 = 33× 加速**
> - 在 Google LF 上,**PSNR 比 NeRFPlayer 高 3.0 dB**;**FPS 4.00 vs 0.12 = 33× 加速**

### Table 3 · Network Ablations(Technicolor)[PDF Table 3 直引]

| Method | PSNR↑ | SSIM↑ | LPIPS↓ | FPS↑ |
|---|---|---|---|---|
| keyframe: every frame | 32.34 | 0.895 | 0.117 | 4.0 |
| **keyframe: every 4 frames(Ours default)** | **32.73** | **0.906** | **0.109** | **4.0** |
| keyframe: every 16 frames | 32.07 | 0.893 | 0.112 | 4.0 |
| keyframe: every 50 frames | 32.35 | 0.896 | 0.110 | 4.0 |
| w/o sample network | 29.08 | 0.815 | 0.209 | 1.3 |
| **Tiny(4 层 128 单元 MLP, 8 primitives)** | 30.09 | 0.835 | 0.157 | **17.5** |
| **Small(4 层 256 单元 MLP, 16 primitives)** | 31.76 | 0.903 | 0.125 | **9.1** |

> **关键消融**:
> - **没 sample network**:PSNR 直接掉 3.65 dB(32.73→29.08),FPS 掉 3×(4.0→1.3)
> - **Tiny model**:**18 FPS @ megapixel**(论文 abstract 直引的 18 FPS 来源);PSNR 损失 -2.6 dB
> - **Small model**:**9 FPS @ megapixel**;PSNR 损失 -0.97 dB
> - **Keyframe interval = 4** 最佳

### Table 4 · Point Offset Ablation(static scenes)[PDF Table 4 直引]

| Scene | Point offset | PSNR↑ | SSIM↑ | LPIPS↓ |
|---|---|---|---|---|
| DoNeRF "Forest"(diffuse) | Without | 34.86 | 0.969 | 0.0146 |
| DoNeRF "Forest"(diffuse) | **With** | **36.34** | **0.975** | **0.0122** |
| Shiny "Lab"(refractive) | Without | 31.28 | 0.943 | 0.0416 |
| Shiny "Lab"(refractive) | **With** | **32.49** | **0.959** | **0.0294** |

## 训练 / 推理资源(综合 PDF §4 + §C 直引)
- **训练 GPU**:**单卡 NVIDIA RTX 3090 / 24 GB**(PDF §4 直引:"run experiments on a single NVIDIA RTX 3090 GPU with 24 GB RAM")
- **训练时长**:
  - Per scene:**~ 1.5 GPU hours**(50-frame chunk,Technicolor,PDF §4 直引)
  - 对比 Neural 3D Video:**~ 1 week × 8 V100 = 1000+ GPU hours**(HyperReel 在 §4.2 直引:"Neural 3D Video on each sequence for approximately one week on a machine with 8 NVIDIA V100 GPUs")
  - **速度差:~ 670× 训练加速**
- **训练 ray batch size**:**16,384 rays**(PDF §D.1 直引)
- **推理 GPU 显存**:**未在 PDF 显式报出**
- **训练 GPU 显存**:**未在 PDF 显式报出**
- **Sample Network 架构**:
  - Full: 6 层 MLP, 256 hidden units, Leaky ReLU
  - Small: 4 层 MLP, 256 hidden units, 16 primitives
  - Tiny: 4 层 MLP, 128 hidden units, 8 primitives
- **Keyframe 间隔**:**4 帧**(PDF §4 直引;补充验证 Table 3)
- **数据集**:
  - Technicolor(4×4 camera rig, 2048×1088, 50 frames)
  - Neural 3D Video Dataset(20 cameras, 2704×2028 → half-res, 6 scenes, 300 frames)
  - Google Immersive(46-fisheye camera rig, 7 scenes)
- **典型 keyframe 数量**:
  - Technicolor 50 frames: **~ 12 keyframes**
  - Neu3D 300 frames: **~ 75 keyframes**
- **典型 splat 数量级**:**不适用**(NeRF 范式,无显式 splat)

## 与本调研主线的关系

### 1. 主线对标(NeRF-style 6-DoF,**非 3DGS 路线**,作为对照)
- HyperReel 是 **NeRF 范式** 6-DoF 视频,**不是 3DGS 范式**;**本项目最终不会直接采用其渲染路径**
- 但其 **"ray-conditioned sample prediction network"** 的"稀疏采样"思想是后续 3DGS 加速路线的精神先驱
- **abstract 级笔记中的 §"与本调研主线的关系"已明确它是 6-DoF NeRF 路线**,本次升级不变

### 2. 借鉴价值
- **"无 custom CUDA" 卖点 = 移动端友好的关键证据**:HyperReel 在 RTX 3090 上 18 FPS @ megapixel,**纯 PyTorch Eager Mode** → 证明 NeRF 范式 6-DoF 在 **JIT-compiled Vulkan / OpenGL ES compute shader** 上有理论可行性
- **"Keyframe + scene flow"思想**与 4DGS-1K 的"Temporal Filter mask"有结构相似性(都是"per-frame sub-volume 复用"思路)—— **可借鉴到 3DGS 4D 场景中**
- **TensoRF-based volume factorization**(XY/XT/YT/XZ/YZ/TZ 6 个 plane)的思想与 HexPlane **几乎一致** —— HexPlane 论文的 6-plane 分解可视为 HyperReel TensoRF 的时序扩展
- **18 FPS @ megapixel Tiny model** = "NeRF-style 6-DoF 在 RTX 3090 上的移动端可期上限"基准

### 3. 不可作为移动端最终方案
- **NeRF 范式 vs 3DGS 范式**:3DGS 在 2023-2024 后成为动态场景主流(PDF Table 2 of 4DGS-1K 中 HyperReel PSNR 31.10 / FPS 2.00 / Storage 360 MB,被 4DGS(31.15/30/90 MB)、STG(32.05/140/200 MB)、E-D3DGS(31.31/74/35 MB) 全面超越)
- **Volumetric rendering 路径** vs **3DGS splatting 路径**:**volumetric 需要 ray marching + 沿射线的多个 sample 查询**,3DGS 一次 splat 即可 → **3DGS 移动端天然更友好**
- **"18 FPS @ megapixel RTX 3090"** 是 HyperReel 上限;**3DGS-1K 在 RTX 3090 上是 805 FPS @ N3V** = **44.7× 加速**

### 4. 对采集端反推
- Technicolor(4×4 同步)+ Neu3D(20 cam)+ Google LF(46 fisheye):**多视角 + 高分辨率 + 短时序**。**与本项目"高速相机阵列预制高密度场景"完全对位**
- **HyperReel training ~ 1.5 GPU hours / 50-frame chunk** = **50 frames 训练预算 ~ 1.5 hr @ RTX 3090**;Neu3D 300 frames = **~ 9 GPU hours @ RTX 3090** = **1.5 工作日内单卡完成**(本项目可行性关键证据)

## 我未找到 / 提请下游注意
- **推理 GPU 显存**:PDF 未显式报出
- **训练 GPU 显存**:PDF 未显式报出
- **#Gauss / splat 数量级**:**不适用**(NeRF 范式,无显式 splat);**PDF vs abstract 不一致** 风险点:abstract 说 "up to 18 FPS at megapixel resolution",Table 3 显示 Tiny 17.5 FPS、Full 4.0 FPS → **abstract 指的是 Tiny model**,这是 **PDF vs abstract 不一致** 的一例
- **移动端 / Vulkan 实现**:未在 PDF 找到
- **GitHub 仓库是否包含 mobile backend**:Meta Reality Labs 的 facebookresearch/hyperreel 未在公开 README 中声明 mobile backend
- **DSSIM vs SSIM 关系**:Table 1/2 报的是 SSIM,**HyperReel 在 Appendix C 显式讨论了 SSIM 的 two failure modes**(data range parameter, downsampled reference) → **SSIM 数字应保留怀疑**

## 我的 commit 节奏
- 此前 abstract 级笔记 6354 B → **本次升级 → 见最终 commit hash**。
- 下游 `02-rendering-acceleration.md` §0(加速技术树)应把 HyperReel 归到 **"NeRF 范式 6-DoF"** 分支,作为 **"非 3DGS 路线"** 对照;不与 4DGS-1K / MEGA 同台比较精度 / FPS 数字。
