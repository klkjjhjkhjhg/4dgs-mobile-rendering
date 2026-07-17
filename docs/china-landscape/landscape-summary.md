# 中国 4DGS / 3DGS 调研 — 速览

> **目的**: 识别国内（含港澳）在 4DGS 加速 / Dynamic 3DGS 方向活跃的单位 + 趋势
> **方法**: paper-first（arxiv listing → PDF affiliation → dedupe），不靠印象
> **数据时间**: 2024-2026（截至 2026-07-17 扫描）
> **详细**: 见 [READING-GUIDE.md](./READING-GUIDE.md)（按地区分类 + 28 个单位深度档）
> **趋势**: 见 [trends.md](./trends.md)（5 派系 × 单位矩阵）
> **时间线**: 见 [timeline.md](./timeline.md)（按季度）

## 速查（按 paper 数排序）

| 排名 | 单位 | 所在地 | Papers | A+B |
|---:|---|---|---:|:-:|
| 1 | [Hong Kong University of Science and Technology](./institutions/HKUST.md) | Hong Kong | 6 | ✅ |
| 2 | [Chinese University of Hong Kong](./institutions/CUHK.md) | Hong Kong | 4 | ✅ |
| 3 | [The University of Hong Kong](./institutions/HKU.md) | Hong Kong | 3 | ✅ |
| 4 | [Hong Kong Polytechnic University](./institutions/PolyU.md) | Hong Kong | 1 | ⚠ |
| 5 | [Peking University](./institutions/PKU.md) | Beijing | 7 | ✅ |
| 6 | [Tsinghua University](./institutions/Tsinghua.md) | Beijing | 6 | ✅ |
| 7 | [Shanghai Jiao Tong University](./institutions/SJTU.md) | Shanghai | 5 | ✅ |
| 8 | [Fudan University](./institutions/Fudan.md) | Shanghai | 4 | ✅ |
| 9 | [Hangzhou Dianzi University](./institutions/HDU.md) | Hangzhou, Zhejiang | 2 | ✅ |
| 10 | [Harbin Institute of Technology](./institutions/HIT.md) | Harbin, Heilongjiang | 2 | ✅ |
| 11 | [Huazhong University of Science and Technology](./institutions/HUST.md) | Wuhan, Hubei | 2 | ✅ |
| 12 | [Southeast University](./institutions/SEU.md) | Nanjing, Jiangsu | 2 | ✅ |
| 13 | [Sun Yat-sen University](./institutions/SYSU.md) | Guangzhou, Guangdong | 2 | ✅ |
| 14 | [University of Science and Technology of China](./institutions/USTC.md) | Hefei, Anhui | 2 | ✅ |
| 15 | [Zhejiang University](./institutions/ZJU.md) | Hangzhou, Zhejiang | 2 | ✅ |

_... 共 28 个 institution，详见 [READING-GUIDE.md](./READING-GUIDE.md)_

## spec 主线（B 派系：4DGS 加速 / 压缩 / 流式）

**5 篇** 直接产出，可作为本项目（移动端实时 4DGS）合作 / 招聘候选池。

- [2505.07539](https://arxiv.org/abs/2505.07539) (2025) — GIFStream: 4D Gaussian-based Immersive Video with Feature Stream
- [2504.18925](https://arxiv.org/abs/2504.18925) (2025) — 4DGS-CC: A Contextual Coding Framework for 4D Gaussian Splatting Data Compression
- [2512.20943](https://arxiv.org/abs/2512.20943) (2025) — AirGS: Real-Time 4D Gaussian Streaming for Free-Viewpoint Video Experiences
- [2510.10030](https://arxiv.org/abs/2510.10030) (2025) — P-4DGS: Predictive 4D Gaussian Splatting with 90$\times$ Compression
- [2605.11427](https://arxiv.org/abs/2605.11427) (2026) — PD-4DGS:Progressive Decomposition of 4D Gaussian Splatting for Bandwidth-Adaptive Dynamic Scene Streaming

## spec 第四优先级提示

**国内大厂直接产出 4DGS / 3DGS 论文仍为空白**：
- 上轮扫描提到的 Shanghai AI Lab / Huawei Noah / Megvii / Sensetime 等大厂在本次 paper-first 扫描中**未直接命中以它们为主导通讯作者的 4DGS/3DGS 论文**
- 华为诺亚出现在 2 篇合作通讯（GS-STVSR + DreamGaussian4D），但不主导
- **结论**：国内大厂的 4DGS 工作可能未公开发表，或发表为内部技术报告 / 商业 SDK 形式
- **建议**：下一轮扫描增加招聘宣讲 / 技术博客 / 中文 arXiv 综述的引用清单，或直接联系大厂图形组 PM
