# Paper Notes × Local PDF 索引

> **本地 PDF stash**:`/.pdfs/`(仓库根目录,**不进 git**,见 `.gitignore`)
> **命名约定**:大部分用纯 arxiv id(`<arxiv-id>.pdf`),4 篇"早期下"的用易读命名(`4DGS-1K.pdf` / `wu-4dgs.pdf` 等)
> **用途**:离线阅读 + `pdfplumber` / `pypdf` 脚本读取 + 团队成员本地分发

## 19 篇 paper ↔ 本地 PDF 索引

| paper note 文件 | arxiv id | 本地 PDF | 页数 | 大小 |
|---|---|---|---|---|
| `2023-attal-hyperreel.md` | 2301.02238 | `.pdfs/attal-hyperreel.pdf` | 16 | 29 MB |
| `2023-fan-lightgaussian.md` | 2311.17245 | `.pdfs/2311.17245.pdf` | 19 | 12 MB |
| `2023-navaneet-compact3d.md` | 2312.08826 | `.pdfs/2312.08826.pdf` | 11 | 0.3 MB |
| `2023-yang-deformable-3dgs.md` | 2309.13101 | `.pdfs/yang-deformable-3dgs.pdf` | 15 | 31 MB |
| `2024-chen-fcgs.md` | 2410.08017 | `.pdfs/2410.08017.pdf` | 27 | 20 MB |
| `2024-chen-hacpp.md` | 2501.12255 | `.pdfs/2501.12255.pdf` | 18 | 11 MB |
| `2024-duan-4drotorgs.md` | 2402.03306 | `.pdfs/2402.03306.pdf` | 16 | 0.4 MB |
| `2024-feng-flashgs.md` | 2408.07967 | `.pdfs/2408.07967.pdf` | 14 | 4 MB |
| `2024-li-spacetime-gaussians.md` | 2312.16812 | `.pdfs/2312.16812.pdf` | 27 | 47 MB |
| `2024-liu-efficientgs.md` | 2404.12777 | `.pdfs/2404.12777.pdf` | 9 | 8 MB |
| `2024-wu-4dgs.md` | 2310.08528 | `.pdfs/wu-4dgs.pdf` | 15 | 4 MB |
| `2024-yu-mip-splatting.md` | 2311.16493 | `.pdfs/2311.16493.pdf` | 19 | 35 MB |
| `2024-zhang-mega-4dgs-acceleration.md` | 2410.13613 | `.pdfs/zhang-mega.pdf` | 15 | 4 MB |
| `2025-huang-seele.md` | 2503.05168 | `.pdfs/2503.05168.pdf` | 11 | 7 MB |
| `2025-liu-4dgrt.md` | 2509.10759 | `.pdfs/2509.10759.pdf` | 22 | 43 MB |
| `2025-shi-sparse4dgs.md` | 2511.07122 | `.pdfs/2511.07122.pdf` | 9 | 2.6 MB |
| `2025-yuan-4dgs-1k.md` | 2503.16422 | `.pdfs/4DGS-1K.pdf` | 20 | 35 MB |
| `2025-zheng-4dgcpro.md` | 2509.17513 | `.pdfs/2509.17513.pdf` | 26 | 40 MB |
| `2026-du-mobile-gs.md` | 2603.11531 | `.pdfs/mobile-gs.pdf` | 19 | 9 MB |

## 总计

- **19 篇 paper notes ↔ 19 个本地 PDF**(一一对应,无遗漏)
- **约 367 MB 总计**

## 重新下载某个 PDF

```bash
cd .pdfs
curl -sL --max-time 90 -o <arxiv-id>.pdf https://arxiv.org/pdf/<arxiv-id>
```

如要给新加的 paper note 配 PDF,**用纯 arxiv id 命名**(如 `2603.11531.pdf`),不用易读名;**不要 commit**(已在 `.gitignore` 排除整个 `.pdfs/` 目录)。
