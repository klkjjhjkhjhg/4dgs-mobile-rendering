# Top 合作候选 shortlist（小米图形架构部视角）

> **目的**：服务主业（小米图形架构部）的对外合作候选清单。
> **数据基础**: 第一轮 paper-first 扫描 28 institutions / 63 papers；Phase 1 反查通讯作者主页 / DBLP。
> **未完成项**: 团队规模、alumni、职称、增量论文 — 见下方各 entry 后续 TODO。

## Tier 1: high（强烈推荐）

### 1. Peking University  (Beijing)
- **代表老师**: Ziwei Liu (Professor (待人工确认职称))
- **个人主页**: https://liuziwei7.github.io/
- **合作切入点**: AIGC/生成
- **代表作**: [2312.17142](https://arxiv.org/abs/2312.17142) — DreamGaussian4D: Generative 4D Gaussian Splatting
- **Papers**: 7 篇；papers 详见 `institutions/PKU.md`

### 2. Tsinghua University  (Beijing)
- **代表老师**: Yebin Liu (Professor (待人工确认职称))
- **个人主页**: https://www.au.tsinghua.edu.cn/en/info/1080/3314.htm
- **合作切入点**: 自动驾驶
- **代表作**: [2511.11175](https://arxiv.org/abs/2511.11175) — Dynamic Gaussian Scene Reconstruction from Unsynchronized Videos
- **Papers**: 6 篇；papers 详见 `institutions/Tsinghua.md`

### 3. Chinese University of Hong Kong  (Hong Kong)
- **代表老师**: Hongliang Ren (Professor (待人工确认职称))
- **个人主页**: https://www.labren.org/
- **合作切入点**: 医疗内窥镜
- **代表作**: [2406.16073](https://arxiv.org/abs/2406.16073) — LGS: A Light-weight 4D Gaussian Splatting for Efficient Surgical Scene Reconstruction
- **Papers**: 4 篇；papers 详见 `institutions/CUHK.md`

### 4. Fudan University  (Shanghai)
- **代表老师**: Li Zhang (Professor (待人工确认职称))
- **个人主页**: https://fudan-zvg.github.io/
- **合作切入点**: 通用
- **代表作**: [2310.10642](https://arxiv.org/abs/2310.10642) — Real-time Photorealistic Dynamic Scene Representation and Rendering with 4D Gaussian Splatting
- **Papers**: 4 篇；papers 详见 `institutions/Fudan.md`

## Tier 2: medium（可考虑）

### 1. Hong Kong University of Science and Technology  (Hong Kong) — 6 papers
   - PI: Dan Xu | 需人工搜
   - 代表作: [2410.13613](https://arxiv.org/abs/2410.13613)
   - 切入点: 人体/Avatar

### 2. Shanghai Jiao Tong University  (Shanghai) — 5 papers
   - PI: Yu Feng | 需人工搜
   - 代表作: [2511.18755](https://arxiv.org/abs/2511.18755)
   - 切入点: AIGC/生成, 移动端/流式, 自动驾驶

### 3. The University of Hong Kong  (Hong Kong) — 3 papers
   - PI: Hengshuang Zhao | 需人工搜
   - 代表作: [2510.01991](https://arxiv.org/abs/2510.01991)
   - 切入点: 场景编辑, 自动驾驶

### 4. Huazhong University of Science and Technology  (Wuhan, Hubei) — 2 papers
   - PI: Xinggang Wang | https://xinggangw.info/
   - 代表作: [2310.08528](https://arxiv.org/abs/2310.08528)
   - 切入点: AIGC/生成

### 5. Zhejiang University  (Hangzhou, Zhejiang) — 2 papers
   - PI: Hujun Bao | http://www.cad.zju.edu.cn/home/bao/
   - 代表作: [2505.07539](https://arxiv.org/abs/2505.07539)
   - 切入点: 移动端/流式

### 6. University of Science and Technology of China  (Hefei, Anhui) — 2 papers
   - PI: Zhibo Chen | https://faculty.ustc.edu.cn/chenzhibo
   - 代表作: [2510.10030](https://arxiv.org/abs/2510.10030)
   - 切入点: 通用

### 7. Harbin Institute of Technology  (Harbin, Heilongjiang) — 2 papers
   - PI: Wangmeng Zuo | http://homepage.hit.edu.cn/wangmengzuo?lang=en
   - 代表作: [2412.06424](https://arxiv.org/abs/2412.06424)
   - 切入点: AIGC/生成

### 8. Sun Yat-sen University  (Guangzhou, Guangdong) — 2 papers
   - PI: Jian-Fang Hu | https://cse.sysu.edu.cn/teacher/HuJianfang
   - 代表作: [2502.17860](https://arxiv.org/abs/2502.17860)
   - 切入点: 通用

### 9. Southeast University  (Nanjing, Jiangsu) — 2 papers
   - PI: Ming Li | https://mingli-ai.github.io/
   - 代表作: [2605.22342](https://arxiv.org/abs/2605.22342)
   - 切入点: 医疗内窥镜

### 10. Hangzhou Dianzi University  (Hangzhou, Zhejiang) — 2 papers
   - PI: Yanyan Li | https://www.researchgate.net/scientific-contributions/Yanyan-Li-2082229610
   - 代表作: [2503.16710](https://arxiv.org/abs/2503.16710)
   - 切入点: 通用

## Tier 3: low（暂缓）

_14 个 institution 单源或 PI 主页未命中，详见 `institutions/institutions.json` 的 `co_op_value=low` entry。_

## TODO（后续人工 + 工具补强）

Phase 1/2 subagent 路径已走到 ROI 边际：HTML 抓取失败率高（JS shell / 跨域 block / 老旧 site）。剩下增量扩 paper 150-200 + 团队规模 + alumni 需要：

1. **手工查 DBLP**: 每个 PI 一次 `https://dblp.org/search?q=<name>`，获取 2024-2026 publications
2. **查实验室主页 publications 列表**: 用 `mcp_minimax_search_web_search` 单独搜每个 PI 的实验室主页（如 `xinggangw.info/publications`）
3. **Google Scholar 个人页**: 直接浏览器打开 `scholar.google.com/citations?user=<id>` （subagent 环境无 scholar ID）
4. **校友去向**: 看每位 PI 主页的 `alumni` / `former members` 段落 + LinkedIn 反查
5. **职称确认**: 看 institution 人事页面或 PI 主页 header

## Phase 1 进度

- 28 个 PI 中:**15 个** 找到 homepage 或 DBLP（命中率 54%）
- **0 个增量 paper**（HTML 抓取失败 / Phase 2 max_iterations 截断）
- **增量扩 paper 150-200 目标未达成**（spec 落空）
