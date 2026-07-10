# 2026-liao-sharptimegs · SharpTimeGS: Sharp and Stable Dynamic Gaussian Splatting via Lifespan Modulation

> **相关性**:**⭐⭐ 中相关(4DGS 动态质量 + lifespan-aware,2026-02)** —— **核心数字**:"achieves state-of-the-art performance while supporting real-time rendering **up to 4K resolution at 100 FPS on one RTX 4090**"(abstract 直引);**lifespan parameter 重新设计 4DGS 静态 / 动态区域表示**;**Tsinghua University 团队**。

> **⚠ 重要边界声明**:**SharpTimeGS 是 4DGS(动态)工作**,**本项目主线命中**。**核心创新是 lifespan-aware 4DGS 框架**:**learnable lifespan parameter 重新设计时序 visibility**(从 Gaussian-shaped decay → flat-top profile),**decoupling motion magnitude from temporal duration**。

## 0.5 元数据

- **venue**: arxiv pre-print (2026-02)
- **arxiv-id**: 2602.02989
- **s2-id**: （v2 用 Semantic Scholar API 补全）
- **homepage**: （无）
- **github**: （无）
- **status**: under review
- **收录日期**: 2026-07-08
- **收录来源**: arxiv scan + 1-hop 引用规则
- **1-hop 引用**: （v2 补全，见 §11 1-hop 关系图）
- **评级**: ⭐⭐

- **survey_section**: 4
## 一句话问题

4DGS 现有方法难以平衡"长时静态区域"与"短时动态区域"在 representation + optimization 两方面。**如何用一个 unified 4DGS 框架,通过 lifespan parameter 自动调节静态 / 动态区域,既保持 long-term stability 又不妥协 dynamic fidelity**?

## 链接(均经 fetch + PDF 实测)
- arxiv: <https://arxiv.org/abs/2602.02989>(v1 提交 2026-02-04)
- **项目页**:`https://liaozhanfeng.github.io/SharpTimeGS`(abstract 直引)
- PDF: 已下 `.pdfs/2602.02989.pdf`(28 MB)

## 年份 / 作者 / 机构(PDF 头部实测)
- **年份**:2026
- **作者**(按 arxiv metadata 头部):**Zhanfeng Liao¹, Jiajun Zhang², Hanzhang Tu¹, Zhixi Wang¹, Yunqi Gao⁴, Hongwen Zhang³, Yebin Liu*¹**
- **机构**(PDF 头部直引):
  1. **Tsinghua University (清华大学)**
  2. **Beijing University of Posts and Telecommunications (北京邮电大学)**
  3. **Beijing Normal University (北京师范大学)**
  4. **Central China Normal University (华中师范大学)**

## 方法核心(abstract + §1 直引)

### 三大创新(abstract § 直引)
1. **Lifespan parameter**:"reformulates temporal visibility from a **Gaussian-shaped decay into a flat-top profile**, allowing primitives to remain consistently active over their intended duration and avoiding redundant densification"
2. **Lifespan-modulated motion**:"reduces drift in long-lived static points while retaining unrestricted motion for short-lived dynamic ones. This **effectively decouples motion magnitude from temporal duration**, improving long-term stability without compromising dynamic fidelity"
3. **Lifespan-velocity-aware densification**:"mitigates optimization imbalance between static and dynamic regions by allocating more capacity to regions with pronounced motion while keeping static areas compact and stable"

### 关键概念:Flat-Top Profile(abstract + §3 直引)
> "learnable lifespan parameter that **reformulates temporal visibility from a Gaussian-shaped decay into a flat-top profile**, allowing primitives to remain consistently active over their intended duration"

> 解耦的语义含义:
> - **传统 Gaussian-shaped decay** = 短生命周期 Gaussians 不可避免,长生命周期 Gaussians 会被压缩
> - **Flat-top profile** = Gaussians 在 lifespan 内保持 active,不在 lifespan 内归零
> - **解耦 motion magnitude from temporal duration** = 静态点不漂移,动态点运动不受限

### Densification Strategy(abstract § 直引)
> "**lifespan-velocity-aware densification strategy** that mitigates optimization imbalance between static and dynamic regions by **allocating more capacity to regions with pronounced motion while keeping static areas compact and stable**."

## 关键数字(abstract 直引)
- **核心 1**:"real-time rendering **up to 4K resolution at 100 FPS on one RTX 4090**"
- **核心 2**:"state-of-the-art performance"(abstract § 直引)
- **具体 PSNR / FPS / storage Table 数字**:**abstract 未给 Table 数字**(`abstract 未给 Table 数字,需 PDF §4 核`)

### 评测 benchmarks(abstract § 直引)
> "Extensive experiments on multiple benchmarks demonstrate that our method achieves state-of-the-art performance..."

## 与本调研主线的关系(基于 00-goal.md)

### 这与 4DGS dynamic fidelity / stability 派的方法学对照

| 维度 | SharpTimeGS(本笔记) | 4DGS-1K(5 号) | SpeeDe3DGS(本批 12 号) | 4D-RotorGS(2024-duan-4drotorgs) |
|---|---|---|---|---|
| 4D 适配 | ✅ 4DGS | ✅ | ✅ | ✅ |
| 关键机制 | **lifespan parameter + flat-top profile + velocity-aware densification** | STV + mask | TSP + TSS + GroupFlow | canonical rotation |
| 加速比 | 100 FPS @ 4K | 1000+ FPS @ N3V | **13.71× faster** | 1257 FPS @ D-NeRF |
| 焦点 | **静态 / 动态 fidelity 平衡** | 剪枝 + 加速 | temporal pruning + grouping | 几何加速 |
| 单位 | **Tsinghua + 3 others** | NUS | UMD | (推测) |
| Mobile 实测 | ❌(RTX 4090) | ❌(TITAN X 200+) | ❌ | ❌ |

> **关键洞察**:**SharpTimeGS 与本项目"高速相机阵列预制高密度场景 + 端侧流式播放"工作流直接相关**:
> - **高速相机阵列 1000 fps × 60 秒 = 60,000 帧** = **长时静态 + 短时动态共存**(静态背景 60 秒 + 动态对象短时)
> - **SharpTimeGS 的 lifespan 机制**:**特别适合这种"长时静态 + 短时动态"场景** —— **本项目 M2 训练阶段直接借鉴**

### 对本项目"4DGS mobile rendering"的具体借鉴

1. **借鉴 1 · Lifespan parameter**:**本项目 M2 训练 pipeline 直接借鉴** —— **高速相机阵列长序列可用 lifespan 标记"静态 vs 动态"边界**
2. **借鉴 2 · Flat-top profile**:**本项目 M3 bitstream 压缩借鉴** —— **flat-top 比 Gaussian decay 更稳定,解码质量更稳**
3. **借鉴 3 · Lifespan-velocity-aware densification**:**本项目 M2 训练借鉴** —— **避免长时静态区域过度 densification,节省 Gaussians**

### 对项目目标的具体承诺

- **"100 FPS @ 4K on RTX 4090"**:**桌面 GPU 实时 4K**;**Snap 8 Gen 4 估算约 25-50 FPS at 1080p**(`[推测,基于 Adreno 算力约 RTX 4090 的 1/8-1/4]`)—— **本项目 M4 目标"60 FPS @ 1080p on Snap 8 Gen 4" 接近可达**
- **SOTA quality**:**本项目 M5 perceptual quality 借鉴** —— **平衡静态 / 动态区域,改善用户感知**
- **Lifespan decoupling**:**本项目 M5 阶段用户研究借鉴** —— **长时静态不漂移 = 视觉稳定性**

## 我未找到 / 提请下游注意

- **Mobile GPU 实测**:**abstract / §1 未提 mobile**(`未在公开 abstract 拿到 mobile GPU 型号`)
- **Vulkan 实现**:**abstract 未提 Vulkan**(`未在公开 abstract 拿到具体 mobile API`)
- **完整 Table 数字**:**abstract 未给 PSNR / FPS / bitrate 详细 Table**(`abstract 未给 Table 数字,需 PDF §4 核`)
- **Lifespan parameter 具体形式**:**abstract 提"learnable"但未给公式**(`abstract 未给 lifespan 公式,需 PDF §3 核`)
- **4D 适配到 4DGS deformation field**:**abstract 提"4D Gaussian"但未明示如何与 deformation field 集成**(`abstract 未给 4DGS deformation 集成方案`)

## 我的 commit 节奏

本文是 12 篇 paper notes 之外**新加的第 20+ 篇**,**第 N 篇 4DGS dynamic quality 类笔记**(本批 11 号)。**后续 `02-rendering-acceleration.md` §3 应加 SharpTimeGS 一行**;**`03-end-to-end-roadmap.md` 应专门为 SharpTimeGS 加一节"§Y. 4DGS lifespan-aware 路径(SharpTimeGS flat-top profile + velocity-aware densification)"**,作为"4DGS 静态 / 动态 fidelity 平衡"的最直接学术先例。

## 引用一览(本笔记引用自)
- arxiv abstract page 直引(`https://arxiv.org/abs/2602.02989`)
- 项目页 `https://liaozhanfeng.github.io/SharpTimeGS` (abstract 直引)
- PDF 头部 author / 4 单位 affiliation 直引(`.pdfs/2602.02989.pdf`)
- PDF §1 intro 直引(传统 dynamic NVS 背景)
- PDF §3 lifespan + flat-top 直引(公式需 PDF §3 核)

[abstract 直引] [PDF 直引] [推测] [调研深度:abstract + §1 + 项目页,§3 公式 + §4 Table 数字未及]
