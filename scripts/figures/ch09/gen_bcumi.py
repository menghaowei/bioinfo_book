#!/usr/bin/env python3
"""第9章 图9.2：barcode、UMI 与计数矩阵的对应关系（v2 全要素重排）。

v1 反馈（作者，2026-10-11）：效果不好、有遮挡——去重箭头穿过矩阵标题、
read3 箭头横穿矩阵行。v2 布局：左区三条 read＋段标注与基因归属；中 corridor
放两个"分子"标记；右区矩阵；全部箭头走空白走廊，不穿文字。

教学要点（与 9.1 节正文一致）：
- read 分三段：细胞 barcode（归细胞）＋UMI（归分子）＋cDNA（比对定基因）；
- 同 barcode 同 UMI = 同一 mRNA 分子的 PCR 重复，去重后只计 1 个分子；
- 计数矩阵中一个数字 = 某细胞某基因的 UMI 分子数。
依据：Zheng et al. Nat Commun 2017;8:14049（示意，序列未按实际长度绘制）。

运行：python3 scripts/figures/ch09/gen_bcumi.py
输出：assets/09-single-cell-and-spatial-omics/002-bc-umi-matrix.svg
"""
from common import (Svg, save, COLOR_TEXT, COLOR_MUTED, COLOR_PRIMARY,
                    COLOR_FILL, COLOR_WARN, COLOR_WARN_FILL, COLOR_LINE,
                    COLOR_BLUE, COLOR_BLUE_FILL, SIZE_NOTE, SIZE_TITLE)

CW = 13          # 等宽字符栅格
BAR_H = 30       # read 条高度

BC = "AACGTACGTA"


def read_bar(s, x, y, umi, fill_umi):
    """一条 read：[barcode 段][UMI 段][cDNA 段]，先画底再画字。返回总宽。"""
    w_bc, w_umi, w_cdna = len(BC) * CW + 12, len(umi) * CW + 12, 8 * CW + 12
    s.rect(x, y, w_bc, BAR_H, fill=COLOR_FILL, stroke=COLOR_PRIMARY)
    s.rect(x + w_bc, y, w_umi, BAR_H, fill=fill_umi, stroke=COLOR_WARN)
    s.rect(x + w_bc + w_umi, y, w_cdna, BAR_H, stroke=COLOR_LINE)
    s.text(x + 6, y + 20, BC, size=13, fill=COLOR_TEXT)
    s.text(x + w_bc + 6, y + 20, umi, size=13, fill=COLOR_TEXT)
    s.text(x + w_bc + w_umi + 6, y + 20, "cDNA…", size=13, fill=COLOR_MUTED)
    return w_bc + w_umi + w_cdna


def main():
    W, H = 920, 392
    s = Svg(W, H, "barcode、UMI 与计数矩阵的对应关系",
            "三条 read 带相同细胞 barcode AACGTACGTA；前两条 UMI 相同（TTAGGC），"
            "是同一 mRNA 分子的 PCR 重复，按 UMI 去重只计 1 个分子并归属 Gene1；"
            "第三条 UMI 不同（CCGATA），是另一个分子，归属 Gene2。"
            "右侧计数矩阵高亮列即该细胞，数字为 UMI 分子数。示意，未按实际长度绘制。")

    x0 = 60
    y1, y2, y3 = 100, 156, 212                     # 三条 read 的 y
    w1 = read_bar(s, x0, y1, "TTAGGC", COLOR_WARN_FILL)   # read1 → Gene1
    read_bar(s, x0, y2, "TTAGGC", COLOR_WARN_FILL)        # read2（PCR 重复）→ Gene1
    read_bar(s, x0, y3, "CCGATA", COLOR_BLUE_FILL)        # read3 → Gene2

    # ── 段标注（对齐 read1 三段正上方）──
    w_bc = len(BC) * CW + 12                       # 142
    w_umi = 6 * CW + 12                            # 90
    for cx, lab in ((x0 + w_bc / 2, "细胞 barcode"),
                    (x0 + w_bc + w_umi / 2, "UMI"),
                    (x0 + w_bc + w_umi + 58, "cDNA")):
        s.text(cx, 76, lab, size=11, mono=False, fill=COLOR_MUTED, anchor="middle")
        s.line(cx, 82, cx, 94, stroke=COLOR_LINE, sw=1)   # 引线小刻度
    s.text(x0 + w_bc / 2, 58, "归细胞", size=10, mono=False, fill=COLOR_PRIMARY,
           anchor="middle")
    s.text(x0 + w_bc + w_umi / 2, 58, "归分子", size=10, mono=False,
           fill=COLOR_WARN, anchor="middle")
    s.text(x0 + w_bc + w_umi + 58, 58, "比对定基因", size=10, mono=False,
           fill=COLOR_MUTED, anchor="middle")

    # ── 基因归属（cDNA 段右侧，短标签避免与说明冲突）──
    s.text(x0 + w1 + 12, y1 + 20, "Gene1", size=13, fill=COLOR_TEXT)
    s.text(x0 + w1 + 12, y2 + 20, "Gene1", size=13, fill=COLOR_TEXT)
    s.text(x0 + w1 + 12, y3 + 20, "Gene2", size=13, fill=COLOR_TEXT)

    # ── PCR 重复虚线分组（read1＋read2）──
    s.rect(x0 - 14, 88, w1 + 28, 110, stroke=COLOR_WARN, dash="5,4", sw=1.2)
    s.text(x0 - 14, 214, "└ barcode 与 UMI 都相同", size=11, mono=False,
           fill=COLOR_WARN)

    # ── 中 corridor：两个分子标记 ──
    mk1 = (480, 140, 132, 26, COLOR_WARN_FILL, COLOR_WARN, "去重后 1 个分子")
    mk2 = (480, 252, 132, 26, COLOR_BLUE_FILL, COLOR_BLUE, "另 1 个分子")
    for mx, my, mw, mh, f, st, lab in (mk1, mk2):
        s.rect(mx, my, mw, mh, fill=f, stroke=st, rx=4)
        s.text(mx + mw / 2, my + 17, lab, size=SIZE_NOTE, mono=False,
               fill=COLOR_TEXT, anchor="middle")
    # 分组框 → 分子1
    s.arrow(x0 + w1 + 28, 143, 480, 153)
    # read3 底部折线 → 分子2（绕开 Gene2 标签）
    s.line(x0 + 170, y3 + BAR_H, x0 + 170, 265, stroke=COLOR_PRIMARY, sw=1.6)
    s.line(x0 + 170, 265, 480, 265, stroke=COLOR_PRIMARY, sw=1.6)

    # ── 右区：计数矩阵 ──
    mtitle_y = 116
    s.text(735, mtitle_y, "细胞×基因计数矩阵（数字 = UMI 分子数）",
           size=SIZE_TITLE, mono=False, fill=COLOR_PRIMARY, weight="bold",
           anchor="middle")
    mx0, my0 = 646, 130
    col_ws = [36, 110, 36]                          # …/AACGTACGTA/…
    col_x = [mx0, mx0 + 36, mx0 + 146]
    row_h, n_rows = 34, 4
    rows = ["Gene1", "Gene2", "Gene3", "…"]
    vals = {0: ("1", COLOR_WARN), 1: ("1", COLOR_BLUE), 2: ("0", COLOR_MUTED)}
    # 列头
    heads = ["…", BC, "…"]
    for j in range(3):
        if j == 1:
            s.rect(col_x[j] + 1, my0, col_ws[j] - 2, 22, fill=COLOR_FILL)
        s.text(col_x[j] + col_ws[j] / 2, my0 + 15, heads[j], size=10,
               anchor="middle", fill=COLOR_TEXT if j == 1 else COLOR_MUTED)
    # 行
    for i, r in enumerate(rows):
        ry = my0 + 26 + i * row_h
        s.text(mx0 - 10, ry + 22, r, size=12, anchor="end", fill=COLOR_TEXT)
        for j in range(3):
            if j == 1:
                s.rect(col_x[j] + 1, ry + 2, col_ws[j] - 2, row_h - 4,
                       fill=COLOR_FILL, stroke=COLOR_PRIMARY)
                v, vc = vals.get(i, ("0", COLOR_MUTED))
                s.text(col_x[j] + col_ws[j] / 2, ry + 23, v, size=14,
                       anchor="middle", fill=vc, weight="bold")
            else:
                s.rect(col_x[j] + 1, ry + 2, col_ws[j] - 2, row_h - 4,
                       stroke=COLOR_LINE, dash="3,3")
                s.text(col_x[j] + col_ws[j] / 2, ry + 23, "·", size=12,
                       anchor="middle", fill=COLOR_LINE)
    # 分子 → 矩阵（沿空白走廊，不穿文字）
    s.arrow(612, 153, 690, 172)                      # 分子1 → Gene1 格
    s.arrow(612, 265, 690, 208)                      # 分子2 → Gene2 格

    # ── 底部小结 ──
    s.text(x0, 336, "前两条 read 是同一个分子的 PCR 重复：按 UMI 去重，只给 Gene1 记 1（琥珀）；"
           "第三条 UMI 不同，给 Gene2 记 1（蓝色）。",
           size=SIZE_NOTE, mono=False, fill=COLOR_TEXT)
    s.text(x0, 360, "矩阵里一个数字的含义：这个细胞里，这个基因被捕获并计数到几个 UMI 分子（去重后）。",
           size=SIZE_NOTE, mono=False, fill=COLOR_MUTED)

    save("002-bc-umi-matrix", s)


if __name__ == "__main__":
    main()
