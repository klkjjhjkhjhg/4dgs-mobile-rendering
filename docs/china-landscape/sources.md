# Sources & 白名单

## 引用规范（沿用 `05-survey-methodology.md`）

- **1-hop 引用**：每条引用必须有直接验证源（PDF 首页 affiliation 字符串 + arxiv abs URL）
- **paper-first 流程**：本轮所有论文关联都从 arxiv 拉论文 → 抓 PDF → 抽 affiliation → dedupe
- **A+B fact-check**：每个 institution entry 至少 2 篇独立可验证论文（已标记 A+B 通过 = ≥2 papers；单源 = 1 paper）
- **白名单**（venues.md Tier 1/2）：SIGGRAPH / CVPR / ICCV / ECCV / NeurIPS / ICLR / ICML / TPAMI / TVCG / ACM TOG / arxiv cs.CV + cs.GR
- **本轮独立扩展**：不依赖 subagent 的 institution 联想；每条 paper 都从 arxiv PDF affiliation 字符串直接抽

## 数据来源链路

1. arxiv API listing: 4D/3D Gaussian Splatting 关键词搜索 (346 papers, 2024-2026)
2. arxiv abs 抓取: 346 个 author + submit date
3. arxiv PDF 抓取: 109/141 PDFs (32 个超时未完成)
4. PDF 首页 affiliation 抽取 (pdfplumber + 正则 tokenize)
5. China/港澳关键词过滤 (66 篇 China-affiliated)
6. 主对话 manual dedupe: 按 affiliation 字符串 → 28 个 institution

## 论文 URL 全量清单（去重）

- https://arxiv.org/abs/2310.08528
- https://arxiv.org/abs/2310.10642
- https://arxiv.org/abs/2312.17142
- https://arxiv.org/abs/2401.16416
- https://arxiv.org/abs/2402.03307
- https://arxiv.org/abs/2405.17872
- https://arxiv.org/abs/2406.04251
- https://arxiv.org/abs/2406.16073
- https://arxiv.org/abs/2410.13613
- https://arxiv.org/abs/2411.01218
- https://arxiv.org/abs/2411.15582
- https://arxiv.org/abs/2412.00333
- https://arxiv.org/abs/2412.06299
- https://arxiv.org/abs/2412.06424
- https://arxiv.org/abs/2412.20720
- https://arxiv.org/abs/2502.17860
- https://arxiv.org/abs/2503.06587
- https://arxiv.org/abs/2503.10286
- https://arxiv.org/abs/2503.13948
- https://arxiv.org/abs/2503.16710
- https://arxiv.org/abs/2503.18052
- https://arxiv.org/abs/2504.06815
- https://arxiv.org/abs/2504.18318
- https://arxiv.org/abs/2504.18925
- https://arxiv.org/abs/2505.07539
- https://arxiv.org/abs/2505.08196
- https://arxiv.org/abs/2505.18197
- https://arxiv.org/abs/2506.02774
- https://arxiv.org/abs/2508.02129
- https://arxiv.org/abs/2508.12015
- https://arxiv.org/abs/2510.01991
- https://arxiv.org/abs/2510.09997
- https://arxiv.org/abs/2510.10030
- https://arxiv.org/abs/2510.12174
- https://arxiv.org/abs/2510.18489
- https://arxiv.org/abs/2510.23087
- https://arxiv.org/abs/2510.27318
- https://arxiv.org/abs/2511.07122
- https://arxiv.org/abs/2511.11175
- https://arxiv.org/abs/2511.14540
- https://arxiv.org/abs/2511.18367
- https://arxiv.org/abs/2511.18755
- https://arxiv.org/abs/2511.23044
- https://arxiv.org/abs/2512.20943
- https://arxiv.org/abs/2601.17835
- https://arxiv.org/abs/2602.06343
- https://arxiv.org/abs/2603.00952
- https://arxiv.org/abs/2603.07552
- https://arxiv.org/abs/2603.11543
- https://arxiv.org/abs/2603.13783
- https://arxiv.org/abs/2604.01884
- https://arxiv.org/abs/2604.04063
- https://arxiv.org/abs/2604.18047
- https://arxiv.org/abs/2605.00177
- https://arxiv.org/abs/2605.11427
- https://arxiv.org/abs/2605.14880
- https://arxiv.org/abs/2605.16022
- https://arxiv.org/abs/2605.22020
- https://arxiv.org/abs/2605.22342
- https://arxiv.org/abs/2605.23672
- https://arxiv.org/abs/2606.10656
- https://arxiv.org/abs/2606.21753
- https://arxiv.org/abs/2607.04761
