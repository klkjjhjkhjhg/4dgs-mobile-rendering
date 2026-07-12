# D-NeRF

**作者**: Albert Pumarola, Enric Corona, Gerard Pons-Moll, Francesc Moreno-Noguer
**机构**: University of Barcelona, ETH Zürich
**会议**: CVPR 2021
**arxiv-id**: 2011.13961 (v1 2020-11-27)
**本地 PDF**: `.pdfs/2011.13961.pdf`
**survey citekey**: `pumarola2021dnerf`
**GitHub**: https://github.com/albertpumarola/D-NeRF

## 一句话
D-NeRF — 把 NeRF 扩展到 dynamic scenes: 训练时把时间作为额外输入
(MLP learns canonical + deformation field)，test 时给时间戳 query 即可。

## 关键数字（paper 实测）
- **Training time**: "约 2 天 on a single GTX 1080" (paper §5.2)
- **Datasets**: 自带 synthetic + real monocular 数据集
- **PSNR synthetic**: 30+ dB（具体 paper Table 1）
- **Stand Up scene 训练时间**（v5.17 patch 修正）: 不是 "8 min on A100", 实是 "约 2 days GTX 1080"

## 重要 claim
- **D-NeRF 训练** requires ~2 days 单 GPU（旧 hardware）
- D-NeRF 是 **monocular dynamic** 鼻祖 — 后续 4DGS 都参考

## 评价（survey 引用规范）
- 引用作为 **dynamic NeRF 原型** (跟 TiNeuVox, HyperNeRF 同类)
- **不要混淆 D-NeRF 跟 N3V (Neural 3D Video)**: D-NeRF 是单目动态, N3V 是多目动态
- "D-NeRF achieves 30+ dB" — paper 实际数字
- **v5.17 patch 关键修正**: D-NeRF "8 min on A100" 错, 改 "2 days on GTX 1080"

## 关键段落 anchor
- Abstract: dynamic NeRF
- §3 Method: time-conditioned MLP
- §5.1 Synthetic dataset
- §5.2 Real-world dataset
