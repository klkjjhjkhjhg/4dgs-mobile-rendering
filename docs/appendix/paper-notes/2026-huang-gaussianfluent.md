# 2026-huang-gaussianfluent · GaussianFluent: Gaussian Simulation for Dynamic Scenes with Mixed Materials

> **相关性**：**⭐⭐ 派系 A 4DGS 表示 + 派系 B 动静态分离（边界）** —— CVPR 2026 Oral (arxiv:2601.09265)；核心：**3DGS + 物理模拟（弹性 + 脆性断裂 + 切片）+ 混合材质**（abstract 直引）。**北大 + BIGAI**（Beijing Institute for General AI）。**对 4DGS Mobile 加速**: 物理模拟与 4DGS 时序预测思路有交叉，**但本项目主线不直接是物理模拟**。

> **⚠ 重要区分**：这是 **3DGS + 物理仿真** 跨领域工作，**不是 4DGS 加速**。**对 4DGS 适用性**: GaussianFluent 用 MPM 做物理模拟，**4DGS-CC 的神经上下文编码思路可以做"几何-物理"混合 representation**（`[推测]`）。**对本项目 4DGS Mobile 路线间接价值**。

## 一句话问题

3DGS **没有内部纹理**（仅表面），**没有 fracture-aware simulation**——所以**不能做脆性断裂 / 切片 / 内部结构变化**。**如何用 3DGS 表示 + 物理模拟生成真实的多材质动态场景**？

## 链接

- arxiv：<https://arxiv.org/abs/2601.09265>（v1 2026-01-14）
- 项目页：<https://hb-pencil-zero.github.io/GaussianFluent/>
- GitHub：not found in abstract
- PDF：已下 `.pdfs/2601.09265.pdf`（16 页，14.8 MB）
- 会议：**CVPR 2026 Oral**（`ooonesevennn/CVPR_2026_Oral_Papers` 直引，url=`https://cvpr.thecvf.com/virtual/2026/oral/40287`）

## 年份 / 作者 / 机构（PDF 头部实测）

- **年份**：2026（v1 2026-01-14）
- **第一作者**：**Bei Huang**（黄蓓）— 北大 + BIGAI 共培
- **通讯作者**：Yixin Chen（陈奕欣，BIGAI）/ Siyuan Huang（黄思远，BIGAI）
- **机构**（PDF 头部直引）：
  1. **State Key Laboratory of General Artificial Intelligence, Peking University**（北大通用人工智能国家重点实验室）
  2. **State Key Laboratory of General Artificial Intelligence, BIGAI**（北京通用人工智能研究院）

> **北大 + BIGAI 双背书** —— BIGAI 是朱松纯 2020 年牵头成立的通用 AI 研究院，**国家级 AI 实验室**

## 方法核心（PDF §1 abstract + Fig.1 直引）

### §1 问题诊断：3DGS 物理模拟 2 大盲点

1. **3DGS 没有 volumetric interior** —— 标准 3DGS Gaussian 在物体**表面**，**没有内部纹理**（jelly / 糖 / 软糖等需要内部）
2. **没有 fracture-aware simulation method** —— 现有 3DGS 物理模拟主要针对**软体 deformable** 材料（布料、果冻），**脆性断裂（fracture）= 开放问题**

### §3 GaussianFluent 解法

1. **Densifying internal Gaussians guided by generative models** —— 用生成模型（diffusion）给 3DGS 物体"填满"内部 Gaussian，模拟内部纹理（jelly 内部蓝色糖）
2. **CD-MPM (Continuum Damage Material Point Method)** —— 优化版的 MPM 用于**脆性断裂** simulation
3. **Mixed-material 支持** —— 同一物体不同部分用不同物理参数（jelly + sugar + rigid bullet）
4. **Multi-stage fracture propagation** —— 子弹穿透 → 裂纹扩展 → 碎片飞散

## 关键数字 / 能力（abstract 直引）

| 能力 | 描述 |
|---|---|
| **物理现象** | "elastic deformation, fracture, and slicing"（abstract 直引） |
| **混合材质** | "mixed materials (e.g., jelly with internal blue sugar penetrated by a rigid bullet in top row)"（Fig.1 直引） |
| **渲染真实感** | "photorealistic interiors by densifying internal Gaussians"（abstract 直引） |
| **模拟速度** | "brittle fracture simulation at remarkably high speed"（abstract 直引） — **未给具体 FPS 数字** |
| **场景复杂度** | "complex scenarios including mixed-material objects and multi-stage fracture propagation"（abstract 直引） |
| **质量** | "achieving results infeasible with previous" methods（abstract 直引） |

> **没看到具体 FPS / PSNR 数字**（`[未在 abstract 拿到]`）—— PDF §4 experiments 应有

## 与本调研主线的关系

### 派系归属：**派系 A 4DGS 表示**（间接），**派系 B 动静态分离**（弱）

- **派系 A 弱相关**：GaussianFluent 是 3DGS + 物理，**不是 4DGS**。但 **MPM 物理模拟 + 3DGS 渲染** 的组合对 4DGS 动态预测有方法学价值
- **派系 B 弱相关**：dynamic 4DGS = 物体运动 + 形变。GaussianFluent 给"形变"提供工具，**4DGS-1K 的 STV pruning 给"运动"提供工具**

### 对项目目标的具体承诺

- **4DGS Mobile 路线价值有限**：本项目 4DGS 主线关注**实时流式渲染**（4DGCPro / GS-NFS 路线），不是**物理模拟** —— GaussianFluent 的 MPM + 物理 simulation **与本项目 M3/M4/M5 spike 阶段无直接交点**
- **间接价值**：**MPM 的 multi-stage fracture pipeline** 给 4DGS 动态场景的"形变"子问题提供方法学参考

### 我未找到 / 提请下游注意

- **GaussianFluent 的训练时间 / 推理 FPS**：abstract 只说"high speed"，**未给具体数字**——本项目不关心，但需注意
- **GaussianFluent 与 4DGS 表示的兼容性**：MPM 物理模拟通常在**静态 representation** 上跑，**4DGS 加 MPM = 计算量爆炸**（`[推测]`）—— **本项目不要走这条路**
- **GaussianFluent 的开源代码**：PDF 未给 GitHub 链接，**需要追踪**

## 我的 commit 节奏

本文是原 47 篇 paper notes 之外**新加的第 49 篇**。配套 INDEX.md 派系 A（4DGS 表示）加 1 行（边界条目）。
