# 参考资料与素材说明 {#sec-maintenance}

## 阅读说明 {#本次整理}

本书涉及测序原理、数据格式、统计推断和分析工具。阅读时应结合对应工具的官方说明，核对适用版本、输入要求和分析假设。

历史命令、图中说明、算法数值例题和文献来源仍需继续校订，书中的分析流程尚未逐项在统一环境和数据上实际运行验证。网页可正常阅读不代表科学内容已全部验收。

## 参考资料 {#本轮校订与工程依据}

以下官方资料可用于进一步阅读与核对。正文中的其他参考链接与署名随对应内容保留。

| 资料 | 用途 |
|---|---|
| [Illumina SBS](https://www.illumina.com/science/technology/next-generation-sequencing/sequencing-technology.html) | 边合成边测序与可逆终止 |
| [Illumina patterned flow cell](https://www.illumina.com/science/technology/next-generation-sequencing/sequencing-technology/patterned-flow-cells.html) | 区分平台结构 |
| [SAM/BAM 规范](https://samtools.github.io/hts-specs/SAMv1.pdf) | 字段、标志和坐标 |
| [DESeq2 官方教程](https://bioconductor.org/packages/release/bioc/vignettes/DESeq2/inst/doc/DESeq2.html) | counts 与归一化输入 |
| [GATK HaplotypeCaller](https://gatk.broadinstitute.org/hc/en-us/articles/21905025322523-HaplotypeCaller) | 局部组装、似然与 gVCF 工作流 |
| [Oxford Nanopore 技术说明](https://nanoporetech.com/platform/technology) | 纳米孔电流信号 |
| [PacBio RNA 测序](https://www.pacb.com/products-and-services/applications/rna-sequencing/) | 全长 cDNA 与 Iso-Seq |

: 表题待补 {#tbl-a-references-and-materials-01}

## 待完善的引用与素材

原稿 RNA-seq 及已移入单细胞与空间组学章的内容共有文献编号 1—13，但未提供完整的逐条参考文献表。本版保留编号并转换为可点击脚注，脚注明确标为“完整书目信息待完善”，不推测文献出处。

Windows/OpenSSH 部分两张石墨外链截图当前无法下载，保留图位并标为“原图待完善”。其他已引用图片均已整理到本地素材目录。

## 阅读形式 {#后续-pdf}

本书当前提供在线 HTML 阅读。使用范围见[版权与使用条款](https://book.bioinfo.info/license.html)。
