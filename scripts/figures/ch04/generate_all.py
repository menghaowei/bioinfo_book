"""生成第4章算法示意图 SVG（BWT、哈希表、双序列比对）。

运行：python3 scripts/figures/ch04/generate_all.py
输出：assets/04-quality-control-and-alignment/svg/*.svg

图只保留 illustration 功能：矩阵、字符、高亮与箭头；解释性文字一律放正文。
DP 表为教科书标准画法：每格标注取值来源方向箭头（对角/上/左），回溯路径加粗。
"""

import math
from common import (Svg, save, COLOR_TEXT, COLOR_MUTED, COLOR_PRIMARY,
                    COLOR_FILL, COLOR_WARN, COLOR_WARN_FILL, COLOR_LINE,
                    SIZE_SEQ, SIZE_LABEL, SIZE_TITLE, SIZE_NOTE, CHAR_W, ROW_H)

# ---------------------------------------------------------------- BWT 系列

BWT_TEXT = "ACAACG"


def rotations(t):
    n = len(t)
    return [t[i:] + t[:i] for i in range(n)]


def bwt_matrix_rows():
    rows = sorted(rotations(BWT_TEXT + "$"))
    return rows, [r[0] for r in rows], [r[-1] for r in rows]


def fig_bwt_rotations():
    rows = rotations(BWT_TEXT + "$")
    x0, y0 = 90, 66
    w, h = 520, y0 + len(rows) * ROW_H + 24
    svg = Svg(w, h, "BWT 构建第 1 步：全部循环旋转",
              "对 ACAACG$ 写出 7 个循环旋转，高亮行为原序列本身。")
    svg.text(x0, 40, "ACAACG$ 的 7 个循环旋转", mono=False, size=SIZE_TITLE, weight="bold")
    for i, r in enumerate(rows):
        y = y0 + i * ROW_H + 16
        svg.text(x0 - 34, y, str(i + 1), size=SIZE_LABEL, fill=COLOR_MUTED)
        if i == 0:
            svg.rect(x0 - 8, y - 17, (len(r) - 1) * CHAR_W + 26, 24, fill=COLOR_FILL)
        svg.seq(x0, y, r)
    save("bwt-01-rotations", svg)


def fig_bwt_sorted():
    rows, f, l = bwt_matrix_rows()
    x0, y0 = 90, 92
    w, h = 560, y0 + len(rows) * ROW_H + 24
    svg = Svg(w, h, "BWT 构建第 2 步：排序后的旋转矩阵",
              "全部循环旋转按 $<A<C<G 排序；F 列为第一列，L 列为最后一列（BWT）。")
    svg.text(x0, 40, "排序后的旋转矩阵（$ < A < C < G）", mono=False, size=SIZE_TITLE, weight="bold")
    svg.text(x0 - 2, y0 - 12, "F", weight="bold", fill=COLOR_PRIMARY)
    svg.text(x0 + (len(rows[0]) - 1) * CHAR_W + 2, y0 - 12, "L", weight="bold", fill=COLOR_WARN)
    for i, r in enumerate(rows):
        y = y0 + i * ROW_H + 16
        svg.text(x0 - 34, y, str(i + 1), size=SIZE_LABEL, fill=COLOR_MUTED)
        svg.seq(x0, y, r)
        svg.rect(x0 - 6, y - 16, 20, 22, fill=COLOR_FILL, sw=1.4)
        lx = x0 + (len(r) - 1) * CHAR_W - 4
        svg.rect(lx, y - 16, 20, 22, fill=COLOR_WARN_FILL, stroke=COLOR_WARN, sw=1.4)
    save("bwt-02-sorted-matrix", svg)


def _decode_columns(svg, x0, y0):
    rows, f, l = bwt_matrix_rows()
    fx, lx = x0 + 30, x0 + 230
    svg.text(fx, y0 - 12, "F 列", mono=False, size=SIZE_LABEL, fill=COLOR_PRIMARY, weight="bold")
    svg.text(lx, y0 - 12, "L 列", mono=False, size=SIZE_LABEL, fill=COLOR_WARN, weight="bold")
    for i, (fc, lc) in enumerate(zip(f, l)):
        y = y0 + i * ROW_H + 16
        svg.text(x0 - 20, y, str(i + 1), size=SIZE_LABEL, fill=COLOR_MUTED)
        svg.text(fx, y, fc)
        svg.text(lx, y, lc)
    return fx, lx


def _hl_f(svg, fx, y0, i):
    svg.rect(fx - 6, y0 + i * ROW_H + 0, 20, 22, fill=COLOR_FILL, sw=1.4)


def _hl_l(svg, lx, y0, i):
    svg.rect(lx - 6, y0 + i * ROW_H + 0, 20, 22,
             fill=COLOR_WARN_FILL, stroke=COLOR_WARN, sw=1.4)


def _cy(y0, i):
    return y0 + i * ROW_H + 10


def fig_bwt_decode(step):
    rows, f, l = bwt_matrix_rows()
    x0, y0 = 70, 92
    w, h = 420, y0 + 7 * ROW_H + 24
    meta = {
        1: ("第 1 步：原序列以 G 结尾", [(0, 0)]),
        2: ("第 2 步：G 前面是 C", [(6, 0), (6, 6)]),
        3: ("第 3 步：C 前面是 A", [(5, 5), (5, 6)]),
    }
    title, pairs = meta[step]
    svg = Svg(w, h, f"BWT 解码{title}",
              f"BWT解码第{step}步的LF映射：琥珀为L列来源格，绿色为F列命中格，箭头表示LF映射方向。")
    svg.text(x0, 40, title, mono=False, size=SIZE_TITLE, weight="bold")
    fx, lx = _decode_columns(svg, x0, y0)
    seen_f, seen_l = set(), set()
    for fr, lr in pairs:
        if fr not in seen_f:
            _hl_f(svg, fx, y0, fr); seen_f.add(fr)
        if lr not in seen_l:
            _hl_l(svg, lx, y0, lr); seen_l.add(lr)
    for fr, lr in pairs:
        svg.arrow(lx - 8, _cy(y0, lr), fx + 16, _cy(y0, fr), sw=1.8)
    save(f"bwt-0{step + 2}-decode-step{step}", svg)


def fig_bwt_decode_rest():
    rows, f, l = bwt_matrix_rows()
    x0, y0 = 70, 92
    w, h = 460, y0 + 7 * ROW_H + 110
    svg = Svg(w, h, "BWT 解码第 4—6 步与逆序还原",
              "继续LF映射得到GCAA、GCAAC、GCAACA；逆序即原序列ACAACG。")
    svg.text(x0, 40, "第 4—6 步：继续 LF 映射", mono=False, size=SIZE_TITLE, weight="bold")
    fx, lx = x0 + 30, x0 + 230
    steps = [(5, 2), (2, 1), (1, 4)]
    svg.text(fx, y0 - 12, "F 列", mono=False, size=SIZE_LABEL, fill=COLOR_PRIMARY, weight="bold")
    svg.text(lx, y0 - 12, "L 列", mono=False, size=SIZE_LABEL, fill=COLOR_WARN, weight="bold")
    for i, (fc, lc) in enumerate(zip(f, l)):
        y = y0 + i * ROW_H + 16
        svg.text(x0 - 20, y, str(i + 1), size=SIZE_LABEL, fill=COLOR_MUTED)
        svg.text(fx, y, fc)
        svg.text(lx, y, lc)
    badges = ["4", "5", "6"]
    for (lr, fr), bd in zip(steps, badges):
        _hl_l(svg, lx, y0, lr)
        _hl_f(svg, fx, y0, fr)
        mx = (fx + lx) / 2
        my = (_cy(y0, lr) + _cy(y0, fr)) / 2
        svg.arrow(lx - 8, _cy(y0, lr), fx + 16, _cy(y0, fr), sw=1.8)
        svg.rect(mx - 9, my - 12, 18, 18, fill="#ffffff", stroke=COLOR_PRIMARY, sw=1.2)
        svg.text(mx, my + 1, bd, size=SIZE_LABEL, weight="bold", fill=COLOR_PRIMARY, anchor="middle")
    y = y0 + 7 * ROW_H + 36
    svg.seq(x0 + 10, y, "GCAACA")
    svg.arrow(x0 + 10 + 6 * CHAR_W + 8, y - 5, x0 + 10 + 6 * CHAR_W + 58, y - 5)
    svg.text(x0 + 10 + 6 * CHAR_W + 33, y - 12, "逆序", mono=False, size=SIZE_NOTE,
             fill=COLOR_MUTED, anchor="middle")
    svg.seq(x0 + 10 + 6 * CHAR_W + 72, y, "ACAACG", weight="bold", fill=COLOR_PRIMARY)
    save("bwt-06-decode-steps4-6", svg)


# ---------------------------------------------------------------- 哈希表系列

def fig_hash_encoding():
    seq = "ATGCT"
    digits = "01321"
    powers = ["4⁴", "4³", "4²", "4¹", "4⁰"]
    terms = ["0×256", "1×64", "3×16", "2×4", "1×1"]
    x0, y0 = 90, 78
    w, h = 640, 280
    svg = Svg(w, h, "碱基的四进制编码",
              "把 A、T、G、C 分别编码为 0、1、3、2，按最左位权值最高计算，ATGCT 的关键码为 121。")
    svg.text(x0, 42, "把碱基编码成数字：A→0，T→1，G→3，C→2", mono=False,
             size=SIZE_TITLE, weight="bold")
    for i, ch in enumerate(seq):
        x = x0 + i * 100
        svg.rect(x - 14, y0 - 24, 56, 52, fill=COLOR_FILL if i == 0 else "none")
        svg.text(x + 14, y0, ch, size=22, weight="bold", anchor="middle")
        svg.text(x + 14, y0 + 24, digits[i], fill=COLOR_PRIMARY, weight="bold", anchor="middle")
        svg.text(x + 14, y0 + 48, powers[i], size=SIZE_LABEL, fill=COLOR_MUTED, anchor="middle")
    svg.line(x0 - 20, y0 + 62, x0 + 5 * 100 - 30, y0 + 62, stroke=COLOR_LINE)
    y = y0 + 100
    svg.text(x0 - 20, y, "H(ATGCT) =", size=SIZE_LABEL)
    cx = x0 + 90
    for i, t in enumerate(terms):
        svg.text(cx + i * 84, y, t + (" +" if i < 4 else ""), size=SIZE_LABEL)
    svg.text(cx + 5 * 84 - 10, y, "=", size=SIZE_LABEL)
    svg.text(cx + 5 * 84 + 14, y, "121", size=20, weight="bold", fill=COLOR_PRIMARY)
    svg.text(x0 - 20, y + 30, "最左边的碱基权值最高（4⁴），最右边的碱基权值最低（4⁰）。",
             mono=False, size=SIZE_NOTE, fill=COLOR_MUTED)
    save("hash-01-base-encoding", svg)


def fig_hash_kmer_table():
    ref = "ATGCGTAACT"
    x0, y0 = 80, 84
    w, h = 760, 340
    svg = Svg(w, h, "k-mer 哈希表的构建（k=5）",
              "参考序列的全部 5-mer 作为关键码，哈希表记录每个 5-mer 出现的位置。")
    svg.text(x0, 42, "把参考序列拆成 k-mer（k=5），建立哈希表", mono=False,
             size=SIZE_TITLE, weight="bold")
    svg.seq(x0, y0, ref)
    for i in range(len(ref)):
        svg.text(x0 + i * CHAR_W - 2, y0 - 14, str(i + 1), size=10, fill=COLOR_MUTED)
    svg.rect(x0 - 4, y0 - 16, 5 * CHAR_W + 8, 24, fill="none", stroke=COLOR_PRIMARY, sw=1.6)
    svg.text(x0 + 5 * CHAR_W + 12, y0 + 2, "k-mer 1", size=SIZE_LABEL, fill=COLOR_PRIMARY)
    svg.rect(x0 + CHAR_W - 4, y0 + 14, 5 * CHAR_W + 8, 24, fill="none", stroke=COLOR_WARN, sw=1.6)
    svg.text(x0 + 6 * CHAR_W + 12, y0 + 32, "k-mer 2", size=SIZE_LABEL, fill=COLOR_WARN)
    tx, ty = x0 + 330, y0 - 30
    svg.rect(tx, ty, 300, 190, stroke=COLOR_LINE, rx=6)
    svg.text(tx + 16, ty + 26, "哈希表", mono=False, size=SIZE_LABEL,
             weight="bold", fill=COLOR_PRIMARY)
    svg.text(tx + 80, ty + 26, "关键码", mono=False, size=SIZE_NOTE, fill=COLOR_MUTED)
    svg.text(tx + 190, ty + 26, "位置", mono=False, size=SIZE_NOTE, fill=COLOR_MUTED)
    table = [("ATGCG", "1", COLOR_PRIMARY), ("TGCGT", "2", COLOR_WARN),
             ("GCGTA", "3", COLOR_TEXT), ("CGTAA", "4", COLOR_TEXT), ("…", "…", COLOR_MUTED)]
    for j, (kmer, pos, c) in enumerate(table):
        y = ty + 54 + j * 26
        svg.seq(tx + 16, y, kmer, size=SIZE_LABEL, fill=c)
        svg.text(tx + 130, y, "→", size=SIZE_LABEL, fill=COLOR_MUTED)
        svg.seq(tx + 160, y, pos, size=SIZE_LABEL, fill=c)
    svg.text(x0, ty + 216, "同一个 k-mer 可在基因组多个位置出现，哈希表记录全部位置。",
             mono=False, size=SIZE_NOTE, fill=COLOR_MUTED)
    save("hash-02-kmer-table", svg)


def fig_hash_pigeonhole():
    read = "ATGCGT" + "TAAGTA" + "CGTACG" + "GTACGT"
    segs = [read[i:i + 6] for i in range(0, 24, 6)]
    x0, y0 = 70, 70
    w, h = 720, 330
    svg = Svg(w, h, "鸽洞原理示意图",
              "把 read 分成 4 段，允许 1 处错配时至少有 3 段能精确命中参考基因组。")
    svg.text(x0, 40, "鸽洞原理：分段容错定位", mono=False, size=SIZE_TITLE, weight="bold")
    svg.text(x0, y0 - 6, "read（24 nt，第 2 段含 1 处错配）：", mono=False, size=SIZE_LABEL)
    seg_w = 6 * CHAR_W + 12
    for i, seg in enumerate(segs):
        sx = x0 + i * seg_w
        bad = (i == 1)
        svg.rect(sx, y0 + 6, 6 * CHAR_W + 8, 28,
                 fill=COLOR_WARN_FILL if bad else COLOR_FILL,
                 stroke=COLOR_WARN if bad else COLOR_PRIMARY)
        svg.seq(sx + 4, y0 + 26, seg)
        if bad:
            svg.text(sx + 4 + 2 * CHAR_W, y0 - 6, "✗ 错配", size=SIZE_LABEL, fill=COLOR_WARN)
    gy = y0 + 150
    svg.text(x0, gy - 12, "参考基因组", mono=False, size=SIZE_LABEL, fill=COLOR_MUTED)
    svg.line(x0, gy, x0 + 4 * seg_w, gy, stroke=COLOR_PRIMARY, sw=2)
    for i in range(4):
        sx = x0 + i * seg_w + 3 * CHAR_W
        bad = (i == 1)
        svg.arrow(sx, y0 + 40, sx, gy - 8,
                  stroke=COLOR_WARN if bad else COLOR_PRIMARY)
        svg.text(sx - 6, gy + 22, "✗ 不命中" if bad else "✓ 命中",
                 size=SIZE_LABEL, fill=COLOR_WARN if bad else COLOR_PRIMARY)
    svg.text(x0, gy + 64, "允许 1 处错配时把 read 分成 4 段：即使有 1 段因错配查不到，",
             mono=False, size=SIZE_NOTE, fill=COLOR_MUTED)
    svg.text(x0, gy + 86, "其余 3 段仍能在哈希表中命中，read 的候选位置不会丢失。",
             mono=False, size=SIZE_NOTE, fill=COLOR_MUTED)
    save("hash-03-pigeonhole", svg)


# ---------------------------------------------------------------- 双序列比对系列

SEQ1 = "AAGT"
SEQ2 = "AGCT"
GAP = -5


def _score(a, b):
    return 5 if a == b else -4


def _nw_matrix():
    m = [[0] * 5 for _ in range(5)]
    for i in range(5):
        m[i][0] = -5 * i
    for j in range(5):
        m[0][j] = -5 * j
    for i in range(1, 5):
        for j in range(1, 5):
            m[i][j] = max(m[i-1][j-1] + _score(SEQ1[i-1], SEQ2[j-1]),
                          m[i-1][j] + GAP, m[i][j-1] + GAP)
    return m


def _sw_matrix():
    m = [[0] * 5 for _ in range(5)]
    for i in range(1, 5):
        for j in range(1, 5):
            m[i][j] = max(0,
                          m[i-1][j-1] + _score(SEQ1[i-1], SEQ2[j-1]),
                          m[i-1][j] + GAP, m[i][j-1] + GAP)
    return m


def _sources(mat, sw=False):
    src = [[set() for _ in range(5)] for _ in range(5)]
    for i in range(1, 5):
        for j in range(1, 5):
            v = mat[i][j]
            if sw and v == 0:
                continue
            if mat[i-1][j-1] + _score(SEQ1[i-1], SEQ2[j-1]) == v:
                src[i][j].add('d')
            if mat[i-1][j] + GAP == v:
                src[i][j].add('u')
            if mat[i][j-1] + GAP == v:
                src[i][j].add('l')
    return src


def _dp_grid_frame(svg, x0, y0, cell=56, init=None):
    svg.text(x0 + cell // 2 - 6, y0 - 12, "∅", fill=COLOR_MUTED)
    for j, b in enumerate(SEQ2):
        svg.text(x0 + (j + 1) * cell + cell // 2 - 6, y0 - 12, b, weight="bold", fill=COLOR_PRIMARY)
    svg.text(x0 - 96, y0 + 12, "seq2 →", mono=False, size=SIZE_LABEL, fill=COLOR_MUTED)
    for i, b in enumerate(SEQ1):
        svg.text(x0 - 26, y0 + (i + 1) * cell + 20, b, weight="bold", fill=COLOR_PRIMARY)
    svg.text(x0 - 28, y0 + 2 * cell + 4, "seq1", mono=False, size=SIZE_LABEL, fill=COLOR_MUTED)
    for i in range(6):
        svg.line(x0, y0 + i * cell, x0 + 5 * cell, y0 + i * cell, stroke="#e5e7eb", sw=1)
    for j in range(6):
        svg.line(x0 + j * cell, y0, x0 + j * cell, y0 + 5 * cell, stroke="#e5e7eb", sw=1)
    if init is not None:
        for j in range(5):
            svg.text(x0 + j * cell + cell // 2 - 12, y0 + cell // 2 + 6,
                     str(init[0][j]), fill=COLOR_MUTED)
        for i in range(5):
            svg.text(x0 + cell // 2 - 12, y0 + i * cell + cell // 2 + 6,
                     str(init[i][0]), fill=COLOR_MUTED)


def _cell_center(x0, y0, cell, i, j):
    return x0 + j * cell + cell // 2, y0 + i * cell + cell // 2


def _src_arrows(svg, x0, y0, cell, i, j, srcs, color=COLOR_MUTED):
    cx, cy = _cell_center(x0, y0, cell, i, j)
    r = cell * 0.30
    for d, (dx, dy) in {'d': (-1, -1), 'u': (0, -1), 'l': (-1, 0)}.items():
        if d in srcs:
            x2 = cx + dx * r
            y2 = cy + dy * r
            svg.arrow(cx + dx * r * 0.25, cy + dy * r * 0.25, x2, y2,
                      stroke=color, sw=1.6)


def fig_scoring_matrix():
    bases = "AGCT"
    x0, y0, cell = 110, 96, 62
    w, h = 600, 430
    svg = Svg(w, h, "双序列比对示例的打分矩阵",
              "match 得 5 分，mismatch 扣 4 分，空位罚分 d=-5。")
    svg.text(x0 - 30, 42, "打分矩阵与空位罚分", mono=False, size=SIZE_TITLE, weight="bold")
    for j, b in enumerate(bases):
        svg.text(x0 + (j + 1) * cell + cell // 2 - 6, y0 - 16, b, weight="bold", fill=COLOR_PRIMARY)
    for i, b in enumerate(bases):
        svg.text(x0 - 26, y0 + (i + 1) * cell + 24, b, weight="bold", fill=COLOR_PRIMARY)
    for i in range(4):
        for j in range(4):
            x = x0 + (j + 1) * cell + 8
            y = y0 + (i + 1) * cell + 30
            match = bases[i] == bases[j]
            svg.rect(x, y - 22, cell - 12, cell - 12,
                     fill=COLOR_FILL if match else COLOR_WARN_FILL,
                     stroke=COLOR_PRIMARY if match else COLOR_WARN)
            svg.text(x + (cell - 12) // 2 - 12, y + 4, "+5" if match else "-4",
                     weight="bold", fill=COLOR_PRIMARY if match else COLOR_WARN)
    ly = y0 + 4 * cell + 44
    legend = [("match +5", COLOR_FILL, COLOR_PRIMARY),
              ("mismatch −4", COLOR_WARN_FILL, COLOR_WARN),
              ("空位罚分 d = −5", "none", COLOR_PRIMARY)]
    lx = x0 - 30
    for text, fill, stroke in legend:
        svg.rect(lx, ly - 18, 168, 26, fill=fill, stroke=stroke, rx=4)
        svg.text(lx + 14, ly, text, mono=False, size=SIZE_LABEL, fill=stroke, weight="bold")
        lx += 184
    svg.text(x0 - 30, ly + 34, "示例：A 对 A 得 +5；A 对 G 扣 4；每开一个空位扣 5 分。",
             mono=False, size=SIZE_NOTE, fill=COLOR_MUTED)
    save("pairwise-01-scoring-matrix", svg)


def fig_empty_grid():
    x0, y0, cell = 120, 92, 56
    w, h = 520, 410
    nw = _nw_matrix()
    svg = Svg(w, h, "待填写的动态规划表格（第 0 行/列已初始化）",
              "行为 seq1=AAGT，列为 seq2=AGCT；以全局比对为例，第 0 行/第 0 列已填入空位累计罚分。")
    svg.text(x0 - 60, 40, "动态规划表格（第 0 行/列已初始化）", mono=False,
             size=SIZE_TITLE, weight="bold")
    _dp_grid_frame(svg, x0, y0, cell, init=nw)
    svg.text(x0 - 60, y0 + 5 * cell + 34, "灰色为初始化值（0、-5、-10…，空位累计罚分）；空格请按规则填写。",
             mono=False, size=SIZE_NOTE, fill=COLOR_MUTED)
    save("pairwise-02-empty-grid", svg)


def fig_nw_matrix():
    x0, y0, cell = 120, 92, 56
    w, h = 660, 490
    mat = _nw_matrix()
    srcs = _sources(mat)
    svg = Svg(w, h, "Needleman-Wunsch 全局比对填表结果",
              "每格箭头标出取值来源（对角/上/左）；加粗路径为回溯，右下角最优得分 5。")
    svg.text(x0 - 70, 40, "Needleman-Wunsch 全局比对", mono=False, size=SIZE_TITLE, weight="bold")
    _dp_grid_frame(svg, x0, y0, cell, init=mat)
    path = {(4, 4), (3, 3), (3, 2), (2, 1)}
    for i in range(1, 5):
        for j in range(1, 5):
            cx, cy = _cell_center(x0, y0, cell, i, j)
            on_path = (i, j) in path
            if on_path:
                svg.rect(x0 + j * cell + 2, y0 + i * cell + 2, cell - 4, cell - 4,
                         fill=COLOR_FILL, sw=0)
            svg.text(cx - 22, cy - 6, str(mat[i][j]),
                     weight="bold" if on_path else "normal",
                     fill=COLOR_PRIMARY if on_path else COLOR_TEXT)
            _src_arrows(svg, x0, y0, cell, i, j, srcs[i][j],
                        color=COLOR_PRIMARY if on_path else COLOR_MUTED)
    svg.rect(x0 + 0 * cell + 2, y0 + 1 * cell + 2, cell - 4, cell - 4, fill=COLOR_FILL, sw=0)
    svg.text(x0 + 0 * cell + cell // 2 - 12, y0 + 1 * cell + cell // 2 - 6, str(mat[1][0]),
             weight="bold", fill=COLOR_PRIMARY)
    fx, fy = x0 + 4 * cell + 2, y0 + 4 * cell + 2
    svg.rect(fx, fy, cell - 4, cell - 4, fill="none", stroke=COLOR_PRIMARY, sw=2.2)
    y = y0 + 5 * cell + 44
    svg.text(x0 - 70, y, "最优比对（得分 5）：", mono=False, size=SIZE_LABEL)
    svg.seq(x0 + 120, y, "A A G - T", weight="bold", fill=COLOR_PRIMARY)
    svg.seq(x0 + 120, y + 26, "- A G C T", weight="bold", fill=COLOR_PRIMARY)
    svg.text(x0 + 320, y + 13, "（回溯路径见加粗格与绿色箭头）", mono=False,
             size=SIZE_NOTE, fill=COLOR_MUTED)
    save("pairwise-03-nw-matrix", svg)


def fig_sw_matrix():
    x0, y0, cell = 120, 92, 56
    w, h = 700, 530
    mat = _sw_matrix()
    srcs = _sources(mat, sw=True)
    svg = Svg(w, h, "Smith-Waterman 局部比对填表结果",
              "负值记 0 的格子没有来源箭头；两个最高分 10 分别回溯得到两个最优局部比对。")
    svg.text(x0 - 70, 40, "Smith-Waterman 局部比对", mono=False, size=SIZE_TITLE, weight="bold")
    _dp_grid_frame(svg, x0, y0, cell, init=[[0]*5 for _ in range(5)])
    path1 = {(3, 2), (2, 1)}
    path2 = {(4, 4), (3, 3), (3, 2), (2, 1)}
    for i in range(1, 5):
        for j in range(1, 5):
            cx, cy = _cell_center(x0, y0, cell, i, j)
            in1 = (i, j) in path1
            in2 = (i, j) in path2
            if in1 or in2:
                svg.rect(x0 + j * cell + 2, y0 + i * cell + 2, cell - 4, cell - 4,
                         fill=COLOR_FILL if in1 else COLOR_WARN_FILL, sw=0)
            val = mat[i][j]
            svg.text(cx - 22, cy - 6, str(val),
                     weight="bold" if val == 10 else "normal",
                     fill=COLOR_PRIMARY if val == 10 else COLOR_TEXT)
            if val > 0:
                _src_arrows(svg, x0, y0, cell, i, j, srcs[i][j],
                            color=(COLOR_PRIMARY if in1 else (COLOR_WARN if in2 else COLOR_MUTED)))
    svg.rect(x0 + 0 * cell + 2, y0 + 1 * cell + 2, cell - 4, cell - 4, fill=COLOR_FILL, sw=0)
    for (i, j) in [(3, 2), (4, 4)]:
        svg.rect(x0 + j * cell + 2, y0 + i * cell + 2, cell - 4, cell - 4,
                 fill="none", stroke=COLOR_PRIMARY, sw=2.2)
    y = y0 + 5 * cell + 44
    svg.text(x0 - 70, y, "两个并列最优（各 10 分）：", mono=False, size=SIZE_LABEL)
    svg.seq(x0 + 170, y, "A G", weight="bold", fill=COLOR_PRIMARY)
    svg.seq(x0 + 170, y + 24, "A G", weight="bold", fill=COLOR_PRIMARY)
    svg.text(x0 + 240, y + 13, "；", mono=False)
    svg.seq(x0 + 270, y, "A G - T", weight="bold", fill=COLOR_WARN)
    svg.seq(x0 + 270, y + 24, "A G C T", weight="bold", fill=COLOR_WARN)
    svg.text(x0 - 70, y + 58, "绿色与琥珀路径分别从两个 10 分格回溯；记 0 的格子没有来源箭头（比对新起点的候选）。",
             mono=False, size=SIZE_NOTE, fill=COLOR_MUTED)
    save("pairwise-04-sw-matrix", svg)


def main():
    fig_bwt_rotations()
    fig_bwt_sorted()
    for step in (1, 2, 3):
        fig_bwt_decode(step)
    fig_bwt_decode_rest()
    fig_hash_encoding()
    fig_hash_kmer_table()
    fig_hash_pigeonhole()
    fig_scoring_matrix()
    fig_empty_grid()
    fig_nw_matrix()
    fig_sw_matrix()


if __name__ == "__main__":
    main()
