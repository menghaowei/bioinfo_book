#!/usr/bin/env Rscript
# Run in a working directory; the two small inputs are downloaded if absent.
# Packages: DESeq2, pheatmap, svglite; see data/README.md for input provenance.
suppressPackageStartupMessages({
  library(DESeq2)
  library(pheatmap)
  library(svglite)
})

data_dir <- "heatmap-data"
out_dir <- "."
dir.create(data_dir, recursive = TRUE, showWarnings = FALSE)
count_file <- "GSE56010_raw_counts_GRCh38.p13_NCBI.tsv.gz"
symbol_file <- "GSE56010_gene_symbols.tsv.gz"
count_url <- paste0("https://www.ncbi.nlm.nih.gov/geo/download/?format=file&",
                    "type=rnaseq_counts&acc=GSE56010&file=", count_file)
symbol_url <- paste0("https://book.bioinfo.info/assets/06-rna-seq/data/", symbol_file)
if (!file.exists(file.path(data_dir, count_file)))
  download.file(count_url, file.path(data_dir, count_file), mode = "wb")
if (!file.exists(file.path(data_dir, symbol_file)))
  download.file(symbol_url, file.path(data_dir, symbol_file), mode = "wb")
cts <- read.delim(gzfile(file.path(data_dir,
  "GSE56010_raw_counts_GRCh38.p13_NCBI.tsv.gz")), row.names = 1,
  check.names = FALSE)
symbols <- read.delim(gzfile(file.path(data_dir,
  "GSE56010_gene_symbols.tsv.gz")), colClasses = "character")

samples <- data.frame(
  row.names = c("GSM1502498", "GSM1502499", "GSM1502502", "GSM1502503"),
  condition = factor(c("Control", "Control", "METTL3_KD", "METTL3_KD"),
                     levels = c("Control", "METTL3_KD"))
)
cts <- as.matrix(cts[, rownames(samples)])
stopifnot(identical(colnames(cts), rownames(samples)),
          all(is.finite(cts)), all(cts >= 0), all(cts == round(cts)))

# Keep genes with at least 10 counts in at least two samples.
dds <- DESeqDataSetFromMatrix(cts, samples, design = ~ condition)
dds <- dds[rowSums(counts(dds) >= 10) >= 2, ]
dds <- DESeq(dds)
res <- results(dds, contrast = c("condition", "METTL3_KD", "Control"),
               alpha = 0.05)

# The gene selection uses the group labels; this is a display of DE patterns.
de <- which(!is.na(res$padj) & res$padj < 0.05 & abs(res$log2FoldChange) > 1)
stopifnot(length(de) >= 30)
de <- de[order(res$padj[de], rownames(res)[de])]
gene_ids <- rownames(res)[de[seq_len(30)]]

# The statistical test uses counts; only the visualization uses VST and Z scores.
vsd <- vst(dds, blind = FALSE)
mat <- assay(vsd)[gene_ids, , drop = FALSE]
z <- t(scale(t(mat)))
stopifnot(all(is.finite(z)), max(abs(rowMeans(z))) < 1e-10)
gene_names <- symbols$Symbol[match(gene_ids, symbols$GeneID)]
missing <- is.na(gene_names) | gene_names == ""
gene_names[missing] <- paste0("GeneID:", gene_ids[missing])
gene_names <- make.unique(gene_names)
annotation <- data.frame(Condition = samples$condition,
                         row.names = rownames(samples))

# Euclidean distance and complete linkage are specified for both dendrograms.
row_tree <- hclust(dist(z), method = "complete")
col_tree <- hclust(dist(t(z)), method = "complete")
palette <- colorRampPalette(c("#2166AC", "#FFFFFF", "#B2182B"))(101)
svglite(file.path(out_dir, "heatmap-gse56010.svg"), width = 7.4, height = 8.1)
hm <- pheatmap(z, color = palette, breaks = seq(-2, 2, length.out = 102),
  cluster_rows = row_tree, cluster_cols = col_tree,
  labels_row = gene_names, annotation_col = annotation,
  annotation_colors = list(Condition = c(Control = "#186254", METTL3_KD = "#B45309")),
  border_color = NA, fontsize = 11, fontsize_row = 10, fontsize_col = 10,
  angle_col = 45, treeheight_row = 65, treeheight_col = 55,
  main = "METTL3 knockdown: 30 DE genes\nVST expression, row Z score")
dev.off()
# Add a short text alternative without changing the plotted values.
svg_file <- file.path(out_dir, "heatmap-gse56010.svg")
svg_text <- paste(readLines(svg_file), collapse = "\n")
svg_text <- sub("(<svg[^>]*>)", paste0("\\1",
  "<title>METTL3 knockdown: 30 differentially expressed genes</title>",
  "<desc>Four GSE56010 samples; gene and sample dendrograms use Euclidean ",
  "distance with complete linkage on row-standardized VST expression. ",
  "Red is above and blue below each gene's mean.</desc>"), svg_text, perl = TRUE)
writeLines(svg_text, svg_file)

# Save the exact values and tree order used in the figure.
write.table(data.frame(GeneID = gene_ids, Symbol = gene_names,
  as.data.frame(res[gene_ids, ]), z, check.names = FALSE),
  file.path(data_dir, "GSE56010_heatmap_values.tsv"),
  sep = "\t", row.names = FALSE, quote = FALSE)
writeLines(c(paste("Genes after filtering:", nrow(dds)),
  paste("DE genes (padj < 0.05, abs(log2FC) > 1):", length(de)),
  paste("Column order:", paste(colnames(z)[col_tree$order], collapse = ", ")),
  paste("Row order:", paste(gene_names[row_tree$order], collapse = ", ")),
  capture.output(sessionInfo())), file.path(data_dir, "GSE56010_heatmap_session.txt"))
