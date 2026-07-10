# Paper Notes 更新指南

> 适用范围：项目 `~/Codes/4dgs-mobile-rendering`
> 触发时机：每收一篇新 paper note（无论是 cron 扫的还是人工加的）
> 必读：[UPDATE_EVOLUTION.md](./UPDATE_EVOLUTION.md)（演进图是受 note 影响最严重的一处，独立专项）

## TL;DR — 5 件事，按顺序

```
1. 写 paper note        →  docs/appendix/paper-notes/<id>.md
2. 更新 INDEX.md         →  派系归属行 + 总数刷新
3. 升级 venues.md        →  如果有 pre-print 升级（venue_upgrade cron 自动做）
4. 同步演进图数据        →  详见 UPDATE_EVOLUTION.md（独立专项）
5. 刷新汇总文档          →  00-goal / 04-trends / 01-03 主线 / README
```

⚠ **绝对不要只做第 1 步**。只写 note 不更新下游 = 5 处文档静默 drift（这是本项目 2026-07-09 的实际事故）。

---

## 步骤 1：写 paper note（cron 自动 / 9 区块模板）

**触发方式**：
- cron `arxiv_4dgs_scan`（周一/四/日 9:00）
- cron `meeting_scan`（会议前后 1 月）
- 人工加论文（用 `discovery.md` 方法论）

**格式**：9 区块 + §0.5 元数据。模板见 `cron_scripts/add_metadata.py` + 任意现有 paper note。

**关键字段**（用于下游联动）：
- `## 0.5 元数据` 段里的 `arxiv-id`（去重 + INDEX 链接）
- `**相关性**` 顶引里的 **派系名**（派系归属 + INDEX 分组依据）
- `## 2. 链接` 里的 arxiv URL + 本地 PDF 路径（INDEX 引用）

**完成后**：
- cron 会自动写 `cron/arxiv-YYYY-MM-DD-candidates.md`（已收录 + 争议项）
- 人工 case：手动建一行 `docs/appendix/paper-notes/<id>.md` 然后跑步骤 2

---

## 步骤 2：更新 INDEX.md（必做，**派系归属就在这里定**）

**文件**：`docs/appendix/paper-notes/INDEX.md`

**改 4 处**：

### 2.1 总数 + 收录日期
```markdown
> **总计**: **50 篇 paper notes ↔ 50 个本地 PDF**（截至 2026-07-09）  ← 改这里
```

### 2.2 派系分组标题下的子标题
派系 A/B/C/D/E 的标题计数要和实际节点数一致：
```markdown
## A. 4DGS 表示（高精度表示主线，9 篇）  ← 改 (9 篇)
```
但更精确的方式是 **派系计数 = 演进图节点数**（取下游真实值，反向校对这里）。

### 2.3 新增 1 行 note 引用
按派系分组插到对应表里：
```markdown
| [2026-mousa-provablepruning.md](paper-notes/2026-mousa-provablepruning.md) | 2607.02721 | 2026-07 | 首个可证明 3DGS coreset theory（派系 C 理论补强 + D 部署） | ⭐⭐ |
```

### 2.4 新批扩展 marker（如果是新批次）
如：本批 3 (2026-07-09 arxiv 扫描): 4 篇 — Provable Pruning / GRay / TemporalGS / L2D2-GS

---

## 步骤 3：升级 venues.md（**只 pre-print 升级时做**）

**触发**：
- cron `venue_upgrade`（每月 1 号 9:00）— **自动**
- 人工在 Semantic Scholar 看到 paper 上会议 — 手动

**改**：`venues.md` 的 `Pre-print` 段对应行（从 `Unknown / arxiv pre-print` 改成 `会议名 年份`），同时改 paper note §0.5 的 venue 字段。

**不做**：cron 已经自动处理了 — **不要人工重复改**。

---

## 步骤 4：同步演进图数据（**独立专项，必读 UPDATE_EVOLUTION.md**）

**简版**：
```bash
cd ~/Codes/4dgs-mobile-rendering
python3 cron_scripts/evolution_gen.py
# 验收流程见 UPDATE_EVOLUTION.md 第 5 节
```

**完整流程**：见 [UPDATE_EVOLUTION.md](./UPDATE_EVOLUTION.md)

---

## 步骤 5：刷新汇总文档（按相关性选择性更新）

不是每篇 note 都要动所有文档，按相关性选择：

### 5.1 `docs/00-goal.md`
**触发条件**：新论文影响"对标主线"或"SOTA 数字"
**改**：
- 派系计数（如 A 14 → 15）
- 对标主线段（如新增了 L2D2-GS 是小米合作，可能影响主线选择）
- SOTA 数字对比表

### 5.2 `docs/04-trends-2026H1.md`
**触发条件**：新论文是派系 #1/#2 候选，或代表新趋势
**改**：
- §3 派系排名表（"派系 3 (mobile 渲染)" / "派系 4 (mobile streaming)" 等等）
- §2 路径 A/B/C/D 的代表论文列表
- §3 SOTA TOP2 数字

### 5.3 `docs/01-03 主线文档`
**触发条件**：新论文核心方法落在某个主线段
**改**：对应 §X.X 段加 1 条引用 + 简短评价

### 5.4 `docs/README.md`
**触发条件**：总数 / 派系分布 / TOP2 SOTA 变化
**改**：
- 顶部"30 秒看懂"统计
- §2 派系 SOTA 排名
- §1 "为什么可达" 论据表（如理论补强 mousa-provablepruning）

### 5.5 不需要改的文档
- `docs/05-survey-methodology.md`（方法论，跟具体 paper 数无关）
- `cron/`（cron 自己的运行日志，独立维护）
- `docs/appendix/paper-notes/` 其他 note（除非被引）

---

## 验收清单（必跑）

每次更新后人工 review 5 项：

```
□ INDEX.md 总数 = 实际 note 文件数 (ls *.md | wc -l)
□ INDEX.md 派系分组计数 = 演进图节点数 (jq '.nodes | group_by(.faction) | map({(.[0].faction): length})' docs/evolution/data/evolution.json)
□ evolution.json 节点数 = INDEX 总数（差 ±2 以内合理，因为可能有"未收录但 JSON 有的"边缘 case）
□ 无 lint error（HTML/CSS/JS 无 syntax error）
□ 主页 https://klkjjhjkhjhg.github.io/4dgs-mobile-rendering/evolution/ 实际渲染无 console error
```

---

## 反模式（不要做）

❌ **只写 note 不更新下游**（最常见 drift 原因，本项目 2026-07-09 真实事故）

❌ **直接改 evolution.json 手写**（绕过 evolution_gen.py，破坏后续 cron 同步）

❌ **派系名写模糊**（如"派系 C/D" → 必须选一个主派系，注里可写次要派系）

❌ **跳过验收**（光改完代码不浏览器实测，2026-07-10 演进图打磨就是这个坑）

❌ **commit message 用 emoji 但缺上下文**（如 `📝 update` → 应该是 `[paper 2607.02721] Provable Pruning 收录：派系 C`）

---

## 实际事故案例（写在最前面吸取教训）

**2026-07-09**：`arxiv_4dgs_scan` 写了 4 篇 note（mousa / poirier / song / zhou），但下游 INDEX / 04-trends / evolution.json 全没同步。**直至 7/10 用户手动对比才发现**，已 drift 5+ 处。

**根因**：
1. cron `arxiv_4dgs_scan` prompt 步骤 4 说"无冲突: 写新 note 进 INDEX + 更新演进图" — 但**没指定怎么做**（哪个字段 / 哪几行）
2. cron `evolution_update` 是**每周日**才跑，中间 3 天窗口 drift 累积
3. 没有"note 数量 vs JSON 数量"一致性检查

**修复**：
- 写本指南（指定每步具体改什么）
- 演进图专项文档（[UPDATE_EVOLUTION.md](./UPDATE_EVOLUTION.md)）独立验收流程
- cron 加 hook：note 写完后立即跑 `evolution_gen.py` + diff 警告

---

## 相关文件

- **方法论文档**：`docs/05-survey-methodology.md`
- **发现日志**：`docs/appendix/discovery.md`（项目内沉淀 vs 读论文）
- **Skill**：`research-survey-3dgs`（Hermes skill，含白名单 / 一跳引用规则）
- **Cron 配置**：`~/.hermes/profiles/main/cron/jobs.json`（id: arxiv_4dgs_scan / meeting_scan / venue_upgrade / evolution_update）