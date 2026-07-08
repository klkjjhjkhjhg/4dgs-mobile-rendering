# Venues — 3DGS / 4DGS / Mobile Rendering 调研白名单

> 用途：每篇 paper note 的 `venue:` 字段引用本表。**所有 49 篇 note + 后续扩的 note 都按本表分级**。
>
> 维护：每次新接收的 paper → 立刻改对应 note 的 `venue:` 字段 + 更新本表。

---

## Tier 1 — 计算机视觉（必读）

| 缩写 | 全称 | 节奏 | 检索方式 |
|------|------|------|----------|
| CVPR | IEEE/CVF Conference on Computer Vision and Pattern Recognition | 6 月 | openaccess.thecvf.com/menu |
| ICCV | International Conference on Computer Vision | 10 月（奇数年）| openaccess.thecvf.com/menu |
| ECCV | European Conference on Computer Vision | 10 月（偶数年）| www.ecva.net/papers.php |

## Tier 1 — 图形学（必读）

| 缩写 | 全称 | 节奏 | 检索方式 |
|------|------|------|----------|
| SIGGRAPH | ACM SIGGRAPH | 8 月 | dl.acm.org |
| SIGGRAPH Asia | ACM SIGGRAPH Asia | 12 月 | dl.acm.org |

## Tier 1 — 机器学习（必读）

| 缩写 | 全称 | 节奏 | 检索方式 |
|------|------|------|----------|
| NeurIPS | Conference on Neural Information Processing Systems | 12 月 | papers.nips.cc |
| ICLR | International Conference on Learning Representations | 5 月 | openreview.net |
| ICML | International Conference on Machine Learning | 7 月 | proceedings.mlr.press |

## Tier 1 — 体系结构（必读）— 跨方向高价值

| 缩写 | 全称 | 节奏 | 检索方式 |
|------|------|------|----------|
| ASPLOS | Intl Conf on Architectural Support for Programming Languages and Operating Systems | 3 月 | dl.acm.org |
| ISCA | Intl Symposium on Computer Architecture | 6 月 | dl.acm.org |
| MICRO | Intl Symposium on Microarchitecture | 11 月 | dl.acm.org |
| HPCA | Intl Symposium on High-Performance Computer Architecture | 2 月 | ieeexplore.ieee.org |

## Tier 2 — AI 综合（必读）

| 缩写 | 全称 | 节奏 | 检索方式 |
|------|------|------|----------|
| AAAI | AAAI Conference on Artificial Intelligence | 2 月 | ojs.aaai.org |
| IJCAI | Intl Joint Conference on Artificial Intelligence | 8 月 | www.ijcai.org |

## Tier 2 — 3D 视觉专项（必读）

| 缩写 | 全称 | 节奏 | 检索方式 |
|------|------|------|----------|
| 3DV | International Conference on 3D Vision | 11 月 | ieeexplore.ieee.org |
| ICCP | Intl Conf on Computational Photography | 5 月 | ieeexplore.ieee.org |

## Tier 2 — 期刊（必读）

| 缩写 | 全称 | 节奏 | 检索方式 |
|------|------|------|----------|
| ACM TOG | ACM Transactions on Graphics | 季刊 | dl.acm.org/toftog |
| IEEE TVCG | IEEE Transactions on Visualization and Computer Graphics | 月刊 | ieeexplore.ieee.org |
| TPAMI | IEEE Trans on Pattern Analysis and Machine Intelligence | 月刊 | ieeexplore.ieee.org |
| IJCV | International Journal of Computer Vision | 月刊 | link.springer.com |

## Tier 2 — 设计自动化（跨方向，高价值）

| 缩写 | 全称 | 节奏 | 检索方式 |
|------|------|------|----------|
| DAC | Design Automation Conference | 6 月 | ieeexplore.ieee.org |
| ICCAD | Intl Conf on Computer-Aided Design | 11 月 | ieeexplore.ieee.org |

## Tier 2 — 移动系统（跨方向，高价值）

| 缩写 | 全称 | 节奏 | 检索方式 |
|------|------|------|----------|
| MobiSys | Intl Conf on Mobile Systems, Applications, and Services | 6 月 | dl.acm.org |
| MobiCom | Intl Conf on Mobile Computing and Networking | 10 月 | dl.acm.org |

## Tier 3 — 编译器（选读）

| 缩写 | 全称 | 节奏 | 检索方式 |
|------|------|------|----------|
| CGO | Intl Symp on Code Generation and Optimization | 2 月 | ieeexplore.ieee.org |

---

## Cross-disciplinary（跨方向，单篇必读）

> 收录标准：**算法 + 架构 / 系统双优化**的少数工作，数量少但每篇都精读。
> 优先级高于本表任何 Tier。

| 标题 | arxiv | 作者组 | 主页 | 状态 |
|------|-------|--------|------|------|
| Lumina | 2506.05682 | Feng et al. | 暂无公开主页（arxiv-only）| under review / venue unknown |

**豁免规则**：Cross-disciplinary 栏允许**仅 arxiv 收录**（不强求主页），但 `venue:` 字段必须标"under review / venue unknown"。

---

## Pre-print（含完整 demo 主页 / 代码 / 主页 任一即可）

> 收录标准（**宽松版**）：
> 1. 已在 arxiv 公开
> 2. **有主页即可**（代码 / demo / 视频任一，非全部强制）
> 3. 来自 Tier 1/2 作者组的代表性工作，**或 GitHub awesome 列表收录**
> 4. **正在投 / 审稿中** → `venue:` 字段标 `under review`
> 5. **接收后立即升级 `venue:` 字段 + 移入正式栏**

| 标题 | arxiv | 作者组 | 主页 | 状态 |
|------|-------|--------|------|------|
| _（待收录）_ | — | — | — | — |

---

## 1-hop 引用规则

> **目的**：扫 references 既是补全高质量论文（防漏），又是画研究脉络（杠杆化体力活）。

**触发**：找到一篇高质量论文（Tier 1/2 接收 OR Pre-print 栏已收 OR Cross-disciplinary）。

**操作**：
1. 读它的 references（arxiv / OpenReview / DOI / Semantic Scholar）
2. **逐条读 references 的题目**（**不是关键词匹配，是人工判断**）→ 判断是否相关
3. **相关判定主题**：
   - 3DGS / 4DGS 渲染加速
   - 移动端 / 端侧推理
   - 神经渲染 / 神经场压缩
   - 渲染性能优化（kernel / 内存 / 带宽）
4. 相关的 → 走**正常收录流程**（搜 PDF + 写 paper note + INDEX + 白名单）—— **跟会议扫到的论文完全同等对待**
5. **不向下追 references**（一跳即停）—— 防止膨胀

**目标产能**：每次扫到高质量论文，预期 **+3-8 篇 note**（不是 +20）。

**注意**：
- 题目里出现 "Survey" / "Review" / "Tutorial" → 不索引（综述类不直接追）
- 已经在 INDEX 里的 → 不重复
- 题目含 "for autonomous driving" / "for medical" / "for SLAM" 等场景词 → 标 [domain-specific]，**除非**与移动端加速直接相关

**Lumina 30 references 验证**（2026-07-08 完成）：
- 30 总 references → 23 不相关（医学 / 自动驾驶 / SLAM / 任务规划 / 行人预测 等）→ 7 核心相关
- 7 核心相关：**3DGS / Splatfacto / Mip-Splatting / Scaffold-GS / 4DGS / 4DGS-CC / Mobile-GS**
- **7 条 100% 已在 INDEX** → 0 新增
- **结论**：49 篇 INDEX 质量密度被验证 = 调研齐全

---

## 检索工作流

| 场景 | 命令 / 入口 |
|------|-------------|
| 每周新 paper 扫描（**arXiv 扫**）| arxiv listing/cs.CV + listing/cs.GR + 关键词 "Gaussian Splatting" |
| 会议接收名单（**会议扫**）| openaccess.thecvf.com/menu / openreview.net / dl.acm.org |
| ICLR / NeurIPS 审稿意见 | openreview.net/forum?id=... |
| CVPR / ICCV 接收名单 | openaccess.thecvf.com/menu |
| SIGGRAPH | dl.acm.org 搜 "Gaussian Splatting" |
| 体系结构接收名单 | iscaconf.org / microarch.org / asplos.org |

---

## 维护规则

1. **新 paper 接收**：立刻改对应 note 的 `venue:` 字段，并加到本表
2. **跨方向工作**：归到 Cross-disciplinary 栏
3. **白名单增删**：本文件 PR review，理由写明
4. **Cron 升级机制**：详见 `docs/05-survey-methodology.md` §5
