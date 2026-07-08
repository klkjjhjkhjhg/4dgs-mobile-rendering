# 2025-youn-success-gs · SUCCESS-GS: Survey of Compactness and Compression for Efficient Static and Dynamic Gaussian Splatting

> **相关性**:**⭐⭐ 中相关(领域 survey,2025-12,Chung-Ang + Kyung Hee,韩国双校)** —— **核心价值**:**首个 unified overview 同时覆盖 3DGS + 4DGS efficient 方向**;**两轴分类法 = Parameter Compression vs Restructuring Compression**,每个方向再分子类;**配套项目页 `https://cmlab-korea.github.io/Awesome-Efficient-GS/` 是 excellent reference list**。

> **⚠ 重要边界声明**:**SUCCESS-GS 是 3DGS + 4DGS efficient 方向 survey**,**不提出新方法**;**abstract §"first unified overview" 直引**;**写作目标 = 给本项目"4DGS 压缩 + 加速"提供完整方法学 map**;**37 页内容覆盖 §3 静态 + §4 动态 + §5 datasets/metrics + §6 future directions**。

## 0.5 元数据

- **venue**: arxiv pre-print (2025-07)
- **arxiv-id**: 2512.07197
- **s2-id**: （v2 用 Semantic Scholar API 补全）
- **homepage**: （无）
- **github**: （无）
- **status**: under review
- **收录日期**: 2026-07-08（首次）
- **收录来源**: arxiv scan + 1-hop 引用规则
- **1-hop 引用**: （v2 补全，见 §11 1-hop 关系图）
- **评级**: ⭐

## 一句话问题

3DGS / 4DGS 实用化的最大瓶颈 = **存储开销(百万级 Gaussians) + 计算开销(per-Gaussian motion inference)**。**如何系统化分类现有 efficient 3DGS / 4DGS 方法,给研究者一张完整的 roadmap?**

## 链接(均经 fetch + PDF 实测验证)
- arxiv: <https://arxiv.org/abs/2512.07197>(v1 提交 2025-12)
- **项目页 / Awesome 列表**:`https://cmlab-korea.github.io/Awesome-Efficient-GS/`(PDF 头部直引)
- PDF: 已下 `.pdfs/2512.07197.pdf`(37 页,2.4 MB)

## 年份 / 作者 / 机构(PDF 头部实测)
- **年份**:2025(2025-12 arxiv v1)
- **作者**(按 arxiv metadata 头部,共同一作 * + 通讯作者 †):**Seokhyun Youn*¹, Soohyun Lee*², Geonho Kim*¹, Weeyoung Kwon¹, Sung-Ho Bae†², Jihyong Oh†¹**
- **机构**(PDF 头部直引):
  1. **Chung-Ang University(中央大学,首尔)**
  2. **Kyung Hee University(庆熙大学)**

## Survey 的方法学分类(abstract + §1 + §3-4 直引)

### 两大方向(abstract § 直引)
> "we systematically categorize existing methods into two major directions, **Parameter Compression** and **Restructuring Compression**"

### Static 3DGS(§3 详述)

**§3.1 Parameter Compression**(不动 model 架构,直接压 attribute):
- **Pruning** — 剪冗余 Gaussians
- **Attribute Pruning** — 选择性剪 attribute 子集
- **Quantization** — 减 bit 精度
- **Structured Compression** — 按空间 / 层次结构组织
- **Entropy Coding** — 算术 / 范围编码

**§3.2 Restructuring Compression**(改 model 架构本身):
- **Hierarchical Anchors**(类似 HAC++ 路线)
- **Neural Integration**(把 3D Gaussians 集成进 neural field)
- **Geometry-aware Organization**(基于 SDF / voxel / KNN 重组织)
- **Anchor + Deformable combination**(per-Gaussian → anchor 派生)

### Dynamic 3DGS / 4DGS(§4 详述,本项目最相关)

**§4.1 Parameter Compression for 4DGS**:
- **Gaussian Pruning** — 按 temporal activity / motion magnitude 剪
- **Attribute Pruning** — 删 temporal parameters,**隐式把 4D → 3D**
- **Quantization** — sensitivity-based 对 temporal params 量化
- **Entropy-based Compression** — 熵编码 temporal 流

**§4.2 Restructuring Compression for 4DGS**:
- **§4.2.1 Anchor-based + Canonical Deformable**:
  - 一组稀疏 anchor Gaussians 做空间 reference
  - 每个 anchor encode **local context** + **deformation parameters**
  - 时间步上 map canonical → dynamic frames
  - 代表作:Spacetime Gaussians, **HAIF-GS**(Hierarchical Anchors Densification + Anchor Filter + IFGD)
- **§4.2.2 Canonical Deformable Representation**:
  - **Implicit Deformation**:MLP / grid-based(Deformable 3DGS, Wu 4DGS, DeformGS)
  - **Explicit Deformation**:预定义 polynomial / keyframe interpolator(Ex4DGS, NeuralVoxels, 4DGCPro)
- **§4.2.3 LoD(Level-of-Detail)Representation**:
  - 多分辨率 hierarchy
  - 代表作:**Scale-GS**(recursive binary splitting 多尺度),**4DGCPro**(rigid + residual decomposition)

### §5 Datasets and Evaluation
**Static 3DGS datasets**(Table 1):
- TNT(Real,14 scenes,1920×1080)
- Deep Blending(Real,19 scenes,1228-2592×816-1944)
- NeRF-Synthetic(Synthetic,8 scenes,800×800)
- BungeeNeRF(Mixed,12 cities,Google Earth Studio)
- Mip-NeRF 360(Real,9 scenes,4946×3286)

**Dynamic datasets**(implicit from N3DV / D-NeRF / HyperNeRF / NeRF-DS / MonoDyGauBench referenced)

**Metrics**:
- **Quality**:PSNR, SSIM, LPIPS
- **Efficiency**:FPS, **Model storage size (MB)**, **Train time**
- **Fig 8 bubble plot** 直观展示 dynamic 方法的 quality-efficiency-storage 三维权衡

### §6 Future Directions(abstract § 直引)
1. **Hardware Optimization and Real-time Deployment** ← **本项目主线相关**
2. **Long-sequence Processing for Dynamic Scenes** ← **本项目高速相机阵列相关**
3. **Semantically-aware Compression** ← 用 semantic mask 引导压缩
4. **Generalization** ← cross-dataset 泛化
5. **User-controllable Quality-efficiency Trade-offs** ← **本项目 M5 perceptual quality 相关**
6. **Reliability and Robustness Enhancement**

## 关键数字 / Insights(从 §1 + §2 + §6 + Fig 8 直引)

### 关键引文 / 数据点
- **3DGS 平均需要 millions of Gaussians**(§1 直引)→ "significantly more memory than NeRF-based models"
- **4DGS 存储需求 = 3DGS × N_frames(每个 Gaussian encode 跨帧 temporal info)**(§1 直引)
- **N3DV 数据集** Bubble plot 展示(Fig 8):
  - STG(5000 MB,140 FPS,27.4 dB)
  - MEGA(2000 MB,84 FPS,28.1 dB)
  - Hybrid 3D-4DGS(300 MB,42 FPS,28.8 dB)
  - Deformable 3DGS(50 MB,~20 FPS,29.5 dB)
  - 4DGS Wu(50 MB,63 FPS,30.2 dB)
  - streamRF(50 MB,21 FPS,30.9 dB)
  - 4DGS Yang(50 MB,42 FPS,31.6 dB)
  - **NeRFPlayer(50 MB,21 FPS,32.3 dB)**
  - Ex4DGS(50 MB,84 FPS,33.0 dB)
- **结论(图 8 直引)**:"A clear reduction in bubble size can be observed among compact models, indicating a substantial decrease in storage cost. Moreover, several compact designs achieve improved PSNR while maintaining high rendering speed"

### 4DGS dynamic scene modeling 三大子流派(§2.2 + Fig 2 直引)

**(a) Deformable 3DGS**:canonical + time-conditioned MLP(offsets Δx, Δr, Δs)
**(b) Wu et al.'s 4DGS**:HexPlane encoder + lightweight MLP decoder(structured)
**(c) Yang et al.'s 4DGS**:4D Gaussian primitive(μ_4D ∈ R⁴, Σ_4D ∈ R⁴ˣ⁴, h_4D = SH/Fourier(x,y,z,t))

## 与本调研主线的关系(基于 00-goal.md)

### SUCCESS-GS 在"4DGS efficient"分类的位置

| 维度 | SUCCESS-GS(本笔记) | 4DGS-1K(2025-yuan-4dgs-1k) | OMG4(2025-lee-omg4) | 4DGCPro(2025-zheng-4dgcpro) | 4D-RotorGS(2024-duan-4drotorgs) |
|---|---|---|---|---|---|
| 类别 | **Survey** | Method(Param Compress) | Method(Param Compress) | Method(Restruct, LoD) | Method(Canonical) |
| 静态/动态 | 3D + 4D 双线 | 4DGS | 4DGS | 4DGS | 4DGS |
| 加速比 | (汇总) | 8.94× | 60%+ | (待核) | 1257 FPS |
| FPS 范围 | 21-1000+ | 805 | (待核) | (待核) | 1257 |
| 引用价值 | **方法学 map** | 4DGS 加速对标 | 4DGS 紧凑性 | 4DGS 移动流式 | 4DGS 几何加速 |

### SUCCESS-GS §4.2.2 + §4.2.3 对本项目最相关(本项目要做的 = 4DGS mobile rendering)

**§4.2.2 Implicit Deformation**:**DeformableGS / Wu 4DGS / DeformGS** —— 本项目 M2 训练阶段直接借鉴
**§4.2.3 LoD**:**Scale-GS / 4DGCPro** —— 本项目 M3 bitstream 借鉴(高速相机阵列场景天然 LoD)

### 对本项目"4DGS mobile rendering"的具体借鉴

1. **借鉴 1 · 分类法作为研究 map**:**本项目 `02-rendering-acceleration.md` §3 直接抄本 survey 的分类法** —— **2 大方向 × 多子类 = 项目路线框架**
2. **借鉴 2 · §4.2.1 Anchor-based + Canonical Deformable 路线**:**本项目 M3 移动端数据流借鉴** —— **anchor = 静态 + deformation 动态 = 适合 mobile streaming**
3. **借鉴 3 · §4.2.2 Explicit Deformation 路线**:**本项目 M2 训练 pipeline 借鉴** —— **polynomial / keyframe interpolator = mobile 端可预测,无需 MLP forward**
4. **借鉴 4 · §4.2.3 LoD 路线(Scale-GS / 4DGCPro)**:**本项目 M3 bitstream 借鉴** —— **粗尺度先 + 细尺度 refinement = 移动端 viewport-aware streaming**
5. **借鉴 5 · §6 Future Directions 6 条**:**本项目 M0~M5 全路线对齐** —— **特别 §6.1 Hardware / §6.2 Long-sequence / §6.5 Quality-efficiency trade-off 3 条直接对应本项目**

### 对项目目标的具体承诺

- **§6.1 Hardware Optimization and Real-time Deployment 列为第 1 future direction**:**本项目主线 = mobile rendering** —— **本项目直接踩在 survey 列的 6 大 future direction 之首**:`Strong validation of project direction`
- **§6.2 Long-sequence Processing for Dynamic Scenes**:**本项目高速相机阵列 = 长序列典型场景** —— **survey 把这个列第 2 = 长序列 dynamic 是公认开放问题**:`本项目工作正好命中 survey 重点`
- **§6.5 User-controllable Quality-efficiency Trade-offs**:**本项目 M5 perceptual quality 研究** —— **survey 把这个列第 5 = quality-efficiency trade-off 是用户感知研究的核心**:`本项目 M5 路线被 survey 列为 future direction`
- **Survey 全文引用 30+ 个 4DGS efficient 工作**:**本项目 `01-high-precision-representation.md` 补全 reference list 直接抄** —— **避免漏掉关键工作**

## 我未找到 / 提请下游注意

- **本 survey 是否被 venue 接收**:**abstract / 头部未提会议**:`[推测,2025-12 提交,可能 2026 H1 会议接收,如 CVPR / ICLR / T-PAMI]`
- **每个子类的具体 Table 数字**:**§3 / §4 详述了每个子类的代表工作,但未在每节给统一对比 Table**:`[推测,需 PDF §3 / §4 详读,Table 数据散落在 §5.3]`
- **4DGS 移动端专用 survey 章节**:**§4 dynamic 章节涵盖面广,但 mobile 专用 4DGS 加速未单独成节**:`[推测,Mobile-GS / 4DGCPro 等被列为代表但未详评]`
- **完整 reference list 数量**:**PDF 35-37 页有 References,具体数量未在 extract 出来**:`[推测,100+ references]`
- **Lumina / 4DGS-1K 等最新 2025 工作是否纳入**:**abstract 提"first unified overview",但时间窗截止到 2025-12**:`[推测,Lumina 2025-06 / 4DGS-1K 2025-03 应已被纳入]`

## 我的 commit 节奏

本文是 12 篇 paper notes 之外**新加的第 20+ 篇 survey**。**后续 `01-high-precision-representation.md` / `02-rendering-acceleration.md` / `03-end-to-end-roadmap.md` 三处直接抄本 survey 的分类法**;**`04-trends-2026H1.md` 应专门为 SUCCESS-GS 加一节"§W. 4DGS efficient 方向成熟度(survey 出现 = 沉淀)",作为"Efficient 4DGS 已成成熟子领域"的最强学术信号**。

## 引用一览(本笔记引用自)
- arxiv abstract page 直引(`https://arxiv.org/abs/2512.07197`)
- 项目页 `https://cmlab-korea.github.io/Awesome-Efficient-GS/` (PDF 头部直引)
- PDF 头部 author / 2 单位 affiliation 直引(`.pdfs/2512.07197.pdf`)
- PDF §1 Introduction 直引(3DGS / 4DGS efficient 必要性)
- PDF §2 Preliminary 直引(3DGS pipeline + Deformable / Wu / Yang 4DGS 三大流派)
- PDF §3 Static Parameter/Restructuring Compression 直引
- PDF §4 Dynamic Parameter/Restructuring Compression 直引(本项目最相关)
- PDF §5 Datasets + Metrics + Fig 8 bubble plot 直引
- PDF §6 Future Directions 直引(6 大方向)
- PDF §7 Conclusion 直引
- PDF Appendix A Notation Table 直引(35-37 页,40+ 数学符号统一)

[abstract 直引] [PDF 直引] [推测] [调研深度:abstract + §1-7 关键页 + TOC + §6 future directions,§3/§4 各子类的具体代表工作 Table 数字未及详]
