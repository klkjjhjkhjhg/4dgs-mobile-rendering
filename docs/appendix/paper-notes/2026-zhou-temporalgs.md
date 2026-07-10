# 2026-zhou-temporalgs · TemporalGS: Training-Free Plug-and-Play Acceleration for 3D Gaussian Splatting Rendering via Temporal Priors

> **相关性**：**⭐⭐ 派系 C 渲染加速新基线** —— **"training-free + plug-and-play + 无 post-training"** 路径在 3DGS 加速方法中**首次明确提出**（abstract 直引 "the first training-free plug-and-play algorithmic approach"）。**对 4DGS 移动端意义**：本工作**显式承认未来工作方向是 "develop a TemporalGS counterpart in 4D Gaussian Splatting"**（PDF §5 Future Work 第 8 页）—— **4DGS 移动端的方向背书**。

## 0.5 元数据

- **venue**: （未给 / 预投期刊模板 = IEEE Transactions on Visualization and Computer Graphics / TVCG 推测，**未验证**）
- **arxiv-id**: 2607.03390
- **s2-id**: （v2 用 Semantic Scholar API 补全）
- **homepage**: （未在 abstract 拿到）
- **github**: （未在 abstract 拿到；**需从项目页 / PDF 核**）
- **status**: preprint
- **收录日期**: 2026-07-09
- **收录来源**: arxiv scan（cron arxiv_4dgs_scan）
- **1-hop 引用**: （v2 补全，见 §11 1-hop 关系图）
- **评级**: ⭐⭐

- **survey_section**: 5
## 1. 一句话问题

如何在 **tile-based 3DGS 渲染管线**（**软件 rasterization 起点 + 可移植到硬件 rasterization**）中利用**相邻帧之间 Gaussian 重叠**这一时序先验，**无需任何 post-training / post-processing** 即获得**最高 1.48× 渲染加速**，并保持 competitive rendering quality？

## 2. 链接

- arxiv：<https://arxiv.org/abs/2607.03390>（v1 提交 2026-07-03）
- PDF：已下 `.pdfs/2607.03390.pdf`（9 页，1.16 MB）

## 3. 年份 / 作者 / 机构（PDF §1 底部直引）

- **年份**：2026（v1 2026-07-03）
- **作者**：Yuhongze Zhou, Zihao Yang, Xinxin Zuo, Juwei Lu
- **机构**（PDF 第 1 页底部脚注直引）：
  1. **Yuhongze Zhou — McGill University**, Montréal, Canada
  2. **Zihao Yang — University of Waterloo**, Waterloo, Canada
  3. **Xinxin Zuo — Concordia University**, Montréal, Canada
  4. **Juwei Lu — University of Toronto**, Toronto, Canada

> **全是加拿大 4 所大学联合**：McGill + Waterloo + Concordia + Toronto。**没有产业界背书**（对比 Flux-GS 的 UTS + Baidu + Adelaide）。**纯学术工作**。

## 4. 派系分类

- **派系 C 渲染加速**（核心）

## 5. 方法核心（PDF §1-§3 直引 + abstract 直引）

### 5.1 时序先验的两个关键 buffer（PDF §1 + §3 直引）

- **Temporal Geometry Buffer (TGB)**：warped depth 几何缓存
- **Temporal Appearance Buffer (TAB)**：warped 颜色 / alpha 外观缓存

### 5.2 两大加速策略（abstract 直引）

1. **Temporal Dynamic Culling (TDC)**：
   - **Adaptive Frustum Culling (AFC)**：剔除新视角物理视锥外的 Gaussians
   - **Temporal Occlusion Culling (TOC)**：剔除**被 warped TGB 几何遮挡**的 Gaussians
2. **Selective Rendering (SR)**：
   - 只渲染**无法被 warped TAB 近似**的 tile
   - **未选中 tile** 用 warped TAB 直接填回
   - **stitching**：渲染 tile + warped TAB 拼接成新帧

### 5.3 自适应参考帧插入（PDF §3 直引）

- **问题**：相机运动快 / 3DGS 表面表示不精确 → **unmatched tile 增加 → warping 错误 → 加速收益降低**
- **解法**：当连续 SR 帧 selected tile 比例超过 **η = 40%**（PDF §3 直引）时，**强制插入一个 pseudo reference frame**（标准 3DGS 渲染）
- **核心**：trade-off between rendering efficiency and quality

### 5.4 跨平台可移植性（abstract 直引 + PDF §IV 直引）

- **软件 rasterization**：原生实现
- **硬件 rasterization**：扩展到 **fastgauss** 和 **web-splat**（PDF §IV-B2 + Table II 第 7 页直引）
- **CUDA**：为提升跨平台性能，**实现到 CUDA**（PDF §IV-B2 第 7 页直引："we implement TemporalGS in CUDA for its popularity and excellent performance across small- and large-scale scenes"）

## 6. 关键数字（PDF Table I 第 6 页直引）

### Table I · 大规模 aerial / street-view 场景（5 数据集平均）

| 类别 | 方法 | Avg PSNR↑ | Avg SSIM↑ | Avg LPIPS↓ | Avg FPS↑ | Mem(GB)↓ |
|---|---|---|---|---|---|---|
| Baseline | CityGS | 24.43 | 0.815 | 0.238 | **122** | 8.22 |
| Post-training | LightGS | 22.77 | 0.753 | 0.311 | 267 | **2.23** |
| Post-training | CP3DGS | 23.26 | 0.753 | 0.304 | 176 | 2.50 |
| Post-training | StochasticSplats | 21.79 | 0.557 | 0.426 | 93 | **7.44** |
| Training | C3DGS | 21.28 | 0.673 | 0.411 | 464 | 1.27 |
| Post-processing | RadSplat | 24.12 | 0.811 | 0.241 | 216 | 8.28 |
| Temporal-coherence | NeoG | 23.44 | 0.807 | 0.244 | 130 | 12.37 |
| **Training-free plug-and-play** | **CityGS-TGS** | 23.69 | 0.774 | 0.255 | **287** | 8.48 |
| Training-free plug-and-play | LightGS-TGS | 22.32 | 0.720 | 0.323 | **559** | 2.35 |
| Training-free plug-and-play | CP3DGS-TGS | 22.78 | 0.720 | 0.319 | 437 | 2.72 |
| Training-free plug-and-play | StochasticSplats-TGS | 21.99 | 0.584 | 0.399 | 187 | 7.70 |
| Training-free plug-and-play | C3DGS-TGS | 21.09 | 0.654 | 0.418 | **918** | 1.31 |
| Training-free plug-and-play | RadSplat-TGS | 23.40 | 0.769 | 0.259 | **392** | 8.54 |

> **核心比值**（abstract 数字）：
> - **"up to 1.48× acceleration"**（abstract 直引）
> - **训练/后处理开销 = 0**（abstract 直引 "without any post-training or post-processing"）
> - **CityGS-TGS vs CityGS**：287/122 = **2.35× FPS↑**，**代价 -0.74 dB PSNR + 0.26 GB mem↑**（表 I 第 6 页直引计算）

### Table IV · 模块消融（PDF 第 7 页直引）

| AFC | TOC | SR | Kitchen PSNR↑ | Kitchen FPS↑ | Residence PSNR↑ | Residence FPS↑ |
|---|---|---|---|---|---|---|
| ✓ | ✓ |  | 30.03 | 328 | 21.13 | 300 |
| ✓ |  | ✓ | 30.03 | 313 | 21.16 | 258 |
|  | ✓ | ✓ | 30.04 | 311 | 21.13 | 246 |
| ✓ | ✓ | ✓ | 30.82 | **244** | 22.05 | **165** |
| ✓ | ✓ | ✓ | **30.03** | **331** | **21.16** | **320** |
| 3DGS / CityGS baseline |  |  | 30.84 | 231 | 22.03 | 126 |

> **模块贡献**（PDF §IV-B3 第 7 页直引）：
> - **SR 模块贡献最大**：Kitchen +87 FPS / Residence +155 FPS
> - **TOC 模块**：Kitchen +18 FPS / Residence +62 FPS
> - **AFC 模块**：Kitchen +3 FPS / Residence +20 FPS
> - **PSNR 影响**：TOC 和 AFC 对 PSNR 影响小；full combo 比单一模块 PSNR 略低

### Table V · 相机运动速度影响（PDF 第 7 页直引）

| Interval | Kitchen PSNR↑ | Kitchen FPS↑ | SR Tile(%) |
|---|---|---|---|
| 0.02 (慢) | 30.03 | 331 | 33.59 |
| 0.05 | 30.15 | 282 | 45.65 |
| 0.1 (快) | 30.29 | 255 | 63.87 |

| Interval | Residence PSNR↑ | Residence FPS↑ | SR Tile(%) |
|---|---|---|---|
| 0.1 | 21.16 | 320 | 9.22 |
| 0.2 | 21.58 | 302 | 15.84 |
| 0.4 | 21.23 | 260 | 23.69 |

> **结论**（PDF §IV-B3 直引）：相机越快 → SR tile 比例越高 → 加速收益下降；Residence 大场景相对稳定（9% → 24%），Kitchen 小场景敏感（34% → 64%）。

## 7. 评估（abstract 直引）

- **评测数据集**（PDF §IV-A 第 5 页直引）：
  1. **小规模**：Mip-NeRF-360 9 个场景（outdoor ×4 downsample, indoor ×2 downsample）
  2. **大规模 aerial**：MatrixCity + Residence + Building + Rubble
  3. **大规模 street-view**：Hierarchical Gaussian Small City
  4. **大规模 indoor**：OccluScene3D（canteen / classroom / building）
- **基线对比**：
  - Baseline：CityGS
  - Post-training：LightGS / CP3DGS / StochasticSplats
  - Training-based：C3DGS
  - Post-processing：RadSplat
  - Temporal-coherence：NeoG
  - **6 个 baseline 全部可以 plug-in TemporalGS**（PDF §IV 直引）
- **核心结论**（abstract 直引）："achieving **up to 1.48× acceleration**, while maintaining competitive rendering quality"

## 8. 引用（PDF §REFERENCES 第 8 页起，关键引文）

- **[1]** Kerbl et al., 3D Gaussian Splatting for Real-Time Radiance Field Rendering, ACM TOG 2023（**3DGS 原论文**）
- **[2]** Fan et al., LightGaussian, NeurIPS 2024
- **[9]** Feng et al., FlashGS, CVPR 2025（**与本项目派系 C 直接相关**）
- **[10]** Liao et al., TC-GS, SIGGRAPH Asia 2025
- **[11]** Kheradmand et al. （GScore 引用）
- **[16]** Hierarchical Gaussian (street-view dataset reference)
- **[32]** NeRFBuff（camera motion simulation reference）
- **[36]** Mip-NeRF 360 dataset
- **[37]** MatrixCity dataset
- **[38]** Rubble / Building / Residence real-world datasets

> **关键引用关系**：FlashGS（派系 C 同主线）是 TemporalGS 引用列表 #9，**说明 TemporalGS 团队知道并对标了 FlashGS 路径**。同时 FlashGS 的 "average 4× acceleration over mobile consumer GPUs" 是本调研更关心的数字，**TemporalGS 的 1.48× 在 mobile 上是次优数字**。

## 9. Insight（与本调研主线的关系）

### 9.1 派系 C 排名意义

| 维度 | TemporalGS | Flux-GS（ECCV 2026） | FlashGS（CVPR 2025） |
|---|---|---|---|
| 训练 / 后处理开销 | **零**（核心卖点） | 11 min 训练 | 标准 3DGS 训练 |
| 加速比（avg） | **1.48×**（abstract 直引） | 13.7× over 3DGS（Fig.1） | **4× over mobile consumer GPU**（abstract） |
| 移动端实测 | ❌ **未做**（桌面 RTX 系） | ✅ Snap 8 Gen 3 | ✅ mobile consumer GPU |
| 4DGS 适配 | ❌ 未做（**Future Work 提到**） | ❌ 未做（3DGS static） | ❌ 未做 |

> **核心 trade-off**：TemporalGS 是**桌面 software-rasterization 优化**路线，**加速比温和（1.48×）但完全无训练开销**；FlashGS / Flux-GS 是**移动端实测 + 更大加速比（4×-13.7×）但需训练**。**对本项目 Snap 8 Gen 4 + Vulkan 1.3 的意义**：TemporalGS 的 training-free plug-and-play 思路**对 4DGS 实时渲染路径具有启发性**（4DGS temporal dimension 自然提供 frame-to-frame overlap）。

### 9.2 4DGS 移动端路径的具体承诺

- **PDF §5 Future Work 第 8 页直引**："**It is also interesting to develop a TemporalGS counterpart in 4D Gaussian Splatting.**" —— **作者本人承认 4DGS 是直接外推目标**。
- **本项目对应动作**：M3 spike 阶段可借鉴 **TGB / TAB 双 buffer** 思想：4DGS 的 temporal dimension 在 t→t+i 时**自然产生 Gaussian 重叠**（deformation field 推导 + canonical anchor），**TGB/TAB 概念可直接迁移到 4DGS canonical → 当前帧 warp 流程**。
- **派系 C 更新**：TemporalGS 进 INDEX 派系 C，**排在 C3DGS / FlashGS / Flux-GS / Mobile-GS 之后**（因 mobile 实测缺失 + 加速比 1.48× 偏低）。

### 9.3 关键边界声明

- **未在移动端实测**：abstract + 实验部分**全部在桌面 RTX 系**（PDF §IV 第 5-7 页）；**Snap 8 Gen 4 + Vulkan 1.3 适配性未知**。
- **web-splat 兼容但加速有限**：PDF §IV-B2 第 7 页直引："**TemporalGS does not significantly boost web-splat in some cases. The main reason is that depth rendering requires float16 instead of uint8, and WebGPU does not optimize float16 as it does for uint8.**" —— **WebGPU/Vulkan 移植警告**。
- **加速比温和**：1.48× 平均加速 vs Flux-GS 13.7× / FlashGS 4×，**对 mobile 资源极度受限的 Adreno 8 Gen 4 单独使用不够**。

## 10. 我未找到 / 提请下游注意

- **GitHub repo**：abstract 未给；**需 PDF 核 §V 第 8 页或项目页**。
- **Snap 8 Gen 3 / 8 Gen 4 实测**：abstract 完全未提；**桌面 RTX 系为唯一评测平台**。
- **Mobile GPU 显存数字**：Table I 仅给 desktop peak memory（GB），**未给 mobile 适配后显存**。
- **Vulkan 1.3 兼容性**：未做实验，**需本项目 M3 spike 阶段实测**。
- **venue**：PDF 头部 "JOURNAL OF LATEX CLASS FILES" 是预投模板，**实际会议 / 期刊未确定**。

## 11. 1-hop 关系图

### 11.1 TemporalGS 引用列表中相关工作 (downstream 视角)

- **3DGS 原论文**：[2023-kerbl-3dgs](2023-kerbl-3dgs.md)
- **FlashGS (CVPR 2025)**：[2024-feng-flashgs](2024-feng-flashgs.md)（**派系 C 直接相关**，被 TemporalGS 引用为 #9）
- **LightGaussian (NeurIPS 2024)**：[2023-fan-lightgaussian](2023-fan-lightgaussian.md)（post-training 压缩，被 TemporalGS 引用为 #2）
- **C3DGS**：（未在 INDEX，需 v2 补全）
- **NeoG**：（v2 补全）
- **RadSplat (3DV 2025)**：（v2 补全）

### 11.2 4DGS / mobile 直接相关下游

- **本项目相关下游**：TemporalGS 是派系 C 渲染加速中**唯一明确提出"training-free plug-and-play"路径**的工作，**与 Flux-GS（训练路线）形成路径对比**。**两路径可在本项目 M3 spike 阶段对比验证**。
- **推测的 1-hop 引用**：RetimeGS / SharpTimeGS / CAGS / 4DGS-CC / SpeeDe3DGS 派系 B 工作**未来可能会引用 TemporalGS**（因为 TemporalGS 是 3DGS 加速的最新基线之一）—— **v2 用 S2 API 自动拉取完整 cited-by 列表**。
