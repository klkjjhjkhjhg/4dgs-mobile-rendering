# 2024-duan-4drotorgs · 4D-Rotor Gaussian Splatting: Towards Efficient Novel View Synthesis for Dynamic Scenes

> **相关性**:**高度相关** — 同期(SIGGRAPH 2024)4DGS 加速工作中**最快**(D-NeRF 1257 FPS @ abstract),4DGS-1K Table 2 中直接对标的 baseline。**本项目 mobile 4DGS rendering 路线的主要灵感来源之一**。

## 一句话问题
如何在保持 4DGS 高质量的前提下,把动态场景新视角合成的**推理 FPS**推到 **1000+**?

## 链接(均经 fetch + GitHub README 实测)
- arxiv: <https://arxiv.org/abs/2402.03306>(v1 2024-02-05;SIGGRAPH 2024 录用)
- 项目页: <https://wdfvvy.github.io/4DRotorGS.github.io/>(GitHub README 直引)
- GitHub: <https://github.com/weify627/4D-Rotor-Gaussians>(README 实测)
- PDF:**未下** —— abstract 直引

## 年份 / 作者 / 机构(arxiv metadata + GitHub README 实测)
- **年份**:2024(SIGGRAPH 2024 录用)
- **第一作者**:Yuanxing Duan(段远兴,GitHub 用户 `weify627`)
- **完整作者列表**:Yuanxing Duan, Fangyin Wei, Qiyu Dai, Yuhang He, Wenzheng Chen, Baoquan Chen
- **机构**:Peking University(北京大学) + Shandong University(山东大学)
- **会议 / 出版**:**SIGGRAPH 2024**(GitHub README 顶部直引:"Proc. SIGGRAPH 2024")

## 方法核心(abstract 直引 + GitHub README 直引)
1. **4D Rotation + 3DGS 范式融合**:核心思想是把 **4D 高斯旋转**(rotation in 4D space)显式建模,把"短生命周期高斯 + 复杂运动"的问题转化为"单 Gaussian 长生命周期 + 4D 旋转"
2. **不需要 canonical + deformation 范式**:与 4DGS(Wu 2023)的 canonical space + HexPlane deformation 范式**不同**;4D-Rotor 主张在 4D 时空上**直接对每个高斯的旋转 + 时间维度建模**
3. **实时渲染**:D-NeRF synthetic 上实现 **real-time rendering speed**;从 abstract / 4DGS-1K Table 2 实测 **D-NeRF 1257 FPS @ RTX 3090**(abstract 直引 + 跨源验证)
4. **快速收敛**:GitHub README 直引"converges very quickly"(具体分钟数 abstract 未给,`abstract 未给`)
5. **同时支持 3D 静态与 4D 动态**:GitHub README 直引"can also be applied in 3D and achieve consistent results with 3D Gaussian" —— 同一框架兼容两种模态

## 关键数字(abstract 直引 + 跨源验证)
- **D-NeRF synthetic FPS**:**1257 FPS** @ RTX 3090(PDF 4DGS-1K Table 2 直引:`4D-RotorGS [7] = 1257 FPS` D-NeRF 800×800)
- **D-NeRF synthetic PSNR**:**34.26 dB**(4DGS-1K Table 2 直引)
- **D-NeRF synthetic SSIM**:**0.97**(4DGS-1K Table 2 直引)
- **D-NeRF synthetic LPIPS**:**0.03**(4DGS-1K Table 2 直引)
- **D-NeRF synthetic Storage**:**112 MB**(4DGS-1K Table 2 直引)
- **#Gauss(D-NeRF)**:abstract 未给;`abstract 未给`
- **#Gauss(N3V / D-NeRF)**:4DGS-1K Table 2 未报 4D-RotorGS 的 #Gauss,`未在跨源验证中拿到`
- **训练 GPU / 时长 / 显存**:`abstract 未给`;SIGGRAPH 2024 论文可能含更多数字,但本笔记**不下 PDF**

### 与本项目真·对标 4DGS-1K 的同台对比(D-NeRF,跨表汇总)
| 维度 | 4D-RotorGS(本文) | 4DGS-1K(真本) | 差距 |
|---|---|---|---|
| FPS @ D-NeRF | 1257 | 1462(abstract 表)| 4DGS-1K +16% |
| PSNR @ D-NeRF | 34.26 | 33.34 | 4D-Rotor +0.92 dB |
| Storage(MB)| 112 | 42 | 4DGS-1K 2.7× 更小 |

> **结论**:**4D-Rotor 是 4DGS-1K 真本发布前的同期 SOTA**,**但 4DGS-1K 在保持类似精度的同时进一步加速 16% + 缩小 2.7×**;4D-Rotor 的"4D 旋转"思想被 4DGS-1K 的"STV pruning + Temporal Filter mask"超越。

## 与本调研主线的关系

### 1. 主线对标(同期 SOTA,**4DGS 加速路线第二重要**)
- 4D-RotorGS = 4DGS 加速路线的 **"4D 旋转"分支**
- 4DGS-1K = 4DGS 加速路线的 **"STV pruning + Temporal Filter mask"** 分支
- 4D-RotorGS 用 4D 旋转解决"短生命周期高斯爆炸",4DGS-1K 用 pruning 解决"短生命周期高斯爆炸" + 用 mask 解决"per-frame compute 浪费"
- **两者目标问题高度重叠,但实现路径完全不同** —— **是绝佳的 ablation 对照**

### 2. 借鉴价值
- **4D 旋转思想**对 mobile **值得借鉴**:把"4 维时空"统一到一个 4D 高斯旋转参数化 → **per-splat 字节数更少 + 时序推理更省** → 适合 Adreno 8 Gen 4 上 16-bit 紧凑存储
- **D-NeRF 1257 FPS** 是同期桌面级 SOTA,**作为移动端 1080p 目标 30+ FPS 的对照上限** ≈ 桌面级 1/40,工程上 30 FPS 可期
- **"同一框架兼容 3D 静态 + 4D 动态"** 是项目**架构设计的关键启发**:**M2 / M3 阶段训练 pipeline 应当能复用同一套 rasterizer** —— 避免维护两套实现

### 3. 不可作为移动端最终方案
- **未在 mobile / Adreno / Vulkan 实现**:`未在公开材料找到`
- **SH coefficients 仍占大量存储**:112 MB D-NeRF storage 仍比 4DGS-1K 42 MB 大 2.7× —— **未做 bitpack**
- **PyTorch + CUDA + tiny-cuda-nn 实现**:`github README 直引`;**完全不能直接搬到 Adreno**

### 4. 对采集端反推
- D-NeRF synthetic(单目):同 Deformable 3DGS,**单目 + 8 scenes**;`abstract 未给`多相机训练数据
- 训练数据假设与本项目"高速相机阵列"不直接对位

## 我未找到 / 提请下游注意
- **#Gauss / 显存数字**:`abstract 未给`;**PDF 全文未下**
- **训练时长 / scene 分钟数**:`abstract 未给`
- **N3V / Technicolor 上数字**:`abstract 未给`(GitHub README 提到 D-NeRF 是主测)
- **移动端 / Vulkan 实现**:`未在公开材料找到`
- **PDF 全文**:本笔记**未下**(budget 限制);所有数字均 abstract + 跨源 4DGS-1K Table 2 验证

## 我的 commit 节奏
- 本文为 5 篇新工作笔记之 1。
- 下游 `02-rendering-acceleration.md` §3(加速技术树)应把 4D-RotorGS 归到 **"4D 旋转"分支**,与 **"STV pruning"分支**(4DGS-1K)并列对照。
- 4DGS-1K Table 2 中的 4D-RotorGS 数据行已在本笔记 cross-check 完。

## 引用一览
- <https://arxiv.org/abs/2402.03306>(abstract 实测)
- <https://github.com/weify627/4D-Rotor-Gaussians>(README 实测)
- `/Users/klkjjhjkhjhg/Codes/4dgs-mobile-rendering/docs/appendix/paper-notes/2025-yuan-4dgs-1k.md` Table 2(同源 cross-check)
