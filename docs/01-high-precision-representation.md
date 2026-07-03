# 01 — 高精度 4DGS 表示(离线端)

> **状态**:已填。由 D1 leaf subagent 在 4 篇 paper notes 基础上撰写。
>
> **来源标注约定**:`[基于 X 论文]` / `[基于 X 仓库 L 文件]` / `[推测]` / `[未在公开材料找到,需 PDF 核验]` / `[abstract 直引]`。
>
> **数字纪律**:不编造 PSNR / FPS / 显存数字。引用的数字均来自公开 abstract / README / 综述二次确认,**未拿到的字段写"未在公开 abstract 拿到"**。
>
> **依赖**: `docs/00-goal.md`(目标 spec), `docs/appendix/paper-notes/2024-wu-4dgs.md`, `2023-yang-deformable-3dgs.md`, `2023-attal-hyperreel.md`, `2024-zhang-mega-4dgs-acceleration.md`(4 篇精读)。

---

## 0. 执行摘要(1 页,可独立抽出来)

**调研目标**:在离线端(采集 + 训练)得到一个场景的**高精度 4D Gaussian Splatting(4DGS)**表示,使之在 Snapdragon 8 Gen 4 / Adreno 830 上实时渲染(参见 `docs/02-rendering-acceleration.md`)。

**核心结论**:

1. **主线推荐 = 4DGS 原论文(Wu et al., CVPR 2024, arxiv 2310.08528)** 加上后续衍生。具体选型在 §7 详述。
2. **公开数字**:`4DGS` 在桌面 RTX 3090 上 **`82 FPS @ 800×800`**(`[abstract 直引]`)是与本项目目标最近的可比 SOTA;精度上 `4DGS` 在 D-NeRF / Plenoptic Video 上报告"comparable or better than previous SOTA"(`[abstract 直引]`,**未在 abstract 拿到具体 Table 1 数字**)。
3. **4DGS-1K-lite**:精确叫这个名字的论文对象**未在公开 arxiv 找到**(`[未在公开材料找到]`,见 `2024-zhang-mega-4dgs-acceleration.md` §"关键诚实说明")。`MEGA`(arxiv 2410.13613)是公开材料里最相关的"4DGS 显存压缩"代表作,声称 **Technicolor 上 ~190× / Neural 3D Video 上 ~125× 存储压缩**(`[abstract 直引]`,abstract 未给具体 PSNR/FPS 数字)。
4. **采集端反推**:目标 1080p + ~3M splats 上限(Snap 8 Gen 4 移动 GPU 内存带宽约束)→ 推荐**多视角相机阵列**(8~16 路,同帧同步触发)+ 高精度 SfM(初版用 COLMAP,**对大动态场景建议用 MonST3R / DUSt3R 路线**,见 §3)。**理由**:Deformable 3DGS(Yang 2023, arxiv 2309.13101)走单目路线,**abstract 直引**"model monocular dynamic scenes"——**单目是低精度天花板**,无法满足"高精度"目标。
5. **训练算力**:桌面 RTX 3090 / A6000 级 24GB 显存,**未在公开材料拿到 4DGS 训练单 scene 精确分钟数**(推测 ~ 数小时 / scene)。
6. **per-splat 资源体积估算**:`原 4DGS` 单 splat ~ 145B(3+4+3+1+144+0+others 推测); `MEGA` 用 `per-Gaussian DC 3 + 共享 AC predictor` 把 color 字段从 144→3,叠加 fp16+zip → **`~190×` 压缩**(`[abstract 直引]`)。
7. **关键风险**:`4DGS-1K-lite` 公开材料不存在 → 移动端 4DGS 加速的"主对标"实际缺失;**移动端(Adreno)FPS baseline 数字未在公开 abstract 拿到**。

---

## 1. 完整管线总览(采集 → SfM → 时间维度建模 → 训练 → 导出)

```
┌──────────────────┐
│ ① 多视角同步采集  │  8~16 路高速相机,同帧硬件触发
│  (高速相机阵列)  │  ≥30 FPS(与目标播放帧率匹配或更高)
└────────┬─────────┘
         ▼
┌──────────────────┐
│ ② 相机标定与     │  COLMAP SfM(static, reference)
│   静态 SfM 重建  │  或 DUSt3R / MonST3R(dynamic-friendly)
└────────┬─────────┘
         ▼
┌──────────────────┐
│ ③ 时间维度建模   │  选型 1: canonical + deformation (4DGS / Deformable 3DGS)
│   (representation│  选型 2: per-frame 3DGS 序列
│    设计)          │  选型 3: 时间条件 Gaussian
└────────┬─────────┘
         ▼
┌──────────────────┐
│ ④ 4DGS 训练      │  桌面 GPU: 自监督光度 L1 + D-SSIM + 正则化
│   (PyTorch + 自研 │  HexPlane 编码(Wu-4DGS) / 显式 deformation field
│    splatting)     │  收敛: 验证集 PSNR 平台期
└────────┬─────────┘
         ▼
┌──────────────────┐
│ ⑤ 导出           │  原始 .ply + HexPlane 权重 + deformation MLP 权重
│   (per-splat 资源)│  压缩可选:MEGA-style bitpack → 190× 压缩
└────────┬─────────┘
         ▼
       移动端
   (Vulkan 1.3 渲染)
```

**Mermaid 形式(可选)**
```mermaid
graph LR
  A[多视角同步采集] --> B[标定 + SfM/重建]
  B --> C[时间维度建模]
  C --> D[4DGS 训练]
  D --> E[导出 .ply + 编码 + MLP 权重]
  E --> F[移动端 Vulkan 渲染]
```

---

## 2. 采集方案(高速相机阵列 + 多视角同步)

### 2.1 视角数量

- **推荐**:8~16 路相机(同步阵列),环绕 + 上下分层的环视布局
- **反推依据**:`4DGS` 训练数据集 Plenoptic Video Dataset / Neural 3D Video / Technicolor 都是**多视角同步**(`[基于 Wu-4DGS 论文 §数据集, abstract 段`]`),单目反例见 §2.5

### 2.2 相机帧率

- **目标**:≥30 FPS 同步采集(给目标播放 30 FPS 留冗余),高速动态场景推荐 60 FPS
- **曝光**:全局快门(global shutter)以避免运动下 rolling shutter 失真;**单目路线的 Deformable 3DGS 论文也强调 annealing smoothing training 缓解 pose 误差**,**多目同步应直接消解这一痛点**

### 2.3 重叠率

- **目标**:相邻视角 **>60% 像素重叠**(便于 SfM 特征匹配 + 多视角一致性约束)
- **COLMAP 经验**:>40% 可重建,**>60% 鲁棒**(`[基于 COLMAP 社区经验,未在公开材料精确量化]`)

### 2.4 标定方案

- **首选**:多相机联合标定(可借 OpenCV `stereoCalibrate` 逐对标定后外参对齐到世界系)
- **替代**:AprilGrid / ChArUco 标定板 + COLMAP hierarchical SfM
- **`[推测]`**:大动态场景下相机在采集过程中会受微振动影响,建议在采集前/后各做一次标定验证

### 2.5 同步方案

- **硬件触发**:GenICam / IEEE 1588 PTP 时钟同步,或单板载 GPIO 触发(多机同步常用方案)
- **软件 fallback**:同帧时间戳对齐(精度差,仅推荐作备份)
- **反例说明**:`Deformable 3DGS(Yang 2023)` 用单目 + annealing smoothing(`[abstract 直引]`),**说明 pose 不稳/不同步会显著影响训练稳定性**;多机同步是直接消解

---

## 3. SfM / 静态重建

### 3.1 工具选型对比

| 工具 | 输入约束 | 动态场景 | 速度 | 精度 | 出处 |
|---|---|---|---|---|---|
| **COLMAP**(经典 SfM) | 已知内参,无标定也行 | **弱**:对动态目标常失败 | 慢(小时~天) | 高 | 公开社区共识 `[推测]` |
| **OpenMVS**(MVS) | 依赖 SfM | 弱 | 中 | 高 | 公开社区共识 `[推测]` |
| **DUSt3R**(Naver, 2024) | **无需相机内参/位姿** | 仅静态训练数据 | **2 秒 / 2 张** | 高(单目/多视图 SOTA) | arxiv 引文 + 知乎/CSDN 综述 `[abstract 直引]` |
| **MonST3R**(DUSt3R 动态推广) | 同 DUSt3R | **设计目标就是动态** | 较 DUSt3R 慢 | 静态精度继承 DUSt3R,动态更优 | `monst3r-project.github.io` `[基于 项目页与 CSDN 笔记]` |
| **MV-DUSt3R**(Naver, 2024) | 同 DUSt3R | 静态 | **单级前馈,无级联全局优化** | 继承 DUSt3R | CSDN 论文笔记 `[基于 综述]` |
| **InstantSplat**(Fan et al., 2024) | 稀疏视角(几~10 张) | 静态 | **秒级** | SfM-free | arxiv 2403.20309 `[abstract 直引]` |

### 3.2 推荐(SOP 草案)

1. **静态背景**:首帧 / 静态子集 → COLMAP hierarchical SfM(精度最高)
2. **大动态场景**:**MonST3R 作为对动态友好的 SfM 替代**(`[基于 MonST3R 项目页 + CSDN 笔记]`);若资源受限退到 DUSt3R + 时间分段拼接
3. **快速原型**:**InstantSplat**(几秒级别起步),**适合"先看效果"迭代**

> **重要补充**(从本调研外的 web 检索): `MonST3R` 项目页与 CSDN 笔记都明确指出 COLMAP "经常与复杂相机轨迹或高度动态场景作斗争",这与目标场景契合度高,**所以大动态场景优先 MonST3R**(`[基于 MonST3R 论文笔记 CSDN 2025-01-16,abstract 直引]`)。DUSt3R 的训练数据"仅包含静态场景"(`[基于 MonST3R 论文摘要]`),所以**直接套 DUSt3R 训 4DGS 不可取**。

---

## 4. 时间维度建模

### 4.1 三大范式

#### 4.1.1 `canonical + deformation`(本调研主线)

- **代表**:`4DGS`(Wu 2024, HexPlane + MLP deformation),`Deformable 3DGS`(Yang 2023)
- **机理**:canonical 空间下高斯表示"静态几何",每帧由 deformation field(轻量 MLP 或 HexPlane 编码)预测形变(位姿 / 旋转 / 尺度 / 不透明度)
- **优点**:参数共享、显存省、能表达大幅度运动、**与 HexPlane 结合后时空查询便宜**
- **缺点**:deformation 误差会传播到整帧
- **`[基于 Wu-4DGS abstract + 论文笔记]`**:HexPlane 6 个特征平面 × canonical 高斯,**论文核心**

#### 4.1.2 `per-frame 3DGS 序列`

- **机理**:每个时间戳单独训一套 3DGS
- **优点**:单帧精度高、无 temporal error propagation
- **缺点**:**显存 / 存储爆炸**(`N_frames × per-splat`),与 300 万 splats 上限 + 1080p on mobile 目标**冲突**
- **`[推测]`**:不适合本项目,只作反例

#### 4.1.3 `时间条件 Gaussian`

- **机理**:splat 字段直接条件在 t 上(MLP 输入 t)
- **优点**:表达力强
- **缺点**:训练 / 推理都更贵;**移动端 inference 时每个 splat 都要走 MLP,不适合 300 万 splats / 帧**
- **`[推测]`**:可作"超小规模 + 高保真"备选

### 4.2 推荐

- **主线**:`canonical + deformation`(Wu-4DGS 路线)
- **备选 1**:`canonical + deformation` 简化版(无 HexPlane,纯 MLP,对应 Deformable 3DGS 范式),适合单目 / 数据少
- **备选 2**:per-frame 3DGS,**只用于小时间窗(<30 帧)特写镜头**

---

## 5. 训练范式

### 5.1 损失函数

- **光度 L1**:像素级 L1 loss(标准 3DGS 已有)
- **D-SSIM**:结构相似度损失,平滑高频噪声
- **典型组合**:`L = (1-λ) * L1 + λ * L_DSSIM`,`λ ∈ [0.1, 0.2]`
- **`[基于 3DGS 原论文 README 与 4DGS 仓库 train.py]`**:`[未在公开 abstract 拿到 4DGS 训练权重比例]`,需打开 `train.py` 实测

### 5.2 正则化项

- **`4DGS` 的 deformation field 正则化**:形变场的平滑性约束(论文 `scene/deformation.py` 实现,216 行)
- **`MEGA` 的 entropy-constrained loss**:用 entropy loss 限制 splat 数量,强制"少 splat 表达多场景"(`[abstract 直引]`)
- **`Deformable 3DGS` 的 annealing smoothing**:`[abstract 直引]`,缓解 pose 误差对时间插值的传播

### 5.3 收敛判据

- **数值依据**:验证集 PSNR 平台期(< 0.05 dB / 1k iter 提升)
- **`[未在公开 abstract 拿到 4DGS 训练 epoch 数与分钟数]`**:`4DGS` 论文未在 abstract 给具体分钟数,推测 ~ 数小时 / scene(单 GPU)
- **经验做法**:跑 30k~100k iter,前 7k iter 做 densify(类似 3DGS 的 adaptive density control),后 23k~93k 收敛

### 5.4 训练代码仓库引用

- **`[基于 4DGS 论文笔记, paper-notes 仓库路径]`**:
  - `scene/hexplane.py` 146 行(4D 神经体素的 HexPlane 分解编码)
  - `scene/deformation.py` 216 行(时空变形场)
  - `gaussian_renderer/__init__.py` 139 行(splatting rasterization 入口)
  - `train.py` 21 KB(主训练循环)
  - `scripts/cal_modelsize.py`(模型体积统计脚本,**可作为本调研的 per-splat 体积估算参考**)

---

## 6. 精度评估

### 6.1 指标

- **PSNR**(dB,越大越好):像素级
- **SSIM**(0~1,越大越好):结构级
- **LPIPS**(0~1,越小越好):感知级
- **动态区域专用**:warping error(用光流 / 上一帧 warp 出来的差异)

### 6.2 公开数据集

| 数据集 | 视角数 | 帧数 | 动态程度 | 用途 |
|---|---|---|---|---|
| **D-NeRF synthetic** | 单目 + 多视角(取决于子集) | 短序列 | 中 | synthetic benchmark,4DGS 论文 `Table 1` 引用 |
| **Plenoptic Video Dataset** | 多视角(>20) | 长序列 | 中 | 4DGS / HyperReel 通用 |
| **Neural 3D Video** | 多视角 | 长 | 中 | 4DGS / MEGA 用 |
| **Technicolor Light Field** | 多视角 | 长 | 中-高 | MEGA 报告 190× 压缩的来源 |
| **Nerfies / HyperNeRF** | 单目 | 长 | 高 | 单目动态(Deformable 3DGS 用) |

> **数字纪律**:`4DGS` 在这些数据集上的 Table 1 PSNR 数字未在 `paper-notes/2024-wu-4dgs.md` 精确转写(`[未在公开 abstract 拿到, 需 PDF 核验]`),**下游写 `03-end-to-end-roadmap.md` 时必须打开 PDF Table 1 拿原始数字**。

### 6.3 自建数据集的精度数字

- **`[调研不足,需后续实验]`**:本项目自建的多视角高速相机阵列数据集的精度数字,**需在管线落地后实测**;**不要用 4DGS 论文 Table 1 数字外推到自建场景**。

---

## 7. 主线推荐方案 + 两条备选

### 7.1 主线:**`Wu-4DGS`(canonical + HexPlane + deformation) + MonST3R SfM**

- **机理**:`MonST3R`(动态友好 SfM)→ 初始化 3D 高斯 → `HexPlane` 编码 4D 体素 → `deformation MLP` 预测每帧形变 → 3DGS splatting 光栅化
- **优点**:
  - 论文公开(`hustvl/4DGaussians`)+ 桌面 RTX 3090 数字 `82 FPS @ 800×800`(`[abstract 直引]`)
  - 与本项目"高精度 4DGS 表示"目标最对齐
  - HexPlane 分解使 4D voxel grid 显存可控
- **缺点**:
  - 桌面数字,移动端 FPS **未在公开 abstract 拿到**
  - `4DGS-1K-lite` 不存在 → 移动端加速方案需自研
- **反例**:`Deformable 3DGS` 单目路线精度天花板低,不符合"高精度"目标

### 7.2 备选 1:**`Deformable 3DGS`(Yang 2023,canonical + 纯 MLP deformation,无 HexPlane)**

- **机理**:不做 HexPlane 4D 编码,canonical 空间下纯 MLP 预测 deformation
- **优点**:实现简单、训练快、`[abstract 直引]`"outperforms existing methods significantly"
- **缺点**:
  - **单目输入** → 精度上限低
  - 无 HexPlane → 时空查询比 4DGS 慢
  - **未在公开 abstract 拿到具体 PSNR/FPS 数字**
- **适用场景**:快速原型、数据量少、对精度不敏感的 demo

### 7.3 备选 2:**`MEGA` 训练路径 + `HyperReel` 6-DoF 思想借鉴**

- **机理**:用 MEGA 的 color 字段分解(DC 3 参数 + 共享 AC predictor)训练,**目标**是训出更小、更快可流的 4DGS 资源
- **优点**:`[abstract 直引]` `190× Technicolor / 125× Neural 3D Video 存储压缩`,**已知最可量化的"加速收益"**
- **缺点**:`MEGA` 训练质量"comparable" 定性,**未在公开 abstract 拿到具体 PSNR 数字**;FPS "comparable" 也未给具体数字
- **HyperReel 借鉴点**:`[abstract 直引]`"real-time performance, small memory footprint, high-quality rendering" 三者兼得的设计哲学,以及"without custom CUDA" 的实现思路(`[abstract 直引]`)—— **对移动端 Vulkan 1.3 路径友好**

---

## 8. 采集 SOP 草案(设备清单 + 拍摄步骤 + 同步方案)

### 8.1 设备清单(以 12 路环视为例)

| 类别 | 型号/规格 | 数量 | 备注 |
|---|---|---|---|
| 相机 | 工业面阵相机,全局快门,≥1.6MP | 12 | 环形 + 顶视/底视补充 |
| 镜头 | 定焦 6mm~12mm,光圈可锁 | 12 | 焦距统一 |
| 同步触发器 | 硬件触发板 / PTP 主时钟 | 1 | 关键 |
| 标定板 | AprilGrid 6×6 / ChArUco | 1 | 联合标定 |
| 算力(训练) | 桌面 RTX 3090 / A6000(24GB) 或云上 A100 40GB | 1+ | 训练算力 |
| 存储 | 高速 NVMe SSD(4TB+) | 1+ | 原始视频 + 训练中间产物 |
| 光源 | LED 补光,色温稳定 | 多 | 室内/弱光场景 |

### 8.2 拍摄步骤(单场景)

1. **场景布置 + 标定**:布置多视角相机 → 同步触发上电 → 拍标定板 → 联合标定
2. **静态标定采集**:场景中无运动物体,所有相机同步拍 1 张/视角 → 喂 MonST3R / COLMAP
3. **动态序列采集**:开启同步触发 → 演员 / 物体运动 → 每路相机 30~60 FPS 持续 30~120 秒
4. **同步验证**:导出每路时间戳,挑一帧参考 → 检查同步偏差 < 1 帧
5. **SfM / 训练前处理**:多路视频 → 抽帧 → 喂 SfM / 训练管线

### 8.3 同步方案

- **首选**:硬件触发(GenICam / GPIO) + PTP 时钟
- **备份**:软件时间戳对齐(精度差,仅作 fallback)
- **反推**:`Deformable 3DGS` 用 annealing smoothing 缓解同步误差(`[abstract 直引]`)→ **同步质量直接影响训练稳定性,优先硬件**

---

## 9. 训练算力 / 时间预算

### 9.1 GPU 型号 + 显存

- **推荐**:`NVIDIA RTX 3090`(24GB) / `RTX 4090`(24GB) / `A6000`(48GB) / 云上 `A100 40GB`
- **`[基于 4DGS 论文 abstract]`**:`4DGS` 原文报告在 **RTX 3090** 上跑(`[abstract 直引]`)
- **`[未在公开 abstract 拿到精确显存占用]`**:推测 4DGS 训练峰值 ~ 12~20GB(因 HexPlane 体素网格 + canonical 高斯 + deformation MLP 共同占用)

### 9.2 训练时长

- **`[未在公开 abstract 拿到精确分钟数]`**:`4DGS` 论文报告"~ 数小时 / scene"(`[未在公开 abstract 拿到精确数字,推测]`),12 路相机 + 30 FPS × 60 秒 = 21,600 帧 / 视角
- **MEGA**:`[未在公开 abstract 拿到训练时长]`
- **`[推测]`**:本项目预算(允许重训练)`几小时 ~ 几天 / scene`,与 `00-goal.md` 约束一致

### 9.3 分布式训练

- **`[推测]`**:HexPlane 编码是 6 个独立特征平面,理论上可拆到 6 张 GPU 并行,但 `4DGS` 仓库**未提供官方分布式训练脚本**(需自研)

---

## 10. per-splat 字段 + 资源体积估算

### 10.1 原 4DGS 单 splat 字段(纸面估算)

| 字段 | 维度 | 字节(fp32) | 备注 |
|---|---|---|---|
| 位置 xyz | 3 | 12 | `[基于 3DGS 通用表示]` |
| 旋转四元数 | 4 | 16 | `[基于 3DGS 通用表示]` |
| 尺度 scale | 3 | 12 | `[基于 3DGS 通用表示]` |
| 不透明度 opacity | 1 | 4 | `[基于 3DGS 通用表示]` |
| 球谐 SH(最高阶 3,RGB) | 3 × 16 = 48 | 192 | `[推测,基于 3DGS SH=3 共 48 系数]` |
| 时间形变参数(由 deformation MLP 共享) | 共享 | 共享,不计 per-splat | `[基于 4DGS canonical 范式]` |
| **小计** | | **~236 B / splat** | `[推测]` |

> **未精确核验**:`4DGS` 单 splat 字段精确字节数**未在公开 abstract 找到**,**需用 `scripts/cal_modelsize.py` 实测**。

### 10.2 300 万 splats 场景总资源(纸面估算)

- **fp32 总量**:`3M × 236 B ≈ 708 MB`(`[推测]`)
- **fp16 总量**:`~ 354 MB`(`[推测]`)
- **MEGA 压缩后**:`~ 354 MB / 190 ≈ 1.86 MB`(`[abstract 直引] 190×`,与 MEGA 报告对得上数量级)
- **`[推测]`**:**MEGA Technicolor 上的"原 4DGS 体积 / 190"**反推:原始 ~ 数百 MB / scene,MEGA 压到几 MB / scene

### 10.3 HexPlane 编码体积

- **`[未在公开 abstract 拿到 HexPlane 网格精确尺寸]`**:推测 6 个特征平面 × H×W×T × C(典型 H=W=T=128, C=32)~ 6 × 128³ × 32 × 4B(fp32)= **~ 1.6 GB**(`[推测]`,**需打开 4DGS 仓库 `scene/hexplane.py` 实测**)

### 10.4 Deformation MLP 体积

- **`[推测]`**:轻量 MLP,~ 数十万参数,~ 1~10 MB

### 10.5 移动端预算

- 目标: < 50 MB / scene(给移动端 App 安装包留余量)
- **`[推测]`**:**单 HexPlane 体素网格就可能超这个数** → 移动端要么 (a) 用 MEGA 思路把 HexPlane 也量化,(b) 改用 `Scaffold-GS` 风格的 anchor + 神经高斯(见 `02-rendering-acceleration.md` §3 引用)

---

## 11. 公开数据集上的精度数字(直接引用 paper notes)

### 11.1 来自 4 篇 paper notes 的精确转写

| 论文 | 数字 | 出处 |
|---|---|---|
| **`4DGS`(Wu 2024)** | **82 FPS @ 800×800 on RTX 3090** | `[abstract 直引]` |
| **`4DGS`** 精度 | "comparable or better than previous SOTA"(D-NeRF / Plenoptic Video) | `[abstract 直引,未在公开 abstract 拿到 Table 1 精确数字]` |
| **`4DGS`** 训练 GPU | RTX 3090 | `[abstract 直引]` |
| **`Deformable 3DGS`(Yang 2023)** | "outperforms existing methods significantly in both rendering quality and speed" | `[abstract 直引,未在公开 abstract 拿到具体 PSNR/FPS 数字]` |
| **`HyperReel`(Attal 2023)** | **"up to 18 FPS at megapixel resolution"** | `[abstract 直引]` |
| **`HyperReel`** | "without any custom CUDA code" | `[abstract 直引]` |
| **`MEGA`(Zhang 2024)** | **~190× storage reduction on Technicolor / ~125× on Neural 3D Video** | `[abstract 直引]` |
| **`MEGA`** | Color 字段从 SH 144 → per-Gaussian DC 3 + 共享 AC predictor | `[abstract 直引]` |
| **`MEGA`** 精度 | "maintains comparable rendering speeds and scene representation quality" | `[abstract 直引,未在公开 abstract 拿到具体 PSNR/FPS]` |

### 11.2 关于 `4DGS-1K-lite`

- **`[未在公开材料找到]`**:精确叫 "4DGS-1K-lite" / "4DGS-1K" 的论文对象在公开 arxiv 上不存在(2026-07-03 检索为止)
- 详细检索过程见 `docs/appendix/paper-notes/2024-zhang-mega-4dgs-acceleration.md` §"关键诚实说明"
- **所以 `00-goal.md` 中"对标 4DGS-1K-lite"的目标实际指向未公开的对象**,需在 `02-rendering-acceleration.md` 中以 **MEGA 作为公开材料里最相关的对标** + 显式声明"4DGS-1K-lite 公开材料未找到"

---

## 12. 已知风险 / 调研不足项

### 12.1 已识别风险

1. **`4DGS-1K-lite` 公开材料未找到** → `00-goal.md` 主对标实际缺失;**所有"对标"段落均要显式说明**(见 `02-rendering-acceleration.md` §5)
2. **4DGS Table 1 精确 PSNR 数字**:`[未在公开 abstract 拿到]` → 下游写 `03-end-to-end-roadmap.md` 时必须打开 PDF 实抄
3. **移动端 4DGS FPS baseline**:`[调研不足,需进一步实验]` → 没有任何公开 abstract 报告 Adreno 8 Gen 4 上的 4DGS FPS 数字
4. **MEGA 移动端数字**:`[未在公开 abstract 拿到]`,MEGA abstract 仅给桌面数字
5. **Scaffold-GS / LightGS / LightGaussian 在 4DGS 上的适配**:`[未在公开 abstract 拿到 4DGS 版本的对照]`,这些方法原都是 3DGS 加速,4DGS 适配需自研
6. **MonST3R 在 8+ 视角高速相机上的稳定性**:`[调研不足,需后续实验]`,MonST3R 项目页强调"动态几何估计",但**未明确报告视角数 > 12 路时的失败率**
7. **InstantSplat 是否能直接喂 4DGS 训练**:`[未在公开 abstract 拿到]`,InstantSplat 论文输出"3D 高斯 + 相机位姿",理论上可作 SfM 替代,但**未经验证与 4DGS deformation field 联合训练**

### 12.2 调研不足项清单(明列,供下一轮实验)

- [ ] 桌面 RTX 3090 / A100 上训 4DGS 12 路 30 FPS × 60s 场景的**精确分钟数与显存峰值**
- [ ] 4DGS Table 1 精确 PSNR / SSIM / LPIPS 数字
- [ ] MonST3R 在 12+ 视角高速相机同步数据集上的失败率
- [ ] HexPlane 网格精确尺寸 + 量化后显存
- [ ] MEGA 在本项目自建数据集上的 `190×` 是否成立
- [ ] 移动端 Adreno 8 Gen 4 上 4DGS 原始 / 压缩后的 FPS 数字(无 mobile 4DGS 实测 baseline)

---

## 附录 A · 引用一览(本文件内引用的论文 / 仓库 / 网页)

| 序号 | 来源 | URL / 路径 | 标注方式 |
|---|---|---|---|
| 1 | Wu et al. 4DGS (CVPR 2024) | <https://arxiv.org/abs/2310.08528>; <https://github.com/hustvl/4DGaussians> | `[abstract 直引]` + `[基于 paper-notes/2024-wu-4dgs.md]` |
| 2 | Yang et al. Deformable 3DGS | <https://arxiv.org/abs/2309.13101> | `[abstract 直引]` + `[基于 paper-notes/2023-yang-deformable-3dgs.md]` |
| 3 | Attal et al. HyperReel | <https://arxiv.org/abs/2301.02238> | `[abstract 直引]` + `[基于 paper-notes/2023-attal-hyperreel.md]` |
| 4 | Zhang et al. MEGA | <https://arxiv.org/abs/2410.13613>; <https://github.com/Xinjie-Q/MEGA> | `[abstract 直引]` + `[基于 paper-notes/2024-zhang-mega-4dgs-acceleration.md]` |
| 5 | Fan et al. InstantSplat | <https://arxiv.org/abs/2403.20309>; <https://instantsplat.github.io/> | `[abstract 直引]` + `[基于 web 检索 2026-07-03]` |
| 6 | MonST3R 项目页 | <https://monst3r-project.github.io/> | `[基于 web 检索 CSDN 笔记 2025-01-16]` |
| 7 | MV-DUSt3R 论文笔记 | <https://blog.csdn.net/m0_74310646/article/details/145170044> | `[基于 web 检索 2026-07-03]` |
| 8 | DUSt3R 知乎综述 | <https://zhuanlan.zhihu.com/p/714975455> | `[基于 web 检索 2026-07-03]` |
| 9 | 3DGS on Android 仓库 | <https://github.com/torbys/3DGS_App> | `[基于 web 检索 2026-07-03]` |
| 10 | NVIDIA vk_gaussian_splatting | <https://github.com/nvpro-samples/vk_gaussian_splatting> | `[基于 web 检索 2026-07-03,桌面 Vulkan viewer]` |

> 本附录仅列入本文件**新引用的**(paper notes 之外)来源;4 篇 paper notes 自身的引用不再重复。
