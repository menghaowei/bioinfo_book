"""生成第4章全部序列示意图 SVG。

运行：python3 scripts/figures/ch04/generate_all.py
输出：assets/04-quality-control-and-alignment/svg/*.svg

内容均依据以下可核实来源重新绘制：
- BWT/哈希表/双序列比对：按算法逐步重算（示例 ACAACG、ATGCT、AAGT/AGCT）；
- CIGAR 示例：SAM 官方规范 SAMv1 第 1.4 节的参考序列与 reads；
- 可变剪接、FASTQ→SAM 流程、GTF 示例：按正文内容自绘。
"""

from common import (Svg, save, MONO, SANS, COLOR_TEXT, COLOR_MUTED, COLOR_PRIMARY,
                    COLOR_FILL, COLOR_WARN, COLOR_WARN_FILL, COLOR_LINE,
                    SIZE_SEQ, SIZE_LABEL, SIZE_TITLE, SIZE_NOTE, CHAR_W, ROW_H)

# ---------------------------------------------------------------- BWT 系列

BWT_TEXT = "ACAACG"


def rotations(t):
    """返回 t 的全部循环旋转（左移一位）。"""
    n = len(t)
    return [t[i:] + t[:i] for i in range(n)]


def bwt_matrix_rows():
    rows = sorted(rotations(BWT_TEXT + "$"))
    f = [r[0] for r in rows]
    l = [r[-1] for r in rows]
    return rows, f, l


def fig_bwt_rotations():
    rows = rotations(BWT_TEXT + "$")
    x0, y0 = 70, 70
    w, h = 560, y0 + len(rows) * ROW_H + 74
    svg = Svg(w, h, "BWT 构建第 1 步：写出全部循环旋转",
              "对 ACAACG 加结束符 $ 后写出 7 个循环旋转，第一行是原序列本身。")
    svg.text(x0, 40, "第 1 步：给 ACAACG 末尾加上 $，写出全部 7 个循环旋转",
             mono=False, size=SIZE_TITLE, weight="bold")
    for i, r in enumerate(rows):
        y = y0 + i * ROW_H + 16
        if i == 0:
            svg.rect(x0 - 14, y - 17, (len(r) + 2) * CHAR_W, 24, fill=COLOR_FILL)
        svg.seq(x0, y, r)
    svg.text(x0, y0 + len(rows) * ROW_H + 18,
             "高亮的第一行就是原序列 ACAACG$；其余每一行都是把它循环左移一位得到，$ 只出现在结尾。",
             mono=False, size=SIZE_NOTE, fill=COLOR_MUTED)
    save("bwt-01-rotations", svg)


def fig_bwt_sorted():
    rows, f, l = bwt_matrix_rows()
    x0, y0 = 70, 70
    w, h = 620, y0 + len(rows) * ROW_H + 96
    svg = Svg(w, h, "BWT 构建第 2 步：排序后的旋转矩阵与 F、L 列",
              "全部循环旋转按 $<A<C<G 排序；第一列为 F 列，最后一列为 L 列（BWT）。")
    svg.text(x0, 40, "第 2 步：把 7 个旋转按 $ < A < C < G 排序",
             mono=False, size=SIZE_TITLE, weight="bold")
    for i, r in enumerate(rows):
        y = y0 + i * ROW_H + 16
        svg.seq(x0, y, r)
        # F 列：绿色框
        svg.rect(x0 - 14, y - 17, 22, 24, fill=COLOR_FILL, sw=1.4)
        # L 列：琥珀框
        lx = x0 + (len(r) - 1) * CHAR_W - 4
        svg.rect(lx, y - 17, 22, 24, fill=COLOR_WARN_FILL, stroke=COLOR_WARN, sw=1.4)
    svg.text(x0 - 14, y0 + len(rows) * ROW_H + 16, "F 列 = 排序矩阵的第一列",
             mono=False, size=SIZE_LABEL, fill=COLOR_PRIMARY, weight="bold")
    svg.text(x0 + 100, y0 + len(rows) * ROW_H + 16,
             "L 列 = 最后一列，即 BWT = GC$AAAC",
             mono=False, size=SIZE_LABEL, fill=COLOR_WARN, weight="bold")
    svg.text(x0, y0 + len(rows) * ROW_H + 40,
             "第 3 步：把 L 列从上到下连起来，就得到 BWT 字符串 GC$AAAC（7 个字符）。",
             mono=False, size=SIZE_NOTE, fill=COLOR_MUTED)
    save("bwt-02-sorted-matrix", svg)


def _decode_base(svg, x0, y0):
    """画解码步骤图共用的 F/L 双列与行号，返回 (fx, lx)。"""
    rows, f, l = bwt_matrix_rows()
    svg.text(x0, y0 - 14, "F 列", mono=False, size=SIZE_LABEL,
             fill=COLOR_PRIMARY, weight="bold")
    fx = x0 + 24
    lx = x0 + 150
    svg.text(lx - 20, y0 - 14, "L 列", mono=False, size=SIZE_LABEL,
             fill=COLOR_WARN, weight="bold")
    for i, (fc, lc) in enumerate(zip(f, l)):
        y = y0 + i * ROW_H + 16
        svg.text(x0 - 26, y, f"{i + 1}", size=SIZE_LABEL, fill=COLOR_MUTED)
        svg.text(fx, y, fc)
        svg.text(lx, y, lc)
    return fx, lx


def _cell_xy(x, y0, i):
    return x, y0 + i * ROW_H + 16 - 6


def fig_bwt_decode(step):
    rows, f, l = bwt_matrix_rows()
    x0, y0 = 70, 84
    w = 640
    notes = {
        1: ("第 1 步：确定原序列的最后一个字符",
            "排序后第 1 行是 $ACAACG，即原序列本身；它末尾的 G 就是原序列最后一个字符。",
            "G"),
        2: ("第 2 步：LF 映射走一步，确定 G 前面的字符",
            "L 列第 1 个 G 对应 F 列第 1 个 G（第 7 行）；第 7 行的 L 是 C，说明 G 前面是 C。",
            "GC"),
        3: ("第 3 步：继续 LF 映射，确定 C 前面的字符",
            "第 7 行的 C 是 L 列第 2 个 C，对应 F 列第 2 个 C（第 6 行）；第 6 行的 L 是 A。",
            "GCA"),
    }
    title, note, cur = notes[step]
    h = y0 + 7 * ROW_H + 110
    svg = Svg(w, h, f"BWT 解码{title}",
              f"{note}当前还原结果为 {cur}。")
    svg.text(x0, 44, title, mono=False, size=SIZE_TITLE, weight="bold")
    fx, lx = _decode_base(svg, x0, y0)

    if step == 1:
        c1 = _cell_xy(fx, y0, 0)
        c2 = _cell_xy(lx, y0, 0)
        svg.rect(fx - 10, y0 + 0 * ROW_H + 16 - 17, 22, 24, fill=COLOR_FILL, sw=1.4)
        svg.rect(lx - 10, y0 + 0 * ROW_H + 16 - 17, 22, 24,
                 fill=COLOR_WARN_FILL, stroke=COLOR_WARN, sw=1.4)
        svg.arrow(c1[0] + 12, c1[1], c2[0] - 14, c2[1])
    elif step == 2:
        svg.rect(lx - 10, y0 + 0 * ROW_H + 16 - 17, 22, 24,
                 fill=COLOR_WARN_FILL, stroke=COLOR_WARN, sw=1.4)
        svg.rect(fx - 10, y0 + 6 * ROW_H + 16 - 17, 22, 24, fill=COLOR_FILL, sw=1.4)
        svg.rect(lx - 10, y0 + 6 * ROW_H + 16 - 17, 22, 24,
                 fill=COLOR_WARN_FILL, stroke=COLOR_WARN, sw=1.4)
        c1 = _cell_xy(lx, y0, 0)
        c2 = _cell_xy(fx, y0, 6)
        svg.arrow(c1[0] + 12, c1[1] + 2, c2[0] + 20, c2[1] + 4)
        c3 = _cell_xy(fx, y0, 6)
        c4 = _cell_xy(lx, y0, 6)
        svg.arrow(c3[0] + 12, c3[1] + 8, c4[0] - 14, c4[1] + 8)
    else:
        svg.rect(lx - 10, y0 + 6 * ROW_H + 16 - 17, 22, 24,
                 fill=COLOR_WARN_FILL, stroke=COLOR_WARN, sw=1.4)
        svg.rect(fx - 10, y0 + 5 * ROW_H + 16 - 17, 22, 24, fill=COLOR_FILL, sw=1.4)
        svg.rect(lx - 10, y0 + 5 * ROW_H + 16 - 17, 22, 24,
                 fill=COLOR_WARN_FILL, stroke=COLOR_WARN, sw=1.4)
        c1 = _cell_xy(lx, y0, 6)
        c2 = _cell_xy(fx, y0, 5)
        svg.arrow(c1[0] + 12, c1[1] + 2, c2[0] + 20, c2[1])
        c3 = _cell_xy(fx, y0, 5)
        c4 = _cell_xy(lx, y0, 5)
        svg.arrow(c3[0] + 12, c3[1] + 8, c4[0] - 14, c4[1] + 8)

    ytext = y0 + 7 * ROW_H + 26
    svg.text(x0, ytext, note, mono=False, size=SIZE_NOTE, fill=COLOR_MUTED)
    svg.text(x0, ytext + 28, "当前还原结果（从后往前）：", mono=False, size=SIZE_LABEL)
    svg.seq(x0 + 210, ytext + 28, cur, weight="bold", fill=COLOR_PRIMARY)
    save(f"bwt-0{step + 2}-decode-step{step}", svg)


def fig_bwt_decode_rest():
    x0, y0 = 70, 70
    rows_def = [
        ("4", "第 6 行的 A（L 列第 3 个 A）", "第 3 行的 A", "第 3 行的 L：A", "GCAA"),
        ("5", "第 3 行的 A（L 列第 1 个 A）", "第 2 行的 A", "第 2 行的 L：C", "GCAAC"),
        ("6", "第 2 行的 C（L 列第 1 个 C）", "第 5 行的 C", "第 5 行的 L：A", "GCAACA"),
    ]
    w, h = 760, 330
    svg = Svg(w, h, "BWT 解码第 4—6 步与最终还原",
              "按 LF 映射继续回溯得到 GCAA、GCAAC、GCAACA；逆序即原序列 ACAACG。")
    svg.text(x0, 44, "第 4—6 步：继续 LF 映射，直到把序列补全", mono=False,
             size=SIZE_TITLE, weight="bold")
    heads = ["步骤", "当前字符（L 列）", "对应 F 列", "新确定的字符", "当前还原结果"]
    xs = [x0, x0 + 50, x0 + 280, x0 + 410, x0 + 570]
    for i, hd in enumerate(heads):
        svg.text(xs[i], y0 + 6, hd, mono=False, size=SIZE_LABEL, fill=COLOR_MUTED)
    for j, (st, cur, fmap, newch, res) in enumerate(rows_def):
        y = y0 + 40 + j * 44
        svg.text(xs[0], y, st)
        svg.text(xs[1], y, cur, mono=False, size=SIZE_LABEL)
        svg.text(xs[2], y, fmap, mono=False, size=SIZE_LABEL)
        svg.text(xs[3], y, newch, mono=False, size=SIZE_LABEL)
        svg.text(xs[4], y, res, weight="bold", fill=COLOR_PRIMARY)
        svg.line(x0 - 10, y + 12, x0 + 660, y + 12, stroke="#e5e7eb", sw=1)
    y = y0 + 40 + 3 * 44 + 8
    svg.seq(x0, y, "GCAACA")
    svg.text(x0 + 90, y, "逆序阅读", mono=False, size=SIZE_LABEL, fill=COLOR_MUTED)
    svg.arrow(x0 + 160, y - 5, x0 + 210, y - 5)
    svg.seq(x0 + 220, y, "ACAACG", weight="bold", fill=COLOR_PRIMARY)
    svg.text(x0 + 310, y, "= 原序列，解码成功", mono=False, size=SIZE_LABEL, fill=COLOR_PRIMARY)
    save("bwt-06-decode-steps4-6", svg)


# ---------------------------------------------------------------- 哈希表系列

def fig_hash_encoding():
    seq = "ATGCT"
    digits = "01321"
    powers = ["4⁴", "4³", "4²", "4¹", "4⁰"]
    x0, y0 = 90, 74
    w, h = 620, 260
    svg = Svg(w, h, "碱基的四进制编码",
              "把 A、T、G、C 分别编码为 0、1、3、2，按最左位权值最高计算，ATGCT 的关键码为 121。")
    svg.text(x0, 40, "把碱基编码成数字：A→0，T→1，G→3，C→2", mono=False,
             size=SIZE_TITLE, weight="bold")
    for i, ch in enumerate(seq):
        x = x0 + i * 64
        svg.rect(x - 12, y0 - 22, 44, 46, fill=COLOR_FILL if i == 0 else "none")
        svg.text(x + 10, y0, ch, size=20, weight="bold")
        svg.text(x + 10, y0 + 26, digits[i], fill=COLOR_PRIMARY, weight="bold")
        svg.text(x + 4, y0 + 52, powers[i], size=SIZE_LABEL, fill=COLOR_MUTED)
    svg.line(x0 - 10, y0 + 66, x0 + 5 * 64 - 20, y0 + 66, stroke=COLOR_LINE)
    y = y0 + 100
    svg.text(x0 - 30, y, "H(ATGCT) = 0×4⁴ + 1×4³ + 3×4² + 2×4¹ + 1×4⁰ = 0 + 64 + 48 + 8 + 1 = ",
             size=SIZE_LABEL)
    svg.text(x0 + 480, y, "121", size=18, weight="bold", fill=COLOR_PRIMARY)
    svg.text(x0 - 30, y + 30, "最左边的碱基权值最高（4⁴），最右边的碱基权值最低（4⁰）。",
             mono=False, size=SIZE_NOTE, fill=COLOR_MUTED)
    save("hash-01-base-encoding", svg)


def fig_hash_kmer_table():
    ref = "ATGCGTAACT"
    x0, y0 = 90, 74
    w, h = 720, 300
    svg = Svg(w, h, "k-mer 哈希表的构建（k=5）",
              "参考序列的全部 5-mer 作为关键码，哈希表记录每个 5-mer 出现的位置。")
    svg.text(x0, 40, "把参考序列拆成 k-mer（k=5），建立哈希表", mono=False,
             size=SIZE_TITLE, weight="bold")
    # 参考序列与位置刻度
    svg.seq(x0, y0 + 10, ref)
    for i in range(len(ref)):
        svg.text(x0 + i * CHAR_W - 4, y0 + 30, str(i + 1), size=10, fill=COLOR_MUTED)
    # 前两个 k-mer 的覆盖框
    svg.rect(x0 - 4, y0 - 14, 5 * CHAR_W, 22, fill="none", stroke=COLOR_PRIMARY)
    svg.rect(x0 + CHAR_W - 4, y0 - 14 + 26, 5 * CHAR_W, 22, fill="none", stroke=COLOR_WARN)
    svg.text(x0 + 5 * CHAR_W + 10, y0 + 2, "ATGCG（k-mer 1）", size=SIZE_LABEL, fill=COLOR_PRIMARY)
    svg.text(x0 + 6 * CHAR_W + 10, y0 + 44, "TGCGT（k-mer 2）", size=SIZE_LABEL, fill=COLOR_WARN)
    # 哈希表
    tx, ty = x0 + 320, y0 - 4
    svg.rect(tx, ty - 18, 280, 168, stroke=COLOR_LINE, rx=6)
    svg.text(tx + 16, ty + 4, "哈希表（关键码 → 位置）", mono=False, size=SIZE_LABEL,
             weight="bold", fill=COLOR_PRIMARY)
    table = [("ATGCG", "1"), ("TGCGT", "2"), ("GCGTA", "3"), ("CGTAA", "4"), ("…", "…")]
    for j, (kmer, pos) in enumerate(table):
        y = ty + 34 + j * 26
        svg.seq(tx + 16, y, kmer)
        svg.text(tx + 100, y, "→", fill=COLOR_MUTED)
        svg.seq(tx + 130, y, pos)
    svg.text(x0, ty + 190, "检索时把 read 拆成 k-mer，先在哈希表中查位置，再做延伸比对。",
             mono=False, size=SIZE_NOTE, fill=COLOR_MUTED)
    svg.text(x0, ty + 212, "同一个 k-mer 在基因组中可能出现多次，哈希表会记录全部位置。",
             mono=False, size=SIZE_NOTE, fill=COLOR_MUTED)
    save("hash-02-kmer-table", svg)


def fig_hash_pigeonhole():
    read = "ATGCGT" + "TACGTA" + "CGTACG" + "GTACGT"
    segs = [read[i:i + 6] for i in range(0, 24, 6)]
    segs[1] = "TAAGTA"  # 第 2 段带一个错配
    x0, y0 = 70, 70
    w, h = 700, 320
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
    # 基因组线
    gy = y0 + 140
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

SEQ1 = "AAGT"   # 行
SEQ2 = "AGCT"   # 列
NW = [
    [0, -5, -10, -15, -20],
    [-5, 5, 0, -5, -10],
    [-10, 0, 1, -4, -9],
    [-15, -5, 5, 0, -5],
    [-20, -10, 0, 1, 5],
]
SW = [
    [0, 0, 0, 0, 0],
    [0, 5, 0, 0, 0],
    [0, 5, 1, 0, 0],
    [0, 0, 10, 5, 0],
    [0, 0, 5, 6, 10],
]


def _dp_grid(svg, x0, y0, cell=52):
    """画 DP 表格头（第 0 行/列 + 碱基），返回单元格左上角坐标函数。"""
    svg.text(x0 + cell // 2 - 6, y0 - 12, "∅", fill=COLOR_MUTED)
    for j, b in enumerate(SEQ2):
        svg.text(x0 + (j + 1) * cell + cell // 2 - 6, y0 - 12, b, weight="bold",
                 fill=COLOR_PRIMARY)
    svg.text(x0 - 88, y0 + 12, "seq2 →", mono=False, size=SIZE_LABEL, fill=COLOR_MUTED)
    for i, b in enumerate(SEQ1):
        svg.text(x0 - 26, y0 + (i + 1) * cell + 20, b, weight="bold", fill=COLOR_PRIMARY)
    svg.text(x0 - 30, y0 + 2 * cell, "seq1", mono=False, size=SIZE_LABEL, fill=COLOR_MUTED)
    for i in range(5):
        for j in range(5):
            svg.line(x0 + j * cell, y0 + i * cell, x0 + 5 * cell, y0 + i * cell,
                     stroke="#e5e7eb", sw=1)
            svg.line(x0 + j * cell, y0 + i * cell, x0 + j * cell, y0 + 5 * cell,
                     stroke="#e5e7eb", sw=1)
    return lambda i, j: (x0 + j * cell + cell // 2 - 12, y0 + i * cell + cell // 2 + 6)


def fig_scoring_matrix():
    bases = "AGCT"
    x0, y0, cell = 110, 84, 62
    w, h = 560, 380
    svg = Svg(w, h, "双序列比对示例的打分矩阵",
              "match 得 5 分，mismatch 扣 4 分，空位罚分 d=-5。")
    svg.text(x0 - 30, 40, "打分矩阵与空位罚分", mono=False, size=SIZE_TITLE, weight="bold")
    for j, b in enumerate(bases):
        svg.text(x0 + (j + 1) * cell + cell // 2 - 6, y0 - 14, b, weight="bold",
                 fill=COLOR_PRIMARY)
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
            svg.text(x + (cell - 12) // 2 - 10, y + 4, "5" if match else "-4",
                     weight="bold", fill=COLOR_PRIMARY if match else COLOR_WARN)
    y = y0 + 5 * cell + 30
    svg.rect(x0, y, 320, 40, stroke=COLOR_PRIMARY, fill="none")
    svg.text(x0 + 20, y + 26, "空位罚分 d = -5（每个空位扣 5 分）", mono=False,
             size=SIZE_LABEL, weight="bold", fill=COLOR_PRIMARY)
    save("pairwise-01-scoring-matrix", svg)


def fig_empty_grid():
    x0, y0 = 120, 90
    w, h = 480, 400
    svg = Svg(w, h, "待填写的双序列比对动态规划表格",
              "行为 seq1=AAGT，列为 seq2=AGCT，表格用于 Needleman-Wunsch 与 Smith-Waterman 填表。")
    svg.text(x0 - 60, 40, "动态规划表格（待填写）", mono=False, size=SIZE_TITLE, weight="bold")
    svg.text(x0 + 30, y0 - 30, "列：seq2 = A G C T", mono=False, size=SIZE_LABEL, fill=COLOR_MUTED)
    svg.text(x0 - 60, y0 + 160, "行：seq1 = A A G T", mono=False, size=SIZE_LABEL,
             fill=COLOR_MUTED)
    _dp_grid(svg, x0, y0)
    save("pairwise-02-empty-grid", svg)


def _traceback_arrow(svg, c1, c2, cell, color):
    x1, y1 = c1
    x2, y2 = c2
    import math
    ang = math.atan2(y2 - y1, x2 - x1)
    r = cell * 0.62
    cx = x2 - r * math.cos(ang)
    cy = y2 - r * math.sin(ang)
    svg.arrow(cx, cy, x2 - 8 * math.cos(ang), y2 - 8 * math.sin(ang), stroke=color, sw=1.8)


def fig_nw_matrix():
    x0, y0, cell = 120, 90, 52
    w, h = 620, 470
    svg = Svg(w, h, "Needleman-Wunsch 全局比对填表结果",
              "右下角最优得分 5；虚线为回溯路径，对应比对 AAG-T / -AGCT。")
    svg.text(x0 - 70, 40, "Needleman-Wunsch 全局比对", mono=False, size=SIZE_TITLE, weight="bold")
    xy = _dp_grid(svg, x0, y0, cell)
    for i in range(5):
        for j in range(5):
            x, y = xy(i, j)
            svg.text(x, y, str(NW[i][j]))
    # 最终格高亮
    fx, fy = xy(4, 4)
    svg.rect(fx - 16, fy - 22, cell - 8, cell - 8, fill=COLOR_FILL, sw=1.6)
    svg.text(fx, fy, "5", weight="bold", fill=COLOR_PRIMARY)
    # 回溯箭头：(4,4)←(3,3) 对角；(3,3)←(3,2) 左；(3,2)←(2,1) 对角；(2,1)←(1,0) 对角
    for (i1, j1, i2, j2) in [(4, 4, 3, 3), (3, 3, 3, 2), (3, 2, 2, 1), (2, 1, 1, 0)]:
        _traceback_arrow(svg, xy(i2, j2), xy(i1, j1), cell, COLOR_PRIMARY)
    # 结果
    y = y0 + 5 * cell + 40
    svg.text(x0 - 70, y, "最优比对（得分 5）：", mono=False, size=SIZE_LABEL)
    svg.seq(x0 + 120, y, "A A G - T", weight="bold", fill=COLOR_PRIMARY)
    svg.seq(x0 + 120, y + 26, "- A G C T", weight="bold", fill=COLOR_PRIMARY)
    svg.text(x0 + 300, y + 13, "（把两端的 A、T 对齐，中间用空位消化差异）",
             mono=False, size=SIZE_NOTE, fill=COLOR_MUTED)
    save("pairwise-03-nw-matrix", svg)


def fig_sw_matrix():
    x0, y0, cell = 120, 90, 52
    w, h = 640, 500
    svg = Svg(w, h, "Smith-Waterman 局部比对填表结果",
              "矩阵最高分 10 有两处：分别回溯得到 AG/AG 与 AG-T/AGCT 两个最优局部比对。")
    svg.text(x0 - 70, 40, "Smith-Waterman 局部比对", mono=False, size=SIZE_TITLE, weight="bold")
    xy = _dp_grid(svg, x0, y0, cell)
    for i in range(5):
        for j in range(5):
            x, y = xy(i, j)
            svg.text(x, y, str(SW[i][j]))
    # 两个最高分 10
    for (i, j) in [(3, 2), (4, 4)]:
        x, y = xy(i, j)
        svg.rect(x - 16, y - 22, cell - 8, cell - 8, fill=COLOR_FILL, sw=1.6)
        svg.text(x, y, "10", weight="bold", fill=COLOR_PRIMARY)
    # 路径1（绿）：(3,2)←(2,1)←(1,0)
    for (i1, j1, i2, j2) in [(3, 2, 2, 1), (2, 1, 1, 0)]:
        _traceback_arrow(svg, xy(i2, j2), xy(i1, j1), cell, COLOR_PRIMARY)
    # 路径2（琥珀）：(4,4)←(3,3)左←(3,2)对角←(2,1)←(1,0)
    for (i1, j1, i2, j2) in [(4, 4, 3, 3), (3, 3, 3, 2), (3, 2, 2, 1), (2, 1, 1, 0)]:
        _traceback_arrow(svg, xy(i2, j2), xy(i1, j1), cell, COLOR_WARN)
    y = y0 + 5 * cell + 36
    svg.text(x0 - 70, y, "两个并列最优（各 10 分）：", mono=False, size=SIZE_LABEL)
    svg.seq(x0 + 170, y, "A G", weight="bold", fill=COLOR_PRIMARY)
    svg.seq(x0 + 170, y + 24, "A G", weight="bold", fill=COLOR_PRIMARY)
    svg.text(x0 + 240, y + 13, "；", mono=False)
    svg.seq(x0 + 270, y, "A G - T", weight="bold", fill=COLOR_WARN)
    svg.seq(x0 + 270, y + 24, "A G C T", weight="bold", fill=COLOR_WARN)
    svg.text(x0 - 70, y + 60, "回溯从最高分单元格开始，遇到 0 停止；两条路径分别对应上图绿色与琥珀色箭头。",
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
