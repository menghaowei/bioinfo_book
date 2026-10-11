"""FIG：to2i 子集实测 M-bias 曲线（真实数据绘图）。

数据：.ch08-data/wgbss/meth_extract/to2i_dedup.deduplicated.M-bias.txt
运行：python3 gen_mbias.py
输出：assets/09-base-imbalanced-sequencing/mbias-real.png
"""

import re
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager

ROOT = Path(__file__).resolve().parents[3]
DATA = ROOT.parent / ".ch08-data" / "wgbss" / "meth_extract" / "to2i_dedup.deduplicated.M-bias.txt"
OUT = ROOT / "assets" / "09-base-imbalanced-sequencing" / "mbias-real.png"

PRIMARY = "#186254"
MUTED = "#6b7280"
FILL = "#e8f4f1"
WARN = "#b45309"

for f in ("PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", "Noto Sans CJK SC"):
    if any(f.lower() in x.name.lower() for x in font_manager.fontManager.ttflist):
        plt.rcParams["font.family"] = f
        break
plt.rcParams["axes.unicode_minus"] = False


def load(path):
    sections = {}
    cur = None
    for line in open(path):
        m = re.match(r"(\w+) context \(R(\d)\)", line)
        if m:
            cur = f"{m.group(1)}_R{m.group(2)}"
            sections[cur] = []
            continue
        if cur and line[:1].isdigit():
            p, mc, uc, pct, cov = line.split()
            sections[cur].append((int(p), int(mc), int(uc), int(cov)))
    return sections


def main():
    sec = load(DATA)
    fig, axes = plt.subplots(1, 2, figsize=(8.6, 3.5), dpi=200, sharey=True)
    for ax, read in zip(axes, ("R1", "R2")):
        for ctx, color, lw in (("CpG", PRIMARY, 1.9), ("CHH", WARN, 1.6)):
            rows = [r for r in sec[f"{ctx}_{read}"] if r[3] >= 200]
            xs = [r[0] for r in rows]
            # 覆盖度加权滑动平均（窗口 5）抑制低覆盖抖动
            ys = []
            vals = [r[1] / (r[1] + r[2]) * 100 for r in rows]
            covs = [r[3] for r in rows]
            for i in range(len(rows)):
                lo, hi = max(0, i - 2), min(len(rows), i + 3)
                num = sum(v * c for v, c in zip(vals[lo:hi], covs[lo:hi]))
                den = sum(covs[lo:hi])
                ys.append(num / den)
            ax.plot(xs, ys, color=color, lw=lw,
                    label={"CpG": "CpG 语境（真甲基化）", "CHH": "CHH 语境（噪声地板）"}[ctx])
        ax.set_title(f"{read}", fontsize=10, color=MUTED)
        ax.set_xlabel("read 内位置（bp）", fontsize=9, color=MUTED)
        ax.set_xlim(1, 100)
    axes[0].set_ylabel("平均甲基化率（%）", fontsize=9, color=MUTED)
    axes[1].annotate("R2 前 2 bp 已被 --ignore_r2 排除\n（末端修复反应会体外改写甲基化状态）",
                     xy=(4, 6.5), xytext=(22, 13), fontsize=8.5, color=WARN,
                     arrowprops=dict(arrowstyle="->", color=WARN, lw=0.9))
    axes[0].text(0.05, 0.88, "曲线平坦 = 无需大段修剪", fontsize=9, color=PRIMARY,
                 transform=axes[0].transAxes)
    axes[0].legend(fontsize=8.5, frameon=False, loc="lower right")
    for ax in axes:
        for sp in ("top", "right"):
            ax.spines[sp].set_visible(False)
        ax.tick_params(labelsize=8, colors=MUTED)
    fig.tight_layout()
    fig.savefig(OUT, bbox_inches="tight")
    print("written", OUT)


if __name__ == "__main__":
    main()
