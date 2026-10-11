#!/usr/bin/env python3
"""第7章三张自绘 SVG 生成脚本（R5）。

遵守绘制铁律：高亮底层先画、文字后画；文字与图形留 ≥8px；
SVG 带固有 width/height 与 viewBox；中文标注 anchor 对齐格心。

运行：python3 scripts/figures/ch07/generate_all.py
输出：assets/08-wgs-and-wes/*.svg
"""
from common import (Svg, save, COLOR_TEXT, COLOR_MUTED, COLOR_PRIMARY,
                    COLOR_FILL, COLOR_WARN, COLOR_WARN_FILL, COLOR_LINE,
                    SIZE_LABEL, SIZE_NOTE, SIZE_TITLE)


def box(s, x, y, w, h, label, *, fill="none", stroke=COLOR_PRIMARY,
        tsize=SIZE_NOTE, tcolor=COLOR_TEXT, dash=None, rx=6, weight="normal"):
    s.rect(x, y, w, h, fill=fill, stroke=stroke, dash=dash, rx=rx)
    lines = label.split("\n")
    line_h = tsize + 6
    y0 = y + h / 2 - (n := len(lines) - 1) * line_h / 2 + tsize * 0.36
    for k, ln in enumerate(lines):
        s.text(x + w / 2, y0 + k * line_h, ln, size=tsize, mono=False,
               fill=tcolor, anchor="middle", weight=weight)


# ───────────────── 图A 外显子、内含子与剪接 ─────────────────
def fig_exon_intron_splicing():
    W, H = 780, 380
    s = Svg(W, H, "外显子、内含子与剪接的关系示意",
            "上：DNA 上的基因结构，外显子为方块、内含子为折线段；"
            "中：转录得到的 pre-mRNA 仍含内含子；下：剪接移除内含子、"
            "外显子相连并加上 5' 帽与 poly(A) 尾，形成成熟 mRNA。")
    # DNA 行
    y_dna = 60
    s.text(24, 34, "DNA（基因结构）", size=SIZE_TITLE, fill=COLOR_PRIMARY, weight="bold")
    intron_y = y_dna + 24
    ex = [(70, 20), (150, 42), (270, 26), (350, 34), (480, 22), (560, 30)]
    exs = []
    for i, (x, w) in enumerate(ex):
        s.rect(x, y_dna + 8, w, 32, fill=COLOR_PRIMARY, rx=3)
        s.text(x + w / 2, y_dna + 29, f"E{i+1}", size=SIZE_NOTE, mono=False,
               fill="#ffffff", anchor="middle")
    # 内含子折线
    for i in range(len(ex) - 1):
        x1, x2 = ex[i][0] + ex[i][1], ex[i + 1][0]
        mid = (x1 + x2) / 2
        s.line(x1, y_dna + 24, mid, y_dna + 8, stroke=COLOR_LINE, sw=1.6)
        s.line(mid, y_dna + 8, x2, y_dna + 24, stroke=COLOR_LINE, sw=1.6)
    s.text(700, y_dna + 29, "← 基因方向", size=SIZE_NOTE, fill=COLOR_MUTED, mono=False)

    # 转录箭头
    s.arrow(390, 104, 390, 140, stroke=COLOR_PRIMARY, sw=1.8)
    s.text(404, 126, "转录", size=SIZE_LABEL, mono=False, fill=COLOR_PRIMARY)

    # pre-mRNA 行
    y_pre = 160
    s.text(24, 152, "pre-mRNA（初级转录本）", size=SIZE_TITLE, fill=COLOR_PRIMARY, weight="bold")
    for i, (x, w) in enumerate(ex):
        s.rect(x, y_pre, w, 26, fill=COLOR_PRIMARY, rx=3)
        s.text(x + w / 2, y_pre + 17, f"E{i+1}", size=SIZE_NOTE, mono=False,
               fill="#ffffff", anchor="middle")
    for i in range(len(ex) - 1):
        x1, x2 = ex[i][0] + ex[i][1], ex[i + 1][0]
        s.line(x1, y_pre + 13, x2, y_pre + 13, stroke=COLOR_LINE, sw=1.6, dash="4,3")
        mid = (x1 + x2) / 2
        s.text(mid, y_pre - 6, "内含子", size=SIZE_NOTE, fill=COLOR_MUTED,
               mono=False, anchor="middle")

    # 剪接箭头
    s.arrow(390, 208, 390, 244, stroke=COLOR_PRIMARY, sw=1.8)
    s.text(404, 230, "剪接（移除内含子）", size=SIZE_LABEL, mono=False, fill=COLOR_PRIMARY)

    # 成熟 mRNA 行
    y_mat = 268
    s.text(24, 262, "成熟 mRNA", size=SIZE_TITLE, fill=COLOR_PRIMARY, weight="bold")
    mx = 70
    s.text(mx, y_mat + 18, "5'帽", size=SIZE_NOTE, mono=False, fill=COLOR_WARN)
    mx += 34
    for i, (x, w) in enumerate(ex):
        s.rect(mx, y_mat, w, 26, fill=COLOR_PRIMARY, rx=3)
        s.text(mx + w / 2, y_mat + 17, f"E{i+1}", size=SIZE_NOTE, mono=False,
               fill="#ffffff", anchor="middle")
        mx += w + 4
    s.text(mx + 8, y_mat + 18, "poly(A) 尾 AAAAA…", size=SIZE_NOTE, mono=False,
           fill=COLOR_MUTED)

    # 底部注解
    s.text(24, 348, "外显子（exon）：出现在成熟 RNA 中；内含子（intron）：转录后被剪接移除。",
           size=SIZE_NOTE, fill=COLOR_TEXT, mono=False)
    s.text(24, 370, "全部外显子的集合即外显子组（exome），是 WES 捕获测序的目标区域。",
           size=SIZE_NOTE, fill=COLOR_TEXT, mono=False)
    save("003-exon-intron-splicing", s)


# ───────────────── 图B 前处理流程总览（竖版） ─────────────────
def fig_preprocessing_overview():
    W, H = 640, 1210
    s = Svg(W, H, "DNA 小变异分析的前处理流程",
            "从 FASTQ 到分析就绪 BAM 的六个步骤（竖版），每步给出输出与目的；"
            "右侧标注各步的检查点。BQSR 之后进入变异检测。")
    steps = [
        ("① 原始质控与过滤", "FASTQ", "去接头、去低质量末端\nfastp / cutadapt", "保留率、Q30 比例（FastQC/MultiQC）"),
        ("② 比对", "SAM/BAM", "reads 定位到参考基因组\nbwa mem（写入 @RG）", "比对率、@RG 是否完整"),
        ("③ 排序", "BAM（按坐标）", "按基因组位置排列\nsamtools sort", "索引可用、坐标有序"),
        ("④ 标记重复", "BAM（带 FLAG 标记）", "PCR 重复不算独立证据\nMarkDuplicates", "重复率是否异常升高"),
        ("⑤ 碱基质量校正", "recal BAM", "校准质量值系统偏差\nBaseRecalibrator + ApplyBQSR", "recal table 是否收敛"),
        ("⑥ 分析就绪，进入变异检测", "BAM + 质控指标", "比对率、重复率、深度分布\n全部达标后调用", "深度是否覆盖目标区域"),
    ]
    bw, bh = 470, 66
    x, y0, gap = 60, 66, 118
    for i, (title, out, why, check) in enumerate(steps):
        y = y0 + i * (bh + gap)
        fill = COLOR_FILL if i == 5 else "none"
        box(s, x, y, bw, bh, title, fill=fill, tsize=SIZE_LABEL, weight="bold")
        s.text(x + bw + 16, y + 20, out, size=SIZE_NOTE, fill=COLOR_PRIMARY,
               mono=False, weight="bold")
        s.text(x + bw + 16, y + 40, why.split("\n")[0], size=SIZE_NOTE, fill=COLOR_MUTED, mono=False)
        s.text(x + bw + 16, y + 56, why.split("\n")[1], size=SIZE_NOTE, fill=COLOR_MUTED, mono=False)
        s.text(x + 10, y + bh + 16, "检查：" + check, size=SIZE_NOTE, fill=COLOR_WARN, mono=False)
        if i < 5:
            ya = y + bh + 26
            s.arrow(x + bw / 2, ya, x + bw / 2, ya + gap - 44, sw=2.0)
    s.text(60, 36, "每一步都在为变异检测整理证据：跳过或做错，错误会直接进入候选变异列表",
           size=SIZE_TITLE, fill=COLOR_PRIMARY, weight="bold")
    save("preprocessing-overview", s)


# ───────────────── 图C VCF 记录解剖 ─────────────────
def fig_vcf_record_anatomy():
    W, H = 880, 430
    s = Svg(W, H, "一条 VCF 记录的逐列解剖",
            "上方是一条 VCF 数据行按列拆开；中部标注各列含义；"
            "下方展开 FORMAT 字段 GT:AD:DP:GQ:PL 的读法。")
    s.text(24, 32, "VCF 一行 = 一个（样本×位点的）变异记录", size=SIZE_TITLE,
           fill=COLOR_PRIMARY, weight="bold")
    cols = [
        ("CHROM", "chr21", "染色体"),
        ("POS", "9068512", "位置（1 起算）"),
        ("ID", ".", "已知编号"),
        ("REF", "C", "参考等位"),
        ("ALT", "T", "替代等位"),
        ("QUAL", "214.64", "变异置信度"),
        ("FILTER", ".", "过滤结论"),
    ]
    widths = [64, 78, 40, 44, 44, 64, 56]
    x = 24
    y_tab = 56
    th = 26
    vh = 30
    for (name, val, meaning), w in zip(cols, widths):
        s.rect(x, y_tab, w, th, fill="#f4faf8", stroke="#cfe3dd")
        s.text(x + w / 2, y_tab + 17, name, size=SIZE_NOTE, mono=False,
               fill=COLOR_PRIMARY, anchor="middle", weight="bold")
        s.rect(x, y_tab + th, w, vh, fill="none", stroke=COLOR_PRIMARY)
        s.text(x + w / 2, y_tab + th + 20, val, size=SIZE_NOTE,
               fill=COLOR_TEXT, anchor="middle")
        # 下方标注（斜向错开防重叠）
        ax = x + w / 2
        s.line(ax, y_tab + th + vh + 2, ax, y_tab + th + vh + 16, stroke=COLOR_LINE)
        s.text(ax, y_tab + th + vh + 32, meaning, size=SIZE_NOTE, mono=False,
               fill=COLOR_MUTED, anchor="middle")
        x += w + 6
    # INFO 与 FORMAT+样本 两块
    y_row2 = y_tab + 34
    s.rect(x, y_row2, 210, th, fill="#f4faf8", stroke="#cfe3dd")
    s.text(x + 105, y_row2 + 17, "INFO", size=SIZE_NOTE, mono=False,
           fill=COLOR_PRIMARY, anchor="middle", weight="bold")
    s.rect(x, y_row2 + th, 210, vh, stroke=COLOR_PRIMARY)
    s.text(x + 8, y_row2 + th + 20, "DP=13;QD=16.51;FS=2.276…", size=SIZE_NOTE, fill=COLOR_TEXT)
    s.text(x + 105, y_row2 + th + vh + 32, "位点级统计", size=SIZE_NOTE, mono=False,
           fill=COLOR_MUTED, anchor="middle")
    s.line(x + 105, y_row2 + th + vh + 2, x + 105, y_row2 + th + vh + 16, stroke=COLOR_LINE)

    x2 = x + 216
    s.rect(x2, y_row2, 240, th, fill="#f4faf8", stroke="#cfe3dd")
    s.text(x2 + 120, y_row2 + 17, "FORMAT + 样本列", size=SIZE_NOTE, mono=False,
           fill=COLOR_PRIMARY, anchor="middle", weight="bold")
    s.rect(x2, y_row2 + th, 240, vh, stroke=COLOR_PRIMARY)
    s.text(x2 + 120, y_row2 + th + 20, "GT:AD:DP:GQ:PL   0/1:6,7:13:99:222,0,132",
           size=SIZE_NOTE, fill=COLOR_TEXT, anchor="middle")
    s.line(x2 + 120, y_row2 + th + vh + 2, x2 + 120, y_row2 + th + vh + 16, stroke=COLOR_LINE)
    s.text(x2 + 120, y_row2 + th + vh + 32, "样本级基因型与证据", size=SIZE_NOTE,
           mono=False, fill=COLOR_MUTED, anchor="middle")

    # FORMAT 字段卡片
    y_cards = 208
    cards = [
        ("GT", "基因型", "0/0 纯合参考\n0/1 杂合\n1/1 纯合替代"),
        ("AD", "各等位基因\n支持 reads 数", "6,7 =\n6 条支持 C\n7 条支持 T"),
        ("DP", "过滤后深度", "13×"),
        ("GQ", "基因型置信度", "99≈上限\n（Phred 缩放）"),
        ("PL", "各基因型\n相对似然", "222,0,132\n最小者最可能\n（0/1 最优）"),
    ]
    cw, ch = 160, 118
    cx = 24
    for name, meaning, detail in cards:
        s.rect(cx, y_cards, cw, ch, fill=COLOR_FILL, stroke=COLOR_PRIMARY, rx=8)
        s.text(cx + 12, y_cards + 24, name, size=SIZE_TITLE, fill=COLOR_PRIMARY,
               weight="bold")
        s.text(cx + 12, y_cards + 44, meaning.split("\n")[0], size=SIZE_NOTE,
               mono=False, fill=COLOR_TEXT)
        if "\n" in meaning:
            s.text(cx + 12, y_cards + 60, meaning.split("\n")[1], size=SIZE_NOTE,
                   mono=False, fill=COLOR_TEXT)
        dy = y_cards + 84
        for ln in detail.split("\n"):
            s.text(cx + 12, dy, ln, size=SIZE_NOTE, mono=False, fill=COLOR_MUTED)
            dy += 16
        cx += cw + 14
    s.text(24, 372, "读记录顺序：先 GT 定基因型，再看 AD/DP 的证据量与比例，最后 QUAL/GQ/PL 看置信度。",
           size=SIZE_NOTE, fill=COLOR_TEXT, mono=False)
    s.text(24, 394, "AD 的比例失衡（如 34,2 的“杂合”）是最需要在 IGV 复核的信号。",
           size=SIZE_NOTE, fill=COLOR_WARN, mono=False)
    save("vcf-record-anatomy", s)




# ───────────────── 图D reads 支持计数示意（IGV 风格） ─────────────────
def fig_reads_support_counts():
    """候选位点 k 条 reads、l 条与参考一致（正文例子 G:A = 4:1）。

    IGV 风格：reads 为带方向箭头的灰条，与参考一致的碱基以深灰字母标出，
    错配以 IGV 配色字母（A 红）标出；参考行候选位点高亮并加星标。
    """
    W, H = 900, 470
    s = Svg(W, H, "一个候选位点的 reads 支持计数示意",
            "k=5 条 reads 比对到候选位点，l=4 条为参考碱基 G（深灰），"
            "k-l=1 条为错配碱基 A（红色）；reads 方向交替（箭头示 3' 端）。")
    SEQ = "atcatgacggcaGtagcatat"
    VI = 12                      # 候选碱基在 SEQ 中的下标（G）
    BP = 34                      # 每碱基像素
    X0 = 60
    BASE_COLOR = {'A': '#C0392B', 'C': '#2471A3', 'G': '#1E8449', 'T': '#B7950B'}

    # 参考行
    y_ref = 96
    for i, ch in enumerate(SEQ):
        x = X0 + i * BP
        big = (i == VI)
        if big:
            s.rect(x - 4, y_ref - 20, BP + 8, 30, fill=COLOR_FILL, stroke=COLOR_PRIMARY, sw=1.6, rx=2)
        s.text(x + BP / 2, y_ref, ch.upper() if big else ch, size=15 if big else 13,
               fill=COLOR_PRIMARY if big else COLOR_TEXT, anchor='middle',
               weight='bold' if big else 'normal')
    s.text(8, y_ref, "REF", size=SIZE_NOTE, mono=False, fill=COLOR_MUTED)
    s.text(X0 + VI * BP + BP / 2, y_ref - 30, "★ 候选位点", size=SIZE_NOTE,
           mono=False, fill=COLOR_PRIMARY, anchor='middle', weight='bold')

    # reads：4 条 G（一致）、1 条 A（错配），方向交替
    reads = [
        ("r1", 0, True, 1), ("r2", 3, False, 0), ("r3", 0, True, 2),
        ("r4", 5, False, 0), ("r5", 2, True, 0),
    ]
    # (名称, 起始偏移, 方向(True=正向→), 该 read 的错配碱基序号(在read内), None 表示一致 G)
    y0, rh, rgap = 150, 26, 42
    for idx, (name, off, fwd, mismatch) in enumerate([
        ("r1", 0, True, None), ("r2", 3, False, None), ("r3", 0, True, None),
        ("r4", 4, False, "A"), ("r5", 1, True, None),
    ]):
        y = y0 + idx * rgap
        rlen = 17                        # read 长 17bp
        rx = X0 + off * BP
        rw = rlen * BP
        # 灰条
        s.rect(rx, y, rw, rh, fill='#e5e7eb', stroke='#d1d5db', sw=0.8, rx=3)
        # 方向箭头（3' 端）：正向右端、反向左端
        import math
        ax = rx + rw + 2 if fwd else rx - 2
        ay = y + rh / 2
        d = 1 if fwd else -1
        s.add(f"<path d='M {ax:.1f} {ay-6:.1f} L {ax+10*d:.1f} {ay:.1f} L {ax:.1f} {ay+6:.1f} Z' "
              f"fill='#9ca3af'/>")
        # 候选位点碱基：一致 G 深灰、错配 A 红
        vx = X0 + VI * BP
        base = mismatch if mismatch else SEQ[VI].upper()
        color = BASE_COLOR[base] if mismatch else '#4b5563'
        s.text(vx + BP / 2, y + rh / 2 + 5, base, size=15, fill=color,
               anchor='middle', weight='bold')
        s.text(8, y + rh / 2 + 4, name, size=SIZE_NOTE, mono=False, fill=COLOR_MUTED)

    # 候选位点贯穿竖线
    s.line(X0 + VI * BP + BP / 2, y_ref + 14, X0 + VI * BP + BP / 2, y0 + 4 * rgap + rh + 8,
           stroke=COLOR_PRIMARY, sw=1.1, dash='5,4')

    # 统计框
    bx, by = 620, 150
    s.rect(bx, by, 236, 96, fill=COLOR_FILL, stroke=COLOR_PRIMARY, rx=8)
    s.text(bx + 16, by + 28, "计数（对应正文记号）", size=SIZE_NOTE, mono=False,
           fill=COLOR_PRIMARY, weight='bold')
    s.text(bx + 16, by + 52, "k = 5 条 reads 比对到该位点", size=SIZE_NOTE, mono=False)
    s.text(bx + 16, by + 72, "l = 4 条与参考一致（G）", size=SIZE_NOTE, mono=False)
    s.text(bx + 16, by + 90, "k - l = 1 条错配（A），G:A = 4:1", size=SIZE_NOTE, mono=False)

    # 图例
    ly = 396
    s.rect(X0, ly - 12, 16, 12, fill='#e5e7eb', stroke='#d1d5db', sw=0.8, rx=2)
    s.text(X0 + 24, ly - 2, "read（箭头示 3′ 端方向）", size=SIZE_NOTE, mono=False, fill=COLOR_MUTED)
    s.text(X0 + 240, ly - 2, "深灰字母＝与参考一致　彩色字母＝错配（IGV 配色）", size=SIZE_NOTE, mono=False, fill=COLOR_MUTED)
    s.text(X0, ly + 22, "仅凭 G:A = 4:1 的比例不足以判定杂合——还需要质量值、链方向与先验（见下文）。",
           size=SIZE_NOTE, mono=False, fill=COLOR_TEXT)
    save("001-reads-support-counts", s)


if __name__ == "__main__":
    fig_preprocessing_overview()
    fig_vcf_record_anatomy()
    fig_reads_support_counts()
