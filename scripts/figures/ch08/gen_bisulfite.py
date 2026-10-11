"""从单个位点解释亚硫酸盐处理、PCR读数和C/T计数。

示例是同一参考C位点、不同原始分子的有效观测，仅展示正链；
完全转化及5hmC的解释边界在正文图注中说明。
运行 python3 scripts/figures/ch08/gen_bisulfite.py。
"""
from common import Svg, COLOR_TEXT, COLOR_MUTED, COLOR_PRIMARY, COLOR_FILL, COLOR_WARN, COLOR_WARN_FILL, COLOR_LINE


def gen_bisulfite_chemistry():
    s = Svg(600, 654, "亚硫酸盐处理如何变成 C/T 读数",
            "上：未甲基化C在处理后变U，PCR和测序后读作T；5mC经处理保留，测序读作C。"
            "下：同一参考C位点的5个独立分子观测，3条C、2条T，比例估计60%。")
    s.text(300, 31, "从化学处理到测序读数", mono=False, size=22, weight="bold", anchor="middle")
    for cx, first, second in [(184,"原始 DNA",""),(346,"亚硫酸盐","处理后"),(508,"PCR 与","测序后")]:
        s.text(cx, 63, first, mono=False, size=16, anchor="middle", fill=COLOR_MUTED)
        if second:
            s.text(cx, 84, second, mono=False, size=16, anchor="middle", fill=COLOR_MUTED)
    for cy, label, small, letters, color, fill in [
        (136,"未甲基化","C",["C","U","T"],COLOR_WARN,COLOR_WARN_FILL),
        (244,"甲基化","5mC",["5mC","5mC","C"],COLOR_PRIMARY,COLOR_FILL),
    ]:
        s.text(25, cy-6, label, mono=False, size=17, weight="bold", fill=color)
        s.text(25, cy+20, small, size=19, fill=color)
        for cx, symbol in zip((184,346,508),letters):
            s.rect(cx-46,cy-35,92,70,fill=fill,stroke=color,sw=1.1,rx=8)
            s.text(cx,cy+11,symbol,size=31,weight="bold",anchor="middle",fill=color)
        for a,b in [(230,300),(392,462)]:
            s.arrow(a+10,cy,b-10,cy,stroke=color,sw=2)
        s.text(265,cy+28,"脱氨" if small=="C" else "保留",mono=False,size=14,anchor="middle",fill=color)
        s.text(427,cy+28,"读作",mono=False,size=14,anchor="middle",fill=color)
    s.line(24,303,576,303,stroke=COLOR_LINE)
    s.text(24,336,"同一个参考 C 位点，可以读到 C 或 T",mono=False,size=20,weight="bold")
    seq = "ATCGTA"
    xs = [169+44*i for i in range(len(seq))]
    ys = [379,420,453,486,519,552]
    reads = [seq,seq,seq,seq[:2]+"T"+seq[3:],seq[:2]+"T"+seq[3:]]
    assert sum(row[2]=="C" for row in reads)==3 and sum(row[2]=="T" for row in reads)==2
    for row,(y,text) in enumerate(zip(ys,[seq]+reads)):
        s.text(40,y,"参考" if row==0 else f"read {row}",mono=False,size=16,fill=COLOR_MUTED)
        base=text[2]
        color=COLOR_TEXT if row==0 else (COLOR_PRIMARY if base=="C" else COLOR_WARN)
        fill="#f1f3f2" if row==0 else (COLOR_FILL if base=="C" else COLOR_WARN_FILL)
        s.rect(xs[2]-16,y-23,32,29,fill=fill,stroke=color,sw=1,rx=4)
        for i,ch in enumerate(text):
            s.text(xs[i],y,ch,size=22,anchor="middle",fill=color if i==2 else COLOR_MUTED,
                   weight="bold" if i==2 else "normal")
    s.text(442,459,"3 条读作 C",mono=False,size=16,weight="bold",fill=COLOR_PRIMARY)
    s.text(442,536,"2 条读作 T",mono=False,size=16,weight="bold",fill=COLOR_WARN)
    s.rect(68,578,464,40,fill=COLOR_FILL,stroke="none",rx=6)
    s.text(300,605,"比例估计：3 / (3 + 2) = 60%",mono=False,size=20,weight="bold",fill=COLOR_PRIMARY,anchor="middle")
    s.text(300,641,"5 条 reads 来自不同原始分子；此处仅展示正链。",mono=False,size=15,anchor="middle",fill=COLOR_MUTED)
    return s


if __name__ == "__main__":
    from pathlib import Path
    out = Path(__file__).resolve().parents[3] / "assets/09-base-imbalanced-sequencing/bisulfite-conversion-principle.svg"
    out.write_text(gen_bisulfite_chemistry().render(), encoding="utf-8")
    print("written", out)
