# 4DGS Mobile Rendering

在 **Snapdragon 8 Gen 4 / Adreno 830 + Vulkan 1.3** 上实时渲染 **动态 4D Gaussian Splatting** 的可行性调研。

## 一句话定位

> 4DGS 在桌面 RTX 3090 已有 **1000+ FPS**(@N3V) / 1462 FPS(@D-NeRF) 实测(arxiv:2503.16422, Yuan et al., NUS 2025-03);
> 在 **Snapdragon 8 Gen 3** 的 3DGS 已有 **127 FPS** 实测(arxiv:2603.11531, Du et al., **ICLR 2026**)。
>
> **Adreno 8 Gen 4 上 4DGS @ 1080p,60 FPS 应可达**(`[推测,有上述两 SOTA 作为锚]`)。
>
> 详细风险与 baseline 缺口见 §"现状与关键风险"。

---

## 这份调研是什么 · 不是什么

| 是 | 不是 |
|---|---|
| 两块调研 + 路线图 + 12 篇 paper notes | 实机 demo / 代码工程实现 |
| 列出现有公开 SOTA,标注每条数字的可追溯出处 | 拍胸脯保证 mobile 4DGS 一定跑得动 |
| 明确指出"未在公开材料找到 / 调研不足"的地方 | 凭印象补全缺失数字 |

---

## 仓库内容

```
docs/
├─ 00-goal.md             调研目标 spec(硬约束 / 必覆盖 / 产出要求)
├─ 01-high-precision-representation.md   第一块调研:离线高精度 4DGS 表示
├─ 02-rendering-acceleration.md         第二块调研:渲染加速(Vulkan 1.3 移动端)
├─ 03-end-to-end-roadmap.md              整合路线图(6 个月 M0~M6)
└─ appendix/
   ├─ paper-notes/         12 篇核心论文 PDF 全文级精读笔记(详见下)
   ├─ collection-sop.md    采集 SOP(指针型,内容在 01- §8)
   └─ vulkan-impl-notes.md Vulkan 1.3 实现笔记(指针型,内容在 02- §7)
```

---

## 调研结论(三条)

### 1. 高精度表示:四篇必读 + 一条主线

| 主线 / 备选 | 论文 | 关键数字 | 适用场景 |
|---|---|---|---|
| **主线** | **Wu-4DGS** (CVPR 2024, arxiv:2310.08528) | 82 FPS @ 800×800 on RTX 3090;HexPlane + canonical + deformation | **本项目首选** |
| 备选 1 | Deformable 3DGS (Yang 2023) | 单目路线,< 250K splats @ 30 FPS | 快速原型 |
| 备选 2 | Mega + 4DGS-1K 训练路径 | Mega 190× 存储压缩;4DGS-1K 8.94× FPS + 41.7× 压缩组合后 **几乎零精度损失** | 训练期 bitpack + 稀疏化 |

### 2. 渲染加速:7 步加速链(都在 `02-` §1)

| 步骤 | 收益(已实测/推测) | 证据 |
|---|---|---|
| 起点:vanilla 4DGS | 90 FPS @ N3V | 4DGS-1K Table 1 直接对照基线 |
| 1. Spatial-Temporal Variation Score 剪枝 | **5× sparser**,几乎无损 | 4DGS-1K Table 3 |
| 2. 训练期 bitpack(VQ + 1st-order SH distill) | **41.7× 存储压缩** | 4DGS-1K-PP / Mobile-GS Table 1 |
| 3. Tile-based GPU 优化 | 1.5~3× `推测` | 通用 GPU 实践 |
| 4. Temporal Filter mask + 跨帧复用 | **9.25× raster FPS**,PSNR -0.04 dB | 4DGS-1K Table 1,3,**Activation IoU ≈ 1** |
| 5. 内部降采样(540/720p) | 0.25~0.69× pixel `推测` | 理论值 |
| 6. FSR 2 / Arm ASR 上采样到 1080p | 2× 像素成本 `abstract` | MIT 许可,可商用 |
| 7. Vulkan 1.3 compute + fragment 分工 | 1.3~1.5× `推测` | Adreno tile-based 优势 |

**桌面总和**:3.3M → 0.67M splats,storage 2085 → 50 MB,**FPS 90 → 805 = 8.94×**。
**TITAN X(2015 Maxwell)上 4DGS-1K 仍 200+ FPS**:`arxiv:2503.16422 §7.2 直引`,直接证据 mobile 路径成立。

### 3. 移动端可迁移路径(已找到先例!)

**Mobile-GS(arxiv:2603.11531, Du et al., ICLR 2026)** —— 3DGS 类首个 **实测 Snapdragon 8 Gen 3** 的工作,**Vulkan 2.0 实现**:

| 方法 | **Snap 8 Gen 3 FPS** | Storage |
|---|---|---|
| 3DGS vanilla (quantized) | 8 | 61.8 MB |
| LocoGS-S | 17 | 8.5 MB |
| SortFreeGS | 24 | 64.3 MB |
| **Mobile-GS (Ours)** | **127** | **4.6 MB** |

**本项目最优路径 = Mobile-GS Vulkan 2.0 渲染管线 + 4DGS-1K pruning + Temporal Filter mask**。**两个 SOTA 的"取最长项"组合,论文没做,本项目可以做**(`推测,基于 Mobile-GS Table 2 + 4DGS-1K Table 1 直引`)。

---

## Paper Notes 库(12 篇,全部 PDF 全文级)

按相关性 + 时间排序:

| 年份 | 论文 | 类别 | 相关性 | 核心数字 |
|---|---|---|---|---|
| **2026-03** | **Mobile-GS** (Du, ICLR 2026, arxiv:2603.11531) | mobile-GPU | **⭐⭐⭐ 高度** | **Snap 8 Gen 3 上 127 FPS** |
| **2025-03** | **4DGS-1K** (Yuan, NUS, arxiv:2503.16422) | 4DGS 加速 | **⭐⭐⭐ 主线** | **1000+ FPS / 41.7× 压缩** |
| 2024-10 | **MEGA** (Zhang, arxiv:2410.13613) | 4DGS bitpack | ⭐⭐⭐ 对照 | 190× Technicolor 压缩 |
| **2024-02** | **4D-RotorGS** (Duan, SIGGRAPH 2024) | 4DGS 加速 | ⭐⭐⭐ | **D-NeRF 1257 FPS** |
| 2024-04 | Mip-Splatting (Yu, CVPR 2024 best student) | 3DGS 抗锯齿 | ⭐⭐ 视觉质量 | "无推理开销" |
| 2024-04 | Spacetime Gaussians (Li, CVPR 2024) | 4DGS | ⭐⭐ | CC0 视觉质量 |
| 2023-10 | Wu-4DGS (CVPR 2024, arxiv:2310.08528) | 4DGS 奠基 | ⭐⭐⭐ 主线 | 82 FPS @ 800×800 on RTX 3090 |
| 2023-09 | Deformable 3DGS (Yang) | 4DGS 备选 | ⭐⭐ | 单目,< 250K splats |
| 2023-01 | HyperReel (Attal) | NeRF dynamic | ⭐ 路线对照 | 18 FPS @ megapixel |
| 2024-06 | LightGaussian (NeurIPS 2024 Spotlight) | 3DGS 剪枝 | ⭐ | pruning 通用技术 |
| 2023 | Compact3D / CompGS (ECCV 2024) | 3DGS VQ | ⭐ | K-means codebook |
| (Wu 4DGS 原版) | Deformable 3DGS (Yang 2023) | 单目 | ⭐⭐ 备选 | (同上) |

---

## 现状与关键风险

| 状态 | 描述 |
|---|---|
| ✅ **桌面 RTX 3090 上 4DGS 1000+ FPS 实测存在**(4DGS-1K) |
| ✅ **桌面 TITAN X(2015 Maxwell)上 4DGS-1K 200+ FPS 实测** |
| ✅ **Snap 8 Gen 3 上 3DGS 127 FPS 实测存在**(Mobile-GS) |
| ❌ **Adreno 8 Gen 4 上 4DGS 实测 FPS = 0**(调研空白,需项目 M4 实测) |
| ❌ **4DGS-1K 仅 CUDA 实现,无 Vulkan/Adreno 移植**(项目 M3/M4 必须自研移植) |

**最坏情形**:即便 mobile 路径成立,在 8 Gen 4 上能否到 60 FPS,取决于:
- deformation field 的 per-frame compute 在 Adreno 上的开销(目前 `推测`)
- Temporal Filter mask 在 Adreno Vulkan 1.3 的实现效率(目前 `推测`)
- Splat 数 ≤ 300 万的剪枝 + bitpack + 上采样三件套合计开销(`推测`)

---

## 项目调研纪律(贯穿全文)

- **`绝不瞎编历史`**:`facts/discovery/never-fabricate-history` 红线,不据 CSDN / 二手综述转写为已验证数字
- 每条结论标 `[abstract 直引]` / `[PDF Table X 直引]` / `[基于 X 论文]` / `[推测]` / `[未在公开材料找到,需 PDF 核验]` / `[调研不足,需进一步实验]`
- 仓库 visibility: `private`;不写真名 / 个人邮箱 / token / 私人 key

---

## 怎么读这份调研

1. **先读 `docs/00-goal.md`**(200 行左右,明确"为什么做这件事")
2. **如果只看一个数字**:读完本文档即可。Snap 8 Gen 3 实测 127 FPS(3DGS)+ TITAN X 实测 200 FPS(4DGS-1K) = Adreno 8 Gen 4 4DGS 应 60 FPS。
3. **如果要做工程**:读 `02-rendering-acceleration.md` §1(7 步加速链) + `03-end-to-end-roadmap.md`(M0~M6 路线),然后读 `paper-notes/2026-du-mobile-gs.md` + `2025-yuan-4dgs-1k.md`。
4. **如果做调研**:直接读 `01-` / `02-` / 每篇 paper note,数字全部 PDF Table 直引。
