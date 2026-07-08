# 演进图（Evolution Graph）

> **目的**：把 49 篇 paper notes 的"时间 × 派系 × 引用"3 维关系**可视化**，3D 渲染 + 2D fallback。

---

## 0. 30 秒读懂

打开 `index.html` 看到的是：
- **3D 视图**（默认）= 时间 (X) × 派系 (Y) × 引用密度 (Z) 的散点图
- **2D fallback**（右下角切换）= 时间 × 派系的双轴 DAG

**5 个派系** = 4 个核心派系 + 1 个 Cross-disciplinary：
- A 4DGS 表示（红）
- B 4DGS 加速 / 动静态分离（蓝）
- C 3DGS 加速（绿）
- D 移动端 / 流式落地（黄）
- E Cross-disciplinary（紫）

**4 个转折点**（T1 / T2 / T3 / T4）= **半透明橙色面**作为时间标记：
- T1 (2023.7) — 3DGS 起点
- T2 (2024.1) — 4DGS 起点
- T3 (2025.3) — 4DGS-1K 动静态分离
- T4 (2025.4) — Lumina 移动端 + 体系结构

---

## 1. 文件结构

```
docs/evolution/
├── index.html              # Three.js 主入口（19KB）
├── styles.css              # 样式（4.8KB）
├── data/evolution.json     # 49 节点 + 48 边（12KB）
└── README.md               # 本文件

scripts_refs/evolution_gen.py  # 自动生成 evolution.json（7.7KB）
```

---

## 2. 本地预览

演进图是纯静态 HTML + 三个 CDN（Three.js + OrbitControls）。**用 HTTP 服务器打开**（**不要用 `file://` 协议** —— fetch 加载 JSON 会失败）。

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

### 3D 视图（默认）
- **左键拖动** = 旋转视角
- **滚轮** = 缩放
- **鼠标 hover 节点** = tooltip（题目 / 派系 / 时间 / arxiv / 评级）
- **点击节点** = 弹窗 paper note 摘要 + 跳转链接
- **右上角派系筛选** = 4 个 checkbox（取消勾选 = 隐藏该派系）
- **右上角时间范围** = 2 个 slider（控制 X 轴起止）
- **右下角 "2D 视图" 按钮** = 切换 2D fallback

### 2D 视图（fallback）
- **派系筛选** = 同 3D
- **时间范围** = 同 3D
- **hover 节点** = tooltip
- **点击节点** = 弹窗

---

## 4. 数据源

### v1（当前）
- **49 节点** = `scripts_refs/evolution_gen.py` 从 49 篇 note 文件名 + INDEX.md 自动解析
- **48 边** = 手写（基于 Lumina 30 references 验证 + 49 篇中明显引用关系）

### v2（计划）
- 边 = **S2 API 拉取**（每篇 note 的 references 自动构建边）
- 节点 `refs` 字段 = S2 API 引用数（用于 3D Z 轴凸起高度）

---

## 5. 自动更新

由 `cron-paper-evolve`（每周日 9:00）触发：
1. 跑 `scripts_refs/evolution_gen.py` 重生成 `evolution.json`
2. git commit
3. Telegram 通知

**演进图与 INDEX.md 同步**：每改 1 个 note 标题 / 派系 / 时间 → 周日自动重生成。

---

## 6. GitHub Pages 部署

1. 仓库 **Settings → Pages**
2. Source: `main` branch / `docs` folder
3. Custom path: `/evolution`（用 `docs/evolution/index.html` 直接发布）
4. 访问: `https://<username>.github.io/4dgs-mobile-rendering/evolution/`

---

## 7. 已知限制

- **3D Z 轴** = 引用密度（refs 字段），**v1 全部为 0**（手写节点没有引用数）—— 所有节点 Z=0，呈平面分布。**v2 接入 S2 API 后凸起**
- **2D fallback** = 节点可能重叠（49 节点 + 5 派系 + 时间密集区）
- **移动端** = 默认 2D fallback（3D 性能考虑）
- **CDN 失败** = 3D 不工作，自动 fallback 2D

---

## 8. 不在本演进图范围

- ❌ 派系 SOTA 排名（见 `README.md` §2）
- ❌ README §1 论据表（见 `README.md` §1）
- ❌ 4 docs 调研正文（见 `docs/00-04`）
- ❌ 实验数据（见 `experiments/`）

---

## 9. 引用一览

- **数据源** = `docs/appendix/paper-notes/INDEX.md`
- **白名单** = `venues.md`
- **方法论** = `docs/05-survey-methodology.md`
- **mission** = `docs/mission/mission.md`
- **Three.js** = https://threejs.org/
- **OrbitControls** = https://threejs.org/docs/#examples/en/controls/OrbitControls
