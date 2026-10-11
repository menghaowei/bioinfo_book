"""可复现的 IGV 风格教学示意，非真实 IGV 截图。

灰色窄 reads、末端方向箭头及配对连接线；覆盖度从绘出的 reads 计算。
运行 python3 scripts/figures/ch04/gen_igv.py。
"""
from common import (Svg, save, COLOR_PRIMARY, COLOR_FILL, COLOR_TEXT,
                    COLOR_MUTED, COLOR_LINE, COLOR_WARN, COLOR_WARN_FILL)


def read_arrow(s, x1, x2, y, direction, h=11, fill="#9ca3af"):
    tip = min(8, (x2-x1)/4)
    if direction == "+":
        pts = [(x1,y-h/2),(x2-tip,y-h/2),(x2,y),(x2-tip,y+h/2),(x1,y+h/2)]
    else:
        pts = [(x2,y-h/2),(x1+tip,y-h/2),(x1,y),(x1+tip,y+h/2),(x2,y+h/2)]
    points = " ".join(f"{x:.2f},{yy:.2f}" for x,yy in pts)
    s.add(f"<polygon points='{points}' fill='{fill}'/>")


def fig_tlen():
    left, right_start, cigar_ref_span = 10946, 11123, 145
    right_end = right_start + cigar_ref_span - 1
    span = right_end - left + 1
    assert right_end == 11267 and span == 322
    s = Svg(640, 360, "TLEN：一对 reads 的外侧跨度",
            "左端起点10946，右端read起点11123、CIGAR为145M，最后一个碱基11267。"
            "跨度11267−10946+1=322；左端TLEN+322，右端−322。左端read长度仅示意。")
    s.text(320, 32, "TLEN：从最左端到最右端", mono=False, size=21, weight="bold", anchor="middle")
    px = lambda p: 50 + (p-left)*540/span
    axis_y = 78
    s.line(40, axis_y, 600, axis_y, stroke=COLOR_LINE)
    for pos in (left, right_start, right_end):
        x = px(pos)
        s.line(x, axis_y-5, x, axis_y+6)
        s.text(x, axis_y+29, str(pos), size=19, anchor="middle")
        s.line(x, axis_y+38, x, 134, dash="3 4")
    # Mate length is not present in the source SAM record: this width is illustrative.
    up_end = px(left) + 222
    down_x, end_x = px(right_start), px(right_end+1)
    s.text(58, 153, "左端 read（+链）", mono=False, size=17)
    s.text(down_x+8, 153, "右端 read（−链，145M）", mono=False, size=16)
    s.line(up_end, 180, down_x, 180, stroke=COLOR_LINE, sw=1.2)
    read_arrow(s, px(left), up_end, 180, "+", h=18)
    read_arrow(s, down_x, end_x, 180, "-", h=18)
    s.text(158, 217, "TLEN = +322", size=19, anchor="middle", fill=COLOR_PRIMARY, weight="bold")
    s.text((down_x+end_x)/2, 217, "TLEN = −322", size=19, anchor="middle", fill=COLOR_PRIMARY, weight="bold")
    for x in (px(left), end_x):
        s.line(x, 195, x, 248, dash="3 4")
    s.line(px(left), 246, end_x, 246, stroke=COLOR_PRIMARY, sw=2)
    s.line(px(left), 238, px(left), 254, stroke=COLOR_PRIMARY, sw=2)
    s.line(end_x, 238, end_x, 254, stroke=COLOR_PRIMARY, sw=2)
    s.text(320, 281, "11267 − 10946 + 1 = 322 bp", size=21, anchor="middle", fill=COLOR_PRIMARY, weight="bold")
    s.text(320, 317, "右端最后一个碱基：11123 + 145 − 1 = 11267", mono=False, size=16, anchor="middle")
    s.text(320, 342, "坐标为 1-based 闭区间；左端 read 的长度仅作示意。", mono=False, size=15, anchor="middle", fill=COLOR_MUTED)
    save("tlen-calculation", s)


BACKGROUND_PAIRS = [(10,90,175,255), (30,110,225,305),
                    (85,165,260,340), (120,200,300,380)]
DUPLICATE_PAIR = (75,145,235,305)


def coverage(pairs):
    return [sum(a <= x < b or c <= x < d for a,b,c,d in pairs) for x in range(400)]


def _pileup(s, top, pairs, after=False):
    x0, scale, baseline, ymax = 74, 1.23, top+100, 10
    px = lambda v: x0+v*scale
    cov = coverage(pairs)
    assert max(cov) <= ymax
    for v in (0, 5, 10):
        y = baseline-v*5
        s.line(x0-5, y, px(400), y, stroke="#dde2df", sw=.8)
        s.text(x0-12, y+5, str(v), size=13, anchor="end", fill=COLOR_MUTED)
    s.text(24, top+75, "覆盖", mono=False, size=13, fill=COLOR_MUTED)
    points = [(px(0),baseline)]
    for x,n in enumerate(cov):
        points.extend([(px(x),baseline-n*5),(px(x+1),baseline-n*5)])
    points.append((px(400),baseline))
    s.add("<polygon points='"+" ".join(f"{x:.1f},{y:.1f}" for x,y in points)+"' fill='#9ca3af' opacity='.65'/>")
    for pos in (0,100,200,300,400):
        s.text(px(pos), baseline+21, str(pos), size=13, anchor="middle", fill=COLOR_MUTED)
    row0 = baseline+40
    # Highlight the known synthetic PCR family. These are read pairs, not genomic repeats.
    box_y = row0+4*12-8
    s.rect(px(75)-5, box_y, (305-75)*scale+10, (len(pairs)-4)*12+1,
           fill=COLOR_FILL if after else COLOR_WARN_FILL,
           stroke=COLOR_PRIMARY if after else COLOR_WARN, sw=1.6, dash="5 4")
    for row,(a,b,c,d) in enumerate(pairs):
        y = row0+row*12
        s.line(px(b), y, px(c), y, stroke=COLOR_LINE, sw=.8)
        read_arrow(s, px(a), px(b), y, "+", h=9)
        read_arrow(s, px(c), px(d), y, "-", h=9)
    return cov


def fig_pcr_duplicates():
    before = BACKGROUND_PAIRS + [DUPLICATE_PAIR]*6
    after = BACKGROUND_PAIRS + [DUPLICATE_PAIR]
    s = Svg(600, 660, "PCR 重复与覆盖度：过滤前后对照",
            "自绘IGV风格示意。上：4对独立片段加1个片段的6份PCR拷贝，共10对reads；"
            "下：重复组标记并过滤后保留1份，共5对。两图坐标和覆盖度刻度相同。")
    s.text(300, 30, "PCR 重复会抬高表观覆盖", size=21, mono=False, weight="bold", anchor="middle")
    s.text(24, 63, "A  过滤前：10 对 reads", size=18, mono=False, weight="bold")
    a = _pileup(s, 62, before)
    s.text(300, 337, "框内 6 对端点相同：示例中来自同一个原始片段", mono=False, size=16, anchor="middle", fill=COLOR_WARN)
    s.line(24, 359, 576, 359, stroke=COLOR_LINE)
    s.text(24, 389, "B  标记并过滤后：5 对 reads", size=18, mono=False, weight="bold")
    b = _pileup(s, 388, after, after=True)
    assert all(x >= y for x,y in zip(a,b))
    assert sum(a) == sum((b-a)+(d-c) for a,b,c,d in before)
    assert sum(b) == sum((b-a)+(d-c) for a,b,c,d in after)
    s.text(300, 617, "同端点组保留 1 份，其他独立片段保留。", mono=False, size=16, anchor="middle", fill=COLOR_PRIMARY)
    s.text(300, 644, "IGV 风格示意；横轴为同一区域的示意坐标（bp）。", mono=False, size=14, anchor="middle", fill=COLOR_MUTED)
    save("pcr-duplicate-pileup", s)


if __name__ == "__main__":
    fig_tlen()
    fig_pcr_duplicates()
