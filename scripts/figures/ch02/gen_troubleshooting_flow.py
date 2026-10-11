"""第二章「排错的基本思路」流程图生成脚本。

视觉规范遵循 AUTHORING_GUIDE 第 14 节（统一色表、SVG 固有尺寸+viewBox、title/desc、
几何自检），复用 scripts/figures/ch04/common.py 的 Svg 类与常量，输出到
assets/02-computing-and-programming/svg/。

教学目的：配合 2.8「排错的基本思路」正文，给出四步递进排查的全景——
每一步都可能直接解决问题（已解决出口），未解决才进入下一步，最终以记录收尾。
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "ch04"))
from common import (  # noqa: E402
    Svg,
    COLOR_TEXT, COLOR_MUTED, COLOR_PRIMARY, COLOR_FILL,
    COLOR_WARN, COLOR_LINE,
    SIZE_NOTE, SIZE_TITLE,
)

OUT = Path(__file__).resolve().parents[3] / "assets" / "02-computing-and-programming" / "svg"

W, H = 560, 700
BOX_X, BOX_W, BOX_H = 60, 300, 86
STEPS = [
    ("① 读报错", ["找 error 而不是 warning", "最后几行通常是关键"]),
    ("② 最小复现", ["出错一步单独拿出来", "用最小输入重跑一遍"]),
    ("③ 查输入", ["head 看格式，wc -l 数行数", "与上一步输出对照"]),
    ("④ 问对问题", ["带报错原文＋执行的命令", "以及期望与实际结果"]),
]
GAP = 34          # 主链箭头长度（含标签）
COLLECT_X = 430   # 「已解决」汇流线 x
REC_Y, REC_H = 592, 64

svg = Svg(W, H, "排错的基本流程", "四步递进排查：读报错、最小复现、查输入、问对问题；"
         "任一步解决即从右侧出口收尾记录，未解决顺主链进入下一步。")

# 标题与副题
svg.text(W / 2, 34, "排错的基本流程", size=SIZE_TITLE + 2, mono=False,
         fill=COLOR_TEXT, weight="650", anchor="middle")
svg.text(W / 2, 54, "四步递进，解决即收尾", size=SIZE_NOTE, mono=False,
         fill=COLOR_MUTED, anchor="middle")

# 竖直线栅格（防止绘制错位）：主链中心 x
cx = BOX_X + BOX_W / 2

# 状态框
boxes = []
y = 90
for title, details in STEPS:
    svg.rect(BOX_X, y, BOX_W, BOX_H, fill=COLOR_FILL, stroke=COLOR_PRIMARY, sw=1.6, rx=6)
    svg.text(BOX_X + 16, y + 28, title, size=SIZE_TITLE, mono=False,
             fill=COLOR_PRIMARY, weight="650")
    for i, d in enumerate(details):
        svg.text(BOX_X + 16, y + 50 + i * 18, d, size=SIZE_NOTE, mono=False, fill=COLOR_TEXT)
    boxes.append((y, y + BOX_H))
    y += BOX_H + GAP

# 主链箭头（未解决→下一步 / 最后一步→记录收尾）
for i, (top, bottom) in enumerate(boxes):
    if i + 1 < len(boxes):
        y2 = boxes[i + 1][0]
        label = "未解决"
    else:
        y2 = REC_Y
        label = "验证后"
    svg.arrow(cx, bottom, cx, y2 - 2, stroke=COLOR_PRIMARY, sw=1.8)
    svg.text(cx + 10, (bottom + y2) / 2 + 4, label, size=SIZE_NOTE,
             mono=False, fill=COLOR_MUTED)

# 「已解决」出口：右侧灰线汇入 COLLECT_X 竖线，最终一支箭头进入记录框
for top, bottom in boxes:
    mid = (top + bottom) / 2
    svg.line(BOX_X + BOX_W, mid, COLLECT_X, mid, stroke=COLOR_LINE, sw=1.4)
    svg.text(BOX_X + BOX_W + 8, mid - 6, "已解决", size=SIZE_NOTE,
             mono=False, fill=COLOR_MUTED)
svg.line(COLLECT_X, (boxes[0][0] + boxes[0][1]) / 2, COLLECT_X, REC_Y - 2,
         stroke=COLOR_LINE, sw=1.4)
svg.arrow(COLLECT_X, REC_Y - 30, COLLECT_X, REC_Y - 2, stroke=COLOR_LINE, sw=1.4)

# 记录收尾框（深绿实底白字）
svg.rect(BOX_X, REC_Y, 370, REC_H, fill=COLOR_PRIMARY, stroke=COLOR_PRIMARY, sw=1.6, rx=6)
svg.text(BOX_X + 185, REC_Y + 27, "记录收尾", size=SIZE_TITLE, mono=False,
         fill="#ffffff", weight="650", anchor="middle")
svg.text(BOX_X + 185, REC_Y + 48, "一行记下：报错、原因、改法", size=SIZE_NOTE,
         mono=False, fill="#ffffff", anchor="middle")

# 底部琥珀注记（问人问 AI 的共同提醒）
svg.text(W / 2, 684, "问人问 AI 时：AI 也会自信地猜——每条建议验证后再前进",
         size=SIZE_NOTE, mono=False, fill=COLOR_WARN, anchor="middle")

# ---- 几何自检：文字估宽不越框、框间不重叠、元素不出画布 ----
def est_w(s, size):
    return sum(size if ord(c) > 0x2E7F else size * 0.55 for c in s)

problems = []
for title, details in STEPS:
    for t in [title, *details]:
        if BOX_X + 16 + est_w(t, SIZE_TITLE if t is title else SIZE_NOTE) > BOX_X + BOX_W - 8:
            problems.append(f"文字越框: {t}")
    if max(est_w(d, SIZE_NOTE) for d in details) > BOX_W - 32:
        problems.append(f"详情过宽: {title}")
for i in range(len(boxes) - 1):
    if boxes[i][1] >= boxes[i + 1][0]:
        problems.append(f"框重叠: {i}")
if BOX_X + 370 > W or REC_Y + REC_H > H:
    problems.append("记录框出界")
assert not problems, problems

OUT.mkdir(parents=True, exist_ok=True)
(OUT / "troubleshooting-flow.svg").write_text(svg.render(), encoding="utf-8")
print(f"written troubleshooting-flow.svg ({W}x{H})，几何自检通过")
