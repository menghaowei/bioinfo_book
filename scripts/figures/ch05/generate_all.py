#!/usr/bin/env python3
"""第5章七张示意图生成脚本（v2：修复几何检测告警）。

绘制铁律（第4章三轮迭代总结，务必遵守）：
1. 高亮矩形一律先画、文字后画（SVG 后画者在上层）；
2. 数值与来源箭头分居格子两角，物理隔离不重叠；
3. 所有文字与相邻图形留至少 8px 间距；
4. SVG 必须带固有 width/height 与 viewBox，画布按内容收紧；
5. 中文标注 anchor 对齐格心；演示数据全部程序生成，不手填。

运行：python3 scripts/figures/ch05/generate_all.py
输出：assets/06-rna-seq/svg/*.svg
"""
from common import (Svg, save, COLOR_TEXT, COLOR_MUTED, COLOR_PRIMARY,
                    COLOR_FILL, COLOR_WARN, COLOR_WARN_FILL, COLOR_LINE,
                    SIZE_LABEL, SIZE_NOTE, SIZE_TITLE)


def box(s, x, y, w, h, label, *, fill="none", stroke=COLOR_PRIMARY, tsize=SIZE_NOTE,
        tcolor=COLOR_TEXT, dash=None, rx=6):
    """先画框、后画字（铁律1）。label 支持 \n 多行，逐行居中。"""
    s.rect(x, y, w, h, fill=fill, stroke=stroke, dash=dash, rx=rx)
    lines = label.split("\n")
    n = len(lines)
    line_h = tsize + 6
    y0 = y + h / 2 - (n - 1) * line_h / 2 + tsize * 0.36
    for k, ln in enumerate(lines):
        s.text(x + w / 2, y0 + k * line_h, ln, size=tsize, mono=False,
               fill=tcolor, anchor="middle")


# ─────────────────────── 图A 基因组与转录组 ───────────────────────
def fig_genome_transcriptome():
    W, H = 600, 330
    s = Svg(W, H, "基因组与转录组的关系示意图",
            "左侧一个基因组（基因结构示意），右侧三种细胞状态各自的转录本集合；"
            "同一套基因组在不同细胞状态转录出不同的 RNA 组合。")
    # 左：基因组（纵向居中）
    gx, gy, gw, gh = 24, 80, 170, 170
    s.rect(gx, gy, gw, gh, fill=COLOR_FILL, rx=8)
    s.text(gx + gw / 2, gy + 26, "基因组", size=SIZE_TITLE, mono=False,
           fill=COLOR_PRIMARY, anchor="middle", weight="bold")
    ex = [(gx + 26, gy + 62, 26, 16), (gx + 70, gy + 62, 34, 16), (gx + 120, gy + 62, 22, 16)]
    for (x, y, w, h) in ex:
        s.rect(x, y, w, h, fill=COLOR_PRIMARY, rx=2)
    s.line(ex[0][0] + ex[0][2], gy + 70, ex[1][0], gy + 70, stroke=COLOR_LINE)
    s.line(ex[1][0] + ex[1][2], gy + 70, ex[2][0], gy + 70, stroke=COLOR_LINE)
    s.text(gx + gw / 2, gy + 102, "外显子/内含子结构", size=SIZE_NOTE, mono=False,
           fill=COLOR_MUTED, anchor="middle")
    s.text(gx + gw / 2, gy + 132, "所有细胞同一套", size=SIZE_NOTE, mono=False,
           fill=COLOR_TEXT, anchor="middle")
    s.text(gx + gw / 2, gy + 150, "DNA 序列不变", size=SIZE_NOTE, mono=False,
           fill=COLOR_TEXT, anchor="middle")
    # 右：三种细胞状态（纵向堆叠，扇形箭头不穿框）
    states = [("神经细胞：转录组 1", [1, 0, 1, 1, 0]),
              ("免疫细胞：转录组 2", [0, 1, 1, 0, 1]),
              ("应激状态：转录组 3", [1, 1, 0, 1, 1])]
    bw, bh, gap = 300, 82, 16
    bx = 270
    for k, (name, on) in enumerate(states):
        by = 26 + k * (bh + gap)
        s.rect(bx, by, bw, bh, fill="none", stroke=COLOR_PRIMARY, rx=8)
        s.text(bx + 12, by + 22, name, size=SIZE_LABEL, mono=False,
               fill=COLOR_PRIMARY, anchor="start", weight="bold")
        genes = ["基因A", "基因B", "基因C", "基因D", "基因E"]
        cxp = bx + 12
        for g, active in enumerate(on):
            cw2 = 54
            if active:
                s.rect(cxp, by + 40, cw2, 20, fill=COLOR_PRIMARY, rx=3)
                s.text(cxp + cw2 / 2, by + 54, genes[g], size=SIZE_NOTE, mono=False,
                       fill="#ffffff", anchor="middle")
            else:
                s.rect(cxp, by + 40, cw2, 20, fill="none", stroke=COLOR_LINE, dash="3,3", rx=3)
                s.text(cxp + cw2 / 2, by + 54, genes[g], size=SIZE_NOTE, mono=False,
                       fill=COLOR_MUTED, anchor="middle")
            cxp += cw2 + 2
        # 扇形箭头：基因组右缘 → 框左缘（不进入任何框）
        s.arrow(gx + gw + 6, gy + gh / 2, bx - 10, by + bh / 2, sw=1.4)
    s.text(W / 2, H - 12, "同一套基因组 —— 转录（开启的基因集合不同）——> 三个不同的转录组",
           size=SIZE_LABEL, mono=False, fill=COLOR_TEXT, anchor="middle", weight="bold")
    save("genome-transcriptome", s)


# ─────────────────────── 图B RNA 类型全景 ───────────────────────
def fig_rna_classes():
    W, H = 700, 400
    s = Svg(W, H, "细胞总 RNA 的主要类型与占比示意图",
            "上方占比条显示 rRNA 约 80–90%、tRNA 约 10–15%、其余（含 mRNA）约 3%；"
            "下方六张卡片给出 mRNA、rRNA、tRNA、miRNA、lncRNA、circRNA 的名称与代表性结构。")
    bx, by, bw, bh = 60, 34, 560, 24
    segs = [(0.85, "#2f6e60"), (0.12, "#7ab5a8"), (0.03, COLOR_WARN)]
    x = bx
    for frac, color in segs:
        w = bw * frac
        s.rect(x, by, w, bh, fill=color, stroke="#ffffff", sw=1, rx=0)
        x += w
    # 标签：条下方排开，互不重叠
    s.text(bx + bw * 0.425, by + bh + 20, "rRNA ≈ 80–90%", size=SIZE_NOTE, mono=False,
           fill=COLOR_TEXT, anchor="middle")
    s.text(bx + bw * 0.91, by + bh + 20, "tRNA ≈ 10–15%", size=SIZE_NOTE, mono=False,
           fill=COLOR_TEXT, anchor="end")
    s.text(bx + bw, by - 10, "其他 ≈ 3%（含 mRNA）", size=SIZE_NOTE, mono=False,
           fill=COLOR_WARN, anchor="end")
    s.text(bx, by - 10, "总 RNA 构成（数量级口径）", size=SIZE_LABEL, mono=False,
           fill=COLOR_MUTED, anchor="start")
    cards = [
        ("mRNA", "5′ 帽—编码区—poly(A) 尾", "编码蛋白，仅占百分之几"),
        ("rRNA", "核糖体的结构骨架", "占绝对大头，建库要处理"),
        ("tRNA", "三叶草二级结构", "转运氨基酸，含量第二"),
        ("miRNA", "发卡前体 → 22 nt 成熟体", "小 RNA 调控，需专门文库"),
        ("lncRNA", "长非编码 RNA（>200 nt）", "调控多样，多无 poly(A) 尾"),
        ("circRNA", "反向剪接成环、无游离末端", "去 rRNA/去线性可测到"),
    ]
    cw, ch, gap = 200, 108, 12
    for i, (name, struct, note) in enumerate(cards):
        cx = 60 + (i % 3) * (cw + gap)
        cy = 96 + (i // 3) * (ch + gap)
        s.rect(cx, cy, cw, ch, fill=COLOR_FILL, rx=8)
        s.text(cx + 12, cy + 24, name, size=SIZE_LABEL, mono=False,
               fill=COLOR_PRIMARY, anchor="start", weight="bold")
        ix, iy = cx + cw - 64, cy + 14
        if name == "mRNA":
            s.rect(ix, iy + 8, 8, 8, fill=COLOR_PRIMARY, rx=2)
            s.line(ix + 8, iy + 12, ix + 40, iy + 12, stroke=COLOR_PRIMARY, sw=2)
            s.text(ix + 42, iy + 16, "AAA", size=9, mono=True, fill=COLOR_PRIMARY)
        elif name == "rRNA":
            s.rect(ix, iy + 2, 52, 20, fill="none", stroke=COLOR_PRIMARY, rx=10)
            s.text(ix + 26, iy + 16, "核糖体", size=10, mono=False, fill=COLOR_PRIMARY, anchor="middle")
        elif name == "tRNA":
            for cxo, cyo in [(ix + 14, iy + 6), (ix + 6, iy + 16), (ix + 22, iy + 16)]:
                s.add(f"<circle cx='{cxo}' cy='{cyo}' r='6' fill='none' stroke='{COLOR_PRIMARY}' stroke-width='1.6'/>")
        elif name == "miRNA":
            s.add(f"<path d='M {ix} {iy+18} q 8 -20 16 0 q 8 20 16 0' fill='none' stroke='{COLOR_PRIMARY}' stroke-width='1.8'/>")
        elif name == "lncRNA":
            s.line(ix, iy + 12, ix + 52, iy + 12, stroke=COLOR_PRIMARY, sw=2)
            s.line(ix + 12, iy + 6, ix + 12, iy + 18, stroke=COLOR_PRIMARY, sw=1.4)
        elif name == "circRNA":
            s.add(f"<circle cx='{ix+24}' cy='{iy+12}' r='11' fill='none' stroke='{COLOR_PRIMARY}' stroke-width='2.2'/>")
        s.text(cx + 12, cy + 56, struct, size=SIZE_NOTE, mono=False, fill=COLOR_TEXT, anchor="start")
        s.text(cx + 12, cy + 80, note, size=SIZE_NOTE, mono=False, fill=COLOR_MUTED, anchor="start")
    s.text(W / 2, H - 12, "建库策略的选择，本质上就是决定“总 RNA 里的哪些部分进入文库”",
           size=SIZE_LABEL, mono=False, fill=COLOR_TEXT, anchor="middle", weight="bold")
    save("rna-classes", s)


# ─────────────────────── 图C 两种建库策略对比 ───────────────────────
def fig_lib_compare():
    W, H = 700, 470
    s = Svg(W, H, "富集 poly(A) 与去 rRNA 两种建库策略的对比",
            "顶部为 DNA 双链上一段基因与转录出的带 poly(A) 尾 mRNA；左右两条泳道分别是"
            "富集 poly(A) 与去 rRNA 的建库流程及各自能测到的 RNA 类型。")
    dx, dy = 200, 26
    s.text(dx, dy + 4, "DNA（双链）", size=SIZE_LABEL, mono=False, fill=COLOR_MUTED)
    s.line(dx + 96, dy - 10, dx + 96, dy + 22, stroke=COLOR_PRIMARY, sw=2)
    s.line(dx + 104, dy - 10, dx + 104, dy + 22, stroke=COLOR_PRIMARY, sw=2)
    for xx in range(dx + 90, dx + 112, 6):
        s.line(xx, dy - 10, xx + 4, dy + 22, stroke=COLOR_LINE, sw=0.8)
    for (ox, ow) in [(150, 26), (196, 34), (246, 22)]:
        s.rect(dx + ox, dy - 4, ow, 18, fill=COLOR_PRIMARY, rx=2)
    s.arrow(dx + 300, dy + 5, dx + 336, dy + 5)
    s.text(dx + 318, dy - 6, "转录", size=SIZE_NOTE, mono=False, fill=COLOR_MUTED, anchor="middle")
    my = dy + 5
    s.text(dx + 388, my - 10, "RNA", size=SIZE_NOTE, mono=False, fill=COLOR_MUTED, anchor="middle")
    exl3 = [(dx + 352, dx + 370), (dx + 382, dx + 406), (dx + 414, dx + 428)]
    prev = dx + 348
    for a0, b0 in exl3:
        s.line(prev, my, a0, my, stroke=COLOR_PRIMARY, sw=2)
        s.rect(a0, my - 5, b0 - a0, 10, fill=COLOR_PRIMARY, rx=2)
        prev = b0
    s.line(prev, my, dx + 432, my, stroke=COLOR_PRIMARY, sw=2)
    s.text(dx + 436, my + 4, "poly(A)", size=9, mono=False, fill=COLOR_WARN)
    lanes = [
        (36, "策略一：富集 poly(A)", COLOR_PRIMARY,
         ["磁珠捕获 poly(A) RNA", "片段化", "反转录＋加接头", "PCR 扩增成文库"],
         "测到：mRNA ＋ 含 poly(A) 尾的 lncRNA\n测不到：无尾 lncRNA、circRNA、rRNA"),
        (252, "策略二：去 rRNA", COLOR_WARN,
         ["探针/酶去除 rRNA", "其余 RNA 全保留", "反转录＋加接头", "PCR 扩增成文库"],
         "测到：mRNA、lncRNA、circRNA 等\n代价：常有 5–20% read 来自残留 rRNA"),
    ]
    for ly, title, color, steps, outcome in lanes:
        s.text(30, ly + 14, title, size=SIZE_TITLE, mono=False, fill=color,
               anchor="start", weight="bold")
        for i, step in enumerate(steps):
            bx = 30 + i * 162
            box(s, bx, ly + 26, 148, 44, step,
                fill=COLOR_FILL if color == COLOR_PRIMARY else COLOR_WARN_FILL)
            if i < len(steps) - 1:
                s.arrow(bx + 150, ly + 48, bx + 160, ly + 48, sw=1.4)
        for k, ln in enumerate(outcome.split("\n")):
            s.text(30, ly + 102 + k * 18, ln, size=SIZE_NOTE, mono=False, fill=COLOR_TEXT)
    s.arrow(430, 46, 214, 49, stroke=COLOR_LINE, sw=1.2)
    s.line(430, 46, 682, 46, stroke=COLOR_LINE, sw=1.2)
    s.line(682, 46, 682, 258, stroke=COLOR_LINE, sw=1.2)
    s.arrow(682, 258, 676, 264, stroke=COLOR_LINE, sw=1.2)
    s.rect(30, 408, 640, 46, fill=COLOR_FILL, rx=6)
    s.text(350, 428, "选择：研究蛋白编码基因、样本质量好 → 富集 poly(A)；", size=SIZE_LABEL,
           mono=False, fill=COLOR_TEXT, anchor="middle")
    s.text(350, 446, "要覆盖非编码 RNA / circRNA、或样本有降解 → 去 rRNA", size=SIZE_LABEL,
           mono=False, fill=COLOR_TEXT, anchor="middle")
    save("lib-compare", s)


# ─────────────────────── 图D dUTP 链特异性建库 ───────────────────────
def fig_stranded_lib():
    W, H = 700, 300
    s = Svg(W, H, "dUTP 链特异性建库流程示意图",
            "第一链 cDNA 正常合成；第二链以 dUTP 替代 dTTP；接头连接后 USER 酶特异降解含 dUTP 的第二链，"
            "只保留与原始 RNA 互补的第一链进入 PCR，read 与转录本链的对应关系因此确定。")
    y0 = 60
    box(s, 24, y0, 100, 44, "RNA 转录本", fill=COLOR_FILL)
    box(s, 158, y0, 126, 44, "第一链 cDNA\n合成（dTTP）", fill=COLOR_FILL)
    box(s, 318, y0, 126, 44, "第二链 cDNA\n掺入 dUTP", fill=COLOR_WARN_FILL)
    for i in range(5):
        s.add(f"<circle cx='{334 + i * 22}' cy='{y0 + 40}' r='3' fill='{COLOR_WARN}'/>")
    box(s, 474, y0, 124, 44, "USER 酶降解\n含 dUTP 第二链", fill="none", stroke=COLOR_WARN)
    box(s, 632, y0, 48, 44, "PCR", fill=COLOR_FILL)
    s.arrow(126, y0 + 22, 156, y0 + 22)
    s.arrow(286, y0 + 22, 316, y0 + 22)
    s.arrow(446, y0 + 22, 472, y0 + 22, stroke=COLOR_WARN)
    s.arrow(600, y0 + 22, 630, y0 + 22)
    s.text(656, y0 - 8, "仅第一链", size=SIZE_NOTE, mono=False, fill=COLOR_MUTED, anchor="middle")
    s.text(221, y0 + 62, "与 RNA 互补、保留", size=SIZE_NOTE, mono=False, fill=COLOR_MUTED, anchor="middle")
    s.line(508, y0 + 4, 544, y0 + 40, stroke=COLOR_WARN, sw=2.4)
    s.line(544, y0 + 4, 508, y0 + 40, stroke=COLOR_WARN, sw=2.4)
    y1 = 190
    s.text(350, y1 - 34, "为什么能分清链：保留的第一链方向对应原始转录本，read 比对后唯一归属正链或负链",
           size=SIZE_LABEL, mono=False, fill=COLOR_TEXT, anchor="middle")
    gxx = 200
    s.text(gxx - 122, y1 - 10, "基因组正链基因", size=SIZE_NOTE, mono=False, fill=COLOR_MUTED, anchor="start")
    exl = [(gxx + ox, gxx + ox + 26) for ox in (-110, -60, 10, 70, 110)]
    prev = gxx - 122
    for a0, b0 in exl:
        s.line(prev, y1, a0, y1, stroke=COLOR_PRIMARY, sw=2)
        s.rect(a0, y1 - 6, 26, 12, fill=COLOR_PRIMARY, rx=2)
        prev = b0
    s.line(prev, y1, gxx + 130, y1, stroke=COLOR_PRIMARY, sw=2)
    s.text(gxx + 150, y1 + 5, "read →", size=SIZE_NOTE, mono=False, fill=COLOR_PRIMARY)
    s.text(gxx - 122, y1 + 46, "反义转录本", size=SIZE_NOTE, mono=False, fill=COLOR_MUTED, anchor="start")
    exl2 = [(gxx + ox, gxx + ox + 22) for ox in (-90, -20, 50, 100)]
    prev = gxx - 122
    for a0, b0 in exl2:
        s.line(prev, y1 + 56, a0, y1 + 56, stroke=COLOR_LINE, sw=1.6)
        s.rect(a0, y1 + 50, 22, 12, fill=COLOR_WARN, rx=2)
        prev = b0
    s.line(prev, y1 + 56, gxx + 130, y1 + 56, stroke=COLOR_LINE, sw=1.6)
    s.text(gxx + 150, y1 + 61, "read →", size=SIZE_NOTE, mono=False, fill=COLOR_WARN)
    s.text(350, y1 + 96, "普通文库两条链的 read 混在一起；链特异性文库能把它们分开计数",
           size=SIZE_NOTE, mono=False, fill=COLOR_MUTED, anchor="middle")
    save("stranded-lib", s)


# ─────────────────────── 图E 火山图演示 ───────────────────────
def fig_volcano_demo():
    import random
    rng = random.Random(20261010)
    W, H = 600, 360
    s = Svg(W, H, "火山图读法演示",
            "模拟的差异分析结果：横轴 log2 倍数变化、纵轴 -log10 p 值；灰色为不显著基因，"
            "绿色为显著上调、琥珀为显著下调；虚线为常用阈值。")
    ox, oy, pw, ph = 64, 26, 330, 268
    pts = []
    import random as _r
    for _ in range(450):
        pts.append((min(max(rng.gauss(0, 0.55), -3.6), 3.6), min(abs(rng.gauss(0.9, 0.7)), 5.2), "ns"))
    for _ in range(88):
        pts.append((min(rng.gauss(2.3, 0.5), 3.6), min(abs(rng.gauss(3.2, 1.0)), 5.2), "up"))
    for _ in range(76):
        pts.append((max(rng.gauss(-2.25, 0.5), -3.6), min(abs(rng.gauss(2.9, 1.0)), 5.2), "down"))
    XMIN, XMAX, YMAX = -4, 4, 5.5
    def px(x): return ox + (x - XMIN) / (XMAX - XMIN) * pw
    def py(y): return oy + ph - y / YMAX * ph
    colors = {"ns": "#c4cbd0", "up": COLOR_PRIMARY, "down": COLOR_WARN}
    s.rect(ox, oy, pw, ph, fill="#ffffff", stroke=COLOR_LINE, sw=1, rx=4)
    for gx in (-2, 0, 2):
        s.line(px(gx), oy, px(gx), oy + ph, stroke="#eef1ee", sw=1)
        s.text(px(gx), oy + ph + 16, str(gx), size=SIZE_NOTE, fill=COLOR_MUTED, anchor="middle")
    for gy in (1, 2, 3, 4, 5):
        s.line(ox, py(gy), ox + pw, py(gy), stroke="#eef1ee", sw=1)
        s.text(ox - 8, py(gy) + 4, str(gy), size=SIZE_NOTE, fill=COLOR_MUTED, anchor="end")
    s.line(px(-1), oy, px(-1), oy + ph, stroke=COLOR_LINE, sw=1, dash="4,4")
    s.line(px(1), oy, px(1), oy + ph, stroke=COLOR_LINE, sw=1, dash="4,4")
    s.line(ox, py(1.3), ox + pw, py(1.3), stroke=COLOR_LINE, sw=1, dash="4,4")
    for x, y, c in pts:
        s.add(f"<circle cx='{px(x):.1f}' cy='{py(y):.1f}' r='2.6' fill='{colors[c]}' fill-opacity='0.85'/>")
    s.text(ox + pw / 2, oy + ph + 36, "log2 fold change", size=SIZE_LABEL, fill=COLOR_TEXT, anchor="middle")
    s.add(f"<text x='24' y='{oy + ph / 2}' font-family='PingFang SC,Hiragino Sans GB,sans-serif' "
          f"font-size='13' fill='{COLOR_TEXT}' text-anchor='middle' "
          f"transform='rotate(-90 24 {oy + ph / 2})'>−log10 p</text>")
    s.text(px(-1), oy + ph + 16, "-1", size=SIZE_NOTE, fill=COLOR_MUTED, anchor="middle")
    s.text(px(1), oy + ph + 16, "1", size=SIZE_NOTE, fill=COLOR_MUTED, anchor="middle")
    s.text(ox + pw - 8, py(1.3) - 6, "p = 0.05", size=9, fill=COLOR_MUTED, anchor="end")
    lx = ox + pw + 24
    s.rect(lx, oy + 8, 108, 62, fill="#ffffff", stroke=COLOR_LINE, rx=4)
    up_c, down_c, ns_c = colors["up"], colors["down"], colors["ns"]
    s.add(f"<circle cx='{lx + 14}' cy='{oy + 24}' r='3' fill='{up_c}'/>")
    s.text(lx + 24, oy + 28, "显著上调", size=SIZE_NOTE, fill=COLOR_TEXT)
    s.add(f"<circle cx='{lx + 14}' cy='{oy + 42}' r='3' fill='{down_c}'/>")
    s.text(lx + 24, oy + 46, "显著下调", size=SIZE_NOTE, fill=COLOR_TEXT)
    s.add(f"<circle cx='{lx + 14}' cy='{oy + 60}' r='3' fill='{ns_c}'/>")
    s.text(lx + 24, oy + 64, "不显著", size=SIZE_NOTE, fill=COLOR_TEXT)
    s.text(ox + pw - 10, oy - 8, "右上／左上越远越显著", size=SIZE_NOTE, fill=COLOR_MUTED, anchor="end")
    save("volcano-demo", s)


# ─────────────────────── 图F 聚类热图演示 ───────────────────────
def fig_heatmap_demo():
    import random
    rng = random.Random(5)
    W, H = 470, 452
    s = Svg(W, H, "聚类热图读法演示",
            "模拟的显著基因×样本计数矩阵（按行标准化）：对照两列与敲降两列各自聚类并排，"
            "颜色表示该基因在该样本中的相对高低。")
    genes, samples = 14, 4
    cell = 22
    ox, oy = 116, 78
    data = []
    for g in range(genes):
        base = rng.uniform(-0.4, 0.4)
        eff = rng.choice([-1, 1]) * rng.uniform(0.6, 1.4) if g < 10 else 0
        row = [base + (eff if k >= 2 else 0) + rng.gauss(0, 0.18) for k in range(4)]
        m = max(abs(min(row)), abs(max(row)))
        data.append([v / m for v in row])
    s.line(ox + cell * 0.5, oy - 26, ox + cell * 1.5, oy - 26, stroke=COLOR_PRIMARY, sw=1.4)
    s.line(ox + cell * 0.5, oy - 26, ox + cell * 0.5, oy - 14, stroke=COLOR_PRIMARY, sw=1.4)
    s.line(ox + cell * 1.5, oy - 26, ox + cell * 1.5, oy - 14, stroke=COLOR_PRIMARY, sw=1.4)
    s.line(ox + cell * 2.5, oy - 26, ox + cell * 3.5, oy - 26, stroke=COLOR_WARN, sw=1.4)
    s.line(ox + cell * 2.5, oy - 26, ox + cell * 2.5, oy - 14, stroke=COLOR_WARN, sw=1.4)
    s.line(ox + cell * 3.5, oy - 26, ox + cell * 3.5, oy - 14, stroke=COLOR_WARN, sw=1.4)
    s.text(ox + cell * 1.0, oy - 34, "对照", size=SIZE_NOTE, fill=COLOR_PRIMARY, anchor="middle")
    s.text(ox + cell * 3.0, oy - 34, "敲降", size=SIZE_NOTE, fill=COLOR_WARN, anchor="middle")
    for r, row in enumerate(data):
        for c, v in enumerate(row):
            t = (v + 1) / 2
            color = f"#{int(210 - t * 30):02x}{int(90 + t * 80):02x}{int(60 + t * 20):02x}"
            s.add(f"<rect x='{ox + c * cell}' y='{oy + r * cell}' width='{cell - 1}' height='{cell - 1}' fill='{color}'/>")
    for c, (name, dy) in enumerate([("对照1", 0), ("", 0), ("敲降1", 0), ("", 0)]):
        if not name:
            continue
        col = c
        s.text(ox + col * cell + cell / 2, oy + genes * cell + 18, name, size=SIZE_NOTE,
               fill=COLOR_TEXT, anchor="middle")
    for c, name in [(1, "对照2"), (3, "敲降2")]:
        s.text(ox + c * cell + cell / 2, oy + genes * cell + 38, name, size=SIZE_NOTE,
               fill=COLOR_TEXT, anchor="middle")
    for r in range(0, genes, 2):
        s.text(ox - 10, oy + r * cell + cell / 2 + 4, f"基因{r + 1}", size=SIZE_NOTE,
               fill=COLOR_MUTED, anchor="end")
    lgx = ox + 4 * cell + 30
    for i in range(10):
        t = i / 9
        color = f"#{int(210 - t * 30):02x}{int(90 + t * 80):02x}{int(60 + t * 20):02x}"
        s.add(f"<rect x='{lgx}' y='{oy + i * 12}' width='14' height='12' fill='{color}'/>")
    s.text(lgx + 7, oy - 8, "低—高", size=SIZE_NOTE, fill=COLOR_MUTED, anchor="middle")
    s.text(lgx + 8, oy + 150, "要点：", size=SIZE_NOTE, fill=COLOR_TEXT, anchor="start")
    for k, ln in enumerate(["1. 重复样本并排＝聚类正确", "2. 组间分块＝差异真实", "3. 行＝基因，按行标准化"]):
        s.text(lgx + 8, oy + 170 + k * 18, ln, size=SIZE_NOTE, fill=COLOR_MUTED)
    s.text(W / 2, H - 8, "颜色深浅＝该基因在各样本中的相对表达（按行标准化）",
           size=SIZE_NOTE, fill=COLOR_TEXT, anchor="middle")
    save("heatmap-demo", s)


# ─────────────────────── 图G 富集气泡图演示 ───────────────────────
def fig_bubble_demo():
    W, H = 520, 380
    s = Svg(W, H, "富集分析气泡图读法演示",
            "模拟的 GO/KEGG 富集结果：横轴为基因比例，气泡大小为显著基因数，颜色深浅为 p 值；"
            "右上角大气泡是最值得关注的通路。")
    terms = [("细胞周期", 0.31, 68, 2e-6), ("DNA 复制", 0.26, 54, 8e-6),
             ("染色体分离", 0.22, 41, 4e-5), ("DNA 修复", 0.18, 33, 2e-4),
             ("程序性细胞死亡", 0.14, 21, 1e-3), ("RNA 剪接", 0.11, 18, 4e-3),
             ("蛋白质折叠", 0.09, 12, 2e-2), ("信号转导", 0.06, 8, 6e-2)]
    ox, oy, pw, ph = 130, 30, 300, 264
    XMAX = 0.36
    def px(x): return ox + x / XMAX * pw
    def py(i): return oy + 18 + i * (ph - 24) / (len(terms) - 1)
    s.rect(ox, oy, pw, ph, fill="#ffffff", stroke=COLOR_LINE, rx=4)
    for gx in (0.1, 0.2, 0.3):
        s.line(px(gx), oy, px(gx), oy + ph, stroke="#eef1ee")
        s.text(px(gx), oy + ph + 16, f"{gx:.1f}", size=SIZE_NOTE, fill=COLOR_MUTED, anchor="middle")
    import math as _m
    def pcolor(p):
        t = min(1, max(0, -_m.log10(p) / 6))
        return f"#{int(190 - t * 130):02x}{int(215 - t * 80):02x}{int(205 - t * 140):02x}"
    for i, (name, ratio, cnt, p) in enumerate(terms):
        r = 6 + (cnt - 6) * 0.42
        s.add(f"<circle cx='{px(ratio):.1f}' cy='{py(i):.1f}' r='{r:.1f}' fill='{pcolor(p)}' stroke='{COLOR_PRIMARY}' stroke-opacity='0.45' stroke-width='1'/>")
        s.text(ox - 12, py(i) + 4, name, size=SIZE_NOTE, fill=COLOR_TEXT, anchor="end")
    s.text(ox + pw / 2, oy + ph + 36, "基因比例（显著基因中注释到该通路的占比）", size=SIZE_LABEL,
           fill=COLOR_TEXT, anchor="middle")
    lx = ox + pw + 24
    s.text(lx, oy + 10, "基因数", size=SIZE_NOTE, fill=COLOR_MUTED)
    for k, cnt in enumerate([15, 40, 70]):
        r = 6 + (cnt - 6) * 0.42
        s.add(f"<circle cx='{lx + 12}' cy='{oy + 34 + k * 44 + 10}' r='{r:.1f}' fill='#e5ece9' stroke='{COLOR_LINE}'/>")
        s.text(lx + 36, oy + 44 + k * 44, str(cnt), size=SIZE_NOTE, fill=COLOR_TEXT)
    s.text(lx, oy + 190, "p 值", size=SIZE_NOTE, fill=COLOR_MUTED)
    for k, p in enumerate([1e-1, 1e-3, 1e-5]):
        s.add(f"<circle cx='{lx + 12}' cy='{oy + 210 + k * 26}' r='7' fill='{pcolor(p)}' stroke='{COLOR_LINE}'/>")
        s.text(lx + 28, oy + 214 + k * 26, f"{p:.0e}", size=SIZE_NOTE, fill=COLOR_TEXT)
    s.text(W / 2, H - 12, "读图：右上角大而深的气泡＝基因比例高、p 值小、贡献基因多",
           size=SIZE_NOTE, fill=COLOR_TEXT, anchor="middle")
    save("bubble-demo", s)




# ─────────────────── 流程图通用竖排链 ───────────────────
def vchain(s, x, y0, w, h, steps, gap=26, fill=COLOR_FILL):
    """竖排流程链；返回 (末框中心 y, 链底部 y)。"""
    cy = y0
    for i, st in enumerate(steps):
        box(s, x, cy, w, h, st, fill=fill)
        if i < len(steps) - 1:
            s.arrow(x + w / 2, cy + h + 2, x + w / 2, cy + h + gap - 4, sw=1.4)
        cy += h + gap
    return cy - gap - h / 2, cy - gap


def fig_workflow_rnaseq():
    W, H = 430, 560
    s = Svg(W, H, "有参考基因组的 RNA-seq 分析流程",
            "从原始 FASTQ 出发的竖版主线：质控过滤、构建索引、剪接感知比对、（可选）转录本组装、"
            "表达定量、差异分析、功能富集。")
    steps = ["原始测序数据（FASTQ）", "质量控制与过滤", "构建参考基因组索引", "剪接感知比对（HISAT2/STAR）",
             "表达定量（count／TPM）", "差异表达分析（DESeq2/edgeR）", "功能注释与富集（clusterProfiler）"]
    x, w, h = 40, 220, 40
    cy = 24
    centers = []
    for i, st in enumerate(steps):
        box(s, x, cy, w, h, st)
        centers.append(cy + h / 2)
        if i < len(steps) - 1:
            s.arrow(x + w / 2, cy + h + 2, x + w / 2, cy + h + 22, sw=1.4)
        cy += h + 24
    # 可选支线：比对 → 转录本组装 → 定量
    bx, bw, bh = 300, 100, 46
    by = centers[3]
    s.line(x + w, by, bx, by, stroke=COLOR_LINE, sw=1.2)
    s.text(x + w + 10, by - 8, "可选", size=SIZE_NOTE, fill=COLOR_MUTED)
    box(s, bx, by - bh / 2, bw, bh, "转录本组装\n（StringTie）", fill="none", dash="4,3")
    s.line(bx + bw / 2, by + bh / 2, bx + bw / 2, centers[4], stroke=COLOR_LINE, sw=1.2)
    s.arrow(bx + bw / 2, centers[4] - 8, x + w + 6, centers[4], sw=1.2)
    s.text(W / 2, H - 12, "主线对应本书 5.2—5.6 节的展开顺序（重绘自原稿示意图）",
           size=SIZE_NOTE, fill=COLOR_MUTED, anchor="middle")
    save("rnaseq-workflow", s)


def fig_workflow_lncrna():
    W, H = 440, 560
    s = Svg(W, H, "lncRNA 测序分析流程",
            "左侧主线：质控、比对、从注释取已知 lncRNA；右侧支线：组装转录本并过滤编码潜力得到新 lncRNA；"
            "两者合并为总 lncRNA 后定量、差异分析并做功能注释。")
    main = ["FASTQ 原始数据", "质量控制", "基因组比对", "已知 lncRNA（注释）",
            "总 lncRNA", "表达定量", "差异表达分析", "功能注释（直接／靶基因）"]
    side = ["转录本组装（可选）", "编码潜力过滤", "新 lncRNA"]
    h, gap = 38, 26
    mx, mw = 24, 172
    centers_main = []
    cy = 24
    for i, st in enumerate(main):
        box(s, mx, cy, mw, h, st)
        centers_main.append(cy + h / 2)
        if i < len(main) - 1:
            s.arrow(mx + mw / 2, cy + h + 2, mx + mw / 2, cy + h + gap - 4, sw=1.4)
        cy += h + gap
    sx, sw2 = 252, 150
    sy = centers_main[2]           # 对齐“基因组比对”
    s.arrow(mx + mw, sy, sx - 8, sy, sw=1.2)
    cy2 = sy - h / 2
    for i, st in enumerate(side):
        box(s, sx, cy2, sw2, h, st, fill="none", dash="4,3")
        if i < len(side) - 1:
            s.arrow(sx + sw2 / 2, cy2 + h + 2, sx + sw2 / 2, cy2 + h + gap - 4, sw=1.2)
        cy2 += h + gap
    total_cy = centers_main[4]
    s.arrow(sx, total_cy, mx + mw + 8, total_cy, sw=1.4)
    s.text(W / 2, H - 12, "两条来源汇入“总 lncRNA”（重绘自原稿示意图）",
           size=SIZE_NOTE, fill=COLOR_MUTED, anchor="middle")
    save("lncrna-workflow", s)


def fig_workflow_smallrna():
    W, H = 450, 616
    s = Svg(W, H, "small RNA 测序分析流程",
            "主线：质控、按长度筛选、比对 miRBase 已知 miRNA；支线：发卡结构预测新 miRNA；"
            "合并后差异分析、靶基因预测与功能富集。")
    main = ["FASTQ 原始数据", "质量控制", "长度筛选（18–30 nt）", "比对已知 miRNA\n（miRBase 索引）",
            "总 miRNA", "差异表达分析", "靶标基因预测", "注释与富集分析"]
    side = ["发卡结构预测", "新 miRNA"]
    h, gap = 46, 26
    mx, mw = 24, 186
    centers = []
    cy = 24
    for i, st in enumerate(main):
        box(s, mx, cy, mw, h, st)
        centers.append(cy + h / 2)
        if i < len(main) - 1:
            s.arrow(mx + mw / 2, cy + h + 2, mx + mw / 2, cy + h + gap - 4, sw=1.4)
        cy += h + gap
    sx, sw2 = 262, 146
    sy = centers[2]               # 对齐“长度筛选”
    s.arrow(mx + mw, sy, sx - 8, sy, sw=1.2)
    cy2 = sy - h / 2
    for i, st in enumerate(side):
        box(s, sx, cy2, sw2, h, st, fill="none", dash="4,3")
        if i < len(side) - 1:
            s.arrow(sx + sw2 / 2, cy2 + h + 2, sx + sw2 / 2, cy2 + h + gap - 4, sw=1.2)
        cy2 += h + gap
    side_bottom = cy2 - gap
    total_cy = centers[4]
    s.line(sx + sw2 / 2, side_bottom, sx + sw2 / 2, total_cy, stroke=COLOR_PRIMARY, sw=1.4)
    s.arrow(sx + sw2 / 2, total_cy, mx + mw + 8, total_cy, sw=1.4)
    s.text(W / 2, H - 12, "miRDeep2 可完成新 miRNA 预测与定量（重绘自原稿示意图）",
           size=SIZE_NOTE, fill=COLOR_MUTED, anchor="middle")
    save("smallrna-workflow", s)


def fig_workflow_circrna():
    W, H = 470, 616
    s = Svg(W, H, "circRNA 测序分析流程",
            "主线：质控、基因组比对、识别反向剪接位点、比对 circBase 已知 circRNA；"
            "支线：软件预测新 circRNA；合并后差异分析、宿主基因注释与特征分析。")
    main = ["FASTQ 原始数据", "质量控制", "基因组比对", "识别反向剪接位点",
            "已知 circRNA（circBase）", "总 circRNA", "差异表达分析", "宿主基因注释／特征分析"]
    side = ["软件预测\n（find_circ／CIRI）", "新 circRNA"]
    h, gap = 46, 26
    mx, mw = 24, 196
    centers = []
    cy = 24
    for i, st in enumerate(main):
        box(s, mx, cy, mw, h, st)
        centers.append(cy + h / 2)
        if i < len(main) - 1:
            s.arrow(mx + mw / 2, cy + h + 2, mx + mw / 2, cy + h + gap - 4, sw=1.4)
        cy += h + gap
    sx, sw2 = 272, 172
    sy = centers[3]               # 对齐“识别反向剪接位点”
    s.arrow(mx + mw, sy, sx - 8, sy, sw=1.2)
    cy2 = sy - h / 2
    for i, st in enumerate(side):
        box(s, sx, cy2, sw2, h, st, fill="none", dash="4,3")
        if i < len(side) - 1:
            s.arrow(sx + sw2 / 2, cy2 + h + 2, sx + sw2 / 2, cy2 + h + gap - 4, sw=1.2)
        cy2 += h + gap
    side_bottom = cy2 - gap
    total_cy = centers[5]
    s.line(sx + sw2 / 2, side_bottom, sx + sw2 / 2, total_cy, stroke=COLOR_PRIMARY, sw=1.4)
    s.arrow(sx + sw2 / 2, total_cy, mx + mw + 8, total_cy, sw=1.4)
    s.text(W / 2, H - 12, "连接点 read 是鉴定的特征信号（见 5.7 节；重绘自原稿示意图）",
           size=SIZE_NOTE, fill=COLOR_MUTED, anchor="middle")
    save("circrna-workflow", s)


if __name__ == "__main__":
    fig_genome_transcriptome()
    fig_rna_classes()
    fig_lib_compare()
    fig_stranded_lib()
    fig_volcano_demo()
    fig_heatmap_demo()
    fig_bubble_demo()
    fig_workflow_rnaseq()
    fig_workflow_lncrna()
    fig_workflow_smallrna()
    fig_workflow_circrna()
