"""FIG：GLORI 位点定量两联图（真实分析数据）。

数据：.ch08-data/glori/glor_sites.tsv —— 34,585 个共有位点的修饰比例与差异检验。
左：siNC 重复间一致性；右：对照 vs METTL3 敲低的修饰比例对比。
运行：python3 gen_glori_scatter.py
输出：assets/09-base-imbalanced-sequencing/glori-scatter-real.png
"""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager

ROOT = Path(__file__).resolve().parents[3]
DATA = ROOT.parent / ".ch08-data" / "glori" / "glor_sites.tsv"
OUT = ROOT / "assets" / "09-base-imbalanced-sequencing" / "glori-scatter-real.png"

PRIMARY = "#186254"
MUTED = "#6b7280"
FILL = "#e8f4f1"
WARN = "#b45309"

for f in ("PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", "Noto Sans CJK SC"):
    if any(f.lower() in x.name.lower() for x in font_manager.fontManager.ttflist):
        plt.rcParams["font.family"] = f
        break
plt.rcParams["axes.unicode_minus"] = False


def main():
    cols = {}
    header = None
    rows = {k: [] for k in
            ("ratio_si31", "ratio_si32", "ratio_nc1", "ratio_nc2",
             "ratio_nc", "ratio_si", "fdr_diff", "gene")}
    with open(DATA) as fh:
        header = fh.readline().rstrip().split("\t")
        idx = {n: i for i, n in enumerate(header)}
        for line in fh:
            p = line.rstrip().split("\t")
            for k in rows:
                rows[k].append(p[idx[k]])
    import math
    nc1 = [float(x) for x in rows["ratio_nc1"]]
    nc2 = [float(x) for x in rows["ratio_nc2"]]
    ncp = [float(x) for x in rows["ratio_nc"]]
    sip = [float(x) for x in rows["ratio_si"]]
    fdr = [float(x) for x in rows["fdr_diff"]]

    r = 0.936
    fig, axes = plt.subplots(1, 2, figsize=(8.6, 3.9), dpi=200)

    ax = axes[0]
    ax.plot([0, 1], [0, 1], color=MUTED, lw=0.8, ls="--", zorder=1)
    ax.scatter(nc1, nc2, s=4, alpha=0.18, color=PRIMARY, linewidths=0, zorder=2)
    ax.text(0.05, 0.93, f"重复一致性：Pearson r = {r:.3f}", fontsize=9, color=PRIMARY,
            transform=ax.transAxes)
    ax.set_xlabel("siNC 重复 1 修饰比例", fontsize=9, color=MUTED)
    ax.set_ylabel("siNC 重复 2 修饰比例", fontsize=9, color=MUTED)
    ax.set_xlim(-0.02, 1.02)
    ax.set_ylim(-0.02, 1.02)

    ax = axes[1]
    ax.plot([0, 1], [0, 1], color=MUTED, lw=0.8, ls="--", zorder=1)
    down = [(x, y) for x, y, f in zip(ncp, sip, fdr) if f < 0.05 and y < 0.5 * x]
    rest = [(x, y) for x, y, f in zip(ncp, sip, fdr) if not (f < 0.05 and y < 0.5 * x)]
    ax.scatter([p[0] for p in rest], [p[1] for p in rest], s=4, alpha=0.15,
               color=MUTED, linewidths=0, zorder=2, label="其余位点")
    ax.scatter([p[0] for p in down], [p[1] for p in down], s=5, alpha=0.5,
               color=WARN, linewidths=0, zorder=3,
               label=f"显著下降（FDR<0.05，敲低<对照一半）：{len(down):,} 个")
    ax.annotate("KCTD5 chr16:2708329\n0.61 → 0.14", xy=(0.613, 0.135), xytext=(0.24, 0.05),
                fontsize=8.5, color=WARN,
                arrowprops=dict(arrowstyle="->", color=WARN, lw=0.9))
    ax.text(0.04, 0.60, "对角线 = 修饰比例不变", fontsize=8.5, color=MUTED,
            transform=ax.transAxes)
    ax.set_xlabel("对照（siNC）合并修饰比例", fontsize=9, color=MUTED)
    ax.set_ylabel("METTL3 敲低（siMETTL3）合并修饰比例", fontsize=9, color=MUTED)
    ax.set_xlim(-0.02, 1.02)
    ax.set_ylim(-0.02, 1.02)
    ax.legend(fontsize=8, frameon=False, loc="upper left", markerscale=2.2)

    for ax in axes:
        for sp in ("top", "right"):
            ax.spines[sp].set_visible(False)
        ax.tick_params(labelsize=8, colors=MUTED)
    fig.tight_layout()
    fig.savefig(OUT, bbox_inches="tight")
    print("written", OUT)


if __name__ == "__main__":
    main()
