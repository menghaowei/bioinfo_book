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
    W, H = 640, 340
    s = Svg(W, H, "基因组与转录组的关系示意图",
            "左侧一个基因组（基因结构示意），右侧三种细胞状态各自的转录本集合；"
            "同一套基因组在不同细胞状态转录出不同的 RNA 组合。")
    gx, gy, gw, gh = 24, 90, 168, 176
    s.rect(gx, gy, gw, gh, fill="#f4faf8", stroke="#cfe3dd", rx=12)
    s.text(gx + gw / 2, gy + 28, "基因组", size=SIZE_TITLE, fill=COLOR_PRIMARY, anchor="middle", weight="bold")
    ex = [(gx + 24, gy + 66, 28, 18), (gx + 70, gy + 66, 36, 18), (gx + 122, gy + 66, 24, 18)]
    for (xx, yy, ww, hh) in ex:
        s.rect(xx, yy, ww, hh, fill=COLOR_PRIMARY, rx=3)
    s.line(ex[0][0] + ex[0][2], gy + 75, ex[1][0], gy + 75, stroke=COLOR_LINE, sw=1.6)
    s.line(ex[1][0] + ex[1][2], gy + 75, ex[2][0], gy + 75, stroke=COLOR_LINE, sw=1.6)
    s.text(gx + gw / 2, gy + 108, "外显子／内含子结构", size=SIZE_NOTE, fill=COLOR_MUTED, anchor="middle")
    s.text(gx + gw / 2, gy + 136, "所有细胞同一套", size=SIZE_NOTE, fill=COLOR_TEXT, anchor="middle")
    s.text(gx + gw / 2, gy + 156, "DNA 序列不变", size=SIZE_NOTE, fill=COLOR_TEXT, anchor="middle")
    states = [("神经细胞：转录组 1", [1, 0, 1, 1, 0]),
              ("免疫细胞：转录组 2", [0, 1, 1, 0, 1]),
              ("应激状态：转录组 3", [1, 1, 0, 1, 1])]
    bw2, bh2, gap2 = 300, 84, 14
    bx = 306
    genes = ["A", "B", "C", "D", "E"]
    for k, (name, on) in enumerate(states):
        by = 22 + k * (bh2 + gap2)
        s.rect(bx, by, bw2, bh2, fill="#ffffff", stroke=COLOR_PRIMARY, rx=10)
        s.text(bx + 14, by + 24, name, size=SIZE_LABEL, fill=COLOR_PRIMARY, anchor="start", weight="bold")
        cwp = 52
        xp = bx + 14
        for g, active in enumerate(on):
            if active:
                s.rect(xp, by + 42, cwp, 24, fill=COLOR_PRIMARY, rx=4)
                s.text(xp + cwp / 2, by + 58, genes[g], size=SIZE_NOTE, fill="#ffffff", anchor="middle")
            else:
                s.rect(xp, by + 42, cwp, 24, fill="#f2f4f3", stroke="#c4cbd0", rx=4)
                s.text(xp + cwp / 2, by + 58, genes[g], size=SIZE_NOTE, fill=COLOR_MUTED, anchor="middle")
            xp += cwp + 4
        s.add(f"<path d='M {gx+gw+8} {gy+gh/2} C {bx-70} {gy+gh/2}, {bx-70} {by+bh2/2}, {bx-10} {by+bh2/2}' fill='none' stroke='#9ca3af' stroke-width='1.6'/>")
        s.arrow(bx - 16, by + bh2 / 2, bx - 8, by + bh2 / 2, sw=1.6)
    s.text(W / 2, H - 10, "同一套基因组 —— 转录（开启的基因集合不同）→ 三个不同的转录组",
           size=SIZE_LABEL, fill=COLOR_TEXT, anchor="middle", weight="bold")
    save("genome-transcriptome", s)


def fig_rna_classes():
    W, H = 720, 440
    s = Svg(W, H, "细胞总 RNA 的主要类型与占比示意图",
            "上方占比条：rRNA 约 80–90%、tRNA 约 10–15%、其余（含 mRNA）约 3%；"
            "下方六张卡片绘制 mRNA、rRNA、tRNA、miRNA、lncRNA、circRNA 的代表性结构。")
    bx, by, bw, bh = 60, 40, 560, 26
    x = bx
    for frac, color in [(0.85, "#2f6e60"), (0.12, "#7ab5a8"), (0.03, "#b45309")]:
        s.rect(x, by, bw * frac, bh, fill=color, stroke="#ffffff", sw=1.5)
        x += bw * frac
    s.text(bx + bw * 0.425, by + bh + 22, "rRNA ≈ 80–90%", size=SIZE_NOTE, fill=COLOR_TEXT, anchor="middle")
    s.text(bx + bw * 0.91, by + bh + 22, "tRNA ≈ 10–15%", size=SIZE_NOTE, fill=COLOR_TEXT, anchor="end")
    s.text(bx + bw, by - 10, "其他 ≈ 3%（含 mRNA）", size=SIZE_NOTE, fill="#b45309", anchor="end")
    s.text(bx, by - 10, "总 RNA 构成（数量级口径）", size=SIZE_LABEL, fill=COLOR_MUTED, anchor="start")

    cards = [
        ("mRNA", "5′ 帽—编码区—poly(A) 尾", "编码蛋白，仅占百分之几", "mrna"),
        ("rRNA", "核糖体的结构骨架", "占绝对大头，建库要处理", "rrna"),
        ("tRNA", "三叶草二级结构", "转运氨基酸，含量第二", "trna"),
        ("miRNA", "发卡前体 → 22 nt 成熟体", "小 RNA 调控，需专门文库", "mirna"),
        ("lncRNA", "长非编码 RNA（>200 nt）", "调控多样，多无 poly(A) 尾", "lncrna"),
        ("circRNA", "反向剪接成环、无游离末端", "去 rRNA/去线性可测到", "circrna"),
    ]
    cw, ch, gap = 204, 132, 12
    for i, (name, struct, note, kind) in enumerate(cards):
        cx = 60 + (i % 3) * (cw + gap)
        cy = 108 + (i // 3) * (ch + gap)
        s.rect(cx, cy, cw, ch, fill="#f4faf8", stroke="#cfe3dd", rx=10)
        s.text(cx + 14, cy + 24, name, size=SIZE_LABEL, fill=COLOR_PRIMARY, anchor="start", weight="bold")
        ix, iy = cx + cw - 78, cy + 12
        P = COLOR_PRIMARY
        if kind == "mrna":
            s.add(f"<circle cx='{ix+8}' cy='{iy+22}' r='7' fill='{P}'/>")
            s.rect(ix + 20, iy + 14, 40, 16, fill=P, rx=3)
            s.line(ix + 60, iy + 22, ix + 66, iy + 22, stroke=P, sw=3)
            for k in range(3):
                s.text(ix + 68 + k * 11, iy + 26, "A", size=11, mono=True, fill="#b45309")
        elif kind == "rrna":
            s.add(f"<ellipse cx='{ix+22}' cy='{iy+16}' rx='20' ry='11' fill='none' stroke='{P}' stroke-width='2.2'/>")
            s.add(f"<ellipse cx='{ix+34}' cy='{iy+30}' rx='20' ry='11' fill='none' stroke='{P}' stroke-width='2.2'/>")
        elif kind == "trna":
            s.add(f"<circle cx='{ix+16}' cy='{iy+12}' r='8' fill='none' stroke='{P}' stroke-width='2.2'/>")
            s.add(f"<circle cx='{ix+8}' cy='{iy+26}' r='8' fill='none' stroke='{P}' stroke-width='2.2'/>")
            s.add(f"<circle cx='{ix+24}' cy='{iy+26}' r='8' fill='none' stroke='{P}' stroke-width='2.2'/>")
            s.line(ix + 16, iy + 20, ix + 16, iy + 32, stroke=P, sw=2.2)
            s.text(ix + 13, iy + 42, "3′", size=9, mono=True, fill=P)
        elif kind == "mirna":
            s.add(f"<path d='M {ix} {iy+34} C {ix+10} {iy-4} {ix+24} {iy-4} {ix+34} {iy+34}' fill='none' stroke='#c9d6d1' stroke-width='2.4'/>")
            s.add(f"<path d='M {ix+34} {iy+34} C {ix+44} {iy+62} {ix+58} {iy+62} {ix+68} {iy+34}' fill='none' stroke='{P}' stroke-width='2.6'/>")
        elif kind == "lncrna":
            s.rect(ix, iy + 20, 68, 12, fill="none", stroke=P, sw=2.2, rx=6)
            s.add(f"<circle cx='{ix+18}' cy='{iy+10}' r='5' fill='#cfe3dd'/>")
            s.add(f"<circle cx='{ix+46}' cy='{iy+10}' r='5' fill='#cfe3dd'/>")
        elif kind == "circrna":
            s.add(f"<circle cx='{ix+34}' cy='{iy+26}' r='16' fill='none' stroke='{P}' stroke-width='3'/>")
            s.add(f"<circle cx='{ix+34}' cy='{iy+10}' r='4.5' fill='#b45309'/>")
        s.text(cx + 14, cy + 62, struct, size=SIZE_NOTE, fill=COLOR_TEXT, anchor="start")
        s.text(cx + 14, cy + 84, note, size=SIZE_NOTE, fill=COLOR_MUTED, anchor="start")
    s.text(W / 2, H - 10, "建库策略的选择，本质上就是决定“总 RNA 里的哪些部分进入文库”",
           size=SIZE_LABEL, fill=COLOR_TEXT, anchor="middle", weight="bold")
    save("rna-classes", s)


def fig_lib_compare():
    W, H = 700, 470
    s = Svg(W, H, "富集 poly(A) 与去 rRNA 两种建库策略的对比",
            "顶部为 DNA 双链上一段基因与转录出的带 poly(A) 尾 mRNA；下方两条泳道分别为"
            "富集 poly(A) 与去 rRNA 的建库流程、各自能测到与测不到的 RNA 类型。")
    dx, dy = 190, 30
    s.text(dx, dy + 4, "DNA（双链）", size=SIZE_LABEL, fill=COLOR_MUTED)
    for xx in (dx + 96, dx + 104):
        s.line(xx, dy - 10, xx, dy + 22, stroke=COLOR_PRIMARY, sw=2.2)
    for xx in range(dx + 90, dx + 112, 6):
        s.line(xx, dy - 10, xx + 4, dy + 22, stroke="#d5ddd9", sw=1)
    for (ox, ow) in [(150, 26), (196, 34), (246, 22)]:
        s.rect(dx + ox, dy - 4, ow, 18, fill=COLOR_PRIMARY, rx=3)
    s.arrow(dx + 300, dy + 5, dx + 338, dy + 5)
    s.text(dx + 319, dy - 6, "转录", size=SIZE_NOTE, fill=COLOR_MUTED, anchor="middle")
    my = dy + 5
    s.text(dx + 388, my - 12, "RNA", size=SIZE_NOTE, fill=COLOR_MUTED, anchor="middle")
    exl = [(dx + 348, dx + 370), (dx + 380, dx + 406), (dx + 414, dx + 428)]
    prev = dx + 346
    for a0, b0 in exl:
        s.line(prev, my, a0, my, stroke=COLOR_PRIMARY, sw=2.4)
        s.rect(a0, my - 5, b0 - a0, 10, fill=COLOR_PRIMARY, rx=2)
        prev = b0
    s.line(prev, my, dx + 434, my, stroke=COLOR_PRIMARY, sw=2.4)
    for k in range(4):
        s.text(dx + 438 + k * 10, my + 4, "A", size=10, mono=True, fill="#b45309")
    lanes = [
        (58, "富集 poly(A)", COLOR_PRIMARY, "#f4faf8",
         ["磁珠捕获 poly(A) RNA", "片段化", "反转录＋加接头", "PCR 成文库"],
         ["测到：mRNA ＋ 含 poly(A) 尾的 lncRNA", "测不到：无尾 lncRNA、circRNA、rRNA"]),
        (266, "去 rRNA", "#b45309", "#fdf6ec",
         ["探针/酶去除 rRNA", "其余 RNA 全保留", "反转录＋加接头", "PCR 成文库"],
         ["测到：mRNA、lncRNA、circRNA 等", "代价：常有 5–20% read 来自残留 rRNA"]),
    ]
    for ly, title, color, fill, steps, outcome in lanes:
        s.text(28, ly + 13, title, size=SIZE_TITLE, fill=color, anchor="start", weight="bold")
        for i, step in enumerate(steps):
            bx = 28 + i * 160
            box(s, bx, ly + 24, 146, 42, step, fill=fill, stroke=color)
            if i < len(steps) - 1:
                s.arrow(bx + 148, ly + 45, bx + 158, ly + 45, sw=1.4)
        s.rect(28, ly + 84, 622, 52, fill="#ffffff", stroke="#cfe3dd", rx=8)
        for k, ln in enumerate(outcome):
            s.text(40, ly + 104 + k * 20, ln, size=SIZE_NOTE, fill=COLOR_TEXT)
    s.add("<path d='M 430 48 C 430 48, 260 50, 100 80' fill='none' stroke='#9ca3af' stroke-width='1.4'/>")
    s.arrow(100, 80, 96, 84, sw=1.4)
    s.add("<path d='M 430 48 C 430 48, 640 120, 660 288' fill='none' stroke='#9ca3af' stroke-width='1.4'/>")
    s.arrow(660, 288, 656, 292, sw=1.4)
    s.text(W / 2, H - 10, "研究蛋白编码基因、样本好 → 富集 poly(A)；覆盖非编码 RNA／circRNA 或有降解 → 去 rRNA",
           size=SIZE_LABEL, fill=COLOR_TEXT, anchor="middle", weight="bold")
    save("lib-compare", s)



def fig_stranded_lib():
    W, H = 700, 310
    s = Svg(W, H, "dUTP 链特异性建库流程示意图",
            "第一链 cDNA 正常合成；第二链以 dUTP 替代 dTTP；接头连接后 USER 酶特异降解含 dUTP 的第二链，"
            "只保留与原始 RNA 互补的第一链进入 PCR，read 与转录本链的对应关系因此确定。")
    y0 = 56
    P = COLOR_PRIMARY
    A = "#b45309"
    box(s, 22, y0, 104, 46, "RNA 转录本", fill="#f4faf8")
    box(s, 158, y0, 128, 46, "第一链 cDNA\n合成（dTTP）", fill="#f4faf8")
    box(s, 318, y0, 128, 46, "第二链 cDNA\n掺入 dUTP", fill="#fdf6ec", stroke=A)
    for i in range(5):
        s.add(f"<circle cx='{334 + i * 22}' cy='{y0 + 42}' r='3.4' fill='{A}'/>")
    box(s, 474, y0, 126, 46, "USER 酶降解\n含 dUTP 第二链", fill="none", stroke=A)
    box(s, 632, y0, 48, 46, "PCR", fill="#f4faf8")
    s.arrow(128, y0 + 23, 156, y0 + 23)
    s.arrow(288, y0 + 23, 316, y0 + 23)
    s.arrow(448, y0 + 23, 472, y0 + 23, stroke=A)
    s.arrow(602, y0 + 23, 630, y0 + 23)
    s.text(656, y0 - 10, "仅第一链", size=SIZE_NOTE, fill=COLOR_MUTED, anchor="middle")
    s.text(222, y0 + 64, "与 RNA 互补、保留", size=SIZE_NOTE, fill=COLOR_MUTED, anchor="middle")
    s.line(506, y0 + 2, 542, y0 + 44, stroke=A, sw=2.8)
    s.line(542, y0 + 2, 506, y0 + 44, stroke=A, sw=2.8)
    y1 = 196
    s.text(350, y1 - 30, "为什么能分清链：保留的第一链方向对应原始转录本，read 比对后唯一归属正链或负链",
           size=SIZE_LABEL, fill=COLOR_TEXT, anchor="middle")
    gxx = 196
    s.text(gxx - 118, y1 - 10, "基因组正链基因", size=SIZE_NOTE, fill=COLOR_MUTED, anchor="start")
    exl = [(gxx - 110, 26), (gxx - 60, 26), (gxx + 10, 26), (gxx + 70, 26), (gxx + 110, 26)]
    prev = gxx - 118
    for a0, w0 in exl:
        s.line(prev, y1, a0, y1, stroke=P, sw=2.4)
        s.rect(a0, y1 - 6, w0, 12, fill=P, rx=2)
        prev = a0 + w0
    s.line(prev, y1, gxx + 150, y1, stroke=P, sw=2.4)
    s.text(gxx + 162, y1 + 5, "read →", size=SIZE_NOTE, fill=P)
    s.text(gxx - 118, y1 + 44, "反义转录本", size=SIZE_NOTE, fill=COLOR_MUTED, anchor="start")
    exl2 = [(gxx - 90, 22), (gxx - 20, 22), (gxx + 50, 22), (gxx + 100, 22)]
    prev = gxx - 118
    for a0, w0 in exl2:
        s.line(prev, y1 + 54, a0, y1 + 54, stroke="#c4cbd0", sw=2)
        s.rect(a0, y1 + 48, w0, 12, fill=A, rx=2)
        prev = a0 + w0
    s.line(prev, y1 + 54, gxx + 150, y1 + 54, stroke="#c4cbd0", sw=2)
    s.text(gxx + 162, y1 + 59, "read →", size=SIZE_NOTE, fill=A)
    s.text(350, H - 8, "普通文库两条链的 read 混在一起；链特异性文库能把它们分开计数",
           size=SIZE_NOTE, fill=COLOR_MUTED, anchor="middle")
    save("stranded-lib", s)



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




# ─────────────────── 图L 建库策略树状图（重绘 001） ───────────────────
def fig_lib_tree():
    W, H = 600, 440
    s = Svg(W, H, "四种 RNA 测序建库策略",
            "总 RNA 经四种处理进入测序文库：富集 poly(A)、去 rRNA、去线性（RNase R）与小 RNA 文库，"
            "每条路线标注各自能测到的 RNA 类型。")
    box(s, 210, 20, 180, 40, "总 RNA 提取", fill=COLOR_FILL)
    lanes = [
        ("富集 poly(A)", "磁珠捕获带 poly(A) 尾的 RNA", "测到：mRNA、含尾 lncRNA", COLOR_PRIMARY),
        ("去 rRNA", "探针/酶去除 rRNA，其余保留", "测到：mRNA、lncRNA、circRNA 等", COLOR_PRIMARY),
        ("去线性（RNase R）", "降解线性 RNA，保留环形分子", "测到：circRNA（专项富集）", COLOR_WARN),
        ("小 RNA 文库", "按长度回收 18–30 nt 片段", "测到：miRNA 等小 RNA", COLOR_WARN),
    ]
    y0 = 110
    # 母线式布线：主干→左侧通道→各层横 stub 进框（先画线）
    s.line(300, 60, 300, 84, stroke=COLOR_LINE, sw=1.6)
    s.line(300, 84, 36, 84, stroke=COLOR_LINE, sw=1.6)
    s.line(36, 84, 36, y0 + 3 * 74 + 22, stroke=COLOR_LINE, sw=1.6)
    for k, (name, how, what, color) in enumerate(lanes):
        ly = y0 + k * 74
        bx, bw, bh = 60, 180, 44
        s.arrow(36, ly + 22, 56, ly + 22, sw=1.2)
        box(s, bx, ly, bw, bh, name, fill=COLOR_FILL)
        s.text(258, ly + 17, how, size=SIZE_NOTE, fill=COLOR_MUTED)
        s.text(258, ly + 36, what, size=SIZE_NOTE, fill=color)
    s.text(W / 2, H - 12, "同一批总 RNA，四种文库决定“谁能进入测序”（重绘自原稿示意图）",
           size=SIZE_LABEL, fill=COLOR_TEXT, anchor="middle", weight="bold")
    save("lib-tree", s)


# ─────────────────── 图M ceRNA 概念图（重绘 008） ───────────────────
def fig_cerna_concept():
    W, H = 560, 424
    s = Svg(W, H, "ceRNA：多种 RNA 竞争结合 miRNA",
            "mRNA、lncRNA、circRNA 都携带 miRNA 结合位点，像海绵一样竞争结合同一批 miRNA，"
            "间接影响彼此的翻译抑制强度。")
    cx, cy = 280, 200
    nodes = [
        (110, 60, "mRNA", "3′ UTR 结合位点", COLOR_PRIMARY),
        (450, 60, "lncRNA", "部分含结合位点", COLOR_PRIMARY),
        (450, 340, "circRNA", "环形骨架上多位点", COLOR_WARN),
    ]
    # 先画连线（铁律：线先字后）
    for nx, ny, *_ in nodes:
        s.line(nx, ny, cx, cy, stroke=COLOR_LINE, sw=1.4)
    # 结合位点小刻度画在连线上
    for t in (0.35, 0.55):
        for nx, ny, *_ in nodes:
            mx, my = nx + (cx - nx) * t, ny + (cy - ny) * t
            s.rect(mx - 5, my - 5, 10, 10, fill=COLOR_FILL, stroke=COLOR_PRIMARY, rx=2)
    # 中央 miRNA
    s.add(f"<circle cx='{cx}' cy='{cy}' r='34' fill='{COLOR_FILL}' stroke='{COLOR_PRIMARY}' stroke-width='1.8'/>")
    s.text(cx, cy + 5, "miRNA", size=SIZE_TITLE, mono=False, fill=COLOR_PRIMARY, anchor="middle", weight="bold")
    for nx, ny, name, note, color in nodes:
        box(s, nx - 62, ny - 22, 124, 44, name, fill="#ffffff", tcolor=color)
        s.text(nx, ny + 40, note, size=SIZE_NOTE, fill=COLOR_MUTED, anchor="middle")
    s.text(W / 2, H - 12, "结合位点越多、亲和力越强，“海绵”作用越强（重绘自原稿示意图）",
           size=SIZE_LABEL, fill=COLOR_TEXT, anchor="middle", weight="bold")
    save("cerna-concept", s)


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
    fig_lib_tree()
    fig_cerna_concept()
