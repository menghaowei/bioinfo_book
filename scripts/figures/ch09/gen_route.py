#!/usr/bin/env python3
"""第9章 图9.3：全章路线图（v2 竖版，仿第8章图8.4 风格；作者 2026-10-11 反馈）。

v1 为横版双泳道；v2 改竖版双列：左列单细胞线六步、右列空间线四步，
每步框内附一行琥珀色检查点（8.4 风格的"输出/目的/检查"压缩为步名＋检查），
底部汇合到"去卷积与参考映射"，再收束到完整案例与误区。
重绘自原稿课程流程图（原 jpg 保留于 assets/06-rna-seq/009-sc-rna-seq-analysis.jpg）。

运行：python3 scripts/figures/ch09/gen_route.py
输出：assets/09-single-cell-and-spatial-omics/001-ch09-route.svg
"""
import math
from common import (Svg, save, COLOR_TEXT, COLOR_MUTED, COLOR_PRIMARY,
                    COLOR_FILL, COLOR_WARN, COLOR_WARN_FILL, COLOR_LINE,
                    SIZE_NOTE, SIZE_TITLE)

BOX_W, BOX_H, GAP = 340, 64, 30


def step_box(s, x, y, name, check):
    """步骤框：加粗步名＋琥珀检查点。先框后字。"""
    s.rect(x, y, BOX_W, BOX_H, stroke=COLOR_PRIMARY, rx=6)
    s.text(x + 14, y + 26, name, size=SIZE_NOTE, mono=False,
           fill=COLOR_TEXT, weight="bold")
    s.text(x + 14, y + 48, "检查：" + check, size=11, mono=False,
           fill=COLOR_WARN)


def down_arrow(s, cx, y1, y2):
    s.line(cx, y1, cx, y2, stroke=COLOR_PRIMARY, sw=1.8)
    for da in (0.42, -0.42):
        s.line(cx, y2, cx - 8 * math.sin(da), y2 - 9 * math.cos(da),
               stroke=COLOR_PRIMARY, sw=1.8)


def main():
    W, H = 880, 800
    s = Svg(W, H, "第9章分析路线图（竖版）",
            "左列单细胞线六步：读入计数矩阵、细胞质控、归一化与高变基因、降维与聚类、"
            "细胞类型注释、多样本比较；右列空间线四步：Space Ranger 计数矩阵、spot 质控、"
            "空间可视化、区域识别与注释；每步附一行检查点；两列在去卷积与参考映射处汇合，"
            "收束到完整案例与常见误区。")

    # 顶部主旨句（仿 8.4）
    s.text(40, 36, "两条线各自把“表达”整理成可比较、可定位的对象，最后在去卷积与参考映射处汇合",
           size=SIZE_TITLE, mono=False, fill=COLOR_PRIMARY, weight="bold")

    lx, rx = 40, 500
    # ── 左列：单细胞线 ──
    s.text(lx + BOX_W / 2, 66, "单细胞线（9.1–9.5）", size=SIZE_TITLE, mono=False,
           fill=COLOR_PRIMARY, weight="bold", anchor="middle")
    s.text(lx + BOX_W / 2, 86, "输入：细胞×基因 UMI 计数矩阵", size=SIZE_NOTE,
           mono=False, fill=COLOR_MUTED, anchor="middle")
    left = [
        ("① 读入计数矩阵", "三件套齐全、barcode 数合理"),
        ("② 细胞质控", "阈值有组织依据；双细胞比例"),
        ("③ 归一化与高变基因", "高变基因含已知身份基因"),
        ("④ 降维与聚类", "主成分数、分辨率都要报告"),
        ("⑤ 细胞类型注释", "经典 marker 互证，证据分级"),
        ("⑥ 多样本比较", "整合未抹掉目标信号；伪批量用真重复"),
    ]
    y = 100
    for i, (name, check) in enumerate(left):
        step_box(s, lx, y, name, check)
        if i < len(left) - 1:
            down_arrow(s, lx + BOX_W / 2, y + BOX_H, y + BOX_H + GAP)
        y += BOX_H + GAP
    left_end = y - GAP                                  # 634

    # ── 右列：空间线 ──
    s.text(rx + BOX_W / 2, 66, "空间线（9.6–9.7）", size=SIZE_TITLE, mono=False,
           fill=COLOR_PRIMARY, weight="bold", anchor="middle")
    s.text(rx + BOX_W / 2, 86, "输入：spot×基因计数矩阵＋空间坐标", size=SIZE_NOTE,
           mono=False, fill=COLOR_MUTED, anchor="middle")
    right = [
        ("① Space Ranger 计数矩阵", "spot 数、每 spot UMI 分布"),
        ("② spot 质控", "低计数 spot 与组织形态对照"),
        ("③ 空间可视化", "表达图案与解剖结构一致"),
        ("④ 区域识别与注释", "注释与 H&E 图互证"),
    ]
    y = 100
    for i, (name, check) in enumerate(right):
        step_box(s, rx, y, name, check)
        if i < len(right) - 1:
            down_arrow(s, rx + BOX_W / 2, y + BOX_H, y + BOX_H + GAP)
        y += BOX_H + GAP
    right_end = y - GAP                                  # 446

    # ── 汇合轨道 → 汇合框 ──
    rail_y = 664
    lcx, rcx = lx + BOX_W / 2, rx + BOX_W / 2
    s.line(lcx, left_end, lcx, rail_y, stroke=COLOR_PRIMARY, sw=1.8)
    s.line(rcx, right_end, rcx, rail_y, stroke=COLOR_PRIMARY, sw=1.8)
    s.line(lcx, rail_y, rcx, rail_y, stroke=COLOR_PRIMARY, sw=1.8)
    mid = (lcx + rcx) / 2
    down_arrow(s, mid, rail_y, 682)
    s.rect(mid - 330, 682, 660, 48, fill=COLOR_FILL, stroke=COLOR_PRIMARY, rx=6)
    s.text(mid, 711, "⑦ 去卷积与参考映射：单细胞参考解释 spot 构成，空间分布印证细胞状态（9.8）",
           size=SIZE_NOTE, mono=False, fill=COLOR_TEXT, anchor="middle")

    # ── 收束：完整案例与误区 ──
    down_arrow(s, mid, 730, 750)
    s.rect(mid - 330, 750, 660, 34, stroke=COLOR_LINE, dash="5,4")
    s.text(mid, 771, "完整案例与检查点清单 · 常见误区（9.8）", size=SIZE_NOTE,
           mono=False, fill=COLOR_TEXT, anchor="middle")

    save("001-ch09-route", s)


if __name__ == "__main__":
    main()
