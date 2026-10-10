"""FIG-A2：ATAC-seq 实测片段长度分布（真实数据绘图）。

数据：GSE101670 SRR5852294（Irf8+/+ rep1）全深度 BAM 的 TLEN 分布，
由 samtools view | awk 生成两列 TSV（长度、片段数）。
运行：python3 scripts/figures/ch06/gen_fragment_dist.py <fragment_dist.txt>
输出：assets/07-chip-seq-and-atac-seq/018-fragment-dist-real.png
"""

import sys
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "assets" / "07-chip-seq-and-atac-seq" / "018-fragment-dist-real.png"

PRIMARY = "#186254"
MUTED = "#6b7280"
FILL = "#e8f4f1"
WARN = "#b45309"

for f in ("PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", "Noto Sans CJK SC"):
    if any(f.lower() in x.name.lower() for x in font_manager.fontManager.ttflist):
        plt.rcParams["font.family"] = f
        break
plt.rcParams["axes.unicode_minus"] = False


def main(data_path):
    xs, ys = [], []
    with open(data_path) as fh:
        for line in fh:
            a = line.split()
            if len(a) != 2:
                continue
            x, y = int(a[0]), int(a[1])
            if 0 < x <= 700:  # 展示到 700 bp，覆盖 NFR 与前几个核小体峰
                xs.append(x)
                ys.append(y)
    total = sum(ys)
    fig, ax = plt.subplots(figsize=(7.6, 3.6), dpi=200)
    ax.fill_between(xs, ys, color=FILL, zorder=1)
    ax.plot(xs, ys, color=PRIMARY, lw=1.8, zorder=2)
    peak_notes = [(38, "NFR（<100 bp）"), (185, "单核小体（~200 bp）"), (385, "双核小体（~400 bp）")]
    ymax = max(ys)
    for x, label in peak_notes:
        # 在各峰附近取窗口最大值作标注锚点
        win = [yv for xv, yv in zip(xs, ys) if abs(xv - x) <= 25]
        if not win:
            continue
        py = max(win)
        ax.annotate(label, xy=(x, py), xytext=(x + 26, py + ymax * 0.06),
                    fontsize=8.5, color=WARN,
                    arrowprops=dict(arrowstyle="-", color=WARN, lw=0.8))
    ax.set_xlabel("插入片段长度（bp）", fontsize=9, color=MUTED)
    ax.set_ylabel("片段数", fontsize=9, color=MUTED)
    ax.set_xlim(0, 700)
    ax.set_ylim(0, ymax * 1.12)
    ax.spines[["top", "right"]].set_visible(False)
    ax.spines[["left", "bottom"]].set_color(MUTED)
    ax.tick_params(colors=MUTED, labelsize=8)
    ax.set_title(f"ATAC-seq 实测片段长度分布（SRR5852294，去重后 {total:,} 个片段）",
                 fontsize=10, color="#333333")
    fig.tight_layout()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT)
    print("written:", OUT.name)


if __name__ == "__main__":
    main(sys.argv[1])
