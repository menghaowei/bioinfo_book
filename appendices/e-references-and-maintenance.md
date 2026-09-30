# 参考文献与维护记录 {#sec-maintenance}

## 本次整理

2026-09-30：按已确认的大纲建立三篇、十章、71 个小节，迁移原稿正文与现有 1—25 题，统一章节文件和素材目录，并建立 Quarto HTML 工程。

原稿正文、题库的其他版本和旧汇总稿保留在工程的 `archive/` 中。逐小节映射见 `editorial/section-mapping.tsv`，素材映射见 `editorial/asset-mapping.tsv`，精确的更正前后文本见 `editorial/corrections.json`。归档用于核对历史内容，后续写作应修改 `manuscript/` 和 `appendices/`。

本次修正了读长与平台的过时绝对表述、SBS 化学的部分错误说明、FPKM/RPKM 单位、SAM FLAG/MAPQ/CIGAR、杂合子似然、后验概率比例关系，以及 HaplotypeCaller 与联合分型的混淆。其余历史命令、图中说明、算法数值例题和文献来源仍需继续校订，不将本轮整理视作全书科学内容已全部验收。

## 本轮校订与工程依据

以下为本轮读取的官方说明，核对日期为 2026-09-30。历史原稿中的其他链接与署名随正文保留。

| 资料 | 用途 |
|---|---|
| [Illumina SBS](https://www.illumina.com/science/technology/next-generation-sequencing/sequencing-technology.html) | 边合成边测序与可逆终止 |
| [Illumina patterned flow cell](https://www.illumina.com/science/technology/next-generation-sequencing/sequencing-technology/patterned-flow-cells.html) | 区分平台结构 |
| [SAM/BAM 规范](https://samtools.github.io/hts-specs/SAMv1.pdf) | 字段、标志和坐标 |
| [DESeq2 官方教程](https://bioconductor.org/packages/release/bioc/vignettes/DESeq2/inst/doc/DESeq2.html) | counts 与归一化输入 |
| [GATK HaplotypeCaller](https://gatk.broadinstitute.org/hc/en-us/articles/21905025322523-HaplotypeCaller) | 局部组装、似然与 gVCF 工作流 |
| [Oxford Nanopore 技术说明](https://nanoporetech.com/platform/technology) | 纳米孔电流信号 |
| [PacBio RNA 测序](https://www.pacb.com/products-and-services/applications/rna-sequencing/) | 全长 cDNA 与 Iso-Seq |
| [Quarto book structure](https://quarto.org/docs/books/book-structure.html) | 章节、分篇和附录 |
| [Quarto GitHub Pages](https://quarto.org/docs/publishing/github-pages.html) | HTML 构建与发布 |

## 待完善的引用与素材

原稿 RNA-seq 部分有文献上标 1—13，但未提供完整的逐条参考文献表。本版保留编号并转换为可点击脚注，脚注明确标为“完整书目信息待完善”，不推测文献出处。

Windows/OpenSSH 部分两张石墨外链截图当前无法下载，保留图位并标为“原图待完善”。其他已引用图片均已整理到本地素材目录。

## 后续 PDF

PDF 排版另行实施，基础采用已确认的 ElegantBook 中文教材风格。本轮只配置 HTML 输出。
