# 调研文档总览

> **本目录是整个调研的"成品区"**,每个模块由 subagent 在调研过程中分阶段写入。
> 文件命名严格按 `00-` / `01-` / `02-` / `03-` 顺序,避免阅读时跳页。

## 文件清单与状态

| 文件 | 主题 | 状态 |
|---|---|---|
| [00-goal.md](./00-goal.md) | 调研目标 spec(约束 / 必须覆盖 / 产出要求) | ✅ 已写(由主对话 session) |
| [01-high-precision-representation.md](./01-high-precision-representation.md) | 第一块调研:离线端高精度 4DGS 表示 | ✅ 已写 (48KB, 2026-07-08) |
| [02-rendering-acceleration.md](./02-rendering-acceleration.md) | 第二块调研:Vulkan 1.3 渲染加速 | ✅ 已写 (25KB, 2026-07-08) |
| [03-end-to-end-roadmap.md](./03-end-to-end-roadmap.md) | 整合路线图:采集 → 训练 → 实机 demo | ✅ 已写 (40KB, 2026-07-08) |

## 横向切片 (`docs/china-landscape/`)

> 与 `00-03` 正交 —— 不替代时间线，**按地域（国内）切片**。产物可反哺主时间线。

| 文件 | 主题 | 状态 |
|---|---|---|
| [china-landscape/landscape-summary.md](./china-landscape/landscape-summary.md) | 国内调研速览（按 paper 数排序 top-15 + B 派系论文池） | ✅ 已写 (2026-07-17) |
| [china-landscape/READING-GUIDE.md](./china-landscape/READING-GUIDE.md) | 28 个单位按地区分类 + 深度说明 | ✅ 已写 (2026-07-17) |
| [china-landscape/trends.md](./china-landscape/trends.md) | 5 派系 × 28 单位矩阵 + 趋势观察 | ✅ 已写 (2026-07-17) |
| [china-landscape/timeline.md](./china-landscape/timeline.md) | 63 papers 按季度排序 | ✅ 已写 (2026-07-17) |
| [china-landscape/institutions/](./china-landscape/institutions/) | 28 个 per-unit 深度档 | ✅ 已写 (2026-07-17) |
| [china-landscape/sources.md](./china-landscape/sources.md) | 63 个 arxiv URL + 引用规范 | ✅ 已写 (2026-07-17) |
| [china-landscape/00-goal.md](./china-landscape/00-goal.md) | 本切片调研目标 spec | ✅ 已写 (2026-07-17) |

**入口建议**：先读 [landscape-summary.md](./china-landscape/landscape-summary.md)（2 分钟速览），再按需展开 [READING-GUIDE.md](./china-landscape/READING-GUIDE.md)。

## 附录 (`docs/appendix/`)

| 子模块 | 内容 |
|---|---|
| `paper-notes/` | 每篇关键论文的精读笔记 |
| `collection-sop.md` | 采集 SOP 草案(设备清单 / 同步方案) |
| `vulkan-impl-notes.md` | Vulkan 1.3 实现细节笔记 |

## 阅读顺序建议

1. 先读 `00-goal.md` 明确任务边界
2. 然后 `01-` 高精度表示 → `02-` 渲染加速
3. 最后 `03-` 整合路线图
4. 附录按需补充深读材料
5. **横向补充**: `china-landscape/landscape-summary.md` + `READING-GUIDE.md`（按地域切片的国内单位 landscape，与主时间线正交）
