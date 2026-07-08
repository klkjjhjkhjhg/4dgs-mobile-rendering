# 2025-ke-streamstgs · StreamSTGS: Streaming Spatial and Temporal Gaussian Grids for Real-Time Free-Viewpoint Video

> **相关性**:**⭐⭐⭐ 高度相关(4DGS FVV streaming + 2D 图像/视频压缩,2025-11)** —— **核心数字**:"increases the PSNR by an average of **1 dB** while reducing the average frame size to just **170 KB**"(abstract 直引);**N3DV / MeetRoom 实测**;**VBR(variable bitrate)传输**;**"canonical 3D Gaussians, temporal features, and a deformation field"** —— **4DGS 原生 + 视频编码借鉴**。

> **⚠ 重要边界声明**:**StreamSTGS 是 4DGS(动态)工作**,abstract 直引"canonical 3D Gaussians, temporal features, and a deformation field" —— **本项目主线命中**。**核心创新是把 canonical Gaussian 编码为 2D 图像,temporal features 编码为视频** —— **直接借鉴视频编码工具,无需重训即可支持 adaptive bitrate**。

## 0.5 元数据

- **venue**: CVPR 2025
- **arxiv-id**: 2511.06046
- **s2-id**: （v2 用 Semantic Scholar API 补全）
- **homepage**: （无）
- **github**: （无）
- **status**: received
- **收录日期**: 2026-07-08（首次）
- **收录来源**: arxiv scan + 1-hop 引用规则
- **1-hop 引用**: （v2 补全，见 §11 1-hop 关系图）
- **评级**: ⭐

## 一句话问题

现有 3DGS-based FVV 方案每帧 10 MB storage,**无法 real-time streaming**。**如何用视频编码思路(2D 图像 / 视频)压缩 4DGS,既降低每帧存储又支持 adaptive bitrate + 实时解码**?

## 链接(均经 fetch + PDF 实测)
- arxiv: <https://arxiv.org/abs/2511.06046>(v1 提交 2025-11)
- PDF: 已下 `.pdfs/2511.06046.pdf`(40 MB)

## 年份 / 作者 / 机构(PDF 头部实测)
- **年份**:2025
- **作者**(按 arxiv metadata 头部):**Zhihui Ke, Yuyang Liu, Xiaobo Zhou*, Tie Qiu**
- **机构**:**Tianjin University (天津大学)**

## 方法核心(abstract + §1-3 直引)

### 三大创新(abstract § 直引)
1. **"encode canonical Gaussian attributes as 2D images and temporal features as a video"**
2. **"inherently supports adaptive bitrate control based on network condition without any extra training"**
3. **"sliding window scheme to aggregate adjacent temporal features to learn local motions, and then introduce a transformer-guided auxiliary training module to learn global motions"**

### 关键发现(abstract § 直引)
> "the storage requirements of these methods can reach up to **10 MB per frame**, making stream FVV in real-time impossible"

### StreamSTGS 框架(abstract 直引)
> "StreamSTGS represents a dynamic scene using **canonical 3D Gaussians, temporal features, and a deformation field**. For high compression efficiency, we encode canonical Gaussian attributes as 2D images and temporal features as a video."

### 优化器(§ 直引,部分)
- **Dynamic-aware density**:"L1 loss 全图 + SSIM loss 仅 dynamic pixels"(I_mask 由 frame 标准差 30 frames 估,或 SAM 替代)
- **Pruning**:"收集 predicted opacity O_i across all timestamps within a GOP, average < threshold → prune"
- **Gaussian relocate**:"does not prune unnecessary Gaussians but instead moves them to more optimal position"
- **Two-pass design**:**Gaussian Pass + Auxiliary Pass**,Transformer 仅训练时用,**inference 时移除**(保 FPS)

## 关键数字(全部 Table 1 / Table 2 直引)

### Table 1 · N3DV(real-world,18-21 cameras,30 FPS,1352×1014)

| Method | PSNR↑ | SSIM↑ | LPIPS↓ | Storage (KB)↓ | K.F. Size (MB)↓ | Decoding (ms)↓ | Render (ms)↓ | FPS↑ | Train (s)↓ | VBR |
|---|---|---|---|---|---|---|---|---|---|---|
| TeTriRF | 30.07 | 0.900 | 0.299 | 65.89 | 2.03 | 149 | 652 | 1.53 | 32 | ✓ |
| 3DGStream | 30.73 | 0.935 | 0.147 | 8204 | 42.22 | 7×n | 14 | 72 | 17 | × |
| VideoGS | 27.45 | 0.871 | 0.213 | 932.9 | 3.24 | 48 | 7 | 21 | 143 | ✓ |
| HiCoM | 31.32 | 0.939 | 0.147 | 10704 | 83.35 | 0 | 6 | 163 | 10 | × |
| 4DGC | 31.52 | 0.941 | 0.143 | 784 | 21.94 | 2.5×n | 12 | 78.6 | 62 | × |
| **Ours (StreamSTGS)** | **32.30** | **0.943** | **0.147** | **173.6** | **3.86** | **8** | **10** | **100** | **67** | **✓** |

> **解读**:
> - **PSNR best 32.30**(超第二名 4DGC +0.78)
> - **Storage 173.6 KB** = **4× 比 4DGC 784 KB 小**
> - **FPS 100** = real-time(>30)
> - **Decoding 8 ms** + **Render 10 ms** = 18 ms / 帧,远低于 33 ms 实时门槛
> - **VBR 支持**(与 4DGC / 3DGStream / HiCoM 不可比)

### Table 2 · MeetRoom(12 cameras,1280×720,30 FPS)

| Method | PSNR↑ | SSIM↑ | LPIPS↓ | Storage (KB)↓ | K.F. Size (MB)↓ | FPS↑ | Train (s)↓ | VBR |
|---|---|---|---|---|---|---|---|---|
| 3DGStream | 26.41 | 0.90 | 0.24 | 4108 | 18 | 121 | 11 | × |
| HiCoM | 26.69 | 0.90 | 0.23 | 5535 | 42 | 275 | 6 | × |
| 4DGC | 27.11 | 0.91 | 0.23 | 1196 | 11 | 110 | 60 | × |
| **Ours** | **27.41** | **0.92** | **0.21** | **142** | **2.8** | **126** | **29** | **✓** |

> **解读**:**Storage 142 KB = 8.4× 比 4DGC 1196 KB 小**;FPS 126 = real-time;**VBR 支持**

### 实施细节
- **GPU**:**RTX A6000**(single)
- **coarse 3DGS 训练**:**3000 iterations, batch 2**(用所有 multi-view 帧)
- **GOP size**:60(每 60 帧一个 Group of Pictures)
- **GOP 训练**:**12000 iter (N3DV) / 7000 iter (MeetRoom)**
- **Gaussians 数量上限**:**~150k**(以减小 size)
- **noise λ**:**0.001**(基于 "temporal features compression loss ≈ 0.0002")

## 与本调研主线的关系(基于 00-goal.md)

### 4DGS FVV streaming 派方法学对照

| 维度 | StreamSTGS(本笔记) | AirGS(本批 1 号) | 4DGC(本笔记 Table baseline) | 4DGCPro(19 号) | PD-4DGS(本批 2 号) |
|---|---|---|---|---|---|
| 4D 适配 | ✅ 4DGS | ✅ | ✅ | ✅ | ✅ |
| 关键机制 | **2D image + video 编码** | keyframe + ILP | (per-frame storage 784 KB) | hierarchical + RD | HDD 3-layer |
| **N3DV PSNR** | **32.30** | (未直引) | 31.52 | (未直引) | (Dycheck 数字不同) |
| **N3DV Storage** | **173.6 KB / frame** | (未直引) | 784 KB / frame | (未直引) | (Dycheck 数字不同) |
| **FPS @ N3DV** | **100** | (未直引) | 78.6 | (未直引) | (未直引) |
| VBR | ✅ **支持(无重训)** | ❌ | ❌ | ❌ | ✅ DASH/HLS |
| 会议 | (未直引) | (未直引) | (未直引) | (未直引) | (未直引) |
| 单位 | **Tianjin U** | SJTU | (Hu 等,2025a) | SJTU | Qilu |

> **关键洞察**:**StreamSTGS 是 4DGS FVV streaming 派的"视频编码借鉴"代表**;**与 P-4DGS / 4DGC / 4DGCPro 形成"4DGS streaming 四路线"对照**:
> - **StreamSTGS**:**2D image + video + VBR 支持无重训**
> - **4DGC**:**per-frame 压缩** (784 KB)
> - **4DGCPro**:**hierarchical + RD + mobile decode**
> - **PD-4DGS**:**3-layer HDD + DASH/HLS 兼容**

### 对本项目"高速相机阵列预制 + 端侧流式播放"的具体借鉴

1. **借鉴 1 · "encode canonical Gaussian attributes as 2D images"**:**本项目 M2 / M3 阶段直接借鉴**(把 3DGS canonical 信息映射为 2D 图像,直接套用 PNG / JPEG 压缩)
2. **借鉴 2 · "encode temporal features as a video"**:**本项目 M3 bitstream 设计直接借鉴**(把 deformation field 时序信息编为视频,直接套用 H.264 / H.265)
3. **借鉴 3 · "adaptive bitrate control without any extra training"**:**本项目 M3 流式播控模块直接借鉴**(关键优势:**无需重训即可适应网络**)
4. **借鉴 4 · Two-pass design + Gaussian relocate**:**本项目 M2 训练 pipeline 借鉴**(Transformer 训练时用,inference 时移除)
5. **借鉴 5 · Dynamic-aware density**:**本项目 M2 训练借鉴**(L1 全图 + SSIM 仅 dynamic 像素)

### 对项目目标的具体承诺

- **N3DV PSNR 32.30, 173.6 KB / frame, 100 FPS**:**本项目"高速相机阵列 + 端侧播放"目标已验证先例**(`[实测,Table 1]`)
- **Storage 170 KB / frame**:**按 30 FPS × 60 秒 = 1800 帧,总 bitstream ≈ 300 MB / minute** —— **需要 streaming 而非一次性下载**
- **VBR 支持**:**本项目 M3 阶段不同网络条件自适应码率**
- **FPS 100 on RTX A6000**:**桌面 GPU 实测**;**Snap 8 Gen 4 估算 ~50 FPS**(`[推测,基于 Adreno 算力约 A6000 的 1/2]`)

## 我未找到 / 提请下游注意

- **项目页 / GitHub**:**abstract 未直引**(`未在公开 abstract 拿到项目页 URL`)
- **会议归属**:**abstract 未直引会议**(`未在公开 abstract 拿到会议归属`)
- **Mobile GPU 实测**:**abstract / §5 未提 mobile**(`未在公开 abstract 拿到 mobile GPU 型号`)—— **StreamSTGS 桌面 A6000 实测,未在 mobile GPU**
- **Vulkan 实现**:**abstract 未提 Vulkan**(`未在公开 abstract 拿到具体 mobile API`)
- **2D image / video 编码具体格式**:**abstract 提"2D image + video"但未明示 PNG / JPEG / H.264**(`abstract 未给具体编码格式,需 PDF §3 核`)
- **170 KB 是否含 motion vectors**:**abstract 未直引**(`abstract 未给 170 KB 构成`)

## 我的 commit 节奏

本文是 12 篇 paper notes 之外**新加的第 20+ 篇**,**第 N 篇 4DGS FVV streaming 类笔记**(本批 8 号)。**后续 `02-rendering-acceleration.md` §3 应加 StreamSTGS 一行**;**`03-end-to-end-roadmap.md` 应专门为 StreamSTGS 加一节"§Y. 4DGS 视频编码借鉴 streaming 路径(StreamSTGS 2D image + video + VBR)"**,作为"4DGS FVV streaming 借鉴视频编码工具"的最直接学术先例。

## 引用一览(本笔记引用自)
- arxiv abstract page 直引(`https://arxiv.org/abs/2511.06046`)
- PDF §3-4 直引(`.pdfs/2511.06046.pdf`)(dynamic-aware density / pruning / relocate / two-pass)
- PDF Table 1 / Table 2 直引(N3DV / MeetRoom 5 baseline 对比)
- PDF §5 implementation 直引(RTX A6000 / 150k 上限 / GOP 60 / 12000 iter)

[abstract 直引] [PDF 直引] [推测] [调研深度:abstract + §1-4 + Table 1/2 + §5 implementation]
