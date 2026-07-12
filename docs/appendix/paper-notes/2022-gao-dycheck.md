# Monocular Dynamic View Synthesis: A Reality Check (DyCheck)

**作者**: Hang Gao, Ruilong Li, Shubham Tulsiani, Bryan Russell, Angjoo Kanazawa
**机构**: UC Berkeley, FAIR, Google Research
**会议**: 3DV 2022
**arxiv-id**: 2210.13445 (v1 2022-10-24)
**本地 PDF**: `.pdfs/2210.13445.pdf`
**survey citekey**: `gao2022dycheck`
**GitHub**: https://github.com/KevinQian07/DyCheck (iPhone dataset)

## 一句话
DyCheck — 提供 **iPhone 采集的 real-world dynamic 场景数据集** (5 场景:
Cookie, Splicing, Crab, Paper, Spin) + benchmark monocular dynamic view synthesis
(测试方法在 iPhone 自己训 + eval)。

## 关键数字（paper 实测）
- **5 场景 iPhone 数据集** (Cookie, Splicing, Crab, Paper, Spin)
- **18 cameras per scene** (per paper §4)
- **PSNR Dyb synth / real**: paper 测 RoDynRF, Nerfies, TiNeuVox, HyperNeRF 等

## 重要 claim
- **iPhone 采集** — 跟 D-NeRF 的 synthetic + HyperNeRF 的 vrig 都不同
- 5 场景真实 (not synthetic)
- benchmark 评估 monocular dynamic view synthesis 的现实表现

## 评价（survey 引用规范）
- 引用作为 **dynamic 4DGS 数据集** (D-NeRF / N3V / DyCheck 三大数据集之一)
- survey.tex 引用在 sec-7-datasets-metrics.tex + sec-8-discussion.tex
- **v5.34+v5.35 patch 关键修正**:
  - survey.bib title 之前是 "Dynamic Visual Reasoning by Learning Differentiable Physics Models" (错的, 是 Ding et al. 2110.15358)
  - 改为 "Monocular Dynamic View Synthesis: A Reality Check" (真)
  - author 之前是 "Hang Gao and Yitong Li and Hang Zhou and Xibin Song and Mingliang Xu" (全 fabricated)
  - 改为 "Gao, Hang and Li, Ruilong and Tulsiani, Shubham and Russell, Bryan and Kanazawa, Angjoo" (arxiv 真实)
  - eprint 2210.13445 (真)

## 关键段落 anchor
- Abstract: iPhone dataset
- §3 Dataset collection
- §4 Benchmark protocol
- §5 Results
