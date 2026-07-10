# 2024-li-spacetime-gaussians · Spacetime Gaussian Feature Splatting for Real-Time Dynamic View Synthesis

> **相关性**:**高度相关** — 同期(CVPR 2024)4DGS 范式,**与 Wu 4DGS(2023-10)同思路,实现路径不同**;直接对标 4DGS-1K 的"per-Gaussian 时间建模"路线。**本项目 mobile 4DGS rendering 的"per-Gaussian trajectory"思路来源**。

## 0.5 元数据

- **venue**: CVPR 2024
- **arxiv-id**: 2312.16812
- **s2-id**: （v2 用 Semantic Scholar API 补全）
- **homepage**: （无）
- **github**: https://github.com/oppo-us-research/SpacetimeGaussians
- **status**: received
- **收录日期**: 2026-07-08（首次）
- **收录来源**: arxiv scan + 1-hop 引用规则
- **1-hop 引用**: （v2 补全，见 §11 1-hop 关系图）
- **评级**: ⭐

- **survey_section**: 3
## 一句话问题
如何让 4D 高斯显式包含"时间轨迹",从而在动态场景中实现**实时 + 高质量**渲染?

## 链接(均经 fetch + GitHub README 实测)
- arxiv: <https://arxiv.org/abs/2312.16812>(v1 2023-12-27)
- 项目页 / GitHub: <https://github.com/oppo-us-research/SpacetimeGaussians>(README 实测)
- PDF:**未下**(budget 限制)—— abstract 直引

## 年份 / 作者 / 机构(arxiv metadata + GitHub README 实测)
- **年份**:2024(CVPR 2024 录用)
- **第一作者**:Zhan Li(李展,OPPO US Research)
- **完整作者列表**:Zhan Li, Zhang Chen, Zhong Li, Yi Xu
- **机构**:**OPPO US Research Center** + **Portland State University**(波特兰州立大学)
- **会议 / 出版**:**CVPR 2024**(GitHub README 标题直引:`[CVPR 2024]`)

## 方法核心(abstract 直引 + 4DGS-1K Table 1 跨源验证)
1. **"Spacetime Gaussian"概念**:把每个 3D 高斯 + **显式的 per-Gaussian 时间轨迹(time trajectory)** 合并为"4D spacetime Gaussian"
2. **特征 splatting**:对每条时间轨迹用一组可学习特征参数化,渲染时通过时间插值得到任意 t 的高斯参数
3. **不需要 canonical space + deformation**:与 4DGS(Wu 2023)的 canonical + HexPlane 范式**不同**;Spacetime Gaussians 是 **"per-Gaussian 直接显式轨迹"** 路线
4. **实时渲染**:沿用 3DGS splatting,推理时不需要 deformation MLP
5. **4DGS-1K Table 1 / Table 2 中的 baseline**:从 4DGS-1K Table 1 N3V 行:`4DGaussian [39] = PSNR 31.15 / SSIM 0.940 / LPIPS 0.049 / Storage 90 MB / FPS 30` —— **4DGS-1K 论文引用的 [39] 即本文**

## 关键数字(4DGS-1K Table 1 / Table 3 跨源验证)
- **N3V(Coffee Martini,300 frames @ 1352×1014)**:
  - PSNR **31.15** dB
  - SSIM **0.940**
  - LPIPS **0.049**
  - Storage **90 MB**
  - FPS **30**
  - Raster FPS — (`未在跨源验证中拿到`)
  - #Gauss — (`未在跨源验证中拿到`)
- **D-NeRF synthetic(800×800)**:**未在 4DGS-1K Table 2 引用 4DGaussian [39] 行** —— `未在跨源验证中拿到 D-NeRF 数字`
- **训练 GPU / 时长**:`abstract 未给`
- **训练显存**:`abstract 未给`

### 与本项目真·对标 4DGS-1K 的同台对比(N3V)
| 维度 | Spacetime Gaussian(本文) | 4DGS-1K | 差距 |
|---|---|---|---|
| FPS @ N3V | 30 | 805 | 4DGS-1K **26.8× 更快** |
| PSNR @ N3V | 31.15 | 31.88 | 4DGS-1K +0.73 dB |
| Storage(MB)| 90 | 418(no-PP) / 50(PP) | 4DGS-1K-PP 1.8× 更小 |

> **结论**:**Spacetime Gaussians 是 4DGS-1K 真本发布前的同期 SOTA**,被 4DGS-1K 全面超越;**但其"per-Gaussian 时间轨迹"思想值得在 M3 阶段借鉴**。

## 与本调研主线的关系

### 1. 主线对标(同期 SOTA,**"per-Gaussian 轨迹"分支**)
- Spacetime Gaussians = 4DGS 加速路线的 **"per-Gaussian 显式时间轨迹"** 分支
- 4DGS(Wu 2023) = **"canonical + HexPlane deformation"** 分支
- 4D-RotorGS(2024)= **"4D 旋转"** 分支
- 4DGS-1K(2025)= **"STV pruning + Temporal Filter mask"** 分支
- **Spacetime Gaussians 是 Wu 4DGS 的"per-Gaussian 版本"** —— 把 deformation MLP 拆解到每个 Gaussian 上,牺牲 per-Gaussian 参数换取并行度

### 2. 借鉴价值
- **per-Gaussian 时间轨迹**思想:**对 mobile GPU 友好** —— **per-Gaussian 状态可独立存储 / 缓存 / 复用**
- **30 FPS @ N3V** 是 4DGS-1K 805 FPS 的 1/27,**说明 4DGS-1K 的 STV pruning 是跨越式提升** —— `未在公开材料找到` 4DGS-1K 之前有 work 接近 1000 FPS
- **同思路同源**:OPPO US Research 是工业界团队,**说明 4DGS 工业落地在 2024 年已经开始**

### 3. 不可作为移动端最终方案
- **30 FPS @ N3V @ RTX 3090** 是上限,Adreno 8 Gen 4 上难以满足 30+ FPS @ 1080p
- **90 MB / scene storage 仍偏大** —— 不适合 mobile 4~8 GB 共享显存预算
- **PyTorch + CUDA 实现**:`未在公开材料找到` mobile / Vulkan 版本

### 4. 对采集端反推
- N3V(20 cameras, half-res 1352×1014, 6 scenes, 300 frames):**多相机同步 + 高分辨率** → **与本项目"高速相机阵列"完全对位**
- **300 frames × 6 scenes = 1800 frames** 训练预算:**~ 40 min / scene × 6 = 4 hr / dataset**(从 4DGS Table 3 N3V 训练时长推断)

## 我未找到 / 提请下游注意
- **D-NeRF 数字**:`abstract 未给`,4DGS-1K Table 2 也没引用 Spacetime Gaussians 行
- **#Gauss / 训练显存**:`abstract 未给`
- **训练时长 / scene**:`abstract 未给`
- **PDF 全文**:本笔记**未下**
- **GitHub commit 是否包含 mobile backend**:`未在公开材料找到`

## 我的 commit 节奏
- 本文为 5 篇新工作笔记之 3。
- 下游 `02-rendering-acceleration.md` §3(加速技术树)应把 Spacetime Gaussians 归到 **"per-Gaussian 显式时间轨迹"分支**,与 **"HexPlane deformation"** / **"4D 旋转"** / **"STV pruning"** 三者并列。

## 引用一览
- <https://arxiv.org/abs/2312.16812>(abstract 实测)
- <https://github.com/oppo-us-research/SpacetimeGaussians>(README 实测)
- `/Users/klkjjhjkhjhg/Codes/4dgs-mobile-rendering/docs/appendix/paper-notes/2025-yuan-4dgs-1k.md` Table 1(同源 cross-check)
