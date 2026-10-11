"""FIG：IGV 风格的真实甲基化轨迹（官方 mm9 表，替代原自绘示意图）。

数据：.ch08-data/wgbss/cpg_mm9.tsv（GSE67867 处理表）与 dss_dmrs.tsv（DSS callDMR）。
区域：chr13:73,152,624-73,153,119（diff 0.850，21 个 CpG），展示窗口 ±700 bp。
运行：python3 gen_igv_real.py
输出：assets/09-base-imbalanced-sequencing/igv-methylation-real.png
"""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager

ROOT = Path(__file__).resolve().parents[3]
DATA = ROOT.parent / ".ch08-data" / "wgbss" / "cpg_mm9.tsv"
OUT = ROOT / "assets" / "09-base-imbalanced-sequencing" / "igv-methylation-real.png"

CHROM, DS, DE = "chr13", 73152624, 73153119
FLANK = 700

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
    rows = []
    with open(DATA) as fh:
        fh.readline()
        for line in fh:
            p = line.rstrip().split("\t")
            if p[0] != CHROM:
                continue
            pos = int(p[1])
            if DS - FLANK <= pos <= DE + FLANK:
                rows.append((pos, int(p[2]), int(p[3]), int(p[4]), int(p[5])))
    print(f"sites in window: {len(rows)}")

    fig, axes = plt.subplots(2, 1, figsize=(8.2, 4.4), dpi=200, sharex=True,
                             gridspec_kw={"hspace": 0.32})
    for ax, (label, ncol, xcol, color) in zip(
            axes, (("血清培养（toSerum）", 4, 5, PRIMARY),
                   ("2i 培养（to2i）", 2, 3, WARN))):
        # 逐位点条形：高度=甲基化比例，底宽按覆盖示意
        for pos, n2i, x2i, nse, xse in rows:
            n, x = (n2i, x2i) if ncol == 2 else (nse, xse)
            pct = 100 * x / n if n else 0
            ax.bar(pos, pct, width=22, color=color, alpha=0.9, zorder=3)
            # 覆盖深度：底部灰色刻度线（按 log 比例，仅示意深度）
            import math
            cov_h = min(1.0, math.log10(n + 1) / math.log10(200)) * 9
            ax.bar(pos, -cov_h, width=22, color=MUTED, alpha=0.45, zorder=2)
        ax.set_ylim(-12, 104)
        ax.set_yticks([0, 50, 100])
        ax.set_yticklabels(["0", "50", "100%"], fontsize=7.5, color=MUTED)
        ax.set_ylabel(label, fontsize=9, color=MUTED)
        ax.axhline(0, color=MUTED, lw=0.7)
        for sp in ("top", "right", "left"):
            ax.spines[sp].set_visible(False)
        ax.tick_params(labelsize=7.5, colors=MUTED)
        # DMR 阴影
        ax.axvspan(DS, DE, color=FILL, zorder=1)

    axes[1].set_xlabel(f"{CHROM} 位置（mm9）", fontsize=9, color=MUTED)
    axes[0].set_title("DMR（DSS callDMR：21 个 CpG，组间差 85 个百分点）",
                      fontsize=9, color=PRIMARY, pad=6)
    axes[0].annotate("条形=逐位点甲基化比例；条形下方灰色深度=覆盖",
                     xy=(0.995, 0.06), xycoords="axes fraction", ha="right",
                     fontsize=7.5, color=MUTED)
    fig.savefig(OUT, bbox_inches="tight")
    print("written", OUT)


if __name__ == "__main__":
    main()
