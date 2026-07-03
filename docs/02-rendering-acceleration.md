# 02 — 渲染加速(Vulkan 1.3,移动端高通旗舰)

> **状态**:占位文件,由 subagent 调研后填入。
>
> **必覆盖优先级**(摘自 `docs/00-goal.md`):
> 1. 稀疏化与剪枝(importance mask)
> 2. bitpack 压缩(32→16/8 bit,量化方案,解压代价)
> 3. tile-based GPU 优化(on-tile sort,wave size,compute + fragment 分工)
> 4. 时空复用(temporal mask + frame coherence) ← **4DGS-1K-lite 核心,重点**
> 5. 上采样到 1080p(FSR 1/2 / 自研 TAA-Upsample)
>
> **对标主线**:4DGS-1K-lite 原论文/仓库、LightGS / Scaffold-GS / Mip-Splatting / GauHuman、现有移动端 3DGS/4DGS 项目、Adreno SDK + Vulkan compute 加速范式

## 推荐章节结构(checklist)

- [ ] 0. 执行摘要(1 页,benchmark 数字密集)
- [ ] 1. 加速技术树(从原始 4DGS 到 30~60 FPS 的链路)
- [ ] 2. 稀疏化与剪枝(mask 设计 / 评分方法 / 阈值经验)
- [ ] 3. bitpack(每字段位宽推荐 / 量化精度损失 / 解压实现位置)
- [ ] 4. Tile-based GPU 优化(on-tile vs host sort / wave size / compute 与 fragment 分工)
- [ ] 5. 时空复用(temporal mask 设计 / 复用率 / 串扰抑制)
- [ ] 6. 上采样到 1080p(540p / 720p / 900p 内部渲染 + FSR 对比)
- [ ] 7. Vulkan 1.3 实现细节草案
- [ ] 8. 公开 SOTA 的 mobile 4DGS FPS baseline
- [ ] 9. ≥5 项风险与未知(Adreno 半精度 / Vulkan 1.3 compute 厂商覆盖 等)

## 强制输出项

> **加速技术树**(从原始 4DGS 到目标 FPS 的每一步),**每步收益估计**(压缩比、加速比、质量损失),**Vulkan 1.3 实现草案**,**FPS baseline 表**,**≥5 项风险清单**。

## 每条结论的格式要求

> **结论陈述** + **可追溯标记**(`基于 X 论文 §Y` / `基于 X 仓库 L 文件` / `推测`)
