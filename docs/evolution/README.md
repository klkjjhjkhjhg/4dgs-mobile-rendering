# 演进图（Evolution Graph）

> **目的**：把 54 篇 paper notes 的"时间 × 派系 × 引用"3 维关系**可视化**，**d3 force-directed 2D**（早期 v1 试过 Three.js 3D，commit `db6e572` / `16f3e2a` 因 GitHub Pages ES module 不稳定回退到 r147 UMD；之后 commit `12966ff` 进一步简化为 2D 力导向布局）。

---

## 0. 30 秒读懂

打开 `index.html` 看到的是：

- **2D 力导向图**（默认）= 节点按引用关系力布局，X 轴 = 时间，Y 轴 = 派系，颜色 = 派系
- 节点大小 ∝ `refs` 字段（被引数）
- 边 = 一跳引用关系（手写 + 后续 S2 API 自动）

**5 个派系** = 4 个核心派系 + 1 个 Cross-disciplinary：
- A 4DGS 表示（红）
- B 4DGS 加速 / 动静态分离（蓝）
- C 3DGS 加速（绿）
- D 移动端 / 流式落地（黄）
- E Cross-disciplinary（紫）

**4 个转折点**（T1 / T2 / T3 / T4）= 派系里程碑用大节点标记：
- T1 (2023.7) — 3DGS 起点
- T2 (2024.1) — 4DGS 起点
- T3 (2025.3) — 4DGS-1K 动静态分离
- T4 (2025.4) — Lumina 移动端 + 体系结构

---

## 1. 文件结构

```
docs/evolution/
├── index.html              # d3 force-directed 主入口 (45.9KB)
├── styles.css              # 样式
├── data/evolution.json     # 54 节点 + 56 边 (19.7KB, total_nodes=54)
└── README.md               # 本文件

cron_scripts/evolution_gen.py  # 自动生成 evolution.json (从 INDEX.md 解析)
```

---

## 2. 本地预览

演进图是纯静态 HTML + d3 CDN。**用 HTTP 服务器打开**（**不要用 `file://` 协议** —— fetch 加载 JSON 会失败）。

```bash
cd ~/Codes/4dgs-mobile-rendering
python3 -m http.server 8000 --directory docs/evolution
# 浏览器打开 http://localhost:8000
```

或者用任意静态服务器：
```bash
npx http-server docs/evolution -p 8000
```

---

## 3. 交互

### 2D 力导向视图（默认）
- **左键拖动节点** = 重排力布局
- **滚轮** = 缩放
- **鼠标 hover 节点** = tooltip（题目 / 派系 / 时间 / arxiv / 评级）
- **点击节点** = 弹窗 paper note 摘要 + 跳转链接
- **右上角派系筛选** = 5 个 checkbox（取消勾选 = 隐藏该派系）
- **右上角时间范围** = 2 个 slider（控制 X 轴起止）

---

## 4. 数据源

### v1（当前）
- **54 节点** = `cron_scripts/evolution_gen.py` 从 54 篇 note 文件名 + INDEX.md 自动解析
- **56 边** = 手写（基于 Lumina 30 references 验证 + 54 篇中明显引用关系）

### v2（计划）
- 边 = **S2 API 拉取**（每篇 note 的 references 自动构建边）
- 节点 `refs` 字段 = S2 API 引用数（用于节点大小）

---

## 5. 自动更新

由 `cron-paper-evolve`（每周日 9:00）触发：
1. 跑 `cron_scripts/evolution_gen.py` 重生成 `evolution.json`
2. git commit
3. Telegram 通知

**演进图与 INDEX.md 同步**：每改 1 个 note 标题 / 派系 / 时间 → 周日自动重生成。
