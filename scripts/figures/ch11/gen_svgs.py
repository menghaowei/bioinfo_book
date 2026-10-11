# -*- coding: utf-8 -*-
"""第 11 章三张 SVG 示意图：学习地图、设计矩阵、PCA 原理。

配色与字体沿用 ch04/common.py 的全书统一视觉（指南第 14 节）。
画布按网页正文栏宽（约 760px）设计，字号即页面实际阅读字号（2026-10-11 反馈修订）。
运行：python3 gen_svgs.py
"""

from common import (Svg, COLOR_TEXT, COLOR_MUTED, COLOR_PRIMARY, COLOR_FILL,
                    COLOR_WARN, COLOR_WARN_FILL, COLOR_LINE, SANS, MONO,
                    SIZE_LABEL, SIZE_TITLE, SIZE_NOTE, save)

# 反馈修订后的统一字号（页面 1:1 显示，等效正文阅读字号）
SZ_Q = 15      # 问题列（粗体）
SZ_M = 14      # 方法列
SZ_B = 13      # 基础列第一行
SZ_P = 12      # 章节小字
SZ_HEAD = 16   # 列标题
SZ_NOTE2 = 12.5
SZ_TAB = 14    # 表格
SZ_FORMULA = 15


def learning_map():
    """问题类型 → 方法族 → 数学基础与章节的三列地图（紧凑版，760×486）。"""
    w = 760
    rows = [
        ("这批数据长什么样？", "均值 · 方差 · 分位数 · 可视化", "初等统计", "11.2", False),
        ("数据是怎么产生的？", "概率分布：泊松/负二项/正态", "概率论", "11.3", False),
        ("两组之间有没有差异？", "t 检验 · 效应量 · FDR", "数理统计", "11.4", False),
        ("样本之间可以比较吗？", "归一化：CPM/TPM/size factor", "统计前提", "11.5", False),
        ("多个因素怎么分离？", "线性模型 · 设计公式 · 对照水平", "线性代数＋统计", "11.6", False),
        ("样本和基因是什么关系？", "相关 · 聚类 · PCA/t-SNE/UMAP", "线性代数 / 图论", "11.7–11.8", False),
        ("想预测或分类？", "有监督机器学习（分类 · 回归）", "统计学习", "指向进阶资源", True),
    ]
    x1, cw1 = 8, 210
    x2, cw2 = 242, 268
    x3, cw3 = 536, 216
    y0, rh, gap = 46, 46, 8
    h = y0 + len(rows) * (rh + gap) - gap + 8 + 22   # 行区 + 注释行
    s = Svg(w, h, "生信分析中的统计问题学习地图",
            "按问题类型组织统计与机器学习方法：左列问题、中列方法、右列数学基础与本书章节")
    # 列标题（紧贴首行，不留整段空白）
    for x, cw, t in ((x1, cw1, "你想回答什么"), (x2, cw2, "常用方法"),
                     (x3, cw3, "数学基础 · 本书位置")):
        s.text(x + cw / 2, 30, t, size=SZ_HEAD, mono=False,
               weight="bold", anchor="middle", fill=COLOR_PRIMARY)
    for i, (q, m, base, pos, beyond) in enumerate(rows):
        y = y0 + i * (rh + gap)
        mid = y + rh / 2
        qc = COLOR_WARN if beyond else COLOR_PRIMARY
        qf = COLOR_WARN_FILL if beyond else COLOR_FILL
        s.rect(x1, y, cw1, rh, fill=qf, stroke=qc, sw=1.4)
        s.text(x1 + cw1 / 2, mid + 5, q, size=SZ_Q, mono=False,
               anchor="middle", fill=COLOR_TEXT, weight="bold")
        s.arrow(x1 + cw1 + 5, mid, x2 - 5, mid)
        s.rect(x2, y, cw2, rh, fill="none", stroke=COLOR_PRIMARY, sw=1.2)
        s.text(x2 + cw2 / 2, mid + 5, m, size=SZ_M, mono=False,
               anchor="middle", fill=COLOR_TEXT)
        s.arrow(x2 + cw2 + 5, mid, x3 - 5, mid)
        s.rect(x3, y, cw3, rh, fill="none", stroke=COLOR_LINE, sw=1.1)
        s.text(x3 + 14, y + 19, base, size=SZ_B, mono=False, fill=COLOR_TEXT)
        s.text(x3 + 14, y + 37, pos, size=SZ_P, mono=False, fill=COLOR_MUTED)
    s.text(w / 2, h - 8, "学习顺序自上而下；底行为有监督学习，本章只做定位，深入靠进阶资源。",
           size=SZ_NOTE2, mono=False, anchor="middle", fill=COLOR_MUTED)
    save("fig-11-01-learning-map", s)


def design_matrix():
    """alb ~ tissue 的哑变量展开与系数含义（竖排注解紧凑版，760×442）。"""
    w = 760
    s = Svg(w, 442, "设计公式到模型矩阵的展开",
            "alb ~ tissue 中分类型变量展开为 0/1 哑变量，回归系数对应组均值与均值差")
    # 顶部公式
    s.text(w / 2, 26, "fit <- lm(alb ~ tissue, data = d2)", size=SZ_FORMULA,
           mono=True, fill=COLOR_TEXT, weight="bold", anchor="middle")
    s.text(w / 2, 45, "设计公式读作：alb 由 tissue 解释（R 把分类型变量展开成 0/1 哑变量列）",
           size=SZ_NOTE2, mono=False, fill=COLOR_MUTED, anchor="middle")
    # 模型矩阵表（居中）
    cols = ["样本（前 2 + 后 2 行）", "(截距)", "tissuePancreas", "alb"]
    data = [
        ("Liver · 样本1", "1", "0", "15.412"),
        ("Liver · 样本2", "1", "0", "15.850"),
        ("……（各 10 行）", "1", "0", "·"),
        ("Pancreas · 样本1", "1", "1", "9.376"),
        ("Pancreas · 样本2", "1", "1", "8.707"),
    ]
    cw = [218, 84, 158, 100]
    tw = sum(cw)
    x0 = (w - tw) / 2
    y0, rh = 58, 36
    cx_list = []
    cx = x0
    for c in cw:
        cx_list.append((cx, c))
        cx += c
    for (cxa, cwb), c in zip(cx_list, cols):
        s.rect(cxa, y0, cwb, rh, fill=COLOR_FILL, stroke=COLOR_PRIMARY, sw=1.2)
        s.text(cxa + cwb / 2, y0 + rh / 2 + 5, c, size=SZ_TAB, mono=False,
               anchor="middle", weight="bold", fill=COLOR_TEXT)
    for i, row in enumerate(data):
        yy = y0 + rh * (i + 1)
        for (cxa, cwb), v in zip(cx_list, row):
            s.rect(cxa, yy, cwb, rh, fill="none", stroke=COLOR_LINE, sw=1.0)
            s.text(cxa + cwb / 2, yy + rh / 2 + 5, v, size=SZ_TAB,
                   mono=(cx_list.index((cxa, cwb)) > 0), anchor="middle",
                   fill=COLOR_TEXT if cx_list.index((cxa, cwb)) == 0 else COLOR_PRIMARY)
    y_tab_end = y0 + rh * (len(data) + 1)
    # 系数注解框：表格正下方两格并排，连线指向对应列
    bw, bh, bgap = 350, 62, 24
    bx1 = x0 + 12
    bx2 = bx1 + bw + bgap
    by = y_tab_end + 26
    # 连线：截距列中点 → 左框；tissuePancreas 列中点 → 右框
    ax1 = cx_list[1][0] + cx_list[1][1] / 2
    ax2 = cx_list[2][0] + cx_list[2][1] / 2
    s.arrow(ax1, y_tab_end + 2, bx1 + 70, by - 2)
    s.arrow(ax2, y_tab_end + 2, bx2 + 90, by - 2)
    s.rect(bx1, by, bw, bh, fill=COLOR_FILL, stroke=COLOR_PRIMARY, sw=1.4)
    s.text(bx1 + bw / 2, by + 24, "(Intercept) = 14.909", size=SZ_TAB, mono=True,
           anchor="middle", weight="bold")
    s.text(bx1 + bw / 2, by + 46, "Liver 组均值（首个水平当截距）", size=SZ_P,
           mono=False, anchor="middle", fill=COLOR_MUTED)
    s.rect(bx2, by, bw, bh, fill=COLOR_WARN_FILL, stroke=COLOR_WARN, sw=1.4)
    s.text(bx2 + bw / 2, by + 24, "tissuePancreas = −6.503", size=SZ_TAB, mono=True,
           anchor="middle", weight="bold")
    s.text(bx2 + bw / 2, by + 46, "均值差（胰 − 肝），即 log2FC 方向", size=SZ_P,
           mono=False, anchor="middle", fill=COLOR_MUTED)
    # 底部拟合式
    s.text(w / 2, by + bh + 30, "拟合结果：alb = 14.909 − 6.503 × tissuePancreas",
           size=SZ_FORMULA, mono=True, fill=COLOR_TEXT, weight="bold", anchor="middle")
    s.text(w / 2, by + bh + 50, "Liver 行哑变量为 0，胰腺行为 1；换对照水平，系数与符号随之改变。",
           size=SZ_NOTE2, mono=False, fill=COLOR_MUTED, anchor="middle")
    save("fig-11-04-design-matrix", s)


def pca_principle():
    """两基因散点上的 PC1/PC2 方向与投影（紧凑版，760×540）。"""
    import math
    w, h = 760, 540
    s = Svg(w, h, "主成分分析的投影直觉",
            "两个基因维度上的散点云，PC1 取投影方差最大的方向，PC2 与之垂直")
    ox, oy, L = 66, 468, 660
    s.arrow(ox, oy, ox + L, oy, stroke=COLOR_LINE, sw=1.2)
    s.arrow(ox, oy, ox, oy - 380, stroke=COLOR_LINE, sw=1.2)
    s.text(ox + L, oy + 20, "基因 A 表达（log2）", size=SZ_M, mono=False,
           anchor="end", fill=COLOR_MUTED)
    s.text(ox - 8, oy - 380, "基因 B 表达（log2）", size=SZ_M, mono=False,
           anchor="start", fill=COLOR_MUTED)
    pts = [(128, 352), (156, 322), (182, 342), (212, 304), (238, 318),
           (264, 278), (292, 296), (318, 256), (346, 270), (372, 234),
           (398, 248), (424, 210), (450, 224), (476, 188), (502, 202),
           (528, 164)]
    for px, py in pts:
        s.add(f"<circle cx='{px}' cy='{py}' r='6' fill='{COLOR_PRIMARY}' "
              f"opacity='0.75'/>")
    cx0 = sum(p[0] for p in pts) / len(pts)
    cy0 = sum(p[1] for p in pts) / len(pts)
    dx, dy = 1.0, -0.75
    n = math.hypot(dx, dy)
    ux, uy = dx / n, dy / n
    r1 = 300
    s.arrow(cx0 - ux * r1, cy0 - uy * r1, cx0 + ux * r1, cy0 + uy * r1,
            stroke=COLOR_PRIMARY, sw=3.0)
    s.text(cx0 + ux * r1 + 8, cy0 + uy * r1 - 4, "PC1（方差最大）",
           size=SZ_HEAD, mono=False, fill=COLOR_PRIMARY, weight="bold")
    vx, vy = -uy, ux
    r2 = 108
    s.arrow(cx0 - vx * r2, cy0 - vy * r2, cx0 + vx * r2, cy0 + vy * r2,
            stroke=COLOR_WARN, sw=2.2)
    s.text(cx0 + vx * r2 + 8, cy0 + vy * r2 + 16, "PC2（垂直于 PC1）",
           size=SZ_M, mono=False, fill=COLOR_WARN, weight="bold")
    ex, ey = pts[11]
    t = (ex - cx0) * ux + (ey - cy0) * uy
    qx, qy = cx0 + t * ux, cy0 + t * uy
    s.line(ex, ey, qx, qy, stroke=COLOR_WARN, sw=1.4, dash="5,4")
    s.add(f"<circle cx='{qx:.0f}' cy='{qy:.0f}' r='7' fill='none' "
          f"stroke='{COLOR_WARN}' stroke-width='2'/>")
    s.text(ex + 10, ey - 8, "样本", size=SZ_P, mono=False, fill=COLOR_TEXT)
    s.text(qx + 10, qy + 20, "它在 PC1 上的投影（得分）", size=SZ_P,
           mono=False, fill=COLOR_MUTED)
    s.text(ox, h - 10, "实心点为示意样本；虚线是样本到 PC1 的垂线，所有点的投影构成主成分得分。",
           size=SZ_NOTE2, mono=False, fill=COLOR_MUTED)
    save("fig-11-05-pca-principle", s)


if __name__ == "__main__":
    learning_map()
    design_matrix()
    pca_principle()
