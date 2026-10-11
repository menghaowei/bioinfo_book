#!/usr/bin/env Rscript
# 第9章 R 实跑图（003–007），由第9章轮3实跑证据（C1/D2）生成：
#   003-pbmc-qc.png           质控小提琴（过滤前分布，展示阈值判断对象）
#   004-pbmc-umap.png         聚类 UMAP
#   005-pbmc-marker-dot.png   经典 marker 点图
#   006-ifnb-integration.png  ifnb 整合前后对比
#   007-visium-regions.png    Visium 小鼠脑区域基因空间图
# 数据与实跑日志：BioinfoBook_local_records/chapter09-revision-2026-10-11/evidence/（E-010）
# 环境：R 4.4.1；Seurat 5.1.0；运行：Rscript --no-init-file generate_r_plots.R

.libPaths("/Volumes/fast_SSD/R_lib_4.4")
suppressPackageStartupMessages({
  library(Seurat); library(ggplot2); library(patchwork)
})

EVID <- "/Users/meng/14.LLM_project/02.mhw_bioinfo_books/01.bioinfo_book_codex/BioinfoBook_local_records/chapter09-revision-2026-10-11/evidence/data"
OUT  <- file.path(Sys.getenv("PWD"), "../../../assets/09-single-cell-and-spatial-omics")
OUT  <- normalizePath(OUT, mustWork = FALSE)
dir.create(OUT, showWarnings = FALSE, recursive = TRUE)
set.seed(123)

# ---- 003 质控小提琴（过滤前）----
counts <- Read10X(file.path(EVID, "filtered_gene_bc_matrices/hg19"))
pbmc0 <- CreateSeuratObject(counts = counts, project = "pbmc3k",
                            min.cells = 3, min.features = 200)
pbmc0[["percent.mt"]] <- PercentageFeatureSet(pbmc0, pattern = "^MT-")
p <- VlnPlot(pbmc0, features = c("nFeature_RNA", "nCount_RNA", "percent.mt"),
             ncol = 3, pt.size = 0.05) &
  theme(axis.title.x = element_blank(), plot.title = element_text(size = 12))
ggsave(file.path(OUT, "003-pbmc-qc.png"), p, width = 11, height = 3.8, dpi = 150)

# ---- 004 UMAP / 005 点图（来自实跑 rds）----
pbmc <- readRDS(file.path(EVID, "outputs/pbmc3k_seurat.rds"))
ggsave(file.path(OUT, "004-pbmc-umap.png"),
       DimPlot(pbmc, reduction = "umap", label = TRUE, label.size = 5) +
         ggtitle(NULL) + theme(axis.title = element_text(size = 11)),
       width = 6.4, height = 5, dpi = 150)
canonical <- c("IL7R", "CCR7", "CD14", "LYZ", "MS4A1", "CD79A", "CD8A",
               "FCGR3A", "GNLY", "NKG7", "FCER1A", "PPBP")
canonical <- intersect(canonical, rownames(pbmc))
ggsave(file.path(OUT, "005-pbmc-marker-dot.png"),
       DotPlot(pbmc, features = canonical) + RotatedAxis() +
         theme(axis.text.x = element_text(size = 10), axis.text.y = element_text(size = 10)) +
         ggtitle(NULL),
       width = 9, height = 4.6, dpi = 150)

# ---- 006 ifnb 整合前后对比 ----
ifnb <- readRDS(file.path(EVID, "outputs/ifnb_integrated.rds"))
p1 <- DimPlot(ifnb, reduction = "umap.unintegrated", group.by = "stim") +
  ggtitle("整合前：按条件着色") + theme(legend.position = "bottom",
        plot.title = element_text(size = 12), axis.title = element_text(size = 10))
p2 <- DimPlot(ifnb, reduction = "umap.harmony", group.by = "seurat_annotations",
              label = TRUE, repel = TRUE, label.size = 3.5) +
  ggtitle("整合后：按细胞类型着色") + theme(legend.position = "bottom",
        plot.title = element_text(size = 12), axis.title = element_text(size = 10))
ggsave(file.path(OUT, "006-ifnb-integration.png"), p1 + p2,
       width = 12.4, height = 5.6, dpi = 150)

# ---- 007 Visium 区域基因 ----
brain <- readRDS(file.path(EVID, "outputs/visium_brain.rds"))
feats <- c("Hpca", "Plp1", "Rorb", "Cux2")
p <- SpatialPlot(brain, features = feats, ncol = 2, crop = TRUE) &
  theme(legend.position = "right", plot.title = element_text(size = 12))
ggsave(file.path(OUT, "007-visium-regions.png"), p, width = 9.6, height = 10, dpi = 120)

cat("done. 输出目录:", OUT, "\n")
for (f in list.files(OUT)) cat(" ", f, file.size(file.path(OUT, f)), "\n")
