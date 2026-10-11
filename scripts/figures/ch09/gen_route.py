#!/usr/bin/env python3
"""第9章 全章路线图（001-ch09-route.svg，锚点 fig-06-rna-seq-009）。

重绘自原稿课程流程图（原 jpg 保留于 assets/06-rna-seq/009-sc-rna-seq-analysis.jpg），
扩展为覆盖单细胞线与空间线的完整路线，两线在"去卷积与参考映射"汇合。

运行：python3 scripts/figures/ch09/gen_route.py
"""
from common import (Svg, save, COLOR_TEXT, COLOR_MUTED, COLOR_PRIMARY,
                    COLOR_FILL, COLOR_WARN, COLOR_WARN_FILL, COLOR_LINE,
                    SIZE_NOTE, SIZE_TITLE)

BOX_W, BOX_H = 112, 46


def step(s, x, y, label, sec, *, fill=COLOR_FILL, stroke=COLOR_PRIMARY):
    """流程框：主文字 + 灰色小节号。先画框后画字。"""
    s.rect(x, y, BOX_W, BOX_H, fill=fill, stroke=stroke)
    lines = label.split("\n")
    line_h = 17
    y0 = y + BOX_H / 2 - ((len(lines) - 1) * line_h + 13) / 2 + 11
    for k, ln in enumerate(lines):
        s.text(x + BOX_W / 2, y0 + k * line_h, ln, size=SIZE_NOTE, mono=False,
               fill=COLOR_TEXT, anchor="middle")
    s.text(x + BOX_W / 2, y + BOX_H - 7, sec, size=11, mono=False,
           fill=COLOR_MUTED, anchor="middle")


def main():
    W, H = 880, 368
    s = Svg(W, H, "第9章分析路线图",
            "上方为单细胞线：计数矩阵经质控、归一化与特征选择、降维聚类、注释、"
            "多样本比较；下方为空间线：spaceranger 矩阵经 spot 质控、空间可视化与区域解释；"
            "两线在去卷积与参考映射处汇合，随后是完整案例与误区核查。")

    y1, y2 = 56, 246
    x0 = 110
    gap = 16

    # 泳道标题
    s.text(24, y1 + BOX_H / 2 + 5, "单细胞线", size=SIZE_TITLE, mono=False,
           fill=COLOR_PRIMARY, weight="bold")
    s.text(24, y2 + BOX_H / 2 + 5, "空间线", size=SIZE_TITLE, mono=False,
           fill=COLOR_PRIMARY, weight="bold")

    # ── 上泳道：单细胞线 ──
    top = [
        ("计数矩阵\ncellranger", "9.1"),
        ("细胞质控", "9.2"),
        ("归一化与\n特征选择", "9.3"),
        ("降维与聚类", "9.3"),
        ("细胞类型注释", "9.4"),
        ("多样本比较", "9.5"),
    ]
    for i, (lab, sec) in enumerate(top):
        x = x0 + i * (BOX_W + gap)
        step(s, x, y1, lab, sec)
        if i:
            s.arrow(x - gap + 2, y1 + BOX_H / 2, x - 2, y1 + BOX_H / 2)

    # ── 下泳道：空间线 ──
    bot = [
        ("spot 计数矩阵\nspaceranger", "9.6"),
        ("spot 质控", "9.6"),
        ("空间可视化", "9.7"),
        ("组织区域识别", "9.7"),
    ]
    for i, (lab, sec) in enumerate(bot):
        x = x0 + i * (BOX_W + gap)
        step(s, x, y2, lab, sec)
        if i:
            s.arrow(x - gap + 2, y2 + BOX_H / 2, x - 2, y2 + BOX_H / 2)

    # ── 汇合框：去卷积与参考映射（右侧，位于两泳道之间）──
    hub_x, hub_y, hub_w, hub_h = 690, 140, 170, 116
    s.rect(hub_x, hub_y, hub_w, hub_h, fill=COLOR_WARN_FILL, stroke=COLOR_WARN)
    s.text(hub_x + hub_w / 2, hub_y + 34, "去卷积与参考映射", size=SIZE_NOTE, mono=False,
           fill=COLOR_TEXT, anchor="middle", weight="bold")
    s.text(hub_x + hub_w / 2, hub_y + 56, "单细胞参考解释 spot 构成", size=11, mono=False,
           fill=COLOR_TEXT, anchor="middle")
    s.text(hub_x + hub_w / 2, hub_y + 74, "空间分布印证细胞状态", size=11, mono=False,
           fill=COLOR_TEXT, anchor="middle")
    s.text(hub_x + hub_w / 2, hub_y + 102, "9.8", size=11, mono=False,
           fill=COLOR_MUTED, anchor="middle")

    # 上泳道末框 → 汇合框（末框底部中央向下）
    top_last_x = x0 + 5 * (BOX_W + gap)          # 第 6 框
    s.arrow(top_last_x + BOX_W / 2, y1 + BOX_H, hub_x + hub_w / 2 - 28, hub_y - 2)
    # 下泳道末框 → 汇合框（末框右侧斜向上）
    bot_last_x = x0 + 3 * (BOX_W + gap)          # 第 4 框
    s.arrow(bot_last_x + BOX_W, y2 + BOX_H / 2, hub_x - 4, hub_y + hub_h - 14)

    # ── 底部收束：完整案例与检查点 ──
    fin_x, fin_y, fin_w, fin_h = x0, 330, 750, 32
    s.rect(fin_x, fin_y, fin_w, fin_h, stroke=COLOR_LINE, dash="5,4")
    s.text(fin_x + fin_w / 2, fin_y + 21, "完整案例与检查点清单 · 常见误区（9.8）",
           size=SIZE_NOTE, mono=False, fill=COLOR_TEXT, anchor="middle")
    s.arrow(hub_x + hub_w / 2, hub_y + hub_h, hub_x + hub_w / 2, fin_y - 2)

    # 输入注记
    s.text(x0, y1 - 14, "输入：细胞×基因 UMI 计数矩阵", size=SIZE_NOTE, mono=False, fill=COLOR_MUTED)
    s.text(x0, y2 - 14, "输入：spot×基因计数矩阵＋空间坐标", size=SIZE_NOTE, mono=False, fill=COLOR_MUTED)

    save("001-ch09-route", s)


if __name__ == "__main__":
    main()
