#!/usr/bin/env python3
"""第9章 图9.1：10x Genomics 与 BD Rhapsody 单细胞捕获流程对比（重绘自课程原图）。

信息边界（作者确认，2026-10-11）：只画"微反应载体"层——怎么把一个细胞和一个
条形码载体关进一个小空间；barcode/UMI 细节留给图 9.2，本图不重复。
依据：Zheng 2017 Nat Commun（GEM 过程）、Fan 2015 Science（CytoSeq 微孔板）。

运行：python3 scripts/figures/ch09/gen_platforms.py
输出：assets/09-single-cell-and-spatial-omics/008-10x-bd-platforms.svg
"""
import math
from common import (Svg, save, COLOR_TEXT, COLOR_MUTED, COLOR_PRIMARY,
                    COLOR_FILL, COLOR_WARN, COLOR_WARN_FILL, COLOR_LINE,
                    SIZE_NOTE, SIZE_TITLE)

BOX_W = 330
BOX_H = 64


def step_box(s, x, y, title, sub):
    """步骤框：第一行加粗步骤名，第二行灰色补充。先框后字。"""
    s.rect(x, y, BOX_W, BOX_H, stroke=COLOR_PRIMARY, rx=6)
    s.text(x + 14, y + 26, title, size=SIZE_NOTE, mono=False,
           fill=COLOR_TEXT, weight="bold")
    s.text(x + 14, y + 48, sub, size=11, mono=False, fill=COLOR_MUTED)


def down_arrow(s, cx, y1, y2):
    s.line(cx, y1, cx, y2, stroke=COLOR_PRIMARY, sw=1.8)
    for da in (0.42, -0.42):
        s.line(cx, y2, cx - 8 * math.sin(da), y2 - 9 * math.cos(da),
               stroke=COLOR_PRIMARY, sw=1.8)


def droplet_motif(s, cx, cy):
    """10x：油包水液滴——圆内一个细胞（小圆）＋一颗凝胶珠（小方块）。"""
    s.add(f"<circle cx='{cx}' cy='{cy}' r='26' fill='{COLOR_FILL}' "
          f"stroke='{COLOR_PRIMARY}' stroke-width='1.4'/>")
    s.add(f"<circle cx='{cx - 8}' cy='{cy + 4}' r='7' fill='none' "
          f"stroke='{COLOR_TEXT}' stroke-width='1.4'/>")            # 细胞
    s.add(f"<circle cx='{cx - 8}' cy='{cy + 4}' r='2.5' fill='{COLOR_TEXT}'/>")  # 细胞核
    s.rect(cx + 6, cy - 4, 11, 11, fill=COLOR_WARN_FILL, stroke=COLOR_WARN)     # 凝胶珠
    s.text(cx, cy + 44, "GEM：油包水液滴", size=11, mono=False,
           fill=COLOR_MUTED, anchor="middle")


def microwell_motif(s, cx, cy):
    """BD：蜂窝板微孔——三个六边形孔，两孔各一细胞，磁珠落入一孔。"""
    r = 15
    for dx, dy in ((-16, 9), (16, 9), (0, -8)):
        pts = []
        for k in range(6):
            a = math.pi / 6 + k * math.pi / 3
            pts.append((cx + dx + r * math.cos(a), cy + dy + r * math.sin(a)))
        pstr = " ".join(f"{px:.1f},{py:.1f}" for px, py in pts)
        s.add(f"<polygon points='{pstr}' fill='none' stroke='{COLOR_PRIMARY}' "
              f"stroke-width='1.4'/>")
    s.add(f"<circle cx='{cx - 16}' cy='{cy + 9}' r='6' fill='none' "
          f"stroke='{COLOR_TEXT}' stroke-width='1.3'/>")            # 孔内细胞
    s.rect(cx - 4, cy - 12, 9, 9, fill=COLOR_WARN_FILL, stroke=COLOR_WARN)      # 孔内磁珠
    s.text(cx, cy + 44, "微孔板：一孔一细胞", size=11, mono=False,
           fill=COLOR_MUTED, anchor="middle")


def main():
    W, H = 880, 660
    s = Svg(W, H, "10x Genomics 与 BD Rhapsody 单细胞捕获流程对比",
            "左栏 10x 液滴法五步：两路液流在微流控节点被油相包裹成 GEM，"
            "液滴内裂解反转录，破乳合并扩增建库；右栏 BD 微孔板法三步："
            "细胞重力落入蜂窝板微孔，磁珠入孔配对，孔内完成反应。"
            "两栏底部汇合：把一个细胞和一个条形码载体关进一个小空间，后续建库测序几乎一致。")

    # ── 栏标题与示意图 ──
    lx, rx = 40, 500                     # 两栏左上角
    s.text(lx + BOX_W / 2, 40, "10x Genomics（液滴法）", size=SIZE_TITLE,
           mono=False, fill=COLOR_PRIMARY, weight="bold", anchor="middle")
    s.text(rx + BOX_W / 2, 40, "BD Rhapsody（微孔板法）", size=SIZE_TITLE,
           mono=False, fill=COLOR_PRIMARY, weight="bold", anchor="middle")
    droplet_motif(s, lx + 70, 100)
    microwell_motif(s, rx + 70, 100)

    # ── 左栏五步 ──
    left = [
        ("① 两路液流汇入微流控节点", "细胞＋试剂一条通道，凝胶珠（带寡核苷酸）另一条"),
        ("② 油相包裹成 GEM 液滴", "理想情况：一个液滴里进入一个细胞和一颗凝胶珠"),
        ("③ 液滴内：裂解与反转录", "凝胶珠溶解释放引物，cDNA 带上 barcode 和 UMI"),
        ("④ 破乳合并，统一扩增建库", "所有液滴的 cDNA 合并成一个文库"),
        ("⑤ 测序：read 自带条形码", "barcode 归细胞、UMI 归分子（见下图）"),
    ]
    y = 170
    step_gap = 18
    for i, (t, sub) in enumerate(left):
        step_box(s, lx, y, t, sub)
        if i < len(left) - 1:
            down_arrow(s, lx + BOX_W / 2, y + BOX_H, y + BOX_H + step_gap)
        y += BOX_H + step_gap

    # ── 右栏三步 ──
    right = [
        ("① 悬液流过蜂窝板", "数十万微孔，细胞靠重力落入，理想一孔一细胞"),
        ("② 磁珠铺板，入孔配对", "带寡核苷酸的磁珠落入微孔，与细胞同处一孔"),
        ("③ 微孔内：裂解与反转录", "孔就是反应器，cDNA 同样带上条形码"),
    ]
    y = 170
    for i, (t, sub) in enumerate(right):
        step_box(s, rx, y, t, sub)
        if i < len(right) - 1:
            down_arrow(s, rx + BOX_W / 2, y + BOX_H, y + BOX_H + step_gap)
        y += BOX_H + step_gap

    # ── 底部汇合框 ──
    rail_y = 585                     # 汇合轨道：低于左栏末框（562）与右栏末框（398）
    hub_top = 600
    left_cx, right_cx = lx + BOX_W / 2, rx + BOX_W / 2
    s.line(left_cx, 562, left_cx, rail_y, stroke=COLOR_PRIMARY, sw=1.8)
    s.line(right_cx, 398, right_cx, rail_y, stroke=COLOR_PRIMARY, sw=1.8)
    s.line(left_cx, rail_y, right_cx, rail_y, stroke=COLOR_PRIMARY, sw=1.8)
    mid = (left_cx + right_cx) / 2
    down_arrow(s, mid, rail_y, hub_top)
    s.rect(mid - 330, hub_top, 660, 44, fill=COLOR_FILL,
           stroke=COLOR_PRIMARY, rx=6)
    s.text(mid, hub_top + 27, "殊途同归：把一个细胞和一个条形码载体关进一个小空间，"
           "后续建库、测序流程几乎一致", size=SIZE_NOTE, mono=False,
           fill=COLOR_TEXT, anchor="middle")

    save("008-10x-bd-platforms", s)


if __name__ == "__main__":
    main()
