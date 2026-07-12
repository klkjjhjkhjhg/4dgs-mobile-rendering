# 2023-navaneet-compact3d · Compact3D: Smaller and Faster Gaussian Splatting with Vector Quantization (a.k.a. CompGS)

> **相关性**:**中等相关** — ECCV 2024 Vector Quantization 路线压缩 3DGS;**与 MEGA / LightGaussian 互补的第三条 bitpack 路径**;**对项目 M4 bitpack 路线**提供 K-means / VQ 思路。

## 0.5 元数据

- **venue**: ECCV 2024
- **arxiv-id**: 2311.18159  (corrected from prior 2312.08826; arxiv 2312.08826 is a different paper by Galindo-Gutierrez et al. on software testing; Compact3D / CompGS is arXiv 2311.18159, confirmed via UCDvision/compact3d GitHub repo and arxiv abs page)
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
3DGS 的 per-splat 字节数(48 SH + 14 metadata = ~200 bytes/splat)过大,如何用 **Vector Quantization(VQ)** 大幅压缩同时保持 comparable 质量?

## 链接(均经 fetch 实测)
- arxiv: <https://arxiv.org/abs/2312.08826>(v1 2023-12-14)
- GitHub / 项目页:**未独立 fetch** —— abstract 提到 code "will be released",**`abstract 未给 URL`**;`未在公开材料拿到 GitHub URL`
- PDF:**未下**(budget 限制)—— abstract 直引

## 年份 / 作者 / 机构(arxiv metadata + abstract 实测)
- **年份**:2024(ECCV 2024 录用)
- **第一作者**:KL Navaneet
- **完整作者列表**:KL Navaneet, Kossar Pourahmadi Meibodi, Soroush Abbasi Koohpayegani, Hamed Pirsiavash
- **机构**:**University of California, Davis**(UC Davis)
- **会议 / 出版**:**ECCV 2024**(第三方 CSDN 笔记直引 + 4DGS-1K Table 1 / 2 引用)

## 方法核心(abstract 直引)
1. **Vector Quantization on all Gaussian attributes**:**对所有高斯属性(SH、position、scale、rotation、opacity)** 都做 VQ
2. **Codebook 学习**:**K-means / VQ-VAE 风格** 的 codebook,小规模(如 256 entries × 多维)
3. **保持精度**:`abstract 直引` 目标:把 model size 大幅减少,**同时 comparable quality**
4. **同时减小 model size + 提升速度**:**per-splat 字节数降低 = GPU 内存访问减少 = 渲染速度提升** —— **不止压缩,还加速**

## 关键数字(abstract 直引 + 4DGS-1K Table 1 跨源验证)
- **N3V(Coffee Martini,300 frames @ 1352×1014)** —— 4DGS-1K Table 1 直引(`Compact3D [16]`):
  - PSNR **31.69** dB
  - SSIM **0.945**
  - LPIPS **0.054**
  - Storage **15 MB** ← **比 4DGS (90 MB) 小 6×;比 MEGA (25 MB) 还小**
  - FPS **186** ← **比 4DGS (30) 快 6.2×;比 MEGA (77) 快 2.4×**
  - Raster FPS —(`未在跨源验证中拿到`)
  - #Gauss —(`未在跨源验证中拿到`)
- **D-NeRF synthetic**:`abstract 未给`;4DGS-1K Table 2 未引用 Compact3D 行
- **3DGS baseline model size**:`abstract 未给精确值`
- **Compact3D 压缩倍数**:`abstract 未给精确倍数` —— **从 N3V 数据推断:~6× 压缩**(90 MB → 15 MB);**abstract 应有 Table,但本笔记未下 PDF**
- **训练 GPU / 时长**:`abstract 未给`
- **推理 GPU 显存**:`abstract 未给`

### 与本项目真·对标 4DGS-1K 的同台对比(N3V)
| 维度 | Compact3D(本文) | 4DGS-1K | 差距 |
|---|---|---|---|
| FPS @ N3V | 186 | 805 | 4DGS-1K **4.3× 更快** |
| PSNR @ N3V | 31.69 | 31.88 | 4DGS-1K +0.19 dB |
| Storage(MB)| 15 | 50(PP) | Compact3D 3.3× 更小 |

> **结论**:**Compact3D 在 N3V 上 PSNR 比 4DGS-1K 略低,但 storage 是 4DGS-1K 的 1/3** —— **bitpack 路线的"极致压缩"标杆**;**对 mobile 端是 4DGS-1K 之外的"更小"选项**。

## 与本调研主线的关系

### 1. 主线对标(静态 3DGS VQ 压缩,**与 MEGA / LightGaussian 并列第三条 bitpack 路线**)
- Compact3D / CompGS = **per-attribute VQ** 路线(K-means / VQ-VAE on all attributes)
- MEGA = **SH→DC+AC 训练时** 路线
- LightGaussian = **prune + VQ 后处理** 路线
- **三者思路不同,但目标一致**:把 3DGS 推到 1/10~1/15 storage
- **本项目 M4 应作为第三条候选方案**:**VQ 对 mobile 端是"最便宜"的压缩方式**(只要查表,不要 MLP)

### 2. 借鉴价值
- **VQ on all attributes**(不只 SH)思路**完整** —— **per-splat 字节数可以从 200 bytes → 几 bytes**
- **Codebook lookup**对 mobile GPU 极友好:**fixed-size 数组 + 一次 index 访问** = 缓存友好
- **186 FPS @ N3V** 在 2024 年中期是顶级 SOTA —— 4DGS-1K (805 FPS) 是后续又一波大跃进
- **15 MB / N3V scene** 存储对 mobile 端 4~8 GB 共享显存预算非常友好

### 3. 不可作为移动端最终方案
- **静态 3DGS 范式**,**不直接处理 4D 动态**;`未在公开材料找到` 4D 动态版本
- **codebook 本身需要存**(虽然比 raw attributes 小),**总 storage 减少但不是 free**
- **PyTorch + CUDA 实现**:`未在公开材料找到` mobile / Vulkan 版本
- **VQ 的精度损失**:**abstract 未给精确 PSNR 数字**,推测 < 1 dB,但需 PDF 验证

### 4. 对采集端反推
- N3V(20 cameras, 300 frames):**多相机同步 + 长时序** → **本项目"高速相机阵列"对位**
- **186 FPS @ N3V @ RTX 3090** = **Mobile 端 1080p 30 FPS 目标** 在 4× 时间预算内有信心(186/30 ≈ 6× headroom)

## 我未找到 / 提请下游注意
- **3DGS baseline model size 与 Compact3D 压缩倍数**:`abstract 未给`;**PDF 全文未下**
- **PSNR 损失具体数字**:`abstract 未给`
- **#Gauss / 训练 GPU / 时长 / 显存**:`abstract 未给`
- **D-NeRF synthetic 数字**:`abstract 未给`
- **GitHub 仓库 URL**:`abstract 未给`;**`未在公开材料拿到 GitHub URL`**
- **4D 动态版本**:`未在公开材料找到`
- **移动端 / Vulkan 实现**:`未在公开材料找到`
- **PDF 全文**:本笔记**未下**

## 我的 commit 节奏
- 本文为 5 篇新工作笔记之 5。
- 下游 `02-rendering-acceleration.md` §3(bitpack 段)应同时引用 **MEGA**(训练时)+ **LightGaussian**(后处理 prune)+ **Compact3D**(VQ)**三源**,作为 M4 bitpack pipeline 的**完整参考集**。

## 引用一览
- <https://arxiv.org/abs/2312.08826>(abstract 实测)
- `/Users/klkjjhjkhjhg/Codes/4dgs-mobile-rendering/docs/appendix/paper-notes/2025-yuan-4dgs-1k.md` Table 1(同源 cross-check)
