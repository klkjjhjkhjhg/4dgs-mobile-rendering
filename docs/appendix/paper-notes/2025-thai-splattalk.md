# SplatTalk: 3D VQA with Gaussian Splatting

**作者**: Anh Thai¹,², Songyou Peng², Kyle Genova², Leonidas Guibas², Thomas Funkhouser²
**机构**: ¹Georgia Institute of Technology; ²Google DeepMind
**会议**: ICCV 2025
**arxiv-id**: 2503.06271
**本地 PDF**: .pdfs/iccv2025-Thai_SplatTalk_3D_VQA_with_Gaussian_Splatting_ICCV_2025_paper.pdf
**survey citekey**: (待 M2b extract_paper_summary.py 自动生成)
**GitHub**: project page https://splat-talk.github.io/（源码链接未在 PDF 公开）
**收录日期**: 2026-08-13
**收录来源**: P36 精读补全（v1 + v2 subagent 交叉验证）

## 一句话
SplatTalk 提出了首个 self-supervised 3D-language Gaussian Splatting 框架，从多视角 RGB 图像（无需深度、点云或 3D-language 标注）训练出可由 LLM 直接查询的 3D token 场，实现 zero-shot 3D VQA，并在 ScanQA / SQA3D / MSR3D 三个 benchmark 上以 2D LMM 类别 SOTA 超越 2D 基线（如 LLaVA-OV）。

## 关键数字（paper 实测） — v2 重抽中间页（page 5–6）补全 Table 1 / Table 2 全部 cell
### ScanQA (val) Table 1 部分（2D LMM-Based 类）
|| Method | Modality | CIDEr | METEOR | ROUGE | EM@1 | EM@1-R |
||---|---|---|---|---|---|---|
|| LLaVA-OV [21] | I | 50.0 | 13.0 | 29.4 | 15.6 | 32.5 |
|| **SplatTalk** | I | **61.7** | **14.2** | **32.7** | **17.1** | **32.2** |
|| SplatTalk-ScanQA-FT | I | 77.1 | 15.4 | 38.7 | 22.3 | 38.3 |
|| SplatTalk-3DVQA-FT | I | 77.5 | 15.6 | 38.5 | 22.4 | 38.3 |

### SQA3D (test) Table 1 部分
|| Method | Modality | EM@1 | EM@1-R |
||---|---|---|---|
|| LLaVA-OV [21] | I | 25.4 | 35.8 |
|| SplatTalk-ScanQA-FT | I | 42.0 | 44.7 |
|| **SplatTalk-3DVQA-FT** | I | **47.6** | **49.4** |

### MSR3D Table 2 zero-shot
|| Model | Input | Counting | Existence | Attributes | Spatial | Navigation | Others | Overall |
||---|---|---|---|---|---|---|---|---|
|| LEO [17] | T+PC | 0.80 | 15.5 | 11.8 | 7.3 | 2.3 | 15.3 | 7.8 |
|| LLaVA-OV [21] | T+I | 18.6 | 31.2 | 24.8 | 19.5 | 16.7 | 36.3 | 24.0 |
|| **SplatTalk** | T+I | **19.6** | **60.3** | **44.0** | **35.8** | **35.5** | **61.8** | **41.8** |
|| SplatTalk-ScanQA-FT | T+I | 28.9 | 66.0 | 43.2 | 28.3 | 33.8 | 60.0 | 41.5 |

### Table 3 / Table 4 消融（page 8）— v1 已抽到，v2 保留
- 32,076 tokens (44 images) vs 729 tokens (1 image)：ScanQA EM@1 16.2 → 17.1（+0.9），EM@1-R 30.7 → 32.2；MSR3D EM@1 7.9 → 14.1（几近翻倍）
- Entropy sampling ablation 是最优

### 训练开销（v1 已抽到）
- 500 ScanQA 训练场景，100 views/scene，单 H100 80GB GPU
- LoRA fine-tune 与推理同样在单 H100

## 重要 claim（v2 至少补到 5 个以上）
1. **首个 self-supervised 3D Gaussian-based zero-shot 3D VQA**，仅需多视角 RGB 图，无需 depth / point cloud / 3D-language 标注 *(PDF p.2 §1)*
2. **EM 推导的 mean feature 编码 holistic 场景语义**：高斯的最优 3D feature f*ᵢ = Σ R·F_gt / Σ R 由 E-step (渲染) + M-step (重建) 推得 (PDF p.6 §3.2, Eq 4)，区别于 SAM/CLIP-based object-centric 嵌入
3. **Entropy-adaptive token sampling** 取 top-k 最高熵的 Gaussian，匹配 LLM 的 visual token capacity，无须额外训练 *(PDF p.6 §3.3)*
4. **joint-train RGB + semantic** 在 latent Gaussian triplet 中 end-to-end 优化；区别于 ChatSplat 等先训练 RGB Gaussian 再冻结注入 language features 的两阶段路线 *(PDF p.5 §3.1)*
5. **3D tokens 无显式 positional encoding**：每个 token 的 3D 位置已隐式编码于 rendering/fusion 的 feature 中，输入 LLM 形成 unordered set（类似 point cloud） *(PDF p.6 §3.3)*
6. **无需 pre-trained per-scene autoencoder**：跨所有训练场景 train 单一 autoencoder，且 feature decoder 与 3DGS 分离（joint 训会引入不稳定） *(PDF p.5 §3.1)*
7. **CUDA parallel rasterizer 同时渲染 semantic 与 RGB**：共享 Gaussian 参数，处理 256 维高维 features *(PDF p.5 §3.1)*
8. **MSR3D zero-shot 比 LLaVA-OV 翻倍以上**：如 Existence 31.2 → 60.3、Overall 24.0 → 41.8 *(PDF p.6 Table 2)*

## 评价（survey 引用规范）
- 派系归属：**E** (Cross-disciplinary：3DGS × Language × VQA，与 LangSplat/Feature3DGS/OpenSplat3D 同子方向)
- 相关性：**低-中**（不解决动态场景 / mobile rendering / SLAM / 位姿估计；只解决静态室内 3D 场景的语义问答；但 "feed-forward 3DGS + entropy sampling" 思路对 §1 高精度表示主线与 §3 移动端加速主线均无直接借鉴价值；主要供 §5 cross-disciplinary 拓展参考）
- 方法简述：基于 FreeSplat 的 feed-forward 3DGS pipeline；LLaVA-OV 的高维 visual token 经 scene-wise autoencoder 压到 256 维 hypersphere 作为 Gaussian latent feature；推理阶段 entropy-aware sampling top-k 3D Gaussian features 直接作为 LLM 的 visual tokens；EM 推导支撑 "mean feature 已够，无需用 cov/opacity"。

## 关键段落 anchor — v2 重核
- §1 Introduction：p.1–p.2，论述"3D-language 标注依赖"与"token 维度耦合 2D VLM"两大痛点
- §2 Related Work：p.3，区分 (a) open-vocab segmentation (CLIP/SAM/LSeg)、(b) 3D LMM (ChatSplat 等)、(c) FreeSplat feed-forward 3DGS
- §3 Method：p.4 起 —— §3.1 Feature Autoencoder 与 Joint Training (p.4–p.5)，§3.2 Extracting 3D Language Features 含 EM 推导 (p.5–p.6)，§3.3 3D VQA Inference + Entropy Sampling (p.6)
- §4 Experiments：p.6 起 —— §4.1 Implementation Details (p.6)，§4.2 Datasets (p.6)，§4.3 Main Results **Table 1 / Table 2** (p.6–p.7)，§4.4 Ablations **Table 3 / Table 4** (p.7–p.8)
- **Table 1 (ScanQA/SQA3D)**：**p.6**
- **Table 2 (MSR3D zero-shot)**：**p.6**
- Table 3 (Gaussian Sampling Ablation Random/Point Density/FPS/Entropy)：p.8
- Table 4 (Visual Input Length Ablation 729 vs 32,076 tokens)：p.8
- Figure 1 (Teaser)：p.1，pipeline 总图 multi-view RGB → 2D VLM → 3D-language Gaussian Field → LLM 推理
- Figure 3 (Qualitative)：p.7，ScanQA 4 个 spatial reasoning Q&A 对比 LLaVA-OV / Ours / GT
- Project page: https://splat-talk.github.io/

**v1 已标 / v2 仍未补的项**：
- 训练细节（learning rate / batch size / optimizer / 8-bit/16-bit 训练）：PDF 未明确给出，需查 supplementary
- Project page 是否有 code release：未在 PDF/public HTML 找到明确 release 日期
- 与 ChatSplat 的 mIoU/ScanQA 直接 cell 数字对比：Table 1 未列 ChatSplat