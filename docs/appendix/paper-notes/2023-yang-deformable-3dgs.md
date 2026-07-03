# 2023-yang-deformable-3dgs · Deformable 3D Gaussians for High-Fidelity Monocular Dynamic Scene Reconstruction

## 一句话问题
如何用 **3D Gaussian Splatting + canonical + deformation** 范式,在**单目视频**输入下重建出可实时渲染的动态 3D 场景?

## 链接(均经 fetch 验证)
- arxiv: <https://arxiv.org/abs/2309.13101>(v1 提交于 2023-09-22)
- GitHub: arxiv abstract 未直接列出仓库页,**未在公开材料找到** —— 不外推

## 年份 / 作者
- **年份**:2023(arxiv v1 提交)+ 2024(CVPR 录用,推测,需下游从 CVPR 2024 论文集再确认)
- **第一作者**:Ziyi Yang(杨子逸)
- **完整作者**:Ziyi Yang, Xinyu Gao, Wen Zhou, Shaohui Jiao, Yuqing Zhang, Xiaogang Jin(6 人,顺序按 arxiv metadata)
- **机构**:arXiv metadata 未给;**未在公开材料核到机构**,不外推

## 方法核心(原文摘要直引 + 简短整理)
> **原文 abstract 摘要要点**(摘自 arxiv 2309.13101 `<meta name="citation_abstract">` 直引):
>
> "Implicit neural representation has paved the way for new approaches to dynamic scene reconstruction and rendering. Nonetheless, cutting-edge dynamic neural rendering methods rely heavily on these implicit representations, which frequently struggle to capture the intricate details of objects in the scene. Furthermore, implicit methods have difficulty achieving real-time rendering in general dynamic scenes, limiting their use in a variety of tasks. To address the issues, we propose a deformable 3D Gaussians Splatting method that reconstructs scenes using 3D Gaussians and learns them in canonical space with a deformation field to model monocular dynamic scenes. We also introduce an annealing smoothing training mechanism with no extra overhead, which can mitigate the impact of inaccurate poses on the smoothness of time interpolation tasks in real-world datasets. Through a differential Gaussian rasterizer, the deformable 3D Gaussians not only achieve higher rendering quality but also real-time rendering speed. Experiments show that our method outperforms existing methods significantly in terms of both rendering quality and speed, making it well-suited for tasks such as novel-view synthesis, time interpolation, and real-time rendering."

3~5 条核心要点:
1. **canonical space + deformation field**(同 4DGS 的范式,但输入约束只单目相机)
2. **deformation field** 学习从 canonical 3D 高斯到各时间戳的形变(位姿 / 旋转 / 尺度 / 不透明度的扰动)
3. **annealing smoothing training mechanism** 缓解 pose estimation 误差对时间插值的传播
4. **differential Gaussian rasterizer** 复用 3DGS 光栅化器,继承 3DGS 的实时性
5. **单目输入**(monocular) —— 这与 4DGS 要求多视角相机阵列**相反**,这是个**反例标定**:本论文说明"单目路线可达,"但**单目精度不满足"高精度场景重建"**;本调研主目标"多视角相机阵列 + 高精度 SfM"会选择 4DGS / 多视角路线

## 关键数字
> 以下数字严格从 arxiv abstract / 摘要中可拿到的部分转写;**没在公开材料中核到的部分不写**。

| 维度 | 数值 | 出处 / 置信度 |
|---|---|---|
| **输入约束** | 单目相机(monocular) | arxiv abstract 直引:"model monocular dynamic scenes" |
| **精度** | "outperforms existing methods significantly in terms of both rendering quality and speed"(定性陈述,**未在公开 abstract 看到具体 PSNR/SSIM/LPIPS 数字**) | **需下游从论文 Table / 实验章节读取**,本笔记不外推 |
| **FPS** | "real-time rendering speed" —— 阈值性,abstract 无具体 fps 数字 | **未在公开 abstract 拿到具体 fps** |
| **训练 GPU / 训练时长** | **未在 abstract 拿到** | **未在公开 abstract 拿到** |
| **per-splat 资源体积** | abstract 未给 | **未在公开 abstract 拿到** |
| **与 3DGS 的差异** | deformation field 是额外参数(MLP) | 推测,需下游核验 |

> **结论 / 数字字段透明度**:abstract 未给出 PSNR 数字,**未在公开 abstract 拿到具体精度**。下游 subagent 在 `01-high-precision-representation.md` 引用本论文时**必须从 arxiv PDF 实验章节精确抄数字**,不要用"outperforms significantly"作为精度数据。

## 与本调研主线的关系(基于 prompt 00-goal.md)
- **反例标定 / 横向参照**:
  - **`docs/00-goal.md` §"对标主线"明确列出了 "Dynamic 3DGS(Yang et al.)"**。**注意:可能存在两个 "Yang"**:用户 prompt 文字"`Yang et al.`"**对得上本篇(Ziyi Yang et al.)**,因为本篇就是 Ziyi Yang 一作。
  - **另一篇 "Deformable 3DGS"也叫 Yang(不同组):** 用户 / prompt 可能还会让人摸 错 —— **本笔记明确锁定 Deformable 3DGS = arxiv 2309.13101**,不混。
- **"动态场景"路线对比**:
  - 4DGS(Wu et al.,多视角):HexPlane + canonical + deformation
  - Deformable 3DGS(本篇,**单目**):canonical + deformation,无 HexPlane
  - **单目 vs 多视角**:本调研主目标"多视角相机阵列 + 高精度 SfM"在采集端**反推**:Deformable 3DGS **不能作为高精度采集方案**(单目精度天花板低);但其 deformation field 设计是**低成本动态扩展**的候选思路,可在场景的"动起来"那块被借鉴。
- **不可作为移动端最终方案**:real-time 但**桌面 GPU 数字**,未给出 Adreno / 手机数字。**反例基准**:不是移动端方案。

## 我未找到 / 提请下游注意
- **GitHub 仓库**:arxiv abstract 末尾未列,**未在公开 abstract 拿到仓库 URL**。下游需用 google 检索"`Deformable 3D Gaussians` github"独立确认。
- **PSNR / SSIM / LPIPS 具体数字**:需要从 PDF Table 转写。
- **训练 GPU / 时长**:需从 Section 4 / Appendix 实验描述核到。
- **per-splat 资源体积**:需用实际模型体积估算工具跑。
- **CVPR 录用确认**:我推测 2024,但**未在 arxiv 拿到 acceptance 信息**,下游需从 OpenAccess / dblp 再核。

## 我的 commit 节奏
本文为 4 篇核心论文笔记的第 2 篇(本仓库 `docs/appendix/paper-notes/` 第 2 个 .md)。
- 第 1 篇:`2024-wu-4dgs.md` (commit `cba124f`,已 push)
- 第 2 篇:**本文**(待 commit + push)
