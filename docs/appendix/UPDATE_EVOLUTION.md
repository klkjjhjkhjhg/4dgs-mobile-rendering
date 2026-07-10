# 演进图更新指南（专项）

> 范围：`docs/evolution/`（主页 + 演进图 + JSON 数据）
> 适用场景：每收一篇新 paper 都要走一遍；演进图升级大改时也要走

## TL;DR

```bash
cd ~/Codes/4dgs-mobile-rendering

# 1. 跑脚本重生成 JSON（自动从 INDEX.md 拉派系归属）
python3 cron_scripts/evolution_gen.py

# 2. 检查 JSON vs INDEX 一致性
python3 cron_scripts/check_drift.py  # 见 §5.3 自建

# 3. 启 server，浏览器实跑验收
cd docs && python3 -m http.server 8123 &

# 4. 验收必须 PASS（见 §5 完整流程）
# - V1: 节点数 = INDEX 总数
# - V2: 派系分组计数与右侧面板一致
# - V3: 5 个 cluster hull 渲染正常无重叠
# - V4: 拖时间轴 → 节点数动态变化
# - V5: 搜索"4DGS" → 7+ 匹配
# - V6: 派系开关 → 节点数减少
# - V7: 无 JS error

# 5. commit + push
git add docs/evolution/ docs/appendix/paper-notes/INDEX.md
git commit -m "[paper <id>] <title> 收录：派系 X"
git push origin main
```

⚠ **绝不 commit 没通过 §5 验收的代码**。验收失败 = 回炉修，不是妥协 commit。

---

## §1 演进图架构速览

```
docs/evolution/
├── index.html              # 演进图主页面 (vanilla JS + d3 force-directed)
├── styles.css              # Mocha 主题样式
├── data/
│   └── evolution.json      # 50 节点 / 5 派系 / 4 转折点 / 48 边
├── README.md               # 演进图使用说明
└── (no /index.html sub-folder)
```

**数据流**：`INDEX.md` → `evolution_gen.py` → `evolution.json` → `index.html`（前端 fetch 解析）

**前端架构**：
- d3 force-directed 派系聚类（不是 Three.js 3D，commit `12966ff` 改的）
- 5 个派系的不规则闭合曲线（polygonHull + Cardinal 贝塞尔，commit `c6ee8fd`）
- 4 大功能：A1 时间轴播放 / B1 Trending Now / B5 Dead End Watch / C3 议题搜索

---

## §2 必须更新的 3 类数据

### 2.1 节点（nodes）
**位置**：`docs/evolution/data/evolution.json` → `nodes` 数组

**每节点字段**：
```json
{
  "id": "2026-mousa-provablepruning",     // 必须 = paper note 文件名 (去掉 .md)
  "label": "ProvablePruning",             // 显示名（短）
  "year": 2026.5,                          // 时间轴位置（精确到月）
  "faction": "C",                          // A / B / C / D / E
  "arxiv": "2607.02721",                   // arxiv-id（INDEX 链接）
  "rating": "⭐⭐"                          // ⭐ / ⭐⭐ / ⭐⭐⭐
}
```

**id 命名约定**：
- 主姓在前：`2024-wu-4dgs`（Wu 是 4DGS 第一作者）
- 多作者取第一：`2026-poiri...` 取 `poiri` 截断
- 不带大写：全小写 + 连字符
- 必须与 INDEX.md 表格里的 paper note 文件名（例如 `2026-zhou-temporalgs.md`）完全一致

**label 命名**：
- 短（≤14 字符，节点圆圈宽度限制）
- 学术圈惯用名（如 3DGS / 4DGS / SpeedSplat）
- 移除冗余前缀（如 "Efficient" / "Real-Time"）

### 2.2 边（edges）
**位置**：`evolution.json` → `edges` 数组

**每边字段**：
```json
{
  "from": "2024-wu-4dgs",         // source 论文 id
  "to": "2026-mousa-provablepruning",  // target 论文 id
  "type": "indirect"              // "direct"（直接引用） / "indirect"（一跳间接）
}
```

**判定依据**：
- `direct`：新 paper references 里明确列出某已有论文（PDF § References 段）
- `indirect`：新 paper 没直接引，但某已有论文 references 引用了它（**反向引用关系**）
- **不要**做"二跳"以上（颗粒度爆炸）

**来源**：paper note §11 "1-hop 引用关系图"（write_paper_note 时已生成）

### 2.3 派系（factions）
**位置**：`evolution.json` → `meta.factions`

```json
"factions": {
  "A": {"name": "4DGS 表示", "color": "#e74c3c", "y": 0},
  "B": {"name": "4DGS 加速 / 动静态分离", "color": "#3498db", "y": 1},
  "C": {"name": "3DGS 加速", "color": "#2ecc71", "y": 2},
  "D": {"name": "移动端 / 流式落地", "color": "#f1c40f", "y": 3},
  "E": {"name": "Cross-disciplinary", "color": "#9b59b6", "y": 4}
}
```

**硬规矩**：
- 5 派系名 + 颜色 + y 坐标 **锁死**（用户偏好）
- 修改需用户拍板（不要自动改）

---

## §3 evolution_gen.py 行为详解

### 3.1 派系自动判定逻辑（看代码行）
```python
FACTION_KEYWORDS = {
    "A": ["4dgs", "4d gaussian", "4dgs-1k", "spacetime", ...],
    "B": ["4dgscc", "4dgcpro", "mega", "flashgs", ...],
    ...
}
```

**坑 1**：关键字匹配的是 **id 字符串**，不是 paper note §0.5 里的派系标注
**坑 2**：新论文 id 不在关键词里 → **派系归 None** → 节点不出现在图上

**修复**：在 `cron_scripts/evolution_gen.py` 的 `FACTION_KEYWORDS` 加新 id 关键字。

### 3.2 边自动判定
**当前实现**：v2 加了 S2 API 拉 references（看 evolution_gen.py 头部注释）
**风险**：S2 API rate limit / 离线情况 → 部分新论文没边

**回退**：手动编辑 `evolution.json` 的 `edges` 数组，按 §2.2 字段填。

### 3.3 时间轴 year 字段
**格式**：`YYYY.M`（如 `2026.07`）
**取值**：从 paper note §0.5 的 arxiv-id v1 提交日期（如 2607.02721 → 2026.07）

**坑**：v2 / v3 重提交不改 year，只更新版本号。**取 v1 提交日**才是首次出现时间。

---

## §4 更新流程（人工 + cron 双路径）

### 4.1 cron 自动路径（arxiv_4dgs_scan）

**当前 cron prompt**（在 `jobs.json` `arxiv_4dgs_scan`）：
```
步骤 4: 无冲突: 写新 note 进 INDEX + 更新演进图 + 写 cron/arxiv-...-candidates.md
```

**问题**：
1. "更新演进图" 没指定怎么做
2. "写新 note 进 INDEX" 没指定哪个字段
3. 没有"完成度自检"

**改进 prompt**（见 §7 cron patch 段）。

### 4.2 人工路径（推荐用于 ≥3 篇新 paper）

```bash
# 1. 写完 note（已自动）
# 2. 更新 INDEX.md（见 UPDATE_GUIDE.md §2）
# 3. 跑 evolution_gen.py
cd ~/Codes/4dgs-mobile-rendering
python3 cron_scripts/evolution_gen.py

# 4. 自建 check_drift.py（见 §5.3）或手动对比
diff <(jq -r '.nodes[].id' docs/evolution/data/evolution.json | sort) \
     <(ls docs/appendix/paper-notes/ | grep -v INDEX | sed 's/\.md$//' | sort)
# 差集 = 漂移的 note

# 5. 浏览器验收（见 §5）
# 6. commit + push
```

---

## §5 验收流程（**硬门槛，不通过不 commit**）

### 5.1 启 server

```bash
cd ~/Codes/4dgs-mobile-rendering/docs
python3 -m http.server 8123 &
sleep 2
curl -s -o /dev/null -w "%{http_code}\n" http://localhost:8123/evolution/
# 期望: 200
```

### 5.2 浏览器自动化验收（用 Hermes `browser_*` 工具）

```python
# Step 1: navigate
browser_navigate("http://localhost:8123/evolution/")

# Step 2: 等 force simulation 稳定（5-8 秒）
sleep(8)

# Step 3: 视觉验证（必跑）
browser_vision("""
5 个派系 hull 是不是不规则平滑闭合曲线（不是规整圆）？
5 个派系是否清楚分开？
5 个派系标签 A/B/C/D/E 是否都能完整看到？
节点是否基本都在所属派系 hull 内？
""")

# Step 4: 控制台验证（必跑）
browser_console("""
JSON.stringify({
  nodes: document.querySelectorAll('.node').length,
  visibleNodes: Array.from(document.querySelectorAll('.node')).filter(n => n.style.display !== 'none').length,
  factions: Array.from(document.querySelectorAll('.cluster-bg')).map(c => c.getAttribute('class')),
  dLenSum: Array.from(document.querySelectorAll('.cluster-bg')).reduce((s,c) => s + (c.getAttribute('d')||'').length, 0),
  errs: window.__jsErrs || []
})
""")
# 期望: nodes = INDEX 总数, factions 5 个 .cluster-bg.cluster-X, dLenSum > 15000, errs = []

# Step 5: 时间轴交互
browser_console("""
document.getElementById('timeline-slider').value = '2024.3';
document.getElementById('timeline-slider').dispatchEvent(new Event('input', { bubbles: true }));
'ok'
""")
sleep(2)
browser_console("JSON.stringify(document.getElementById('time-display')?.textContent)")
# 期望: 包含 "2024.04" 或 "2024.3"

# Step 6: 搜索交互
browser_console("""
const i = document.getElementById('topic-search');
i.value = '4DGS';
i.dispatchEvent(new Event('input', { bubbles: true }));
'ok'
""")
sleep(1)
browser_console("""
JSON.stringify({
  match: document.querySelectorAll('.search-match').length,
  dim: document.querySelectorAll('.search-dim').length
})
""")
# 期望: match ≥ 5, dim = total - match

# Step 7: 派系开关
browser_click("@e71")  # E 派系 checkbox（ref 视情况而定）
sleep(2)
browser_console("""
JSON.stringify(Array.from(document.querySelectorAll('.node')).filter(n => n.style.display !== 'none').length)
""")
# 期望: 可见节点数 = 总数 - 7
```

### 5.3 check_drift.py（自建，建议提交）

```python
#!/usr/bin/env python3
"""
check_drift.py — 一致性检查脚本

跑在 evolution_gen.py 之后。fail = 必须修。

Usage:
  python3 cron_scripts/check_drift.py
"""
import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
NOTES_DIR = REPO_ROOT / "docs" / "appendix" / "paper-notes"
INDEX_FILE = NOTES_DIR / "INDEX.md"
JSON_FILE = REPO_ROOT / "docs" / "evolution" / "data" / "evolution.json"


def main():
    # 1. INDEX 总数
    notes_on_disk = sorted([p.stem for p in NOTES_DIR.glob("*.md") if p.stem != "INDEX"])
    # 2. INDEX.md 引用数
    index_ids = set(re.findall(r"\((\d{4}-[a-z\-]+)\.md\)", INDEX_FILE.read_text()))
    # 3. JSON 节点数
    data = json.loads(JSON_FILE.read_text())
    json_ids = set(n["id"] for n in data["nodes"])

    errs = []
    # 磁盘 vs INDEX
    disk_only = set(notes_on_disk) - index_ids
    if disk_only:
        errs.append(f"⚠ 磁盘有但 INDEX 没引用 ({len(disk_only)}): {sorted(disk_only)[:5]}")
    # INDEX vs JSON
    index_only = index_ids - json_ids
    if index_only:
        errs.append(f"⚠ INDEX 有但 JSON 没节点 ({len(index_only)}): {sorted(index_only)[:5]}")
    # JSON vs INDEX
    json_only = json_ids - index_ids
    if json_only:
        errs.append(f"⚠ JSON 有但 INDEX 没引用 ({len(json_only)}): {sorted(json_only)[:5]}")

    # 派系计数
    factions = {}
    for n in data["nodes"]:
        factions[n["faction"]] = factions.get(n["faction"], 0) + 1

    # 报告
    print(f"📊 演进图一致性检查")
    print(f"  磁盘 note 数: {len(notes_on_disk)}")
    print(f"  INDEX 引用数: {len(index_ids)}")
    print(f"  JSON 节点数: {len(json_ids)}")
    print(f"  派系分布: {factions}")
    if errs:
        print("\n❌ 不一致项:")
        for e in errs:
            print(f"  {e}")
        return 1
    print("\n✅ 全一致")
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
```

---

## §6 已知坑 & 修法

### 6.1 演进图节点数 vs INDEX 总数漂移（2026-07-09 实际事故）
**症状**：`evolution.json` 50 节点但 `INDEX.md` / `paper-notes/` 有 55 篇
**根因**：cron 写完 note 但没立即触发 evolution_gen.py（周日才跑）
**修法**：见 §7 cron patch

### 6.2 派系归属到 None（节点不出现在图）
**症状**：新 node 在 JSON 里但派系是空或缺失
**根因**：`evolution_gen.py` 的 `FACTION_KEYWORDS` 没覆盖新 id
**修法**：编辑 `cron_scripts/evolution_gen.py` 加 keyword；或临时改 `evolution.json` 手动指定

### 6.3 浏览器实测 PATCH 改 7 轮才 PASS（2026-07-10 实际事故）
**症状**：subagent 报告 PASS 但 vision 截图 FAIL
**根因**：force-directed 派系引力不够 → 5 hull 严重重叠
**修法**：派系引力 0.08 → 1.6，charge -180 → -550，collision 28 → 50（commit `c6ee8fd`）

### 6.4 标签被信息卡遮挡
**症状**：E 标签只显示 "ross-disciplinary"
**根因**：labelGroup anchor middle 但 leftClamp 没避信息卡
**修法**：`refreshFactionHulls` 的 `leftClamp = 410`（避开信息卡 320px + 锚点 90px）

### 6.5 时间轴拖动后节点 opacity 没改
**症状**：`style.opacity` 全空
**根因**：d3 `.style('opacity', ...)` 写到 element.__style__ 不一定写到 inline attribute
**修法**：用 `getComputedStyle().opacity` 测，或直接看 d3 internal state

### 6.6 `evolution.json` 边过少
**症状**：50 节点但只有 48 边（理论上 50 节点应该有更多引用关系）
**根因**：S2 API 拉的 references 不全 / 部分论文没 abstract URL
**修法**：从 paper note §11 "1-hop 引用关系图" 手动补边（按 §2.2 字段填）

### 6.7 截图缓存导致 vision 误判
**症状**：vision 报告 "E 标签被截断" 但 DOM 显示完整
**根因**：`browser_vision` 拿的是缓存截图，不是当前 viewport
**修法**：用 PIL 像素扫描确认，或加 `?v=N` query string 强制刷新

---

## §7 cron patch（改进 arxiv_4dgs_scan + evolution_update）

### 7.1 现状问题
- `arxiv_4dgs_scan` 步骤 4 说"写新 note + 更新演进图"但**没指定怎么做**
- `evolution_update` 周日跑一次，**窗口 3 天 drift**
- 没有"完成度自检"环节

### 7.2 改进 1：arxiv_4dgs_scan 步骤 4 加具体步骤

**原文**：
```
### 步骤 4: 对每个新 paper
...
5. **无冲突**: 写新 note 进 INDEX + 更新演进图 + 写 `cron/arxiv-YYYY-MM-DD-candidates.md`
```

**改为**：
```
### 步骤 4: 对每个新 paper
...
5. **无冲突**（按顺序执行 5 步）:
   a. **更新 INDEX.md**: 在对应派系分组表格插入新行，更新总数 "**N 篇 paper notes**"
   b. **立即跑 evolution_gen.py**:
      ```bash
      python3 cron_scripts/evolution_gen.py
      ```
   c. **跑 check_drift.py**（首次需要先创建，见 UPDATE_EVOLUTION.md §5.3）:
      ```bash
      python3 cron_scripts/check_drift.py
      ```
      **失败则终止**：不更新不进 Telegram 通知，告诉用户"请检查 drift"
   d. **浏览器验收**（首次需要启 server）:
      ```bash
      cd docs && python3 -m http.server 8123 &
      sleep 2
      # 用 browser_navigate + browser_console 跑 UPDATE_EVOLUTION.md §5.2 的 7 步
      ```
      **失败则终止**：不更新不进 Telegram 通知
   e. **写 candidates.md** + **commit + push**:
      ```bash
      git add docs/appendix/paper-notes/ docs/appendix/paper-notes/INDEX.md docs/evolution/data/evolution.json
      git commit -m "[paper <id>] <title> 收录：派系 X"
      git push origin main
      ```
```

### 7.3 改进 2：evolution_update 改成"每日 check"模式

**原文 schedule**: `0 9 * * 0`（周日 9:00）
**改为**: `0 9 * * *`（每天 9:00）

**理由**：
- `evolution_gen.py` 是幂等的，重复跑不会出错
- 每天跑 = 把 drift 窗口从 3 天压到 1 天
- 万一有别的手动改动遗漏，第二天 cron 自动 catch up

**prompt 改进**（在原有步骤后加）：
```
### 步骤 4（新增）: 跑 check_drift.py
如果 JSON 节点数 ≠ INDEX 引用数，触发 Telegram 警告：
```
⚠ 演进图 drift 警告

JSON: 50 节点
INDEX: 55 引用
差: 5 篇未同步

详见 cron/drift-YYYY-MM-DD.md
```
```

### 7.4 改进 3：人工同步触发器

**触发**：用户在聊天说 "演进图同步" 或 "同步论文到图"
**响应**：跑 `python3 cron_scripts/evolution_gen.py` + `check_drift.py` + 浏览器验收 + commit + push（不需 Telegram 通知，因为是人工触发）

---

## §8 演进图升级大改（架构层面）

### 8.1 触发条件
- 用户明确要求改（如 "换成 3D" / "改成矩阵布局" / "加新功能"）
- 调研 subagent 报告后用户拍板

### 8.2 流程（参考 2026-07-10 演进图打磨）

1. **写调研 prompt** → 派 subagent 调研方案 → 用户拍板
2. **写执行 prompt** → 派 subagent 实现 → 用户验收
3. **强制 browser 实跑验收**（视觉 + 交互各 ≥2 PASS）
4. **验收失败 → 修 → 重跑**（不妥协 commit）
5. **commit + push**

### 8.3 验收标准（参考）

**视觉**：
- 5 hull 互不重叠
- 5 标签完整可见
- 节点清晰归位
- 整体美观

**交互**：
- 时间轴拖动 → 节点数变化
- 搜索 → 高亮 + dim
- 派系开关 → display:none
- 节点拖动 → hull 实时变形

**错误**：
- 0 JS error
- 0 404（资源 / 数据）
- d3 .style() 不破现有功能

---

## §9 相关文件 / 链接

- 主页：`docs/index.html`
- 演进图：`docs/evolution/`
- 数据：`docs/evolution/data/evolution.json`
- INDEX：`docs/appendix/paper-notes/INDEX.md`
- 方法论：`docs/05-survey-methodology.md`
- 指南：`docs/appendix/UPDATE_GUIDE.md`
- 脚本：`cron_scripts/evolution_gen.py` / `cron_scripts/add_metadata.py`
- Cron：`~/.hermes/profiles/main/cron/jobs.json`（id: arxiv_4dgs_scan / evolution_update）
- GitHub Pages：https://klkjjhjkhjhg.github.io/4dgs-mobile-rendering/evolution/

---

**最后更新**：2026-07-10（基于 2026-07-10 演进图打磨事故复盘）
**维护者**：小元 + 梁昊 review