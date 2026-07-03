# Vulkan 1.3 实现细节笔记

> **状态**:内容已分阶段落入主体调研文档。
>
> 本文件**不再写新内容**(避免与主体文档重复 / 浪费 commit);只保留**索引**,告诉你"Vulkan 实现细节该看哪儿"。

## 速查索引

| 用户预期的问题 | 在哪儿找 |
|---|---|
| 必备 Vulkan 1.3 拓展清单 | [`docs/02-rendering-acceleration.md` §7.4 "Adreno 兼容性要点"](../../02-rendering-acceleration.md#74-adreno-兼容性要点) |
| Compute shader 与 fragment shader 的分工(每阶段的 pipeline 划分) | 同上 §7.1 "Compute + Fragment 分工" |
| 显存布局(SoA vs AoS,per-frame uniform / SSBO / UBO 用法) | 同上 §7.2 "显存布局(SoA)" |
| On-tile sort 在 Adreno 上的实现要点 | 同上 §4 "Tile-based GPU 优化(Adreno 特别重要)" + §7.1 |
| Wave size 与 occupancy 调优指南 | 同上 §7.2 末段 + §7.4 |
| 与 4DGS-1K-lite 公开实现的对照清单 | 同上 §7.3 "与 4DGS-1K-lite 对标 (`[调研不足]`)" —— **4DGS-1K-lite 公开论文未找到**,对照清单基于推测,需后续实验 |
| 已知 Android 厂商平台兼容性(Snapdragon 8 Gen 3 / 4 实测差异) | 同上 §9.1 第 4、5 项风险 + §7.4 |

## 加速技术树里的"Vulkan 步骤"

参考 [`docs/02-rendering-acceleration.md` §1 "加速技术树"](../../02-rendering-acceleration.md#1-加速技术树从原始-4dgs--30-60-fps--1080p-on-snap-8-gen-4) 第 7 步 — "Vulkan 1.3 compute + fragment 分工",其中 §7.5 "性能数字" 给出的纸面估算**全部为推测**。

## 与其他关系说明

详见 `collection-sop.md` "主体文档 vs 附录 vs 路线图 关系说明"。本节与该节同步。

## 来源标注延续

沿用主体文档的标注约定:`[abstract 直引]` / `[基于 X 论文]` / `[推测]` / `[未在公开材料找到,需 PDF 核验]` / `[调研不足,需进一步实验]`。本附录指向的所有内容均继承此约定。

## 调研不足项专项(本附录主动汇总)

Vulkan 这一块是本调研最大"纸上谈兵"区,以下 5 项明确**调研不足**,必须在对应里程碑实测补:

1. **`VkPhysicalDeviceTileShadingFeatures` 在 Adreno 7xx/8xx 各驱动的支持情况** —— `02- §9.1.5`
2. **`storageBuffer16BitAccess` / `storageBuffer8BitAccess` 在 Adreno 各 SKU 上的 feature 差异** —— `02- §9.1.4`
3. **on-tile compute vs host-side sort 在 Adreno 730/740/750/830 的实际开销比** —— `02- §7.5`(实测填补 §1 加速技术树的步骤 3 收益估计)
4. **Adreno 上 fp16 storage 的精度损失对比 fp32 PSNR 数字** —— `02- §3.1 + §9.1.3`
5. **Vulkan 1.3 compute + FSR 2 / Arm ASR 联合调度的实测帧时间** —— `02- §6 + §7.5`

以上 5 项单独立项,在 M4 / M5 阶段实测后,再回填进 `02- §7`。
