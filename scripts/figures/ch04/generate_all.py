"""生成第4章算法示意图 SVG（BWT、哈希表、双序列比对）。

运行：python3 scripts/figures/ch04/generate_all.py
绘制铁律（视觉验收教训）：
1. 高亮矩形一律先画、文字后画（SVG 后画者在上层）；
2. 数值与箭头分居格子两角，物理隔离；
3. 所有文字与相邻图形留至少 8px 间距。
"""

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
    w = 340
    x0 = (w - 7 * CHAR_W) // 2 + 17
    y0 = 66
    h = y0 + len(rows) * ROW_H + 24
    svg = Svg(w, h, "BWT 构建第 1 步：全部循环旋转",
              "对 ACAACG$ 写出 7 个循环旋转，高亮行为原序列本身。")
    svg.text(w // 2, 40, "ACAACG$ 的 7 个循环旋转", mono=False, size=SIZE_TITLE, weight="bold", anchor="middle")
    for i, r in enumerate(rows):
        y = y0 + i * ROW_H + 16
        svg.text(x0 - 34, y, str(i + 1), size=SIZE_LABEL, fill=COLOR_MUTED)
        if i == 0:
            svg.rect(x0 - 10, y - 17, (len(r) - 1) * CHAR_W + 30, 24, fill=COLOR_FILL)
        svg.seq(x0, y, r)
    save("bwt-01-rotations", svg)


def fig_bwt_sorted():
    rows, f, l = bwt_matrix_rows()
    w = 380
    x0 = (w - 7 * CHAR_W) // 2 + 17
    y0 = 92
    h = y0 + len(rows) * ROW_H + 24
    svg = Svg(w, h, "BWT 构建第 2 步：排序后的旋转矩阵",
              "全部循环旋转按 $<A<C<G 排序；F 列为第一列，L 列为最后一列（BWT）。")
    svg.text(w // 2, 40, "排序后的旋转矩阵", mono=False, size=SIZE_TITLE, weight="bold", anchor="middle")
    svg.text(x0 - 4, y0 - 12, "F", weight="bold", fill=COLOR_PRIMARY)
    svg.text(x0 + (len(rows[0]) - 1) * CHAR_W + 4, y0 - 12, "L", weight="bold", fill=COLOR_WARN)
    for i, r in enumerate(rows):
        y = y0 + i * ROW_H + 16
        svg.text(x0 - 34, y, str(i + 1), size=SIZE_LABEL, fill=COLOR_MUTED)
        # 先画高亮框，后画文字（文字永远在最上层）
        svg.rect(x0 - 6, y - 15, 16, 21, fill=COLOR_FILL, sw=1.4)
        lx = x0 + (len(r) - 1) * CHAR_W - 2
        svg.rect(lx, y - 15, 16, 21, fill=COLOR_WARN_FILL, stroke=COLOR_WARN, sw=1.4)
        svg.seq(x0, y, r)
    save("bwt-02-sorted-matrix", svg)


def _decode_columns(svg, x0, y0, hl_f_rows, hl_l_rows):
    """F/L 两列 + 行号；高亮框先画、字符后画。"""
    rows, f, l = bwt_matrix_rows()
    fx, lx = x0 + 30, x0 + 190
    svg.text(fx, y0 - 14, "F 列", mono=False, size=SIZE_LABEL, fill=COLOR_PRIMARY, weight="bold")
    svg.text(lx, y0 - 14, "L 列", mono=False, size=SIZE_LABEL, fill=COLOR_WARN, weight="bold")
    for i in hl_f_rows:
        svg.rect(fx - 6, y0 + i * ROW_H, 16, 21, fill=COLOR_FILL, sw=1.4)
    for i in hl_l_rows:
        svg.rect(lx - 6, y0 + i * ROW_H, 16, 21,
                 fill=COLOR_WARN_FILL, stroke=COLOR_WARN, sw=1.4)
    for i, (fc, lc) in enumerate(zip(f, l)):
        y = y0 + i * ROW_H + 16
        svg.text(x0 - 20, y, str(i + 1), size=SIZE_LABEL, fill=COLOR_MUTED)
        svg.text(fx, y, fc)
        svg.text(lx, y, lc)
    return fx, lx


def _cy(y0, i):
    return y0 + i * ROW_H + 10


def fig_bwt_decode(step):
    x0, y0 = 60, 92
    w, h = 340, y0 + 7 * ROW_H + 24
    meta = {
        1: ("第 1 步：原序列以 G 结尾", [(0, 0)], []),
        2: ("第 2 步：G 前面是 C", [(6, 0)], [0, 6]),
        3: ("第 3 步：C 前面是 A", [(5, 5)], [5, 6]),
    }
    title, arrows, hl_l = meta[step]
    hl_f = sorted({fr for fr, lr in arrows})
    svg = Svg(w, h, f"BWT 解码{title}",
              f"BWT解码第{step}步的LF映射：琥珀为L列来源格，绿色为F列命中格。")
    svg.text(x0, 40, title, mono=False, size=SIZE_TITLE, weight="bold")
    fx, lx = _decode_columns(svg, x0, y0, hl_f, hl_l)
    for fr, lr in arrows:
        svg.arrow(lx - 10, _cy(y0, lr), fx + 18, _cy(y0, fr), sw=1.8)
    save(f"bwt-0{step + 2}-decode-step{step}", svg)


def fig_bwt_decode_rest():
    x0, y0 = 60, 92
    w, h = 400, y0 + 7 * ROW_H + 104
    svg = Svg(w, h, "BWT 解码第 4—6 步与逆序还原",
              "继续LF映射得到GCAA、GCAAC、GCAACA；逆序即原序列ACAACG。")
    svg.text(x0, 40, "第 4—6 步：继续 LF 映射", mono=False, size=SIZE_TITLE, weight="bold")
    steps = [(5, 2), (2, 1), (1, 4)]  # (L行, F行)
    hl_f = sorted({fr for _, fr in steps})
    hl_l = sorted({lr for lr, _ in steps})
    fx, lx = _decode_columns(svg, x0, y0, hl_f, hl_l)
    for k, (lr, fr) in enumerate(steps):
        svg.arrow(lx - 10, _cy(y0, lr), fx + 18, _cy(y0, fr), sw=1.8)
        mx = (fx + lx) / 2
        my = (_cy(y0, lr) + _cy(y0, fr)) / 2
        svg.rect(mx - 10, my - 13, 20, 20, fill="#ffffff", stroke=COLOR_PRIMARY, sw=1.2)
        svg.text(mx, my + 1, str(k + 4), size=SIZE_LABEL, weight="bold",
                 fill=COLOR_PRIMARY, anchor="middle")
    y = y0 + 7 * ROW_H + 40
    svg.seq(x0 + 10, y, "GCAACA")
    svg.arrow(x0 + 10 + 6 * CHAR_W + 10, y - 5, x0 + 10 + 6 * CHAR_W + 62, y - 5)
    svg.text(x0 + 10 + 6 * CHAR_W + 36, y - 13, "逆序", mono=False, size=SIZE_NOTE,
             fill=COLOR_MUTED, anchor="middle")
    svg.seq(x0 + 10 + 6 * CHAR_W + 76, y, "ACAACG", weight="bold", fill=COLOR_PRIMARY)
    save("bwt-06-decode-steps4-6", svg)


# ---------------------------------------------------------------- 哈希表系列

def fig_hash_encoding():
    seq = "ATGCT"
    digits = "01321"
    powers = ["4⁴", "4³", "4²", "4¹", "4⁰"]
    terms = ["0×256", "1×64", "3×16", "2×4", "1×1"]
    x0, y0 = 90, 86
    w, h = 640, 290
    svg = Svg(w, h, "碱基的四进制编码",
              "把 A、T、G、C 分别编码为 0、1、3、2，按最左位权值最高计算，ATGCT 的关键码为 121。")
    svg.text(x0, 42, "把碱基编码成数字：A→0，T→1，G→3，C→2", mono=False,
             size=SIZE_TITLE, weight="bold")
    for i, ch in enumerate(seq):
        x = x0 + i * 100
        svg.rect(x - 16, y0 - 26, 60, 54, fill=COLOR_FILL if i == 0 else "none")
        svg.text(x + 14, y0, ch, size=22, weight="bold", anchor="middle")
        svg.text(x + 14, y0 + 24, digits[i], fill=COLOR_PRIMARY, weight="bold", anchor="middle")
        svg.text(x + 14, y0 + 50, powers[i], size=SIZE_LABEL, fill=COLOR_MUTED, anchor="middle")
    svg.line(x0 - 22, y0 + 66, x0 + 5 * 100 - 32, y0 + 66, stroke=COLOR_LINE)
    y = y0 + 104
    svg.text(x0 - 22, y, "H(ATGCT) =", size=SIZE_LABEL)
    cx = x0 + 92
    for i, t in enumerate(terms):
        svg.text(cx + i * 74, y, t + (" +" if i < 4 else ""), size=SIZE_LABEL)
    svg.text(cx + 5 * 74 - 12, y, "=", size=SIZE_LABEL)
    svg.text(cx + 5 * 74 + 14, y, "121", size=20, weight="bold", fill=COLOR_PRIMARY)
    svg.text(x0 - 22, y + 32, "最左边的碱基权值最高（4⁴），最右边的碱基权值最低（4⁰）。",
             mono=False, size=SIZE_NOTE, fill=COLOR_MUTED)
    save("hash-01-base-encoding", svg)


def fig_hash_kmer_table():
    ref = "ATGCGTAACT"
    x0, y0 = 80, 96
    w, h = 780, 330
    svg = Svg(w, h, "k-mer 哈希表的构建（k=5）",
              "参考序列的全部 5-mer 作为关键码，哈希表记录每个 5-mer 出现的位置。")
    svg.text(x0, 42, "把参考序列拆成 k-mer（k=5）", mono=False,
             size=SIZE_TITLE, weight="bold")
    # 位置刻度：与序列字符拉开 18px
    for i in range(len(ref)):
        svg.text(x0 + i * CHAR_W - 2, y0 - 22, str(i + 1), size=10, fill=COLOR_MUTED)
    # 序列
    svg.seq(x0, y0, ref)
    # k-mer 窗口：全部画在序列下方，两层错开，与字符留 14px 间距
    svg.rect(x0 - 5, y0 + 14, 5 * CHAR_W + 10, 22, fill="none", stroke=COLOR_PRIMARY, sw=1.6)
    svg.text(x0 + 5 * CHAR_W + 12, y0 + 30, "k-mer 1（ATGCG，位置 1）", size=SIZE_LABEL, fill=COLOR_PRIMARY)
    svg.rect(x0 + CHAR_W - 5, y0 + 44, 5 * CHAR_W + 10, 22, fill="none", stroke=COLOR_WARN, sw=1.6)
    svg.text(x0 + 6 * CHAR_W + 12, y0 + 60, "k-mer 2（TGCGT，位置 2）", size=SIZE_LABEL, fill=COLOR_WARN)
    # 哈希表（右侧独立区域）
    tx, ty = x0 + 360, y0 - 44
    svg.rect(tx, ty, 310, 196, stroke=COLOR_LINE, rx=6)
    svg.text(tx + 16, ty + 28, "哈希表", mono=False, size=SIZE_LABEL,
             weight="bold", fill=COLOR_PRIMARY)
    svg.text(tx + 84, ty + 28, "关键码", mono=False, size=SIZE_NOTE, fill=COLOR_MUTED)
    svg.text(tx + 196, ty + 28, "位置", mono=False, size=SIZE_NOTE, fill=COLOR_MUTED)
    table = [("ATGCG", "1", COLOR_PRIMARY), ("TGCGT", "2", COLOR_WARN),
             ("GCGTA", "3", COLOR_TEXT), ("CGTAA", "4", COLOR_TEXT), ("…", "…", COLOR_MUTED)]
    for j, (kmer, pos, c) in enumerate(table):
        y = ty + 58 + j * 26
        svg.seq(tx + 16, y, kmer, size=SIZE_LABEL, fill=c)
        svg.text(tx + 136, y, "→", size=SIZE_LABEL, fill=COLOR_MUTED)
        svg.seq(tx + 168, y, pos, size=SIZE_LABEL, fill=c)
    save("hash-02-kmer-table", svg)


def fig_hash_pigeonhole():
    """图身零说明文字：说明全部放图题。"""
    read = "ATGCGT" + "TAAGTA" + "CGTACG" + "GTACGT"
    segs = [read[i:i + 6] for i in range(0, 24, 6)]
    x0, y0 = 70, 76
    w, h = 660, 240
    svg = Svg(w, h, "鸽洞原理示意",
              "read 分成 4 段、第 2 段含 1 处错配（✗）：即使该段无法精确命中，"
              "其余 3 段（✓）仍能在哈希表中定位到参考基因组上。")
    svg.text(x0, 40, "鸽洞原理：分段容错定位", mono=False, size=SIZE_TITLE, weight="bold")
    seg_w = 6 * CHAR_W + 34
    for i, seg in enumerate(segs):
        sx = x0 + i * seg_w
        bad = (i == 1)
        svg.rect(sx, y0, 6 * CHAR_W + 8, 30,
                 fill=COLOR_WARN_FILL if bad else COLOR_FILL,
                 stroke=COLOR_WARN if bad else COLOR_PRIMARY)
        svg.seq(sx + 4, y0 + 21, seg)
        svg.text(sx + 6 * CHAR_W + 14, y0 + 21, "✗" if bad else "✓",
                 size=SIZE_LABEL, weight="bold",
                 fill=COLOR_WARN if bad else COLOR_PRIMARY)
    gy = y0 + 108
    svg.line(x0, gy, x0 + 4 * seg_w, gy, stroke=COLOR_PRIMARY, sw=2)
    svg.text(x0 + 4 * seg_w + 12, gy + 4, "参考基因组", mono=False,
             size=SIZE_LABEL, fill=COLOR_MUTED)
    for i in range(4):
        sx = x0 + i * seg_w + 3 * CHAR_W
        bad = (i == 1)
        svg.arrow(sx, y0 + 38, sx, gy - 8,
                  stroke=COLOR_WARN if bad else COLOR_PRIMARY)
        svg.text(sx - 6, gy + 24, "✗ 不命中" if bad else "✓ 命中",
                 size=SIZE_LABEL, fill=COLOR_WARN if bad else COLOR_PRIMARY)
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


def _dp_grid_frame(svg, x0, y0, cell=58, init=None, skip=None):
    svg.text(x0 + cell // 2 - 6, y0 - 12, "∅", fill=COLOR_MUTED)
    for j, b in enumerate(SEQ2):
        svg.text(x0 + (j + 1) * cell + cell // 2 - 6, y0 - 12, b, weight="bold", fill=COLOR_PRIMARY)
    svg.text(x0 - 98, y0 + 12, "seq2 →", mono=False, size=SIZE_LABEL, fill=COLOR_MUTED)
    for i, b in enumerate(SEQ1):
        svg.text(x0 - 26, y0 + (i + 1) * cell + 22, b, weight="bold", fill=COLOR_PRIMARY)
    svg.text(x0 - 30, y0 + 2 * cell + 6, "seq1", mono=False, size=SIZE_LABEL, fill=COLOR_MUTED)
    for i in range(6):
        svg.line(x0, y0 + i * cell, x0 + 5 * cell, y0 + i * cell, stroke="#e5e7eb", sw=1)
    for j in range(6):
        svg.line(x0 + j * cell, y0, x0 + j * cell, y0 + 5 * cell, stroke="#e5e7eb", sw=1)
    if init is not None:
        skip = skip or set()
        for j in range(5):
            if (0, j) in skip:
                continue
            svg.text(x0 + j * cell + cell // 2 - 12, y0 + cell // 2 + 6,
                     str(init[0][j]), fill=COLOR_MUTED)
        for i in range(5):
            if (i, 0) in skip:
                continue
            svg.text(x0 + cell // 2 - 12, y0 + i * cell + cell // 2 + 6,
                     str(init[i][0]), fill=COLOR_MUTED)


def _cell_value_pos(x0, y0, cell, i, j):
    """数值固定在格子左上角。"""
    return x0 + j * cell + 9, y0 + i * cell + 21


def _src_arrows(svg, x0, y0, cell, i, j, srcs, color=COLOR_MUTED):
    """来源箭头收在格子右下角小区，与左上角数值物理隔离。"""
    cx = x0 + j * cell + cell - 14
    cy = y0 + i * cell + cell - 12
    r = 11
    for d, (dx, dy) in {'d': (-1, -1), 'u': (0, -1), 'l': (-1, 0)}.items():
        if d in srcs:
            svg.arrow(cx + dx * r * 0.25, cy + dy * r * 0.25,
                      cx + dx * r, cy + dy * r, stroke=color, sw=1.5)


def fig_scoring_matrix():
    bases = "AGCT"
    w, h = 640, 450
    x0, y0, cell = 160, 100, 64
    svg = Svg(w, h, "双序列比对示例的打分矩阵",
              "match 得 5 分，mismatch 扣 4 分，空位罚分 d=-5。")
    svg.text(x0 - 30, 44, "打分矩阵与空位罚分", mono=False, size=SIZE_TITLE, weight="bold")
    for j, b in enumerate(bases):
        svg.text(x0 + (j + 1) * cell + (cell - 14) // 2, y0 - 16, b, anchor="middle",
                 weight="bold", fill=COLOR_PRIMARY)
    for i, b in enumerate(bases):
        svg.text(x0 - 26, y0 + (i + 1) * cell + 26, b, weight="bold", fill=COLOR_PRIMARY)
    for i in range(4):
        for j in range(4):
            x = x0 + (j + 1) * cell + 8
            y = y0 + (i + 1) * cell + 32
            match = bases[i] == bases[j]
            svg.rect(x, y - 24, cell - 14, cell - 14,
                     fill=COLOR_FILL if match else COLOR_WARN_FILL,
                     stroke=COLOR_PRIMARY if match else COLOR_WARN)
            svg.text(x + (cell - 14) // 2, y + 4, "+5" if match else "-4",
                     anchor="middle",
                     weight="bold", fill=COLOR_PRIMARY if match else COLOR_WARN)
    ly = y0 + 4 * cell + 46
    legend = [("match +5", COLOR_FILL, COLOR_PRIMARY),
              ("mismatch −4", COLOR_WARN_FILL, COLOR_WARN),
              ("空位罚分 d = −5", "none", COLOR_PRIMARY)]
    chip_w, chip_gap = 176, 18
    total = 3 * chip_w + 2 * chip_gap
    lx = (w - total) // 2
    for text, fill, stroke in legend:
        svg.rect(lx, ly - 19, chip_w, 27, fill=fill, stroke=stroke, rx=4)
        svg.text(lx + chip_w // 2, ly + 1, text, mono=False, size=SIZE_LABEL,
                 anchor="middle", fill=stroke, weight="bold")
        lx += chip_w + chip_gap
    svg.text(w // 2, ly + 36, "示例：A 对 A 得 +5；A 对 G 扣 4；每开一个空位扣 5 分。",
             mono=False, size=SIZE_NOTE, fill=COLOR_MUTED, anchor="middle")
    save("pairwise-01-scoring-matrix", svg)


def fig_empty_grid():
    x0, y0, cell = 130, 100, 58
    w, h = 540, 430
    nw = _nw_matrix()
    svg = Svg(w, h, "待填写的动态规划表格（第 0 行/列已初始化）",
              "行为 seq1=AAGT，列为 seq2=AGCT；以全局比对为例，第 0 行/第 0 列已填入空位累计罚分。")
    svg.text(x0 - 60, 44, "动态规划表格（第 0 行/列已初始化）", mono=False,
             size=SIZE_TITLE, weight="bold")
    _dp_grid_frame(svg, x0, y0, cell, init=nw, skip={(0, 0)})
    svg.text(x0 - 60, y0 + 5 * cell + 36, "灰色为初始化值（0、-5、-10…，空位累计罚分）；空格请按规则填写。",
             mono=False, size=SIZE_NOTE, fill=COLOR_MUTED)
    save("pairwise-02-empty-grid", svg)


def fig_nw_matrix():
    x0, y0, cell = 130, 100, 58
    w, h = 680, 520
    mat = _nw_matrix()
    srcs = _sources(mat)
    svg = Svg(w, h, "Needleman-Wunsch 全局比对填表结果",
              "数值在格左上角，右下角小箭头为取值来源（对角/上/左）；加粗路径为回溯，右下角最优得分 5。")
    svg.text(x0 - 70, 44, "Needleman-Wunsch 全局比对", mono=False, size=SIZE_TITLE, weight="bold")
    _dp_grid_frame(svg, x0, y0, cell, init=mat, skip={(0, 0), (1, 0)})
    path = {(4, 4), (3, 3), (3, 2), (2, 1)}
    for i in range(1, 5):
        for j in range(1, 5):
            on_path = (i, j) in path
            if on_path:
                svg.rect(x0 + j * cell + 2, y0 + i * cell + 2, cell - 4, cell - 4,
                         fill=COLOR_FILL, sw=0)
    # 先铺所有底色，再统一写文字
    for i in range(1, 5):
        for j in range(1, 5):
            on_path = (i, j) in path
            tx, ty = _cell_value_pos(x0, y0, cell, i, j)
            svg.text(tx, ty, str(mat[i][j]),
                     weight="bold" if on_path else "normal",
                     fill=COLOR_PRIMARY if on_path else COLOR_TEXT)
    for i in range(1, 5):
        for j in range(1, 5):
            on_path = (i, j) in path
            _src_arrows(svg, x0, y0, cell, i, j, srcs[i][j],
                        color=COLOR_PRIMARY if on_path else COLOR_MUTED)
    svg.rect(x0 + 0 * cell + 2, y0 + 1 * cell + 2, cell - 4, cell - 4, fill=COLOR_FILL, sw=0)
    svg.text(x0 + 0 * cell + 9, y0 + 1 * cell + 21, str(mat[1][0]), weight="bold", fill=COLOR_PRIMARY)
    svg.rect(x0 + 4 * cell + 2, y0 + 4 * cell + 2, cell - 4, cell - 4,
             fill="none", stroke=COLOR_PRIMARY, sw=2.2)
    y = y0 + 5 * cell + 48
    svg.text(x0 - 70, y, "最优比对（得分 5）：", mono=False, size=SIZE_LABEL)
    svg.seq(x0 + 120, y, "A A G - T", weight="bold", fill=COLOR_PRIMARY)
    svg.seq(x0 + 120, y + 26, "- A G C T", weight="bold", fill=COLOR_PRIMARY)
    svg.text(x0 + 320, y + 13, "（加粗格与绿色箭头为回溯路径）", mono=False,
             size=SIZE_NOTE, fill=COLOR_MUTED)
    save("pairwise-03-nw-matrix", svg)


def fig_sw_matrix():
    x0, y0, cell = 130, 100, 58
    w, h = 720, 560
    mat = _sw_matrix()
    srcs = _sources(mat, sw=True)
    svg = Svg(w, h, "Smith-Waterman 局部比对填表结果",
              "数值在格左上角，右下角小箭头为取值来源；记 0 的格子无箭头；"
              "两个最高分 10（加框）分别回溯得到两个最优局部比对。")
    svg.text(x0 - 70, 44, "Smith-Waterman 局部比对", mono=False, size=SIZE_TITLE, weight="bold")
    _dp_grid_frame(svg, x0, y0, cell, init=[[0]*5 for _ in range(5)], skip={(0, 0), (1, 0)})
    path1 = {(3, 2), (2, 1)}
    path2 = {(4, 4), (3, 3), (3, 2), (2, 1)}
    for i in range(1, 5):
        for j in range(1, 5):
            in1 = (i, j) in path1
            in2 = (i, j) in path2
            if in1 or in2:
                svg.rect(x0 + j * cell + 2, y0 + i * cell + 2, cell - 4, cell - 4,
                         fill=COLOR_FILL if in1 else COLOR_WARN_FILL, sw=0)
    for i in range(1, 5):
        for j in range(1, 5):
            tx, ty = _cell_value_pos(x0, y0, cell, i, j)
            val = mat[i][j]
            svg.text(tx, ty, str(val),
                     weight="bold" if val == 10 else "normal",
                     fill=COLOR_PRIMARY if val == 10 else COLOR_TEXT)
    for i in range(1, 5):
        for j in range(1, 5):
            if mat[i][j] == 0:
                continue
            in1 = (i, j) in path1
            in2 = (i, j) in path2
            _src_arrows(svg, x0, y0, cell, i, j, srcs[i][j],
                        color=(COLOR_PRIMARY if in1 else (COLOR_WARN if in2 else COLOR_MUTED)))
    svg.rect(x0 + 0 * cell + 2, y0 + 1 * cell + 2, cell - 4, cell - 4, fill=COLOR_FILL, sw=0)
    for (i, j) in [(3, 2), (4, 4)]:
        svg.rect(x0 + j * cell + 2, y0 + i * cell + 2, cell - 4, cell - 4,
                 fill="none", stroke=COLOR_PRIMARY, sw=2.2)
    y = y0 + 5 * cell + 48
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
