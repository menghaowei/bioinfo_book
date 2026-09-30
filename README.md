# BioinfoBook

第一版 HTML 已于 2026-09-30 发布，并完成线上电脑端验收。[成功的 Actions 运行](https://github.com/menghaowei/bioinfo_book/actions/runs/36689316643)；完整发布记录与本机写作环境见 [HANDOFF.md](HANDOFF.md)。

**以高通量数据分析为基础的生物信息学入门**。三篇、十章、71 个小节；保留原稿讲解与现有 1—25 道基础题。

- 在线阅读：<https://menghaowei.github.io/bioinfo_book/>
- 写作入口：`manuscript/*.md` 和 `appendices/*.md`
- 完整网页：`docs/`（包含图片、脚本、搜索索引及本地 MathJax）
- 迁移核对：`editorial/section-mapping.tsv`、`editorial/asset-mapping.tsv`

这是开放写作版。缺失正文明确标为“待完善”；网页构建通过不代表正文中所有生物信息分析命令都已实际执行。

## 1. 日常写作

直接编辑对应章节的 Markdown；不要修改生成的 `docs/*.html`。章节文件与素材目录使用相同名称：

| 章 | 正文文件（均在 `manuscript/`） | 素材目录（均在 `assets/`） |
|---|---|---|
| 1 学习地图与研究设计 | `01-learning-and-study-design.md` | `01-learning-and-study-design/` |
| 2 计算环境、命令行与必要编程 | `02-computing-and-programming.md` | `02-computing-and-programming/` |
| 3 高通量测序原理与生物数据表示 | `03-sequencing-and-data-formats.md` | `03-sequencing-and-data-formats/` |
| 4 从原始 reads 到可信的比对结果 | `04-quality-control-and-alignment.md` | `04-quality-control-and-alignment/` |
| 5 统计推断与数据探索的必要基础 | `05-statistics-and-exploration.md` | `05-statistics-and-exploration/` |
| 6 RNA-seq | `06-rna-seq.md` | `06-rna-seq/` |
| 7 ChIP-seq 与 ATAC-seq | `07-chip-seq-and-atac-seq.md` | `07-chip-seq-and-atac-seq/` |
| 8 WGS 与 WES | `08-wgs-and-wes.md` | `08-wgs-and-wes/` |
| 9 Snakemake 与可复现分析 | `09-snakemake-and-reproducibility.md` | `09-snakemake-and-reproducibility/` |
| 10 AI 与独立分析 | `10-ai-and-independent-analysis.md` | `10-ai-and-independent-analysis/` |

没有图片的章节保留空素材目录说明。新增素材建议用 `编号-简短英文主题.ext` 命名，如 `191-read-quality-example.png`；不要改动已被正文引用的文件名。现有编号是迁移时的稳定标识，不必随着正文顺序重排。

章节标题用 `#`，已定小节用 `##`。保留已有 `{#sec-...}` 标识即可维持链接。插图示例：

```markdown
![图片说明](../assets/06-rna-seq/191-read-quality-example.png){#fig-rna-quality-example}

解释见 @fig-rna-quality-example。

$$
Q=-10\log_{10}p
$$ {#eq-phred-example}

相关说明[^note-example]。

[^note-example]: 脚注正文。
```

跨章链接可写 `[SAM/BAM 操作](04-quality-control-and-alignment.md#sec-04-06)`。请勿手写会随重排变化的“图 3.1”或公式号。代码用普通围栏，例如三个反引号加 `bash` / `python` / `r`，不使用会执行的 `{r}` 块。

## 2. 安装与本地预览

安装 [Quarto **1.8.27**](https://github.com/quarto-dev/quarto-cli/releases/tag/v1.8.27) 和 Python **3.10+**。本工程不要求安装 R、LaTeX 或生物信息分析软件。Python 构建脚本只用标准库。

```bash
git clone https://github.com/menghaowei/bioinfo_book.git
cd bioinfo_book
quarto --version
python3 scripts/preview.py
```

打开 <http://localhost:4200>，修改 Markdown 后自动刷新。按 `Ctrl+C` 停止。Windows 如使用 Python Launcher，可把 `python3` 替换为 `py -3`。

## 3. 一键构建完整 HTML

```bash
python3 scripts/build.py
```

这个命令依次执行 Quarto 渲染、复制本地数学排版资源、生成旧网址跳转页，并检查 10 章、71 小节、迁移锚点、图片、脚本和站内链接。通过后，完整输出位于 `docs/`。

只阅读已构建网页，无需安装 Quarto：

```bash
python3 -m http.server 8000 --directory docs
```

打开 <http://localhost:8000>。推荐使用本地 HTTP 服务，以保证搜索等浏览器功能正常；无需联网加载字体、公式引擎或正文图片。原文链接和文献链接仍指向互联网。

## 4. Markdown 更新后自动发布

把正文、素材或配置提交到 `master` 后，`.github/workflows/publish.yml` 自动：

1. 安装固定版本 Quarto，构建 HTML；
2. 运行结构、路径与锚点检查，发现错误则停止；
3. 将生成的 `docs/` 和校验报告提交回仓库；
4. 上传完整网页并部署到 GitHub Pages。

网页地址保持为 <https://menghaowei.github.io/bioinfo_book/>。站点的 [`build.json`](https://menghaowei.github.io/bioinfo_book/build.json) 记录当前部署的源码提交和工作流运行链接。Actions 页的 **Build and publish BioinfoBook** 显示最新构建状态，也支持手动运行。PR 仅构建和检查，不发布。手动运行也仅在 `master` 上部署。自动生成的提交带 `[skip ci]`，不触发重复构建。

更新示例：

```bash
git add manuscript/06-rna-seq.md assets/06-rna-seq/
git commit -m "完善 RNA-seq 定量讲解"
git push origin master
```

Actions 会自动提交 HTML；下一次开始本地写作前先 `git pull --ff-only`，同步这些生成文件。如果同时有人更新了远端，自动提交可能因非快进而失败，此时同步后重新运行工作流，避免覆盖别人的更新。

## 5. 原稿核对与已知待完善项

- `archive/original-rmd/`：原始 Rmd 快照，含旧汇总/测试稿；不参与日常构建。
- `archive/question-drafts/`：题库所有 Markdown 版本；有 MHW 修订版的题组以该版为迁移主稿，其他版本完整保留。
- `editorial/outline.json`：已定三篇十章大纲与各小节规划。
- `editorial/section-mapping.tsv`：原文件、原小节、原行号、原块 SHA256、新章节、新锚点。
- `editorial/asset-mapping.tsv`：原路径、新路径、内容 SHA256 和路径修复依据。
- `editorial/corrections.json`：本轮重要校订的精确前后文本。
- `editorial/validation.json`：最近一次 HTML 结构检查结果。

原稿尚缺的内容、13 个 RNA-seq 文献编号对应的完整书目信息、两张失效外链截图均明确留有标记。旧图中的文字、历史安装命令、算法数值例子和实战预期输出仍待继续校订和运行验证。

`scripts/migrate_sources.py` 和 `scripts/apply_editorial_corrections.py` 是一次性迁移审计脚本，**日常写作和 CI 不运行它们**，以免覆盖后续作者修改。重新迁移须在独立副本中进行。完整的首次迁移依据是两份用户提供的原始 ZIP。

## 6. PDF

本轮仅构建 HTML。后续 PDF 以已确认的 **ElegantBook 中文教材风格**为基础实施，不在当前工作流中安装 LaTeX 或输出 PDF。
