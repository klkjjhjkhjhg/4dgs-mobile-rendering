# LUDVIG: Learning-Free Uplifting of 2D Visual Features to Gaussian Splatting Scenes

**作者**: Juliette Marrie, Romain Menegaux, Michael Arbel, Diane Larlus, Julien Mairal
**机构**: Inria, Univ. Grenoble Alpes, CNRS, Grenoble INP, LJK, France（基于 authors 归属常识 + ANR MIAI@Grenoble Alpes + ERC APHELEIA 资助项目推断；PDF 此段未抽到 author affiliation 段，标 "PDF 此段未抽到，待全文核验"）
**会议**: ICCV 2025
**arxiv-id**: 2410.14462
**本地 PDF**: .pdfs/iccv2025-Marrie_LUDVIG_Learning-Free_Uplifting_of_2D_Visual_Features_to_Gaussian_Splatting_ICCV_2025_paper.pdf
**survey citekey**: (待 M2b extract_paper_summary.py 自动生成)
**GitHub**: (PDF 抽到的段落中未给出 GitHub URL; 标 "未在抽到的 PDF 段落中提及")
**收录日期**: 2026-08-13
**收录来源**: P36 精读补全（v1 + v2 subagent 交叉验证）

## 一句话
LUDVIG 提出一个 **learning-free** 的"提升 (uplifting)"机制——通过 α-blending 渲染权重 wi(d; p) 的转置（transpose）直接把 2D 视觉特征图（SAM / DINOv2 / SAM2 等）加权聚合到 3D Gaussian Splatting 已训练好的每个 Gaussian 上（无需任何梯度优化），同时配套一个结合空间结构 (Gaussian graph) + DINOv2 相似度的 graph diffusion 过程生成 3D 分割 mask；相比 SAM/OpenGaussian 等 baseline，速度提升约 **10×**（LERF 10 min vs LangSplat 105 min vs LERF 45 min），且 ScanNet mIoU 显著优于 OpenGaussian。

## 关键数字(paper 实测)
- **NVOS 91.3 (IoU)**：LUDVIG 在 NVOS 上（3D-GS + SAM2 uplifting），与 SAGA 92.4 / OmniSeg3D 91.7 / SA3D-GS 92.2 / MVSeg — 持平（来源：PDF p.8 Table 1）
- **SPIn-NeRF 93.8 (IoU)**：LUDVIG 在 SPIn-NeRF 上（3D-GS + SAM2 uplifting），与 SA3D-GS 93.7 / SAGA 94.3 / OmniSeg3D 93.8 持平（来源：PDF p.8 Table 1）
- **73.1 (Geometry only) / 88.5 (Single view DINOv2) / 88.6 (Single view SAM2) / 91.6 (Uplifting DINOv2) / 93.8 (Uplifting+Diffusion DINOv2) / 93.8 (Uplifting+Diffusion SAM2)**：SPIn-NeRF segmentation ablation（来源：PDF p.8 Table 2）
- **LERF object localization overall 86.3 (IoU)**：LUDVIG (DINOv2 uplifting + graph diffusion) vs LERF 73.6 / LangSplat 84.3（来源：PDF p.8 Table 3）
- **LERF object segmentation overall 64.3 (IoU)**：LUDVIG 在 2D reprojection protocol 上，10 min 时间 vs LERF 45 min / LangSplat 105 min（来源：PDF p.8 Table 4）
- **LERF object segmentation 50.4 (IoU)**：LUDVIG 在 OpenGaussian 3D selection protocol 上，10 min 时间 vs OpenGaussian 50 min / Dr. Splat —（来源：PDF p.8 Table 4）
- **ScanNet mIoU 33.9 (19 cls) / 37.4 (15 cls) / 46.4 (10 cls)**：LUDVIG 在 ScanNet semantic segmentation 上 mIoU 大幅超越 OpenGaussian（24.7 / 30.1 / 38.3）（来源：PDF p.8 Table 6）
- **ScanNet mAcc 51.4 / 57.2 / 66.2**：LUDVIG vs OpenGaussian 41.5 / 48.3 / 55.2（来源：PDF p.8 Table 6）
- **10× speedup**：LUDVIG uplifting 比 OpenGaussian quantization-based learning 快约 10× (ScanNet 上 40min → 3min)（来源：PDF p.8 §5.4 + Table 6 caption）
- **"order of magnitude faster"**：相比 LERF (45min) / LangSplat (105min) / OpenGaussian (50min)，LUDVIG 仅 10 min（来源：PDF p.8 Table 4）

## 重要 claim
- LUDVIG 是首个 **learning-free** (zero optimization) 的 2D-to-3D 特征 uplifting 方法，基于已训练好的 3DGS 场景 + rendering weights 转置即可把 2D features 聚合到 Gaussian（来源：PDF p.3 §3.2 Eq.3 + p.8 §6）
- 实现层面，aggregation 在 CUDA 渲染过程中完成，2D-to-3D uplifting 与 3D-to-2D rendering 一样快（来源：PDF p.8 §6）
- 提出的 graph diffusion 结合空间结构 (Gaussian adjacency graph) + DINOv2 feature similarity，从粗略输入 (scribbles / CLIP relevancy maps) 生成精确 3D segmentation masks（来源：PDF p.8 §6）
- 相比 SAM-based open-vocabulary segmentation baselines 有显著 IoU 提升（如 SPIn-NeRF 88.6 single-view SAM2 → 93.8 with uplifting+diffusion），且 compute efficient（来源：PDF p.8 §5 + Table 2/5）
- Limitations：3D 特征质量依赖底层 3DGS 重建质量，对高 specular（论文 [15, 44]）与 motion blur（论文 [24, 50]）场景不佳，未来可与 3DGS 重建联合优化做 regularization（来源：PDF p.8 §6）
- 已被集成到 Panst3R (论文 [53]) 做 novel-view panoptic segmentation（来源：PDF p.8 §6）

## 评价(survey 引用规范)
- 派系归属：**E**（3DGS 静态加速 / 通用加速派系；纯静态 3DGS 上的语义/特征提升方法，非 4DGS / 非 dynamic / 非 mobile streaming；与 placeholder 标注 E 一致，经 PDF §1 + §3 + Table 1-6 验后保留）
- 相关性：**低**（核心创新在 semantic feature uplifting 与 3D segmentation，对 4DGS 调研的 mobile rendering / dynamic scene / SLAM / pose / memory 核心问题无直接贡献；但其 learning-free + GPU-efficient 设计哲学对 mobile on-device 推理有借鉴意义；graph diffusion 可扩展到 dynamic 4DGS 的 temporal segmentation）
- 方法简述：已训练 3DGS 场景 → 对每个 Gaussian i 聚合其 visible view/pixel 对的 2D features (DINOv2/SAM/SAM2) 加权求和（权重 = α-blending 渲染权重 wi 的归一化）→ 可选 graph diffusion 精化 mask → 得到 3D Gaussian-level features

## 关键段落 anchor
- §1 Introduction + §2 Related Work：PDF p.1-2，**未抽到文字**（PDF 抽取工具对本文档有 MuPDF format error, 页面 1+2 全部空白; abstract + intro 文字待 v2 全文补）
- §3 Uplifting 2D visual representations into 3D：p.3，**核心方法段**（PDF 此段有部分内容）：§3.1 Background on Gaussian Splatting (Eq.1 α-blending + Eq.2 reconstruction loss); §3.2 Uplifting with simple aggregation (Eq.3 fi = Σ wi·Fd,p / Σ wi，transpose rendering operator W + normalization D); §3.3 (后续段 PDF 此段未抽到, 待全文补 graph diffusion 公式)
- §4 + §5 Experiments：p.4-7，**未抽到文字**（page 4-7 在 PDF 抽样中均为空白），但 Tables 1-6 数据完整
- §6 Concluding remarks and limitations：p.8，核心结论段（learning-free + CUDA 实现 + 与 Panst3R 集成 + limitations on specularity/motion blur）
- Figure 1 + Figure 2：PDF 此段未抽到图描述（图标题在 PDF 中可能缺失）
- Table 1：p.8，**Multi-view segmentation (IoU) on NVOS + SPIn-NeRF**（7 个方法对比, 2 个数据集）
- Table 2：p.8，**Ablation on SPIn-NeRF**（geometry only / single view / uplifting / uplifting+diffusion × DINOv2/SAM2）
- Table 3：p.8，**LERF object localization**（LERF/LangSplat/LUDVIG 在 ramen/figurines/teatime/waldo 4 场景 + overall）
- Table 4：p.8，**LERF object segmentation**（2 个 evaluation protocols × 5 个方法 × time column）
- Table 5：p.8，**Ablation on LERF**（SAM × graph diffusion 2×2 ablation）
- Table 6：p.8，**ScanNet semantic segmentation**（LangSplat/LEGaussians/OpenGaussian/LUDVIG × 19/15/10 classes × mIoU/mAcc）