# HyperNeRF

**作者**: Keunhong Park, Utkarsh Sinha, Peter Hedman, Jonathan T. Barron, Sofien Bouaziz, Dan B Goldman, Ricardo Martin-Brualla, Steven M. Seitz
**机构**: Google Research, University of Washington
**会议**: SIGGRAPH Asia 2021
**arxiv-id**: 2106.13228 (v1 2021-06-24)
**本地 PDF**: `.pdfs/2106.13228.pdf`
**survey citekey**: `hypernerf2022`
**GitHub**: https://github.com/google/hypernerf

## 一句话
HyperNeRF — 把 Nerfies 翘曲场扩展到 **拓扑变化** (topology change) 场景
(如切开/合上物体)；用 ambient slicing 处理 5D 高维空间。

## 关键数字（paper 实测）
- **Training time**: "约 8 hours on 4 TPUv4" (v5.17 patch 修正)
- **Datasets**: 自带 vrig (vibrating rig) + interp 数据集
- **PSNR**: 30+ dB
- **vrig dataset**: 静态相机 + 振动 (vibration) 装置，6 场景

## 重要 claim
- **8h 4 TPUv4** (v5.17 patch 修正, 之前 survey 写 "30 min" 错)
- 拓扑变化场景 (切开 → 变成两个分开的物体)
- 后续 **4DGS-derived work 大量用 HyperNeRF 数据集** vrig

## 评价（survey 引用规范）
- 引用作为 **deformable NeRF 扩展** (Nerfies 的拓扑版)
- survey.tex citekey `hypernerf2022` (year=2022 venue, arxiv 2021-06)
- 引用 **vrig dataset** (6 场景, paper §6) — 4DGS 测试常用
- **v5.17 patch 关键修正**: "8 hours on 4 TPUv4" 不是 "30 min"

## 关键段落 anchor
- Abstract: topological variation
- §3 Method: ambient slicing
- §5 Datasets: vrig + interp
- §6 Experiments
