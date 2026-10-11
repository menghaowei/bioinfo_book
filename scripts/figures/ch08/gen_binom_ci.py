"""FIG：二项比例置信区间演示（覆盖深度如何决定比例的可信度）。

数学计算图（Clopper–Pearson 精确区间），非实验数据。
运行：python3 gen_binom_ci.py
输出：assets/09-base-imbalanced-sequencing/binom-ci-demo.png
"""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from scipy import stats

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "assets" / "09-base-imbalanced-sequencing" / "binom-ci-demo.png"

PRIMARY = "#186254"
MUTED = "#6b7280"
FILL = "#e8f4f1"
WARN = "#b45309"

for f in ("PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", "Noto Sans CJK SC"):
    if any(f.lower() in x.name.lower() for x in font_manager.fontManager.ttflist):
        plt.rcParams["font.family"] = f
        break
plt.rcParams["axes.unicode_minus"] = False


def cp_interval(x, n, a=0.05):
    lo = 0.0 if x == 0 else stats.beta.ppf(a / 2, x, n - x + 1)
    hi = 1.0 if x == n else stats.beta.ppf(1 - a / 2, x + 1, n - x)
    return lo, hi


def main():
    fig, ax = plt.subplots(figsize=(7.6, 3.7), dpi=200)
    cases = [
        (5, 0, "N=5, X=0"),
        (5, 3, "N=5, X=3"),
        (30, 0, "N=30, X=0"),
        (30, 18, "N=30, X=18"),
        (100, 60, "N=100, X=60"),
    ]
    for i, (n, x, lab) in enumerate(cases):
        lo, hi = cp_interval(x, n)
        p = x / n
        y = len(cases) - 1 - i
        color = WARN if (hi - lo) > 0.3 else PRIMARY
        ax.plot([lo, hi], [y, y], color=color, lw=4, solid_capstyle="round")
        ax.plot([p], [y], marker="o", ms=5, color="#ffffff",
                markeredgecolor=color, markeredgewidth=1.6, zorder=3)
        ax.text(hi + 0.03, y, f"{lab}：区间 [{lo:.2f}, {hi:.2f}]",
                va="center", fontsize=9, color=MUTED)
    ax.set_yticks([])
    ax.set_xlim(-0.06, 1.06)
    ax.set_ylim(-0.7, len(cases) - 0.1)
    ax.set_xlabel("位点甲基化比例 p 的 95% 置信区间（Clopper–Pearson）", fontsize=9, color=MUTED)
    ax.text(0.02, 0.97, "同样估计 0 或 60%，覆盖越高区间越窄；橙色区间宽度超过 0.3，比例几乎没有信息量",
            fontsize=8.5, color=WARN, va="top", transform=ax.transAxes)
    ax.axvline(0, color=MUTED, lw=0.6, ls=":")
    ax.axvline(1, color=MUTED, lw=0.6, ls=":")
    for sp in ("top", "right", "left"):
        ax.spines[sp].set_visible(False)
    ax.tick_params(labelsize=8, colors=MUTED)
    fig.tight_layout()
    fig.savefig(OUT, bbox_inches="tight")
    print("written", OUT)


if __name__ == "__main__":
    main()
