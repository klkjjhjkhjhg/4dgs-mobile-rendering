# 综述 LaTeX 文档

> 目标: 系统性整理 4DGS 在移动端 GPU（Snapdragon 8 Gen 4 / Adreno 830 + Vulkan 1.3）实时渲染方向的最新进展。
> 与项目主文档 README.md 互补——前者侧重学术调研纵深，后者侧重工程落地路径。

## 当前状态

**M1 骨架完成**（commit 见 git log）：
- 9 节结构（Introduction / Background / Representation / Training Accel / Rendering Accel / Mobile Deployment / Datasets / Discussion / Conclusion）
- acmart + sigconf 双栏模板
- 中文支持（xeCJK + Hiragino Sans GB）
- 14 条关键 paper bib 占位（M2 回填 50+）
- `survey.pdf` 编译通过（215KB, 0 error）

## 编译

```bash
# 需要: TeX Live 2023+, acmart 包, xelatex (中文)
make           # 编译 survey.pdf
make clean     # 清理临时文件
make view      # 用 Preview.app 打开
```

## 文件结构

```
docs/survey/
├── survey.tex          # 主文件 (9 节 \input{})
├── survey.bib          # BibTeX (14 条占位)
├── Makefile            # 编译脚本
├── .gitignore          # 排除 latex 临时文件
├── sections/
│   ├── sec-1-intro.tex
│   ├── sec-2-background.tex
│   ├── sec-3-representation.tex
│   ├── sec-4-training-acceleration.tex
│   ├── sec-5-rendering-acceleration.tex
│   ├── sec-6-mobile-deployment.tex
│   ├── sec-7-datasets-metrics.tex
│   ├── sec-8-discussion.tex
│   └── sec-9-conclusion.tex
└── survey.pdf          # 编译产物
```

## 模板选择说明

- **不用 tog 官方模板**：版权非商用，GitHub Pages 公开发布有风险
- **用 acmart + sigconf**：ACM 官方开源，工业界综述通用，视觉接近 TOG

## 后续里程碑

- **M2**（下周）：54 篇 paper notes `survey_section:` 字段回填 + 主线内容填充
- **M3**（2 周后）：GitHub Action + PDF diff
- **M4**（1 月内）：跑一次 cron 模拟验收

详见 `/root/goal-archive/survey-goal.md`（原 goal 文档）。
