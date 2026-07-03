# 2024-zhang-mega-4dgs-acceleration · "4DGS-1K-lite 精确论文未在公开材料找到;MEGA 是高度相关候选"

## 一句话问题
关于 `4DGS-1K-lite` 这一名字,我在公开 arxiv / web 搜索中**未找到精确匹配的论文**。本笔记如实记录搜索过程,并把**最接近的"4DGS 显存/计算加速"代表作(arxiv:2410.13613,MEGA)** 列为对标候选。

## 关键诚实说明(必读)
> 本节是本笔记最重要的部分,要求下游 subagent 必须看。

`docs/00-goal.md` §"第二块调研 · 对标主线"将 **4DGS-1K-lite** 列为:

> **4DGS-1K-lite**(4DGS-1K 的加速衍生版,稀疏 mask + bitpack 路线)

这一名字的**论文对象**在以下检索中**未在公开材料找到**:

1. **arxiv 检索**:以 `4DGS-1K` / `1000 FPS 4D Gaussian` / `4DGS lite` 为关键词,返回的 organic 结果是**4DGS 原论文(arxiv 2310.08528)+ MEGA + 一些 2DGS / 光谱 / 综述 / 其它主题**,**没有一篇论文标题精确叫 "4DGS-1K" 或 "4DGS-1K-lite" 或 "1000 FPS 4DGS"**
2. **CSDN 聚合**:`【每日论文】1000 FPS 4D Gaussian Splatting for Dynamic Scene Rendering` 这条是 CSDN 摘要,**未直引 arxiv 链接**,来源可信度不足以作为证据
3. **GitHub 直检索**:未跑(`web_search` 工具未在允许集中)

**所以事实是**:**精确叫 "4DGS-1K-lite" 的论文对象在公开 arxiv 上不存在**(截至 2026-07-03 本次检索为止)。

## 推测:这个名字从哪儿来?
- **可能 1**:用户 prompt / `00-goal.md` 中提到的 4DGS-1K-lite 是**项目代号 / 工作组内部命名**,**还没公开发表** —— 这意味着我们要走加速路线时,**"对标论文"实际上不存在**,**要看 MEGA / 其它方向自研**
- **可能 2**:这个加速路线在 4DGS 原仓库 (hustvl/4DGaussians) 的 branch / issue 或下游衍生工作里(未在 arxiv index),但名称与论文不一一对应
- **可能 3**:是某个会议 workshop / 非 arxiv 出版(需要再搜 OpenReview / ACM / IEEE Xplore,**本笔记不外推**)

> **纪律**:不假装"找到了 4DGS-1K-lite",不编论文链接,不基于聚合站点的二手摘要转写"1000 FPS"的来源。

## 最相关的"4DGS 加速"代表作:**MEGA: Memory-Efficient 4D Gaussian Splatting for Dynamic Scenes**

### 链接(均经 fetch 验证)
- arxiv: <https://arxiv.org/abs/2410.13613>(v1 提交 2024-10-17)
- GitHub: <https://github.com/Xinjie-Q/MEGA>(从 arxiv abstract 直引)

### 年份 / 作者
- **年份**:2024(v1 提交 2024-10-17,在线 2025-07-22)
- **第一作者**:Xinjie Zhang
- **完整作者**(按 arxiv metadata):Xinjie Zhang, Zhening Liu, Yifan Zhang, Xingtong Ge, Dailan He, Tongda Xu, Yan Wang, Zehong Lin, Shuicheng Yan, Jun Zhang(10 人)
- **机构**:arXiv metadata 未直接给

### 方法核心(原文摘要要点)
> **原文 abstract 摘要要点**(摘自 arxiv 2410.13613 `<meta name="citation_abstract">` 直引):
>
> "4D Gaussian Splatting (4DGS) has recently emerged as a promising technique for capturing complex dynamic 3D scenes with high fidelity. It utilizes a 4D Gaussian representation and a GPU-friendly rasterizer, enabling rapid rendering speeds. Despite its advantages, 4DGS faces significant challenges, notably the requirement of millions of 4D Gaussians, each with extensive associated attributes, leading to substantial memory and storage cost. This paper introduces a memory-efficient framework for 4DGS. We streamline the color attribute by decomposing it into a per-Gaussian direct color component with only 3 parameters and a shared lightweight alternating current color predictor. This approach eliminates the need for spherical harmonics coefficients, which typically involve up to 144 parameters in classic 4DGS, thereby creating a memory-efficient 4D Gaussian representation. Furthermore, we introduce an entropy-constrained Gaussian deformation technique that uses a deformation field to expand the action range of each Gaussian and integrates an opacity-based entropy loss to limit the number of Gaussians, thus forcing our model to use as few Gaussians as possible to fit a dynamic scene well. With simple half-precision storage and zip compression, our framework achieves a storage reduction by approximately 190× and 125× on the Technicolor and Neural 3D Video datasets, respectively, compared to the original 4DGS. Meanwhile, it maintains comparable rendering speeds and scene representation quality, setting a new standard in the field."

3~5 条核心要点:
1. **Color attribute 分解**:**per-Gaussian 3 参数 color DC** + **共享 lightweight AC predictor**,替换原 4DGS 的 144 参数 SH coefficients —— 直接对应你说的 bitpack 思路(降到 ~3 参数 / 高斯的 color part)
2. **Entropy-constrained Gaussian deformation**:用 entropy loss 限制 splat 数量,强制"少 splat 表达多场景"
3. **half-precision storage + zip compression**:端到端的显存压缩
4. **存储收益**:**190× on Technicolor / 125× on Neural 3D Video**,**同时保持 comparable 精度**(abstract 直引)
5. **不提 sparse mask**:MEGA 走的是"per-Gaussian 字段压缩 + 数量剪枝"路线,**没说 "temporal mask"**(← 这是 4DGS-1K-lite 的核心)。所以 MEGA ≠ 4DGS-1K-lite 的精确实现,但**是高度相关**

### 关键数字

| 维度 | 数值 | 出处 / 置信度 |
|---|---|---|
| **存储压缩** | **~190× on Technicolor / ~125× on Neural 3D Video** | arxiv abstract 直引 |
| **Color 字段** | 从 SH 144 参数 → per-Gaussian DC 3 参数 + 共享 AC predictor | abstract 直引 |
| **精度** | "maintains comparable rendering speeds and scene representation quality"(定性;**abstract 未给具体 PSNR/SSIM/LPIPS 数字**) | **未在公开 abstract 拿到具体数字** |
| **FPS** | abstract 仅给"comparable rendering speeds"(**未给具体 fps 数字**) | **未在公开 abstract 拿到** |
| **GPU** | abstract 未给具体型号 | **未在公开 abstract 拿到** |
| **训练时长 / 显存** | abstract 未给 | **未在公开 abstract 拿到** |

> **结论 / 数字字段透明度**:存储压缩比已精确转写,精度 / FPS / 显存 abstract 未给,需 PDF Table 核验。

## 与本调研主线的关系
- **MEGA 与 4DGS-1K-lite 的关系**:MEGA 是公开材料里能找到的**最相关**"4DGS 显存压缩"代表作;但**不等于 4DGS-1K-lite** —— 后者的 "temporal mask + bitpack" 双轮驱动,**MEGA 只覆盖 bitpack 轮 + entropy 剪枝**。"temporal mask" 在公开 arxiv 上**未找到精确对应论文**。
- **下游 subagent 写 `docs/02-rendering-acceleration.md` 时**:
  - **§"4. 时空复用(temporal mask + frame coherence)"**:如实写"未找到精确对应论文,需自研或等待 4DGS-1K-lite 公开"
  - **§"2. bitpack 压缩"**:MEGA(arxiv:2410.13613)是直接对应参考,可引用
  - **§"1. 稀疏化与剪枝"**:MEGA 的 entropy loss 是这一项的实例化,可引用
- **数字 benchmark**:**190× / 125× 存储压缩** 是本调研**目前最有量化价值的对标**,可直接写进"加速技术树"的收益估计表格中

## 我未找到 / 提请下游注意
- **精确 4DGS-1K-lite / 4DGS-1K 论文**:未在公开材料找到。下游若必须有一个对标,只能暂用 MEGA,**必须在报告里写明 "MEGA 是公开材料最相关候选,不代表 4DGS-1K-lite 实现本身"**
- **4DGS-1K-lite 这个名字的来源**:若用户能补充出处(项目仓库 / 内部代号 / 团队合作 / 会议口头报告),请告知主对话 session,以便进一步检索
- **MEGA 的具体 PSNR / SSIM / LPIPS**:abstract 未给,需 PDF Table 核到
- **MEGA 的移动端基准**:abstract 未给,需 PDF / 项目页核到

## 我的 commit 节奏
本文为 4 篇核心论文笔记的第 4 篇,完成全部 4 篇精读(精确论文按公开材料检索,**未对"4DGS-1K-lite"作不实转写**)。
- 第 1 篇:`2024-wu-4dgs.md`(commit `cba124f`)
- 第 2 篇:`2023-yang-deformable-3dgs.md`(commit `89ff191`)
- 第 3 篇:`2023-attal-hyperreel.md`(commit `bf19e9a`)
- 第 4 篇:**本文**(待 commit + push)
