# RNA-seq DAG

`generate_dag.py` 从第 10 章当前 Markdown 的 `rnaseq/Snakefile`、配置和样本表提取代码，在临时目录创建空输入，只运行 Snakemake `--dag`，不执行生信分析。验证版本 Snakemake 9.27.0。

```bash
python3 scripts/figures/ch10/generate_dag.py
dot -Tsvg assets/10-snakemake-and-reproducibility/rnaseq-dag.dot > assets/10-snakemake-and-reproducibility/rnaseq-dag.svg
```

`rnaseq-dag-raw.dot` 保存原始导出；`rnaseq-dag.dot` 只添加字体、配色和按样本分组的布局。带 `style=invis` 的边只约束版面，不表示依赖，不生成可见箭头。19 个节点和 35 条可见依赖均来自原始 DOT。最终 SVG 使用 Graphviz 3.0.0（Quarto 1.8.27 内置 WASM）渲染，包含 title/desc 文本替代。
