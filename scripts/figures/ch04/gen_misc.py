"""生成第4章其余示意图 SVG：FASTQ→SAM 流程、可变剪接、GTF 示例、CIGAR 示例。

运行：python3 scripts/figures/ch04/gen_misc.py
CIGAR 示例内容依据 SAM 官方规范（SAMv1 第 1.4 节）的参考序列与 reads 重绘。
"""

from common import (Svg, save, COLOR_TEXT, COLOR_MUTED, COLOR_PRIMARY,
                    COLOR_FILL, COLOR_WARN, COLOR_WARN_FILL, COLOR_LINE,
                    SIZE_SEQ, SIZE_LABEL, SIZE_TITLE, SIZE_NOTE, CHAR_W, ROW_H)


def fig_pipeline():
    """竖版技术路线：自上而下流动，适配正文单栏与窄屏。"""
    w, h = 560, 860
    svg = Svg(w, h, "从 FASTQ 到 SAM/BAM 的技术路线（竖版）",
              "FASTQ 经质控得到 clean reads，借助索引比对得到 SAM，"
              "再转换为排序索引的 BAM，经检查后进入下游分析。")
    cx = w // 2
    svg.text(cx, 40, "从 FASTQ 到比对结果", mono=False, size=SIZE_TITLE,
             weight="bold", anchor="middle")
    nodes = [
        ("FASTQ", "原始测序数据", "data"),
        ("质控", "FastQC / cutadapt", "tool"),
        ("clean reads", "质控后的数据", "data"),
        ("比对", "bowtie2 / bwa + 索引", "tool"),
        ("SAM", "比对结果", "data"),
        ("BAM", "转换 + 排序 + 索引", "data"),
        ("检查", "qualimap / IGV", "tool"),
        ("下游分析", "表达量 / 变异 / 峰", "data"),
    ]
    bw, bh, gap = 300, 52, 42
    y = 66
    centers = []
    for name, sub, kind in nodes:
        fill = COLOR_FILL if kind == "data" else "none"
        stroke = COLOR_PRIMARY if kind == "data" else COLOR_LINE
        svg.rect(cx - bw // 2, y, bw, bh, fill=fill, stroke=stroke)
        svg.text(cx, y + 22, name, mono=(kind == "data"), anchor="middle",
                 weight="bold", fill=COLOR_PRIMARY if kind == "data" else COLOR_TEXT)
        svg.text(cx, y + 40, sub, mono=False, size=SIZE_NOTE, anchor="middle",
                 fill=COLOR_MUTED)
        centers.append((cx, y, y + bh))
        y += bh + gap
    for k in range(len(centers) - 1):
        _, _, ybot = centers[k]
        _, ytop, _ = centers[k + 1]
        svg.arrow(cx, ybot + 4, cx, ytop - 4)
    save("fastq-to-sam-pipeline", svg)


def fig_splicing():
    w, h = 760, 320
    svg = Svg(w, h, "可变剪接示意图",
              "同一个基因经不同的剪接方式，从一条 pre-mRNA 生成多种成熟 mRNA。")
    ex_w, gap, ey = 92, 46, 84
    xs = [70 + i * (ex_w + gap) for i in range(4)]
    svg.text(xs[0], 46, "DNA / pre-mRNA", mono=False, size=SIZE_TITLE, weight="bold")
    for i, x in enumerate(xs):
        svg.rect(x, ey, ex_w, 36, fill=COLOR_FILL, stroke=COLOR_PRIMARY)
        svg.text(x + ex_w // 2 - 6, ey + 24, str(i + 1), weight="bold", fill=COLOR_PRIMARY)
        if i < 3:
            svg.line(x + ex_w, ey + 18, xs[i + 1], ey + 18, stroke=COLOR_LINE, sw=1.6)
            # 剪接折线
            mx = (x + ex_w + xs[i + 1]) / 2
            svg.line(mx, ey + 6, mx, ey + 30, stroke=COLOR_WARN, sw=1.2, dash="3 3")
    svg.text(xs[0] + ex_w + 6, ey - 10, "外显子（exon）", mono=False, size=SIZE_NOTE,
             fill=COLOR_MUTED)
    svg.text(xs[0] + ex_w + 52, ey + 52, "内含子（intron）", mono=False, size=SIZE_NOTE,
             fill=COLOR_MUTED)

    variants = [
        ("组成型", [1, 2, 3, 4], False),
        ("外显子跳跃", [1, 2, 4], False),
        ("内含子保留", [1, 2, 3, 4], True),
    ]
    for vi, (name, keep, retained) in enumerate(variants):
        vy = 168 + vi * 46
        svg.text(70, vy + 20, name, mono=False, size=SIZE_LABEL, weight="bold")
        cx = 210
        for idx in keep:
            svg.rect(cx, vy, ex_w, 26, fill=COLOR_FILL, stroke=COLOR_PRIMARY)
            svg.text(cx + ex_w // 2 - 6, vy + 19, str(idx), fill=COLOR_PRIMARY)
            cx += ex_w
            if idx != keep[-1]:
                nxt = keep[keep.index(idx) + 1]
                gapw = ex_w + gap if nxt == idx + 1 else ex_w + gap
                if retained and idx == 3:
                    svg.line(cx, vy + 13, cx + ex_w + gap, vy + 13, stroke=COLOR_WARN, sw=2.4)
                    svg.text(cx + ex_w + gap // 2 - 40, vy - 4, "保留的内含子",
                             mono=False, size=SIZE_NOTE, fill=COLOR_WARN)
                    cx += ex_w + gap
                else:
                    svg.line(cx, vy + 13, cx + gap, vy + 13, stroke=COLOR_LINE, sw=1.2)
                    cx += gap
    svg.text(70, 306, "同一个基因经可变剪接可以产生多种成熟 mRNA，进而在蛋白水平产生多样性。",
             mono=False, size=SIZE_NOTE, fill=COLOR_MUTED)
    save("alternative-splicing", svg)


GTF_COLS = ["seqname", "source", "feature", "start", "end", "score", "strand", "frame", "attribute"]
GTF_ROWS = [
    ("chr1", "hg19_ncbiRefSeq", "exon", "66999252", "66999355", "0.000000", "+", ".",
     'gene_id "SGIP1"; transcript_id "NM_001308203.1";'),
    ("chr1", "hg19_ncbiRefSeq", "start_codon", "67000042", "67000044", "0.000000", "+", ".",
     'gene_id "SGIP1"; transcript_id "NM_001308203.1";'),
    ("chr1", "hg19_ncbiRefSeq", "CDS", "67000042", "67000051", "0.000000", "+", "0",
     'gene_id "SGIP1"; transcript_id "NM_001308203.1";'),
    ("chr1", "hg19_ncbiRefSeq", "exon", "66999929", "67000051", "0.000000", "+", ".",
     'gene_id "SGIP1"; transcript_id "NM_001308203.1";'),
    ("chr1", "hg19_ncbiRefSeq", "CDS", "67208756", "67208775", "0.000000", "+", "2",
     'gene_id "SGIP1"; transcript_id "NM_001308203.1";'),
]


def fig_gtf_example():
    widths = [5, 15, 12, 9, 9, 9, 6, 5, 50]
    x0, y0 = 46, 76
    w = sum(widths) * CHAR_W + x0 * 2
    h = y0 + (len(GTF_ROWS) + 1) * ROW_H + 70
    svg = Svg(w, h, "标准 GTF 格式文件示例",
              "GTF 每行 9 列，以 TAB 分隔；示例为人类 SGIP1 基因的部分注释行。")
    svg.text(x0, 42, "一个标准 GTF 文件的示例（人类 SGIP1 基因，节选）", mono=False,
             size=SIZE_TITLE, weight="bold")
    # 列头
    cx = x0
    for name, wd in zip(GTF_COLS, widths):
        svg.text(cx, y0, name, size=SIZE_LABEL, fill=COLOR_MUTED)
        cx += wd * CHAR_W
    # 列分隔线
    total_w = sum(widths) * CHAR_W
    for ri, row in enumerate(GTF_ROWS):
        ry = y0 + (ri + 1) * ROW_H + 8
        if ri == 0:
            svg.rect(x0 - 8, ry - 18, total_w + 16, 24, fill=COLOR_FILL, sw=0)
        cx = x0
        for val, wd in zip(row, widths):
            svg.seq(cx, ry, val, size=SIZE_LABEL)
            cx += wd * CHAR_W
    cx = x0
    for wd in widths[:-1]:
        cx += wd * CHAR_W
        svg.line(cx, y0 - 14, cx, y0 + len(GTF_ROWS) * ROW_H + 12,
                 stroke="#e5e7eb", sw=1)
    ynote = y0 + (len(GTF_ROWS) + 1) * ROW_H + 34
    svg.text(x0, ynote, "高亮行是 SGIP1 的第一个 exon（66999252-66999355），正文问答 24 用它演示转录本坐标换算。",
             mono=False, size=SIZE_NOTE, fill=COLOR_MUTED)
    svg.text(x0, ynote + 22, "完整文件中还有更多行；无论行数多少，每行都是同样的 9 列结构。",
             mono=False, size=SIZE_NOTE, fill=COLOR_MUTED)
    save("gtf-example", svg)


# SAM 规范（SAMv1 §1.4）官方示例数据
REF = "AGCATGTTAGATAAGATAGCTGTGCTAGTAGGCAGTCAGCGCCAT"


def fig_cigar():
    x0, ruler_y = 96, 78
    w = x0 + len(REF) * CHAR_W + 190
    h = 478
    svg = Svg(w, h, "reads 比对到参考序列的示意（CIGAR 操作符）",
              "依据 SAM 规范官方示例绘制：展示 M、I、D、N、S、H 等 CIGAR 操作符的含义。")
    svg.text(x0, 42, "reads 比对到参考序列（依据 SAM 规范官方示例重绘）", mono=False,
             size=SIZE_TITLE, weight="bold")
    # 参考序列与刻度
    svg.text(x0 - 46, ruler_y, "REF", size=SIZE_LABEL, fill=COLOR_MUTED)
    svg.seq(x0, ruler_y, REF, size=SIZE_LABEL)
    for p in [1, 5, 10, 15, 20, 25, 30, 35, 40, 45]:
        svg.text(x0 + (p - 1) * CHAR_W - 8, ruler_y - 16, str(p), size=10, fill=COLOR_MUTED)

    def col(p):
        """参考位置 p（1-based）对应画布 x 坐标。"""
        return x0 + (p - 1) * CHAR_W

    rows = [
        # (y偏移, 名称, CIGAR, 起始位置, 绘制说明)
        dict(name="r001/1 +", cigar="8M2I4M1D3M", pos=7,
             segs=[("TTAGATAA", 7, "M"), ("AG", None, "I"), ("AGAT", 15, "M"),
                   ("▪", 19, "D"), ("CTG", 20, "M")]),
        dict(name="r002 +", cigar="3S6M1P1I4M", pos=9,
             segs=[("aaa", 6, "S"), ("AGATAA", 9, "M"), ("G", None, "I"),
                   ("GATA", 15, "M")]),
        dict(name="r003 +", cigar="5S6M", pos=9,
             segs=[("gccta", 6, "S"), ("AGCTAA", 9, "M")]),
        dict(name="r004 +", cigar="6M14N5M", pos=16,
             segs=[("ATAGCT", 16, "M"), ("~", 22, "N"), ("TCAGC", 36, "M")]),
        dict(name="r003 −", cigar="6H5M", pos=29,
             segs=[("(N/A)", 23, "H"), ("TAGGC", 29, "M")]),
        dict(name="r001/2 −", cigar="9M", pos=37,
             segs=[("CAGCGGCAT", 37, "M")]),
    ]
    for ri, r in enumerate(rows):
        y = ruler_y + 56 + ri * 44
        svg.text(x0 - 66, y, r["name"], size=SIZE_LABEL, fill=COLOR_MUTED)
        for si, (seq, pos, kind) in enumerate(r["segs"]):
            if kind == "M":
                svg.seq(col(pos), y, seq, size=SIZE_LABEL, fill=COLOR_PRIMARY,
                        weight="bold")
            elif kind == "S":
                svg.seq(col(pos), y, seq, size=SIZE_LABEL, fill=COLOR_MUTED)
                svg.rect(col(pos) - 3, y - 14, len(seq) * CHAR_W + 2, 20,
                         fill="none", stroke=COLOR_LINE, dash="4 3")
            elif kind == "H":
                svg.rect(col(pos), y - 14, 6 * CHAR_W, 20, fill="none",
                         stroke=COLOR_WARN, dash="4 3")
                svg.text(col(pos) + 4, y, "6bp 已剪除", size=SIZE_LABEL, fill=COLOR_WARN)
            elif kind == "I":
                # 插入片段画在下一段比对的起点之前、略高于行基线
                nxt = r["segs"][si + 1]
                ax = col(nxt[1]) - 14
                svg.seq(ax - len(seq) * CHAR_W, y - 13, seq, size=SIZE_LABEL,
                        fill=COLOR_WARN)
                svg.text(ax - 6, y + 2, "⌄", fill=COLOR_WARN)
            elif kind == "D":
                svg.text(col(pos), y, seq, size=SIZE_LABEL, fill=COLOR_WARN, weight="bold")
            elif kind == "N":
                svg.line(col(pos), y - 4, col(pos + 14), y - 4, stroke=COLOR_WARN,
                         sw=1.4, dash="5 4")
                svg.text(col(pos) + 8, y - 12, "跳过 14bp", size=SIZE_LABEL, fill=COLOR_WARN)
        # 行尾 CIGAR
        svg.seq(x0 + len(REF) * CHAR_W + 20, y, r["cigar"], size=SIZE_LABEL,
                fill=COLOR_TEXT, weight="bold")
    # 图例
    ly = ruler_y + 56 + len(rows) * 44 + 16
    legend = [
        ("M", "比对（含错配）", COLOR_PRIMARY), ("I", "插入（read 有）", COLOR_WARN),
        ("D", "缺失（参考有）", COLOR_WARN), ("N", "跳过参考区域（如内含子）", COLOR_WARN),
        ("S", "软剪切（序列保留在 SEQ 列）", COLOR_MUTED), ("H", "硬剪切（序列不保留）", COLOR_WARN),
    ]
    for li, (op, desc, color) in enumerate(legend):
        lx = x0 + (li % 3) * 250
        lyy = ly + (li // 3) * 24
        svg.text(lx, lyy, op, size=SIZE_LABEL, weight="bold", fill=color)
        svg.text(lx + 24, lyy, desc, mono=False, size=SIZE_NOTE, fill=COLOR_MUTED)
    save("cigar-alignment-example", svg)


def main():
    fig_pipeline()
    fig_splicing()
    fig_gtf_example()
    fig_cigar()


if __name__ == "__main__":
    main()
