"""第4章序列示意图 SVG 生成的共享样式与工具。

全书序列示意图统一使用这些常量，保证各图字体、字号、配色一致：
- 序列字符使用等宽字体逐字符定位，保证严格列对齐；
- 中文标注使用系统无衬线中文字体栈；
- 配色与网站主题（book.css）保持一致：主色深绿、浅绿高亮、琥珀色警示。
"""

from pathlib import Path
from xml.sax.saxutils import escape

# 字体栈（SVG 通过 <img> 引用时无法继承页面 CSS，必须内嵌声明）
MONO = "ui-monospace, 'SFMono-Regular', Menlo, Consolas, 'Liberation Mono', monospace"
SANS = "'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', 'Noto Sans CJK SC', sans-serif"

# 配色（与 styles/book.css 主题一致）
COLOR_TEXT = "#333333"       # 正文
COLOR_MUTED = "#6b7280"      # 辅助说明
COLOR_PRIMARY = "#186254"    # 主题深绿（强调、框线、匹配）
COLOR_FILL = "#e8f4f1"       # 浅绿底（单元格高亮）
COLOR_WARN = "#b45309"       # 琥珀（错配、删除、警示文字）
COLOR_WARN_FILL = "#fdf3e3"  # 浅琥珀底
COLOR_LINE = "#9ca3af"       # 坐标线、辅助线
COLOR_PAGE = "#fcfcf9"       # 与网站暖白一致（仅用于不透明底场景，默认透明）

# 字号（viewBox 坐标系内）
SIZE_SEQ = 16        # 序列字符
SIZE_LABEL = 13      # 行列标注
SIZE_TITLE = 15      # 图内标题
SIZE_NOTE = 12       # 图内注释

# 等宽字符栅格：字符间距与行高
CHAR_W = 12
ROW_H = 24


class Svg:
    """极简 SVG 画布：收集元素，最后输出字符串。"""

    def __init__(self, width, height, title, desc):
        self.w = width
        self.h = height
        self.title = title
        self.desc = desc
        self.parts = []

    def add(self, s):
        self.parts.append(s)

    def text(self, x, y, s, *, size=SIZE_SEQ, mono=True, fill=COLOR_TEXT,
             weight="normal", anchor="start", style=None):
        fam = MONO if mono else SANS
        extra = f" font-style='{style}'" if style else ""
        self.add(f"<text x='{x}' y='{y}' font-family=\"{fam}\" font-size='{size}' "
                 f"fill='{fill}' font-weight='{weight}' text-anchor='{anchor}'{extra}>"
                 f"{escape(s)}</text>")

    def rect(self, x, y, w, h, *, fill="none", stroke=COLOR_PRIMARY, sw=1.2, rx=3, dash=None):
        d = f" stroke-dasharray='{dash}'" if dash else ""
        self.add(f"<rect x='{x}' y='{y}' width='{w}' height='{h}' rx='{rx}' "
                 f"fill='{fill}' stroke='{stroke}' stroke-width='{sw}'{d}/>")

    def line(self, x1, y1, x2, y2, *, stroke=COLOR_LINE, sw=1.2, dash=None):
        d = f" stroke-dasharray='{dash}'" if dash else ""
        self.add(f"<line x1='{x1}' y1='{y1}' x2='{x2}' y2='{y2}' "
                 f"stroke='{stroke}' stroke-width='{sw}'{d}/>")

    def arrow(self, x1, y1, x2, y2, *, stroke=COLOR_PRIMARY, sw=1.6):
        """带箭头的连线（直线）。"""
        import math
        self.line(x1, y1, x2, y2, stroke=stroke, sw=sw)
        ang = math.atan2(y2 - y1, x2 - x1)
        L, A = 9, 0.45
        for da in (A, -A):
            bx = x2 - L * math.cos(ang + da)
            by = y2 - L * math.sin(ang + da)
            self.add(f"<line x1='{x2:.1f}' y1='{y2:.1f}' x2='{bx:.1f}' y2='{by:.1f}' "
                     f"stroke='{stroke}' stroke-width='{sw}'/>")

    def seq(self, x, y, s, *, size=SIZE_SEQ, fill=COLOR_TEXT, weight="normal"):
        """按固定字符间距逐字符绘制序列，保证等宽列对齐。"""
        cw = CHAR_W if size == SIZE_SEQ else CHAR_W * size / SIZE_SEQ
        for i, ch in enumerate(s):
            self.text(x + i * cw, y, ch, size=size, fill=fill, weight=weight)
        return x + len(s) * cw

    def render(self):
        head = (f"<svg xmlns='http://www.w3.org/2000/svg' width='{self.w}' height='{self.h}' "
                f"viewBox='0 0 {self.w} {self.h}' role='img' aria-labelledby='t d'>\n"
                f"<title id='t'>{escape(self.title)}</title>\n"
                f"<desc id='d'>{escape(self.desc)}</desc>\n")
        return head + "\n".join(self.parts) + "\n</svg>\n"


OUT_DIR = Path(__file__).resolve().parents[3] / "assets" / "04-quality-control-and-alignment" / "svg"


def save(name, svg):
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / f"{name}.svg").write_text(svg.render(), encoding="utf-8")
    print(f"written {name}.svg ({svg.w}x{svg.h})")
