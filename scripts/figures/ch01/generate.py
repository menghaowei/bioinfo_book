#!/usr/bin/env python3
"""Chapter 1 conceptual figures. Run with Python 3; no external dependencies.

These drawings illustrate learning and research relationships, not measured data.
Colors follow AUTHORING_GUIDE section 14. Text remains editable in the SVGs.
"""
from pathlib import Path
from html import escape

OUT = Path(__file__).resolve().parents[3] / 'assets/01-ai-era-introduction'
GREEN, LIGHT, AMBER, CREAM = '#186254', '#e8f4f1', '#b45309', '#fdf3e3'
INK, GREY, LINE, BG = '#333333', '#6b7280', '#9ca3af', '#fcfcf9'
FONT = "'PingFang SC','Hiragino Sans GB','Microsoft YaHei','Noto Sans CJK SC',sans-serif"


class Figure:
    def __init__(self, height, title, description):
        self.height = height
        self.parts = [f'''<svg xmlns="http://www.w3.org/2000/svg" width="640" height="{height}" viewBox="0 0 640 {height}" role="img" aria-labelledby="title description">
<title id="title">{escape(title)}</title><desc id="description">{escape(description)}</desc>
<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M0 1 L9 5 L0 9" fill="none" stroke="{GREEN}" stroke-width="1.6"/></marker>
<marker id="return" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto"><path d="M0 1 L9 5 L0 9" fill="none" stroke="{AMBER}" stroke-width="1.6"/></marker></defs>
<rect width="640" height="{height}" fill="{BG}"/>
<g stroke-linecap="round" stroke-linejoin="round">''']

    def rect(self, x, y, w, h, fill=LIGHT, stroke='none', radius=14, sw=2):
        self.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')

    def text(self, x, y, value, size=24, color=INK, weight=400, anchor='start'):
        self.parts.append(f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="{size}" fill="{color}" font-weight="{weight}" text-anchor="{anchor}">{escape(value)}</text>')

    def path(self, d, color=GREEN, width=2.5, arrow=False, dash=False, fill='none'):
        end = f' marker-end="url(#{"return" if color == AMBER else "arrow"})"' if arrow else ''
        dash_attr = ' stroke-dasharray="7 7"' if dash else ''
        self.parts.append(f'<path d="{d}" fill="{fill}" stroke="{color}" stroke-width="{width}"{end}{dash_attr}/>')

    def line(self, x1, y1, x2, y2, **kwargs):
        self.path(f'M{x1} {y1} L{x2} {y2}', **kwargs)

    def circle(self, x, y, r, fill=LIGHT, stroke=GREEN, sw=2):
        self.parts.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')

    def save(self, name):
        OUT.mkdir(parents=True, exist_ok=True)
        path = OUT / name
        path.write_text('\n'.join(self.parts) + '\n</g></svg>\n', encoding='utf-8')
        print(path.name)


def learning():
    f = Figure(804, '围绕问题组织学习',
                '明确问题、查找相关知识、尝试实践、检查结果。AI 在各环节协助解释、实现和整理，发现知识缺口后再回查相关知识。箭头表示学习步骤和回查，不表示自动得到可靠结论。')
    steps = [
        ('明确要回答的问题', '样本是什么？希望比较什么？', 'AI 协助：梳理问题和背景'),
        ('找到需要的知识', '生物学 · 实验设计 · 统计 · 编程', 'AI 协助：解释概念，整理线索'),
        ('把知识用到当前任务中', '用小数据尝试，观察输入与输出', 'AI 协助：实现步骤，排查报错'),
        ('检查结果，回看依据', '结果能回答最初的问题吗？', 'AI 协助整理；结合原始材料核对'),
    ]
    for i, (title, detail, help_text) in enumerate(steps):
        y = 24 + i * 180
        f.rect(64, y, 548, 144)
        f.circle(94, y + 35, 18, fill=GREEN, stroke='none')
        f.text(94, y + 44, str(i + 1), 25, 'white', 600, 'middle')
        f.text(126, y + 44, title, 27, GREEN, 600)
        f.text(88, y + 84, detail, 24)
        f.text(88, y + 120, help_text, 23, GREEN)
        if i < 3:
            f.line(336, y + 151, 336, y + 169, arrow=True)
    f.path('M64 636 H30 V276 H55', AMBER, 2.5, True, True)
    f.line(102, 753, 148, 753, color=AMBER, dash=True, arrow=True)
    f.text(168, 762, '发现缺口，再回到相关知识中查找', 24, AMBER)
    f.save('001-learning-around-questions.svg')


def scene(f, number, x, y):
    """Small, editable illustrations of work objects, without measured values."""
    if number == 0:  # papers and a question
        f.rect(x + 6, y + 8, 90, 102, 'white', GREEN, 6)
        f.rect(x + 20, y, 90, 102, BG, GREEN, 6)
        for offset, length in [(20, 57), (34, 64), (66, 42), (80, 60)]:
            f.line(x + 32, y + offset, x + 32 + length, y + offset, color=LINE, width=2)
        f.circle(x + 105, y + 47, 28, CREAM, AMBER)
        f.text(x + 105, y + 58, '?', 34, AMBER, 600, 'middle')
    elif number == 1:  # three tubes and a rack
        for offset in [12, 51, 90]:
            f.rect(x + offset, y + 16, 24, 80, 'white', GREEN, 11)
            f.rect(x + offset + 4, y + 54, 16, 38, LIGHT, 'none', 7)
            f.line(x + offset - 2, y + 17, x + offset + 26, y + 17, width=4)
        f.path(f'M{x + 3} {y + 75} H{x + 130} V{y + 108} H{x + 3} Z')
        f.line(x + 9, y + 117, x + 126, y + 117)
    elif number == 2:  # a computer and data table
        f.rect(x + 2, y + 9, 126, 83, 'white', GREEN, 7)
        f.path(f'M{x - 7} {y + 103} H{x + 137} L{x + 124} {y + 114} H{x + 6} Z', fill=LIGHT)
        f.path(f'M{x + 24} {y + 37} l-10 10 10 10 M{x + 42} {y + 35} l-9 24 M{x + 53} {y + 37} l10 10 -10 10')
        f.rect(x + 79, y + 26, 34, 45, LIGHT, GREEN, 0, 1.5)
        for dy in [41, 56]:
            f.line(x + 79, y + dy, x + 113, y + dy, width=1.3)
        f.line(x + 96, y + 26, x + 96, y + 71, width=1.3)
    elif number == 3:  # plot and a microscopy-like image panel
        f.rect(x, y + 8, 88, 88, 'white', GREEN, 5)
        f.path(f'M{x + 16} {y + 23} V{y + 79} H{x + 75}', width=2)
        for dx, dy in [(28, 55), (38, 42), (53, 51), (67, 32)]:
            f.circle(x + dx, y + dy, 3.5, GREEN, 'none')
        f.rect(x + 61, y + 48, 77, 63, LIGHT, GREEN, 5)
        for dx, dy in [(81, 67), (114, 75), (94, 92)]:
            f.circle(x + dx, y + dy, 8, 'white', GREEN, 1.5)
            f.circle(x + dx + 1, y + dy, 2.5, GREEN, 'none')
        f.line(x + 112, y + 102, x + 129, y + 102, width=3)
    elif number == 4:  # manuscript layout
        f.rect(x + 18, y, 98, 118, 'white', GREEN, 5)
        f.line(x + 34, y + 18, x + 98, y + 18, width=4)
        for dx in [34, 72]:
            for dy in [33, 44, 55]:
                f.line(x + dx, y + dy, x + dx + 27, y + dy, color=LINE, width=2)
        f.rect(x + 33, y + 70, 29, 30, LIGHT, GREEN, 2, 1.5)
        f.rect(x + 71, y + 70, 29, 30, LIGHT, GREEN, 2, 1.5)
    else:  # review comments
        f.rect(x + 8, y + 3, 90, 109, 'white', GREEN, 5)
        for dy in [24, 43, 62, 82]:
            f.line(x + 24, y + dy, x + 80, y + dy, color=LINE, width=2)
        f.rect(x + 67, y + 26, 67, 52, CREAM, AMBER, 9)
        f.path(f'M{x + 83} {y + 78} L{x + 75} {y + 91} L{x + 103} {y + 78}', AMBER)
        f.line(x + 82, y + 42, x + 120, y + 42, color=AMBER, width=2)
        f.line(x + 82, y + 56, x + 110, y + 56, color=AMBER, width=2)


def paper():
    f = Figure(1184, '一篇论文联系起多种能力',
                '用文献、实验样本、电脑、图像、论文与审稿六个场景表示研究工作；各环节对应不同知识。虚线表示根据问题回到实验或分析，研究通常需要多人协作。')
    stages = [
        ('文献与研究问题', '领域背景 · 证据与疑问', '从已有研究中确定问题'),
        ('设计并完成实验', '测量方法 · 对照 · 重复', '保留样本信息与实验记录'),
        ('数据整理、编程与分析', '文件管理 · 编程 · 统计', '核对输入、方法与结果'),
        ('绘图与实验图片整理', '图形表达 · 图像信息', '让图忠实表达数据'),
        ('写作、排版与润色', '论述逻辑 · 准确表达', '对应正文、图表和证据'),
        ('投稿、审稿与修改', '回应问题 · 补充证据', '必要时补实验或重新分析'),
    ]
    for i, (title, knowledge, action) in enumerate(stages):
        y = 18 + i * 177
        f.rect(25, y, 555, 153, fill='white', stroke='#d4e3dc')
        scene(f, i, 47, y + 18)
        f.text(215, y + 38, title, 26, GREEN, 600)
        f.rect(205, y + 54, 358, 41, LIGHT, radius=7)
        f.text(218, y + 82, knowledge, 24)
        f.text(215, y + 130, action, 23, GREY)
        if i < 5:
            f.line(110, y + 159, 110, y + 170, arrow=True)
    f.path('M580 979 H612 V270 H588', AMBER, 2.5, True, True)
    f.path('M612 447 H588', AMBER, 2.5, True, True)
    f.line(45, 1110, 91, 1110, color=AMBER, dash=True, arrow=True)
    f.text(110, 1119, '根据问题回查，补实验或重新分析', 24, AMBER)
    f.text(320, 1164, '这些工作通常由不同的人协作完成', 24, GREEN, anchor='middle')
    f.save('002-paper-and-knowledge.svg')


def sample(f, x, y, label):
    f.circle(x, y, 24, 'white')
    f.text(x, y + 9, label, 27, GREEN, 600, 'middle')


def transfer():
    f = Figure(1102, '把项目经验用于新问题',
                '项目 A 的两组为不同个体，项目 B 比较同一个体处理前后。学习者回顾问题、数据、方法与结论的联系，可以沿用明确问题、整理信息和检查结果的做法；新项目必须重新检查样本对应关系并选择方法。字母只示意个体身份。')
    f.rect(24, 20, 592, 238)
    f.text(48, 60, '项目 A：比较两组不同个体', 28, GREEN, 600)
    for y, title, labels in [(119, '组一', 'ABC'), (198, '组二', 'DEF')]:
        f.text(80, y + 8, title, 26)
        for x, label in zip([287, 405, 523], labels):
            sample(f, x, y, label)
    f.line(320, 271, 320, 304, arrow=True)
    f.rect(24, 321, 592, 263, 'white', GREEN)
    f.text(320, 361, '回顾项目，逐渐理清知识之间的联系', 26, GREEN, 600, 'middle')
    for i, label in enumerate(['问题', '数据', '方法', '结论']):
        x = 104 + i * 144
        f.circle(x, 430, 39)
        f.text(x, 440, label, 27, GREEN, 600, 'middle')
        if i < 3:
            f.line(x + 47, 430, x + 96, 430, arrow=True)
    f.text(320, 509, '可以沿用的思考方法', 25, GREEN, 600, 'middle')
    f.text(320, 553, '明确问题 · 整理信息 · 检查结果', 25, INK, anchor='middle')
    f.line(320, 598, 320, 631, arrow=True)
    f.rect(24, 648, 592, 313)
    f.text(48, 690, '项目 B：比较同一个体处理前后', 28, GREEN, 600)
    f.text(270, 738, '处理前', 24, INK, anchor='middle')
    f.text(500, 738, '处理后', 24, INK, anchor='middle')
    for y, label in zip([784, 854, 924], 'GHI'):
        f.text(64, y + 8, '个体 ' + label, 24)
        sample(f, 270, y, label)
        sample(f, 500, y, label)
        f.line(308, y, 461, y, width=2)
    f.rect(24, 984, 592, 96, CREAM, AMBER)
    f.text(48, 1024, '需要重查：样本的对应关系', 27, AMBER, 600)
    f.text(48, 1062, '分析方法也要据此重新选择', 25)
    f.save('003-framework-transfer.svg')


if __name__ == '__main__':
    learning()
    paper()
    transfer()
