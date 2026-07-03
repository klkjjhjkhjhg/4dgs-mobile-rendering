# Experiments

> 实验脚本目录。每个实验一个子目录,有 README 说明目的、输入、产物、可复现性。

## 期望的几个实验

- `exp-mask-coverage/` — temporal mask / spatial mask 的覆盖率与复用率 benchmark
- `exp-bitpack-quant/` — 32→16/8 bit 的 bitpack 精度 vs 性能 trade-off 验证
- `exp-on-tile-sort/` — on-tile sort vs host sort 在 Adreno 上的开销对比
- `exp-upscale-quality/` — FSR 1/2 / TAA-upsample 在 540p/720p/900p 内部渲染下的 PSNR / FPS

## 命名约定

`exp-<主题>/`

每个实验目录:
- `README.md` 实验目的 / 输入 / 输出 / 复现步骤
- `main.py`(或主入口)
- `results/` 产物(图片 / 表格 / 数值)
