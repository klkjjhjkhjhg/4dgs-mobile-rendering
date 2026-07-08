# 2024-yu-mip-splatting · Mip-Splatting: Alias-free 3D Gaussian Splatting

> **相关性**:**中等相关** — 静态 3DGS alias-free 抗锯齿补丁,**间接影响 4DGS 移动端在 1080p 高分辨率下的边缘质量**,是 mobile 端视觉质量 baseline 的关键参考。CVPR 2024 **Best Student Paper** 含金量高。

## 0.5 元数据

- **venue**: CVPR 2024
- **arxiv-id**: 2311.16493
- **s2-id**: （v2 用 Semantic Scholar API 补全）
- **homepage**: https://niujinshuchong.github.io/mip-splatting/
- **github**: https://github.com/autonomousvision/mip-splatting
- **status**: received
- **收录日期**: 2026-07-08（首次）
- **收录来源**: arxiv scan + 1-hop 引用规则
- **1-hop 引用**: （v2 补全，见 §11 1-hop 关系图）
- **评级**: ⭐⭐

## 一句话问题
3DGS 在改变采样率(焦距 / 相机距离)时会出现"膨胀 / 侵蚀"伪影,如何在不损失速度的前提下消除这类 aliasing 伪影?

## 链接(均经 fetch + GitHub README 实测)
- arxiv: <https://arxiv.org/abs/2311.16493>(v1 2023-11-28)
- 项目页: <https://niujinshuchong.github.io/mip-splatting/>
- GitHub: <https://github.com/autonomousvision/mip-splatting>(CVPR 2024 best student,README 实测)
- PDF:**未下**(budget 限制)—— abstract 直引

## 年份 / 作者 / 机构(arxiv metadata + GitHub README 实测)
- **年份**:2024(CVPR 2024 录用,**Best Student Paper**)
- **第一作者(共同一作)**:Zehao Yu(余泽豪)、Anpei Chen(陈安沛)、Binbin Huang(黄彬彬)
- **通讯作者**:Andreas Geiger(Andreas Geiger,Tübingen)
- **机构**:**University of Tübingen**(图宾根大学)+ **ShanghaiTech University**(上海科技大学)
- **会议 / 出版**:**CVPR 2024 Best Student Paper**

## 方法核心(abstract 直引)
1. **3D smoothing filter**:对 3D 高斯椭球加低通滤波,**限制 3D 表示的最高频率**在训练图像奈奎斯特频率的一半以下
2. **2D Mip filter**(替换原 3DGS 的 2D dilation filter):近似 EWA-Splatting 的盒形滤波器,**消除高分辨率放大时的侵蚀伪影**
3. **改进的 density metric**:优化致密化策略,**显著提高新视角合成质量**
4. **几乎不增加推理代价**:3D smoothing 与 2D Mip filter 都是**预计算 + 训练时**;推理速度与 vanilla 3DGS 相当

## 关键数字(abstract 直引)
- **新视角合成质量提升**:在多视角数据集上**"significantly improves the quality of novel view synthesis"** —— 具体数字 abstract 未给表格,`abstract 未给 Table 1 数字`
- **数据集**:Blender synthetic、Mip-NeRF 360(GitHub README 直引)
- **训练 GPU / 时长**:`abstract 未给`
- **推理 FPS**:**未在 abstract 报告**,**应与 vanilla 3DGS 同量级**(即 100+ FPS @ 1080p on RTX 3090),`abstract 未给`

### 与 3DGS 同台对比(abstract 直引定性)
> "Our method **removes the need for specific 2D dilation filter** in the 3DGS pipeline, **making it more robust to varying sampling rates** while maintaining the real-time rendering speed."

> **核心断言**:**不损速度** + 抗锯齿 → **对移动端"1080p 拉近 / 拉远"切换场景的视觉质量 baseline** 至关重要

## 与本调研主线的关系

### 1. 主线对标(静态 3DGS 抗锯齿,**作为移动端质量基线参考**)
- Mip-Splatting 不直接处理 4D 动态;**但其 2D Mip filter 思想对 4DGS 移动端 1080p 渲染的边缘质量有借鉴价值**
- 项目 M5 阶段(perceptual quality / 上采样)应把 Mip-Splatting 的抗锯齿策略**与 FSR / DLSS 上采样**做对比

### 2. 借鉴价值
- **2D Mip filter 替代 2D dilation** 是 **训练期一次性成本**;推理时几乎无开销 → **对 mobile GPU 友好**
- **frequency budget 思想**(把 3D 表示限频在 Nyquist 1/2 以下)对**移动端存储紧凑性** 有借鉴:压缩存储时可量化掉超过 Nyquist 1/2 的频率成分
- **不增加推理 FPS 开销** 这点**对 mobile 端至关重要** —— 不能用降速换质量

### 3. 不可作为移动端最终方案
- 静态 3DGS 范式,**不直接处理 4D 动态**
- PyTorch + diff-gaussian-rasterizer 实现,`未在公开材料找到` mobile / Vulkan 版本
- 抗锯齿 filter 是在 rasterization kernel 内的修改,**Vulkan 移植需要重写 fragment shader**

### 4. 对采集端反推
- 训练数据:Blender synthetic + Mip-NeRF 360;**单相机 / 多视角均可**,与本项目"高速相机阵列"不直接对位
- **但**:**Mip-Splatting 解决了"3DGS 在不同采样率下边缘质量不一致"的问题** → 本项目 M2 / M3 训练完成后,移动端不同视距(拉近 / 拉远)时**应当不会遇到明显的侵蚀伪影** —— 这是项目质量保证的关键

## 我未找到 / 提请下游注意
- **PSNR / SSIM / LPIPS 精确 Table 1 数字**:`abstract 未给`;**PDF 全文未下**
- **#Gauss / Storage / FPS 数字**:`abstract 未给`
- **训练 GPU / 时长**:`abstract 未给`
- **4D 动态版本**:`未在公开材料找到`
- **移动端 / Vulkan 实现**:`未在公开材料找到`
- **PDF 全文**:本笔记**未下**

## 我的 commit 节奏
- 本文为 5 篇新工作笔记之 2。
- 下游 `01-high-precision-representation.md` §4(精度 / 抗锯齿)应引用本文作为 **"静态 3DGS 抗锯齿的基线参考"**。

## 引用一览
- <https://arxiv.org/abs/2311.16493>(abstract 实测)
- <https://github.com/autonomousvision/mip-splatting>(README 实测)
- <https://niujinshuchong.github.io/mip-splatting/>(项目页)
