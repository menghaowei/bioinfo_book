"""双序列比对四图：评分、练习表、NW、SW。

运行 python3 scripts/figures/ch04/gen_pairwise.py。
矩阵、全部最优来源和回溯均由程序求得。底色先画；数值居中，
小来源箭头放右上；格间回溯箭头避开数值，两种箭头在空间和颜色上分开。
"""
import math

from common import (Svg, save, COLOR_TEXT, COLOR_MUTED, COLOR_PRIMARY,
                    COLOR_FILL, COLOR_WARN, COLOR_LINE)

SEQ1, SEQ2, GAP = "AAGT", "AGCT", -5
CELL, X0, Y0, WIDTH = 68, 112, 112, 520


def _score(a, b):
    return 5 if a == b else -4


def _matrix(local=False):
    m = [[0] * (len(SEQ2) + 1) for _ in range(len(SEQ1) + 1)]
    if not local:
        for i in range(len(m)):
            m[i][0] = GAP * i
        for j in range(len(m[0])):
            m[0][j] = GAP * j
    for i, a in enumerate(SEQ1, 1):
        for j, b in enumerate(SEQ2, 1):
            v = [m[i-1][j-1] + _score(a, b), m[i-1][j] + GAP,
                 m[i][j-1] + GAP]
            m[i][j] = max(v + ([0] if local else []))
    return m


def _nw_matrix():
    return _matrix(False)


def _sw_matrix():
    return _matrix(True)


def _sources(mat, sw=False):
    src = [[set() for _ in row] for row in mat]
    for i in range(len(mat)):
        for j in range(len(mat[0])):
            if sw and mat[i][j] == 0:
                continue
            if i and j and mat[i-1][j-1] + _score(SEQ1[i-1], SEQ2[j-1]) == mat[i][j]:
                src[i][j].add("d")
            if i and mat[i-1][j] + GAP == mat[i][j]:
                src[i][j].add("u")
            if j and mat[i][j-1] + GAP == mat[i][j]:
                src[i][j].add("l")
    return src


def tracebacks(mat, local=False):
    """Return every best traceback; each path runs from its score to its origin."""
    src = _sources(mat, local)
    best = max(map(max, mat)) if local else mat[-1][-1]
    starts = [(i, j) for i, row in enumerate(mat) for j, v in enumerate(row)
              if v == best] if local else [(len(SEQ1), len(SEQ2))]
    paths = []

    def walk(i, j, path):
        if (local and mat[i][j] == 0) or (i == 0 and j == 0):
            paths.append(path)
            return
        for d, di, dj in [("d", -1, -1), ("u", -1, 0), ("l", 0, -1)]:
            if d in src[i][j]:
                walk(i + di, j + dj, path + [(i + di, j + dj)])
    for i, j in starts:
        walk(i, j, [(i, j)])
    return paths


def alignment(path):
    a, b = [], []
    for (i, j), (pi, pj) in zip(path, path[1:]):
        a.append(SEQ1[i-1] if pi < i else "-")
        b.append(SEQ2[j-1] if pj < j else "-")
    return "".join(reversed(a)), "".join(reversed(b))


def _arrow(s, a, b, color=COLOR_LINE, width=1.3, dashed=False, head=4):
    x1, y1 = a
    x2, y2 = b
    s.line(x1, y1, x2, y2, stroke=color, sw=width, dash="5 4" if dashed else None)
    ang = math.atan2(y2-y1, x2-x1)
    for delta in (-0.48, 0.48):
        s.line(x2, y2, x2-head*math.cos(ang+delta), y2-head*math.sin(ang+delta),
               stroke=color, sw=width)


def _node(i, j):
    return X0 + j*CELL + 34, Y0 + i*CELL + 38


def _frame(s, mat, paths=(), local=False, empty=False):
    active = {p for path in paths for p in path}
    for i in range(5):
        for j in range(5):
            fill = COLOR_FILL if (i, j) in active else ("#f1f3f2" if i == 0 or j == 0 else "white")
            s.rect(X0+j*CELL, Y0+i*CELL, CELL, CELL, fill=fill,
                   stroke=COLOR_LINE, sw=0.75, rx=0)
    s.text(X0+2.5*CELL, 69, "列：seq2", mono=False, size=16, anchor="middle", fill=COLOR_MUTED)
    s.text(24, Y0+166, "行", mono=False, size=16, fill=COLOR_MUTED)
    s.text(14, Y0+190, "seq1", size=14, fill=COLOR_MUTED)
    for k, b in enumerate("∅"+SEQ2):
        s.text(X0+k*CELL+CELL/2, Y0-12, b, size=21,
               anchor="middle", weight="bold", fill=COLOR_PRIMARY)
    for k, b in enumerate("∅"+SEQ1):
        s.text(X0-25, Y0+k*CELL+45, b, size=21,
               anchor="middle", weight="bold", fill=COLOR_PRIMARY)

    # Shared path edges are solid. Only the second solution's unique edges are dashed.
    edges_a = set(zip(paths[0], paths[0][1:])) if paths else set()
    drawn = set()
    for index, path in enumerate(paths):
        for edge in zip(path, path[1:]):
            if edge in drawn:
                continue
            drawn.add(edge)
            a, b = _node(*edge[0]), _node(*edge[1])
            length = math.dist(a, b)
            u = ((b[0]-a[0])/length, (b[1]-a[1])/length)
            start = (a[0]+28*u[0], a[1]+28*u[1])
            end = (b[0]-28*u[0], b[1]-28*u[1])
            _arrow(s, start, end, COLOR_PRIMARY, 2.6,
                   dashed=index == 1 and edge not in edges_a, head=6)

    sources = _sources(mat, local)
    for i in range(5):
        for j in range(5):
            if empty and i and j:
                continue
            value = str(mat[i][j]).replace("-", "−")
            s.text(X0+j*CELL+34, Y0+i*CELL+45, value, size=22,
                   anchor="middle", weight="bold" if (i, j) in active else "normal",
                   fill=COLOR_PRIMARY if (i, j) in active else COLOR_TEXT)
            if i and j and not empty:
                cx, cy = X0+j*CELL+58, Y0+i*CELL+14
                for d, dx, dy in [("d", -1, -1), ("u", 0, -1), ("l", -1, 0)]:
                    if d in sources[i][j]:
                        _arrow(s, (cx, cy), (cx+dx*9, cy+dy*9), head=3.7)
    for path in paths:
        i, j = path[0]
        s.rect(X0+j*CELL+2, Y0+i*CELL+2, CELL-4, CELL-4,
               stroke=COLOR_PRIMARY, sw=2, rx=0)


def fig_scoring_matrix():
    s = Svg(430, 422, "双序列比对的评分规则", "相同碱基+5，不同碱基−4，每个空位−5。")
    s.text(215, 31, "双序列比对的评分规则", mono=False, size=20, weight="bold", anchor="middle")
    x0, y0, c = 103, 79, 58
    for k, base in enumerate("AGCT"):
        s.text(x0+(k+.5)*c, 65, base, size=22, anchor="middle", weight="bold", fill=COLOR_PRIMARY)
        s.text(79, y0+k*c+37, base, size=22, anchor="middle", weight="bold", fill=COLOR_PRIMARY)
    for i, a in enumerate("AGCT"):
        for j, b in enumerate("AGCT"):
            match = a == b
            s.rect(x0+j*c, y0+i*c, c, c, fill=COLOR_FILL if match else "white",
                   stroke=COLOR_LINE, sw=.8, rx=0)
            s.text(x0+(j+.5)*c, y0+i*c+37, "+5" if match else "−4", size=23,
                   anchor="middle", fill=COLOR_PRIMARY if match else COLOR_WARN,
                   weight="bold" if match else "normal")
    s.text(215, 346, "相同碱基 +5  ·  不同碱基 −4", size=17, mono=False, anchor="middle")
    s.rect(76, 366, 278, 38, fill=COLOR_FILL, sw=0)
    s.text(215, 392, "每个空位 −5（线性罚分）", size=17, mono=False, anchor="middle", fill=COLOR_PRIMARY)
    save("pairwise-01-scoring-matrix", s)


def fig_empty_grid():
    s = Svg(WIDTH, 542, "待填写的动态规划表", "seq1=AAGT，seq2=AGCT。灰格按NW初始化；做SW时将灰格改为0。")
    s.text(WIDTH/2, 32, "动态规划练习表", mono=False, size=21, weight="bold", anchor="middle")
    _frame(s, _nw_matrix(), empty=True)
    s.text(260, 485, "灰格：全局比对的初始化值", mono=False, size=17, anchor="middle")
    s.text(260, 514, "练习局部比对时，先将灰格全部改为 0。", mono=False, size=16,
           anchor="middle", fill=COLOR_MUTED)
    save("pairwise-02-empty-grid", s)


def _result_figure(local):
    mat = _matrix(local)
    paths = tracebacks(mat, local)
    assert len(paths) == 2
    # Keep A as the leading-gap NW solution and as the shorter SW solution.
    paths.sort(key=lambda p: (len(p), alignment(p)[1]))
    best = max(map(max, mat)) if local else mat[-1][-1]
    assert best == (10 if local else 5)
    expected = {("AG", "AG"), ("AG-T", "AGCT")} if local else {
        ("AAG-T", "-AGCT"), ("AAG-T", "A-GCT")}
    assert {alignment(p) for p in paths} == expected
    for p in paths:
        a, b = alignment(p)
        assert sum(GAP if "-" in (x, y) else _score(x, y) for x, y in zip(a, b)) == best
    title = "Smith–Waterman 局部比对" if local else "Needleman–Wunsch 全局比对"
    s = Svg(WIDTH, 668, title, "灰色小箭头显示全部最优来源，绿色连线为回溯。A实线，B独有段虚线，共用段实线。两个并列最优比对得分均为"+str(best)+"。")
    s.text(WIDTH/2, 32, title, mono=False, size=20, weight="bold", anchor="middle")
    _frame(s, mat, paths, local)
    s.text(260, 480, "从加框格回溯，遇到 0 停止" if local else "从右下角回溯到左上角的 0",
           mono=False, size=17, anchor="middle", weight="bold", fill=COLOR_PRIMARY)
    for k, p in enumerate(paths):
        x = 24+k*248
        s.rect(x, 499, 224, 99, fill="#f1f3f2", stroke="none")
        s.line(x+13, 518, x+41, 518, stroke=COLOR_PRIMARY, sw=2.6, dash="5 4" if k else None)
        s.text(x+51, 523, f"{'AB'[k]}  得分 {best}", mono=False, size=16, weight="bold")
        a, b = alignment(p)
        s.text(x+112, 553, " ".join(a), size=20, anchor="middle", fill=COLOR_PRIMARY, weight="bold")
        s.text(x+112, 581, " ".join(b), size=20, anchor="middle", fill=COLOR_PRIMARY, weight="bold")
    s.text(260, 625, "灰色小箭头：本格的全部最优来源", mono=False, size=16, anchor="middle", fill=COLOR_MUTED)
    s.text(260, 650, "绿色回溯：A 实线 · B 独有段虚线 · 共用段实线", mono=False, size=15, anchor="middle", fill=COLOR_PRIMARY)
    save("pairwise-04-sw-matrix" if local else "pairwise-03-nw-matrix", s)


def fig_nw_matrix():
    _result_figure(False)


def fig_sw_matrix():
    _result_figure(True)


if __name__ == "__main__":
    fig_scoring_matrix()
    fig_empty_grid()
    fig_nw_matrix()
    fig_sw_matrix()
