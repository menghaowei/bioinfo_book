#!/usr/bin/env python3
"""第9章 barcode/UMI → 计数矩阵示意图（002-bc-umi-matrix.svg，锚点 fig-09-bc-umi）。

教学要点（与 9.1 节正文一致）：
- 每条 read 分三段：细胞 barcode（归细胞）＋UMI（归分子）＋cDNA 序列；
- 同 barcode 同 UMI 的两条 read 是 PCR 重复，按 UMI 去重只计 1 个分子；
- 计数矩阵中一个数字 = 某细胞某基因的 UMI 分子数。

依据：Zheng et al. Nat Commun 2017;8:14049（10x 早期版本为 14 bp barcode＋10 bp UMI，
示意图中按比例缩短，注明"未按实际长度绘制"）。

运行：python3 scripts/figures/ch09/gen_bcumi.py
"""
from common import (Svg, save, COLOR_TEXT, COLOR_MUTED, COLOR_PRIMARY,
                    COLOR_FILL, COLOR_WARN, COLOR_WARN_FILL, COLOR_LINE,
                    COLOR_BLUE, COLOR_BLUE_FILL, SIZE_NOTE, SIZE_TITLE)

CW = 13          # 等宽字符栅格
BAR_H = 30       # read 条高度


def read_bar(s, x, y, bc, umi, fill_umi):
    """一条 read：[barcode 段][UMI 段][cDNA 段]，先画底再画字。"""
    w_bc, w_umi, w_cdna = len(bc) * CW + 12, len(umi) * CW + 12, 8 * CW + 12
    s.rect(x, y, w_bc, BAR_H, fill=COLOR_FILL, stroke=COLOR_PRIMARY)
    s.rect(x + w_bc, y, w_umi, BAR_H, fill=fill_umi, stroke=COLOR_WARN)
    s.rect(x + w_bc + w_umi, y, w_cdna, BAR_H, stroke=COLOR_LINE)
    # 序列文字居中
    s.text(x + 6, y + 20, bc, size=13, fill=COLOR_TEXT)
    s.text(x + w_bc + 6, y + 20, umi, size=13, fill=COLOR_TEXT)
    s.text(x + w_bc + w_umi + 6, y + 20, "cDNA…", size=13, fill=COLOR_MUTED)
    return w_bc + w_umi + w_cdna


def main():
    W, H = 900, 430
    s = Svg(W, H, "barcode、UMI 与计数矩阵的对应关系",
            "三条 read 带相同细胞 barcode AACGTACGTA；前两条 UMI 相同（TTAGGC），"
            "是同一 mRNA 分子的 PCR 重复，去重后只计 1 个分子并归属到 Gene1；"
            "第三条 UMI 不同（CCGATA），是另一个分子，归属到 Gene2。"
            "右下计数矩阵中高亮列即该细胞，数字为 UMI 分子数（示意，未按实际长度绘制）。")

    x0, y0 = 60, 70
    bc = "AACGTACGTA"

    # ── 左侧：三条 read ──
    s.text(x0 - 12, y0 - 16, "测序得到的 read（同一细胞 barcode）",
           size=SIZE_TITLE, mono=False, fill=COLOR_PRIMARY, weight="bold")
    w1 = read_bar(s, x0, y0, bc, "TTAGGC", COLOR_WARN_FILL)               # read1 → Gene1
    w2 = read_bar(s, x0, y0 + 56, bc, "TTAGGC", COLOR_WARN_FILL)          # read2（PCR 重复）→ Gene1
    w3 = read_bar(s, x0, y0 + 112, bc, "CCGATA", COLOR_BLUE_FILL)         # read3 → Gene2

    # 基因归属注记（cDNA 段右侧）
    s.text(x0 + w1 + 10, y0 + 20, "→ 比对到 Gene1", size=SIZE_NOTE, mono=False, fill=COLOR_TEXT)
    s.text(x0 + w2 + 10, y0 + 76, "→ 比对到 Gene1", size=SIZE_NOTE, mono=False, fill=COLOR_TEXT)
    s.text(x0 + w3 + 10, y0 + 132, "→ 比对到 Gene2", size=SIZE_NOTE, mono=False, fill=COLOR_TEXT)

    # 段说明（顶部标注，指向各段）
    seg_y = y0 - 34
    s.text(x0 + 6, seg_y, "细胞 barcode（归细胞）", size=11, mono=False, fill=COLOR_MUTED)
    s.text(x0 + w1 - 10 * CW, seg_y + 16, "UMI（归分子）", size=11, mono=False, fill=COLOR_WARN)
    s.text(x0 + w1 + 20, seg_y, "cDNA（比对定基因）", size=11, mono=False, fill=COLOR_MUTED)

    # ── 中部：UMI 去重（虚线分组框 + 说明）──
    grp_y = y0 - 14
    s.rect(x0 - 14, grp_y, w1 + 28, 100, stroke=COLOR_WARN, dash="5,4", sw=1.2)
    s.text(x0 + w1 + 44, grp_y + 40, "barcode 相同＋UMI 相同", size=SIZE_NOTE, mono=False,
           fill=COLOR_TEXT)
    s.text(x0 + w1 + 44, grp_y + 58, "= 同一分子的 PCR 重复", size=SIZE_NOTE, mono=False,
           fill=COLOR_TEXT)
    s.text(x0 + w1 + 44, grp_y + 76, "去重后计 1 个分子", size=SIZE_NOTE, mono=False,
           fill=COLOR_WARN, weight="bold")

    # ── 右下：计数矩阵 ──
    mx, my, cw, ch = 560, 210, 92, 34
    cols = ["…", "AACGTACGTA", "…", "…"]
    rows = ["Gene1", "Gene2", "Gene3", "…"]
    hi = 1                                    # 高亮列（本例细胞）
    s.text(mx, my - 26, "细胞×基因计数矩阵（数字 = UMI 分子数）",
           size=SIZE_TITLE, mono=False, fill=COLOR_PRIMARY, weight="bold")
    # 列头
    for j, c in enumerate(cols):
        col_x = mx + j * cw
        if j == hi:
            s.rect(col_x + 2, my - 24, cw - 4, 24, fill=COLOR_FILL)
        s.text(col_x + cw / 2, my - 8, c, size=11, anchor="middle",
               fill=COLOR_TEXT if j == hi else COLOR_MUTED)
    # 行
    vals = {("Gene1", 1): "1", ("Gene2", 1): "1", ("Gene3", 1): "0"}
    for i, r in enumerate(rows):
        ry = my + i * ch
        s.text(mx - 12, ry + 22, r, size=12, anchor="end", fill=COLOR_TEXT)
        for j in range(len(cols)):
            col_x = mx + j * cw
            if j == hi:
                s.rect(col_x + 2, ry + 2, cw - 4, ch - 4, fill=COLOR_FILL,
                       stroke=COLOR_PRIMARY)
                v = vals.get((r, 1), "0")
                s.text(col_x + cw / 2, ry + 23, v, size=14, anchor="middle",
                       fill=COLOR_TEXT, weight="bold")
            else:
                s.rect(col_x + 2, ry + 2, cw - 4, ch - 4, stroke=COLOR_LINE,
                       dash="3,3")
                s.text(col_x + cw / 2, ry + 23, "·", size=12, anchor="middle",
                       fill=COLOR_LINE)

    # ── 去重结果 → 矩阵的箭头 ──
    s.arrow(x0 + w1 + 44 + 128, grp_y + 84, mx + hi * cw + cw / 2, my + 2)      # 分子1 → Gene1 格
    s.arrow(x0 + w3 + 60, y0 + 112 + BAR_H, mx + hi * cw + cw / 2 + 26, my + 34)  # 分子2 → Gene2 格

    # 底部小结
    s.text(x0 - 14, H - 26,
           "一个数字的含义：这个细胞里，这个基因被捕获并计数到几个 UMI 分子。",
           size=SIZE_NOTE, mono=False, fill=COLOR_MUTED)

    save("002-bc-umi-matrix", s)


if __name__ == "__main__":
    main()
