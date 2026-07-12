# Nerfies: Deformable Neural Radiance Fields

**作者**: Keunhong Park, Utkarsh Sinha, Jonathan T. Barron, Steven Bouaziz, Dan B Goldman, Stephen M. Seitz, Richard Szeliski
**机构**: Google Research, University of Washington
**会议**: ICCV 2021
**arxiv-id**: 2011.12948 (v1 2020-11-25)
**本地 PDF**: `.pdfs/2011.12948.pdf`
**survey citekey**: `park2021nerfies`
**GitHub**: https://github.com/google/nerfies

## 一句话
Nerfies — 用弹性 regularization + 翘曲场 (warp field) 把单目视频转成
自由视点视频；**Deformable NeRF 鼻祖之一** (跟 D-NeRF 同期)。

## 关键数字（paper 实测）
- **Training time**: 数小时 per scene 单 GPU
- **PSNR**: 30+ dB range (per paper Table 1)
- **关键贡献**: per-point Jacobian-based elastic regularization

## 重要 claim
- Nerfies 是 **per-scene training** 跟 D-NeRF 同
- **NeRF 系起源** — 后续 4DGS 类 (Deformable 3DGS, HyperNeRF-derived work) 都用 Nerfies 的 elastic reg 思想

## 评价（survey 引用规范）
- 引用作为 **deformable NeRF 代表** (跟 D-NeRF, HyperNeRF)
- survey.tex 已 cite `park2021nerfies`

## 关键段落 anchor
- Abstract: deformable NeRF
- §3 Method: warp field + elastic reg
- §5 Experiments
