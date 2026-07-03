# 调研目标(完整版)

> 本文件是**调研目标 spec**,由主对话 session 写入。后续调研 subagent 在执行时,以此为目标。
> 原文在 Telegram 聊天(用户发出来的简化版)和本仓库外文件,但**核心约束与"必须覆盖"的项**全部在这里,避免任何 subagent / 子任务对任务范围产生二义性。

## 背景 / 任务定位
本研究服务于一个项目:在 Android 高通旗舰芯片上实现 **4DGS(动态 3D Gaussian Splatting)的实时渲染**。
场景 4DGS 资源可以 **离线预制**(采集端允许高成本),但渲染端必须跑在移动端 GPU。
核心难点分两块:

- 如何得到一个场景的 **高精度 4DGS 表示**(离线采集 + 训练)
- 如何对 4DGS 进行 **渲染加速**(移动端 GPU,实时)

## 关键约束(硬参数)

| 维度 | 约束 |
|---|---|
| 目标平台 | 高通旗舰(Snapdragon 8 Gen 3/4,Adreno 750/830) |
| 上限 splats | ~300 万 / 场景 |
| 输出分辨率 | 全屏 1080p,允许内部降采样 + 上采样(FSR/TAA-upsample) |
| API | Vulkan 1.3,优先使用 compute shader |
| GPU 架构 | Tile-based(Adreno),tile memory 与 on-tile compute |
| 场景动态性 | 动态 4DGS,需能表达运动物体或相机运动(不限定具体动态类型) |
| 采集方案 | 多视角高速相机阵列 + 高精度 SfM |
| 训练预算 | 几小时 ~ 几天 / 场景(允许重训练) |
| 对标方法 | **4DGS-1K-lite**(4DGS-1K 的加速衍生版,稀疏 mask + bitpack 路线) |

## 第一块调研:高精度 4DGS 表示(离线端)

### 必须覆盖

- **从相机阵列到 4DGS 的完整管线**:采集 → SfM → 时间维度建模 → 训练 → 导出。每个环节给出方法选型
  - **采集**:视角数量、相机帧率、重叠率、标定方案;同步方案(硬件/软件触发)
  - **SfM / 重建**:COLMAP / OpenMVS / InstantSplat / DUSt3R 等
  - **时间维度建模**:per-frame 3DGS 序列、时间条件 Gaussian、canonical + deformation 模式
  - **训练范式**:自监督光度损失、感知损失、正则化项
- **对标主线**(必查并对比):
  - **4DGS 原论文**(Wu et al., CVPR 2024)及其后继
  - **4DGS-1K / 4DGS-1K-lite**:在原 4DGS 基础上的加速表示
  - **Dynamic 3DGS**(Yang et al.),**Deformable 3DGS**,**4D-GS** 等其他动态 3DGS 变体
  - **Hyperreel / 4D Gaussian Splatting for Real-time Dynamic Scene Rendering**
- **精度指标**:PSNR / SSIM / LPIPS、动态区域专门指标(warping error)
- **对采集端的反推**:要达到当前 SOTA 精度,采集需要多少相机、多少帧、花多长时间;给出可操作的"采集设备清单 + 拍摄 SOP"草案

### 输出要求

1. **一条主线推荐方案 + 两条备选**,各列优缺点
2. **采集 → 训练 → 导出 4DGS 资源** 的端到端步骤图(可用 ASCII / Mermaid)
3. 训练一次场景的 **算力 / 时间预算** 估算(GPU 型号 + 显存占用)
4. **资源体积估算**:per-splat 字段(位置/旋转/scale/sh/DC/feature/时间参数),导出后的最终磁盘体积

## 第二块调研:渲染加速(Vulkan 1.3,移动端)

### 必须覆盖(按优先级)

1. **稀疏化与剪枝**(决定 300 万 splats 上限能不能进一步压)
   - 不重要 mask / invisible mask / 视角无关贡献 mask
   - **重要度评分方法**(基于渲染误差梯度、jacobian、opacity)
2. **比特压缩**(bitpack)
   - 32→16/8 bit 的精度/性能 trade-off
   - 量化方案:线性 / K-means / 学习型量化
   - 当前 SOTA 的 bit 宽度(per-field)、解压代价
3. **Tile-based GPU 优化**(Adreno 特别重要)
   - Frustum culling + 2D 投影 splat 剔除
   - On-tile sorting vs host-side sorting(PowerVR/Adreno 历来推荐 on-tile)
   - 显存布局:SoA vs AoS,wave size 对齐(Adreno 通常 64/128)
   - **Compute shader 预处理**(在 bin/sort 阶段)+ fragment shader 光栅化 的分工
4. **时空复用**(专属于 4DGS 的加速机会,**4DGS-1K-lite 的核心**)
   - **Temporal mask**:相邻帧可见性 / 重要性基本一致,只增量更新
   - Frame coherence:复用上一帧的 sort 结果 + 仅处理 ROI 变化区域
   - 4DGS-1K-lite 的具体 mask 设计(稀疏锚点还是 ROI mask)、bitpack 选型、串扰抑制手段
5. **上采样到 1080p**
   - AMD FSR 1/2(开源,可商用)/ Vulkan 内置 FSR2 / 自研 TAA-Upsample
   - 内部渲染分辨率建议:540p / 720p / 900p 三档对比的 perf-quality 曲线

### 对标主线(必须深读)

- **4DGS-1K-lite 原论文 / 仓库**(主线)
- **3DGS 加速系列**:**LightGS**、**Scaffold-GS**、**Mip-Splatting**、**GauHuman**、**EfficientGS / CompGS / 4DGS-1K 系列** 的稀疏化技巧
- **移动端 / 端侧 3DGS 工作**:**Mobile 3DGS / Edge 3DGS / Qualcomm AI Hub / Adreno GPU 上的 3DGS demo**
- **Vulkan + Compute 相关的 GPU 加速范式**:gpuopen / Adreno SDK 文档 / FastGS / Meshlet culling 思路可类比

### 输出要求

1. **加速技术树**:从原始 4DGS 出发,经过哪些步骤压缩到 30~60 FPS @ 1080p on Snapdragon 8 Gen 4
2. **每一步加速的预期收益**:压缩比、加速比、可能的质量损失(基于公开数据 / 类似方法外推)
3. **Vulkan 1.3 实现细节草案**:compute vs fragment 分工 / 显存布局 / 与 4DGS-1K-lite 对标
4. **当前公开 SOTA 的 mobile 4DGS FPS 数字**:作为 baseline
5. **风险与未知**:≥5 项

## 整体产出要求

- **一份调研文档**(可中文,关键结论要密集),结构:
  - README + 01-high-precision-representation + 02-rendering-acceleration + 03-end-to-end-roadmap + appendix(paper-notes / collection-sop / vulkan-impl-notes) + references + experiments + assets
- **每条结论必须可追溯**:能标"基于 X 论文"或"基于 X 仓库实现细节"的都标;推测性结论显式标"推测"
- **数据不足处**明确说"调研不足,需进一步实验";**不要为了完整性瞎编数字**

## 调研过程管理

- **本地仓库**:`~/Codes/4dgs-mobile-rendering`(本仓库)
- **远端 GitHub**:`klkjjhjkhjhg/4dgs-mobile-rendering`,private
- **commit 节奏**:读完一篇论文 / 跑通一个实验 / 阶段性结论 → 立即 commit
- **push 节奏**:本地第一个 commit 后,等 GitHub auth 完成后立刻建空远端 + push;之后每完成一个主要章节 push 一次;调研结束前最后一次大整理 + push
- **遇远端连接问题**:立即反馈,不憋着
- **不写**:真名 / 个人邮箱 / 临时日志 / 私有 key / 个人 token

## 后续 subagent 启动入口

待 GitHub auth 就绪后,由主对话 session 派 D1 leaf subagent 执行本调研。subagent 将:
1. 在本仓库继续 commit(论文笔记、实验脚本、阶段性调研章节)
2. 每完成一个章节节点,推送到远端
3. 调研结束后产出 `docs/03-end-to-end-roadmap.md` + 执行摘要 + 完整参考文献
