# 4dgs-mobile-rendering 调研项目升级 — 完整 Mission

> **本文件是"完整 goal 提示词"**。**简版 goal 见** `docs/mission/goal-brief.md`。
>
> 用途：4 件套 + 4 cron 的完整设计 + 操作细节，**子 agent / 未来自己 / 同事复用**都看这份。
>
> **纪律**：执行时**不要把用户引入工作回路**——歧义按合理默认走，**只有真正不可调和的决策才打断**。

---

## 0. 背景与现状

**项目**：`~/Codes/4dgs-mobile-rendering` — 3DGS / 4DGS / 移动端渲染技术调研。

**现状**（截至 2026-07-08）：
- 49 篇 paper notes in `docs/appendix/paper-notes/`
- 1 个 INDEX.md（按派系 A/B/C/D/E 分组）
- 1 个 venues.md（Tier 1/2/3 + Pre-print 栏 + 1-hop 引用规则）[本轮新建]
- 4 个 docs（00-goal / 01-precision / 02-accel / 03-roadmap / 04-trends）
- 1 个 README.md（§1 论据表 + §2 派系 SOTA 排名）
- 已验证：Lumina 30 references 中 7 条核心 3DGS/4DGS 引用 **100% 已收录**

**核心洞察**：49 篇质量密度高 = 调研不是关键词瞎扫 = 真覆盖了核心引用圈。

---

## 1. 总目标

完成 **4 件套 + 4 cron** 的"调研项目外循环 + 内循环"完整架构。

- **4 件套 = 内循环**（方法论 + 工具 + 模板）
- **4 cron = 外循环**（自动扫描 + 自动收录 + 自动升级 + 自动演进）

执行顺序：1 → 2 → 3 → 4，**每件套完成后 git commit**，**不强制 push**。

---

## 2. 第 1 件套：方法论 5 步法

### 2.1 目标
写 `docs/05-survey-methodology.md`，把当前散在多处的调研方法论整合成 1 个文件。

### 2.2 5 步法结构

**步骤 1：圈定白名单**
- 引用 `venues.md`（Tier 1/2/3 + Pre-print 栏 + Cross-disciplinary）
- 4 类来源：会议 / 期刊 / 预印本 / Cross-disciplinary

**步骤 2：周期扫描**
- 由 4 个 cron 自动跑（见 §5）
- 入口：arxiv listing + 会议接收名单 + S2 引用图

**步骤 3：1-hop 引用规则**
- 人工读 references 题目 → 判断相关（3DGS/4DGS/移动渲染/加速）
- 相关 → 走正常流程；不相关 → 跳过
- **一跳即停**（不向下追 references，防膨胀）
- **预期产能**：扫 1 篇高质量 → +3-8 篇 note（不是 +20）

**步骤 4：写 9 区块 paper note + INDEX 派系分类**
- 9 区块模板：基本信息 / 摘要 / 派系 / 方法 / 实验 / 数字 / 评估 / 引用 / Insight
- 派系 A/B/C/D/E（已在 INDEX.md 顶部定义）
- 49 篇 note 文件命名 `<year>-<author>-<keyword>.md`

**步骤 5：应用**
- 写进 README.md §1 论据表
- 写进 docs 正文
- 写进演进图（3D / 2D 视图）

### 2.3 必须包含的案例
**Lumina 30 references 验证**：
- 30 总 → 23 不相关 → 7 核心相关（3DGS / 4DGS / 移动渲染 / 加速）
- 7 核心相关全部已在 49 篇 INDEX
- **0 新增** = 调研齐全度验证

### 2.4 完成定义
- `docs/05-survey-methodology.md` 存在
- 5 步法完整，每步含工具 / 入口 / 模板 / 维护规则
- 含 Lumina 验证案例
- 末尾说明"4 cron 在外循环里如何嵌入 5 步法"
- 引用 `venues.md` / 模板 / `scripts_refs/` 各文件路径

---

## 3. 第 2 件套：3D 演进图前端

### 3.1 目标
建一个交互式 3D 演进图，GitHub Pages 可发布。**零 build 工具**，单 `index.html` + Three.js CDN 就能跑。

### 3.2 技术栈
- **Three.js r158+**（CDN 引入，不打包）
- **OrbitControls**（CDN）
- 零 build / 零 npm

### 3.3 文件结构（5 文件）

```
docs/evolution/
├── index.html              # Three.js 渲染主入口
├── data/evolution.json     # 49 节点 + 引用边
├── styles.css              # 节点 / 边 / UI 样式
├── README.md               # 部署说明（GitHub Pages + 本地预览）
└── (无 js 文件：Three.js 通过 CDN)

scripts_refs/evolution_gen.py  # 扫 49 篇 note 自动生成 evolution.json
```

### 3.4 演进图形式（排布 C）

- **X 轴 = 时间**（2023.7 → 2026.7 横向）
- **Y 轴 = 派系**（A 4DGS 表示 / B 4DGS 加速 / C 3DGS 加速 / D 移动端，4 层 Y 平面）
- **Z 轴 = 引用密度**（节点向外凸起高度 = 该 paper 在 49 篇 INDEX 中被多少 paper 引用）
- **节点**：球体
  - 大小 = 引用数
  - 颜色 = 派系（4 色：红 / 蓝 / 绿 / 黄）
  - 发光 = 高被引 paper（top 5）
- **边**：贝塞尔曲线
  - 实线 = 直接引用
  - 虚线 = 间接引用（一跳规则）
- **4 个转折点**（T1 3DGS / T2 4DGS / T3 4DGS-1K / T4 Lumina）= **半透明垂直面**

### 3.5 关键交互
- OrbitControls 旋转 / 缩放
- 鼠标 hover 节点 = tooltip（题目 / 时间 / 派系 / 引用数 / arxiv-id）
- 点击节点 = 弹窗 paper note 摘要 + 跳转链接
- 右上角 UI：
  - 派系筛选器（4 checkbox）
  - 时间段筛选器（slider 2023.7 → 2026.7）
  - 视图模式切换（3D / 2D fallback）

### 3.6 2D fallback
- 右下角按钮"切换 2D 视图"
- 2D = 时间 × 派系 双轴 DAG（纯 SVG / Canvas，**不用 ECharts**）
- 移动端默认 2D（性能考虑）
- CDN 失败自动 fallback 到 2D

### 3.7 节点数据 v1 来源
- 手写 49 节点（题目 / 时间 / 派系 / 引用数 / arxiv-id）
- 手写 ~30 条关键引用边
- `evolution_gen.py` v1 **只生成节点列表**（扫 49 篇 note 文件名 + 解析元数据），v2 补全边

### 3.8 完成定义
- `docs/evolution/index.html` 在浏览器能跑
- 显示 49 节点 + 引用边 + 4 转折点面
- 2D fallback 按钮可用
- 鼠标 hover / 点击交互完整
- `evolution.json` 含 49 节点
- `evolution_gen.py` v1 可跑通（生成节点列表）

---

## 4. 第 3 件套：9 区块 → 11 区块模板升级

### 4.1 目标
升级 9 区块模板，新增 2 个区块，**49 篇 note 批量升级**（机械化），**5 篇示范**做 §11 1-hop 关系图。

### 4.2 新增 §0.5 元数据块（基本信息后插入）

```markdown
## 0.5 元数据

- venue: <Tier 1/2/3 + 会议全名 或 "arxiv pre-print">
- arxiv-id: <xxxx.xxxxx>
- s2-id: <Semantic Scholar ID (如有)>
- homepage: <URL (如有)>
- status: <received | under-review | arxiv-only>
- 收录日期: <YYYY-MM-DD>
- 收录来源: <arxiv scan | 1-hop rule | 会议专扫>
- 1-hop 引用: <相关引用数 / 总引用数>
```

### 4.3 新增 §11 1-hop 关系图（文末）

```markdown
## 11. 1-hop 关系图

### 11.1 引用的相关工作 (downstream)
- 题目 / arxiv-id / 收录状态（在 INDEX / 未收录 / 跳过原因）

### 11.2 被引用的后续工作 (upstream) [v1 可选]
```

### 4.4 49 篇 note 升级范围

- **每篇**加 §0.5 元数据（机械化，扫 49 篇 note + 解析 + 写）
- **§11 1-hop 关系图**：v1 **5 篇示范**
  - 3DGS（2023-kerbl-blur-3dgs 或 4DGS 原论文）
  - 4DGS（2024-wu-4dgs）
  - Mobile-GS（2026-du-mobile-gs）
  - Lumina（2025-feng-lumina）
  - Flux-GS（2026-du-flux-gs）
- 5 篇示范用 Semantic Scholar 拉 references，标 1-hop 关系

### 4.5 完成定义
- 49 篇 paper notes 全部含 §0.5 元数据
- 5 篇示范含 §11 1-hop 关系图
- 不破坏 49 篇 note 已有正文

---

## 5. 第 4 件套：4 个 cron 论文扫描机制

### 5.1 目标
建 4 个 cron jobs（加进 `~/.hermes/profiles/main/cron/jobs.json`），**激进全自动 + 子 agent 复核**。

### 5.2 3 道保险（防幻觉）

1. **数字必标来源页码**——9 区块 note 的"性能数字"段，每条数字**必须附 PDF 页码**
2. **引用必查 S2**——1-hop references 段，**用 Semantic Scholar API 自动验证**
3. **子 agent 冲突即标"待人工"**——主 / 子 agent 任何 1 项不一致 → **自动标 🚩 待人工** + 不进 INDEX

### 5.3 Cron 1: cron-paper-arxiv

- **频率**：**每 3 天**（周一 / 周四 / 周日 9:00）
- **任务**：
  1. 拉 arxiv listing/cs.CV + listing/cs.GR
  2. 关键词过滤："3D Gaussian Splatting" / "4D Gaussian Splatting" / "Mobile Gaussian" / "Real-time Splatting" / "Differentiable Rendering"
  3. Tier 1/2 实验室作者白名单（VITA / Zhejiang U / NTU / PKU / HKUST / Snap Research / NVIDIA / Apple / Meta / Google 等）
  4. 跟 49 篇 INDEX 查重
  5. 命中 → **写 9 区块 paper note**（激进全自动）
  6. **delegate_task 子 agent 复核**（B 中复核：数字 / 引用 / 结论）
  7. 冲突项标 🚩 + 写入 `~/Codes/4dgs-mobile-rendering/cron/arxiv-YYYY-MM-DD-争议项.md`
  8. 无冲突 → 新 note 进 INDEX + 演进图 + venues.md
- **输出**：
  - `cron/arxiv-YYYY-MM-DD-candidates.md`（候选清单）
  - 新 note（无冲突）+ `cron/arxiv-YYYY-MM-DD-争议项.md`（冲突）
  - Telegram 通知

### 5.4 Cron 2: cron-paper-meeting

- **频率**：**每个会议前 1 月 + 后 1 月**（10 个会议/年 = 20 次触发）
- **会议清单**：
  - CVPR 5/7 月 / ICCV 9/11 月（奇数年）/ ECCV 9/11 月（偶数年）
  - NeurIPS 11/1 月 / ICLR 4/6 月 / SIGGRAPH 7/9 月 / SIGGRAPH Asia 11/1 月
  - ASPLOS 2/4 月 / ISCA 5/7 月 / MICRO 10/12 月 / HPCA 1/3 月
- **任务**：
  1. 扫 openaccess.thecvf.com / openreview.net / dl.acm.org 接收名单
  2. 关键词过滤（同 Cron 1）
  3. 跟 INDEX 查重
  4. 命中 → **写 9 区块 paper note**（激进全自动）
  5. **子 agent 复核**
  6. 冲突项标 🚩 + 无冲突进 INDEX
- **输出**：同 Cron 1（`cron/meeting-YYYY-{name}-candidates.md`）

### 5.5 Cron 3: cron-paper-upgrade

- **频率**：**每月 1 号 9:00**
- **任务**：
  1. 扫 `venues.md` Pre-print 栏所有 paper
  2. 检查是否上会议接收名单
  3. 命中 → **自动改 venue 字段**（pre-print → 接收会议）
  4. **子 agent 复核**（改前改后字段对比）
  5. 写 `cron/upgrade-YYYY-MM.md` 日志
  6. **发 Telegram 通知**到 Home channel
- **输出**：
  - `cron/upgrade-YYYY-MM.md`
  - 改后的 `venues.md` + 对应 note
  - Telegram 通知

### 5.6 Cron 4: cron-paper-evolve

- **频率**：**每周日 9:00**
- **任务**：
  1. 跑 `scripts_refs/evolution_gen.py` 重新生成 `evolution.json`
  2. 重新渲染 `evolution.html`（如有 build 步骤，v1 无）
  3. git commit
- **无子 agent 复核**（确定性脚本）
- **输出**：
  - `docs/evolution/data/evolution.json` 更新
  - git commit
  - Telegram 通知

### 5.7 子 agent 复核（B 中复核）

- **粒度**：B 中复核（**只复核数字 / 引用 / 结论**）
- **工具**：`delegate_task`（Hermes 内置）
- **prompt 模板**（在 cron prompt 中复用）：

```
你是论文 note 复核 agent。读主 agent 写的 9 区块 note + 原始 PDF。

重点复核 3 项：
1. **数字**：性能数字是否与 PDF 一致？是否标注页码？
2. **引用**：references 是否拼写正确？是否能在 S2 找到？
3. **结论**：核心结论是否过度推断？是否标 [abstract 直引] / [推测] / [基于 X 论文]？

输出：
- 通过：3 项全 OK
- 冲突：列出具体冲突项 + 你的修正版本
```

### 5.8 完成定义
- 4 个 cron jobs 全部建在 `~/.hermes/profiles/main/cron/jobs.json`
- 每个 cron **dry run 1 次**通过
- 输出格式正确
- Telegram 通知测试通过

---

## 6. 通用约束

- **不改 README.md 论据表 / 不改 4 个 docs 正文**——v3 调研结论，**不在本轮改**
- **不重写 49 篇 note 正文**——只加 §0.5 + §11
- **4 件套按 1 → 2 → 3 → 4 顺序做**，每件套完成后 git commit
- **歧义按合理默认走**，**不打断用户**——除非真正不可调和的决策
- **所有 cron 输出发 Telegram 通知**到 Home channel（不静默）

---

## 7. 完成定义（总）

- ✅ `docs/05-survey-methodology.md` 存在，5 步法完整，含 Lumina 验证案例
- ✅ `docs/evolution/index.html` 在浏览器能跑，显示 49 节点 + 引用边 + 2D fallback
- ✅ `docs/evolution/data/evolution.json` 存在
- ✅ `scripts_refs/evolution_gen.py` v1 可跑通
- ✅ 49 篇 paper notes 全部含 §0.5 元数据
- ✅ 5 篇示范（3DGS / 4DGS / Mobile-GS / Lumina / Flux-GS）含 §11 1-hop 关系图
- ✅ 4 个 cron jobs 全部建好 + dry run 1 次通过
- ✅ 所有改动 git commit

---

## 8. 不做

- ❌ 不做激进全自动的"全 9 区块 LLM 写"——4-9 区块仍人工（**本轮激进全自动 = 4 个 cron 触发时**）
- ❌ 不重写 49 篇 note 正文
- ❌ 不改 README.md / 4 个 docs
- ❌ 不做 GitHub Pages 实际发布（README 说明即可）
- ❌ 不做 mobile 端深度优化（移动端 2D fallback 即可）
- ❌ 不静默执行 cron——所有输出发 Telegram
- ❌ 不打断用户问琐碎决策——按合理默认走
