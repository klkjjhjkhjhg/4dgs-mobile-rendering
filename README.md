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
| 本地仓初始化 | ✅ `~/Codes/4dgs-mobile-rendering/`,主分支 `main` |
| 占位 README + `.gitignore` + docs 骨架 | ✅ |
| 远端 GitHub 仓库 | ❌ 待 GitHub auth 完成后创建 |
| 调研执行 | ❌ 待派 subagent |
| 首个 commit `9a05308` | ✅(仅本地) |

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
