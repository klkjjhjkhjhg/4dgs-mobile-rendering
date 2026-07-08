# 05 — 调研方法论（5 步法）

> **目的**：把散在多处的调研方法（白名单 / 扫描 / 收录 / 1-hop / 应用）整合成 1 个文件，让任何新人都能照着做。
>
> **纪律**：本方法是"活的"，每完成一轮扫描都回头校准本文件。

---

## 0. 30 秒读懂

调研任何技术领域（**不限于 3DGS**）都走 **5 步法**：

1. **圈定白名单**（venues.md）—— 从哪儿找
2. **周期扫描**（4 个 cron）—— 怎么找
3. **1-hop 引用规则**—— 怎么扩散
4. **写 9 区块 paper note** + INDEX 分类—— 怎么存
5. **应用**（README 论据表 / docs 正文 / 演进图）—— 怎么用

**核心思路**：扫描是入口，**1-hop references 是杠杆**（一举三得：补全 / 画脉络 / 验证齐全），**9 区块 note 是基本单位**，**INDEX + 演进图是组织**。

---

## 1. 步骤 1：圈定白名单

### 1.1 目的
解决"扫什么会议 / 期刊 / 预印本"的问题。**不圈白名单 = 关键词瞎扫 = 漏论文 / 收垃圾**。

### 1.2 4 类来源

| 类别 | 例子 | 收录标准 |
|------|------|----------|
| **会议** | CVPR / ICCV / ECCV / SIGGRAPH / NeurIPS / ICLR / ICML / **ASPLOS / ISCA / MICRO / HPCA** | 见 `venues.md` Tier 1 |
| **期刊** | ACM TOG / IEEE TVCG / TPAMI / IJCV | Tier 2 期刊栏 |
| **预印本** | arxiv（cs.CV / cs.GR）| Pre-print 栏：**有主页即可**（代码 / demo / 视频 任一）|
| **Cross-disciplinary** | 跨算法 + 架构的工作（如 Lumina）| Cross-disciplinary 栏，**单篇必读** |

### 1.3 4 Tier 分级理由

- **Tier 1（必读）**= 3DGS 主流圈 + 体系结构顶会（**对移动端加速尤其重要**）
- **Tier 2（必读）**= 3D 视觉专项 + 期刊 + 跨方向高价值（设计自动化 / 移动系统）
- **Tier 3（选读）**= 编译器（3DGS kernel 优化场景才用）
- **Cross-disciplinary**= 跨方向单篇必读，**优先级最高**

### 1.4 操作
- 直接读 `venues.md`（本仓库根目录）
- 维护规则：见 `venues.md` 末尾"维护规则"节

### 1.5 验证

Lumina 30 references 验证（2026-07-08）：
- Lumina 是 Cross-disciplinary 工作（arxiv 2506.05682，体系结构跨方向）
- 30 references → 7 核心 3DGS/4DGS 相关 → 7 全部已在 49 篇 INDEX
- **0 新增** = 白名单收得齐

---

## 2. 步骤 2：周期扫描

### 2.1 目的
解决"什么时候扫"的问题。**手工扫 = 漏**——**用 cron 自动化**。

### 2.2 4 个 cron job（详见 `docs/mission/mission.md` §5）

| Cron | 频率 | 扫什么 | 落地动作 |
|------|------|--------|----------|
| `cron-paper-arxiv` | **每 3 天**（周一/四/日 9:00）| arxiv listing/cs.CV + cs.GR + 关键词 + Tier 1/2 实验室作者白名单 | 写 9 区块 paper note（激进全自动） + 子 agent 复核 |
| `cron-paper-meeting` | **会议前 1 月 + 后 1 月**（10 会议 × 2 = 20 次/年）| openaccess.thecvf / openreview / dl.acm 接收名单 + 关键词 | 同上 |
| `cron-paper-upgrade` | **每月 1 号 9:00** | venues.md Pre-print 栏所有 paper 是否上接收名单 | 自动改 `venue:` 字段 + Telegram 通知 |
| `cron-paper-evolve` | **每周日 9:00** | 跑 `evolution_gen.py` 重生成 `evolution.json` | git commit + Telegram 通知 |

### 2.3 关键词集合（命中任一即收录）

- "3D Gaussian Splatting" / "3DGS"
- "4D Gaussian Splatting" / "4DGS"
- "NeRF" / "Neural Radiance Field"（**限定**有性能优化相关 context）
- "Mobile Gaussian" / "Mobile Rendering" / "Mobile Splatting"
- "Real-time" + "Splatting"
- "Differentiable Rendering"（带性能优化）

### 2.4 排除（避免收垃圾）

- "Survey" / "Review" / "Tutorial"（综述类不直接追，**但用 1-hop 规则顺藤摸瓜**）
- 10 年以上的旧经典（除非该经典被多个 Tier 1 引用）
- 场景词："for autonomous driving" / "for medical" / "for SLAM" — 标 [domain-specific]，**除非**与移动端加速直接相关

### 2.5 Tier 1/2 实验室作者白名单

```
VITA Group (EPFL)
Zhejiang University 3DGS Group
NTU (3D Vision Lab)
PKU (3D Vision)
HKUST (Graphics / Vision)
Snap Research
NVIDIA Research
Apple (ML Research)
Meta Reality Labs
Google Research (3D Perception)
Apple, Microsoft, Adobe Research
```

**扩展规则**：发现新实验室在 Tier 1 顶会连续 3 篇 3DGS 工作 → 加进白名单。

### 2.6 输出位置

```
~/Codes/4dgs-mobile-rendering/cron/
├── arxiv-YYYY-MM-DD-candidates.md      # cron-paper-arxiv 输出
├── arxiv-YYYY-MM-DD-争议项.md            # 主/子 agent 冲突项
├── meeting-YYYY-{name}-candidates.md   # cron-paper-meeting 输出
├── meeting-YYYY-{name}-争议项.md         # 冲突项
└── upgrade-YYYY-MM.md                   # cron-paper-upgrade 日志
```

**所有 cron 输出发 Telegram 通知**到 Home channel（不静默）。

---

## 3. 步骤 3：1-hop 引用规则

### 3.1 目的
解决"扫到一篇高质量论文后，怎么防漏相关后续工作"的问题。**关键词扫只看标题，1-hop 跳进 references 圈层**。

### 3.2 触发条件

找到一篇高质量论文（满足任一）：
- Tier 1/2 接收（CVPR / SIGGRAPH / NeurIPS / ASPLOS 等）
- 已在 Pre-print 栏
- 已在 Cross-disciplinary 栏

### 3.3 操作流程

```
扫到高质量论文
   ↓
读 references（arxiv / OpenReview / DOI / Semantic Scholar API）
   ↓
逐条读 references 题目
   ↓
判断相关（4 类）：
   1. 3DGS / 4DGS 渲染加速
   2. 移动端 / 端侧推理
   3. 神经渲染 / 神经场压缩
   4. 渲染性能优化（kernel / 内存 / 带宽）
   ↓
相关 → 走"正常收录流程"（跟会议扫到完全同等对待）
   ↓
写 9 区块 paper note + INDEX 派系分类
   ↓
一跳即停（不向下追 references）
```

### 3.4 关键设计

- **不关键词匹配**：人工读题目判断（关键词误伤率高，如 "Splatting" 可能是数据可视化）
- **一跳即停**：防止膨胀（**扫 1 篇高质量预期 +3-8 篇，不是 +20**）
- **同等对待**：1-hop 收录的 note 跟会议扫到的 note **完全同等**（不进 9 区块差异，进 INDEX 同样位置）

### 3.5 验证案例：Lumina 30 references

| 阶段 | 数字 |
|------|------|
| Lumina 总 references | 30 |
| 不相关（医学 / 自动驾驶 / SLAM / 任务规划 / 行人预测 等）| 23 |
| 核心相关（3DGS / 4DGS / 移动渲染 / 加速） | **7** |
| 已在 49 篇 INDEX | **7**（100% 命中）|
| 新增 | **0** |

**结论**：49 篇 INDEX 调研密度被验证 = **真覆盖核心引用圈，不是关键词瞎扫**。

### 3.6 与 4 cron 的衔接

1-hop 规则由 **`cron-paper-arxiv` + `cron-paper-meeting` 自动执行**——cron 扫到高质量论文后，**自动跑 1-hop**（用 S2 API 拉 references + 人工 + 子 agent 复核）。

---

## 4. 步骤 4：写 9 区块 paper note + INDEX 分类

### 4.1 目的
解决"扫到了怎么存"的问题。**9 区块 = 标准化模板，INDEX = 标准化组织**。

### 4.2 9 区块模板（每篇 note 必填）

```markdown
# <paper title>

## 0. 基本信息
- 作者 / 年份 / 会议 / arxiv-id / GitHub / 主页

## 0.5 元数据        ← 件套 3 新增
- venue / arxiv-id / s2-id / homepage / status / 收录日期 / 收录来源 / 1-hop 引用

## 1. 一句话总结
- 用 1 句话说清这篇 paper 做了什么

## 2. 摘要（核心 3 段）
- 段 1：问题
- 段 2：方法
- 段 3：结果

## 3. 派系分类（INDEX 同步）
- 派系 A / B / C / D / E 选 1 个

## 4. 方法
- 关键技术 / 网络结构 / 公式（不照搬 paper，**精炼到能复述**）

## 5. 实验
- 数据集 / 训练设置 / baseline

## 6. 性能数字（**必标 PDF 页码**）
- 数字 + 表格 / 图号 / PDF 页码

## 7. 评估
- 跟本项目相关性的具体评估

## 8. 引用
- paper 自己引了什么

## 9. Insight（**必填**）
- 这篇 paper 对本项目有什么用 / 启发

## 11. 1-hop 关系图    ← 件套 3 新增（5 篇示范用）
- 引用的相关工作 + 被引用的后续工作
```

### 4.3 派系 A/B/C/D/E（来自 INDEX.md）

| 派系 | 含义 | 派系 SOTA #1（2026-07-08）|
|------|------|---------------------------|
| **A** | 4DGS 表示（高精度表示主线）| 4DGS-1K (VITA Group) |
| **B** | 4DGS 加速 / 动静态分离 | 4DGS-CC (Zhejiang U) |
| **C** | 3DGS 加速 | Flux-GS (ECCV 2026) |
| **D** | 移动端 / 流式落地 | GS-NFS (NVIDIA) |
| **E** | Cross-disciplinary | Lumina (体系结构跨方向) |

### 4.4 命名约定

- 格式：`<year>-<author>-<keyword>.md`
- 例子：`2024-wu-4dgs.md` / `2026-du-flux-gs.md` / `2025-feng-lumina.md`
- 例外：4 篇"早期下"用易读命名（`4DGS-1K.pdf` / `wu-4dgs.pdf` 等）—— **保持向后兼容**

### 4.5 写 note 的纪律

- **不照搬 paper 全文**——精炼到能复述
- **数字必标 PDF 页码**（3 道保险 #1）
- **每段引文标来源**：`[abstract 直引]` / `[基于 X 论文]` / `[推测]` / `[未在公开材料找到,需 PDF 核验]` / `[调研不足,需进一步实验]`
- **不重写 49 篇 note 正文**——只加 §0.5 + §11（件套 3 范围）

### 4.6 INDEX.md 同步

每写 1 篇新 note → INDEX.md 同步加 1 行（派系 + 一句话 + ⭐ 评级）。

---

## 5. 步骤 5：应用

### 5.1 目的
解决"调研了怎么用"的问题。**3 类应用场景**：

### 5.2 应用 1：README.md §1 论据表

- README.md §1 = "30 秒看懂"——有 7 条核心论据
- 每条论据**必须有 paper 来源**（实测 / 推测 标清楚）
- **新增 paper → 论据表同步加 1 行**（**不删旧论据**）

### 5.2.1 论据表 7 条（2026-07-08 状态）

| # | 论据 | 来源 | 类型 |
|---|------|------|------|
| 1 | 3DGS 在 Snap 8 Gen 3 已 127 FPS @ 4.6 MB | Mobile-GS (ICLR 2026) | 实测 |
| 2 | 4DGS-1K 在 TITAN X 上 200+ FPS | 4DGS-1K | 实测 |
| 3 | 4DGS-1K 在 RTX 3090 上 8.94× 加速 | 4DGS-1K | 实测 |
| 4 | Lumina 在 mobile Volta 上 4.5× speedup + 5.3× energy | Lumina | 实测 |
| 5 | Snap 8 Gen 4 算力 ≈ Gen 3 × 1.3 | 高通官方 | 推测 |
| 6 | Flux-GS Snap 8 Gen 3 147 FPS @ 2.1 MB | Flux-GS (ECCV 2026) | 实测 |
| 7 | GS-NFS Jetson Orin 4DGS 25 FPS decode | GS-NFS (NVIDIA) | 实测 |

### 5.3 应用 2：docs 正文

4 个 docs（00-goal / 01-precision / 02-accel / 03-roadmap / 04-trends）= 调研正文
- 新 paper **如果跟某 doc 章节相关** → 加引用
- **不重写 doc 正文**——只加引用
- 4 docs 是 v3 调研结论，**本轮不改**

### 5.4 应用 3：演进图（件套 2）

- 49 篇 → 演进图（3D + 2D fallback）
- X = 时间 / Y = 派系 / Z = 引用密度
- 4 转折点 = T1 3DGS / T2 4DGS / T3 4DGS-1K / T4 Lumina
- 详见 `docs/evolution/README.md`（件套 2 完成时建）

### 5.5 与 4 cron 的衔接

`cron-paper-evolve`（每周日）→ 跑 `evolution_gen.py` 重生成 `evolution.json` → 演进图自动更新。

---

## 6. 5 步法 + 4 cron 的衔接总图

```
[白名单 venues.md]
       ↓
[4 cron 周期扫描]
       ↓
  ├─ cron-paper-arxiv (每 3 天)
  ├─ cron-paper-meeting (会议前/后 1 月)
  ├─ cron-paper-upgrade (每月 1 号)
  └─ cron-paper-evolve (每周日)
       ↓
[1-hop 引用规则] ← 自动 + 人工双复核
       ↓
[9 区块 paper note + INDEX 分类]
       ↓
[3 类应用]
  ├─ README.md §1 论据表
  ├─ 4 docs 正文引用
  └─ 演进图（3D + 2D fallback）
       ↓
[无止境 ↻]
```

---

## 7. 维护纪律

1. **每写 1 篇 paper note → 同步 INDEX.md 1 行 + 同步 venues.md（如适用）+ 同步 README.md §1 论据表（如适用）**
2. **每接收 1 篇 paper → 立刻改 `venue:` 字段 + 移出 Pre-print 栏**
3. **每跑 1 次 cron → Telegram 通知 + 写日志到 `cron/`**
4. **每扩 1 批 paper（≥ 5 篇）→ 回头校准本方法论文件**

---

## 8. 验证：Lumina 30 references 案例

> 完整案例见 `venues.md` §1-hop 引用规则节末尾。

**核心数据**：
- 30 总 → 23 不相关 → **7 核心相关** → **7 100% 已在 INDEX** → **0 新增**

**3 个启示**：
1. **白名单收得齐**——49 篇覆盖了高质量工作的核心引用圈
2. **1-hop 规则有效**——Lumina 是 Cross-disciplinary 标杆，它的 references 圈层被 100% 覆盖 = 其他工作大概率也覆盖
3. **调研不是关键词瞎扫**——质量密度验证通过

---

## 9. 不在本方法论范围

- **实验**（`experiments/`）—— 调研 ≠ 实验，实验由 `docs/03-end-to-end-roadmap.md` M0-M2 定义
- **采集 SOP**（`docs/appendix/collection-sop.md`）—— 数据采集方法论，与本文件正交
- **Vulkan 1.3 实现细节**（`docs/appendix/vulkan-impl-notes.md`）—— 落地实现，与本文件正交

---

## 10. 引用一览

- **`venues.md`**（仓库根目录）—— 白名单主文件
- **`docs/appendix/paper-notes/INDEX.md`** —— 49 篇 paper note 索引
- **`README.md`** —— §1 论据表 + §2 派系 SOTA 排名
- **`docs/00-goal.md` ~ `docs/04-trends-2026H1.md`** —— 调研正文 4 docs
- **`docs/mission/mission.md`** —— 4 件套 + 4 cron 完整 mission
- **`scripts_refs/`** —— 扫描 / 过滤 / S2 引用图脚本
