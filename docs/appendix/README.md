# Appendix — 调研补充材料

> subagent 调研过程中,以下三种材料沉淀在此:
> - 每篇关键论文的**精读笔记**( `paper-notes/` )
> - **采集 SOP 草案**( `collection-sop.md` )
> - **Vulkan 1.3 实现细节笔记**( `vulkan-impl-notes.md` )

## paper-notes/ 命名约定

每篇论文一个 markdown,文件名 = `年份-作者-方法名.md`,例:
```
2024-wu-4dgs.md
2025-xxx-4dgs-1k-lite.md
2023-yang-dynamic-3dgs.md
```

每篇笔记必含:
- 链接(biorxiv / arxiv / 仓库)
- 一句话问题
- 方法核心(3~5 条要点)
- 关键数字(精度 / FPS / 资源体积)
- 与本调研主线的关系(借鉴 / 反例 / 跳过)
- 关键代码引用文件路径(如果开源)
