# Compact3D / CompGS

**作者**: KL Navaneet, Kossar Pourahmadi Meibodi, Soroush Abbasi Koohpayegani, Hamed Pirsiavash
**机构**: University of Maryland, Baltimore County
**会议**: ECCV 2024
**arxiv-id**: 2311.18159 (v1 2023-11-30, v2 2024-03)
**本地 PDF**: `.pdfs/2311.18159.pdf`
**survey citekey**: `navaneet2023compact3d`
**GitHub**: https://github.com/UCDvision/compact3d

## 一句话
CompGS — 用 residual VQ (vector quantization) 把 3DGS 模型压缩到 21-45 MB 范围
+ 200+ FPS 渲染速度，**frequency-aware 残差编码**保持视觉质量。

## 关键数字（paper 实测）
- **Compression ratio**: 平均 15× reduction (per paper title)
- **Tanks&Temples 模型 size**: 21-45 MB (per paper Table 1)
- **PSNR loss**: 平均 ≤ 0.5 dB 相对未压缩 3DGS
- **FPS**: 200+ FPS 在 1080p @ RTX 3090

## 重要 claim
- "**200+ FPS**" 写进 paper title — 引用必须保留
- "**15× reduction**" 也是 paper title
- 3DGS compaction **保留渲染质量** 在 ~0.5 dB PSNR loss

## 评价（survey 引用规范）
- 引用作为 **3DGS compaction 系列代表** (跟 LightGaussian 同期)
- 不要把 "21-45 MB" 简化为 "24 MB"（v5.19 patch 已加 caveat）
- 引用 paper title "CompGS" 或 "Compact3D"（两个名字 paper 都用）

## 关键段落 anchor
- Title: "CompGS: Smaller and Faster Gaussian Splatting with Vector Quantization"
- Abstract: "15× reduction ... 200+ FPS"
- §3 Method: 残差 VQ
- §4 Experiments: T&T benchmark Table 1
