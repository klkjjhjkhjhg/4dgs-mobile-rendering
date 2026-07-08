# 2023-kerbl-3dgs · 3D Gaussian Splatting for Real-Time Radiance Field Rendering

> **本项目地位**：**⭐⭐⭐ 起点 / 引用密度最高的 paper**。所有 49 篇后续工作的引用基线。
> **收录原因**：件套 3 5 篇示范验证时发现 3DGS 原论文不在 49 篇 INDEX 里（被 5 篇示范同时引用），属于核心引用盲点。

## 0.5 元数据

- **venue**: SIGGRAPH 2023
- **arxiv-id**: 2308.04079
- **s2-id**: （v2 用 Semantic Scholar API 补全）
- **homepage**: （无）
- **github**: https://github.com/graphdeco-inria/gaussian-splatting
- **status**: received
- **收录日期**: 2026-07-08
- **收录来源**: 1-hop 引用规则（5 篇示范 paper 均引用此 paper）
- **1-hop 引用**: 49 篇后续工作全部引用（引用密度最高）
- **评级**: ⭐⭐⭐

## 一句话问题

如何用各向异性 3D 高斯做辐射场（radiance field）表示，**用纯 splatting 光栅化**替代 NeRF 的体积渲染，**在桌面 GPU 上达到 30+ FPS @ 1080p**？

## 链接

- arxiv: <https://arxiv.org/abs/2308.04079>（v1 2023-08-08）
- GitHub: <https://github.com/graphdeco-inria/gaussian-splatting>（官方实现）
- PDF: 未本地存档（公开开源）
- 会议: SIGGRAPH 2023

## 年份 / 作者 / 机构

- **年份**: 2023（SIGGRAPH 2023）
- **第一作者**: Bernhard Kerbl
- **机构**: Inria, Université Côte d'Azur（法国国家信息与自动化研究院）

## 方法核心

1. **3D 高斯作为场景表示**：用各向异性 3D 高斯（均值 μ + 协方差 Σ）替代 NeRF 的 MLP
2. **SfM 初始化**：从 COLMAP 点云初始化高斯位置
3. **可微分光栅化**：把 3D 高斯 splat 到 2D 图像平面，**用纯 splatting 不采样光线**
4. **自适应密度控制**：每 100 步对高斯做 clone / split / prune
5. **球谐函数表示颜色**：view-dependent color

## 关键数字

- **训练**: 单 A6000 GPU 35-45 分钟
- **渲染**: 桌面 RTX A6000 30+ FPS @ 1080p（论文 Table 2）
- **质量**: Mip-NeRF 360 数据集上 PSNR 与 Mip-NeRF 360 持平
- **存储**: ~100-500 MB per scene（高斯数量 ~1-5M）

## 11. 1-hop 关系图

### 11.1 引用的相关工作 (downstream)

3DGS 原论文是**起点**——后续几乎所有 3DGS / 4DGS 工作都引用它：

- 3DGS → 4DGS 演化：[2024-wu-4dgs](2024-wu-4dgs.md)（4DGS 原论文）+ [2023-yang-deformable-3dgs](2023-yang-deformable-3dgs.md)（Deformable 3DGS）
- 3DGS 加速：[2024-yu-mip-splatting](2024-yu-mip-splatting.md) + [2023-fan-lightgaussian](2023-fan-lightgaussian.md) + [2024-liu-efficientgs](2024-liu-efficientgs.md)
- 3DGS 移动端：[2025-feng-lumina](2025-feng-lumina.md) + [2026-du-mobile-gs](2026-du-mobile-gs.md) + [2026-du-flux-gs](2026-du-flux-gs.md)
- 4DGS-1K：[2025-yuan-4dgs-1k](2025-yuan-4dgs-1k.md) 等

### 11.2 被引用的后续工作 (upstream)

**全部 49 篇后续工作均引用此 paper**（引用密度最高）。
**v2 用 S2 API 自动拉取完整 cited-by 列表**。
