#!/usr/bin/env Rscript
# 第5章三张演示图的真实 R 绘制（火山图/聚类热图/富集气泡图）。
# 数据：程序模拟的 RNA-seq 计数（负二项），统计量真实计算（中位数比值归一化、
# Wald 检验、BH 校正），绘图用 ggplot2/pheatmap——与正文 R 代码同一路线。
# 运行：Rscript --no-init-file --no-restore generate_r_plots.R <repo_root>
.libPaths("/Volumes/fast_SSD/R_lib_4.4")
suppressMessages({library(ggplot2); library(pheatmap); library(RColorBrewer)})

args <- commandArgs(trailingOnly = TRUE)
root <- if (length(args)) args[1] else "."
outdir <- file.path(root, "assets/06-rna-seq/svg")
dir.create(outdir, showWarnings = FALSE, recursive = TRUE)
set.seed(20261010)

## ── 1. 模拟计数：800 基因 × 6 样本（Ctrl×3 / KD×3，80 个 DE）──
n_g <- 800
base <- rgamma(n_g, shape = 1.2, scale = 900) + 25
eff <- rep(0, n_g)
de_idx <- sample(n_g, 80)
eff[de_idx] <- sample(c(-1, 1), 80, replace = TRUE) * runif(80, 0.8, 1.6)
sf <- c(1.00, 0.94, 1.06, 1.10, 0.90, 1.03)
samples <- c("Ctrl1", "Ctrl2", "Ctrl3", "KD1", "KD2", "KD3")
counts <- matrix(0, n_g, 6, dimnames = list(paste0("Gene", seq_len(n_g)), samples))
for (j in 1:6) {
  grp <- if (j <= 3) 0 else 1
  mu <- base * sf[j] * 2^(eff * grp)
  counts[, j] <- rnbinom(n_g, mu = mu, size = 1 / 0.15)
}

## ── 2. 真实统计：中位数比值尺寸因子 → log2 归一化 → Wald → BH ──
gm <- exp(rowMeans(log(counts + 1)))
sf2 <- apply(sweep(counts, 1, gm, "/"), 2, median)
nc <- sweep(counts, 2, sf2, "/")
lc <- log2(nc + 1)
lfc <- rowMeans(lc[, 4:6]) - rowMeans(lc[, 1:3])
se <- sqrt(apply(lc[, 1:3], 1, var) / 3 + apply(lc[, 4:6], 1, var) / 3 + 0.05)
stat <- lfc / se
pval <- 2 * pnorm(-abs(stat))
padj <- p.adjust(pval, method = "BH")

## ── 3. 火山图（ggplot2 真绘制；配色与本书主题一致）──
df <- data.frame(lfc = lfc, p = pval, padj = padj)
df$cls <- with(df, ifelse(padj < 0.05 & lfc > 1, "Up",
                   ifelse(padj < 0.05 & lfc < -1, "Down", "NS")))
p <- ggplot(df, aes(lfc, -log10(p), color = cls)) +
  geom_point(size = 1.4, alpha = 0.8) +
  geom_hline(yintercept = -log10(0.05), linetype = 2, color = "grey55") +
  geom_vline(xintercept = c(-1, 1), linetype = 2, color = "grey55") +
  scale_color_manual(values = c(Up = "#186254", Down = "#B45309", NS = "#C4CBD0"),
                     breaks = c("Up", "Down", "NS"), labels = c("Up (padj<0.05, log2FC>1)", "Down (padj<0.05, log2FC<-1)", "Not significant")) +
  labs(x = "log2 fold change (KD vs Ctrl)", y = "-log10(p)",
       title = "Volcano plot of 800 simulated genes") +
  coord_cartesian(ylim = c(0, 8)) +
  theme_classic(base_size = 12.5) +
  theme(legend.position = c(0.99, 0.98), legend.justification = c(1, 1),
        legend.background = element_rect(color = "grey80", fill = "white", linewidth = 0.4),
        legend.title = element_blank(), legend.text = element_text(size = 9),
        legend.key.size = unit(0.8, "lines"), plot.title = element_text(size = 12))
ggsave(file.path(outdir, "volcano-demo-r.svg"), p, width = 6.4, height = 4.8)

## ── 4. 聚类热图（pheatmap 真绘制：方差前 50 基因、行 z-score、列真实 hclust、红高蓝低）──
vars <- apply(lc, 1, var)
top <- order(vars, decreasing = TRUE)[1:50]
z <- t(scale(t(lc[top, ])))
ann <- data.frame(Group = factor(c("Ctrl", "Ctrl", "Ctrl", "KD", "KD", "KD"), levels = c("Ctrl", "KD")),
                  row.names = samples)
ann_colors <- list(Group = c(Ctrl = "#186254", KD = "#B45309"))
col_pal <- colorRampPalette(rev(brewer.pal(11, "RdBu")))(101)  # RdBu 反序：红=高，白=中，蓝=低
svg(file.path(outdir, "heatmap-demo-r.svg"), width = 7.2, height = 6.0, onefile = TRUE)
pheatmap(z, color = col_pal, border_color = NA,
         cluster_rows = FALSE, cluster_cols = TRUE, cutree_cols = 2,
         annotation_col = ann, annotation_colors = ann_colors,
         show_rownames = FALSE, fontsize = 11,
         main = "Top-50 variable genes (row z-score)")
dev.off()

## ── 5. 富集气泡图（ggplot2 真绘制，风格对齐 clusterProfiler dotplot）──
terms <- data.frame(
  ID = c("GO:0007049", "GO:0006260", "GO:0007059", "GO:0006281", "GO:0097194",
         "GO:0008380", "GO:0006457", "GO:0007165"),
  Description = c("cell cycle", "DNA replication", "chromosome segregation",
                  "DNA repair", "programmed cell death", "RNA splicing",
                  "protein folding", "signal transduction"),
  Count = c(68, 54, 41, 33, 21, 18, 12, 8),
  GeneRatio = c(0.31, 0.26, 0.22, 0.18, 0.14, 0.11, 0.09, 0.06),
  p.adjust = c(2e-6, 8e-6, 4e-5, 2e-4, 1e-3, 4e-3, 2e-2, 6e-2))
terms$Description <- factor(terms$Description, levels = rev(terms$Description))
pb <- ggplot(terms, aes(GeneRatio, Description)) +
  geom_point(aes(size = Count, color = p.adjust)) +
  scale_size_continuous(range = c(3, 9), name = "Count") +
  scale_color_gradientn(colors = c("#0F4C3F", "#5FA292", "#D9E8E2"),
                        name = "p.adjust", trans = "log10") +
  labs(x = "GeneRatio", y = NULL,
       title = "Dotplot of simulated enrichment results") +
  theme_classic(base_size = 12.5) +
  theme(plot.title = element_text(size = 12),
        legend.box = "vertical", legend.key.size = unit(0.9, "lines"))
ggsave(file.path(outdir, "bubble-demo-r.svg"), pb, width = 7.0, height = 4.8)

cat("written:", list.files(outdir, pattern = "-r\\.svg$"), "\n")
