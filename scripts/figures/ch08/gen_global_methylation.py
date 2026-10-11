"""FIG：GSE67867 全局 CpG 甲基化（真实数据）。

左：三样本覆盖加权全局 CpG 甲基化条形；右：12.4M 共有位点的 toSerum vs to2i
每位点比例散点（密度可视化，展示全基因组去甲基化）。
数据：.ch08-data/wgbss/cpg_mm9.tsv（由 merge_cpg_mm9.py 生成）
运行：python3 gen_global_methylation.py
输出：assets/09-base-imbalanced-sequencing/global-methylation-real.png
"""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
DATA = ROOT.parent / ".ch08-data" / "wgbss" / "cpg_mm9.tsv"
OUT = ROOT / "assets" / "09-base-imbalanced-sequencing" / "global-methylation-real.png"

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
    cols = {c: i for i, c in enumerate(
        "chr pos N_to2i X_to2i N_toSerum X_toSerum N_TKO X_TKO".split())}
    a = {s: [0, 0] for s in ("TKO", "to2i", "toSerum")}
    serum = []
    twoi = []
    with open(DATA) as fh:
        fh.readline()
        for line in fh:
            p = line.split("\t")
            a["to2i"][0] += int(p[cols["N_to2i"]]); a["to2i"][1] += int(p[cols["X_to2i"]])
            a["toSerum"][0] += int(p[cols["N_toSerum"]]); a["toSerum"][1] += int(p[cols["X_toSerum"]])
            a["TKO"][0] += int(p[cols["N_TKO"]]); a["TKO"][1] += int(p[cols["X_TKO"]])
            if len(serum) < 300000:
                serum.append(int(p[cols["X_toSerum"]]) / int(p[cols["N_toSerum"]]))
                twoi.append(int(p[cols["X_to2i"]]) / int(p[cols["N_to2i"]]))

    pct = {s: 100 * a[s][1] / a[s][0] for s in a}
    print({s: round(v, 2) for s, v in pct.items()})

    fig, axes = plt.subplots(1, 2, figsize=(8.6, 3.6), dpi=200,
                             gridspec_kw={"width_ratios": [1, 1.5]})

    ax = axes[0]
    names = ["TKO\n(Dnmt 三敲)", "to2i\n(2i 培养)", "toSerum\n(血清培养)"]
    vals = [pct["TKO"], pct["to2i"], pct["toSerum"]]
    bars = ax.bar(names, vals, color=[MUTED, WARN, PRIMARY], width=0.62)
    for b, v in zip(bars, vals):
        ax.text(b.get_x() + b.get_width() / 2, v + 1.5, f"{v:.1f}%",
                ha="center", fontsize=9.5, color="#333333")
    ax.set_ylabel("覆盖加权全局 CpG 甲基化（%）", fontsize=9, color=MUTED)
    ax.set_ylim(0, 82)
    ax.tick_params(labelsize=8.5)

    ax = axes[1]
    hb = ax.hexbin(serum, twoi, gridsize=90, bins="log", cmap="Greens",
                   mincnt=1, linewidths=0)
    ax.plot([0, 1], [0, 1], color=MUTED, lw=0.8, ls="--")
    ax.text(0.06, 0.88, "对角线下方 = 2i 中去甲基化的位点", fontsize=9, color=PRIMARY)
    ax.set_xlabel("血清培养（toSerum）位点甲基化比例", fontsize=9, color=MUTED)
    ax.set_ylabel("2i 培养（to2i）位点甲基化比例", fontsize=9, color=MUTED)
    ax.set_xlim(-0.02, 1.02)
    ax.set_ylim(-0.02, 1.02)
    cb = fig.colorbar(hb, ax=ax, pad=0.02)
    cb.set_label("位点数（log）", fontsize=8, color=MUTED)
    cb.ax.tick_params(labelsize=7)

    for ax in axes:
        for sp in ("top", "right"):
            ax.spines[sp].set_visible(False)
        ax.tick_params(colors=MUTED)
    fig.tight_layout()
    fig.savefig(OUT, bbox_inches="tight")
    print("written", OUT)


if __name__ == "__main__":
    main()
