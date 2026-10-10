"""第6章示意图 SVG 生成的共享样式与工具。

沿用 scripts/figures/ch04/common.py 的全书统一视觉（指南第 14 节）：
中文字体栈、等宽字体、深绿主色、浅绿填充、琥珀警示。
"""

import math
from xml.sax.saxutils import escape

MONO = "ui-monospace, 'SFMono-Regular', Menlo, Consolas, 'Liberation Mono', monospace"
SANS = "'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', 'Noto Sans CJK SC', sans-serif"

COLOR_TEXT = "#333333"
COLOR_MUTED = "#6b7280"
COLOR_PRIMARY = "#186254"
COLOR_FILL = "#e8f4f1"
COLOR_WARN = "#b45309"
COLOR_WARN_FILL = "#fdf3e3"
COLOR_LINE = "#9ca3af"
COLOR_PAGE = "#fcfcf9"

SIZE_LABEL = 13
SIZE_TITLE = 15
SIZE_NOTE = 12


class Svg:
    def __init__(self, width, height, title, desc):
        self.w, self.h, self.title, self.desc = width, height, title, desc
        self.parts = []

    def add(self, s):
        self.parts.append(s)

    def text(self, x, y, s, *, size=SIZE_LABEL, mono=False, fill=COLOR_TEXT,
             weight="normal", anchor="start"):
        fam = MONO if mono else SANS
        self.add(f"<text x='{x}' y='{y}' font-family=\"{fam}\" font-size='{size}' "
                 f"fill='{fill}' font-weight='{weight}' text-anchor='{anchor}'>"
                 f"{escape(s)}</text>")

    def rect(self, x, y, w, h, *, fill="none", stroke=COLOR_PRIMARY, sw=1.2, rx=4, dash=None):
        d = f" stroke-dasharray='{dash}'" if dash else ""
        self.add(f"<rect x='{x}' y='{y}' width='{w}' height='{h}' rx='{rx}' "
                 f"fill='{fill}' stroke='{stroke}' stroke-width='{sw}'{d}/>")

    def line(self, x1, y1, x2, y2, *, stroke=COLOR_LINE, sw=1.2, dash=None):
        d = f" stroke-dasharray='{dash}'" if dash else ""
        self.add(f"<line x1='{x1}' y1='{y1}' x2='{x2}' y2='{y2}' "
                 f"stroke='{stroke}' stroke-width='{sw}'{d}/>")

    def arrow(self, x1, y1, x2, y2, *, stroke=COLOR_PRIMARY, sw=1.6):
        self.line(x1, y1, x2, y2, stroke=stroke, sw=sw)
        ang = math.atan2(y2 - y1, x2 - x1)
        L, A = 8, 0.45
        for da in (A, -A):
            bx = x2 - L * math.cos(ang + da)
            by = y2 - L * math.sin(ang + da)
            self.add(f"<line x1='{x2:.1f}' y1='{y2:.1f}' x2='{bx:.1f}' y2='{by:.1f}' "
                     f"stroke='{stroke}' stroke-width='{sw}'/>")

    def box(self, cx, cy, w, h, label, *, sub=None, fill="none", stroke=COLOR_PRIMARY,
            lw=SIZE_LABEL, dash=None):
        """以中心坐标放置流程框：主标签 + 可选第二行说明。"""
        self.rect(cx - w / 2, cy - h / 2, w, h, fill=fill, stroke=stroke, rx=6, dash=dash)
        if sub:
            self.text(cx, cy - 3, label, size=lw, anchor="middle", weight="bold")
            self.text(cx, cy + 15, sub, size=SIZE_NOTE, fill=COLOR_MUTED, anchor="middle")
        else:
            self.text(cx, cy + 4.5, label, size=lw, anchor="middle", weight="bold")

    def circle(self, cx, cy, r, *, fill="none", stroke=COLOR_LINE, sw=1.2):
        self.add(f"<circle cx='{cx}' cy='{cy}' r='{r}' fill='{fill}' "
                 f"stroke='{stroke}' stroke-width='{sw}'/>")

    def path(self, d, *, fill="none", stroke=COLOR_PRIMARY, sw=1.6):
        self.add(f"<path d='{d}' fill='{fill}' stroke='{stroke}' stroke-width='{sw}' "
                 f"stroke-linejoin='round' stroke-linecap='round'/>")

    def save(self, out):
        head = (f"<svg xmlns='http://www.w3.org/2000/svg' width='{self.w}' height='{self.h}' "
                f"viewBox='0 0 {self.w} {self.h}'>\n"
                f"<title>{escape(self.title)}</title>\n<desc>{escape(self.desc)}</desc>\n")
        tail = "\n</svg>\n"
        out.write_text(head + "\n".join(self.parts) + tail, encoding="utf-8")
