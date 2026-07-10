# 2023-fan-lightgaussian · LightGaussian: Unbounded 3D Gaussian Compression with 15× Reduction and 200+ FPS

> **相关性**:**中等相关** — 静态 3DGS 15× 压缩 + 200+ FPS 的**轻量级"后处理"加速**,**对 mobile 端** bitpack 路线**直接借鉴价值**;与 MEGA 思路不同(MEGA 是 SH→DC+AC 训练时;LightGaussian 是训练后 prune + VQ)。

## 0.5 元数据

- **venue**: CVPR 2024
- **arxiv-id**: 2311.17245
- **s2-id**: （v2 用 Semantic Scholar API 补全）
- **homepage**: https://lightgaussian.github.io/
- **github**: https://github.com/VITA-Group/LightGaussian
- **status**: received
- **收录日期**: 2026-07-08（首次）
- **收录来源**: arxiv scan + 1-hop 引用规则
- **1-hop 引用**: （v2 补全，见 §11 1-hop 关系图）
- **评级**: ⭐⭐

- **survey_section**: 4
## 一句话问题
3DGS 训练后的高斯点云**过密**,如何在**不重新训练**的前提下,通过后处理 pipeline 把它压到 1/15 + 200+ FPS?

## 链接(均经 fetch + GitHub README 实测)
- arxiv: <https://arxiv.org/abs/2311.17245>(v1 2023-11-29)
- 项目页: <https://lightgaussian.github.io/>
- GitHub: <https://github.com/VITA-Group/LightGaussian>(README 实测)
- PDF:**未下**(budget 限制)—— abstract 直引

## 年份 / 作者 / 机构(arxiv metadata + GitHub README 实测)
- **年份**:2024(NeurIPS 2024 **Spotlight**)
- **第一作者**:Zhiwen Fan(范志文,UT Austin)
- **完整作者列表**:Zhiwen Fan, Kevin Wang, Kairun Wen, Zehao Zhu, Dejia Xu, Zhangyang Wang
- **机构**:**UT Austin**(University of Texas at Austin,VITA-Group)
- **会议 / 出版**:**NeurIPS 2024 Spotlight**(GitHub README 标签直引)

## 方法核心(abstract 直引)
1. **Pruning + 恢复 pipeline**:基于 **"global significance score"** 剪掉对画面质量贡献较小的高斯点 → **剪枝后用真实图像监督微调剩余高斯点**(fine-tune 进一步减少剪枝对画面质量影响)
2. **SH 蒸馏(Spherical Harmonics Distillation)**:用知识蒸馏 + 伪视图增强,简化 SH 系数 → 进一步减少数据量
3. **Gaussian VQ(Vector Quantization)**:对剪枝 + SH 蒸馏后的高斯点做矢量量化与编码 → **达到高效存储与传输**
4. **后处理,不改训练**:**不需要重新训练** —— 任何已训练好的 3DGS 都可以走这条 pipeline

## 关键数字(abstract 直引)
- **3DGS 模型大小**:**15× 压缩**(abstract 直引:"15x reduction")
- **渲染速度**:**200+ FPS** @ RTX 3090(abstract 直引:"200+ FPS")
- **适用场景**:**unbounded 3D Gaussian**(针对大规模户外 / 城市级场景)
- **数据集**:abstract 直引 **"unbounded 3D Gaussian"** —— 应是 Mip-NeRF 360 / Waymo Open Dataset 类;**具体数据集未在 abstract 列出**;`abstract 未给`
- **PSNR / SSIM / LPIPS 损失**:**abstract 未给具体数值**;**GitHub README 描述"minimal quality loss"**,`abstract 未给 Table 1 数字`
- **训练 GPU / 时长**:`abstract 未给`
- **推理 GPU 显存**:`abstract 未给`

### 3DGS 压缩前后对比(abstract 直引)
| 指标 | Vanilla 3DGS | LightGaussian | 收益 |
|---|---|---|---|
| Storage | X | X / 15 | **15× 压缩** |
| FPS | 30~50 (unbounded) | 200+ | **4~6× 加速** |
| Quality(PSNR)| baseline | "minimal loss" | `abstract 未给精确数字` |

> **核心断言**:**不重新训练 + 15× 压缩 + 200+ FPS** —— 对项目 M4(bitpack 路线)的**后处理 pipeline 直接借鉴**。

## 与本调研主线的关系

### 1. 主线对标(静态 3DGS 后处理压缩,**与 MEGA 训练时压缩路线互补**)
- LightGaussian = **静态 3DGS 训练后 prune + VQ** 路线
- MEGA = **4DGS 训练时 SH→DC+AC + entropy** 路线
- **两者思路不同但可叠加**:
  - **MEGA** 在训练时减少每 splat 字节数(per-splat 3 参 DC + shared MLP)
  - **LightGaussian** 在训练后减少 splat 数量(pruning) + 进一步 VQ
- **本项目 M4 应同时引入两者**:
  - **MEGA** 思路:训练时改 SH 编码
  - **LightGaussian** 思路:训练后做 prune + VQ

### 2. 借鉴价值
- **"global significance score" 剪枝**对 mobile 端是**降低 #Gauss 的有效手段** —— **#Gauss 减少 = 移动端 rasterization 加速** 直接对应
- **SH 蒸馏**对 mobile 端 SH 系数(48 个 float = 192 bytes)压缩有借鉴 → 可减到 1/4
- **Gaussian VQ**对 mobile 端存储 / 传输(从云端到手机)至关重要 → **典型 64-bit codebook lookup**
- **后处理不重新训练** = **可以离线** = **移动端不需要在设备上做训练** → 完美匹配本项目架构

### 3. 不可作为移动端最终方案
- **静态 3DGS 范式**,**不直接处理 4D 动态**;`未在公开材料找到` 4D 动态版本
- **200+ FPS @ unbounded 场景** 是 RTX 3090 上,**Adreno 8 Gen 4 上仍可能不达 30 FPS @ 1080p**(`推测` 实测未在 abstract 给)
- **PyTorch + CUDA 实现**:`未在公开材料找到` mobile / Vulkan 版本

### 4. 对采集端反推
- **unbounded 场景** = 城市 / 街道 / 大型户外 → **本项目"高速相机阵列预制高密度场景"的同场景假设**
- **适合大规模稀疏场景**,**不适合小物体高细节**(Mobile/AR 类)

## 我未找到 / 提请下游注意
- **PSNR / SSIM / LPIPS 精确数字**:`abstract 未给`;**PDF 全文未下**
- **#Gauss 剪枝前 / 剪枝后比例**:`abstract 未给`
- **训练 GPU / 时长 / 显存**:`abstract 未给`
- **数据集精确列表**:`abstract 未给`
- **4D 动态版本**:`未在公开材料找到`
- **移动端 / Vulkan 实现**:`未在公开材料找到`
- **PDF 全文**:本笔记**未下**

## 我的 commit 节奏
- 本文为 5 篇新工作笔记之 4。
- 下游 `02-rendering-acceleration.md` §3(bitpack 段)应同时引用本文(LightGaussian,后处理)+ `2024-zhang-mega-4dgs-acceleration.md`(MEGA,训练时),**作为 M4 bitpack pipeline 的双源参考**。

## 引用一览
- <https://arxiv.org/abs/2311.17245>(abstract 实测)
- <https://github.com/VITA-Group/LightGaussian>(README 实测)
- <https://lightgaussian.github.io/>(项目页)
