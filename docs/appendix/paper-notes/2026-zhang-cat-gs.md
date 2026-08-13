# CaT-GS: Efficient 3DGS Rendering for Large-Scale Scenes with Inter-frame Caching and Tile Scheduling

## 0. 基本信息
- 作者: Tingjia Zhang¹*, Bo Chen², Shengzhong Liu¹†, Fan Wu¹, Guihai Chen¹ [PDF p.1]
- 单位: ¹Shanghai Jiao Tong University, ²University of Illinois Urbana-Champaign [PDF p.1]
- 年份: 2026 (arXiv preprint 提交 20 Jul 2026) [PDF p.1]
- 会议: CVPR 2026 (main)
- arxiv-id: 2607.17842
- GitHub: 未在 PDF 披露 (论文仅声明 UAV City Dataset "will be open-sourced in the future" / "in recent months"，代码仓库未给链接) [PDF p.6, p.11]
- 项目主页: 未在 PDF 披露
- 代码许可: 未在 PDF 披露

## 0.5 元数据
- venue: CVPR 2026 (main)
- arxiv-id: 2607.17842
- status: 收录
- 收录日期: 2026-08-10
- 收录来源: 人工 (本次 9 篇批)
- 评级: T1 (核心 4DGS 表示 / 渲染加速)
- survey_section: 5
- faction: C

## 1. 一句话总结
CaT-GS 提出一个面向大型 3DGS 场景流式渲染的 pipeline，通过 speculative multi-frame pre-processing、inter-frame caching (frustum + sort) 与 load-aware tile-level task splitting + 专用 CUDA kernel 三个机制，对相邻帧复用 pre-processing 结果并把重负载 tile 切分到多 SM 上并行执行，从而把渲染速度提升至原始 3DGS 的最多 10×、先前 SOTA 的最多 70% [PDF p.1 §Abstract]。

## 2. 摘要 (核心 3 段)
- 问题: 3DGS 在大型场景 (UAV 城市场景、虚拟世界) 中 tile-based rasterization 计算负载过大，渲染延迟上升。已有加速方法要么要 retrain (如 ADR-GS [32])，要么只优化 rasterization 单阶段 (Flash-GS [5])，忽略 (1) inter-frame pre-processing 冗余 (frustum culling / sorting 在视角连续时结果几乎一致)、(2) viewpoint redundancy、(3) tile 负载不均导致的 GPU 低利用率 (论文称 10% 的 tile 可能承担 >50% 的计算负载) [PDF p.1-3 §1]。
- 方法: 流水线把连续帧按 group 处理，第一帧为 key-frame、后续为 sub-frame。Key-frame 走 viewpoint-speculative pre-processing：通过相机运动预测 (R,T → R',T') 计算像素级 motion vector (∆u,∆v)，对每个 Gaussian 构造 trace (两条半椭圆 A、B + 两条平行线 C、D 围成的扫掠区域)，用 fine-grained intersection 判断哪些 tile 必须在 batch 内保留；sub-frame 通过 frustum caching + sort caching 直接复用 key-frame 结果，仅重做 feature computing。同时提出 load-aware task splitting：把 Gaussian 数 >2l (l = L/t) 的重 tile 切到接近 l 大小的子块，按 alpha-blending 数学 (Eq.7-8) 分割 R/A 累加，多个 SM 并行处理 [PDF p.3-6 §3.2-3.4]。
- 结果: 在 RTX 5090 + Ryzen 9 9950X 上，10 个模型 (含 5 个自建 UAV-1..UAV-5) 上：vanilla 3DGS 在 Truck 63.4 FPS / UAV-2 仅 23.2 FPS；CaT-GS 在 Truck 达到 736.5 FPS (对 Flash-GS 提升 54%)、UAV-1 241.5 FPS (提升 83%)；UAV 5 个大场景全部 >200 FPS，其他 baseline 在 UAV 上达不到 120 FPS。渲染质量 (PSNR/SSIM) key-frame 与 Flash-GS 一致，sub-frame 略有下降但与 vanilla 3DGS 几乎无差 (Truck 28.16/0.852 vs 3DGS 28.21/0.858)；对原始 3DGS 整体加速可达 10×，对先前 SOTA 可达 70% [PDF p.7-8 §5.2-5.3, Table 1/2]。

## 3. 派系分类
- 派系 C (核心 3DGS 表示 / 渲染加速)：直接归属。论文核心是 vanilla 3DGS 渲染 pipeline 的软件加速 (3K 行 CUDA + Python)，未涉及新表示或 4D / dynamic / dynamic-4D 维度。
- 不属于 A (4DGS 动态表示)、B (Gaussian 几何/语义增强)、D (硬件/SoC 端优化，注：方法在 RTX 5090 GPU 上跑，但工作重心是 software pipeline 优化，不强调 ARM/mobile/SoC)、E (应用层)。

## 4. 方法 (核心机制 5 条)
1. **Speculative multi-frame pre-processing** (key-frame 专用)：用仿射变换 (Eq.3) 把相机运动 (R,T→R',T') 转成每个 Gaussian 像素级 motion vector (∆u,∆v)，构造 Gaussian trace (两条半椭圆 + 两条平行线，Eq.4-6)，以 expanded window + 中心-边界测试判定 tile 是否必须在 batch 内保留，避免 sub-frame 缺 Gaussian [PDF p.3-5 §3.2]。
2. **Motion-adaptive adjustment**：设目标帧率 Ftarget=120、初始窗口 Winitial=4、tile 大小 l、阈值 d=0.4 (深度 > d 才参与)；若 (∆u²+∆v²)^½ > l 则把窗口缩为 ⌊Winitial·l/M⌋；极端情况退化为 1 (跳过 speculation) [PDF p.5 §3.2.3, p.6 §4]。
3. **Inter-frame caching**：
   - **Frustum caching**：key-frame 阶段已通过 trace-based 判断锁定可见 Gaussian 子集，存 hash index；sub-frame 直接复用，跳过 culling 全量遍历 [PDF p.5 §3.3.1]。
   - **Sort caching**：key-frame 排序并 list 生成后 sub-frame 直接复用，跳过 sorting + tile intersection + key-duplication [PDF p.5 §3.3.2]。
4. **Load-aware tile-level task splitting**：tile 内 Gaussian 数 > 2l 视为重 tile，切成接近 l 大小的子任务（Eq.7-8 把 alpha blending 重写为切片形式，每块独立算 C_k 与 A_k，最后合并），多 SM 并行处理，避免重 tile 在单个 SM 上 stall [PDF p.5-6 §3.4]。
5. **Split render kernel (CUDA)**：实现于 PyTorch CUDA extension；在 Tile-Identify 阶段用 Algorithm 1 (Identify Tile Ranges) 写 ranges 数组与 label 数组；额外分块提高 early-termination 阈值，并把第一块设为 task size−split_num·k (而非 k) 以减少多余分块开销；总 task 数写入 task count [PDF p.6 §4, p.11-12 §7.1.2 / Algorithm 1]。

## 5. 实验结果
**平台**：NVIDIA RTX 5090 + AMD Ryzen 9 9950X，Ubuntu 24.04；分辨率 1920×1080；tile 16×16；Ftarget=120 FPS；trace 在 SIBR Viewer 上交互采集，每个模型 10 条轨迹 × 2000 帧 [PDF p.6 §5.1]。

**Table 1 — Avg FPS (PDF p.7)：**
- Truck (2.54M GS)：3DGS 63.4 → Flash-GS 478.3 → CaT-GS **736.5** (↑54% vs SOTA) [PDF p.7 Table 1]
- Train (1.03M GS)：3DGS 89.4 → Flash-GS 528.3 → CaT-GS **892.2** (↑68%) [PDF p.7 Table 1]
- Counter (1.22M GS)：3DGS 122.3 → Flash-GS 606.3 → CaT-GS **907.5** (↑49%) [PDF p.7 Table 1]
- Garden (4.23M GS)：3DGS 92.6 → Flash-GS 201.1 → CaT-GS **295.5** (↑46%) [PDF p.7 Table 1]
- Playroom (2.55M GS)：3DGS 68.1 → Flash-GS 634.2 → CaT-GS **922.3** (↑45%) [PDF p.7 Table 1]
- UAV-1 (6.90M GS)：3DGS 25.2 → Flash-GS 129.2 → CaT-GS **241.5** (↑83%) [PDF p.7 Table 1]
- UAV-2 (7.19M GS)：3DGS 23.2 → Flash-GS 113.1 → CaT-GS **202.5** (↑78%) [PDF p.7 Table 1]
- UAV-3 (5.93M GS)：3DGS 54.3 → Flash-GS 241.1 → CaT-GS **378.5** (↑64%) [PDF p.7 Table 1]
- UAV-4 (8.32M GS)：3DGS 47.2 → Flash-GS 167.3 → CaT-GS **272.1** (↑62%) [PDF p.7 Table 1]
- UAV-5 (7.40M GS)：3DGS 36.1 → Flash-GS 132.3 → CaT-GS **217.3** (↑65%) [PDF p.7 Table 1]
- 总结句：UAV 5 个大场景 CaT-GS 全部 >200 FPS，其他 baseline 在 UAV 上不能保证 120 FPS [PDF p.7 §5.2]。

**Table 2 — 渲染质量 (PSNR / SSIM, PDF p.7)：**
- Truck: 3DGS 28.21 / 0.858; ADR-GS* 26.50 / 0.824 (retrain 退化); Flash-GS 28.19 / 0.856; Ours-Key 28.19 / 0.856; Ours-Sub 28.16 / 0.852 [PDF p.7 Table 2]
- Train: 3DGS 25.82 / 0.872; ADR-GS* 23.92 / 0.768; Flash-GS 25.78 / 0.869; Ours-Key 25.78 / 0.869; Ours-Sub 25.74 / 0.867 [PDF p.7 Table 2]
- UAV-1: 3DGS 30.15 / 0.935; ADR-GS* 29.12 / 0.883; Flash-GS 30.09 / 0.931; Ours-Key 30.09 / 0.931; Ours-Sub 30.05 / 0.926 [PDF p.7 Table 2]
- UAV-2/3/4/5 数值见 PDF p.7 Table 2。

**Table 3 — 消融 (AvgFPS, PDF p.8)：**
- Garden: Full 295.5 / w-cache 242.4 / w-split 279.4 [PDF p.8 Table 3]
- Truck: Full 736.5 / w-cache 494.4 / w-split 672.3 [PDF p.8 Table 3]
- Playroom: Full 922.3 / w-cache 654.8 / w-split 840.6 [PDF p.8 Table 3]
- UAV-1: Full 241.5 / w-cache 155.3 / w-split 210.3 [PDF p.8 Table 3]
- UAV-2: Full 202.5 / w-cache 133.2 / w-split 178.4 [PDF p.8 Table 3]
- UAV-3: Full 378.5 / w-cache 249.6 / w-split 337.6 [PDF p.8 Table 3]
- Inter-frame caching 提升最多 80%；load-aware task splitting 整体提升 >10% [PDF p.8 §5.4]。

**Table 4 — Stage speedup vs 3DGS (PDF p.8)：**
- Flash-GS: pre-proc 3.2× / sort 3.3× / tile-id 1.7× / raster 4.2× [PDF p.8 Table 4]
- Ours-key: pre-proc 3.1× / sort 2.9× / tile-id 1.3× / raster 5.3× [PDF p.8 Table 4]
- Ours-sub: pre-proc 6.8× / sort 0× (跳过) / tile-id 0× (跳过) / raster 5.3× [PDF p.8 Table 4]
- 平均 sorting stage 加速达 7.2× (因为 sub-frame 完全跳过) [PDF p.8 §5.4]。

**Table 5 — Render list length (×10³, PDF p.8)：**
- Garden: 3DGS 18,593 / Flash-GS 6,682 / Ours-key 7,032 / Ours-sub 7,032 [PDF p.8 Table 5]
- Truck: 3DGS 18,969 / Flash-GS 4,124 / Ours-key 4,289 / Ours-sub 4,289 [PDF p.8 Table 5]
- Playroom: 3DGS 22,550 / Flash-GS 3,818 / Ours-key 4,182 / Ours-sub 4,182 [PDF p.8 Table 5]
- UAV-1: 3DGS 37,821 / Flash-GS 10,766 / Ours-key 11,222 / Ours-sub 11,222 [PDF p.8 Table 5]
- UAV-2: 3DGS 52,336 / Flash-GS 12,101 / Ours-key 12,886 / Ours-sub 12,886 [PDF p.8 Table 5]
- UAV-3: 3DGS 34,532 / Flash-GS 8,416 / Ours-key 8,628 / Ours-sub 8,628 [PDF p.8 Table 5]
- Speculation 仅使列表增长约 10% [PDF p.8 §5.4]。

**Table 6 — Speculation window 影响 (UAV-1/2, PDF p.12 补充)：**
- UAV-1: Flash-GS 10,766×10³; None/W-2/W-4/W-8/W-16: list 10,766 / 10,982 / 11,222 / 15,482 / 25,934; max latency(ms) 7.7 / 6.3 / 6.4 / 6.6 / 9.1 / 14.1 [PDF p.12 Table 6]
- UAV-2: list 12,101 / 12,101 / 12,382 / 12,886 / 15,926 / 24,621; max latency 8.6 / 7.1 / 7.2 / 7.5 / 10.9 / 13.4 [PDF p.12 Table 6]
- 论文最终选 Winitial=4 (Table 6 注：W-4 是 full CaT-GS) [PDF p.6 §4]。

**Table 7 — 与 Compact-3DGS pruning 结合 (PDF p.12)：**
- UAV-1/-2/-3 (原始): 3DGS 25.2 / 23.2 / 54.3 FPS；Flash-GS 129.2 / 113.1 / 241.1；Ours 241.5 / 202.5 / 378.5 [PDF p.12 Table 7]
- UAV-1P/-2P/-3P (pruned, size 2.67M/3.27M/2.24M): 3DGS 49.2 / 44.6 / 73.2；Flash-GS 296.6 / 278.2 / 436.9；Ours 489.4 / 448.3 / 746.2 [PDF p.12 Table 7]

## 6. 相关性评估
**5 分 (用户认定)** — 详细分析：
- 论文主旨是 3DGS 渲染 pipeline 软件加速 (frustum + sort + rasterization 三阶段全面优化)，与本项目核心研究方向 (4DGS / 移动端实时渲染) 直接相关。
- 三类冗余的诊断 (inter-frame redundancy / viewpoint redundancy / tile load imbalance) 是渲染管线优化的通用方法论，可迁移到 4DGS / dynamic-3DGS 渲染场景。
- **Inter-frame caching (frustum + sort) 与 trace-based speculative pre-processing** 是核心创新：对视角连续的高帧率流式渲染非常有效；与本项目"up to 10× speedup over original 3DGS"完全吻合。
- **Load-aware task splitting + split render kernel** 针对大型场景 (>5M Gaussian)，与本项目关心的大规模 / 移动端场景一致。
- 实测场景覆盖自建 UAV City Dataset (16 个真实城市场景，每个 1-2 个 city block，>20,000 m²，约 800 图像 + 30FPS 视频 [PDF p.11 §7.1.1])，可直接迁移到 4DGS 大场景评估。
- 实验平台 RTX 5090 + 1920×1080 / 120FPS 与用户核心需求 (tile scheduling + inter-frame caching) 完全契合，可作为 4DGS 加速的 reference baseline。
- 已知限制：渲染质量 sub-frame 比 key-frame 有小幅 PSNR 退化 (e.g. UAV-1 30.05 vs 30.09)，且 CaT-GS 的 key-frame 排序列表略长于 Flash-GS (Table 5 显示 +5-7% list length)，需要权衡。

## 7. 关键洞察 (派生结论)
1. **Inter-frame redundancy 是被忽视的金矿**：vanilla 3DGS 在 120 FPS 视角连续场景下，pre-processing + sorting 阶段占渲染时间显著比例 (论文 Figure 2 显示部分模型 sorting+pre-process 合计可占 ~60%)；speculative batched pre-processing + caching 是高帧率流式渲染的关键杠杆，远胜单帧压缩/剪枝。
2. **GPU 渲染 stall 来自 tile 负载长尾**：作者观察到 10% 的 tile 可承担 >50% 计算负载 (CDF 极端倾斜)，原因是高斯密度分布与高频细节区域共定位；解决方案不是更复杂调度器，而是把重 tile 物理切小让多 SM 并行 (与早期 NeRF 体素分块思想一致)。
3. **软件 pipeline 优化的边际收益仍大于模型压缩**：论文明确指出剪枝类方法 (CompGS, Taming 3DGS) 需 retrain，部署代价高；Flash-GS / CaT-GS 类方法不改模型直接对推理加速，对实时部署更友好，且在 UAV 大场景 (≥6M GS) 上 CaT-GS 加速优势随模型规模放大而扩大 (从 50% → 60-80% 提升)。
4. **质量-速度权衡被 fine-grained trace 控制**：speculation 窗口默认仅 4 帧，冗余列表增长 ~10% (Table 5)；当窗口过大 (W-16) 时 list length 涨 2-3×、max latency 翻倍 (Table 6)，说明 trace-based intersection + motion-adaptive scheduling 是工程稳定性关键。
5. **与 pruning 互补而非替代**：Table 7 显示 pruning 后的 2-3M 模型仍受益于 CaT-GS 加速 (UAV-3P 746.2 FPS)，证明渲染 pipeline 优化和模型压缩可叠加，未来 4DGS 大模型可考虑 pipeline-optimized + pruned 组合。

## 8. 链接
- arxiv: https://arxiv.org/abs/2607.17842
- PDF (本地): .pdfs/2607.17842.pdf

## 9. 笔记出处
- 抽取者: subagent_A (PDF-only)
- 抽取日期: 2026-08-10
- 未二次核字段: 
  - 所有 FPS / PSNR / SSIM / list length / window size 数据直接抄自 PDF Table 1-7 (p.7-8, p.12)；
  - 所有方法描述直接抄自 PDF §3.2-3.4 (p.3-6)、Algorithm 1 与 §7.1.2 (p.11-12)；
  - 平台/参数 (RTX 5090, 120 FPS, Winitial=4, d=0.4, l=16×16) 直接抄自 PDF §4 与 §5.1 (p.6)；
  - 标题 / 作者 / 单位 / arxiv id / 提交日期抄自 PDF p.1；
  - 未在 PDF 披露字段：GitHub 仓库链接、项目主页、代码许可、UAV 数据集具体公开时间 (论文只说 "in the future" / "in recent months")。