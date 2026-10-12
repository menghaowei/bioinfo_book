# 图 5.10：GSE56010 真实 RNA-seq 数据

- `GSE56010_raw_counts_GRCh38.p13_NCBI.tsv.gz`：NCBI 官方重算 counts 原文件，GRCh38.p13，39,376 个 GeneID × 8 个 GSM；2026-10-12 完整下载。图中仅选 GSM1502498/99（对照）与 GSM1502502/03（METTL3 敲降）。本文件不是正文旧自建 featureCounts 文件的副本。
- [原始文件下载](https://www.ncbi.nlm.nih.gov/geo/download/?format=file&type=rnaseq_counts&acc=GSE56010&file=GSE56010_raw_counts_GRCh38.p13_NCBI.tsv.gz)；[NCBI 处理说明](https://www.ncbi.nlm.nih.gov/geo/info/rnaseqcounts.html)。
- `GSE56010_gene_symbols.tsv.gz`：2026-10-12 从 [NCBI 人类 gene_info](https://ftp.ncbi.nlm.nih.gov/gene/DATA/GENE_INFO/Mammalia/Homo_sapiens.gene_info.gz) 按原表 GeneID 提取 GeneID、Symbol 两列，匹配 37,663 个 ID。未匹配 ID 在脚本中保留原编号，图中所选 30 个 ID 均匹配。符号只作标签，统计始终按唯一 GeneID 计算。
- `GSE56010_heatmap_values.tsv`：图中 30 个基因的差异统计量、基因符号和四个 GSM 的行 Z 分数；p 值为 0 表示浮点计算下溢，不是严格等于零的概率。

生成脚本：仓库中的 `scripts/figures/ch05/heatmap_gse56010.R`。在任一工作目录运行脚本，输入保存在 `heatmap-data/`，图为 `heatmap-gse56010.svg`。同名输入存在时不再下载，可将本目录两份 gzip 文件复制到 `heatmap-data/` 离线重现。计算及绘图代码与正文一致。验证环境为 R 4.4.1、DESeq2 1.44.0、pheatmap 1.0.12、svglite 2.2.2。

筛选：至少两个样本 counts ≥ 10；DESeq2 `~ condition`，敲降相对对照；padj < 0.05 且 |log2FC| > 1，再按 padj/GeneID 排序取前 30；VST（blind=FALSE）后逐行 Z 分数，欧氏距离＋完全连接法，行列均聚类。分组参与了基因选择，聚类不是独立的质量检验证据。
