# 2026-mousa-provablepruning · Provable Pruning for Efficient 3D Gaussian Splatting via Coresets

> **相关性**：**⭐⭐ 派系 C 渲染加速 + 派系 D 流式落地的理论基础补强** —— **"provable coreset" 概念首次引入 3DGS 压缩**（abstract 直引 "the first weighted coreset construction theorem for 3DGS"），**对 resource-limited hardware 部署路径提供理论背书**。**重要边界**：本文**理论意义大于工程加速比**（加速比温和 + 无 mobile 实测）。

## 0.5 元数据

- **venue**: （未给 / preprint）
- **arxiv-id**: 2607.02721
- **s2-id**: （v2 用 Semantic Scholar API 补全）
- **homepage**: （未在 abstract 拿到）
- **github**: `github.com/waseem-m/3dgs_provable_coresets`（abstract 直引 "Project page and open-source code"）
- **status**: preprint
- **收录日期**: 2026-07-09
- **收录来源**: arxiv scan（cron arxiv_4dgs_scan）
- **1-hop 引用**: （v2 补全，见 §11 1-hop 关系图）
- **评级**: ⭐⭐

- **survey_section**: 4
## 1. 一句话问题

3DGS 场景中**几百万个 Gaussian** 在 resource-limited hardware 上无法直接部署，**现有启发式剪枝方法**提供**非可证明的近似保证** + **强依赖 cost 高的 post-pruning finetune** 恢复质量；能否**首次构造带可证明 multiplicative guarantee 的 3DGS coreset** —— **resolution-dependent**，为 prescribed rendering resolution（如 representative views / grids of rays）提供**基于 sensitivity 的 importance score**？

## 2. 链接

- arxiv：<https://arxiv.org/abs/2607.02721>（v1 提交 2026-07-02）
- PDF：已下 `.pdfs/2607.02721.pdf`（39 页，7.82 MB）
- GitHub：`github.com/waseem-m/3dgs_provable_coresets`（abstract 直引）

## 3. 年份 / 作者 / 机构（abstract + PDF 第 1 页直引）

- **年份**：2026（v1 2026-07-02）
- **作者**：Waseem Mousa, Alaa Maalouf
- **机构**：**Department of Computer Science, University of Haifa**（以色列海法大学）

> **机构背景**：以色列海法大学 + 双作者（学生 + 导师推测）—— **小团队纯学术工作**。

## 4. 派系分类

- **派系 C 渲染加速**（核心 —— 剪枝 + 压缩）
- **派系 D 流式落地**（次要 —— resource-limited hardware 部署路径）

## 5. 方法核心（PDF §1 + §3 直引 + abstract 直引）

### 5.1 三层理论结果（PDF §3 核心定理，page 4-7）

1. **不可能性结果**：unrestricted setting 下，**no non-trivial multiplicative 3DGS coreset exists**（abstract 直引）
2. **resolution-dependent 构造**：prescribed rendering resolution（如 representative views / grids of rays）下，**Theorem 2 提供 weighted coreset construction theorem**（PDF §3.2 第 6 页）
   - coreset size: `m ≥ 3S/ε²c · log(2|Q'|/δ)`（S = sensitivity bound，εc = relative error，Q' = query set size，δ = failure probability）
   - 证明：sensitivity-based sampling + multiplicative concentration bound + union bound
3. **true rendering guarantee transfer**：fixed-objective guarantee → true rendering guarantee **在 log-transmittance stability 假设下**（Assumption 1 第 7 页）

### 5.2 三个 query 粒度的工程变体（PDF §3.4 + §IV 第 8 页直引）

1. **Per-channel coreset**：每个 Gaussian 在每个 RGB channel 单独的 sensitivity（最细）
2. **Per-pixel coreset**：聚合 RGB channel 到单像素级 luminance / total color contribution
3. **Per-tile coreset**：tile-level aggregation，匹配 3DGS rasterization kernel tile 大小
4. **Per-scene coreset**（默认实验变体）：**整个 representative rendering set 上的 scene-level aggregation**

> **核心 trade-off**：query 粒度越粗（如 per-scene）→ 保证越弱 + 实测质量越高；query 粒度越细（如 per-channel）→ 保证越强但 coreset size 可能反而更大。

### 5.3 Sensitivity Score 的工程实现（PDF §3 直引）

- 基于 **color-aware L1-style contribution score**（默认）+ **L2 variant**（ablation）
- Sensitivity 衡量：单个 Gaussian 在**保留 queries 上的 rendered objective 贡献**
- 关键设计：**log-transmittance stability assumption**（Assumption 1 第 7 页）—— 假设剪枝 + reweighting **不会剧烈扰动 prefix transmittances**

## 6. 关键数字（PDF Table 1 第 8 页直引）

### Table 1 · prune-only 结果（Mip-NeRF 360 / Deep Blending / Tanks & Temples 平均）

**Prune ratio = 0.90**（保留 10% Gaussians）：

| 方法 | Mip-NeRF 360 PSNR↑ | Mip-NeRF 360 SSIM↑ | Mip-NeRF 360 LPIPS↓ | Deep Blending PSNR↑ | Tanks & Temples PSNR↑ |
|---|---|---|---|---|---|
| GHAP | 16.76 | 0.458 | 0.494 | 20.53 | 14.83 |
| PUP | 15.79 | 0.535 | 0.429 | 19.52 | 13.38 |
| Trim | 14.45 | 0.413 | 0.480 | 16.52 | 12.46 |
| Unif (uniform baseline) | 13.16 | 0.391 | 0.516 | 15.69 | 10.22 |
| **Ours (Provable Pruning)** | **18.16** | **0.580** | **0.417** | **22.16** | **16.35** |

**Prune ratio = 0.99**（保留 1% Gaussians，极端压缩）：

| 方法 | Mip-NeRF 360 PSNR↑ | Deep Blending PSNR↑ | Tanks & Temples PSNR↑ |
|---|---|---|---|
| GHAP | 10.19 | 10.14 | 7.94 |
| PUP | 10.67 | 10.13 | 8.94 |
| Trim | 9.58 | 7.66 | 6.23 |
| Unif | 10.27 | 7.84 | 6.92 |
| **Ours (Provable Pruning)** | **13.97** | **15.62** | **11.98** |

> **核心比值**（表 1 计算）：
> - **prune 0.90 Mip-NeRF 360**：Ours vs GHAP = 18.16/16.76 = **+1.40 dB**；Ours vs Unif = 18.16/13.16 = **+5.00 dB**
> - **prune 0.99 Mip-NeRF 360**：Ours vs GHAP = 13.97/10.19 = **+3.78 dB**；Ours vs Unif = 13.97/10.27 = **+3.70 dB**
> - **极端压缩（0.99）相对增益更大**：Ours 优势主要在 aggressive compression + no / minimal recovery compute 场景

### Figure 2 · mip-NeRF 360 上的 prune-only delta 曲线（PDF 第 9 页直引）

- prune ratio 范围 {0.90, 0.93, 0.95, 0.97, 0.99}
- **PSNR gain 2-6 dB**（vs GHAP / PUP / Trim / Unif）
- **SSIM gain 0.05-0.35**（vs all）
- **LPIPS gain 0.05-0.15**（vs all）

### Figure 3 · short-recovery 实验（PDF 第 10 页直引）

- 测试场景：mip-NeRF 360，prune ratio 0.95 / 0.97 / 0.99
- **结论**（PDF §IV 第 10 页直引）："Our methods maintain a clear advantage throughout the low-budget recovery regime"
- **主要例外**：**GHAP 在 200 finetune iterations 后接近 Ours 性能**（PDF §IV 直引："GHAP begins to approach our performance after 200 finetuning iterations. This is expected, since GHAP is a global compaction method rather than standard pruning"）

### 训练硬件（PDF 第 9 页直引）

- **NVIDIA A100-SXM4-40GB GPU** + **AMD EPYC 7742 64-Core CPU**（桌面级）

## 7. 评估（abstract 直引）

- **评测数据集**（PDF §IV 第 9 页直引）：
  - **Mip-NeRF 360**（9 个场景）
  - **Tanks & Temples**（2 个场景：truck, train）
  - **Deep Blending**（2 个场景：drjohnson, playroom）
  - **总计 13 个场景**，与 3DGS 原论文 [1] 一致
- **评测指标**：PSNR↑ / SSIM↑ / LPIPS↓
- **基线对比**（PDF §IV 第 9 页直引）：
  1. **GHAP**：Gaussian Herding across Pens [17]
  2. **PUP 3D-GS**：Principled Uncertainty Pruning for 3D Gaussian Splatting [16]
  3. **Trimming the Fat** [15]
  4. **Uniform sampling**（query-agnostic baseline）
- **核心结论**（abstract 直引）："state-of-the-art performance, showing that principled importance estimation can be both theoretically meaningful and practically useful"

## 8. 引用（PDF §REFERENCES 第 16 页起，关键引文）

- **[1]** Kerbl et al., 3DGS, ACM TOG 2023
- **[15]** Trimming the Fat
- **[16]** PUP 3D-GS: Principled Uncertainty Pruning
- **[17]** GHAP: Gaussian Herding across Pens
- **[52]** Mip-NeRF 360
- **[53]** Tanks & Temples
- **[54]** Deep Blending

## 9. Insight（与本调研主线的关系）

### 9.1 派系 C / D 双层意义

| 维度 | Provable Pruning | Flux-GS (ECCV 2026) | FlashGS (CVPR 2025) | Pocket-SLAM (2026-06) |
|---|---|---|---|---|
| 路径 | **理论 coreset + 剪枝** | SH 压缩 + WebGL | CUDA kernel 优化 | SLAM 内存压缩 |
| 加速机制 | **可证明重要性分数** | Monte Carlo + MLP bake | algorithmic + kernel | memory hierarchy |
| 移动端实测 | ❌ **未做**（桌面 A100） | ✅ Snap 8 Gen 3 | ✅ mobile consumer GPU | ❌ 未给 |
| 训练 / 后处理开销 | prune + **minimal recovery** | 11 min 训练 | 标准 3DGS 训练 | 6.7× 训练加速 |
| 理论保证 | ✅ **首个可证明 coreset** | ❌ | ❌ | ❌ |
| 适合派系 | **D 流式落地**（先压缩再传） | C 移动端 | C 移动端 | C + D |

> **核心定位**：**Provable Pruning 是派系 D 流式落地的理论预研** —— 4DGS streaming（如 PD-4DGS / GS-NFS / AirGS）传输前需要压缩 Gaussians，**可证明重要性分数**提供了**理论安全保证**（不会因为压缩导致渲染目标剧变）。
> **派系 C 排名**：Provable Pruning 进 INDEX 派系 C，**理论意义大于工程加速比**（无 mobile 实测 + 加速比间接通过剪枝）。

### 9.2 4DGS 移动端路径的具体承诺

- **4DGS streaming 场景**：当 4DGS scene 被压缩到 mobile 部署（如 AirGS / PD-4DGS），**可证明 coreset 给传输端一个 "transmission budget 上界"** —— 传输 m 个 Gaussians（m 由 Theorem 2 bound 决定）可保证 rendered objective 不超过 εc 倍误差。
- **4DGS 训练端**：训练阶段每 N 步做一次 coreset pruning（per-scene 或 per-tile variant）→ **降低训练显存 + 加速训练** —— 与派系 A 训练加速相关。
- **派系 D 实际落地**：`{理论 coreset size bound} + {entropy coding (EvoGS / 4DGCPro)}` 组合是**派系 D 的下一步方向** —— **v2 用 S2 API 自动拉取后续工作引用**。

### 9.3 关键边界声明

- **不可能性 + 条件性**：abstract + PDF §3 直引 "in the unrestricted setting, no non-trivial multiplicative 3DGS coreset exists" + guarantee 是 **resolution-dependent**（依赖 prescribed rendering resolution）。
- **Transmittance stability assumption**：Assumption 1 第 7 页是**额外假设**，**理论上不一定对所有场景都成立**（4DGS 大 deformation 场景可能违反）。
- **桌面 A100 训练**：**未在 mobile GPU 实测**（Snap 8 Gen 4 适配性完全未知）。
- **工程加速比间接**：本文**主目标是 prune-only 质量**，**不直接报 FPS**（加速通过 "Gaussian 数量减少" 间接体现）—— **不如 FlashGS / Flux-GS 的 FPS 数字直观**。

## 10. 我未找到 / 提请下游注意

- **Mobile GPU 实测**：abstract 完全未提；**桌面 A100 为唯一评测平台**。
- **FPS 数字**：Table 1 仅报 PSNR / SSIM / LPIPS，**未报 FPS** —— **需结合 [1] / [15-17] baseline 的 FPS 数字估算**。
- **Vulkan 1.3 兼容性**：未做实验。
- **Homepage**：abstract 未给（仅 GitHub）。
- **venue**：预投，**未确定会议 / 期刊**。

## 11. 1-hop 关系图

### 11.1 引用列表中相关工作 (downstream 视角)

- **3DGS 原论文**：[2023-kerbl-3dgs](2023-kerbl-3dgs.md)
- **Trimming the Fat [15]**：（未在 INDEX，需 v2 补全）
- **PUP 3D-GS [16]**：（v2 补全）
- **GHAP [17]**：（v2 补全）

### 11.2 派系 C / D 直接相关下游

- **派系 C 引用关系**：Provable Pruning 与派系 C 中 **Pocket-SLAM（[2026-li-pocket-slam](2026-li-pocket-slam.md)）、Smaller-Faster-3DGS（[2026-gong-dict-3dgs](2026-gong-dict-3dgs.md)）** 共享 "compression for limited hardware" 主线，**但路径不同**：本文理论 coreset；前两者工程压缩。
- **派系 D 引用关系**：与 **GS-NFS（[2026-ghosh-gs-nfs](2026-ghosh-gs-nfs.md)）、AirGS（[2025-wang-airgs](2025-wang-airgs.md)）、PD-4DGS（[2025-li-pd4dgs](2025-li-pd4dgs.md)）、EvoGS（[2026-shi-evogs](2026-shi-evogs.md)）** 共享 "streaming compression" 主线 —— **Provable Pruning 提供理论基础**，**派系 D 提供工程实现**。
- **推测的 1-hop 引用**：派系 C / D 后续工作**很可能引用 Provable Pruning 的 Theorem 2 作为 "传输 budget bound" 理论基础** —— **v2 用 S2 API 自动拉取完整 cited-by 列表**。
