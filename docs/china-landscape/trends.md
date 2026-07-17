# 5 派系 x 单位 矩阵

> 数据来源: paper-first 自动聚合（从 arxiv 拉 4D/3DGS 论文 → PDF 首页 affiliation → dedupe）
> 范围: 2024-2026 (241 论文候选 / 109 PDF 解析 / 64 China 关联 / 28 institutions)
> 格子: `v` = 主攻（≥2 papers）/ `~` = 涉及（1 paper）/ `-` = 无产出
> A+B 验证: ≥2 papers 算 A+B pass；1 paper = 单源待扩展

## 5 派系分布

- **A: 4DGS 表示**: 20 个单位
- **B: 4DGS 加速**: 5 个单位
- **C: 3DGS 加速**: 12 个单位
- **D: 移动端/流式**: 0 个单位
- **E: 跨方向**: 1 个单位

## 完整矩阵

| 单位 | 所在地 | 类型 | papers | A: 4DGS 表示 | B: 4DGS 加速 | C: 3DGS 加速 | D: 移动端/流式 | E: 跨方向 | 应用场景 |
|---|---|---|---|---|---|---|---|---|
| Peking University | Beijing | 高校 | 7 | v | - | v | - | - | AIGC/生成(1) |
| Tsinghua University | Beijing | 高校 | 6 | v | - | ~ | - | - | 几何重建(2), 自动驾驶(1) |
| Hong Kong University of Science and Technology | Hong Kong | 高校（香港） | 6 | v | - | v | - | - | 几何重建(1), 人体/Avatar(1) |
| Shanghai Jiao Tong University | Shanghai | 高校 | 5 | v | ~ | v | - | - | 自动驾驶(1), 几何重建(1) |
| Chinese University of Hong Kong | Hong Kong | 高校（香港） | 4 | v | - | - | - | - | 医疗内窥镜(4), 几何重建(3) |
| Fudan University | Shanghai | 高校 | 4 | v | - | v | - | - | 通用(0) |
| The University of Hong Kong | Hong Kong | 高校（香港） | 3 | v | - | ~ | - | - | 场景编辑(1), 自动驾驶(1) |
| Huazhong University of Science and Technology | Wuhan, Hubei | 高校 | 2 | v | - | - | - | - | AIGC/生成(1) |
| Zhejiang University | Hangzhou, Zhejiang | 高校 | 2 | ~ | ~ | - | - | - | 移动端/流式(1) |
| University of Science and Technology of China | Hefei, Anhui | 高校 | 2 | ~ | ~ | - | - | - | 通用(0) |
| Harbin Institute of Technology | Harbin, Heilongjiang | 高校 | 2 | v | - | - | - | - | AIGC/生成(1) |
| Sun Yat-sen University | Guangzhou, Guangdong | 高校 | 2 | ~ | - | ~ | - | - | 通用(0) |
| Southeast University | Nanjing, Jiangsu | 高校 | 2 | v | - | - | - | - | 医疗内窥镜(1) |
| Hangzhou Dianzi University | Hangzhou, Zhejiang | 高校 | 2 | v | - | - | - | - | 几何重建(1) |
| Hong Kong Polytechnic University | Hong Kong | 高校（香港） | 1 | ~ | - | - | - | - | 通用(0) |
| ShanghaiTech University | Shanghai | 高校 | 1 | - | - | ~ | - | - | 通用(0) |
| Nanjing University | Nanjing, Jiangsu | 高校 | 1 | - | - | - | - | ~ | 通用(0) |
| Shenzhen University | Shenzhen, Guangdong | 高校 | 1 | - | - | ~ | - | - | 几何重建(1) |
| Communication University of China | Beijing | 高校 | 1 | ~ | - | - | - | - | 通用(0) |
| Wuhan University | Wuhan, Hubei | 高校 | 1 | ~ | - | - | - | - | 医疗内窥镜(1), 几何重建(1) |
| Beijing Jiaotong University | Beijing | 高校 | 1 | - | - | ~ | - | - | 通用(0) |
| University of Science and Technology Beijing | Beijing | 高校 | 1 | - | - | ~ | - | - | 自动驾驶(1) |
| Qilu University of Technology | Jinan, Shandong | 高校 | 1 | - | ~ | - | - | - | 移动端/流式(1) |
| Beihang University | Beijing | 高校 | 1 | - | ~ | - | - | - | 通用(0) |
| Chinese Academy of Sciences — Institute of Computing Technology | Beijing | 高校（中科院） | 1 | ~ | - | - | - | - | 几何重建(1), 人体/Avatar(1) |
| Chinese Academy of Sciences — Shenzhen Institute of Advanced Technology | Shenzhen, Guangdong | 高校（中科院） | 1 | ~ | - | - | - | - | 医疗内窥镜(1), 几何重建(1) |
| Xi'an Jiaotong-Liverpool University | Suzhou, Jiangsu | 高校 | 1 | ~ | - | - | - | - | 医疗内窥镜(1), 几何重建(1) |
| Nanjing University of Aeronautics and Astronautics | Nanjing, Jiangsu | 高校 | 1 | - | - | ~ | - | - | 通用(0) |

## 趋势观察

1. **A 派系（4DGS 表示）密度最高** - 国内 4DGS 起点是 HUST（CVPR 2024 4DGS），主流单位（清华/PKU/HKUST/SJTU/CUHK）持续扩张 A 派系
2. **B 派系（4DGS 加速 / 压缩 / 流式）** — USTC P-4DGS（90× 压缩）、HIT Mach Drive 流式、PD-4DGS（QLU 流式）、ADC-GS（SJTU 压缩）、4DGS-CC（BUAA + HKU 压缩）、GS-STVSR（USTC + 华为诺亚 流式）— 比 subagent 上一轮的 1 篇大幅增加（6+ 篇）
3. **D 派系（移动端 / 流式落地）** — Voyager（SJTU + ICT CAS）、Splatonic（SJTU + ICT CAS）— 都是 SJTU 的架构组主导
4. **E 派系（跨方向）** — 主要在 4DGS 生成 / 编辑 / 反渲染：CUHK 香港组（EndoGSim 等医疗系）、PKU (DreamGaussian4D 是跨 NTU 合作)、SJTU (Light4GS)
5. **港校集群（HKUST + HKU + CUHK + PolyU）** 13 papers — 主要在 A 派系；CUHK 偏医疗内窥镜，HKUST 偏 General AI + Skywork AI
6. **应用场景** — 医疗内窥镜（CUHK/WHU/SIAT-CAS 是最大集群）+ 自动驾驶（Tsinghua/PKU/USTB）是国内两大应用热点
7. **缺失的关键玩家** — 上一轮 subagent 列的 'Shanghai AI Lab'、'Huawei Noah'、'Megvii'、'Sensetime' 等大厂在这次 paper-first 扫描中**没有直接 4DGS 论文**（华为诺亚出现在 2 篇合作通讯，但不主导）— 这是 spec 第三优先级'产业落地'的真空

## spec 核心诉求（B 派系 4DGS 加速）的真实密度

- **2512.20943** (2025) — AirGS: Real-Time 4D Gaussian Streaming for Free-Viewpoint Video Experiences — 隶属: SJTU Global College (AirGS streaming)
- **2505.07539** (2025) — GIFStream: 4D Gaussian-based Immersive Video with Feature Stream — 隶属: ZJU (GIFStream 4DGS)
- **2510.10030** (2025) — P-4DGS: Predictive 4D Gaussian Splatting with 90$\times$ Compression — 隶属: USTC (P-4DGS 90× compression)
- **2504.18925** (2025) — 4DGS-CC: A Contextual Coding Framework for 4D Gaussian Splatting Data Compressio — 隶属: BUAA + HKU + Newcastle + Futurewei (4DGS-CC compression)
- **2605.11427** (2026) — PD-4DGS:Progressive Decomposition of 4D Gaussian Splatting for Bandwidth-Adaptiv — 隶属: 齐鲁工业大学 (PD-4DGS bandwidth streaming)

**合计 5 篇 4DGS 加速 / 压缩 / 流式论文** — 这是 spec 主线'移动端加速'的真实可用材料池。