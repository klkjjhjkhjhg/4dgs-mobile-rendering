# 国内 4DGS / Dynamic 3DGS 候选单位 — 主对话预调研种子

> **来源**：主对话 session 在派 subagent 前手动抓的"第一批锚点"，用于给 subagent 一个事实基础，避免它在空白 spec 下乱搜。
> **状态**：未经验证，需 subagent 做 A+B fact-check。

## 第一批候选（已通过公开论文/主页直接命中作者单位）

### 1. 清华大学 (Tsinghua University)
- **候选代表作**：[CVPR 2026] 4C4D: 4 Camera 4D Gaussian Splatting
- **第一作者**：yangzf-1023 (杨振飞)
- **链接**：https://github.com/yangzf-1023/4C4D
- **置信度**：高（GitHub repo + venue 标签）
- **待核实**：通讯作者 / 所属实验室（自动化系？计算机系？）

### 2. 华中科技大学 (HUST) + 杭州电子科技大学 (HDU) + 华为
- **候选代表作**：4D Gaussian Splatting for Real-Time Dynamic Scene Rendering
- **第一作者**：吴冠君 (Guanjun Wu)
- **链接**：https://arxiv.org/abs/2310.08528 / https://guanjunwu.github.io/4dgs/
- **置信度**：高（多次被引用为"4DGS 原论文"）
- **待核实**：吴冠君导师 / 实验室全称

### 3. 商汤 S-Lab + 上海 AI Lab + 北京大学 + 密歇根大学 (海外合作)
- **候选代表作**：DreamGaussian4D: Generative 4D Gaussian Splatting
- **链接**：https://arxiv.org/abs/2312.17142
- **置信度**：中（合作单位复杂，国内纯单位占比待确认）
- **备注**：北京大学单位存在，但合作方含密歇根，spec 要求"中国大陆 + 港澳"，所以北大可以收但要标注合作

## subagent 任务范围（在此基础上扩展）

需要 subagent 做：
1. **A+B fact-check** 上面 3 条：核实通讯作者 / 实验室 / 国内具体二级单位
2. **横向扩散**：从这 3 篇的 references + citations + 作者主页反查其他国内单位（目标是补到 ≥15 个）
3. **方法学**：用 `mcp_minimax_search_web_search` + arxiv listing + 国内 4DGS 综述的参考文献清单

## 推荐的反查关键词组合（subagent 启动时用）

- `"4D Gaussian Splatting" site:arxiv.org China author`
- `"dynamic 3DGS" Tsinghua OR Zhejiang OR Peking OR CAS OR HKUST 2024..2026`
- `"3DGS compression" "Peking University"` / `"Tsinghua"` / `"Zhejiang University"` / `"HKUST"`
- `"3DGS mobile" OR "mobile Gaussian splatting" site:arxiv.org`
- `"4DGS" survey China 2025`
- `"4DGS acceleration" Peking OR Beihang OR USTC OR CAS`

## 注意事项（给 subagent）

- 不要去搜"在做但还没发"的项目
- 不要把台湾 / 新加坡 / 海外华人团队算进来
- 每单位至少 2 个独立信源（论文 author affiliation + 实验室主页/教授主页）
- 论文级深度分析不要做，本 spec 只到"单位 + 代表作 + 趋势"