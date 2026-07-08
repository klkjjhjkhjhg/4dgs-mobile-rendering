# 2025-wang-p4dgs · P-4DGS: Predictive 4D Gaussian Splatting with 90× Compression

> **相关性**:**⭐⭐ 中高相关(4DGS 视频编码范式 + 高压缩率,2025-10)** —— **核心数字**:"achieves up to **40×** and **90× compression on synthetic and real-world scenes**"(abstract 直引);"~**1 MB on average**";USTC(University of Science and Technology of China)。

> **⚠ 重要边界声明**:**P-4DGS 是 4DGS(动态)工作** —— **本项目主线命中**。**核心创新是把 video compression 的 intra-/inter-frame prediction 范式借鉴到 4DGS** —— **canonical space 视作 reference frame,deformation field 视作 motion vector**。**对 M2 训练 pipeline 借鉴价值高**。

## 0.5 元数据

- **venue**: CVPR 2025
- **arxiv-id**: 2510.10030
- **s2-id**: （v2 用 Semantic Scholar API 补全）
- **homepage**: （无）
- **github**: （无）
- **status**: received
- **收录日期**: 2026-07-08（首次）
- **收录来源**: arxiv scan + 1-hop 引用规则
- **1-hop 引用**: （v2 补全，见 §11 1-hop 关系图）
- **评级**: ⭐

## 一句话问题

4DGS 的"deformation field + canonical space"框架有大量 spatial / temporal 冗余,且对 storage 极不友好(典型 4DGS 100+ MB / scene)。**能否借鉴视频编码的 intra-/inter-frame prediction + CABAC 上下文熵编码,把 4DGS 压到 ~1 MB 同时保留 SOTA 质量**?

## 链接(均经 fetch + PDF 实测)
- arxiv: <https://arxiv.org/abs/2510.10030>(v1 提交 2025-10-11)
- PDF: 已下 `.pdfs/2510.10030.pdf`(22.6 MB)

## 年份 / 作者 / 机构(PDF 头部实测)
- **年份**:2025
- **作者**:Henan Wang, Hanxin Zhu, Xinliang Gong, Tianyu He, Xin Li*, Zhibo Chen*
- **机构**:**University of Science and Technology of China (USTC, 中国科学技术大学)**

## 方法核心(abstract 直引 + PDF §1-3 直引)

### 视频编码借鉴动机(intro § 直引)
> "we draw an analogy between dynamic 3D Gaussian representations and established techniques in video compression [4]. Intuitively, deformation field-based 4DGS frameworks parallel the predictive structures used in video coding, where the **canonical space serves as a reference frame** and the **deformation field functions analogously to motion vectors** that describe inter-frame changes."

> "video codecs exploit **spatial redundancy via intra-frame prediction**, **temporal redundancy via inter-frame prediction**, and **contextual redundancy through entropy models such as CABAC**"

### 三大组成(abstract § 直引)
1. **3D anchor point-based spatial-temporal prediction module** —— "fully exploit the spatial-temporal correlations across different 3D Gaussian primitives"
2. **Adaptive quantization + context-based entropy coding** —— "reduce the size of the 3D anchor points"
3. **Spatial prediction**:**nearby Gaussians are predicted by a single anchor point**

### 训练 pipeline(4 stage,§4.1 直引)
1. **Stage 1**:static canonical space(全部帧图,3000 iter)
2. **Stage 2**:quantization-aware training(uniform noise,4-5k iter)
3. **Stage 3**:temporal info(10k iter)
4. **Stage 4**:entropy model + RD(20-40k iter)

## 关键数字(全部 PDF Table 1 / Table 2 直引)

### Table 1 · D-NeRF(synthetic,monocular)

| Method | PSNR↑ | SSIM↑ | LPIPS↓ | Rate (MB)↓ | FPS↑ |
|---|---|---|---|---|---|
| D3DGS | 38.28 | 0.985 | 0.016 | 39.45 | 149 |
| 4DHexPlane | 34.02 | 0.984 | 0.021 | 23.45 | 132 |
| 4DGS | 32.47 | 0.976 | 0.027 | 375.34 | 147 |
| **Ours (P-4DGS)** | **38.10** | **0.985** | **0.017** | **1.039** | **262** |

> **解读**:vs D3DGS = **38.10 vs 38.28 PSNR(-0.18 dB), 1.04 vs 39.45 MB = 38× 压缩**;vs 4DGS vanilla = **+5.63 dB, 361× 压缩**(4DGS baseline 已经过拟合)

### Table 2 · NeRF-DS(real-world,stereo)

| Method | PSNR↑ | SSIM↑ | LPIPS↓ | Rate (MB)↓ | FPS↑ |
|---|---|---|---|---|---|
| D3DGS | 23.75 | 0.847 | 0.179 | 59.38 | 58 |
| 4DHexPlane | 21.08 | 0.729 | 0.281 | 66.37 | 83 |
| 4DGS | 23.00 | 0.814 | 0.259 | 235.95 | 208 |
| **Ours** | **24.18** | **0.855** | **0.184** | **0.704** | **274** |

> **解读**:vs D3DGS = **+0.43 dB PSNR, 84× 压缩**;vs 4DGS vanilla = **+1.18 dB PSNR, 335× 压缩**;FPS 274 = **fastest** baseline(D3DGS 149, 4DGS 208)

### 消融(Table 3 直引,部分)
- **baseline (D3DGS w/ temporal pred only)**:T-Rex 56 MB
- **+ 空间 prediction**:**7 MB**(-87.5%),**+0.3 dB PSNR**
- **+ 紧凑 MLP**(8 → 3 层,256 → 192 dim,float16):-2 MB

## 与本调研主线的关系(基于 00-goal.md)

### 这与 4DGS 压缩派的对照

| 维度 | P-4DGS(本笔记) | 4DGS-1K(5 号) | OMG4(本批 4 号) | 4DGS-CC(本批 5 号) | 4DGCPro(19 号) |
|---|---|---|---|---|---|
| 压缩率 | **40-90×**(abstract) | 41.7×(PP on N3V) | **>60%**(abstract) | 12×(abstract) | 未直引 |
| 4D 适配 | ✅ 4DGS 原生 | ✅ | ✅ | ✅ | ✅ |
| 关键机制 | **视频编码范式** | STV + mask | sample+prune+merge | NVCC + VQCC | hierarchical + RD |
| 量化 | ✅ adaptive quant | PP only | ✅ SVQ | ✅ VQ | ✅ RD |
| Entropy | ✅ **CABAC 类 context** | ❌ | ❌ | ✅ context | ✅ |
| D-NeRF PSNR | **38.10** | 33.34 | (未及) | (未及) | (未及) |
| D-NeRF storage | **1.04 MB** | 7 MB (PP) | (未及) | (未及) | (未及) |
| FPS @ D-NeRF | **262** | 1462 | (未及) | (未及) | (未及) |
| 会议/年份 | USTC, 2025-10 | NUS, 2025-03 | Yonsei, 2025-10 | Beihang, 2025-04 | SJTU, 2025-09 |

> **关键洞察**:**P-4DGS 的"视频编码范式借鉴"是本项目 M2 / M3 阶段最有方法学价值的 4DGS 压缩思路**:
> - **视频编码的 intra-frame prediction ↔ 3D Gaussian spatial 预测**(anchor points)
> - **视频编码的 inter-frame prediction ↔ deformation field motion vector**
> - **CABAC 上下文熵编码 ↔ 4D Gaussian context entropy model**
>
> **借鉴 1**:**3D anchor point-based spatial prediction** —— 邻近 Gaussians 用一个 anchor 预测 —— **本项目 M2 训练 pipeline 直接借鉴**
> **借鉴 2**:**Context-aware entropy model** —— **本项目 M3 bitstream 压缩直接借鉴**
> **借鉴 3**:**Adaptive quantization** —— **本项目 M3 量化阶段借鉴**

### 与本项目"高速相机阵列预制高密度场景"的关系

- **P-4DGS 的"~1 MB / scene"承诺** = **本项目 60K 帧长序列压缩的潜在目标**
- **40-90× 压缩** vs 4DGS vanilla **= 1.04 MB vs 39.45 MB(D-NeRF)** 或 **0.70 MB vs 59.38 MB(NeRF-DS)**
- **借鉴 4**:**Anchor-based spatial prediction** = **本项目 M2 阶段把 60K 帧 / 高速相机数据按空间 anchor 压缩**

### 对项目目标的具体承诺

- **Storage 目标 ≤ 50 MB / scene**:**P-4DGS 已 ~1 MB**(`[实测,Table 1/2]`),**远低于预算**
- **D-NeRF PSNR 38.10** vs 4DGS-1K 33.34 = **+4.76 dB 优势**(因为 P-4DGS 没动 deformation 精度,只压了存储)
- **FPS 262** vs 4DGS-1K 1462 = **4DGS-1K 占优**(因为 P-4DGS 没做 mask / pruning 加速)

## 我未找到 / 提请下游注意

- **项目页 / GitHub**:**abstract 未直引**(`未在公开 abstract 拿到项目页 URL`)
- **会议归属**:**abstract 未直引**(`Preprint. Under review.`,PDF 脚注直引)
- **Mobile GPU 实测**:**abstract / intro 未提 mobile**(`未在公开 abstract 拿到 mobile GPU 型号`)—— **P-4DGS 不做 mobile GPU 端到端**
- **Vulkan 实现**:**abstract 未提 Vulkan**(`未在公开 abstract 拿到 mobile API`)
- **与 4DGS-1K / OMG4 的详细对照**:**abstract 级别不易判定**;**需 PDF §4 实验对比表**核
- **Streaming**:**abstract 未提 streaming / progressive / DASH**(`未在公开 abstract 拿到 streaming 信息`)—— **P-4DGS 是单文件压缩派,不是 streaming 派**

## 我的 commit 节奏

本文是 12 篇 paper notes 之外**新加的第 20+ 篇**,**第 N 篇 4DGS 压缩类笔记**(本批 3 号)。**后续 `02-rendering-acceleration.md` §3 应加 P-4DGS 一行**;**`03-end-to-end-roadmap.md` 应专门为 P-4DGS 加一节"§Y. 4DGS 视频编码借鉴路径(P-4DGS intra-/inter-frame prediction)"**,作为"4DGS 借鉴视频编码范式"的最直接学术先例。

## 引用一览(本笔记引用自)
- arxiv abstract page 直引(`https://arxiv.org/abs/2510.10030`)
- PDF §1 intro 直引(`.pdfs/2510.10030.pdf`)(视频编码 analogy 段)
- PDF §4.1 / Table 1 / Table 2 直引(实验数字)
- PDF §4.3 消融直引(T-Rex 数字)

[abstract 直引] [PDF 直引] [推测] [调研深度:abstract + §1 + Table 1/2 + §4.3 消融,§4.2 主文段未及]
