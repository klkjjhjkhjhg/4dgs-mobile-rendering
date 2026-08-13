# Paper Notes 索引（按主线分组）

> **本地 PDF stash**: `/.pdfs/`（仓库根目录，**不进 git**，见 `.gitignore`）
> **命名约定**: 大部分用纯 arxiv id（`<arxiv-id>.pdf`），4 篇"早期下"的用易读命名（`4DGS-1K.pdf` / `wu-4dgs.pdf` 等）
> **总计**: **185 篇 paper notes ↔ 185 个本地 PDF**（截至 2026-08-10，含本批 arxiv 50 + ICCV 2025 67 = 117 新增，all 模式手动 sync 触发）
> **标记**: ⭐⭐⭐ = 本项目直接对标 / ⭐⭐ = 高相关 / ⭐ = 参考
> **本批扩展（25 H2 ~ 26 H1）**: 14 篇 — `Flux-GS` (ECCV 2026) + 13 篇 2026 H1 arxiv (3DGS 加速 / 压缩 / mobile / streaming 派系)
> **本批触发**: 用户用 GitHub 链接 `https://github.com/xiaobiaodu/Flux-GS` 作为入口，扩到同期 13 篇相关工作
> **本批 2（2026-07-08 ECCV/CVPR 专扫）**: 2 篇 CVPR 2026 Oral — `RetimeGS` (4DGS continuous-time, HKUST+Netflix) + `GaussianFluent` (3DGS 物理模拟, PKU+BIGAI)。**ECCV 2026 接收名单尚未公开（9 月会议，arXiv+web 搜索 4 来源无数据）**；CVPR 2026 Poster 全名单非常稀疏（amusi 3DGS 段仅 3 篇），本项目相关核心（Mobile-GS / Flux-GS / Flow4DGS-SLAM / RAP / FastGS / Topology-Aware）已在前批 commit 覆盖。
> **本批 4（2026-07-13 arxiv 扫描）**: 1 篇 TIER 1 4DGS — `MVFusion-GS` (Tsinghua + UT Dallas + UESTC, 2026-07-02 arxiv)。**Motion-Variance Guided Refinement + MotionFormer Temporal Attention 双模块 plug-in DeGauss**，Neu3D +0.55 dB PSNR 同时 42% 动态 Gaussian 压缩。无 mobile 评测。22 篇新候选已分类 TIER 1/2/3（cron 预算只收 TIER 1）。

---

## A. 4DGS 表示（高精度表示主线，19 篇）

| paper | arxiv id | year | 一句话 | 评 |
|---|---|---|---|---|
| [2024-wu-4dgs.md](2024-wu-4dgs.md) | 2310.08528 | 2023-10 | 4DGS 原论文，canonical + deformation field | ⭐⭐⭐ |
| [2023-yang-deformable-3dgs.md](2023-yang-deformable-3dgs.md) | 2309.13101 | 2023-09 | Deformable 3DGS，canonical anchor + per-frame deformation（NeRF 系起源） | ⭐⭐⭐ |
| [2025-yuan-4dgs-1k.md](2025-yuan-4dgs-1k.md) | 2503.16422 | 2025-03 | **本项目直接对标**，STV 评分 + temporal mask（动静态分离的隐式版本） | ⭐⭐⭐ |
| [2023-attal-hyperreel.md](2023-attal-hyperreel.md) | 2301.02238 | 2023-01 | HyperReel，关键帧 + 光流 warp（NeRF-style 4D） | ⭐⭐ |
| [2024-zhang-mega-4dgs-acceleration.md](2024-zhang-mega-4dgs-acceleration.md) | 2410.13613 | 2024-10 | MEGA，buffer-A/B 残差编码（结构化分离） | ⭐⭐ |
| [2024-duan-4drotorgs.md](2024-duan-4drotorgs.md) | 2402.03307 | 2024-02 | 4D-RotorGS，**canonical rotation** (arxiv-id corrected from prior 2402.03306 which is a math paper by Perrotin)，D-NeRF 1257 FPS（动静态分离的另一变体） | ⭐ |
| [2024-li-spacetime-gaussians.md](2024-li-spacetime-gaussians.md) | 2312.16812 | 2023-12 | Spacetime Gaussians，geometry-aware KNN 时空网格 | ⭐ |
| [2025-shi-sparse4dgs.md](2025-shi-sparse4dgs.md) | 2511.07122 | 2025-11 | Sparse4DGS，稀疏化 + 4DGS 加速 | ⭐ |
| [2025-liu-4dgrt.md](2025-liu-4dgrt.md) | 2509.10759 | 2025-09 | 4DGRT，4DGS Ray Tracing（NTU+Intel） | ⭐ |
| [2026-wang-retimegs.md](2026-wang-retimegs.md) | 2603.13783 | 2026-03 | **RetimeGS** (CVPR 2026 Oral, HKUST+Netflix)，4DGS continuous-time 表示，**消除 temporal aliasing + ghost-free frame interpolation** | ⭐⭐⭐ |
| [2026-huang-gaussianfluent.md](2026-huang-gaussianfluent.md) | 2601.09265 | 2026-01 | **GaussianFluent** (CVPR 2026 Oral, PKU+BIGAI)，3DGS + MPM 物理模拟（elastic / fracture / slicing）+ 混合材质 | ⭐⭐ |
| [2026-song-l2d2-gs.md](2026-song-l2d2-gs.md) | 2606.29374 | 2026-06 | **L2D2-GS** (小米+北大联合)，feedforward 4DGS 动态场景重建 + 自监督 densification policy（**对作者 heliangliang@xiaomi.com 有合作背景**） | ⭐⭐⭐ |
| [2026-hu-mvfusion-gs.md](2026-hu-mvfusion-gs.md) | 2607.01578 | 2026-07 | **MVFusion-GS** (Tsinghua + UT Dallas + UESTC)，plug-in DeGauss with Motion-Variance guided refinement + MotionFormer Temporal Attention 双机制，Neu3D 32.07 dB (+0.55 vs DeGauss) + 42% 动态 Gaussian 压缩 (56,533 → 32,985) | ⭐⭐ |
| [2026-kim-gp-4dgs.md](2026-kim-gp-4dgs.md) | 2604.02915 | 2026-04 | **GP-4DGS** (Seoul National Univ + Wisconsin-Madison)，Variational Gaussian Processes (Matérn×periodic composite kernel) + Chronos inducing points + GP-GS dual optimization，DyCheck Challenging mPSNR 15.02 (+0.46 vs SoM) | ⭐⭐ |
| [2026-zhou-motionscale.md](2026-zhou-motionscale.md) | 2603.29296 | 2026-03 | **MotionScale** (NUS)，cluster-centric motion field (K cluster 共享 SE(3) + B basis 局部精修) + progressive optimization + shadow Gaussians，DyCheck NVS PSNR 17.98 (+1.26 vs SoM)；**未报 FPS/训练时间/Gaussian count** | ⭐⭐ |
| [2026-arxiv-2604-04063-4c4d.md](2026-arxiv-2604-04063-4c4d.md) | 2604.04063 | 2026-04 | **4C4D** (作者未在 PDF 披露)，4 Camera 4DGS + Neural Decaying Function (NDF) MLP per-Gaussian decay，**4 相机稀疏视角 (vs 现有 18-21)**，Neural3DV PSNR 20.60→22.29 (+1.69 dB)，LPIPS -40% | ⭐⭐ |

---


| [2025-y-.md](2025-y-.md) | (待补) | 2025-10 | 4D Gaussian Splatting SLAM | ⭐ |
| [2026-arxiv-2607-04761.md](2026-arxiv-2607-04761.md) | 2607.04761 | 2026-07 | DeGenseGS: Geometrically and Semantically Decoupled Surgical Scene Understanding in 4D Gau | ⭐ |
| [2026-arxiv-2607-12362.md](2026-arxiv-2607-12362.md) | 2607.12362 | 2026-07 | Implicit 4D Gaussian Splatting for Fast Motion with Large Inter-Frame Displacements | ⭐ |
## B. 4DGS 加速 / 动静态分离（25-26 主线之三，18 篇）

| paper | arxiv id | year | 一句话 | 评 |
|---|---|---|---|---|
| [2026-liao-sharptimegs.md](2026-liao-sharptimegs.md) | 2602.02989 | 2026-02 | **SharpTimeGS**，lifespan modulation 时间/动态分层（隐式动静态分离） | ⭐⭐ |
| [2025-lee-omg4.md](2025-lee-omg4.md) | 2510.03857 | 2025-10 | **OMG4**，minimal 4DGS，imperceptible 时间部分剪枝 | ⭐⭐ |
| [2026-yin-cags.md](2026-yin-cags.md) | 2605.09279 | 2026-05 | **CAGS**，色彩自适应的动静态分层 streaming | ⭐ |
| [2025-tu-speede3dgs.md](2025-tu-speede3dgs.md) | 2506.07917 | 2025-06 | **SpeeDe3DGS**，temporal pruning + motion compensation（UMD, 13.71×） | ⭐⭐ |
| [2025-chen-4dgscc.md](2025-chen-4dgscc.md) | 2504.18925 | 2025-04 | **4DGS-CC**，contextual coding framework | ⭐⭐ |
| [2026-li-pd4dgs.md](2026-li-pd4dgs.md) | 2605.11427 | 2026-05 | **PD-4DGS**，progressive decomposition + R-DO（TMC 一致性） | ⭐⭐ |
| [2026-ren-cubifygs.md](2026-ren-cubifygs.md) | 2606.28720 | 2026-06 | **CubifyGS**，object-level asset + rigid rearrangement lifelong dynamic scene（**>40× faster than WildGS-SLAM**） | ⭐ |
| [2026-jiao-mapo.md](2026-jiao-mapo.md) | 2508.19786 | 2025-08 | **MAPo** (Zhejiang U + Sun Yat-Sen U Shenzhen)，dynamic score 递归 temporal partitioning of high-dynamic 3DGS (复制 deformation sub-network) + static baking for low-dynamic + cross-frame consistency loss，N3DV PSNR 31.33 (+0.54 vs E-D3DGS) | ⭐⭐ |
| [2026-xu-layered-4drotor.md](2026-xu-layered-4drotor.md) | (CVPR 2026, 无 arxiv) | 2026-06 | **Layered 4D-Rotor GS** (PKU + Galbot)，**Factorized Covariance Quantization (FCQ)** + Layered Compression + Residual Codebook Quantization (RCQ)，N3DV 180.7 MB → 8.8 MB (**20.5×**)，SelfCap 1194 FPS @ 41.8 MB | ⭐⭐ |

---


| [2025-c-obustplat-ecoupling-ensifi.md](2025-c-obustplat-ecoupling-ensifi.md) | (待补) | 2025-10 | RobustSplat: Decoupling Densification and Dynamics for Transient-Free 3DGS | ⭐ |
| [2025-m-ccidental-ccidental-amera.md](2025-m-ccidental-ccidental-amera.md) | (待补) | 2025-10 | AccidentalGS: 3D Gaussian Splatting from Accidental Camera Motion | ⭐ |
| [2025-s-a-econstructing-imulating.md](2025-s-a-econstructing-imulating.md) | (待补) | 2025-10 | MaGS: Reconstructing and Simulating Dynamic 3D Objects with Mesh-adsorbed Gaussian Splatti | ⭐ |
| [2025-x--xplicit-otion.md](2025-x--xplicit-otion.md) | (待补) | 2025-10 | EMD: Explicit Motion Modeling for High-Quality Street Gaussian Splatting | ⭐ |
| [2025-z-zier-ynamic-rban.md](2025-z-zier-ynamic-rban.md) | (待补) | 2025-10 | BézierGS: Dynamic Urban Scene Reconstruction with Bézier Curve Gaussian Splatting | ⭐ |
| [2026-arxiv-2607-08250.md](2026-arxiv-2607-08250.md) | 2607.08250 | 2026-07 | On the Design of Mixture-of-Experts for Dynamic Gaussian Splatting | ⭐ |
| [2026-arxiv-2607-14990.md](2026-arxiv-2607-14990.md) | 2607.14990 | 2026-07 | JADE-GS: Joint Alternating Deblurring Guided by Events in 3D Gaussian Splatting | ⭐ |
| [2026-arxiv-2607-21099.md](2026-arxiv-2607-21099.md) | 2607.21099 | 2026-07 | Construction and Dynamic Update of Channel Gain Maps via 3D Gaussian Splatting | ⭐ |
| [2026-arxiv-2607-21448.md](2026-arxiv-2607-21448.md) | 2607.21448 | 2026-07 | GrainGS: Gradient-Decoupled Gaussian Splatting for Efficient Dynamic Novel View Synthesis | ⭐ |
## C. 渲染加速（pipeline 级，含 3DGS + 4DGS，34 篇）

| paper | arxiv id | year | 一句话 | 评 |
|---|---|---|---|---|
| [2026-du-flux-gs.md](2026-du-flux-gs.md) | 2606.30017 | 2026-06 | **Flux-GS** (ECCV 2026)，Mobile-GS 团队继任作，**Snap 8 Gen 3 147 FPS @ 2.1 MB**（Indoor） | ⭐⭐⭐ |
| [2026-du-mobile-gs.md](2026-du-mobile-gs.md) | 2603.11531 | 2026-03 | **Mobile-GS**，Snap 8 Gen 3 上 127 FPS（**Vulkan 2.0**） | ⭐⭐⭐ |
| [2025-feng-lumina.md](2025-feng-lumina.md) | 2506.05682 | 2025-06 | **Lumina: Real-Time Mobile Neural Rendering**，SJTU+Rochester，**4.5× speedup + 5.3× energy** | ⭐⭐⭐ |
| [2025-oh-neo.md](2025-oh-neo.md) | 2511.12930 | 2025-11 | **Neo: On-Device 3DGS** with **Reuse-and-Update Sorting Accelerator** | ⭐⭐⭐ |
| [2026-thomas-gausslite.md](2026-thomas-gausslite.md) | 2606.30809 | 2026-06 | **GaussLite** (MIT AeroAstro)，**4 Hz real-time on resource-constrained hardware** + task-conditioned density | ⭐⭐ |
| [2026-li-pocket-slam.md](2026-li-pocket-slam.md) | 2606.24796 | 2026-06 | **Pocket-SLAM**，3DGS-SLAM **60% memory↓ + 2.7× FPS↑**（KITTI seq10 34.2→13.3 GB） | ⭐⭐ |
| [2026-gong-dict-3dgs.md](2026-gong-dict-3dgs.md) | 2605.30396 | 2026-05 | **Smaller-Faster-3DGS** (Linköping)，post-training dictionary learning，**3.95×/3.10×/4.55× comp** + 23-25% FPS↑ | ⭐⭐ |
| [2024-yu-mip-splatting.md](2024-yu-mip-splatting.md) | 2311.16493 | 2023-11 | Mip-Splatting，CVPR 2024 best student（尺度修正） | ⭐⭐ |
| [2024-feng-flashgs.md](2024-feng-flashgs.md) | 2408.07967 | 2024-08 | FlashGS，CVPR 2025 | ⭐⭐ |
| [2024-liu-efficientgs.md](2024-liu-efficientgs.md) | 2404.12777 | 2024-04 | EfficientGS | ⭐ |
| [2024-chen-fcgs.md](2024-chen-fcgs.md) | 2410.08017 | 2024-10 | FCGS，Monash U（频率压缩） | ⭐ |
| [2024-chen-hacpp.md](2024-chen-hacpp.md) | 2501.12255 | 2025-01 | HAC++，ECCV 2024（hierarchical anchor compression） | ⭐ |
| [2026-poirier-ginter-gray.md](2026-poirier-ginter-gray.md) | 2606.30869 | 2026-06 | **GRay** (ACM CGIT 2026, U. Laval + Inria)，3DGS ray tracing **4× vs 3DGRT, 248 FPS**（桌面 RTX 唯一平台） | ⭐⭐ |
| [2026-zhang-cat-gs.md](2026-zhang-cat-gs.md) | 2607.17842 | 2026-07 | **CaT-GS** (SJTU + UIUC)，speculative multi-frame pre-processing + inter-frame caching (frustum + sort) + load-aware tile-level task splitting，**up to 10× over vanilla 3DGS** on RTX 5090，UAV-2 23.2→202.5 FPS；自建 UAV City Dataset 5 个大场景 | ⭐⭐⭐ |
| [2026-wang-filtergs.md](2026-wang-filtergs.md) | 2603.23891 | 2026-03 | **FilterGS** (Beijing Inst Tech)，Traversal-Free Parallel Filtering (R&L + Ancestor Filter, depth-decoupled) + GTC-driven adaptive shrinking，**~300 FPS avg on 6 large-scale scenes** (MatrixCity/UrbanScene)；RTX 4090 only | ⭐⭐ |
| [2026-tran-pointsplat.md](2026-tran-pointsplat.md) | 2604.09903 | 2026-04 | **PointSplat** (GMU, CVPR 2026 3DMV Workshop)，geometry-driven (z-score of opacity × volume) pruning + Dual-Branch Encoder (geom/apperance 分离) + Point Transformer V3 refine，**10% sparse 23.46 PSNR ScanNet++** | ⭐⭐ |
| [2026-zhou-temporalgs.md](2026-zhou-temporalgs.md) | 2607.03390 | 2026-07 | **TemporalGS** (McGill + Waterloo + Toronto)，**首个 training-free plug-and-play** 3DGS 加速，**up to 1.48×**，作者未来工作明示"develop a 4DGS counterpart" | ⭐⭐ |

---


| [2025-s-ptimized-eature-lanes.md](2025-s-ptimized-eature-lanes.md) | (待补) | 2025-10 | Compression of 3D Gaussian Splatting with Optimized Feature Planes and Standard Video Code | ⭐ |
| [2025-s-tochasticplats-tochastic-a.md](2025-s-tochasticplats-tochastic-a.md) | (待补) | 2025-10 | StochasticSplats: Stochastic Rasterization for Sorting-Free 3D Gaussian Splatting | ⭐ |
| [2025-x-ile-wise-mage.md](2025-x-ile-wise-mage.md) | (待补) | 2025-10 | Tile-wise vs. Image-wise: Random-Tile Loss and Training Paradigm for Gaussian Splatting | ⭐ |
| [2026-arxiv-2607-03765.md](2026-arxiv-2607-03765.md) | 2607.03765 | 2026-07 | Sparse-View Surface Reconstruction using Gaussian Splatting through High-Confidence Depth  | ⭐ |
| [2026-arxiv-2607-04127.md](2026-arxiv-2607-04127.md) | 2607.04127 | 2026-07 | Real-Time LiDAR Gaussian Splatting SLAM | ⭐ |
| [2026-arxiv-2607-04144.md](2026-arxiv-2607-04144.md) | 2607.04144 | 2026-07 | Semantic-Guided Progressive Object Removal with Gaussian Splatting | ⭐ |
| [2026-arxiv-2607-05522.md](2026-arxiv-2607-05522.md) | 2607.05522 | 2026-07 | Rendering-Aware Bayesian 3D Gaussian Splatting with Native Uncertainty and Adaptive Comple | ⭐ |
| [2026-arxiv-2607-08808.md](2026-arxiv-2607-08808.md) | 2607.08808 | 2026-07 | StereoSplat+: Feed-Forward Stereo Gaussian Splatting with Diffusion-Assisted Progressive I | ⭐ |
| [2026-arxiv-2607-12656.md](2026-arxiv-2607-12656.md) | 2607.12656 | 2026-07 | SpeedyGS: Content-Aware 3D Gaussian Splatting Compression via Two-Stage Optimization | ⭐ |
| [2026-arxiv-2607-14513.md](2026-arxiv-2607-14513.md) | 2607.14513 | 2026-07 | Compression of 3D Gaussian Splatting Data Using GPU-friendly Graphics Texture Coding | ⭐ |
| [2026-arxiv-2607-16838.md](2026-arxiv-2607-16838.md) | 2607.16838 | 2026-07 | TopoGS: Planar Reconstruction via Topology-aware 3D Gaussian Splatting | ⭐ |
| [2026-arxiv-2607-18067.md](2026-arxiv-2607-18067.md) | 2607.18067 | 2026-07 | QIRF Quantum-Inspired Non-Orthogonal Function-Space Compression for 3D Gaussian Splatting | ⭐ |
| [2026-arxiv-2607-18466.md](2026-arxiv-2607-18466.md) | 2607.18466 | 2026-07 | ECoNGS: Efficient Compressive Neural Gaussian Splats for Volume Visualization | ⭐ |
| [2026-arxiv-2607-22780.md](2026-arxiv-2607-22780.md) | 2607.22780 | 2026-07 | Inter-Reflective Gaussian Splatting for Robust and Efficient Inverse Rendering | ⭐ |
| [2026-arxiv-2607-22890.md](2026-arxiv-2607-22890.md) | 2607.22890 | 2026-07 | Meshless Domain Randomization via Explicit Parameter Perturbation of 3D Gaussian Splatting | ⭐ |
| [2026-arxiv-2607-22956.md](2026-arxiv-2607-22956.md) | 2607.22956 | 2026-07 | 3D Gaussian Splatting for Scientific Particle Data Compression and Rendering | ⭐ |
| [2026-arxiv-2607-24403.md](2026-arxiv-2607-24403.md) | 2607.24403 | 2026-07 | GenSplatCodec: Feed-Forward Gaussian Splatting Compression via One-Step Diffusion | ⭐ |
| [2026-arxiv-2607-26525.md](2026-arxiv-2607-26525.md) | 2607.26525 | 2026-07 | AtlasLC: Fast Codec-Ready Compression of Object-Centric 3D Gaussian Splatting | ⭐ |
| [2026-arxiv-2607-26578.md](2026-arxiv-2607-26578.md) | 2607.26578 | 2026-07 | 3DGBGS: 3D Granular Ball Gaussian Splatting for Compact Novel View Synthesis | ⭐ |
## D. 流式 streaming / 移动端落地（12 篇）

| paper | arxiv id | year | 一句话 | 评 |
|---|---|---|---|---|
| [2026-ghosh-gs-nfs.md](2026-ghosh-gs-nfs.md) | 2606.05650 | 2026-06 | **GS-NFS** (NVIDIA Research)，**4DGS 25 FPS decode on Jetson Orin mobile GPU** | ⭐⭐⭐ |
| [2025-wang-airgs.md](2025-wang-airgs.md) | 2512.20943 | 2025-12 | **AirGS**，4DGS streaming + ILP pruning（**6× 训练加速** + 50% transmission） | ⭐⭐ |
| [2025-zheng-4dgcpro.md](2025-zheng-4dgcpro.md) | 2509.17513 | 2025-09 | **4DGCPro**，4DGS mobile streaming（abstract 级） | ⭐⭐ |
| [2026-li-pd4dgs.md](2026-li-pd4dgs.md) | 2605.11427 | 2026-05 | **PD-4DGS**（同时见派系 B），**iPhone 2 Mbps 移动网络 1.7s 启动**，progressive decomposition + R-DO | ⭐⭐ |
| [2026-liang-clipgstream.md](2026-liang-clipgstream.md) | 2604.13746 | 2026-04 | **ClipGStream** (作者单位 PDF 未明确)，Clip-Stream 4DGS (frozen base + clip-by-clip STF increments) for **任意长度 4DGS 流式重建**，N3DV 98 MB @ 300 frames；扩展 GS-NFS 思路 | ⭐⭐ |
| [2025-ke-streamstgs.md](2025-ke-streamstgs.md) | 2511.06046 | 2025-11 | **StreamSTGS**，streaming spatial-temporal grids（real-time FVV） | ⭐⭐ |
| [2026-shi-evogs.md](2026-shi-evogs.md) | 2606.07179 | 2026-06 | **EvoGS**，continuous-layered Evolution Tree，**2.4× payload↓, 5.5× VRAM↓, redundancy 65%→25%** | ⭐⭐ |
| [2026-veicht-zipsplat.md](2026-veicht-zipsplat.md) | 2606.05102 | 2026-06 | **ZipSplat** (ETH/Microsoft)，feed-forward 3DGS，**6× fewer Gaussians** + token-based scene | ⭐⭐ |
| [2026-yu-codecsplat.md](2026-yu-codecsplat.md) | 2605.25563 | 2026-05 | **CodecSplat** (PKU)，ultra-compact latent coding，**20-108 KiB/scene** | ⭐ |
| [2025-li-gifstream.md](2025-li-gifstream.md) | 2505.07539 | 2025-05 | **GIFStream**，4D Gaussian feature stream | ⭐ |
| [2025-wang-p4dgs.md](2025-wang-p4dgs.md) | 2510.10030 | 2025-10 | **P-4DGS**，**90× compression**（predictive 4DGS） | ⭐ |
| [2025-liu-4dgrt.md](2025-liu-4dgrt.md) | 2509.10759 | 2025-09 | 4DGRT，4DGS Ray Tracing（NTU+Intel） | ⭐ |

---


| [2025-g-mbodiedplat-ersonalized-ea.md](2025-g-mbodiedplat-ersonalized-ea.md) | (待补) | 2025-10 | EmbodiedSplat: Personalized Real-to-Sim-to-Real Navigation with Gaussian Splats from a Mob | ⭐ |
| [2025-m-olue-uthentic-ideo.md](2025-m-olue-uthentic-ideo.md) | (待补) | 2025-10 | VoluMe – Authentic 3D Video Calls from Live Gaussian Splat Prediction | ⭐ |
| [2025-y--eal-ime.md](2025-y--eal-ime.md) | (待补) | 2025-10 | GS-LIVM: Real-Time Photo-Realistic LiDAR-Inertial-Visual Mapping with Gaussian Splatting | ⭐ |
| [2025-y-tream-nline-eneralizable.md](2025-y-tream-nline-eneralizable.md) | (待补) | 2025-10 | StreamGS: Online Generalizable Gaussian Splatting Reconstruction for Unposed Image Streams | ⭐ |
| [2026-arxiv-2607-03872.md](2026-arxiv-2607-03872.md) | 2607.03872 | 2026-07 | SharpSplat: Edge-Regularized 3D Gaussian Splatting for High Fidelity Urban Building Recons | ⭐ |
| [2026-arxiv-2607-09260.md](2026-arxiv-2607-09260.md) | 2607.09260 | 2026-07 | AnythingReality: Robust Online Gaussian Splatting SLAM for Open-Vocabulary VR Scene Explor | ⭐ |
| [2026-arxiv-2607-11184.md](2026-arxiv-2607-11184.md) | 2607.11184 | 2026-07 | GeoGS-SLAM: Online Monocular Reconstruction Using Gaussian Splatting with Geometric Priors | ⭐ |
| [2026-arxiv-2607-12641.md](2026-arxiv-2607-12641.md) | 2607.12641 | 2026-07 | GeoFovea-GS: Geometry-Aware Cross-Layer Gaussian Splatting for Wireless Aerial VR | ⭐ |
| [2026-arxiv-2607-14481.md](2026-arxiv-2607-14481.md) | 2607.14481 | 2026-07 | Immediate 3D Gaussian Splat Reconstruction of Unordered Input with Global Consistency | ⭐ |
| [2026-arxiv-2607-15542.md](2026-arxiv-2607-15542.md) | 2607.15542 | 2026-07 | ImprovedVBGS: Real-time Continual Variational Bayes Gaussian Splatting | ⭐ |
| [2026-arxiv-2607-16624.md](2026-arxiv-2607-16624.md) | 2607.16624 | 2026-07 | SPARE-GS: Structural Parsimony and Resource Efficiency for 3D Gaussian Splatting | ⭐ |
| [2026-arxiv-2607-17965.md](2026-arxiv-2607-17965.md) | 2607.17965 | 2026-07 | Exploration Matters for Escaping the Blur Trap in 3D Gaussian Splatting | ⭐ |
| [2026-arxiv-2607-20325.md](2026-arxiv-2607-20325.md) | 2607.20325 | 2026-07 | MR-Compare: A Mixed-Reality Framework for Spatially Grounded Visual Comparison of 3D Gauss | ⭐ |
| [2026-arxiv-2607-25569.md](2026-arxiv-2607-25569.md) | 2607.25569 | 2026-07 | CORF-GS: Real-Time Wireless Radiance Field Reconstruction via Coupled Optical-RF Gaussian  | ⭐ |
| [2026-arxiv-2607-25971.md](2026-arxiv-2607-25971.md) | 2607.25971 | 2026-07 | SplatStream: Fine Granular Scalable Gaussian Splatting for Adaptive 3D Scene Streaming | ⭐ |
## E. 3DGS 静态加速 / 通用加速（63 篇）

| paper | arxiv id | year | 一句话 | 评 |
|---|---|---|---|---|
| [2023-kerbl-3dgs.md](2023-kerbl-3dgs.md) | 2308.04079 | 2023-08 | **3DGS 原论文**（INRIA, SIGGRAPH 2023 Best Paper），3D Gaussian Splatting for Real-Time Radiance Field Rendering | ⭐⭐⭐ |
| [2023-navaneet-compact3d.md](2023-navaneet-compact3d.md) | 2312.08826 | 2023-12 | Compact3D，ECCV 2024 | ⭐ |
| [2023-fan-lightgaussian.md](2023-fan-lightgaussian.md) | 2311.17245 | 2023-11 | LightGaussian，NeurIPS 2024 Spotlight | ⭐ |
| [2025-huang-seele.md](2025-huang-seele.md) | 2503.05168 | 2025-03 | SEELE（SJTU） | ⭐ |
| [2026-zhang-geta3dgs.md](2026-zhang-geta3dgs.md) | 2605.02086 | 2026-05 | **GETA-3DGS**，joint structured pruning + quantization | ⭐⭐ |
| [2026-li-vedal.md](2026-li-vedal.md) | 2606.02346 | 2026-06 | **VEDAL** (NUST+PolyU)，variational free-energy pruning，**5.2× comp, 0.31 dB PSNR drop, 185 FPS** | ⭐⭐ |
| [2026-chen-refine.md](2026-chen-refine.md) | 2606.09074 | 2026-06 | **REFINE** (西工大)，**3,000× pruning compute↓ + ~20× device-latency speedup**（Hessian-field 解析） | ⭐⭐ |
| [2026-zhao-ace-gs.md](2026-zhao-ace-gs.md) | 2606.21244 | 2026-06 | **ACE-GS** (单作者)，momentum consistency + statistical sensitivity，**4.5× 训练加速 + 745 FPS** | ⭐⭐ |
| [2026-zhao-mmgs.md](2026-zhao-mmgs.md) | 2605.19304 | 2026-05 | **MMGS** (CQU)，multi-view ranking + optimal transport，**10× comp, 10× 训练加速** | ⭐⭐ |
| [2026-mousa-provablepruning.md](2026-mousa-provablepruning.md) | 2607.02721 | 2026-07 | **Provable Pruning** (Univ. of Haifa)，**首个 3DGS 可证明 coreset theorem**，resolution-dependent importance score（理论意义大于工程加速比） | ⭐⭐ |
| [2026-hong-ploymerge.md](2026-hong-polymerge.md) | 2606.16232 | 2026-06 | **PolyMerge** (UC Berkeley)，polytope coverings + Crazyflie drone on-board CBF | ⭐⭐ |

> *注：PolyMerge 文件路径为 `2026-hong-polymerge.md`（修正拼写，之前为 `ploymerge`）*

---

## F. Survey / Roadmap（写作参考，1 篇）

| paper | arxiv id | year | 一句话 | 评 |
|---|---|---|---|---|
| [2025-youn-success-gs.md](2025-youn-success-gs.md) | 2512.07197 | 2025-12 | SUCCESS-GS survey，Parameter/Restructuring 二分法（Chung-Ang+Kyung Hee, 37 页） | ⭐⭐ |
| (内部 [docs/04-trends-2026H1.md](../../04-trends-2026H1.md)) | — | 2026-07 | 本项目自有趋势分析 | ⭐⭐⭐ |

---

## 总数与对照组

```
- **185 篇 paper notes ↔ 185 个本地 PDF**（一一对应，无遗漏）
- **约 790 MB 总计**（`.pdfs/`，截至 2026-07-08）
- **2023**：4 篇
- **2024 H1**：5 篇
- **2024 H2**：4 篇
- **2025 H1**：7 篇
- **2025 H2**：6 篇
- **2026 H1**：27 篇  ←  本批 3 (2026-07-09 cron) 加 4 篇 (mousa / poirier / song / zhou)
```
- 合计 54 + 6 + 1 = **61 篇** 已编 INDEX（v5.43 增 MVFusion-GS 后含 60 paper notes + INDEX.md = 61 .md）
- A. 4DGS 表示（13 篇）  ←  本批 4 加 1 (hu-mvfusion-gs, plug-in DeGauss)
- B. 4DGS 加速 / 动静态分离（7 篇）
- C. 渲染加速 / 移动端（14 篇）  ←  本批 3 加 2 (poirier-gray / zhou-temporalgs)
- D. 流式 streaming / 移动端落地（11 篇）  ←  本批 3 加 1 (mousa-provablepruning, 部署理论)
- E. 3DGS 静态加速 / 通用（9 篇）  ←  补 3DGS 原论文 (2023-kerbl-3dgs) + navaneet 命名修正
- F. Survey / Roadmap（1 篇）
- **合计 61 篇**

---

## ⚠️ 已知空白（待补 paper notes）

下面是 README / §02 / §04 提到但**还没写独立 paper note** 的（虽然 PDF 已在 `.pdfs/` 或尚未下）：

- **动静态分离专门派**: Drivable 3DGS（2503.15882）/ SVG4D（2505.02957）/ ZAWoR（2506.23514）— abstract 已在 §01 §6 中引用，但**未单独建 paper note**
- **3DGS 加速派**: EffiGaussian++（2505.14919）/ HiP-GS（2503.17903）/ GO-VAE（2504.15644）/ MP-GS（2601.07918）/ Neo mobile 实测 / GaussianStream（2510.16862）
- **Survey**: Deep Review（2504.19053）/ Pipeline Survey（2507.19122）/ LoWiS（2504.09080）

→ **这是下一轮调研该补的方向**（用户应该明示 PR 优先级）

---

## 重新下载某个 PDF

```bash
cd .pdfs
curl -sL --max-time 90 -o <arxiv-id>.pdf https://arxiv.org/pdf/<arxiv-id>
```

如要给新加的 paper note 配 PDF，**用纯 arxiv id 命名**（如 `2603.11531.pdf`），不用易读名；**不要 commit**（已在 `.gitignore` 排除整个 `.pdfs/` 目录）。

## G. 4DGS 前身 / 数据集 / 相关工作（6 篇）  ←  v5.42 补全 survey.bib cite key, v5.44 删 2017-simon-handkeypoint（17 年早于 3DGS 提出, 不属 4DGS 调研范围）

| paper | arxiv id | year | 一句话 | 评 |
|---|---|---|---|---|
| [2023-kerbl-3dgs.md](2023-kerbl-3dgs.md) | 2308.04079 | 2023-08 | 3DGS 原论文, SIGGRAPH 2023 Best Paper (INRIA) | ⭐⭐⭐ |
| [2023-navaneet-compact3d.md](2023-navaneet-compact3d.md) | 2311.18159 | 2023-11 | CompGS/Compact3D, residual VQ, 15× reduction + 200+ FPS (UMBC) | ⭐⭐ |
| [2021-pumarola-dnerf.md](2021-pumarola-dnerf.md) | 2011.13961 | 2020-11 | D-NeRF, monocular dynamic NeRF (UB+ETH) | ⭐⭐ |
| [2021-park-nerfies.md](2021-park-nerfies.md) | 2011.12948 | 2020-11 | Nerfies, deformable NeRF (Google+UW) | ⭐⭐ |
| [2021-park-hypernerf.md](2021-park-hypernerf.md) | 2106.13228 | 2021-06 | HyperNeRF, topology-varying + vrig dataset (Google) | ⭐⭐ |
| [2022-gao-dycheck.md](2022-gao-dycheck.md) | 2210.13445 | 2022-10 | DyCheck iPhone dataset, 5 scenes (UCB+FAIR+Google) | ⭐⭐ |

| [2025-a-iummer-ulti-uidance.md](2025-a-iummer-ulti-uidance.md) | (待补) | 2025-10 | MiDSummer: Multi-Guidance Diffusion for Controllable Zero-Shot Immersive Gaussian Splattin | ⭐ |
| [2025-a-o-ense-.md](2025-a-o-ense-.md) | (待补) | 2025-10 | ToF-Splatting: Dense SLAM using Sparse Time-of-Flight Depth and Multi-Frame Integration | ⭐ |
| [2025-a-platalk-.md](2025-a-platalk-.md) | (待补) | 2025-10 | SplatTalk: 3D VQA with Gaussian Splatting | ⭐ |
| [2025-b-tealthttack-obust-oisoning.md](2025-b-tealthttack-obust-oisoning.md) | (待补) | 2025-10 | StealthAttack: Robust 3D Gaussian Splatting Poisoning via Density-Guided Illusions | ⭐ |
| [2025-c-aight-plats-patially.md](2025-c-aight-plats-patially.md) | (待补) | 2025-10 | GaSLight: Gaussian Splats for Spatially-Varying Lighting in HDR | ⭐ |
| [2025-c-eam360-eamless-eal.md](2025-c-eam360-eamless-eal.md) | (待补) | 2025-10 | Seam360GS: Seamless 360° Gaussian Splatting from Real-World Omnidirectional Images | ⭐ |
| [2025-c-elf-nsembling-ew.md](2025-c-elf-nsembling-ew.md) | (待补) | 2025-10 | Self-Ensembling Gaussian Splatting for Few-Shot Novel View Synthesis | ⭐ |
| [2025-c-esson-plats-eacher.md](2025-c-esson-plats-eacher.md) | (待补) | 2025-10 | A Lesson in Splats: Teacher-Guided Diffusion for 3D Gaussian Splats Generation with 2D Sup | ⭐ |
| [2025-c-ong--ong.md](2025-c-ong--ong.md) | (待补) | 2025-10 | Long-LRM: Long-sequence Large Reconstruction Model for Wide-coverage Gaussian Splats | ⭐ |
| [2025-g-ixture-xperts-uided.md](2025-g-ixture-xperts-uided.md) | (待补) | 2025-10 | Mixture of Experts Guided by Gaussian Splatters Matters: A new Approach to Weakly-Supervis | ⭐ |
| [2025-h-ae-elightable-utdoor.md](2025-h-ae-elightable-utdoor.md) | (待补) | 2025-10 | GaRe: Relightable 3D Gaussian Splatting for Outdoor Scenes from Unconstrained Photo Collec | ⭐ |
| [2025-h-econ-eneralizable-urface.md](2025-h-econ-eneralizable-urface.md) | (待补) | 2025-10 | GSRecon: Efficient Generalizable Gaussian Splatting for Surface Reconstruction from Sparse | ⭐ |
| [2025-h-hysplat-hysics-imulation.md](2025-h-hysplat-hysics-imulation.md) | (待补) | 2025-10 | PhysSplat: Efficient Physics Simulation for 3D Scenes via MLLM-Guided Gaussian Splatting | ⭐ |
| [2025-h-ideoplat-irect-cene.md](2025-h-ideoplat-irect-cene.md) | (待补) | 2025-10 | VideoRFSplat: Direct Scene-Level Text-to-3D Gaussian Splatting Generation with Flexible Po | ⭐ |
| [2025-h-obust-asked-art.md](2025-h-obust-asked-art.md) | (待补) | 2025-10 | Robust 3D-Masked Part-level Editing in 3D Gaussian Splatting with Regularized Score Distil | ⭐ |
| [2025-h-ogplat-obust-enerative.md](2025-h-ogplat-obust-enerative.md) | (待补) | 2025-10 | RogSplat: Robust Gaussian Splatting via Generative Priors | ⭐ |
| [2025-h-plats-bservation-ompleten.md](2025-h-plats-bservation-ompleten.md) | (待补) | 2025-10 | OCSplats: Observation Completeness Quantification and Label Noise Separation in 3DGS | ⭐ |
| [2025-j--earning-ree.md](2025-j--earning-ree.md) | (待补) | 2025-10 | LUDVIG: Learning-Free Uplifting of 2D Visual Features to Gaussian Splatting Scenes | ⭐ |
| [2025-j-nsideut-ntegrated-.md](2025-j-nsideut-ntegrated-.md) | (待补) | 2025-10 | InsideOut: Integrated RGB-Radiative Gaussian Splatting for Comprehensive 3D Object Represe | ⭐ |
| [2025-j-onstrained-ptimization-ppro.md](2025-j-onstrained-ptimization-ppro.md) | (待补) | 2025-10 | A Constrained Optimization Approach for Gaussian Splatting from Coarsely-posed Images and  | ⭐ |
| [2025-j-reeplatter-ose-free.md](2025-j-reeplatter-ose-free.md) | (待补) | 2025-10 | FreeSplatter: Pose-free Gaussian Splatting for Sparse-view 3D Reconstruction | ⭐ |
| [2025-k-enerative-enerating-cenes.md](2025-k-enerative-enerating-cenes.md) | (待补) | 2025-10 | Generative Gaussian Splatting: Generating 3D Scenes with Video Diffusion Priors | ⭐ |
| [2025-k-eoplatting-owards-eometry.md](2025-k-eoplatting-owards-eometry.md) | (待补) | 2025-10 | GeoSplatting: Towards Geometry Guided Gaussian Splatting for Physically-based Inverse Rend | ⭐ |
| [2025-l---ontrastive.md](2025-l---ontrastive.md) | (待补) | 2025-10 | CCL-LGS: Contrastive Codebook Learning for 3D Language Gaussian Splatting | ⭐ |
| [2025-l-aussianpdate-ontinual-pdat.md](2025-l-aussianpdate-ontinual-pdat.md) | (待补) | 2025-10 | GaussianUpdate: Continual 3D Gaussian Splatting Update for Changing Environments | ⭐ |
| [2025-m--ierarchical-rban.md](2025-m--ierarchical-rban.md) | (待补) | 2025-10 | HUG: Hierarchical Urban Gaussian Splatting with Block-Based Reconstruction for Large-Scale | ⭐ |
| [2025-m-nterdit-nteractive-ditin.md](2025-m-nterdit-nteractive-ditin.md) | (待补) | 2025-10 | InterGSEdit: Interactive 3D Gaussian Splatting Editing with 3D Geometry-Consistent Attenti | ⭐ |
| [2025-m-oteplat-ough-oting.md](2025-m-oteplat-ough-oting.md) | (待补) | 2025-10 | VoteSplat: Hough Voting Gaussian Splatting for 3D Scene Understanding | ⭐ |
| [2025-p-adarplat-adar-igh.md](2025-p-adarplat-adar-igh.md) | (待补) | 2025-10 | RadarSplat: Radar Gaussian Splatting for High-Fidelity Data Synthesis and 3D Reconstructio | ⭐ |
| [2025-q--elightable-parse.md](2025-q--elightable-parse.md) | (待补) | 2025-10 | SU-RGS: Relightable 3D Gaussian Splatting from Sparse Views under Unconstrained Illuminati | ⭐ |
| [2025-q--utual-boosted.md](2025-q--utual-boosted.md) | (待补) | 2025-10 | MGSR: 2D/3D Mutual-boosted Gaussian Splatting for High-fidelity Surface Reconstruction und | ⭐ |
| [2025-s--nifying-ision.md](2025-s--nifying-ision.md) | (待补) | 2025-10 | CLIP-GS: Unifying Vision-Language Representation with 3D Gaussian Splatting | ⭐ |
| [2025-s-e-aluable-ssistant.md](2025-s-e-aluable-ssistant.md) | (待补) | 2025-10 | NeRF Is a Valuable Assistant for 3D Gaussian Splatting | ⭐ |
| [2025-s-eovatar-daptive-eometrical.md](2025-s-eovatar-daptive-eometrical.md) | (待补) | 2025-10 | GeoAvatar: Adaptive Geometrical Gaussian Splatting for 3D Head Avatar | ⭐ |
| [2025-s-ontra-odebook-ondensed.md](2025-s-ontra-odebook-ondensed.md) | (待补) | 2025-10 | ContraGS: Codebook-Condensed and Trainable Gaussian Splatting for Fast, Memory-Efficient R | ⭐ |
| [2025-s-plrt-rticulation-stimation.md](2025-s-plrt-rticulation-stimation.md) | (待补) | 2025-10 | SplArt: Articulation Estimation and Part-Level Reconstruction with 3D Gaussian Splatting | ⭐ |
| [2025-t---tructure.md](2025-t---tructure.md) | (待补) | 2025-10 | SEGS-SLAM: Structure-enhanced 3D Gaussian Splatting SLAM with Appearance Embedding | ⭐ |
| [2025-t-riven-ulti-obust.md](2025-t-riven-ulti-obust.md) | (待补) | 2025-10 | 3D Gaussian Splatting Driven Multi-View Robust Physical Adversarial Camouflage Generation | ⭐ |
| [2025-w-aussiancc-ully-elf.md](2025-w-aussiancc-ully-elf.md) | (待补) | 2025-10 | GaussianOcc: Fully Self-supervised and Efficient 3D Occupancy Estimation with Gaussian Spl | ⭐ |
| [2025-w-iberated-ndependent-f.md](2025-w-iberated-ndependent-f.md) | (待补) | 2025-10 | Liberated-GS: 3D Gaussian Splatting Independent from SfM Point Clouds | ⭐ |
| [2025-w-plat-ontext-ware.md](2025-w-plat-ontext-ware.md) | (待补) | 2025-10 | CATSplat: Context-Aware Transformer with Spatial Guidance for Generalizable 3D Gaussian Sp | ⭐ |
| [2025-x-azeaussian-igh-idelity.md](2025-x-azeaussian-igh-idelity.md) | (待补) | 2025-10 | GazeGaussian: High-Fidelity Gaze Redirection with 3D Gaussian Splatting | ⭐ |
| [2025-x-utocc-utomatic-pen.md](2025-x-utocc-utomatic-pen.md) | (待补) | 2025-10 | AutoOcc: Automatic Open-Ended Semantic Occupancy Annotation via Vision-Language Guided Gau | ⭐ |
| [2025-y---ree.md](2025-y---ree.md) | (待补) | 2025-10 | PCR-GS: COLMAP-Free 3D Gaussian Splatting via Pose Co-Regularizations | ⭐ |
| [2025-y-elf-alibrating-arge.md](2025-y-elf-alibrating-arge.md) | (待补) | 2025-10 | Self-Calibrating Gaussian Splatting for Large Field-of-View Reconstruction | ⭐ |
| [2025-y-ol-olarimetric-eflective.md](2025-y-ol-olarimetric-eflective.md) | (待补) | 2025-10 | PolGS: Polarimetric Gaussian Splatting for Fast Reflective Surface Reconstruction | ⭐ |
| [2025-y-patialplat-emantic-parse.md](2025-y-patialplat-emantic-parse.md) | (待补) | 2025-10 | SpatialSplat: Efficient Semantic 3D from Sparse Unposed Images | ⭐ |
| [2025-y-u-ulti-aseline.md](2025-y-u-ulti-aseline.md) | (待补) | 2025-10 | MuGS: Multi-Baseline Generalizable Gaussian Splatting Reconstruction | ⭐ |
| [2025-y-une-our-tyle.md](2025-y-une-our-tyle.md) | (待补) | 2025-10 | Tune-Your-Style: Intensity-tunable 3D Style Transfer with Gaussian Splatting | ⭐ |
| [2025-z-2aussian-nchor-raph.md](2025-z-2aussian-nchor-raph.md) | (待补) | 2025-10 | AG2aussian: Anchor-Graph Structured Gaussian Splatting for Instance-Level 3D Scene Underst | ⭐ |
| [2025-z-3-rbitrary-rtistic.md](2025-z-3-rbitrary-rtistic.md) | (待补) | 2025-10 | A3GS: Arbitrary Artistic Style into Arbitrary 3D Gaussian Splatting | ⭐ |
| [2025-z-nstant-aussianmage-enerali.md](2025-z-nstant-aussianmage-enerali.md) | (待补) | 2025-10 | Instant GaussianImage: A Generalizable and Self-Adaptive Image Representation via 2D Gauss | ⭐ |
| [2025-z-uadratic-igh-uality.md](2025-z-uadratic-igh-uality.md) | (待补) | 2025-10 | Quadratic Gaussian Splatting: High Quality Surface Reconstruction with Second-order Geomet | ⭐ |
| [2025-z-urve-ware-arametric.md](2025-z-urve-ware-arametric.md) | (待补) | 2025-10 | Curve-Aware Gaussian Splatting for 3D Parametric Curve Reconstruction | ⭐ |
| [2026-arxiv-2607-03819.md](2026-arxiv-2607-03819.md) | 2607.03819 | 2026-07 | CGGS: Consistency-Augmented Geometric Gaussian Splatting for Ego-Centric 3D Scene Generati | ⭐ |
| [2026-arxiv-2607-05347.md](2026-arxiv-2607-05347.md) | 2607.05347 | 2026-07 | WildSplat: Feedforward Gaussian Splatting from Unposed In-the-Wild Images | ⭐ |
| [2026-arxiv-2607-05598.md](2026-arxiv-2607-05598.md) | 2607.05598 | 2026-07 | SSA-3DGS: Unsupervised Removal of Screen-Space Artifacts for 3D Gaussian Splatting | ⭐ |
| [2026-arxiv-2607-07452.md](2026-arxiv-2607-07452.md) | 2607.07452 | 2026-07 | GeoGS-SLAM: Geometry-Only Gaussian Splatting for Dense Monocular SLAM | ⭐ |
| [2026-arxiv-2607-10050.md](2026-arxiv-2607-10050.md) | 2607.10050 | 2026-07 | SyncSpace: Layout-Conditioned 3D Gaussian Splatting for Space Reskinning in Mixed Reality | ⭐ |
| [2026-arxiv-2607-10912.md](2026-arxiv-2607-10912.md) | 2607.10912 | 2026-07 | DP-Splat: Bayesian Nonparametric Complexity Control for Gaussian Splatting | ⭐ |
| [2026-arxiv-2607-10995.md](2026-arxiv-2607-10995.md) | 2607.10995 | 2026-07 | AsySplat: Efficient Asymmetric 3D Gaussian Splatting for Long-Sequence Scene Modeling | ⭐ |
| [2026-arxiv-2607-12785.md](2026-arxiv-2607-12785.md) | 2607.12785 | 2026-07 | ExtraGS: Enhancing Endoscopic View Extrapolation via Diffusion-Guided 3D Gaussian Splattin | ⭐ |
| [2026-arxiv-2607-13682.md](2026-arxiv-2607-13682.md) | 2607.13682 | 2026-07 | Calibrated Closed-Form Uncertainty for Radiative Gaussian Splatting in Sparse-View CT | ⭐ |
| [2026-arxiv-2607-15536.md](2026-arxiv-2607-15536.md) | 2607.15536 | 2026-07 | E3DGS: Unified Geometric-Photometric Equivariance for 3D Gaussian Splatting via Color-as-G | ⭐ |
| [2026-arxiv-2607-17773.md](2026-arxiv-2607-17773.md) | 2607.17773 | 2026-07 | FillGauss: Fine-Grained Filling-Aware Impact Sound Generation for 3D Gaussian Splatting | ⭐ |
| [2026-arxiv-2607-17803.md](2026-arxiv-2607-17803.md) | 2607.17803 | 2026-07 | FF-ProCams: Feed-Forward Gaussian Splatting for Projector-Camera System | ⭐ |
| [2026-arxiv-2607-18801.md](2026-arxiv-2607-18801.md) | 2607.18801 | 2026-07 | ZeroSplat: Generalized Referring Segmentation in 3D Gaussian Splatting | ⭐ |
| [2026-arxiv-2607-19777.md](2026-arxiv-2607-19777.md) | 2607.19777 | 2026-07 | Look Before You Edit: Attention-Guided Camera Placement and Multi-View Alignment for 3D Ga | ⭐ |
| [2026-arxiv-2607-20417.md](2026-arxiv-2607-20417.md) | 2607.20417 | 2026-07 | ATSplat: Compact Feed-forward 3D Gaussian Splatting with Adaptive Token Expansion | ⭐ |
| [2026-arxiv-2607-26595.md](2026-arxiv-2607-26595.md) | 2607.26595 | 2026-07 | SpatialQ: Understanding 3D Gaussian Splatting Scene Quality via Visual-based MLLM | ⭐ |
| [2026-arxiv-2607-26889.md](2026-arxiv-2607-26889.md) | 2607.26889 | 2026-07 | StructureGS: Structure-aware Gaussian Splatting for Articulated Object Reconstruction | ⭐ |
