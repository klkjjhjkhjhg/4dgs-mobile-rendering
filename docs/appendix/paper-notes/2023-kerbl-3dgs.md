# 3D Gaussian Splatting (3DGS)

**作者**: Bernhard Kerbl, Georgios Kopanas, Thomas Leimkühler, George Drettakis
**机构**: INRIA, Université Côte d'Azur
**会议**: SIGGRAPH 2023 (Best Paper)
**arxiv-id**: 2308.04079 (v1 2023-08-08)
**本地 PDF**: `.pdfs/2308.04079.pdf`
**survey citekey**: `kerbl20233dgs`
**GitHub**: https://github.com/graphdeco-inria/gaussian-splatting (CUDA)

## 一句话
3D Gaussian Splatting (3DGS) — 用各向异性 3D 高斯作为显式辐射场表示 + 可微光栅化，
**首个**在 1080p 达到 real-time (≥30 FPS) 渲染质量的 radiance field 方法。

## 关键数字（paper 实测）
- **1080p @ RTX A6000**: Mip-NeRF 360 场景 ≥30 FPS (paper Table 1, p.7)
- **Training time**: Mip-NeRF 360 场景 35-45 分钟 (paper Table 1)
- **PSNR Mip-NeRF 360** (Ours, paper Table 2): ~27.21 dB (garden / bicycle / stump / room / counter / kitchen / bonsai 平均)
- **vs NeRF**: 训练时间 ~35-45 分钟 vs NeRF ~48 小时, **训练快 ~70-100×**
- **vs Mip-NeRF 360**: 训练快 ~100-1000×, 渲染快 ~100×

## 重要 claim
- "novel view synthesis" **at 1080p resolution** — 引用必须保持 1080p
- "real-time" 定义 ≥30 FPS (paper abstract 1.1 节, 严格说 ≥30 FPS)
- **Mip-NeRF 360 数据集 7 个场景** (garden/bicycle/stump/room/counter/kitchen/bonsai)

## 评价（survey 引用规范）
- 引用作为 **3DGS 原论文 + 4DGS 类工作的 baseline**
- 不要把 "3DGS achieves real-time novel-view synthesis" 简化为 "30-90 FPS"（v5.15 patch 已改）
- 不要把 "100-1000× faster than NeRF" 写成 "50-100×"（v5.16 patch 已改 65-80× + 1000× FPS）

## 关键段落 anchor
- Abstract: "≥30 fps" @ 1080p
- §1 Introduction: 训练快 vs NeRF
- §5.1 Table 1: Mip-NeRF 360 7-scene numbers
- §5.2 Table 2: PSNR/SSIM/LPIPS 跟 NeRF/Mip-NeRF/Plenoxels 对比
