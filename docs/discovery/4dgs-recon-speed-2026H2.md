# 4DGS 重建速度排行榜（2026 H2）

> **口径**：主榜只收动态 NeRF / 4DGS / Deformable-GS；静态 3DGS 仅置于附录对照，不参与名次。按论文明确给出的单场景（或论文定义的单次重建/GOP）秒数升序；无法换算者置底且不授予名次。`Peak FPS` 只描述训练后渲染，**禁止跨数据集横比**。
>
> **证据纪律**：`paper note Lx–Ly` 是本仓 paper note 行号；带 paper Table/§/page 的数字视为 note 中已直引。凡由 note 推算、转引或缺少 PDF 二次核验者均明确标 **[未二次核]**。GPU 未披露时仍填"未披露"，不猜型号。
>
> **链接来源**：每行「链接」列取自该 paper note §0.5 元数据段（`arxiv-id` → arxiv 主页、`homepage` → 项目主页、`github` → 源码）。`venue` 用 italic 标出接收状态（CVPR 2024 Oral / arXiv preprint / ECCV 2026 under review 等），方便读者快速判断"成熟度"。无 `homepage`/`github` 的论文只标 [arXiv]。
>
> **表格格式**：本期用 HTML `<table>` 替代 markdown pipe，是因为数据行较长（含 `[arXiv](...)` 多链接 + paper note Lx-Ly 溯源文字），在 markdown 渲染器横向塞不下会拧麻花。所有 renderer 一致 + 列宽可控。

## 1. 总排行榜

<table>
<thead>
<tr>
<th align="left">paper</th>
<th align="left">类 (per-scene opt / feed-forward)</th>
<th align="left">场景</th>
<th align="left">GPU</th>
<th align="right">训练时间</th>
<th align="right">Peak FPS after train</th>
<th align="left">链接</th>
<th align="left">数据页码</th>
</tr>
</thead>
<tbody>
<tr>
<td>StreamSTGS (Ke et al., 2025)</td>
<td>per-scene opt / streaming GOP</td>
<td>MeetRoom，12 cams，1280×720；按 GOP/论文 Train(s) 口径</td>
<td>1× RTX A6000</td>
<td align="right"><strong>29 s / GOP</strong></td>
<td align="right"><strong>126 FPS</strong>（MeetRoom）</td>
<td>[arXiv](https://arxiv.org/abs/2511.06046) · <em>CVPR 2025</em></td>
<td>note L73–85；paper Table 2 / §5 implementation</td>
</tr>
<tr>
<td>StreamSTGS (Ke et al., 2025)</td>
<td>per-scene opt / streaming GOP</td>
<td>N3DV，18–21 cams，1352×1014；按 GOP/论文 Train(s) 口径</td>
<td>1× RTX A6000</td>
<td align="right">表中 Ours 的 Train(s) 需回看原表行；note 摘要未完整显示，<strong>不排序</strong></td>
<td align="right"><strong>100 FPS</strong>（N3DV）</td>
<td>[arXiv](https://arxiv.org/abs/2511.06046) · <em>CVPR 2025</em></td>
<td>note L53–70、L85–88、L102；paper Table 1 / §5</td>
</tr>
<tr>
<td>L2D2-GS (Song et al., 2026)</td>
<td><strong>feed-forward</strong> dynamic</td>
<td>PandaSet dynamic urban，一次重建</td>
<td><strong>8× NVIDIA H20</strong></td>
<td align="right"><strong>98 s</strong></td>
<td align="right">未报告</td>
<td>[arXiv](https://arxiv.org/abs/2606.29374) · <em>arXiv preprint (2026)</em></td>
<td>note L80–101、L155–159；paper p.6 / Table II p.8</td>
</tr>
<tr>
<td>SpeeDe3DGS (Tu et al., 2025)</td>
<td>per-scene opt（DeformableGS）</td>
<td>NeRF-DS 7 scenes 平均</td>
<td>GPU 型号在该表段未明确；note 仅概括 RTX 3090 / A5000</td>
<td align="right"><strong>625.48 s</strong>（TSP+TSS+GroupFlow）</td>
<td align="right"><strong>505.60 FPS</strong>（同 NeRF-DS）</td>
<td>[arXiv](https://arxiv.org/abs/2506.07917) · <em>CVPR 2025</em></td>
<td>note L79–90；paper Table 1 p.7</td>
</tr>
<tr>
<td>4DGS (Wu et al., 2024)</td>
<td>per-scene opt</td>
<td>D-NeRF synthetic，800×800</td>
<td><strong>RTX 3090</strong></td>
<td align="right"><strong>480 s（8 min）</strong></td>
<td align="right"><strong>82 FPS</strong>（约 30K GS 时约 90 FPS）</td>
<td>[arXiv](https://arxiv.org/abs/2310.08528) · [homepage](https://guanjunwu.github.io/4dgs/) · [code](https://github.com/hustvl/4DGaussians) · <em>CVPR 2024</em></td>
<td>note L46–59、L104–112；paper Table 1 / Fig.9</td>
</tr>
<tr>
<td>4DGS (Wu et al., 2024)</td>
<td>per-scene opt</td>
<td>HyperNeRF vrig，960×540</td>
<td><strong>RTX 3090</strong></td>
<td align="right"><strong>1,800 s（30 min）</strong></td>
<td align="right"><strong>34 FPS</strong></td>
<td>[arXiv](https://arxiv.org/abs/2310.08528) · [homepage](https://guanjunwu.github.io/4dgs/) · [code](https://github.com/hustvl/4DGaussians) · <em>CVPR 2024</em></td>
<td>note L61–72、L107–112；paper Table 2</td>
</tr>
<tr>
<td>AirGS (Wang et al., 2025)</td>
<td>per-scene opt / streaming</td>
<td>FVV benchmark（abstract 未给数据集名）</td>
<td><strong>RTX 3090 [未二次核]</strong></td>
<td align="right"><strong>1,200–2,400 s（20–40 min）[未二次核]</strong>；只由"6×"与假定 2–4 h 基线推算</td>
<td align="right">未报告</td>
<td>[arXiv](https://arxiv.org/abs/2512.20943) · <em>SIGGRAPH 2025</em></td>
<td>note L44–50、L88–101；abstract + note 推测 L90</td>
</tr>
<tr>
<td>4DGS (Wu et al., 2024)</td>
<td>per-scene opt</td>
<td>Neu3D，1352×1014</td>
<td><strong>RTX 3090</strong></td>
<td align="right"><strong>2,400 s（40 min）</strong></td>
<td align="right"><strong>30 FPS</strong></td>
<td>[arXiv](https://arxiv.org/abs/2310.08528) · [homepage](https://guanjunwu.github.io/4dgs/) · [code](https://github.com/hustvl/4DGaussians) · <em>CVPR 2024</em></td>
<td>note L73–85、L107–118；paper Table 3</td>
</tr>
<tr>
<td>SpeeDe3DGS 4DGS variant (Tu et al., 2025)</td>
<td>per-scene opt（4DGS variant）</td>
<td>MonoDyGauBench 50 scenes 平均</td>
<td>GPU 型号在该表段未明确；note 概括 RTX 3090 / A5000</td>
<td align="right"><strong>4,176.49 s</strong>（4DGS Pruning+GroupFlow）</td>
<td align="right"><strong>290.21 FPS</strong>（同 benchmark）</td>
<td>[arXiv](https://arxiv.org/abs/2506.07917) · <em>CVPR 2025</em></td>
<td>note L92–110；paper Table 2 p.8</td>
</tr>
<tr>
<td>MVFusion-GS (Hu et al., 2026)</td>
<td>per-scene opt</td>
<td>Neu3D，7 scenes mean</td>
<td><strong>RTX 4090</strong>（efficiency 表）</td>
<td align="right"><strong>8,136 s（2.26 h）</strong></td>
<td align="right"><strong>62.7 FPS</strong></td>
<td>[arXiv](https://arxiv.org/abs/2607.01578) · [code](https://github.com/toseeai-com/MVFusion-GS) · <em>arXiv preprint (2026)</em></td>
<td>note L133–137；paper Table 11 p.24</td>
</tr>
<tr>
<td>D-NeRF (Pumarola et al., 2021)</td>
<td>per-scene opt / NeRF baseline</td>
<td>Stand Up，单目动态</td>
<td><strong>1× GTX 1080</strong></td>
<td align="right"><strong>约 172,800 s（2 days）</strong></td>
<td align="right">未报告</td>
<td>[arXiv](https://arxiv.org/abs/2011.13961) · [code](https://github.com/albertpumarola/D-NeRF) · <em>CVPR 2021</em></td>
<td>note L15–23；paper §5.2</td>
</tr>
<tr>
<td>Deformable 3DGS (Yang et al., 2023)</td>
<td>per-scene opt</td>
<td>D-NeRF / NeRF-DS / HyperNeRF</td>
<td><strong>1× RTX 3090</strong></td>
<td align="right"><strong>40K iterations；分钟数未披露</strong></td>
<td align="right"><strong>70 FPS</strong>（D-NeRF，跨源转引 <strong>[未二次核]</strong>）；或 >30 FPS when <250K GS</td>
<td>[arXiv](https://arxiv.org/abs/2503.16422) · [homepage](https://ingra14m.github.io/Deformable-3D-Gaussians/) · [code](https://github.com/ingra14m/Deformable-3D-Gaussians) · <em>CVPR 2024</em></td>
<td>note L59–64、L80–101；paper §4.1–4.2，转引 4DGS-1K Table 2</td>
</tr>
<tr>
<td>Sparse4DGS (Shi et al., 2025)</td>
<td>per-scene opt</td>
<td>NeRF-Synthetic / HyperNeRF / NeRF-DS / iPhone-4D sparse-frame</td>
<td><strong>未披露</strong></td>
<td align="right"><strong>未在 abstract 拿到</strong></td>
<td align="right">未在 abstract 拿到</td>
<td>[arXiv](https://arxiv.org/abs/2511.07122) · [homepage](https://changyueshi.github.io/Sparse4DGS/) · <em>arXiv pre-print (2025-11)</em></td>
<td>note L46–52、L86–92；abstract</td>
</tr>
<tr>
<td>RetimeGS (Wang et al., 2026)</td>
<td>per-scene opt</td>
<td>fast motion / non-rigid / occlusion，continuous-time</td>
<td><strong>未披露</strong></td>
<td align="right"><strong>未在 abstract 拿到</strong></td>
<td align="right">未在 abstract 拿到</td>
<td>[arXiv](https://arxiv.org/abs/2603.13783) · [homepage](https://william-wang2.github.io/RetimeGS/) · <em>CVPR 2026 Oral</em></td>
<td>note L59–68、L82–87；abstract</td>
</tr>
<tr>
<td>GaussianFluent (Huang et al., 2026)</td>
<td>per-scene opt / simulation（边界项）</td>
<td>mixed-material dynamic simulation</td>
<td><strong>未披露</strong></td>
<td align="right">abstract 仅称 "high speed"，<strong>无数字</strong></td>
<td align="right">未给具体 FPS</td>
<td>[arXiv](https://arxiv.org/abs/2601.09265) · [homepage](https://hb-pencil-zero.github.io/GaussianFluent/) · <em>CVPR 2026 Oral</em></td>
<td>note L58–69、L83–87；abstract</td>
</tr>
</tbody>
</table>

### 排名说明

1. StreamSTGS 的 29 s 是 **GOP 训练口径**，不是完整长序列从零训练；因此与整场 4DGS 的 480 s、L2D2-GS 的一次 feed-forward 98 s 只可并列展示，不可无条件称"全场最快"。
2. L2D2-GS 的 98 s 用 **8×H20**，且论文说明仍含 24 timesteps iterative process；它不是手机端一次前向延迟。其模型预训练成本也不在 98 s 内。
3. SpeeDe3DGS 的 625.48 s 是 NeRF-DS 上 DeformableGS 三件套；4DGS variant 在 MonoDyGauBench 是 4,176.49 s。两者数据集和基座不同，不能互换。
4. AirGS 的 20–40 min 是 note 由"6×"推理，已经降级为 **[未二次核]**，不用于"最快"硬结论。

## 2. 分场景子表

### A. 单目动态场景（室内小）

<table>
<thead>
<tr>
<th align="left">paper</th>
<th align="left">场景实例</th>
<th align="left">GPU</th>
<th align="right">训练/重建时间</th>
<th align="right">Peak FPS</th>
<th align="left">链接</th>
<th align="left">数据页码</th>
</tr>
</thead>
<tbody>
<tr>
<td>D-NeRF</td>
<td>Stand Up，单目动态</td>
<td>GTX 1080</td>
<td align="right">约 2 days</td>
<td align="right">未报告</td>
<td>[arXiv](https://arxiv.org/abs/2011.13961) · [code](https://github.com/albertpumarola/D-NeRF) · <em>CVPR 2021</em></td>
<td>note L15–23；paper §5.2</td>
</tr>
<tr>
<td>HyperNeRF（作为 4DGS Table 2 baseline）</td>
<td>HyperNeRF vrig，960×540</td>
<td>论文表未给 GPU；4DGS 实验平台 RTX 3090</td>
<td align="right"><strong>32 h</strong></td>
<td align="right"><strong>&lt;1 FPS</strong></td>
<td>[arXiv](https://arxiv.org/abs/2111.01226) · [homepage](https://hypernerf.github.io/) · <em>SIGGRAPH Asia 2021</em></td>
<td><code>2024-wu-4dgs.md</code> L61–71；paper Table 2</td>
</tr>
<tr>
<td>Deformable 3DGS</td>
<td>D-NeRF synthetic / NeRF-DS</td>
<td>RTX 3090</td>
<td align="right">40K iter；分钟数未披露</td>
<td align="right">70 FPS（D-NeRF 跨源转引 <strong>[未二次核]</strong>）；&lt;250K GS 时 >30 FPS</td>
<td>[arXiv](https://arxiv.org/abs/2503.16422) · [homepage](https://ingra14m.github.io/Deformable-3D-Gaussians/) · [code](https://github.com/ingra14m/Deformable-3D-Gaussians) · <em>CVPR 2024</em></td>
<td>note L59–64、L80–101；paper §4.1–4.2</td>
</tr>
<tr>
<td>4DGS</td>
<td>D-NeRF synthetic</td>
<td>RTX 3090</td>
<td align="right"><strong>8 min / scene</strong></td>
<td align="right"><strong>82 FPS</strong></td>
<td>[arXiv](https://arxiv.org/abs/2310.08528) · [homepage](https://guanjunwu.github.io/4dgs/) · [code](https://github.com/hustvl/4DGaussians) · <em>CVPR 2024</em></td>
<td>note L46–59、L107–112；paper Table 1</td>
</tr>
<tr>
<td>4DGS</td>
<td>HyperNeRF vrig</td>
<td>RTX 3090</td>
<td align="right"><strong>30 min / scene</strong></td>
<td align="right"><strong>34 FPS</strong></td>
<td>[arXiv](https://arxiv.org/abs/2310.08528) · [homepage](https://guanjunwu.github.io/4dgs/) · [code](https://github.com/hustvl/4DGaussians) · <em>CVPR 2024</em></td>
<td>note L61–72、L107–112；paper Table 2</td>
</tr>
<tr>
<td>Sparse4DGS</td>
<td>NeRF-Synthetic / HyperNeRF / NeRF-DS / iPhone-4D sparse frames</td>
<td>未披露</td>
<td align="right">未在 abstract 拿到</td>
<td align="right">未在 abstract 拿到</td>
<td>[arXiv](https://arxiv.org/abs/2511.07122) · [homepage](https://changyueshi.github.io/Sparse4DGS/) · <em>arXiv pre-print (2025-11)</em></td>
<td>note L46–52、L86–92；abstract</td>
</tr>
<tr>
<td>AirGS</td>
<td>FVV benchmark（数据集名未披露）</td>
<td>RTX 3090 <strong>[未二次核]</strong></td>
<td align="right"><strong>20–40 min [未二次核]</strong></td>
<td align="right">未报告</td>
<td>[arXiv](https://arxiv.org/abs/2512.20943) · <em>SIGGRAPH 2025</em></td>
<td>note L44–50、L88–101；abstract + note L90 推算</td>
</tr>
<tr>
<td>GaussianFluent</td>
<td>mixed-material fracture / slicing simulation</td>
<td>未披露</td>
<td align="right">abstract 未给</td>
<td align="right">abstract 仅称 high speed，无数字</td>
<td>[arXiv](https://arxiv.org/abs/2601.09265) · [homepage](https://hb-pencil-zero.github.io/GaussianFluent/) · <em>CVPR 2026 Oral</em></td>
<td>note L58–69、L83–87；abstract</td>
</tr>
</tbody>
</table>

**本 split 解释**：只有同一 D-NeRF/HyperNeRF 行才能讨论速度变化。例如 4DGS 在 D-NeRF 是 8 min/82 FPS，而 D-NeRF 自身 Stand Up 为约 2 days，但硬件和具体场景仍不同；这说明数量级演进，不构成严格公平竞赛。Sparse4DGS 的目标是稀疏帧质量，不应因未报时间被判慢。

### B. 复杂 + driving（户外大型 / 多相机）

<table>
<thead>
<tr>
<th align="left">paper</th>
<th align="left">场景实例</th>
<th align="left">GPU</th>
<th align="right">训练/重建时间</th>
<th align="right">Peak FPS</th>
<th align="left">链接</th>
<th align="left">数据页码</th>
</tr>
</thead>
<tbody>
<tr>
<td>L2D2-GS</td>
<td>PandaSet dynamic urban；Waymo zero-shot</td>
<td><strong>8× H20</strong></td>
<td align="right"><strong>98 s</strong>（PandaSet reconstruction）</td>
<td align="right">未报告</td>
<td>[arXiv](https://arxiv.org/abs/2606.29374) · <em>arXiv preprint (2026)</em></td>
<td>note L80–101、L108–118；paper p.6 / Table II p.8</td>
</tr>
<tr>
<td>StreamSTGS</td>
<td>MeetRoom，12 cams，1280×720</td>
<td><strong>1× RTX A6000</strong></td>
<td align="right"><strong>29 s / GOP</strong></td>
<td align="right"><strong>126 FPS</strong></td>
<td>[arXiv](https://arxiv.org/abs/2511.06046) · <em>CVPR 2025</em></td>
<td>note L73–88；paper Table 2 / §5</td>
</tr>
<tr>
<td>StreamSTGS</td>
<td>N3DV，18–21 cams，1352×1014</td>
<td><strong>1× RTX A6000</strong></td>
<td align="right">note 中 Ours Train(s) 行未完整留存；<strong>不填推测值</strong></td>
<td align="right"><strong>100 FPS</strong></td>
<td>[arXiv](https://arxiv.org/abs/2511.06046) · <em>CVPR 2025</em></td>
<td>note L53–70、L84–88、L102；paper Table 1 / §5</td>
</tr>
<tr>
<td>MVFusion-GS</td>
<td>Neu3D，20 synchronized cameras，7 scenes</td>
<td><strong>RTX 4090</strong>（efficiency）；训练 stage 段另称 RTX 3090，<strong>口径有冲突</strong></td>
<td align="right"><strong>2.26 h</strong></td>
<td align="right"><strong>62.7 FPS</strong></td>
<td>[arXiv](https://arxiv.org/abs/2607.01578) · [code](https://github.com/toseeai-com/MVFusion-GS) · <em>arXiv preprint (2026)</em></td>
<td>note L84–90、L133–137；paper Table 11 p.24</td>
</tr>
</tbody>
</table>

**本 split 解释**：StreamSTGS 29 s 是流式 GOP 更新，L2D2-GS 98 s 是 8×H20 上的场景重建，MVFusion-GS 2.26 h 是 Neu3D per-scene optimization。输入规模、输出目标与 GPU 数量均不同，排序只陈列 wall-clock，不声称算法单卡效率等价。

### C. Feed-forward 4DGS（独立赛道）

<table>
<thead>
<tr>
<th align="left">paper</th>
<th align="left">场景实例</th>
<th align="left">GPU</th>
<th align="right">训练/重建时间</th>
<th align="right">Peak FPS</th>
<th align="left">链接</th>
<th align="left">数据页码</th>
</tr>
</thead>
<tbody>
<tr>
<td>L2D2-GS</td>
<td>PandaSet dynamic urban</td>
<td><strong>8× NVIDIA H20</strong></td>
<td align="right"><strong>98 s</strong>；不含通用模型预训练成本</td>
<td align="right">未报告</td>
<td>[arXiv](https://arxiv.org/abs/2606.29374) · <em>arXiv preprint (2026)</em></td>
<td>note L80–105、L155–159；paper p.6 / Table II p.8</td>
</tr>
<tr>
<td>G3R（L2D2-GS 同表 dynamic baseline）</td>
<td>PandaSet</td>
<td><strong>未披露</strong></td>
<td align="right"><strong>60 s</strong></td>
<td align="right">未报告</td>
<td><em>PandaSet baseline in L2D2-GS Table II</em></td>
<td><code>2026-song-l2d2-gs.md</code> L93–101；paper Table II p.8</td>
</tr>
<tr>
<td>G3R*（复现配置）</td>
<td>PandaSet</td>
<td>8×H20 实验环境，但方法逐项 GPU 未明示</td>
<td align="right"><strong>75 s</strong></td>
<td align="right">未报告</td>
<td>[arXiv](https://arxiv.org/abs/2606.29374) · <em>L2D2-GS Table II 同表复现行</em></td>
<td>note L80–101；paper p.6 / Table II p.8</td>
</tr>
<tr>
<td>ZipSplat（静态同类，仅方法对照，<strong>不进 4DGS 主榜</strong>）</td>
<td>DL3DV / RealEstate10K，252×252</td>
<td><strong>未披露</strong></td>
<td align="right">feed-forward"秒级"，<strong>无精确秒数 [未二次核]</strong>；TTO 时间未给</td>
<td align="right">FPS 未报告</td>
<td>[arXiv](https://arxiv.org/abs/2606.05102) · <em>arXiv preprint (2026-06)</em></td>
<td><code>2026-veicht-zipsplat.md</code> L91–99、L124–132；paper §4 / Table 1</td>
</tr>
<tr>
<td>FCGS（静态同类，仅方法对照，<strong>不进 4DGS 主榜</strong>）</td>
<td>现成 3DGS compression</td>
<td><strong>未披露</strong></td>
<td align="right">minutes → seconds，<strong>无精确秒数</strong></td>
<td align="right">未报告</td>
<td>[arXiv](https://arxiv.org/abs/2410.08017) · [code](https://github.com/YihangChen-ee/FCGS) · <em>CVPR 2024</em></td>
<td><code>2024-chen-fcgs.md</code> L40–55、L83–89；abstract</td>
</tr>
</tbody>
</table>

**本 split 解释**：若只看 PandaSet 同表，G3R 的 60 s 比 L2D2-GS 98 s 短，但 L2D2-GS 以 1.2M GS 达到 24.19 dB，G3R 为 3M GS / 23.15 dB；这正是速度、质量与表示规模的三方权衡。ZipSplat/FCGS 是静态先例，仅证明 feed-forward 压缩或重建思路，不是动态榜参赛者。

## 3. 讨论

### 3.1 当前最快重建速度

在可核数字中，per-scene/streaming 赛道最短是 StreamSTGS **29 s/GOP**（MeetRoom, A6000），限制是它不是完整序列从零训练；完整小场景 per-scene opt 可核最短为 4DGS **480 s**（D-NeRF, RTX 3090）。feed-forward 动态主方法为 L2D2-GS **98 s**（8×H20），但不含预训练且未报 FPS。

### 3.2 训练时间 vs Peak FPS 是否 trade-off

不存在稳定单调 trade-off。4DGS 在 D-NeRF 同时做到 **8 min / 82 FPS**，SpeeDe3DGS 在 NeRF-DS 为 **625.48 s / 505.60 FPS**，属于双轴都好的离群点；MVFusion-GS 则为质量和紧凑性牺牲速度：2.1→2.26 h、71→62.7 FPS。FPS 仅限各自数据集内解读。

### 3.3 对 Snap 8 Gen 4 on-device spec 的借鉴

优先借 SpeeDe3DGS 的 TSP/TSS 与 GroupFlow：跨帧剪枝、时间扰动、共享 SE(3) 可消除 per-Gaussian MLP；借 StreamSTGS 的训练时 Transformer、推理时移除及 GOP 更新；借 L2D2-GS 的 compact densification policy。静态 Flux-GS 的 baked MLP、多视角 alpha 剪枝和 WebGL async-sort 也值得移植，但不能把其 147 FPS 当作 4DGS 手机指标。

## 4. 静态 3DGS 重建速度对照（不参与主榜）

<table>
<thead>
<tr>
<th align="left">paper</th>
<th align="left">场景 / GPU</th>
<th align="right">时间</th>
<th align="right">Peak FPS</th>
<th align="left">链接</th>
<th align="left">数据页码</th>
</tr>
</thead>
<tbody>
<tr>
<td>3DGS (Kerbl et al., 2023)</td>
<td>Mip-NeRF 360 / RTX A6000</td>
<td align="right">35–45 min</td>
<td align="right">≥30 FPS @1080p</td>
<td>[arXiv](https://arxiv.org/abs/2308.04079) · [code](https://github.com/graphdeco-inria/gaussian-splatting) · <em>SIGGRAPH 2023</em></td>
<td>note L15–20；paper Table 1 p.7</td>
</tr>
<tr>
<td>FCGS (Chen et al., 2024)</td>
<td>GPU 未披露</td>
<td align="right">minutes → seconds（无精确值）</td>
<td align="right">未报告</td>
<td>[arXiv](https://arxiv.org/abs/2410.08017) · [code](https://github.com/YihangChen-ee/FCGS) · <em>CVPR 2024</em></td>
<td>note L40–55；abstract</td>
</tr>
<tr>
<td>ACE-GS (Zhao et al., 2026)</td>
<td>Mip-NeRF 360 / <strong>GPU 未披露</strong></td>
<td align="right"><strong>5m30s</strong>（vs 3DGS 24m43s）</td>
<td align="right"><strong>745.6 FPS</strong></td>
<td>[arXiv](https://arxiv.org/abs/2606.21244) · <em>arXiv preprint (2026-03)</em></td>
<td>note L73–87；paper Table 1 p.9</td>
</tr>
<tr>
<td>Flux-GS (Du et al., 2026)</td>
<td>Mip-NeRF 360 Indoor / training GPU 未披露；render Snap 8 Gen 3</td>
<td align="right"><strong>11 min</strong>（vs Mobile-GS 86 min）</td>
<td align="right"><strong>147 FPS mobile</strong></td>
<td>[arXiv](https://arxiv.org/abs/2606.30017) · [homepage](https://xiaobiaodu.github.io/flux-gs-project/) · <em>ECCV 2026 (under review)</em></td>
<td>note L74–100；paper Table 1</td>
</tr>
<tr>
<td>ZipSplat (Veicht et al., 2026)</td>
<td>DL3DV / GPU 未披露</td>
<td align="right">feed-forward 秒级但无精确值 <strong>[未二次核]</strong></td>
<td align="right">未报告</td>
<td>[arXiv](https://arxiv.org/abs/2606.05102) · <em>arXiv preprint (2026-06)</em></td>
<td>note L91–99、L124–132；paper §4</td>
</tr>
<tr>
<td>GRay (Poirier-Ginter et al., 2026)</td>
<td>13 standard scenes / GPU 未披露</td>
<td align="right"><strong>1:58 init + 5:40 opt = 7:38 total</strong>；prompt 所给 3:42 opt 与 note 冲突，采用 paper-note Fig.1</td>
<td align="right"><strong>248 FPS</strong></td>
<td>[arXiv](https://arxiv.org/abs/2606.30869) · [code](https://repo-sam.inria.fr/nerphys/gray) · <em>ACM Proc. CGIT 2026</em></td>
<td>note L70–83；paper Fig.1 p.1</td>
</tr>
<tr>
<td>SpeeDe3DGS 静态/高速阵列类概括</td>
<td>GPU 未在相应概括处明确</td>
<td align="right"><strong>9.5 h vs 24 h [未二次核]</strong>（由 note 项目解读，不作本报告实测点）</td>
<td align="right">不适用</td>
<td>[arXiv](https://arxiv.org/abs/2506.07917) · <em>CVPR 2025</em></td>
<td><code>2025-tu-speede3dgs.md</code> L132–137；note 推理</td>
</tr>
<tr>
<td>EvoGS</td>
<td>Mip-360 L1 / desktop GPU（型号未披露）</td>
<td align="right"><strong>未在 abstract 拿到</strong></td>
<td align="right">未报告</td>
<td>[arXiv](https://arxiv.org/abs/2606.07179) · <em>arXiv preprint (2026-05)</em></td>
<td>note L91–96；abstract</td>
</tr>
<tr>
<td>VEDAL</td>
<td>Mip-360 / GPU 未披露</td>
<td align="right"><strong>未在 abstract 拿到</strong></td>
<td align="right">185 FPS</td>
<td>[arXiv](https://arxiv.org/abs/2606.02346) · <em>arXiv preprint (2026-04)</em></td>
<td><code>2026-li-vedal.md</code> L60–72、L88–92；paper Table 1</td>
</tr>
</tbody>
</table>

## 5. 缺失值与复核队列

- **必须二次核**：AirGS 的 20–40 min 与 RTX 3090（note 明示推测）；ZipSplat"秒级"没有精确 wall-clock；SpeeDe3DGS"9.5 h vs 24 h"是项目层解释；Deformable 3DGS 的 70 FPS 为跨源转引。
- **未在 abstract / note 拿到训练时间**：Sparse4DGS、RetimeGS、GaussianFluent、EvoGS、VEDAL；这些条目不参与最快结论。
- **GPU 未披露，禁止猜测**：Sparse4DGS、RetimeGS、GaussianFluent、G3R 逐方法配置及多数静态对照。ACE-GS note 对 RTX 4090 仅作推测，因此表中保留"未披露"。
- **口径冲突**：MVFusion-GS 方法设置段写单 RTX 3090，efficiency Table 11 写 RTX 4090；本榜时间/FPS 采用同一 efficiency 表的 RTX 4090，并保留冲突说明。
- **GRay 时间冲突**：任务摘要给 1:58 + 3:42 = 5:40，但 paper note Fig.1 明确是 init 1:58、opt 5:40；报告采用 note/PDF anchor 的 **总计 7:38**，不把摘要误算写入排行榜。

## 6. 6 条款产品目标 vs 当前 spec (2026-07-22 双盲)

> **目的**：用户给的产品目标是否是当前调研已可实现？这里给两份独立判断。

### 6.1 6 条款双盲对照

| 条款 (产品口径) | A verdict (spec 作者) | B verdict (QA 验收) | 双盲 consensus |
|---|---|---|---|
| ① 20 秒以内 / 4K / 单目视频输入 | missed | missed | **missed** (spec L24 写"多视角高速相机阵列" ≠ 用户口径) |
| ② 适配移动端实时渲染的 4DGS 输出 | covered | covered | **covered** (spec L7–L8, L19–L23) |
| ③ PSNR ≥ 35 dB @ 原始轨迹 + 小范围漫游 | partial | partial | **partial** (L42 有 PSNR 维度，但 35 dB 阈值 / 漫游场景未规定) |
| ④ 无空洞 / 漂浮物 / Ghosting / 时间闪烁 (产品级视觉) | missed | partial | ⚠ **分歧** — A: spec 无任何产品术语; B: L36/L42/L71/L86 间接覆盖 |
| ⑤ 云端生成时间 1h / 挑战 5min | partial | missed | **missed** (L25 "几小时~几天" ≠ 1h/5min，差 1–3 数量级，且未承诺云端) |
| ⑥ 输出与移动端压缩 / 渲染管线兼容 | covered | covered | **covered** (spec L21, L56–L67) |

### 6.2 总体 verdict

**6 条中 2 covered / 2 partial / 2 missed (覆盖率 ≈ 50%)**。该目标当前**未实现**，但 spec 框架可复用 — 4 项缺口都是"在现有 spec 框架里补一段硬指标"，不是"重做 spec"。

### 6.3 双盲一致性

A (spec 作者视角, 宽松) vs B (QA 验收视角, 严格) 独立 `read_file` 同一 `00-goal.md`，不交叉。**6 条中 5 条完全一致，1 条 (条款 4) 分歧**。分歧本质是"研究术语 vs 产品术语"的语义鸿沟 — A 按 spec 字面 zero-mention 判 missed, B 按研究间接覆盖 (串扰抑制 / warping error) 判 partial。本报告采纳 B 的 partial，因为研究端若已做串扰抑制，大概率视觉上不会出现严重 temporal flickering，条款 4 的修订是补一条定性 PASS 条款，不是白手起家。

### 6.4 必改条目 (must-fix, 来源 B)

| # | 当前 spec 表述 | 产品口径 | 修订动作 |
|---|---|---|---|
| (a) 采集 | L24 "多视角高速相机阵列 + 高精度 SfM" | 用户手机自拍 ≤20 秒 4K 单目视频 | 改"用户单目手机视频"为主方案，保留多视角作对照 |
| (b) 精度验收 | L42 "PSNR / SSIM / LPIPS、warping error" | PSNR ≥ 35 dB @ 原始轨迹 + 小范围漫游 | 加 35 dB 阈值 + 视角范围限定 |
| (c) 时效 | L25 "训练预算: 几小时~几天" | 云端 ≤1h 目标 / ≤5min 挑战 | 改预算；明确云端部署形态 |
| (d) 视觉验收 | (无) | 无明显空洞 / 漂浮物 / Ghosting / 时间闪烁 | 加定性 PASS 门槛（参考研究端串扰抑制机制） |

**注意**: 条款 2 与 6 在两份判断里都 covered，无需修改。条款 1 / 5 即使按 B 严格判定为 missed，修订动作都是单行级（采集方案行 + 训练预算行），不重做 spec。
