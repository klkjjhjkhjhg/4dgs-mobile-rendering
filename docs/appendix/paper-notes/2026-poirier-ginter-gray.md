# 2026-poirier-ginter-gray · GRay: Ray Tracing 3D Gaussians Near the Speed of Splats

> **相关性**：**⭐⭐ 派系 C 渲染加速 + 派系 A 表示** —— **首次让 3DGS ray tracing 接近 rasterization 的速度**（abstract 直引："**GRay renders nearly 4× faster and optimizes nearly 10× faster than 3DGRT**"），**已发表于 Proc. ACM CGIT Vol. 9 No. 1 Article 14 (May 2026)**（DOI: 10.1145/3804496）—— **难得的 ACM 同行评审背书**。**对 4DGS 移动端意义**：为未来 4DGS ray tracing 提供速度基线（**4DGRT 已是本项目派系 D 收录工作**）。

## 0.5 元数据

- **venue**: **ACM Proc. CGIT Vol. 9 No. 1 Article 14 (May 2026)**（DOI: 10.1145/3804496，**同行评审已通过**）
- **arxiv-id**: 2606.30869
- **s2-id**: （v2 用 Semantic Scholar API 补全）
- **homepage**: （未给）
- **github / code**: `https://repo-sam.inria.fr/nerphys/gray`（abstract 直引）
- **status**: published
- **收录日期**: 2026-07-09
- **收录来源**: arxiv scan（cron arxiv_4dgs_scan）
- **1-hop 引用**: （v2 补全，见 §11 1-hop 关系图）
- **评级**: ⭐⭐

## 1. 一句话问题

3DGS ray tracing（3DGRT）当前**比 rasterization 慢一个数量级**（3DGRT 优化 9× 慢于 3DGS，PDF §1 直引），**关键瓶颈在 dense initialization (DI) 下 rasterization 慢但 ray tracing 快**这一反直觉观察 —— **能否设计 ray tracer 让 ray tracing 在 dense initialization 下达到近 rasterization 速度**？

## 2. 链接

- arxiv：<https://arxiv.org/abs/2606.30869>（v1 提交 2026-06-29）
- PDF：已下 `.pdfs/2606.30869.pdf`（33 页，24.9 MB）
- 正式发表：<https://doi.org/10.1145/3804496>，ACM Proc. CGIT Vol. 9 No. 1 Article 14 (May 2026)
- Code：<https://repo-sam.inria.fr/nerphys/gray>（abstract 直引）

## 3. 年份 / 作者 / 机构（PDF §1 + footer 直引）

- **年份**：2026（v1 arxiv 2026-06-29，**ACM 正式发表 May 2026**）
- **作者**：Yohan Poirier-Ginter, Jean-François Lalonde, George Drettakis
- **机构**（PDF 第 1 页脚注直引）：
  1. **Yohan Poirier-Ginter** — Université Laval, Quebec, Canada + Inria, Université Côte d'Azur, France
  2. **Jean-François Lalonde** — Université Laval, Quebec, Canada
  3. **George Drettakis** — Inria, Université Côte d'Azur, France

> **Inria + Université Laval 跨国合作** —— **Inria 是欧洲顶级 graphics / vision 实验室**（与 GRAPHDECO 团队深度关联），**学术背书强**。

## 4. 派系分类

- **派系 C 渲染加速**（核心 —— ray tracing 路径的加速）
- **派系 A 表示**（次要 —— dense initialization + weight-based pruning 的表示改进）

## 5. 方法核心（PDF §1-§5 直引）

### 5.1 关键观察：dense initialization 反转 ray tracing / rasterization 的性能关系

**PDF §1 + §3 直引**：
- **Sparse Initialization (SI) + 3DGS rasterization**：~660 FPS @ 0.11M Gaussians
- **SI + 3DGRT ray tracing**：~96 FPS @ 0.11M Gaussians （ray tracing 慢 7×）
- **Dense Initialization (DI) + 3DGS rasterization**：~282 FPS @ 3.97M Gaussians （DI 让 rasterization 慢 0.43×，Gaussian 数从 100K → 4M）
- **DI + 3DGRT ray tracing**：~140 FPS @ 3.97M Gaussians（**ray tracing 在 DI 下反而快 1.46×**）
- **核心结论**："**DI speeds up ray tracing instead of slowing it down**"（PDF §3 第 7 页直引）

### 5.2 5 项关键技术（PDF §5 直引）

1. **Dense Initialization (DI)** + **Initialization Binning**（Table 8：3.97M → 3.27M）
2. **OBB-based BVH**（替代 icosahedron，Table 2：DI 下训练 2× 加速，01:22:12 → 40:05）
3. **Per-Pixel Linked Lists (PPLL)**（Table 4：DI 下 FPS +40%，175 → 248）
4. **Detached Hybrid Transparency (DHT)**（Table 3：稳定 early ray termination，opt time 6:33 → 5:40）
5. **Weight-Based Pruning + Scale Decay**（Table 5：3.27M → 1.52M，FPS 189 → 248；Table 7：FPS 157 → 248）

### 5.3 训练迭代减半（PDF §5 第 11 页 + Table 6 直引）

- DI 让收敛更快 → **训练迭代从 30K → 15K**（"halved training times almost for free"，PDF 第 11 页直引）
- 学习率 schedule 调整：scale / rotation / SH DC 早期更高 + 渐进衰减 + SH higher-order LR 5× = 0.000625

## 6. 关键数字（PDF Fig.1 第 1 页 + Table 9 第 13 页直引）

### Fig. 1 · 三大方法核心对比（13 个标准 3DGS 评测场景平均）

| 方法 | PSNR↑ | SSIM↑ | LPIPS↓ | Init Time | Opt Time↓ | FPS↑ | Init #G↓ | Final #G↓ | Iterations |
|---|---|---|---|---|---|---|---|---|---|
| **3DGS** (vanilla, SI) | 27.10 | 0.831 | 0.262 | 00:00 | 06:18 | **253** | 0.11M | 2.25M | 30000 |
| 3DGRT (SI) | 26.77 | 0.828 | 0.258 | 00:00 | **55:01** | 68 | 0.11M | 3.24M | 30000 |
| **GRay** (DI + 5 项技术) | 26.47 | 0.819 | **0.236** | 01:58 | **05:40** | **248** | 3.27M | **1.52M** | **15000** |

> **核心比值**（abstract + Fig.1 直引）：
> - **GRay vs 3DGRT**：248/68 = **3.65× FPS↑**（abstract 称 "nearly 4×"） + 55:01/05:40 = **9.7× 优化加速**（abstract 称 "nearly 10×"）
> - **GRay vs 3DGS**：248/253 = **0.98× FPS**（competitive but slightly slower）+ 26.47/27.10 = **-0.63 dB PSNR** + LPIPS 反而更好（0.236 vs 0.262）
> - **3DGRT vs 3DGS**：68/253 = **0.27× FPS**（ray tracing 慢 ~4×） + 55:01/06:18 = **8.7× 慢**

### Table 9 · 全方法对比（含 EDGS / RayGaussX 等）

**GRay 关键对比**（PDF Table 9 第 13 页直引）：

| Variant | PSNR↑ | LPIPS↓ | Opt Time↓ | FPS↑ | Final #G↓ | Iter |
|---|---|---|---|---|---|---|
| 3DGS_SI | 27.10 | 0.262 | 06:18 | 253 | 2.25M | 30000 |
| 3DGS_DI | 26.97 | 0.226 | 10:09 | 241 | 3.28M | 30000 |
| EDGS_RegularAdam | 27.55 | 0.204 | **30:38** | 173 | 2.26M | 30000 |
| RayGaussX | **28.14** | 0.221 | 56:18 | 39 | 3.28M | 30000 |
| 3DGRT_DI | 26.46 | 0.229 | 40:05 | 131 | 2.64M | 30000 |
| **GRay** | 26.47 | 0.236 | **05:40** | **248** | **1.52M** | **15000** |

> **GRay vs 同类 SOTA**：
> - **vs RayGaussX**（高质慢速 ray tracer）：FPS 248/39 = **6.4× 快**，PSNR 仅 -1.67 dB
> - **vs EDGS_RegularAdam**：FPS 248/173 = **1.43× 快**，PSNR -1.08 dB，opt time 5:40 vs 30:38 = **5.4× 训练加速**

### Table 1 · SI vs DI 在 3DGS / 3DGRT 上的影响（PDF 第 7 页直引）

| 方法 | #Gaussians↓ | Opt Time↓ | FPS↑ |
|---|---|---|---|
| 3DGS_SI | 0.11M | 00:16 | 660 |
| 3DGS_DI | 3.97M | 00:50 (0.32×) | 282 (0.43×) |
| 3DGRT_SI | 0.11M | 00:31 | 96 |
| 3DGRT_SI* | 0.11M | 00:30 | 98 |
| **3DGRT_DI** | 3.97M | 00:28 (**1.11×**) | **140 (1.46×)** |

> **DI 反转效应**：rasterization 慢 2.3×，ray tracing **快 1.46×**。

### Table 3 / 5 · DHT 与 Pruning 单独贡献

| 组件 | 贡献 |
|---|---|
| **DHT** | Opt time 6:33 → 5:40，skip 40% hit Gaussians，稳定训练 |
| **PPLL** | DI 下 FPS +40%（175 → 248） |
| **Weight-Based Pruning** | 3.27M → 1.52M，FPS 189 → 248，**PSNR 反而提升** |
| **Scale Decay** | FPS 157 → 248（quality-speed trade-off） |

## 7. 评估（abstract + PDF §6 直引）

- **评测数据集**：13 个标准 3DGS 评测场景
  - **Mip-NeRF360**（9 场景）
  - **Tanks & Temples**（2 场景）
  - **Deep Blending**（2 场景）
- **评测指标**：PSNR↑ / SSIM↑ / LPIPS↓ + Init Time + Opt Time + FPS + Gaussian count
- **基线对比**：
  - 3DGS_SI / 3DGS_DI（rasterization baseline）
  - 3DGRT_SI / 3DGRT_DI（**核心 baseline**，ray tracing 原版）
  - **EDGS**（Kotovenko et al. 2025，DI + Regular Adam）
  - **RayGaussX**（慢速高质 ray tracer）
  - 多个 ablation 变体（NoDHT / NoPruning / NoDecay / NoBinning / MultipleTraversal）
- **核心结论**（abstract 直引）："**GRay renders nearly 4× faster and optimizes nearly 10× faster than 3DGRT while maintaining similar quality, and has competitive speed with 3DGS albeit at somewhat lower quality**"

## 8. 引用（PDF §REFERENCES 第 25 页起，关键引文）

- **3DGS 原论文**（Kerbl et al. 2023）
- **3DGRT**（Moenne-Loccoz et al. 2024）—— **核心 baseline**
- **EDGS**（Kotovenko et al. 2025）—— DI 加速收敛
- **EPBRR**（Poirier-Ginter et al. 2025）—— 同一作者前序工作
- **GRTX**（Lee et al. 2026，**concurrent work**）—— 硬件扩展加速 3DGRT
- **RaySplats**（Byrski et al. 2025a）—— early termination approximation
- **3DGUT**（Wu et al. 2025）—— rasterization 扩展到 general camera models
- **EVER**（Mai et al. 2025）—— ray tracing for exact per-pixel sorting
- **Taming 3DGS**（Mallick et al. 2024）—— 改进的 optimizer
- **PPLL**（Yang et al. 2010）—— per-pixel linked lists 原出处
- **OptiX**（Parker et al. 2010）—— NVIDIA ray tracing framework
- **REdiSplats**（Byrski et al. 2025b）—— mesh-aligned Gaussians
- **DHT**（Hahlbohm et al. 2025；Maule et al. 2013）—— detached hybrid transparency

## 9. Insight（与本调研主线的关系）

### 9.1 派系 C 排名意义

| 维度 | GRay | Flux-GS (ECCV 2026) | FlashGS (CVPR 2025) | TemporalGS (2026-07) |
|---|---|---|---|---|
| 路径 | **Ray tracing 加速** | SH 压缩 + WebGL | CUDA kernel 优化 | 时序先验 |
| **核心数字** | **4× vs 3DGRT** | 13.7× over 3DGS | **4× mobile** | **1.48×** |
| **渲染速度（FPS）** | **248** | 147 (Snap 8 Gen 3) | 未给具体 FPS | 287 avg |
| 移动端实测 | ❌ **桌面 RTX 系** | ✅ Snap 8 Gen 3 | ✅ mobile GPU | ❌ 桌面 |
| 训练 / 后处理开销 | **DI 1:58 init + 5:40 opt** | 11 min 训练 | 标准 | 零 |
| **venue** | **ACM CGIT May 2026** ✅ | ECCV 2026 | CVPR 2025 | preprint |

> **核心 trade-off**：GRay 是**桌面 RTX 系 ray tracing 路径**，**248 FPS 已接近 3DGS rasterization 253 FPS**；但**桌面 GPU** 与 **Snap 8 Gen 4 mobile GPU** 完全不同 —— **mobile ray tracing 路径仍未验证**。**派系 C 排名**：GRay 进 INDEX 派系 C，**作为 ray tracing 路径的新基线**，**与 rasterization 路径（FlashGS / Flux-GS / TemporalGS）形成路径对比**。

### 9.2 4DGS 移动端路径的具体承诺

- **4DGRT 已是本项目派系 D 收录工作**（[2025-liu-4dgrt.md](2025-liu-4dgrt.md)）—— **GRay 与 4DGRT 直接同源技术**（3DGRT → 4DGRT 是 3D → 4D 推广），**4DGRT 在 GRay 发表后大概率会参考 GRay 的 DI + 5 项技术**。
- **4DGS Ray Tracing on Mobile**：GRay 给出了**桌面 ray tracing 已达近 rasterization 速度**的证明，但 **mobile GPU (Snap 8 Gen 4 + Vulkan 1.3) 上的 ray tracing 仍未做实验**。**本项目 M3 spike 阶段可探索**：Snap 8 Gen 4 的硬件 ray tracing 单元（Adreno 8 Gen 4 含 hardware ray tracing）能否复用 GRay 的 BVH + PPLL + DHT 路径。
- **派系 D 更新**：GRay 是 4DGRT 桌面版的同源加速版，**未来 4DGRT-on-mobile 路线可参考 GRay**。

### 9.3 关键边界声明

- **桌面 RTX 系**：实验硬件**未给具体 GPU 型号**（PDF §6 第 13 页仅说 "warm start"），**未做 mobile GPU 实测**。
- **FPS = 248 是 rasterization 同等水平**：但**训练时间含 1:58 dense initialization** —— **total time 5:40 = 1:58 init + 3:42 actual opt**（粗算），**vs 3DGS SI 的 6:18 opt without init**。
- **PSNR -0.63 dB vs 3DGS**：是 trade-off，**LPIPS 反而更好**（0.236 vs 0.262）。
- **Iterations 15K（vs 30K）**：需要特定 learning rate schedule（scale / rotation / SH DC 早期更高 + 渐进衰减 + SH LR 5×），**4DGS 适配需要重新调 schedule**。
- **依赖 OptiX（NVIDIA）**：PDF §3 直引使用 OptiX BVH + traversal —— **Snap 8 Gen 4 的 Vulkan 1.3 + Adreno 硬件 ray tracing 兼容性需验证**。

## 10. 我未找到 / 提请下游注意

- **Mobile GPU 实测**：PDF 完全未提；**桌面 RTX 系为唯一平台**。
- **FPS on mobile**：未给任何 mobile FPS 数据。
- **Vulkan 1.3 / OptiX 替代方案**：PDF 完全未提 Vulkan / WebGPU；**Snap 8 Gen 4 ray tracing 路径未知**。
- **4DGS 推广路径**：abstract + PDF 未提及 4DGS；**4DGRT 已发 2025-09 但未引用 GRay**（GRay arxiv 2026-06-29 晚于 4DGRT 2025-09）。

## 11. 1-hop 关系图

### 11.1 GRay 引用列表中相关工作 (downstream 视角)

- **3DGS 原论文**：[2023-kerbl-3dgs](2023-kerbl-3dgs.md)
- **3DGRT**（Moenne-Loccoz et al. 2024）—— **核心 baseline**，未在 INDEX（需 v2 补全）
- **EPBRR**（Poirier-Ginter et al. 2025）—— GRay 同一作者前序工作，未在 INDEX
- **EDGS**（Kotovenko et al. 2025）—— DI + Regular Adam 对比，未在 INDEX
- **GRTX**（Lee et al. 2026，concurrent）—— hardware extension 加速 3DGRT，未在 INDEX

### 11.2 派系 C / D 直接相关下游

- **派系 C 引用关系**：GRay 与派系 C 中 **4DGRT（[2025-liu-4dgrt.md](2025-liu-4dgrt.md)）直接同源**（4DGRT 是 3DGRT 在 4D 推广）—— **GRay 是 4DGRT 桌面 ray tracing 加速版**。
- **派系 D 引用关系**：与 **GS-NFS（[2026-ghosh-gs-nfs.md](2026-ghosh-gs-nfs.md)）**、**Lumina（[2025-feng-lumina.md](2025-feng-lumina.md)）** 共享 "rendering 路径" 主线，但路径完全不同（ray tracing vs streaming vs mobile rasterization）。
- **推测的 1-hop 引用**：4DGRT / 3DGRT / RaySplats / EPBRR 后续工作**很可能引用 GRay 的 DI + PPLL + DHT + Weight-based Pruning + Scale Decay 五件套作为 3DGS ray tracing 的新基线** —— **v2 用 S2 API 自动拉取完整 cited-by 列表**。