# 第 11 章图组生成脚本：GTEx v8 子集上的描述统计 / t 检验 / 回归 / PCA / t-SNE / UMAP
# 运行方式：Rscript gtex_dimred.R <数据目录> <输出目录>
# 数据下载（GTEx v8 开放数据，2026-10 核实直链）：
#   curl -O https://storage.googleapis.com/adult-gtex/bulk-gex/v8/rna-seq/GTEx_Analysis_2017-06-05_v8_RNASeQCv1.1.9_gene_tpm.gct.gz
#   curl -O https://storage.googleapis.com/adult-gtex/annotations/v8/metadata-files/GTEx_Analysis_v8_Annotations_SampleAttributesDS.txt
# 依赖（CRAN）：data.table, R.utils, ggplot2, Rtsne, uwot
# 随机过程：所有 t-SNE / UMAP 调用前 set.seed()；本脚本实测同种子两次运行结果一致

args <- commandArgs(trailingOnly = TRUE)
data_dir <- if (length(args) >= 1) args[1] else "./data"
out_dir  <- if (length(args) >= 2) args[2] else "./output"
dir.create(out_dir, showWarnings = FALSE, recursive = TRUE)

suppressPackageStartupMessages({
  library(data.table)
  library(ggplot2)
  library(Rtsne)
  library(uwot)
  library(showtext)
})
# 用 FreeType 直接渲染中文字体，避免不同平台图形设备的字体解析差异
sysfonts::font_add("pingfang", regular = "/System/Library/Fonts/PingFang.ttc")
showtext_opts(dpi = 300)
showtext_auto()

SEED      <- 20261011
NGENE_HVG <- 3000
PERPLEX   <- c(5, 15, 30)          # n=100 时 Rtsne 要求 perplexity < (n-1)/3 ≈ 33
TISSUES10 <- c("Brain", "Heart", "Lung", "Liver", "Pancreas",
               "Stomach", "Colon", "Blood", "Muscle", "Kidney")
PAL10     <- RColorBrewer::brewer.pal(12, "Paired")[c(1:10)]
FAM       <- "pingfang"                                # showtext 注册的中文字体

save_png <- function(p, file, w = 2600, h = 1500) {
  ggsave(file.path(out_dir, file), p, width = w / 300, height = h / 300,
         dpi = 300, bg = "white")
}

## ---- 1. 读取数据（56,200 基因 × 17,382 样本） ----
tpm   <- fread(file.path(data_dir, "GTEx_v8_gene_tpm.gct.gz"),
               skip = 2, header = TRUE)
annot <- fread(file.path(data_dir,
           "GTEx_v8_Annotations_SampleAttributesDS.txt"),
           select = c("SAMPID", "SMTS"))

## ---- 2. 教学子集：10 组织 × 各 10 个样本 ----
rna <- annot[SAMPID %in% names(tpm)]                 # 只保留 RNA-seq 样本
setorder(rna, SAMPID)                                # 固定取样顺序
samples <- rna[SMTS %in% TISSUES10, head(.SD, 10), by = SMTS]
samples[, tissue := factor(SMTS, levels = TISSUES10)]
cols  <- samples$SAMPID
mat   <- as.matrix(tpm[, ..cols])
rownames(mat) <- tpm$Name
storage.mode(mat) <- "double"
tissue <- samples$tissue
donors <- unique(sub("^(GTEX-[A-Z0-9]+)-.*", "\\1", samples$SAMPID))

## ---- 3. 预处理：log2(TPM+1) 与高变基因 ----
log_tpm  <- log2(mat + 1)
gene_var <- apply(log_tpm, 1, var)
top_genes <- names(sort(gene_var, decreasing = TRUE))[seq_len(NGENE_HVG)]
x <- t(log_tpm[top_genes, ])                         # 样本 × 基因

## ---- 4. 描述统计示例：ALB 在肝组织样本 ----
alb_id  <- tpm$Name[tpm$Description == "ALB"][1]
alb_all <- log_tpm[alb_id, ]
alb_liver <- as.numeric(alb_all[tissue == "Liver"])
mean_liv <- mean(alb_liver); sd_liv <- sd(alb_liver)
se_liv <- sd_liv / sqrt(length(alb_liver))
ci_liv <- mean_liv + c(-1, 1) * qt(0.975, length(alb_liver) - 1) * se_liv

## ---- 5. t 检验与线性回归示例：ALB，肝 vs 胰 ----
d2 <- data.frame(tissue = droplevels(tissue[tissue %in% c("Liver", "Pancreas")]),
                 alb = as.numeric(alb_all[tissue %in% c("Liver", "Pancreas")]))
tt   <- t.test(alb ~ tissue, data = d2)              # Welch（默认）
fit  <- lm(alb ~ tissue, data = d2)

## ---- 6. PCA ----
pca  <- prcomp(x, center = TRUE, scale. = FALSE)
pve  <- pca$sdev^2 / sum(pca$sdev^2)

## ---- 7. t-SNE：perplexity 与种子 ----
run_tsne <- function(perp, seed) {
  set.seed(seed)
  Rtsne(x, dims = 2, perplexity = perp, pca = TRUE,
        check_duplicates = FALSE, max_iter = 1000)$Y
}
tsne_perp <- lapply(PERPLEX, run_tsne, seed = SEED)
tsne_seed <- list(run_tsne(30, SEED), run_tsne(30, 42))
# 可复现性实测：同种子重复运行
repro_tsne <- identical(run_tsne(15, SEED), run_tsne(15, SEED))

## ---- 8. UMAP：n_neighbors 与 min_dist ----
run_umap <- function(nn, md) {
  umap(x, n_neighbors = nn, min_dist = md, metric = "euclidean",
       seed = SEED, n_threads = 1)                   # 单线程保证可复现
}
umap_nn <- lapply(c(5, 15, 50), run_umap, md = 0.1)
umap_md <- lapply(c(0, 0.1, 1),       run_umap, nn = 15)
repro_umap <- identical(run_umap(15, 0.1), run_umap(15, 0.1))

## ---- 9. 图：ALB 两组织比较（11.4 示例） ----
df_alb <- data.frame(tissue = d2$tissue, alb = d2$alb)
p_alb <- ggplot(df_alb, aes(tissue, alb, fill = tissue)) +
  geom_point(shape = 21, size = 4.4, color = "grey20",
             position = position_jitter(width = 0.08, height = 0, seed = 1)) +
  stat_summary(fun = mean, geom = "crossbar", width = 0.45,
               color = "#b45309", size = 0.9) +
  scale_fill_manual(values = c("#1f9e89", "#b5838d"), guide = "none") +
  labs(x = NULL, y = "log2(TPM + 1)",
       title = "ALB 基因在 GTEx 肝与胰腺样本中的表达") +
  theme_classic(base_size = 17) +
  theme(text = element_text(family = FAM),
        plot.title = element_text(size = 18))
save_png(p_alb, "fig-11-03-alb-ttest.png", 1800, 1600)

## ---- 10. 图：模拟泊松 vs 负二项计数（11.3 示例） ----
set.seed(SEED)
pois  <- rpois(4000, lambda = 20)
nbin <- rnbinom(4000, mu = 20, size = 8)             # 方差 = 20 + 20^2/8 = 70
df_sim <- rbind(data.frame(x = pois,  model = "泊松（均值=方差=20）"),
                data.frame(x = nbin, model = "负二项（均值=20，方差=70）"))
p_sim <- ggplot(df_sim, aes(x)) +
  geom_histogram(bins = 45, fill = "#7fc8bd", color = "white") +
  geom_vline(xintercept = 20, color = "#b45309", linewidth = 0.9,
             linetype = "dashed") +
  facet_wrap(~model, ncol = 1, scales = "free_y") +
  labs(x = "一个基因在许多样本中的计数", y = "样本数",
       title = "同样的均值，不同的离散程度（模拟数据）",
       subtitle = "虚线为均值 20") +
  theme_classic(base_size = 17) +
  theme(text = element_text(family = FAM),
        plot.title = element_text(size = 18))
save_png(p_sim, "fig-11-02-count-dist.png", 1800, 2000)

## ---- 11. 图：GTEx PCA（散点 + 方差解释） ----
df_pca <- data.frame(PC1 = pca$x[, 1], PC2 = pca$x[, 2], tissue = tissue)
p_scatter <- ggplot(df_pca, aes(PC1, PC2, color = tissue)) +
  geom_point(size = 4.2, alpha = 0.95) +
  scale_color_manual(values = setNames(PAL10, TISSUES10), name = NULL) +
  labs(x = sprintf("PC1（%.1f%%）", 100 * pve[1]),
       y = sprintf("PC2（%.1f%%）", 100 * pve[2]),
       title = "GTEx 十组织样本的 PCA（top 3000 高变基因）") +
  theme_classic(base_size = 17) +
  theme(text = element_text(family = FAM),
        plot.title = element_text(size = 18),
        legend.position = "right", legend.key.size = unit(14, "pt"))
df_scree <- data.frame(PC = factor(paste0("PC", 1:10), paste0("PC", 1:10)),
                       pve = 100 * pve[1:10])
p_scree <- ggplot(df_scree, aes(PC, pve)) +
  geom_col(fill = "#186254") +
  labs(x = NULL, y = "方差解释比例（%）", title = "前 10 个主成分") +
  theme_classic(base_size = 17) +
  theme(text = element_text(family = FAM),
        plot.title = element_text(size = 18))
save_png(p_scatter, "fig-11-06a-gtex-pca.png", 2600, 1700)
save_png(p_scree,   "fig-11-06b-gtex-scree.png", 1800, 1400)

## ---- 12. 图：t-SNE perplexity 三联与种子对比 ----
mk_tsne_df <- function(y) data.frame(tSNE1 = y[, 1], tSNE2 = y[, 2], tissue = tissue)
p_perp <- lapply(seq_along(PERPLEX), function(i) {
  ggplot(mk_tsne_df(tsne_perp[[i]]), aes(tSNE1, tSNE2, color = tissue)) +
    geom_point(size = 3.4, alpha = 0.95) +
    scale_color_manual(values = setNames(PAL10, TISSUES10), guide = "none") +
    labs(title = sprintf("perplexity = %d", PERPLEX[i])) +
    theme_classic(base_size = 15) +
    theme(text = element_text(family = FAM),
        plot.title = element_text(size = 16))
})
save_png(patchwork::wrap_plots(p_perp, ncol = 3), "fig-11-07a-gtex-tsne-perp.png",
         3000, 1150)
p_seed <- lapply(c(1, 2), function(i) {
  ggplot(mk_tsne_df(tsne_seed[[i]]), aes(tSNE1, tSNE2, color = tissue)) +
    geom_point(size = 3.4, alpha = 0.95) +
    scale_color_manual(values = setNames(PAL10, TISSUES10), guide = "none") +
    labs(title = sprintf("perplexity = 30，随机种子 %s",
                         c("20261011", "42")[i])) +
    theme_classic(base_size = 15) +
    theme(text = element_text(family = FAM),
        plot.title = element_text(size = 16))
})
save_png(patchwork::wrap_plots(p_seed, ncol = 2), "fig-11-07b-gtex-tsne-seed.png",
         2200, 1150)

## ---- 13. 图：UMAP 参数对比 ----
mk_umap_df <- function(y) data.frame(UMAP1 = y[, 1], UMAP2 = y[, 2], tissue = tissue)
nn_vals <- c(5, 15, 50)
p_nn <- lapply(seq_along(nn_vals), function(i) {
  ggplot(mk_umap_df(umap_nn[[i]]), aes(UMAP1, UMAP2, color = tissue)) +
    geom_point(size = 3.4, alpha = 0.95) +
    scale_color_manual(values = setNames(PAL10, TISSUES10), guide = "none") +
    labs(title = sprintf("n_neighbors = %d", nn_vals[i])) +
    theme_classic(base_size = 15) +
    theme(text = element_text(family = FAM),
        plot.title = element_text(size = 16))
})
save_png(patchwork::wrap_plots(p_nn, ncol = 3), "fig-11-08a-gtex-umap-nn.png",
         3000, 1150)
md_vals <- c(0, 0.1, 1)
p_md <- lapply(seq_along(md_vals), function(i) {
  ggplot(mk_umap_df(umap_md[[i]]), aes(UMAP1, UMAP2, color = tissue)) +
    geom_point(size = 3.4, alpha = 0.95) +
    scale_color_manual(values = setNames(PAL10, TISSUES10), guide = "none") +
    labs(title = sprintf("min_dist = %s", format(md_vals[i]))) +
    theme_classic(base_size = 15) +
    theme(text = element_text(family = FAM),
        plot.title = element_text(size = 16))
})
save_png(patchwork::wrap_plots(p_md, ncol = 3), "fig-11-08b-gtex-umap-md.png",
         3000, 1150)

## ---- 14. 汇总输出（正文数值与证据记录） ----
sink(file.path(out_dir, "summary.txt"))
cat("=== 数据 ===\n")
cat(sprintf("TPM 矩阵：%d 基因 × %d 样本；注释表 RNA-seq 样本 %d、SMTS 组织 %d 类\n",
            nrow(tpm), ncol(tpm) - 2, nrow(rna), uniqueN(rna$SMTS)))
cat(sprintf("子集：%d 组织 × %d 样本 = %d（来自 %d 名捐赠者）\n",
            uniqueN(samples$SMTS), 10, nrow(samples), length(donors)))
cat(sprintf("ALB ID: %s\n", alb_id))
cat("\n=== 描述统计（ALB，肝，log2 TPM+1，n=%d） ===\n", length(alb_liver))
cat(sprintf("均值 %.3f，中位数 %.3f，SD %.3f，SE %.3f，95%%CI [%.3f, %.3f]\n",
            mean_liv, median(alb_liver), sd_liv, se_liv, ci_liv[1], ci_liv[2]))
cat("\n=== t 检验（ALB，Liver vs Pancreas） ===\n")
print(tt)
cat("\n=== lm(alb ~ tissue)：Liver 是首个水平（截距） ===\n")
print(round(coef(fit), 3))
cat(sprintf("组均值：Liver %.3f，Pancreas %.3f，差 %.3f\n",
            mean(d2$alb[d2$tissue == "Liver"]),
            mean(d2$alb[d2$tissue == "Pancreas"]),
            mean(d2$alb[d2$tissue == "Pancreas"]) - mean(d2$alb[d2$tissue == "Liver"])))
cat("\n=== PCA ===\n")
cat(sprintf("PC1–PC5 方差解释：%.1f%% %.1f%% %.1f%% %.1f%% %.1f%%\n",
            100 * pve[1], 100 * pve[2], 100 * pve[3], 100 * pve[4], 100 * pve[5]))
cat("各组织 PC1/PC2 均值：\n")
agg <- aggregate(cbind(PC1, PC2) ~ tissue, data = df_pca, FUN = mean)
agg$PC1 <- round(agg$PC1, 1); agg$PC2 <- round(agg$PC2, 1)
print(agg)
cat("\n=== BH 演示 ===\n")
p5 <- c(0.001, 0.008, 0.013, 0.18, 0.35)
print(rbind(p = p5, padj = p.adjust(p5, method = "BH")))
cat("\n=== 可复现性 ===\n")
cat(sprintf("t-SNE 同种子两次运行完全一致：%s\n", repro_tsne))
cat(sprintf("UMAP（单线程）同种子两次运行完全一致：%s\n", repro_umap))
cat("\n=== sessionInfo ===\n")
print(sessionInfo())
sink()

cat("done：图与 summary.txt 已输出到", out_dir, "\n")
