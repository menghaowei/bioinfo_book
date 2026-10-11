"""双侧95% Clopper–Pearson：具体计数→点估计与区间。

数学计算图，非实验数据；独立二项抽样，不涵盖转化误差或生物学差异。
运行：python3 scripts/figures/ch08/gen_binom_ci.py
"""
import json
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from scipy import stats

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "assets" / "09-base-imbalanced-sequencing" / "binom-ci-demo.png"
PRIMARY, MUTED, PAGE = "#186254", "#6b7280", "#fcfcf9"
for name in ("PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", "Noto Sans CJK SC", "Arial Unicode MS"):
    if any(name.lower() == x.name.lower() for x in font_manager.fontManager.ttflist):
        plt.rcParams["font.family"] = name
        break
plt.rcParams["axes.unicode_minus"] = False


def cp_interval(x, n, a=0.05):
    lo = 0.0 if x == 0 else stats.beta.ppf(a/2, x, n-x+1)
    hi = 1.0 if x == n else stats.beta.ppf(1-a/2, x+1, n-x)
    return float(lo), float(hi)


def panel(fig, bounds, cases, reference):
    ax = fig.add_axes(bounds, facecolor=PAGE)
    ax.set_xlim(-2,102)
    ax.set_ylim(-.45,len(cases)-.25)
    ax.set_yticks([])
    ax.set_xticks(range(0,101,20),[f"{x}%" for x in range(0,101,20)])
    ax.tick_params(axis="x",labelsize=11,colors=MUTED,length=3)
    for k in ("top","left","right"):
        ax.spines[k].set_visible(False)
    ax.spines["bottom"].set_color("#9ca3af")
    if 0 < reference < 1:
        ax.axvline(reference*100,color="#9ca3af",ls="--",lw=.8,zorder=0)
    values = []
    for index,(x,n) in enumerate(cases):
        y = len(cases)-1-index
        lo,hi = cp_interval(x,n)
        checked=stats.binomtest(x,n).proportion_ci(confidence_level=.95,method="exact")
        assert abs(lo-checked.low)<1e-10 and abs(hi-checked.high)<1e-10
        ax.plot([lo*100,hi*100],[y,y],color=PRIMARY,lw=3,solid_capstyle="round")
        ax.plot([x/n*100],[y],"o",ms=7,color=PRIMARY,mec=PAGE,mew=1,zorder=3)
        ax.text(0,y+.24,f"{x} 条 C / {n} 条覆盖",fontsize=12.5,color="#333333",va="bottom")
        ax.text(100,y+.24,f"{lo:.1%}–{hi:.1%}",fontsize=12,color=MUTED,ha="right",va="bottom")
        values.append({"C":x,"coverage":n,"estimate":x/n,"lower":lo,"upper":hi})
    ax.set_xlabel("甲基化比例",fontsize=12,color=MUTED,labelpad=7)
    return values


def main():
    fig=plt.figure(figsize=(6,7.6),dpi=220,facecolor=PAGE)
    fig.text(.075,.965,"A  同样估计为 60%，覆盖越高区间越窄",fontsize=14,weight="bold",color=PRIMARY,va="top")
    fig.text(.075,.92,"圆点＝估计比例    横线＝95% 置信区间",fontsize=12,color=MUTED)
    values=panel(fig,[.10,.55,.82,.31],[(3,5),(30,50),(300,500)],.6)
    fig.text(.075,.438,"B  观察到 0 条 C，也不能断定比例为 0",fontsize=14,weight="bold",color=PRIMARY,va="top")
    values+=panel(fig,[.10,.17,.82,.21],[(0,5),(0,30)],0)
    fig.text(.075,.067,"每行按 C 计数与有效覆盖计算双侧精确区间。",fontsize=11,color=MUTED)
    fig.text(.075,.036,"低覆盖时区间更宽，估计的不确定性更大。",fontsize=11,color=MUTED)
    fig.savefig(OUT,facecolor=PAGE)
    plt.close(fig)
    print(json.dumps({"output":str(OUT),"method":"two-sided 95% Clopper–Pearson","cases":values},ensure_ascii=False,indent=2))


if __name__=="__main__":
    main()
