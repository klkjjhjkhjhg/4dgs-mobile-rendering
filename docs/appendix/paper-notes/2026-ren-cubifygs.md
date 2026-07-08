# 2026-ren-cubifygs · CubifyGS: Object-Centric 3D Gaussian Splatting for Lifelong Dynamic Scene Maintenance

> **相关性**：**⭐ 派系 2+3（动静态分离 + 移动端）** —— arXiv 2026-06-27；核心数字：**20 FPS map maintenance, >40× faster than WildGS-SLAM**（abstract 直引）；**+35.83% avg PSNR improvement over MonoGS, +7.58 dB on Bedroom-1**（PDF Table II 直引）。**Object-level 资产化 + spatio-temporal dynamics + 终身动态场景维护**——Lifelong dynamic SLAM 范式。

> **⚠ 重要区分**：这是 **3DGS（静态 per object）+ 4DGS（rigid object rearrangement over time）** 的混合工作，**不是完整 4DGS**。**测试平台：RTX 4090**（不是 mobile GPU）。**对本项目 4DGS Mobile 适用性较弱**，但**对 dynamic SLAM 路线有价值**。

## 0.5 元数据

- **venue**: arxiv pre-print (2026-06)
- **arxiv-id**: 2606.28720
- **s2-id**: （v2 用 Semantic Scholar API 补全）
- **homepage**: （无）
- **github**: （无）
- **status**: under review
- **收录日期**: 2026-07-08
- **收录来源**: arxiv scan + 1-hop 引用规则
- **1-hop 引用**: （v2 补全，见 §11 1-hop 关系图）
- **评级**: ⭐

## 一句话问题

现有 3DGS SLAM 在 **rigid object rearrangement**（家具移动 / 物体出现消失）场景下，**需要 erase-and-reconstruct 全场景**——**如何做到 object-level 资产复用 + 终身动态维护**？

## 链接

- arXiv：<https://arxiv.org/abs/2606.28720>（v2 2026-06-27）
- 项目页：not found in abstract
- GitHub：not found in PDF
- PDF：已下 `.pdfs/2606.28720.pdf`
- 会议：not found in abstract（arXiv preprint）

## 年份 / 作者 / 机构（PDF 头部实测）

- **年份**：2026（v1 2026-06-27，v2 2026-06-27）
- **第一作者**：**Bohan Ren**
- **机构**：中国（具体学校待 PDF 全文确认）—— `not found in first 8 pages extract`

## 方法核心（PDF §3 直引）

### §3.1 Object-Centric Mapping

- 把场景拆成 **movable instances**（可移动物体）+ **static background**（静态背景）
- 每个 movable instance 作为 **reusable Gaussian asset**（一次训练，多次复用）
- **资产检索 / 刚性变换 / 剪枝** 全在 asset 级别做

### §3.2 Spatio-Temporal Dynamics Perception

- Event-triggered adaptive optimization：检测到 rearrangement event 时**只重训**受影响的 asset
- Background inpainting：物体移走后**快速填回 background Gaussian**
- **结果**：~20 FPS map maintenance 速度（远快于 0.5 FPS 的 WildGS-SLAM）

### §3.3 高保真 dynamic rearrangement benchmark

- 论文**新发布了一个高保真动态场景 benchmark**（具体名字待 PDF 完整阅读）

## 关键数字（PDF Table II 直引）

| 场景 | 方法 | PSNR↑ | SSIM↑ | LPIPS↓ |
|---|---|---|---|---|
| Office-1 | CubifyGS | **17.98** | 0.537 | 0.548 |
| Office-1 | MonoGS | 10.08 | 0.314 | 0.669 |
| Office-1 | WildGS-SLAM | 11.61 | 0.410 | 0.677 |
| Bedroom-1 | CubifyGS | (avg) | — | — |
| avg | CubifyGS | **+35.83%** over MonoGS | — | — |
| Bedroom-1 best | CubifyGS | **+7.58 dB** over MonoGS | — | — |

> **abstract 直引**："~20 FPS map maintenance, **>40× faster than WildGS-SLAM** (which is <0.5 FPS)."

## 与本调研主线的关系

### 派系归属：**派系 2（动静态分离 / 4DGS）** 辅，**派系 3（移动端）** 弱

- **派系 2 应用**：**object-level asset 复用**是 4DGS 动静态分离的另一种思路（vs 4DGS-CC 的 contextual coding）—— 4DGS canonical space 的物体 = asset，**temporal 维度只更新 asset transform**
- **派系 3 应用**：20 FPS 在 RTX 4090 上意味着 **移动端不可直接用**（RTX 4090 ≈ 80+ TOPS vs Snap 8 Gen 3 ~10 TOPS = 8× 算力差），**Snap 8 Gen 3 上估算 2-3 FPS**（`[推测]`）

### 对项目目标的具体承诺

- **4DGS Mobile 路线价值有限**：CubifyGS 是 3DGS + 刚性 rearrangement，**本项目 4DGS 关注的是非刚体动态**（人物动作、软体形变）—— CubifyGS 不能直接套
- **但 object-level 资产管理思想可借鉴**：本项目 M4/M5 如果做"长期运行的 4DGS 场景"，**asset-level update 比 frame-level update 省 100× 计算**（`[推测,基于 40× speedup 直引]`）

### 我未找到 / 提请下游注意

- **CubifyGS 测试 GPU 平台**：PDF Table II 标注 "RTX 4090"——**确认不是 mobile GPU**
- **CubifyGS 训练数据集**：abstract 提"高保真 dynamic rearrangement benchmark"——**需要查 benchmark 名字以判断是否与本项目 Dyn/HyperNeRF 子集兼容**
- **CubifyGS 的开源代码**：PDF 未给 GitHub 链接
- **对 4DGS non-rigid 动态的支持**：object-centric 范式**严格只支持 rigid**——**对人物动作 / 软体形变 = 不适用**

## 我的 commit 节奏

本文是 33 + 1 (Flux-GS) + 9 (subagent) 之外**新加的第 44 篇**。配套 INDEX.md 派系 B（4DGS 动静态分离）加 1 行。
