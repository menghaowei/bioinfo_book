# -*- coding: utf-8 -*-
"""第 11 章三张 SVG 示意图：学习地图、设计矩阵、PCA 原理。

配色与字体沿用 ch04/common.py 的全书统一视觉（指南第 14 节）。
运行：python3 gen_svgs.py
"""

from common import (Svg, COLOR_TEXT, COLOR_MUTED, COLOR_PRIMARY, COLOR_FILL,
                    COLOR_WARN, COLOR_WARN_FILL, COLOR_LINE, SANS, MONO,
                    SIZE_LABEL, SIZE_TITLE, SIZE_NOTE, save)


def learning_map():
    """问题类型 → 方法族 → 数学基础与章节的三列地图。"""
    w, h = 1060, 700
    s = Svg(w, h, "生信分析中的统计问题学习地图",
            "按问题类型组织统计与机器学习方法：左列问题、中列方法、右列数学基础与本书章节")
    rows = [
        ("这批数据长什么样？", "均值 · 方差 · 分位数 · 可视化", "初等统计", "11.2", False),
        ("数据是怎么产生的？", "概率分布：泊松/负二项/正态", "概率论", "11.3", False),
        ("两组之间有没有差异？", "t 检验 · 效应量 · FDR", "数理统计", "11.4", False),
        ("样本之间可以比较吗？", "归一化：CPM/TPM/size factor", "统计前提", "11.5", False),
        ("多个因素怎么分离？", "线性模型 · 设计公式 · 对照水平", "线性代数＋统计", "11.6", False),
        ("样本和基因是什么关系？", "相关 · 聚类 · PCA/t-SNE/UMAP", "线性代数 / 图论", "11.7–11.8", False),
        ("想预测或分类？", "有监督机器学习（分类 · 回归）", "统计学习", "指向进阶资源", True),
    ]
    x1, x2, x3 = 30, 335, 700
    cw1, cw2, cw3 = 285, 345, 325
    y0, rh, gap = 96, 66, 12
    # 列标题
    s.text(x1 + cw1 / 2, 66, "你想回答什么", size=SIZE_TITLE, mono=False,
           weight="bold", anchor="middle", fill=COLOR_PRIMARY)
    s.text(x2 + cw2 / 2, 66, "常用方法", size=SIZE_TITLE, mono=False,
           weight="bold", anchor="middle", fill=COLOR_PRIMARY)
    s.text(x3 + cw3 / 2, 66, "数学基础 · 本书位置", size=SIZE_TITLE, mono=False,
           weight="bold", anchor="middle", fill=COLOR_PRIMARY)
    for i, (q, m, base, pos, beyond) in enumerate(rows):
        y = y0 + i * (rh + gap)
        # 问题框：琥珀色仅用于超出本章范围的最后一行
        qc = COLOR_WARN if beyond else COLOR_PRIMARY
        qf = COLOR_WARN_FILL if beyond else COLOR_FILL
        s.rect(x1, y, cw1, rh, fill=qf, stroke=qc, sw=1.4)
        s.text(x1 + cw1 / 2, y + rh / 2 + 5, q, size=SIZE_LABEL + 1, mono=False,
               anchor="middle", fill=COLOR_TEXT, weight="bold")
        s.arrow(x1 + cw1 + 6, y + rh / 2, x2 - 8, y + rh / 2)
        # 方法框
        s.rect(x2, y, cw2, rh, fill="none", stroke=COLOR_PRIMARY, sw=1.2)
        s.text(x2 + cw2 / 2, y + rh / 2 + 5, m, size=SIZE_LABEL, mono=False,
               anchor="middle", fill=COLOR_TEXT)
        s.arrow(x2 + cw2 + 6, y + rh / 2, x3 - 8, y + rh / 2)
        # 基础框
        s.rect(x3, y, cw3, rh, fill="none", stroke=COLOR_LINE, sw=1.1)
        s.text(x3 + 14, y + rh / 2 - 6, base, size=SIZE_LABEL, mono=False,
               fill=COLOR_TEXT)
        s.text(x3 + 14, y + rh / 2 + 18, pos, size=SIZE_NOTE, mono=False,
               fill=COLOR_MUTED)
    s.text(w / 2, h - 18, "学习顺序自上而下；底行为有监督学习，本章只做定位，深入靠进阶资源。",
           size=SIZE_NOTE, mono=False, anchor="middle", fill=COLOR_MUTED)
    save("fig-11-01-learning-map", s)


def design_matrix():
    """alb ~ tissue 的哑变量展开与系数含义。"""
    w, h = 900, 560
    s = Svg(w, h, "设计公式到模型矩阵的展开",
            "alb ~ tissue 中分类型变量展开为 0/1 哑变量，回归系数对应组均值与均值差")
    # 公式
    s.text(60, 70, "R", size=SIZE_TITLE, mono=True, fill=COLOR_MUTED)
    s.text(110, 70, "fit <- lm(alb ~ tissue, data = d2)", size=SIZE_TITLE,
           mono=True, fill=COLOR_TEXT, weight="bold")
    s.text(110, 98, "设计公式读作：alb 由 tissue 解释", size=SIZE_NOTE,
           mono=False, fill=COLOR_MUTED)
    # 模型矩阵表
    cols = ["样本（前 2+后 2 行）", "(截距)", "tissuePancreas", "alb"]
    data = [
        ("Liver · 样本1", "1", "0", "15.412"),
        ("Liver · 样本2", "1", "0", "15.850"),
        ("……（各 10 行）", "1", "0", "·"),
        ("Pancreas · 样本1", "1", "1", "9.376"),
        ("Pancreas · 样本2", "1", "1", "8.707"),
    ]
    x0, y0 = 60, 130
    cw = [220, 110, 190, 110]
    rh = 42
    # 表头
    cx = x0
    for j, c in enumerate(cols):
        s.rect(cx, y0, cw[j], rh, fill=COLOR_FILL, stroke=COLOR_PRIMARY, sw=1.2)
        s.text(cx + cw[j] / 2, y0 + rh / 2 + 5, c, size=SIZE_LABEL, mono=False,
               anchor="middle", weight="bold", fill=COLOR_TEXT)
        cx += cw[j]
    # 数据行
    for i, row in enumerate(data):
        cx = x0
        yy = y0 + rh * (i + 1)
        for j, v in enumerate(row):
            fill = COLOR_TEXT if j == 0 else COLOR_PRIMARY
            mono = j > 0
            s.rect(cx, yy, cw[j], rh, fill="none", stroke=COLOR_LINE, sw=1.0)
            s.text(cx + cw[j] / 2, yy + rh / 2 + 5, v, size=SIZE_LABEL,
                   mono=mono, anchor="middle", fill=fill)
            cx += cw[j]
    # 右侧系数注解
    ax, ay = 740, 150
    s.rect(ax, ay, 140, 84, fill=COLOR_FILL, stroke=COLOR_PRIMARY, sw=1.4)
    s.text(ax + 70, ay + 30, "(Intercept)", size=SIZE_LABEL, mono=True,
           anchor="middle", weight="bold")
    s.text(ax + 70, ay + 54, "14.909", size=SIZE_LABEL + 2, mono=True,
           anchor="middle", fill=COLOR_PRIMARY, weight="bold")
    s.text(ax + 70, ay + 74, "= Liver 组均值", size=SIZE_NOTE, mono=False,
           anchor="middle", fill=COLOR_MUTED)
    by = ay + 130
    s.rect(ax, by, 140, 84, fill=COLOR_WARN_FILL, stroke=COLOR_WARN, sw=1.4)
    s.text(ax + 70, by + 30, "tissuePancreas", size=SIZE_LABEL, mono=True,
           anchor="middle", weight="bold")
    s.text(ax + 70, by + 54, "-6.503", size=SIZE_LABEL + 2, mono=True,
           anchor="middle", fill=COLOR_WARN, weight="bold")
    s.text(ax + 70, by + 74, "= 均值差（胰 − 肝）", size=SIZE_NOTE, mono=False,
           anchor="middle", fill=COLOR_MUTED)
    # 连线：列 → 系数框
    s.arrow(x0 + cw[0] + cw[1] / 2, y0 + rh * 3 + 8, ax - 6, ay + 42)
    s.arrow(x0 + cw[0] + cw[1] + cw[2] / 2, y0 + rh * 3 + 8, ax - 6, by + 42)
    # 拟合式
    s.text(60, h - 40, "拟合结果：alb = 14.909 − 6.503 × tissuePancreas",
           size=SIZE_TITLE, mono=True, fill=COLOR_TEXT, weight="bold")
    s.text(60, h - 16, "Liver 行哑变量为 0，胰腺行为 1；换对照水平，系数与符号随之改变。",
           size=SIZE_NOTE, mono=False, fill=COLOR_MUTED)
    save("fig-11-04-design-matrix", s)


def pca_principle():
    """两基因散点上的 PC1/PC2 方向与投影。"""
    import math
    w, h = 900, 600
    s = Svg(w, h, "主成分分析的投影直觉",
            "两个基因维度上的散点云，PC1 取投影方差最大的方向，PC2 与之垂直")
    # 坐标轴
    ox, oy, L = 90, 500, 720   # 原点与轴长
    s.arrow(ox, oy, ox + L, oy, stroke=COLOR_LINE, sw=1.2)
    s.arrow(ox, oy, ox, oy - 420, stroke=COLOR_LINE, sw=1.2)
    s.text(ox + L, oy + 22, "基因 A 表达（log2）", size=SIZE_LABEL, mono=False,
           anchor="end", fill=COLOR_MUTED)
    s.text(ox - 10, oy - 420, "基因 B 表达（log2）", size=SIZE_LABEL, mono=False,
           anchor="start", fill=COLOR_MUTED)
    # 散点（手工布置的斜向点云，示意数据）
    pts = [(150, 385), (185, 350), (215, 375), (250, 330), (280, 345),
           (310, 300), (345, 320), (375, 275), (410, 290), (440, 250),
           (470, 265), (505, 225), (535, 240), (565, 200), (600, 215),
           (630, 175)]
    for px, py in pts:
        s.add(f"<circle cx='{px}' cy='{py}' r='6' fill='{COLOR_PRIMARY}' "
              f"opacity='0.75'/>")
    # 质心与主成分方向
    cx0 = sum(p[0] for p in pts) / len(pts)
    cy0 = sum(p[1] for p in pts) / len(pts)
    dx, dy = 1.0, -0.75                       # PC1 斜率方向
    n = math.hypot(dx, dy)
    ux, uy = dx / n, dy / n
    r1 = 330
    s.arrow(cx0 - ux * r1, cy0 - uy * r1, cx0 + ux * r1, cy0 + uy * r1,
            stroke=COLOR_PRIMARY, sw=3.0)
    s.text(cx0 + ux * r1 + 12, cy0 + uy * r1 - 6, "PC1（方差最大）",
           size=SIZE_TITLE, mono=False, fill=COLOR_PRIMARY, weight="bold")
    vx, vy = -uy, ux                          # 垂直方向
    r2 = 120
    s.arrow(cx0 - vx * r2, cy0 - vy * r2, cx0 + vx * r2, cy0 + vy * r2,
            stroke=COLOR_WARN, sw=2.2)
    s.text(cx0 + vx * r2 + 10, cy0 + vy * r2 + 18, "PC2（垂直于 PC1）",
           size=SIZE_LABEL, mono=False, fill=COLOR_WARN, weight="bold")
    # 投影示意：一个点到 PC1 的垂线
    ex, ey = pts[11]                           # (505,225)
    t = (ex - cx0) * ux + (ey - cy0) * uy
    qx, qy = cx0 + t * ux, cy0 + t * uy
    s.line(ex, ey, qx, qy, stroke=COLOR_WARN, sw=1.4, dash="5,4")
    s.add(f"<circle cx='{qx:.0f}' cy='{qy:.0f}' r='7' fill='none' "
          f"stroke='{COLOR_WARN}' stroke-width='2'/>")
    s.text(ex + 12, ey - 10, "样本", size=SIZE_NOTE, mono=False, fill=COLOR_TEXT)
    s.text(qx + 12, qy + 22, "它在 PC1 上的投影（得分）", size=SIZE_NOTE,
           mono=False, fill=COLOR_MUTED)
    s.text(ox, h - 16, "实心点为示意样本；虚线是样本到 PC1 的垂线，所有点的投影构成主成分得分。",
           size=SIZE_NOTE, mono=False, fill=COLOR_MUTED)
    save("fig-11-05-pca-principle", s)


if __name__ == "__main__":
    learning_map()
    design_matrix()
    pca_principle()
