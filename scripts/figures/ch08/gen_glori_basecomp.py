"""FIG：GLORI 文库实测逐位置碱基组成（A 的坍缩）。

数据：.ch08-data/glori/glor_perpos.tsv —— SRR21356251（293T GLORI+ rep1）前 ~79 万条 reads
逐位置 A/G/C/T 计数。运行：python3 gen_glori_basecomp.py
输出：assets/09-base-imbalanced-sequencing/glori-basecomp-real.png
"""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager

ROOT = Path(__file__).resolve().parents[3]
DATA = ROOT.parent / ".ch08-data" / "glori" / "glor_perpos.tsv"
OUT = ROOT / "assets" / "09-base-imbalanced-sequencing" / "glori-basecomp-real.png"

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
    pos, a, g, c, t = [], [], [], [], []
    with open(DATA) as fh:
        fh.readline()
        for line in fh:
            p, A, G, C, T, tot = line.split()
            pos.append(int(p))
            a.append(100 * int(A) / int(tot))
            g.append(100 * int(G) / int(tot))
            c.append(100 * int(C) / int(tot))
            t_ = 100 * int(T) / int(tot)
    fig, ax = plt.subplots(figsize=(7.6, 3.4), dpi=200)
    ax.axhspan(0, 100, xmin=0, xmax=1, color="none")
    ax.axvspan(15, 35, color=FILL, zorder=0)
    ax.plot(pos, g, color=MUTED, lw=1.6, label="G", zorder=2)
    ax.plot(pos, a, color=PRIMARY, lw=1.9, label="A", zorder=3)
    ax.axhline(25, color=WARN, lw=0.9, ls="--", zorder=1)
    ymax = max(max(g), max(a)) * 1.18
    ax.annotate("常规 RNA-seq 的 A 比例（约 25%）", xy=(55, 25), xytext=(48, 8),
                fontsize=8.5, color=WARN,
                arrowprops=dict(arrowstyle="-", color=WARN, lw=0.7))
    ax.annotate("插入序列：A 坍缩至约 1%，G 升至 45%", xy=(25, 2.5), xytext=(38, 12),
                fontsize=9, color=PRIMARY,
                arrowprops=dict(arrowstyle="->", color=PRIMARY, lw=0.9))
    ax.annotate("5′ 引物", xy=(5, 45), fontsize=8.5, color=MUTED, ha="center")
    ax.annotate("3′ 接头", xy=(68, 45), fontsize=8.5, color=MUTED, ha="center")
    ax.set_xlabel("reads 中的位置（bp）", fontsize=9, color=MUTED)
    ax.set_ylabel("碱基占比（%）", fontsize=9, color=MUTED)
    ax.set_xlim(1, 75)
    ax.set_ylim(0, ymax)
    ax.legend(fontsize=8.5, frameon=False, loc="upper right", title=None)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    ax.tick_params(labelsize=8, colors=MUTED)
    fig.tight_layout()
    fig.savefig(OUT, bbox_inches="tight")
    print("written", OUT)


if __name__ == "__main__":
    main()
