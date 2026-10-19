#!/usr/bin/env python3
"""Draw the local/remote computing diagram with editable SVG text.

Run with Python 3 from any directory; no external dependencies.
This conceptual illustration follows the book's existing figure palette.
"""
from html import escape
from pathlib import Path


OUT = Path(__file__).resolve().parents[3] / "assets/02-computing-and-programming/svg/local-remote-platform.svg"
GREEN, LIGHT, INK, GREY, LINE, BG = "#186254", "#e8f4f1", "#333333", "#6b7280", "#9ca3af", "#fcfcf9"
FONT = "'PingFang SC','Hiragino Sans GB','Microsoft YaHei','Noto Sans CJK SC',sans-serif"


def draw():
    parts = [f'''<svg xmlns="http://www.w3.org/2000/svg" width="640" height="610" viewBox="0 0 640 610" role="img" aria-labelledby="title description">
<title id="title">本地电脑与远端服务器的分工与连接</title>
<desc id="description">本地电脑按需选择 Windows、macOS 或 Linux，用来编辑代码、绘图和使用 AI agent。通过终端或 VS Code Remote-SSH，以 SSH 连接通常运行 Linux 的远端服务器：命令从本地发往远端，输出从远端返回本地；比对、定量等重计算在服务器执行。两端的系统不必相同。</desc>
<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M1 1 L9 5 L1 9" fill="none" stroke="{GREEN}" stroke-width="1.6"/></marker></defs>
<rect width="640" height="610" fill="{BG}"/>
<g stroke-linecap="round" stroke-linejoin="round">''']

    def rect(x, y, w, h, fill=LIGHT, stroke="none", radius=12, sw=2.5):
        parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')

    def text(x, y, value, size=24, color=INK, weight=400):
        parts.append(f'<text x="{x}" y="{y}" text-anchor="middle" font-family="{FONT}" font-size="{size}" font-weight="{weight}" fill="{color}">{escape(value)}</text>')

    def path(d, color=GREEN, width=2.5, fill="none", arrow=False):
        marker = ' marker-end="url(#arrow)"' if arrow else ''
        parts.append(f'<path d="{d}" fill="{fill}" stroke="{color}" stroke-width="{width}"{marker}/>')

    # Operating systems are alternatives on the local computer, not steps.
    text(140, 49, "本地电脑", 29, GREEN, 600)
    text(500, 49, "远端服务器", 29, GREEN, 600)
    text(140, 93, "按需选择系统", 24)
    text(140, 131, "Windows / macOS", 24)
    text(140, 164, "或 Linux", 24)
    text(500, 93, "通常运行", 24)
    text(500, 145, "Linux", 36, GREEN, 600)

    # Laptop: terminal and plot symbols represent interactive local work.
    rect(44, 210, 192, 122, "white", GREEN, 9)
    rect(55, 221, 170, 96, LIGHT, radius=3)
    path("M70 239 l13 11 -13 11 M92 265 h20", width=3)
    path("M146 240 V298 H207", width=2)
    path("M156 281 l14 -12 13 7 14 -24", width=3)
    path("M44 332 L25 350 Q24 356 34 356 H246 Q256 356 255 350 L236 332 Z", fill=LIGHT)
    path("M119 340 H161", color=LINE, width=3)

    # Rack server, distinct from the local laptop.
    rect(439, 190, 122, 166, "white", GREEN, 10)
    for y in (204, 250, 296):
        rect(450, y, 100, 34, LIGHT, GREEN, 5, 1.7)
        parts.append(f'<circle cx="465" cy="{y + 17}" r="4" fill="{GREEN}"/>')
        for x in (491, 501, 511, 521, 531):
            path(f"M{x} {y + 10} v14", color=LINE, width=1.7)
    path("M451 356 v9 M549 356 v9", width=4)

    # Arrows are remote command/output flow, not file transfer.
    text(320, 225, "发送命令", 23)
    path("M269 241 H371", arrow=True)
    text(320, 283, "SSH", 27, GREEN, 600)
    path("M371 304 H269", arrow=True)
    text(320, 339, "返回输出", 23)
    text(140, 389, "终端或 VS Code", 23)
    text(140, 421, "Remote-SSH", 23, GREY)

    # Typical division of work, as introduced in the adjacent paragraph.
    rect(16, 452, 248, 138)
    rect(376, 452, 248, 138)
    text(140, 488, "编辑代码", 24)
    text(140, 527, "绘图", 24)
    text(140, 566, "使用 AI agent", 24)
    text(500, 507, "比对、定量", 24)
    text(500, 546, "等重计算", 24)

    parts.append("</g></svg>\n")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(parts), encoding="utf-8")
    print(OUT)


if __name__ == "__main__":
    draw()
