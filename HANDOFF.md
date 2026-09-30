# BioinfoBook v1 HTML 发布交接（2026-09-30 更新）

**第一版 HTML 已发布，并完成线上电脑端验收。** 本节是当前状态；后面的原交接文档保留为发布前历史快照。

## 发布结果与版本追溯

- 在线阅读：https://menghaowei.github.io/bioinfo_book/
- 仓库：https://github.com/menghaowei/bioinfo_book ，默认分支 `master`。
- 发布源码提交：`ad10c680d0f1cb46bdb4c2b65323bbf06ebc0414`（Publish BioinfoBook v1 Quarto HTML）。
- Actions 自动保存的完整 HTML 提交：`850eab2caeb99083f6de6cb71d1dfb52bb2fbc8d`。
- 成功运行：https://github.com/menghaowei/bioinfo_book/actions/runs/36689316643 。触发事件为真实的 `push`，build 与 deploy 均为 success，首次运行即成功。
- 部署完成：2026-09-30 16:23:39（Asia/Shanghai；08:23:39 UTC）。
- Pages 的 `build_type` 已从 `legacy` 切换为 `workflow`（GitHub Actions），原网址保持不变。
- 线上 `build.json` 已核对：源码 SHA 与上述发布源码提交一致，包含成功的工作流运行链接。源码提交与自动生成 HTML 提交各自有独立 SHA，这是工作流的预期行为。
- 本节、README 和验收证据随后以仅记录发布结果的 `[skip ci]` 提交归档；该提交不改变已部署的 `docs/`。最终仓库 tip 可由 `git rev-parse HEAD` 查询，工作区顶层 `BioinfoBook_HANDOFF_2026-09-30.md` 另记该 SHA。

## 实际使用的本地工程

`/Users/meng/14.LLM_project/02.mhw_bioinfo_books/01.bioinfo_book_codex/bioinfo_book_publish/`

原同级 `bioinfo_book/` 指向 `menghaowei/bioinfo`，且包含大量未提交修改和一个本地提交，因此没有对它进行合并、清理、提交或修改远端。新版目录从目标仓库正常克隆，保留两条既有历史，再合并交接工程；远端接续起点仍为 `e0dec31fcdb4b8d13b6eec29fe7d7797a0326f2f`。没有 force push，也没有删除旧仓库文件。

`BioinfoBook_v1_handoff/`、原题库及交接 ZIP 保留。交接包的 850 个 SHA256 全部核对通过。正文、附录、素材及原稿归档与交接包逐文件比对一致，未重新运行一次性迁移或校订脚本。

## 本轮修复与发布机制

- 保留三篇、十章、71 小节、25 道基础题、稳定锚点及“待完善”内容。
- 修复行内长网址在窄屏上不换行的问题；命令代码块仍按原行结构横向滚动。用户随后明确以后以电脑端阅读为主，线上验收未继续扩展手机覆盖。
- 工作流仅在非 PR 且分支为 `master` 时回写 HTML 和部署；自动回写范围限定为 `docs/`、`editorial/validation.json`、根目录兼容入口 `index.html`。
- `docs/build.json` 新增对应的 Actions 运行链接，可将线上页面与构建源码直接对应。
- 实际本地构建使用 Quarto 1.8.27 / Python 3.13.0；CI 使用 Quarto 1.8.27 / Python 3.12。

## 验证结果与边界

1. **网页构建验证**：`python3 scripts/build.py` 成功；CI 重新构建成功。校验报告为 10 章、71 小节、32 个 HTML、352 个迁移锚点、190 处图片引用，0 个错误。
2. **线上发布验证**：1440 × 1080 Chromium 检查全部 20 个阅读页面；章节导航、深层页面与稳定锚点、图片、公式、全文搜索正常；`HaplotypeCaller` 搜索返回 2 个相关文档，点击可进入 WGS 页面；12 个旧章节 URL 均跳转到新版目标。无页面错误、站内 HTTP 资源错误、破损图片、公式错误或页面级横向溢出。第 4、5、6、8 章分别渲染 70、94、6、110 个数学节点。
3. **科学内容审校**：本轮没有执行书中的生物信息分析命令，也没有完成全书科学审校。HTML 构建和线上功能成功不等于分析流程已经全部验证。

证据：`handoff-evidence/online-2026-09-30/browser-report.json`、`actions-run.json`、`home.png`、`math.png`。本地构建与早先手机抽查在 `handoff-evidence/local-2026-09-30/`；`mobile-overflow-before-fix.png` 是修复前诊断图，不代表最终页面状态。可复用的浏览器验收脚本为 `handoff-evidence/verify-published-site.cjs`；它需要额外的 Playwright，仅用于验收，不是日常构建依赖。传入 `--desktop-only` 可只验收电脑端。

## 本机日常写作与发布

本机默认 PATH 曾优先选择 Python 3.8，因此使用工作区中的独立工具环境。工具与登录配置位于工作区 `.bioinfobook-tools/`，不属于发布仓库。Git 登录已验证为 `menghaowei`，当前仓库通过本地 credential helper 使用该登录；配置目录权限为 700，凭据文件为 600。

```bash
cd /Users/meng/14.LLM_project/02.mhw_bioinfo_books/01.bioinfo_book_codex/bioinfo_book_publish
source ../.bioinfobook-tools/activate.sh
git pull --ff-only
python3 scripts/preview.py
```

预览地址：<http://localhost:4200>，Ctrl+C 停止。`activate.sh` 设置 Quarto/Python 路径及本次指定的代理；如以后停用代理，应相应调整该本机环境文件。其他电脑按 README 安装 Quarto 1.8.27 与 Python 3.10+ 即可。

继续编辑 `manuscript/*.md`、`appendices/*.md`，新增图片放入对应 `assets/` 子目录；首页编辑 `index.qmd`。保留稳定锚点，不手改 `docs/`，不运行一次性迁移/校订脚本。

```bash
python3 scripts/build.py
git add manuscript appendices assets index.qmd
git add docs editorial/validation.json index.html
git commit -m "完善教材内容"
git push origin master
```

普通内容提交不要使用 `[skip ci]`。推送后 Actions 会重新构建、验证、提交生成 HTML 并部署；下次写作前 `git pull --ff-only`。如构建期间远端被其他人更新，自动推送仍会安全失败，应同步远端后重新运行，不使用 force push。

## 剩余事项

- 第 9、10 章、ATAC-seq 等“待完善”正文、练习和教学单元继续补写。
- 两张失效外链图片仍为明确占位；13 个 RNA-seq 原文文献编号的完整书目信息待补。
- 历史安装命令、图中文字、算法例题、示例数据、分析环境及实战预期输出尚未全面实跑和审校。
- Quarto 1.8.27 构建保留已知非致命警告：Pandoc 未加载 `zh-CN` 翻译数据（正文、导航及数学显示已实测）；Actions 提示旧 action 的 Node 20 运行时已由平台改为 Node 24，以及未来 ubuntu-latest 镜像迁移。此次构建和部署均成功，后续可单独维护工具链。
- PDF 本轮未生成；后续仍按 ElegantBook 中文教材风格实施。

---

# 发布前历史交接原文（下文“尚未发布”等状态已由上文更新）

# BioinfoBook：本地 Codex 项目交接

交接日期：2026-09-30（Asia/Shanghai）。本文件对应 `BioinfoBook_v1_handoff_2026-09-30.zip`。

## 1. 当前结论：本地工程已完成整理和 HTML 构建，尚未发布

**请接续压缩包内的现有工程，不要重新从零迁移、概括或压缩正文。**

用户最新决定：停止当前网页端的发布操作，下载完整工程，在本地 Codex 继续。此次交付的重点是保留现有成果及准确说明尚未完成的工作。

| 项目 | 真实状态 |
|---|---|
| 正文结构 | 已建立三篇、十章、71 个规划小节；缺失内容标为“待完善” |
| 现有题库 | 已迁移第 1—25 题，分为五个附录页面；其余题目没有凭空补写 |
| 素材与追溯 | 190 条素材映射、352 条原稿标题/片段迁移记录，保留原稿归档 |
| 科学与文字校订 | 35 条校订记录；这不等于全书科学内容已完成审校 |
| HTML | 已用 Quarto 1.8.27 构建，完整输出在 `docs/` |
| 本地结构验证 | 10 章、71 小节、352 个迁移锚点、190 处图片引用；0 个错误 |
| 页面总数 | `docs/` 下 32 个 HTML：20 个正文/附录/首页页面，加 12 个旧地址跳转页 |
| 浏览器验证 | 首页及四个代表性章节检查通过；公式、图片、搜索通过；RNA-seq 手机视图无页面级横向溢出 |
| GitHub Actions | 工作流文件已编写，但尚未在该仓库实际运行验证 |
| GitHub 上传 | 未形成新版提交，未更新远端分支 |
| 线上新版 HTML | 尚未发布；不能把本地构建通过报告为线上发布成功 |
| PDF | 尚未实施；后续以 ElegantBook 中文教材风格为基础 |

“190”是素材映射数和渲染图片引用数，不等于素材目录内文件总数；目录还保留说明文件和迁移过程中留下的素材文件。不要仅凭这一数字批量删除文件。

## 2. 已确认的需求与写作约束

1. 沿用现有仓库 `https://github.com/menghaowei/bioinfo_book`，默认分支 `master`。
2. 沿用原网址 `https://menghaowei.github.io/bioinfo_book/`，完成第一版 HTML 发布。
3. 使用 Quarto book 工程。用户日常直接编辑 `manuscript/*.md` 和 `appendices/*.md`，提交后自动构建和发布。
4. 采用已讨论的“三篇、十章”大纲，保留全部 71 个小节；缺正文也保留标题，在内容处写“待完善”。
5. 已有讲解尽量保留深度，可按教学作用重排；不要把长篇原稿改成摘要或仅剩目录。
6. 语言风格参考原稿 `0010-introduction.Rmd`、`0020-introduction_of_NGS.Rmd`、`0040-mapping_and_BAM_operation.Rmd`，以及作者专栏 `https://zhuanlan.zhihu.com/ngs-learning`。这些是风格参考，不代表已经完整抓取或迁移了专栏全部文章。
7. 按章节统一正文文件和素材目录命名，保留原稿到新稿的对应关系。
8. 第一版范围主要是短读长、有参考基因组、bulk 分析；三类实战为 RNA-seq、ChIP-seq/ATAC-seq、WGS/WES 胚系小变异。其他方向保留概念入口，不能宣称已有完整实战。
9. 当前先完成 HTML 和 GitHub 自动发布；不在当前工作流生成 PDF，也不显示未经生成验证的 PDF 下载入口。
10. 后续 PDF 必须采用 **ElegantBook 中文教材风格**：中文教材版式、彩色概念框、编号环境、公式、引用、页底脚注。可以将其环境对应为“核心概念”“分析原理”“操作示例”“常见错误”。用户另有 PDF 要求待补充，不能直接换成其他模板。

## 3. 压缩包内容与权威写作入口

压缩包解压后的项目目录为 `BioinfoBook_v1_handoff/bioinfo_book/`。请在这个目录中打开本地 Codex。项目根目录的 `HANDOFF.md` 与单独提供的交接文档一致。

| 路径 | 用途 |
|---|---|
| `HANDOFF.md` | 本交接文档；本地 Codex 首先阅读 |
| `README.md` | 作者日常写作、预览、一键构建和发布说明 |
| `_quarto.yml` | 分篇、章节、附录、主题、搜索、公式及站点配置 |
| `index.qmd` | 阅读指南、书籍首页、团队与当前版本说明 |
| `manuscript/*.md` | 十章正文，后续主要写作入口 |
| `appendices/*.md` | 25 道基础题、文件格式、数学阅读、复现、参考文献等附录 |
| `assets/<章节名>/` | 按章节整理的图片与素材 |
| `styles/`、`includes/` | 页面样式、响应式处理、回到顶部按钮等 |
| `vendor/mathjax/` | 本地公式引擎及其资源，支持不依赖外部 CDN 的公式显示 |
| `pandoc-data/` | 中文翻译及构建支持文件 |
| `docs/` | 完整已构建 HTML、图片、脚本、搜索索引、公式资源、兼容跳转页 |
| `scripts/build.py` | 一键构建：Quarto render，然后运行验证 |
| `scripts/preview.py` | Quarto 本地实时预览 |
| `scripts/post_render.py` | 复制公式资源、修复公式路径、生成构建信息和旧网址跳转页 |
| `scripts/validate.py` | 结构、文件、站内链接、锚点和迁移标题检查 |
| `scripts/migrate_sources.py` | 一次性原稿迁移脚本，仅供审计或在独立副本复现 |
| `scripts/apply_editorial_corrections.py` | 一次性校订脚本；不要对现稿重复运行 |
| `.github/workflows/publish.yml` | 推送到 master 后构建、保存 HTML、部署 GitHub Pages 的工作流 |
| `editorial/outline.json` | 71 小节完整教学大纲，包括目的、来源、原始状态及补写计划 |
| `editorial/section-mapping.tsv` / `.json` | 原文件、原行号、原稿块 SHA256、新章节和新锚点的对应关系 |
| `editorial/asset-mapping.tsv` / `.json` | 原素材路径、新路径、SHA256 和修复依据 |
| `editorial/corrections.json` | 35 条校订的原因和前后文本 |
| `editorial/missing-assets.tsv` / `.json` | 无法找回的原始图片记录 |
| `editorial/validation.json` | 本次结构和 HTML 校验报告 |
| `archive/original-rmd/` | 原作者 Rmd、旧汇总稿、参考文献等归档 |
| `archive/question-drafts/` | 原题库 Markdown 的不同版本；有 MHW 修订版时以其为迁移主稿 |
| `handoff-evidence/` | 构建日志、浏览器检查日志、三张预览截图、远端状态及 QA 脚本快照 |

项目根目录仍保留旧仓库中的旧 HTML、`css/`、`libs/` 等文件，作为接续仓库时的历史兼容内容。**新版完整网站输出以 `docs/` 为准**；不要继续编辑旧 HTML。根目录 `index.html` 当前是兼容旧 Pages 根目录来源的跳转入口。

包内不携带 `.git/` 历史、Quarto 缓存、运行时软件安装包或未完成的上传分块；这些不属于后续写作和构建的必要文件。原始两份上传 ZIP 本身也未重复装入：主要原稿与题库版本已在 `archive/` 保留，使用中的素材已在 `assets/` 保留。如需从原始 ZIP 完全重做迁移，请另行提供原 `bioinfo_book.zip` 与 `BOOK-Bioinfo-100-questions.zip`，并在隔离副本操作。

交接包已去除网页端上传实验使用的一次性恢复脚本及工作流恢复步骤。本地应使用正常 Git 提交和推送，无需处理上传分块。

## 4. 本地如何阅读、构建和继续写作

### 4.1 先查看现成网页，无需安装 Quarto

在项目根目录执行：

```bash
python3 -m http.server 8000 --directory docs
```

打开 `http://localhost:8000`。建议通过 HTTP 服务阅读，以使搜索等浏览器功能正常工作。页面正文、图片和数学排版资源已本地化；引用的外部文献链接仍需联网。

### 4.2 构建环境

- 本次实际验证版本：**Quarto 1.8.27**。
- Python：3.10 或以上；构建脚本使用标准库，工作流设置为 Python 3.12。
- HTML 构建不要求 R、LaTeX、测序分析软件或实际实验数据。
- `_quarto.yml` 禁用示例代码执行；构建不会运行书中的生物信息学命令。

安装 Quarto 后确认其位于 PATH，再执行：

```bash
quarto --version
python3 scripts/build.py
```

构建后在 `editorial/validation.json` 中确认 `errors` 为空，并通过浏览器查看 `docs/`。若使用 Windows Python Launcher，可将 `python3` 换为 `py -3`。

实时预览：

```bash
python3 scripts/preview.py
```

打开 `http://localhost:4200`。修改 Markdown 后应重新渲染；按 Ctrl+C 停止。

### 4.3 写作规则

- 日常编辑 `manuscript/` 和 `appendices/`；不要手改 `docs/` 中的生成页面。
- 保留 `{#sec-...}`、`{#fig-...}` 等稳定标识，跨章链接使用 `.md#锚点` 或 Quarto 交叉引用。
- 插图放在对应章节的 `assets/` 目录；已经引用的文件不要随意重命名。
- 不运行一次性迁移和校订脚本来“更新书稿”，否则可能覆盖新写内容或因前置文本变化失败。
- `editorial/outline.json` 中 A/B/C 是最初内容盘点状态；后续应基于实际正文更新，不能把它直接当作最新完成度。

## 5. 本次完成的检查及其边界

### 5.1 构建与结构

完整 Quarto HTML 构建已通过。校验覆盖本地文件引用、站内锚点、重复锚点、未解析的交叉引用、十章与 71 小节结构、352 条迁移记录是否在页面中保留。构建日志保存在 `handoff-evidence/local-build.log`。

### 5.2 浏览器抽查

使用 Chromium/Playwright 检查：

| 页面/功能 | 结果 |
|---|---|
| 首页，1440 × 1080 | 标题和页面正常 |
| 第 4 章：质控与比对 | 70 个数学节点；无公式错误、破损图片或页面级横向溢出 |
| 第 5 章：统计 | 94 个数学节点；无公式错误、破损图片或页面级横向溢出 |
| 第 6 章：RNA-seq | 6 个数学节点；无公式错误、破损图片或页面级横向溢出 |
| 第 8 章：WGS/WES | 110 个数学节点；无公式错误、破损图片或页面级横向溢出 |
| RNA-seq，390 × 844 | 无页面级横向溢出；宽内容在阅读栏内滚动 |
| 搜索 `HaplotypeCaller` | 返回 2 个匹配文档 |
| 本次抽查的浏览器页面错误/资源 HTTP 错误 | 未发现 |

数学节点数只是渲染检查指标，不是科学内容审校结果。手机验证目前是代表性页面抽查，尚未逐页覆盖所有浏览器和所有屏幕尺寸。`styles/book.css` 已对表格、代码和展示公式设置局部滚动，并有页面级溢出限制；后续仍应检查长内容是否可完整滚动读取。

日志中列出的部分超宽子元素是滚动容器内的内容，不能仅凭其边界超过屏幕就判定页面仍在整体溢出。实际交互复核比仅看元素宽度更可靠。

### 5.3 尚未完成的内容审校

- 两张原外链截图无法取得，已留明确图位占位；详见 `editorial/missing-assets.json`。
- RNA-seq 中 13 个原文文献编号的完整书目信息尚需补齐。
- 第 9、10 章、ATAC-seq 等新增教学单元仍有大量“待完善”内容。
- 旧图中文字、历史安装步骤、分析命令、算法数值例题及实战预期输出未全部重新验证。
- 尚未建立并运行覆盖全书的示例数据、环境和分析流程。
- 现有校订包括测序原理、SAM FLAG/MAPQ/CIGAR、FPKM/TPM、简化基因型似然、HaplotypeCaller 与联合分型等；请以精确校订记录为准，不假定其他内容已经全部正确。

## 6. GitHub 的真实状态与后续发布步骤

### 6.1 交接时远端状态

- 仓库：`menghaowei/bioinfo_book`，公开仓库。
- 默认分支：`master`。
- 本次交接重新读取到的远端 HEAD：`e0dec31fcdb4b8d13b6eec29fe7d7797a0326f2f`。
- 提交标题：`make sure authers`，日期为 2020-03-31。
- 重新查询到的 Actions 运行总数：`0`。
- 本轮没有创建新版 commit，也没有移动任何分支 ref，没有完成线上发布。
- 上传尝试最多产生未关联到分支的 Git blob；不能把这些对象当成已上传完成的项目。一个大分块上传被用户中止，其最终对象状态未确认，但不会自行更改 master。
- 当前执行环境没有可用于 Git push 的终端凭据；只读 `git ls-remote` 成功，`git push --dry-run` 提示无法读取 GitHub 用户名。这是本环境的认证状态，不代表用户本地环境不能正常推送。
- 旧站此前可访问。交接时未完成新版线上浏览器验收，也没有确认 Pages 发布源是否已切换为 GitHub Actions。

`docs/build.json` 中的 `source_commit` 在本地构建时会记录原有 Git HEAD；此处旧 SHA 不是新版本发布标志。首次真正 CI 构建后应以工作流运行、构建信息及线上页面共同验证。

### 6.2 本地继续发布的推荐顺序

1. **先阅读本文件、README、工作流及校验报告；确认现有成果，而不是重新迁移。**
2. 在本地确认 GitHub 登录及仓库写权限。压缩包不含 `.git/`，推荐先克隆现有仓库，再将项目文件覆盖进去，保留克隆得到的历史。
3. 先检查远端是否在交接后发生变化；若变了，检查差异，不使用强制推送覆盖他人更新。
4. 运行本地构建并抽查页面。确认正文、素材、配置、工作流和完整 `docs/` 都在待提交文件中。
5. 在仓库 Settings → Pages 检查 Source；使用该工作流发布时将来源设为 **GitHub Actions**。同时确认仓库和组织策略允许工作流所需权限。
6. 将工程作为正常新提交推送到 `master`，观察 **Build and publish BioinfoBook** 首次运行。
7. 失败时先读 build/deploy job 日志，修复具体原因；不要用“工作流已写好”代替成功运行。
8. 成功后检查原网址首页、至少一个深层章节、图片、公式、搜索及一个旧章节跳转页，确认访问到的是新版内容。
9. 记录最终提交 SHA、Actions run URL、部署时间和线上验证结果，再宣布第一版发布完成。

macOS/Linux 合并文件的示例（将 `PACKAGE_PROJECT` 改成解压后项目的真实绝对路径）：

```bash
git clone https://github.com/menghaowei/bioinfo_book.git bioinfo_book_publish
cd bioinfo_book_publish
git switch master
git pull --ff-only

PACKAGE_PROJECT="/your/path/BioinfoBook_v1_handoff/bioinfo_book"
rsync -av --exclude='.git/' --exclude='.quarto/' "$PACKAGE_PROJECT/" ./

quarto --version
python3 scripts/build.py
git status --short
git diff --stat

# 检查实际待提交内容后再提交。不要使用 --force。
git add -A
git commit -m "Publish BioinfoBook v1 Quarto HTML"
git push origin master
```

示例不使用 `rsync --delete`，以免删除远端后来新增的文件。Windows 可使用文件复制合并；务必显示并复制 `.github/`、`.gitignore` 等项目配置，但不要覆盖克隆仓库的 `.git/`。

### 6.3 当前工作流的行为和未验证事项

工作流响应 `master` 的 push、PR 以及手动运行：检出代码 → Python 3.12 → Quarto 1.8.27 → `scripts/build.py`。非 PR 运行会把生成内容提交回 master，再上传 `docs/` 并使用 `actions/deploy-pages@v4` 发布。PR 只构建和验证。

自动提交标题含 `[skip ci]`，以避免重复构建；下一次本地写作前应 `git pull --ff-only`。工作流需要 `contents: write`、`pages: write`、`id-token: write`。首次 CI 尚未运行，必须实际验证这些权限、Pages 环境和仓库策略。

并发写作仍有具体风险：构建期间 master 若被其他人更新，自动 `git push` 可能因为不是快进而失败。目前会停止而不是强行覆盖；需要同步最新远端并重新运行。

## 7. 尚未完成的任务，按优先级接续

| 优先级 | 任务 | 完成标准 |
|---|---|---|
| P0 | 正常 Git 上传完整工程 | master 中能看到 Markdown、素材、配置、脚本、工作流及 docs |
| P0 | 首次 GitHub Actions 构建与部署 | build 和 deploy 成功，有可追溯的运行记录 |
| P0 | 原网址新版验收 | 原网址实际显示新版；深层页、图片、公式、搜索、旧跳转正常 |
| P1 | 证明 Markdown 更新会自动发布 | 下一次真实正文修改能完成构建、生成内容提交与 Pages 更新 |
| P1 | 扩大移动端抽查 | 全章重点宽表、命令和长公式均可滚动读取 |
| P1 | 整理首次发布记录 | 记录 SHA、run URL、部署时间、已知问题 |
| P2 | 补写“待完善”内容与文献 | 按大纲逐小节推进，保留讲解深度与教学衔接 |
| P2 | 科学审校及实战复现 | 每项修改有依据；关键流程在明确环境、数据和版本下实际运行 |
| 后续独立任务 | ElegantBook 风格 PDF | 用户补充要求后实现并逐页检查，不影响已有 HTML 写作 |

## 8. 可直接交给本地 Codex 的接续提示词

> 请先阅读项目根目录 `HANDOFF.md`、`README.md`、`_quarto.yml`、`.github/workflows/publish.yml` 和 `editorial/validation.json`。这是已有的 BioinfoBook Quarto 工程，请继续现有成果，不要从零迁移，也不要把正文压缩成摘要。已完成三篇十章71小节、25道基础题、素材整理和本地HTML构建；尚未把新版提交到 GitHub，也没有实际运行成功的部署工作流。
>
> 先检查本地工程、Git状态和远端 `menghaowei/bioinfo_book` 的最新状态，再完成正常 Git 上传、GitHub Actions 首次构建与 Pages 发布，保持原网址 `https://menghaowei.github.io/bioinfo_book/`。不要 force push。若需要账号登录，请指出具体阻塞。以实际日志和线上访问结果为准；完成后给出 commit SHA、Actions链接及访问网址。
>
> 日常写作只编辑 Markdown 和对应素材，保留稳定锚点。缺失内容保留“待完善”。当前不生成PDF，后续PDF必须以已经确认的 ElegantBook 中文教材风格为基础。已有生物信息分析命令尚未逐项实跑，不要把网页构建通过当作科学内容或分析流程全部验收。

## 9. 完整性文件

解压包顶层的 `PACKAGE_CONTENTS.tsv` 列出所有交付文件的相对路径、字节数和 SHA256；`SHA256SUMS.txt` 可用于校验。文件清单不包含它们自身，避免递归计算。

在解压包顶层可运行：

```bash
shasum -a 256 -c SHA256SUMS.txt
```

Linux 如无 `shasum`，可以使用 `sha256sum -c SHA256SUMS.txt`。请保留这份交接包作为首次本地接续的快照，后续以 Git 提交记录跟踪变化。
