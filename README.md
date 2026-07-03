# 4DGS Mobile Rendering

调研仓库:**在 Android 高通旗舰 GPU 上实时渲染 动态 4D Gaussian Splatting**。

> 远端仓库(待 GitHub auth 完成后创建):`klkjjhjkhjhg/4dgs-mobile-rendering`(private)
> 详细调研目标 / 硬约束 / 必覆盖 / 产出要求,见 [`docs/00-goal.md`](./docs/00-goal.md)

## 目录

- [`docs/00-goal.md`](./docs/00-goal.md) — 调研目标 spec(由主对话 session 写入)
- `docs/01-high-precision-representation.md` — 第一块调研:**高精度 4DGS 表示**(占位)
- `docs/02-rendering-acceleration.md` — 第二块调研:**渲染加速**(占位)
- `docs/03-end-to-end-roadmap.md` — 整合路线图(占位)
- `docs/appendix/`
  - `paper-notes/` 关键论文精读笔记
  - `collection-sop.md` 采集 SOP 草案(占位)
  - `vulkan-impl-notes.md` Vulkan 1.3 实现细节笔记(占位)
- `references/` 参考文献
- `experiments/` 实验脚本(mask / bitpack / sort / upscale)
- `assets/` 图片 / 流程图 / 表格

## 现状

| 项 | 状态 |
|---|---|
| 本地仓 | ✅ `~/Codes/4dgs-mobile-rendering/`,主分支 `main` |
| 远端 GitHub 仓库 | ✅ `klkjjhjkhjhg/4dgs-mobile-rendering`(private),9 commits pushed |
| 调研目标 spec | ✅ `docs/00-goal.md` |
| 高精度 4DGS 表示 | ✅ `docs/01-high-precision-representation.md` |
| 渲染加速(Vulkan 1.3 移动端) | ✅ `docs/02-rendering-acceleration.md` |
| 整合路线图(6 个月 M0~M6) | ✅ `docs/03-end-to-end-roadmap.md` |
| 4 篇核心论文精读 | ✅ `docs/appendix/paper-notes/`(Wu 4DGS / Yang Deformable / Attal HyperReel / Zhang MEGA) |
| 采集 SOP / Vulkan 笔记 | ✅ `docs/appendix/{collection-sop, vulkan-impl-notes}.md`(指针型,内容沉在主体文档) |

### 关键调研结论(速读)

**主线**(高精度表示):`Wu-4DGS`(canonical + HexPlane + deformation) + `MonST3R` 动态 SfM,公开数字 `[abstract 直引] 82 FPS @ 800×800 on RTX 3090`。

**备选 1**:`Deformable 3DGS`(Yang 2023),单目路线,精度上限低。

**备选 2**:`MEGA` 训练路径(arxiv:2410.13613,Zhang 2024),`[abstract 直引]` 提供 `~190× storage(Technicolor)/125×(N3V)` 的存储压缩(目标值,本数据集上待验)。

**加速技术树**(7 步全链 + 收益估计 + 质量损失):见 `docs/02-rendering-acceleration.md` §1,每步数字均带 `[推测]` 或 `[调研不足]` 标记。

**核心风险**:`4DGS-1K-lite` 公开论文**未在公开材料找到**;Adreno 8 Gen 4 上 4DGS FPS baseline = 0;**未在 public 找到任何 mobile 4DGS 实测**。完整 ≥ 5 项风险见 `docs/02-rendering-acceleration.md` §9。

### 调研纪律(贯穿)

- `facts/discovery/never-fabricate-history`:`绝不瞎编历史`,数字 / 链接 / 仓库名 / 文件路径 / 论文标题,**未在公开材料核到的写 "未在公开 abstract 拿到"**,**绝不据二手综述 / CSDN 转贴转写为已验证数字**
- 每条结论标 `[abstract 直引]` / `[基于 X 论文]` / `[推测]` / `[未在公开材料找到,需 PDF 核验]` / `[调研不足,需进一步实验]`
- 仓库 visibility:private;不写真名 / 个人邮箱 / token / 私人 key

## 调研过程管理

- **commit 节奏**:读完一篇论文 / 跑通一个实验 / 阶段性结论 → 立即 commit
- **push 节奏**:每完成一个主要章节节点 push 一次;调研结束前最后一次大整理 + push
- **每条结论必须可追溯**;数据不足处明说"调研不足",**不为了完整性瞎编数字**
- **不写**:真名 / 个人邮箱 / token / 私有 key / 临时日志 / 私有论文 PDF

## 后续触发条件

主对话 session 在收到 "GitHub auth 已就绪" 信号后,会执行:
```
gh repo create klkjjhjkhjhg/4dgs-mobile-rendering --private --source=. --push
```
然后派 D1 leaf subagent 调研,prompt = `/tmp/4dgs_goal_prompt.md`(外部文件 / 仓库内亦可备一份)。
