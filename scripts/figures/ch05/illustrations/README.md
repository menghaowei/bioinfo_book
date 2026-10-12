# 第 5 章 RNA 概念插图

图 5.1 与图 5.2 使用 OpenAI 内置 `image_gen` 生成无文字的生物插画，再用 `@oai/artifact-tool` 2.8.71 编排准确的文字、箭头和丰度图。生成与修图提示完整保存于 `prompts.json`，图的概念来源也保存在 PPT 备注与章节脚注中。

## 文件与可编辑范围

正式素材位于 `assets/06-rna-seq/illustrations/`：

- `rna-roles-art.png`、`cell-types-art.png`：生物插画底图，可在 PPT 中整体移动或替换。
- `rna-concepts-editable.pptx`：两页原稿；中文标签、箭头与引线可编辑，第二页的三组丰度图为原生图表，附嵌入数据工作簿。
- `rna-roles.png`、`cell-transcriptomes.png`：最终 PPT 重新导入后导出的 2400 × 2520 PNG，供书稿使用。

插画内部的细胞和分子细节为位图，不能逐个作为矢量对象编辑。采用 Hiragino Sans GB 字体；在其他系统编辑时需安装该字体或统一替换为可用的中文无衬线字体并检查版面。

## 重新生成排版

在可解析 `@oai/artifact-tool` 的 Node 环境中，从正式工程根目录运行：

```bash
node scripts/figures/ch05/illustrations/build_rna_concepts.mjs /path/to/build-directory
```

脚本读取已有底图，输出候选 PPT、两张预览及排版记录。随后执行 Presentations 技能的正式检查与图表工作簿封装，再重新导入最终 PPT 逐页导出、核对文字和箭头。网页构建只使用已完成的 PNG，不调用图片生成或执行此脚本。

## 数值与读图约定

图 5.2 按 RNA A、B、C、D 排列，神经、肌肉、上皮分别为 `[3,5,1,1]`、`[3,1,5,1]`、`[3,1,1,5]`；三个图表使用相同数值范围 0–5.5。横向条形图的数据记录反序写入，使视觉顺序从上到下为 A–D。A–D 与数值均为教学示意，不对应真实基因或实测丰度。

图 5.1 以转录、剪接、输出和翻译为主线；下方调控 RNA 是并列的代表形态，不是主线的必经步骤。所有分子与细胞形态均不按实际尺度绘制。
