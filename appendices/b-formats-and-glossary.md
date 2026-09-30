# 文件格式、坐标与术语速查 {#sec-format-reference}

本附录作为速查入口，详细讲解保留在正文和题库中。

| 需要查找的内容 | 现有讲解 | 后续整理 |
|---|---|---|
| FASTA、FASTQ 与 Phred 质量分数 | [基础问题 1—5](a-questions-01-05.md)；[第 3 章](../manuscript/03-sequencing-and-data-formats.md#sec-03-04) | 统一示例与速查表待完善 |
| SAM/BAM、FLAG、CIGAR、MAPQ | [第 4 章](../manuscript/04-quality-control-and-alignment.md#sec-04-06)；[基础问题 16—20](a-questions-16-20.md) | 增补 CRAM 与过滤练习待完善 |
| GTF/GFF、基因与转录本 | [第 3 章](../manuscript/03-sequencing-and-data-formats.md#sec-03-05)；[基础问题 21—25](a-questions-21-25.md) | 注释版本配套关系待完善 |
| BED、bigWig、VCF | [第 3 章](../manuscript/03-sequencing-and-data-formats.md#sec-03-06)；[第 8 章](../manuscript/08-wgs-and-wes.md#sec-08-06) | 待完善 |
| read、fragment、library、sample、run | 第 1—4 章 | 统一术语表待完善 |

## 坐标的起点与区间边界

把一种文件里的区间拿到另一种工具中使用之前，要同时核对参考版本、染色体名称、坐标起点和右边界是否包含在区间内。SAM 文本中的 POS 从 1 开始计数；BED 通常使用从 0 开始、右端不包含的区间。相同的数字不一定表示同一段序列。

系统示例、转换练习和容易混淆的边界情况待完善。规范来源：[SAM/BAM 格式规范](https://samtools.github.io/hts-specs/SAMv1.pdf)。
