# Vulkan 1.3 实现细节笔记

> 状态:占位。subagent 在 `02-` 调研中期填入。

## 应当包含的内容(checklist)

- [ ] 必备 Vulkan 1.3 拓展清单
- [ ] Compute shader 与 fragment shader 的分工(每阶段的 pipeline 划分)
- [ ] 显存布局(SoA vs AoS,per-frame uniform / SSBO / UBO 用法)
- [ ] On-tile sort 在 Adreno 上的实现要点
- [ ] Wave size 与 occupancy 调优指南
- [ ] 与 4DGS-1K-lite 公开实现的对照清单
- [ ] 已知 Android 厂商平台兼容性(Snapdragon 8 Gen 3 / 4 实测差异)
