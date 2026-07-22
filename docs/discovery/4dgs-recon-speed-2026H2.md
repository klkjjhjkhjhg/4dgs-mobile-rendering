# 4DGS 重建速度排行榜（2026 H2）

> **口径**：主榜只收动态 NeRF / 4DGS / Deformable-GS；静态 3DGS 仅置于附录对照，不参与名次。按论文明确给出的单场景（或论文定义的单次重建/GOP）秒数升序；无法换算者置底且不授予名次。`Peak FPS` 只描述训练后渲染，**禁止跨数据集横比**。
>
> **证据纪律**：`paper note Lx–Ly` 是本仓 paper note 行号；带 paper Table/§/page 的数字视为 note 中已直引。凡由 note 推算、转引或缺少 PDF 二次核验者均明确标 **[未二次核]**。GPU 未披露时仍填"未披露"，不猜型号。
>
> **链接来源**：每行「链接」列取自该 paper note §0.5 元数据段（`arxiv-id` → arxiv 主页、`homepage` → 项目主页、`github` → 源码）。`venue` 用 italic 标出接收状态（CVPR 2024 Oral / arXiv preprint / ECCV 2026 under review 等），方便读者快速判断"成熟度"。无 `homepage`/`github` 的论文只标 [arXiv]。

## 1. 总排行榜

| paper | 类 (per-scene opt / feed-forward) | 场景 | GPU | 训练时间 | Peak FPS after train | 链接 | 数据页码 |
|---|---|---|---|---|---|---|
| StreamSTGS (Ke et al., 2025) | per-scene opt / streaming GOP | MeetRoom，12 cams，1280×720；按 GOP/论文 Train(s) 口径 | 1× RTX A6000 | **29 s / GOP** | **126 FPS**（MeetRoom） | note L73–85；paper Table 2 / §5 implementation | [arXiv](https://arxiv.org/abs/2511.06046) · _CVPR 2025_ |
| StreamSTGS (Ke et al., 2025) | per-scene opt / streaming GOP | N3DV，18–21 cams，1352×1014；按 GOP/论文 Train(s) 口径 | 1× RTX A6000 | **表中 Ours 的 Train(s) 需回看原表行；note 摘要未完整显示**，不排序 | **100 FPS**（N3DV） | note L53–70、L85–88、L102；paper Table 1 / §5 | [arXiv](https://arxiv.org/abs/2511.06046) · _CVPR 2025_ |
| L2D2-GS (Song et al., 2026) | **feed-forward** dynamic | PandaSet dynamic urban，一次重建 | **8× NVIDIA H20** | **98 s** | 未报告 | note L80–101、L155–159；paper p.6 / Table II p.8 | [arXiv](https://arxiv.org/abs/2606.29374) · _arXiv preprint (2026)_ |
| SpeeDe3DGS (Tu et al., 2025) | per-scene opt（DeformableGS） | NeRF-DS 7 scenes 平均 | GPU 型号在该表段未明确；note 仅概括 RTX 3090 / A5000 | **625.48 s**（TSP+TSS+GroupFlow） | **505.60 FPS**（同 NeRF-DS） | note L79–90；paper Table 1 p.7 | [arXiv](https://arxiv.org/abs/2506.07917) · _CVPR 2025_ |
| 4DGS (Wu et al., 2024) | per-scene opt | D-NeRF synthetic，800×800 | **RTX 3090** | **480 s（8 min）** | **82 FPS**（约 30K GS 时约 90 FPS） | note L46–59、L104–112；paper Table 1 / Fig.9 | [arXiv](https://arxiv.org/abs/2310.08528) · [homepage](https://guanjunwu.github.io/4dgs/) · [code](https://github.com/hustvl/4DGaussians) · _CVPR 2024_ |
| 4DGS (Wu et al., 2024) | per-scene opt | HyperNeRF vrig，960×540 | **RTX 3090** | **1,800 s（30 min）** | **34 FPS** | note L61–72、L107–112；paper Table 2 | [arXiv](https://arxiv.org/abs/2310.08528) · [homepage](https://guanjunwu.github.io/4dgs/) · [code](https://github.com/hustvl/4DGaussians) · _CVPR 2024_ |
| AirGS (Wang et al., 2025) | per-scene opt / streaming | FVV benchmark（abstract 未给数据集名） | **RTX 3090 [未二次核]** | **1,200–2,400 s（20–40 min）[未二次核]**；只由“6×”与假定 2–4 h 基线推算 | 未报告 | note L44–50、L88–101；abstract + note 推测 L90 | [arXiv](https://arxiv.org/abs/2512.20943) · _SIGGRAPH 2025_ |
| 4DGS (Wu et al., 2024) | per-scene opt | Neu3D，1352×1014 | **RTX 3090** | **2,400 s（40 min）** | **30 FPS** | note L73–85、L107–118；paper Table 3 | [arXiv](https://arxiv.org/abs/2310.08528) · [homepage](https://guanjunwu.github.io/4dgs/) · [code](https://github.com/hustvl/4DGaussians) · _CVPR 2024_ |
| SpeeDe3DGS (Tu et al., 2025) | per-scene opt（4DGS variant） | MonoDyGauBench 50 scenes 平均 | GPU 型号在该表段未明确；note 概括 RTX 3090 / A5000 | **4,176.49 s**（4DGS Pruning+GroupFlow） | **290.21 FPS**（同 benchmark） | note L92–110；paper Table 2 p.8 | [arXiv](https://arxiv.org/abs/2506.07917) · _CVPR 2025_ |
| MVFusion-GS (Hu et al., 2026) | per-scene opt | Neu3D，7 scenes mean | **RTX 4090**（efficiency 表） | **8,136 s（2.26 h）** | **62.7 FPS** | note L133–137；paper Table 11 p.24 | [arXiv](https://arxiv.org/abs/2607.01578) · [code](https://github.com/toseeai-com/MVFusion-GS) · _arXiv preprint (2026)_ |
| D-NeRF (Pumarola et al., 2021) | per-scene opt / NeRF baseline | Stand Up，单目动态 | **1× GTX 1080** | **约 172,800 s（2 days）** | 未报告 | note L15–23；paper §5.2 | [arXiv](https://arxiv.org/abs/2011.13961) · [code](https://github.com/albertpumarola/D-NeRF) · _CVPR 2021_ |
| Deformable 3DGS (Yang et al., 2023) | per-scene opt | D-NeRF / NeRF-DS / HyperNeRF | **1× RTX 3090** | **40K iterations；分钟数未披露** | **70 FPS**（D-NeRF，跨源转引 **[未二次核]**）；或 >30 FPS when <250K GS | note L59–64、L80–101；paper §4.1–4.2，转引 4DGS-1K Table 2 | [arXiv](https://arxiv.org/abs/2503.16422) · [homepage](https://ingra14m.github.io/Deformable-3D-Gaussians/) · [code](https://github.com/ingra14m/Deformable-3D-Gaussians) · _CVPR 2024_ |
| Sparse4DGS (Shi et al., 2025) | per-scene opt | NeRF-Synthetic / HyperNeRF / NeRF-DS / iPhone-4D sparse-frame | **未披露** | **未在 abstract 拿到** | 未在 abstract 拿到 | note L46–52、L86–92；abstract | [arXiv](https://arxiv.org/abs/2511.07122) · [homepage](https://changyueshi.github.io/Sparse4DGS/) · _arXiv pre-print (2025-11)_ |
| RetimeGS (Wang et al., 2026) | per-scene opt | fast motion / non-rigid / occlusion，continuous-time | **未披露** | **未在 abstract 拿到** | 未在 abstract 拿到 | note L59–68、L82–87；abstract | [arXiv](https://arxiv.org/abs/2603.13783) · [homepage](https://william-wang2.github.io/RetimeGS/) · _CVPR 2026 Oral_ |
| GaussianFluent (Huang et al., 2026) | per-scene opt / simulation（边界项） | mixed-material dynamic simulation | **未披露** | abstract 仅称 “high speed”，**无数字** | 未给具体 FPS | note L58–69、L83–87；abstract | [arXiv](https://arxiv.org/abs/2601.09265) · [homepage](https://hb-pencil-zero.github.io/GaussianFluent/) · _CVPR 2026 Oral_ |

### 排名说明

1. StreamSTGS 的 29 s 是 **GOP 训练口径**，不是完整长序列从零训练；因此与整场 4DGS 的 480 s、L2D2-GS 的一次 feed-forward 98 s只可并列展示，不可无条件称“全场最快”。
2. L2D2-GS 的 98 s 用 **8×H20**，且论文说明仍含 24 timesteps iterative process；它不是手机端一次前向延迟。其模型预训练成本也不在 98 s 内。
3. SpeeDe3DGS 的 625.48 s 是 NeRF-DS 上 DeformableGS 三件套；4DGS variant 在 MonoDyGauBench 是 4,176.49 s。两者数据集和基座不同，不能互换。
4. AirGS 的 20–40 min 是 note 由“6×”推理，已经降级为 **[未二次核]**，不用于“最快”硬结论。

## 2. 分场景子表

### A. 单目动态场景（室内小）

| paper | 场景实例 | GPU | 训练/重建时间 | Peak FPS | 链接 | 数据页码 |
|---|---|---|---|---|---|
| D-NeRF | Stand Up，单目动态 | GTX 1080 | 约 2 days | 未报告 | note L15–23；paper §5.2 | [arXiv](https://arxiv.org/abs/2011.13961) · [code](https://github.com/albertpumarola/D-NeRF) · _CVPR 2021_ |
| HyperNeRF（作为 4DGS Table 2 baseline） | HyperNeRF vrig，960×540 | 论文表未给 GPU；4DGS 实验平台 RTX 3090 | **32 h** | **<1 FPS** | `2024-wu-4dgs.md` L61–71；paper Table 2 | [arXiv](https://arxiv.org/abs/2111.01226) · [homepage](https://hypernerf.github.io/) · _SIGGRAPH Asia 2021_ |
| Deformable 3DGS | D-NeRF synthetic / NeRF-DS | RTX 3090 | 40K iter；分钟数未披露 | 70 FPS（D-NeRF 跨源转引 **[未二次核]**）；<250K GS 时 >30 FPS | note L59–64、L80–101；paper §4.1–4.2 | [arXiv](https://arxiv.org/abs/2503.16422) · [homepage](https://ingra14m.github.io/Deformable-3D-Gaussians/) · [code](https://github.com/ingra14m/Deformable-3D-Gaussians) · _CVPR 2024_ |
| 4DGS | D-NeRF synthetic | RTX 3090 | **8 min / scene** | **82 FPS** | note L46–59、L107–112；paper Table 1 | [arXiv](https://arxiv.org/abs/2310.08528) · [homepage](https://guanjunwu.github.io/4dgs/) · [code](https://github.com/hustvl/4DGaussians) · _CVPR 2024_ |
| 4DGS | HyperNeRF vrig | RTX 3090 | **30 min / scene** | **34 FPS** | note L61–72、L107–112；paper Table 2 | [arXiv](https://arxiv.org/abs/2310.08528) · [homepage](https://guanjunwu.github.io/4dgs/) · [code](https://github.com/hustvl/4DGaussians) · _CVPR 2024_ |
| Sparse4DGS | NeRF-Synthetic / HyperNeRF / NeRF-DS / iPhone-4D sparse frames | 未披露 | 未在 abstract 拿到 | 未在 abstract 拿到 | note L46–52、L86–92；abstract | [arXiv](https://arxiv.org/abs/2511.07122) · [homepage](https://changyueshi.github.io/Sparse4DGS/) · _arXiv pre-print (2025-11)_ |
| AirGS | FVV benchmark（数据集名未披露） | RTX 3090 **[未二次核]** | **20–40 min [未二次核]** | 未报告 | note L44–50、L88–101；abstract + note L90 推算 | [arXiv](https://arxiv.org/abs/2512.20943) · _SIGGRAPH 2025_ |
| GaussianFluent | mixed-material fracture / slicing simulation | 未披露 | abstract 未给 | abstract 仅称 high speed，无数字 | note L58–69、L83–87；abstract | [arXiv](https://arxiv.org/abs/2601.09265) · [homepage](https://hb-pencil-zero.github.io/GaussianFluent/) · _CVPR 2026 Oral_ |

**本 split 解释**：只有同一 D-NeRF/HyperNeRF 行才能讨论速度变化。例如 4DGS 在 D-NeRF 是 8 min/82 FPS，而 D-NeRF 自身 Stand Up 为约 2 days，但硬件和具体场景仍不同；这说明数量级演进，不构成严格公平竞赛。Sparse4DGS 的目标是稀疏帧质量，不应因未报时间被判慢。

### B. 复杂 + driving（户外大型 / 多相机）

| paper | 场景实例 | GPU | 训练/重建时间 | Peak FPS | 链接 | 数据页码 |
|---|---|---|---|---|---|
| L2D2-GS | PandaSet dynamic urban；Waymo zero-shot | **8× H20** | **98 s**（PandaSet reconstruction） | 未报告 | note L80–101、L108–118；paper p.6 / Table II p.8 | [arXiv](https://arxiv.org/abs/2606.29374) · _arXiv preprint (2026)_ |
| StreamSTGS | MeetRoom，12 cams，1280×720 | **1× RTX A6000** | **29 s / GOP** | **126 FPS** | note L73–88；paper Table 2 / §5 | [arXiv](https://arxiv.org/abs/2511.06046) · _CVPR 2025_ |
| StreamSTGS | N3DV，18–21 cams，1352×1014 | **1× RTX A6000** | note 中 Ours Train(s) 行未完整留存；不填推测值 | **100 FPS** | note L53–70、L84–88、L102；paper Table 1 / §5 | [arXiv](https://arxiv.org/abs/2511.06046) · _CVPR 2025_ |
| MVFusion-GS | Neu3D，20 synchronized cameras，7 scenes | **RTX 4090**（efficiency）；训练 stage 段另称 RTX 3090，口径有冲突 | **2.26 h** | **62.7 FPS** | note L84–90、L133–137；paper Table 11 p.24 | [arXiv](https://arxiv.org/abs/2607.01578) · [code](https://github.com/toseeai-com/MVFusion-GS) · _arXiv preprint (2026)_ |

**本 split 解释**：StreamSTGS 29 s 是流式 GOP 更新，L2D2-GS 98 s 是 8×H20 上的场景重建，MVFusion-GS 2.26 h 是 Neu3D per-scene optimization。输入规模、输出目标与 GPU 数量均不同，排序只陈列 wall-clock，不声称算法单卡效率等价。

### C. Feed-forward 4DGS（独立赛道）

| paper | 场景实例 | GPU | 训练/重建时间 | Peak FPS | 链接 | 数据页码 |
|---|---|---|---|---|---|
| L2D2-GS | PandaSet dynamic urban | **8× NVIDIA H20** | **98 s**；不含通用模型预训练成本 | 未报告 | note L80–105、L155–159；paper p.6 / Table II p.8 | [arXiv](https://arxiv.org/abs/2606.29374) · _arXiv preprint (2026)_ |
| G3R（L2D2-GS 同表 dynamic baseline） | PandaSet | **未披露** | **60 s** | 未报告 | `2026-song-l2d2-gs.md` L93–101；paper Table II p.8 | _PandaSet baseline in L2D2-GS Table II_ |
| G3R*（复现配置） | PandaSet | **8×H20 实验环境，但方法逐项 GPU 未明示** | **75 s** | 未报告 | note L80–101；paper p.6 / Table II p.8 | [arXiv](https://arxiv.org/abs/2606.29374) · _L2D2-GS Table II 同表复现行_ |
| ZipSplat（静态同类，仅方法对照，**不进 4DGS 主榜**） | DL3DV / RealEstate10K，252×252 | **未披露** | feed-forward“秒级”，**无精确秒数 [未二次核]**；TTO 时间未给 | FPS 未报告 | `2026-veicht-zipsplat.md` L91–99、L124–132；paper §4 / Table 1 | [arXiv](https://arxiv.org/abs/2606.05102) · _arXiv preprint (2026-06)_ |
| FCGS（静态同类，仅方法对照，**不进 4DGS 主榜**） | 现成 3DGS compression | **未披露** | minutes → seconds，**无精确秒数** | 未报告 | `2024-chen-fcgs.md` L40–55、L83–89；abstract | [arXiv](https://arxiv.org/abs/2410.08017) · [code](https://github.com/YihangChen-ee/FCGS) · _CVPR 2024_ |

**本 split 解释**：若只看 PandaSet 同表，G3R 的 60 s 比 L2D2-GS 98 s 短，但 L2D2-GS 以 1.2M GS 达到 24.19 dB，G3R 为 3M GS / 23.15 dB；这正是速度、质量与表示规模的三方权衡。ZipSplat/FCGS 是静态先例，仅证明 feed-forward 压缩或重建思路，不是动态榜参赛者。

## 3. 讨论

### 3.1 当前最快重建速度

在可核数字中，per-scene/streaming 赛道最短是 StreamSTGS **29 s/GOP**（MeetRoom, A6000），限制是它不是完整序列从零训练；完整小场景 per-scene opt 可核最短为 4DGS **480 s**（D-NeRF, RTX 3090）。feed-forward 动态主方法为 L2D2-GS **98 s**（8×H20），但不含预训练且未报 FPS。

### 3.2 训练时间 vs Peak FPS 是否 trade-off

不存在稳定单调 trade-off。4DGS 在 D-NeRF 同时做到 **8 min / 82 FPS**，SpeeDe3DGS 在 NeRF-DS 为 **625.48 s / 505.60 FPS**，属于双轴都好的离群点；MVFusion-GS 则为质量和紧凑性牺牲速度：2.1→2.26 h、71→62.7 FPS。FPS 仅限各自数据集内解读。

### 3.3 对 Snap 8 Gen 4 on-device spec 的借鉴

优先借 SpeeDe3DGS 的 TSP/TSS 与 GroupFlow：跨帧剪枝、时间扰动、共享 SE(3) 可消除 per-Gaussian MLP；借 StreamSTGS 的训练时 Transformer、推理时移除及 GOP 更新；借 L2D2-GS 的 compact densification policy。静态 Flux-GS 的 baked MLP、多视角 alpha 剪枝和 WebGL async-sort也值得移植，但不能把其 147 FPS 当作 4DGS 手机指标。

## 4. 静态 3DGS 重建速度对照（不参与主榜）

| paper | 场景 / GPU | 时间 | Peak FPS | 链接 | 数据页码 |
|---|---|---|---|---|
| 3DGS (Kerbl et al., 2023) | Mip-NeRF 360 / RTX A6000 | 35–45 min | ≥30 FPS @1080p | note L15–20；paper Table 1 p.7 | [arXiv](https://arxiv.org/abs/2308.04079) · [code](https://github.com/graphdeco-inria/gaussian-splatting) · _SIGGRAPH 2023_ |
| FCGS (Chen et al., 2024) | GPU 未披露 | minutes → seconds（无精确值） | 未报告 | note L40–55；abstract | [arXiv](https://arxiv.org/abs/2410.08017) · [code](https://github.com/YihangChen-ee/FCGS) · _CVPR 2024_ |
| ACE-GS (Zhao et al., 2026) | Mip-NeRF 360 / **GPU 未披露** | **5m30s**（vs 3DGS 24m43s） | **745.6 FPS** | note L73–87；paper Table 1 p.9 | [arXiv](https://arxiv.org/abs/2606.21244) · _arXiv preprint (2026-03)_ |
| Flux-GS (Du et al., 2026) | Mip-NeRF 360 Indoor / training GPU 未披露；render Snap 8 Gen 3 | **11 min**（vs Mobile-GS 86 min） | **147 FPS mobile** | note L74–100；paper Table 1 | [arXiv](https://arxiv.org/abs/2606.30017) · [homepage](https://xiaobiaodu.github.io/flux-gs-project/) · _ECCV 2026 (under review)_ |
| ZipSplat (Veicht et al., 2026) | DL3DV / GPU 未披露 | feed-forward 秒级但无精确值 **[未二次核]** | 未报告 | note L91–99、L124–132；paper §4 | [arXiv](https://arxiv.org/abs/2606.05102) · _arXiv preprint (2026-06)_ |
| GRay (Poirier-Ginter et al., 2026) | 13 standard scenes / GPU 未披露 | **1:58 init + 5:40 opt = 7:38 total**；prompt 所给 3:42 opt 与 note 冲突，采用 paper-note Fig.1 | **248 FPS** | note L70–83；paper Fig.1 p.1 | [arXiv](https://arxiv.org/abs/2606.30869) · [code](https://repo-sam.inria.fr/nerphys/gray) · _ACM Proc. CGIT 2026_ |
| SpeeDe3DGS 静态/高速阵列类概括 | GPU 未在相应概括处明确 | **9.5 h vs 24 h [未二次核]**（由 note 项目解读，不作本报告实测点） | 不适用 | `2025-tu-speede3dgs.md` L132–137；note 推理 | [arXiv](https://arxiv.org/abs/2506.07917) · _CVPR 2025_ |
| EvoGS | Mip-360 L1 / desktop GPU（型号未披露） | **未在 abstract 拿到** | 未报告 | note L91–96；abstract | [arXiv](https://arxiv.org/abs/2606.07179) · _arXiv preprint (2026-05)_ |
| VEDAL | Mip-360 / GPU 未披露 | **未在 abstract 拿到** | 185 FPS | `2026-li-vedal.md` L60–72、L88–92；paper Table 1 | [arXiv](https://arxiv.org/abs/2606.02346) · _arXiv preprint (2026-04)_ |

## 5. 缺失值与复核队列

- **必须二次核**：AirGS 的 20–40 min 与 RTX 3090（note 明示推测）；ZipSplat“秒级”没有精确 wall-clock；SpeeDe3DGS“9.5 h vs 24 h”是项目层解释；Deformable 3DGS 的 70 FPS 为跨源转引。
- **未在 abstract / note 拿到训练时间**：Sparse4DGS、RetimeGS、GaussianFluent、EvoGS、VEDAL；这些条目不参与最快结论。
- **GPU 未披露，禁止猜测**：Sparse4DGS、RetimeGS、GaussianFluent、G3R 逐方法配置及多数静态对照。ACE-GS note 对 RTX 4090 仅作推测，因此表中保留“未披露”。
- **口径冲突**：MVFusion-GS 方法设置段写单 RTX 3090，efficiency Table 11 写 RTX 4090；本榜时间/FPS采用同一 efficiency 表的 RTX 4090，并保留冲突说明。
- **GRay 时间冲突**：任务摘要给 1:58 + 3:42 = 5:40，但 paper note Fig.1 明确是 init 1:58、opt 5:40；报告采用 note/PDF anchor 的 **总计 7:38**，不把摘要误算写入排行榜。
