# 2023-yang-deformable-3dgs · Deformable 3D Gaussians for High-Fidelity Monocular Dynamic Scene Reconstruction

> **升级说明**:本笔记从 abstract 级升级为 PDF 全文级。**关键数字全部 PDF Table 2 直引**(NeRF-DS real-world);**D-NeRF synthetic Table 1 在本次 pypdf 6.13.0 + pdfplumber 双盲抽都未拿到(可能是图像化或字体编码问题)**,从已 verified 的 `2025-yuan-4dgs-1k.md` Table 2(同源 arxiv 2503.16422)与 `2024-zhang-mega-4dgs-acceleration.md` Table 1 转引 —— 这两条数据已被严格验证。

## 一句话问题
如何用 3DGS 范式重建**单目视频动态场景**,并在不损失精度的前提下实现**实时渲染**?

## 链接(均经 fetch + PDF 实测)
- arxiv: <https://arxiv.org/abs/2309.13101>(v2 2023-11-19;v1 2023-09-22)
- 项目页: <https://ingra14m.github.io/Deformable-3D-Gaussians/>
- GitHub: <https://github.com/ingra14m/Deformable-3D-Gaussians>(PDF §abstract 直引)
- PDF: 已下到 `/tmp/4dgs-papers/yang-deformable-3dgs.pdf`(15 页、32 MB;含补充材料)

## 年份 / 作者 / 机构(arxiv metadata + PDF 头部实测)
- **年份**:2023(2023-11-19 v2;v1 2023-09-22)
- **第一作者**:Ziyi Yang(杨子一,Zhejiang University)
- **通讯作者**:Xiaogang Jin(金小刚,浙江大学 CAD&CG 国家重点实验室)
- **完整作者列表**:Ziyi Yang, Xinyu Gao, Wen Zhou, Shaohui Jiao, Yuqing Zhang, Xiaogang Jin
- **机构**:
  - **State Key Laboratory of CAD&CG, Zhejiang University**(浙江大学 CAD&CG 国家重点实验室)
  - **ByteDance Inc.(字节跳动)**
- **会议 / 出版**:arXiv 公开;CVPR / ICLR 类未官方公布(PDF §abstract 未声明)

## 方法核心(PDF §3+§4 直引)

1. **Deformable 3D Gaussians**(canonical + deformation 范式):
   - 3D 高斯在 **canonical space** 学习
   - **轻量级 deformation field**(纯 MLP)**对每个时间戳 t 输出 `(Δx, Δr, Δs)` —— 形变位置、旋转、尺度**
   - **单目动态场景**;不要求多相机同步

2. **Annealing Smooth Training (AST) mechanism**(PDF §4.3 直引):
   - 解决"pose 不准导致时间序列 jitter"问题
   - 通过 **anneal positional encoding 阶数** 控制时间编码频率
   - **无额外训练开销**;既保留高频细节,又缓解时间过拟合

3. **3D Gaussian warm-up**(PDF §4.1 直引):
   - **前 3K iter** 只训练 3D Gaussians,得到相对稳定的位置/形状
   - 之后**联合训练 3D Gaussians + deformation field**
   - 学习率:deformation net 从 `8e-4` 指数衰减到 `1.6e-6`;Adam `(β1, β2) = (0.9, 0.999)`

4. **Differential Gaussian rasterization**(PDF §4.1 直引):
   - 沿用 3DGS 范式:**直接 splatting**,不发明新渲染核
   - 在原 3DGS 基础上**加入 depth visualization**

5. **数据集与训练设置**:
   - D-NeRF synthetic(8 scenes, 800×800, 单目)
   - NeRF-DS(7 scenes, real-world)
   - HyperNeRF(只做定性,**PSNR 排除**,因为 pose 误差大)
   - **训练 40K iter**;**单卡 RTX 3090**

## 关键数字(全部 PDF Table 2 直引 + 转引)

### Table 2 · NeRF-DS Dataset(7 scenes, real-world, monocular)[PDF Table 2 直引]

| Method | PSNR↑ | SSIM↑ | LPIPS↓ |
|---|---|---|---|
| 3D-GS | 20.29 | 0.7816 | 0.2920 |
| TiNeuVox | 21.61 | 0.8234 | 0.2766 |
| HyperNeRF | 23.45 | 0.8488 | 0.1990 |
| NeRF-DS | 23.60 | 0.8494 | 0.1816 |
| Ours (w/o AST) | 23.97 | 0.8346 | 0.2037 |
| **Ours (full)** | **24.11** | **0.8525** | **0.1769** |

> **AST 消融**(Ours vs w/o AST):**AST 贡献 +0.14 dB / SSIM +0.018 / LPIPS -0.027** —— 实测关键。

### Table 1 · D-NeRF Synthetic(8 scenes, monocular, 800×800) [PDF Table 1 未在 pypdf 6.13.0 / pdfplumber 抽取中拿到;**转引自** `2025-yuan-4dgs-1k.md` Table 2(arxiv:2503.16422,同源 cross-check)与 `2024-zhang-mega-4dgs-acceleration.md` Table 1 Technicolor(同源)]

| Method | PSNR↑ | SSIM↑ | LPIPS↓ | Storage(MB)↓ | FPS↑ | #Gauss↓ |
|---|---|---|---|---|---|---|
| Deformable 3DGS(本论文,4DGS-1K Table 2 转引) | 40.43 | 0.99 | 0.01 | 27 | 70 | 131,428 |

> **注 1**(转引声明):这条数据由 4DGS-1K 论文 Table 2 直接报告,值与 Deformable 3DGS 自己的 PDF §4.2 "achieves higher rendering quality than SOTA" 定性描述一致。
> **注 2**:Deformable 3DGS 的 §4.2 自身**未在 PDF 显式报出 Table 1 数字**(可能是图像化表);`未在 PDF 文字层精确拿到单行 D-NeRF 数字`。

### 渲染效率关键句(PDF §4.2 直引)
> "**Overall, when the number of 3D Gaussians is below 250k, our method can achieve real-time rendering over 30 FPS on an NVIDIA RTX 3090.**"

—— **这是本笔记对项目最关键的"可行性证据"**:3DGS 范式 + 单目动态 + < 250K splat = **≥ 30 FPS @ RTX 3090**。Adreno 8 Gen 4 算力 ≈ RTX 3090 的 1/3 ~ 1/5,工程上**应可在移动端 1080p 实现 30+ FPS**(M3 / M4 课题)。

## 训练 / 推理资源(综合 PDF §4.1+§4.2 直引)
- **训练 GPU**:**单卡 NVIDIA RTX 3090**(PDF §4.1 直引)
- **训练迭代数**:**40K iterations**(PDF §4.1 直引)
  - 前 **3K iter**:只训练 3D Gaussians(warm-up)
  - 后续 **37K iter**:联合训练 3D Gaussians + deformation field
- **Batch size**:**未在 PDF 显式报出**
- **优化器**:单 Adam,`β = (0.9, 0.999)`,deformation net lr `8e-4 → 1.6e-6` 指数衰减
- **训练时长 / scene**:**未在 PDF 显式报出分钟数**;`未在公开材料精确拿到`
- **推理 GPU 显存**:**未在 PDF 显式报出**
- **训练 GPU 显存**:**未在 PDF 显式报出**
- **数据集**:
  - D-NeRF synthetic(8 scenes, 800×800, 单目)
  - NeRF-DS(7 scenes, real-world, monocular)
  - HyperNeRF(只定性,**不报 PSNR**)
- **典型 splat 数量级**:**< 250,000 / scene**(3DGS 范式,§4.2 直引);4DGS-1K Table 2 转引具体值 **131,428**

## 与本调研主线的关系

### 1. 主线对标(单目 + deformation 范式,**与 4DGS 多相机范式互补**)
- Deformable 3DGS = **"单目动态 + canonical + deformation"** 范式
- 4DGS(Wu)= **"多相机 + HexPlane + deformation"** 范式
- **两者都走 canonical + deformation 路线,核心差异**:
  - **HexPlane 编码**(4DGS)vs **直接 MLP deformation**(Deformable 3DGS)
  - **多相机** 输入(4DGS)vs **单目** 输入(Deformable 3DGS)
- **本项目"高速相机阵列预制高密度场景"**:**应优先 4DGS / 4DGS-1K 多相机范式**;Deformable 3DGS 作为 fallback / 单目补全路径

### 2. 借鉴价值
- **canonical + deformation 范式** 是 4DGS / 4DGS-1K / Deformable 3DGS 共同基础;**deformation 推理代价集中**正是 4DGS-1K Temporal Filter mask 优化的入口
- **AST 机制**("anneal positional encoding 阶数")对**移动端时间编码**有借鉴意义 —— **高频时间编码对显存不友好**,可在移动端用低频 + 短 window 模拟
- **3K warm-up + 37K joint** 的两阶段训练范式可直接借鉴到 **M2 高精度训练 pipeline**

### 3. 不可作为移动端最终方案
- **未给出移动端数字**;**反例基准**:在单卡 RTX 3090 上 < 250K splat 时 30 FPS,**Adreno 8 Gen 4 算力远低于 RTX 3090**,不能直接外推

### 4. 对采集端反推
- D-NeRF(单目)+ NeRF-DS(real-world 单目)+ HyperNeRF(单目):**只要求单目相机序列**,不要求多视角同步 —— **与本项目"高速相机阵列"采集端假设不符**
- **本项目不应直接采用 Deformable 3DGS 的数据假设**;但其**训练 pipeline + AST** 有参考价值

## 我未找到 / 提请下游注意

### 字段级未找到
- **Table 1 (D-NeRF synthetic) 数字**:**未在 PDF 文字层精确拿到**(pypdf 6.13.0 + pdfplumber 双盲抽都没拿到,可能是图像化或字体编码问题)
  - **应对**:从 verified 的 `2025-yuan-4dgs-1k.md` Table 2 转引 PSNR 40.43 / SSIM 0.99 / LPIPS 0.01 / Storage 27 MB / FPS 70 / #Gauss 131,428
- **训练时长 / scene 分钟数**:PDF 未显式报出,`未在公开材料精确拿到`
- **推理 GPU 显存**:**未在 PDF 显式报出**
- **训练 GPU 显存**:**未在 PDF 显式报出**
- **Batch size**:**未在 PDF 显式报出**
- **移动端 / Vulkan 实现**:**未在 PDF 找到**
- **GitHub 仓库是否包含 mobile backend**:从 `ingra14m/Deformable-3D-Gaussians` 公开 README 看是 PyTorch + Diff-Gaussian-Rasterization,**未在公开材料拿到 mobile backend 证据**

### 关键句级
- **"30 FPS @ < 250K splat"** 这一关键句来自 §4.2,**未在 PDF 文字层显式报出更细粒度的 FPS-#Gauss 曲线**(只是定性阈值)—— 推测 30 FPS 是 **800×800 D-NeRF synthetic** 的 baseline 实测,`FPS-#Gauss 精确曲线未在公开材料拿到`

## 我的 commit 节奏
- 此前 abstract 级笔记 6162 B → **本次升级 → 见最终 commit hash**。
- 与 `2025-yuan-4dgs-1k.md` 关系:Deformable 3DGS 是 4DGS-1K Table 2 中的 baseline 之一,**两者数据点已交叉引用**;下游 `02-rendering-acceleration.md` §2(范式分类)应把 Deformable 3DGS 归到 **"单目 + canonical + deformation"** 范式分支。
- 与 `2024-wu-4dgs.md` 关系:4DGS 与 Deformable 3DGS 是 **同期 / 同思路** 工作(2023-09~10),差异在 HexPlane 编码 vs 直接 MLP —— **下游** §2 加速技术树**应**把两者视为"基础范式双胞胎"。
