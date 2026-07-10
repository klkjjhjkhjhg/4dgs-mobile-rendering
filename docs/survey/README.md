# 综述 LaTeX 文档

> 目标: 系统性整理 4DGS 在移动端 GPU（Snapdragon 8 Gen 4 / Adreno 830 + Vulkan 1.3）实时渲染方向的最新进展。
> 与项目主文档 README.md 互补——前者侧重学术调研纵深，后者侧重工程落地路径。

## 当前状态

**v4.4c 完成**（commit `92ab8d8`，2026-07-11；演进至 v4.4c 跨栏修复）：

- 9 节结构（Introduction / Background / Representation / Training Accel / Rendering Accel / Mobile Deployment / Datasets / Discussion / Conclusion）
- acmart + sigconf 双栏模板，xelatex 路径 + xeCJK font fallback (Noto CJK / Hiragino Sans GB)
- 60 条 bib（54 篇 paper notes + 6 篇 cross-disciplinary，由 `scripts/generate_bib.py` 自动生成）
- 54 篇 paper notes 全部已注入 `survey_section:` 字段（`scripts/assign_survey_section.py` 跑过）
- `survey.pdf` 编译通过（237KB / 15 页 / 0 error，xelatex 3-pass）

## 编译

```bash
# 需要: TeX Live 2023+, acmart 包, xelatex (中文)
make           # 编译 survey.pdf
make clean     # 清理临时文件
make view      # 用 Preview.app 打开
```

CI 路径见 `.github/workflows/survey.yml`（GitHub Action 装 `texlive-full` + `fonts-noto-cjk`，每天 UTC 09:00 自动编译 + commit PDF 回 repo，`[skip ci]` 避免循环）。

## 文件结构

```
docs/survey/
├── survey.tex          # 主文件 (9 节 \input{}) + preamble (xeCJK + \headheight)
├── survey.bib          # BibTeX (60 条, 54 自动 + 6 cross-disc)
├── Makefile            # 编译脚本 (xelatex + bibtex)
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
├── EG_SURVEY_REFERENCE.md    # 3 篇 arXiv survey + 1 EG STAR abstract
├── SURVEY_RUBRIC.md          # 6 维度评价标准 (A/B 双盲评)
└── survey.pdf                # 编译产物 (v4.4c)
```

## 模板选择说明

- **不用 tog 官方模板**：版权非商用，GitHub Pages 公开发布有风险
- **用 acmart + sigconf**：ACM 官方开源，工业界综述通用，视觉接近 TOG

## 演进时间线

- **v1** (中文稿)：M2b 9 节内容填充（commit `38de484`）
- **v2** (英文)：A/B 盲评 2.4/5 → EG 必要结构（commit `ec42172`）
- **v3** (EG 验收)：D/E/F 盲评 3.0/5 → 9/14 EG 项就位（commit `d23ed3b`）
- **v4** (扩充)：H 内容扩充 → 14pp 4.08/5（commit `9a254a4`）
- **v4.1** (修 bug)：I1/I2/I3 复评 4.05/5 → 修重复段（commit `2320aaa`）
- **v4.2** (跨栏)：4 个 table 跨双栏（commit `7b1719a`）
- **v4.3** (右对齐)：数字列 `r` 对齐（commit `63d4d7d`）
- **v4.4** (headheight)：消 fancyhdr warning（commit `7852fad`）
- **v4.4c** (Table 2 限宽)：tab:representation `p{}` 限宽 + `\scriptsize`（commit `92ab8d8`）

详见 `EG_SURVEY_REFERENCE.md` + `SURVEY_RUBRIC.md`。

## 后续目标

- 调研规范**已沉淀**到 `docs/mission/mission.md` + `docs/mission/goal-brief.md`（49 → 54 篇漂移已记录）
- 调研方法论（4 派系 / 一跳规则 / 5 段格式）见 `docs/05-survey-methodology.md`
- 投稿准备按需进行——目前停在"提升文章质量"阶段（2026-07-08 拍板：无投稿 deadline）
