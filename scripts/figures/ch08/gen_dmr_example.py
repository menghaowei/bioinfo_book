"""FIG：DSS 检出的 DMR 示例区域（真实数据）。

数据：.ch08-data/wgbss/dmr_region.tsv（export_dmr_region.R 导出）。
运行：python3 gen_dmr_example.py
输出：assets/09-base-imbalanced-sequencing/dmr-example-real.png
"""

import re
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager

ROOT = Path(__file__).resolve().parents[3]
DATA = ROOT.parent / ".ch08-data" / "wgbss"
OUT = ROOT / "assets" / "09-base-imbalanced-sequencing" / "dmr-example-real.png"

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
    summ = {}
    for line in open(DATA / "dmr_summary.txt"):
        parts = line.rstrip("\n").split("\t")
        summ[parts[0]] = parts[1:]
    chosen = summ["chosen"]  # chr:start-end nCG=.. diff=..
    m = re.match(r"(\w+):(\d+)-(\d+)\s+nCG=(\d+)\s+diff=(-?[\d.]+)", " ".join(summ["chosen"]))
    chrom, ds, de, ncg, diff = m.group(1), int(m.group(2)), int(m.group(3)), m.group(4), float(m.group(5))

    pos, mu1, mu2, p = [], [], [], []
    with open(DATA / "dmr_region.tsv") as fh:
        fh.readline()
        for line in fh:
            a, b, c, d = line.split("\t")
            pos.append(int(a)); mu1.append(float(b)); mu2.append(float(c)); p.append(float(d))

    fig, ax = plt.subplots(figsize=(7.8, 3.6), dpi=200)
    ax.axvspan(ds, de, color=FILL, zorder=0)
    ax.plot(pos, [x * 100 for x in mu1], "o-", color=PRIMARY, ms=3.2, lw=1.2,
            label="血清培养（toSerum）", zorder=3)
    ax.plot(pos, [x * 100 for x in mu2], "o-", color=WARN, ms=3.2, lw=1.2,
            label="2i 培养（to2i）", zorder=3)
    ax.annotate("DMR", xy=((ds + de) / 2, 96), fontsize=10, color=PRIMARY,
                ha="center", weight="bold")
    ax.set_xlabel(f"{chrom} 位置（bp，mm9）", fontsize=9, color=MUTED)
    ax.set_ylabel("平滑甲基化比例（%）", fontsize=9, color=MUTED)
    ax.set_ylim(-4, 104)
    ax.legend(fontsize=8.5, frameon=False, loc="lower left")
    ax.text(0.99, 0.04,
            f"DSS callDMR：{ncg} 个 CpG，差 {abs(diff)*100:.0f} 个百分点",
            fontsize=8.5, color=MUTED, ha="right", transform=ax.transAxes)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    ax.tick_params(labelsize=8, colors=MUTED)
    fig.tight_layout()
    fig.savefig(OUT, bbox_inches="tight")
    print("written", OUT)


if __name__ == "__main__":
    main()
