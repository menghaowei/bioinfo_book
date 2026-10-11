"""图 6.9：end-to-end 与 local 两种比对模式（自绘，参照 Bowtie 2 手册概念）。

运行：python3 scripts/figures/ch06/gen_e2e.py
输出：assets/07-chip-seq-and-atac-seq/020-e2e-vs-local.svg（旧 012 jpg 保留）
"""

from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent))
from common import (Svg, COLOR_TEXT, COLOR_MUTED, COLOR_PRIMARY, COLOR_FILL,
                    COLOR_WARN, COLOR_WARN_FILL, COLOR_LINE, SIZE_NOTE, SIZE_TITLE)

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "assets" / "07-chip-seq-and-atac-seq" / "020-e2e-vs-local.svg"

CHAR_W = 13   # 等宽字符栅格
REF = "GATTACAGGCATTCGATCGATCGAATTCGGATCCGATCGA"
READ_FULL = "GATTACAGTATTCGATCGATCGAATTCGGATCCGATCCT"   # 与参考差 2 个错配
CLIP_L, CLIP_R = 7, 6   # local 模式两端剪除的字符数

X0 = 170   # 序列起点
Y_PANEL = [70, 250]


def draw_seq(s: Svg, x, y, seq, *, colors=None, size=15):
    for i, ch in enumerate(seq):
        fill = (colors[i] if colors else COLOR_TEXT)
        s.text(x + i * CHAR_W, y, ch, size=size, mono=True, fill=fill)


def main():
    s = Svg(980, 480, "end-to-end 与 local 两种比对模式的区别",
            "同一条 read 的两种结局：end-to-end 模式全长参与比对，错配计罚但不剪除；local 模式两端 soft-clip，只保留高分的中间区段。")

    # ---------- 面板 1：end-to-end ----------
    y1 = Y_PANEL[0]
    s.text(60, y1 - 26, "end-to-end（全局比对，默认）", size=SIZE_TITLE, weight="bold", fill=COLOR_PRIMARY)
    s.text(X0 - 12, y1 - 4, "参考", size=SIZE_NOTE, fill=COLOR_MUTED, anchor="end")
    draw_seq(s, X0, y1, REF)
    s.text(X0 - 12, y1 + 26, "read", size=SIZE_NOTE, fill=COLOR_MUTED, anchor="end")
    colors_full = [COLOR_TEXT] * len(READ_FULL)
    for i, (a, b) in enumerate(zip(REF, READ_FULL)):
        if a != b:
            colors_full[i] = COLOR_WARN
    draw_seq(s, X0, y1 + 30, READ_FULL, colors=colors_full)
    # 错配标记
    for i, (a, b) in enumerate(zip(REF, READ_FULL)):
        if a != b:
            s.line(X0 + i * CHAR_W - 4, y1 + 40, X0 + i * CHAR_W + 4, y1 + 40, stroke=COLOR_WARN, sw=2)
    s.text(X0, y1 + 66, "整条 read 全长参与比对：错配（琥珀色）计入罚分，但不剪除任何碱基", size=SIZE_NOTE, fill=COLOR_MUTED)

    # ---------- 面板 2：local ----------
    y2 = Y_PANEL[1]
    s.text(60, y2 - 26, "local（局部比对）", size=SIZE_TITLE, weight="bold", fill=COLOR_PRIMARY)
    s.text(X0 - 12, y2 - 4, "参考", size=SIZE_NOTE, fill=COLOR_MUTED, anchor="end")
    draw_seq(s, X0, y2, REF)
    # 中段完美比对（与参考一致），两端 soft-clip
    mid = REF[CLIP_L:len(REF) - CLIP_R]
    yread = y2 + 30
    # soft-clip 左：灰框 + read 字符灰色
    s.rect(X0 - 6, yread - 16, CLIP_L * CHAR_W + 8, 24, fill=COLOR_WARN_FILL, stroke=COLOR_LINE, dash="4 3", rx=4)
    draw_seq(s, X0, yread, READ_FULL[:CLIP_L], colors=[COLOR_MUTED] * CLIP_L)
    # 中段
    draw_seq(s, X0 + CLIP_L * CHAR_W, yread, mid, colors=[COLOR_TEXT] * len(mid))
    # soft-clip 右
    rx = X0 + (len(REF) - CLIP_R) * CHAR_W
    s.rect(rx - 2, yread - 16, CLIP_R * CHAR_W + 8, 24, fill=COLOR_WARN_FILL, stroke=COLOR_LINE, dash="4 3", rx=4)
    draw_seq(s, X0 + (len(REF) - CLIP_R) * CHAR_W, yread, READ_FULL[len(REF) - CLIP_R:], colors=[COLOR_MUTED] * CLIP_R)
    s.text(X0 + CLIP_L * CHAR_W / 2 - 6, yread + 34, "soft-clip（不计分）", size=SIZE_NOTE, fill=COLOR_MUTED, anchor="middle")
    s.text(X0 + CLIP_L * CHAR_W + len(mid) * CHAR_W / 2, yread + 34, "高分区段参与比对", size=SIZE_NOTE, fill=COLOR_PRIMARY, anchor="middle")
    s.text(rx + CLIP_R * CHAR_W / 2 + 4, yread + 34, "soft-clip（不计分）", size=SIZE_NOTE, fill=COLOR_MUTED, anchor="middle")
    s.text(X0, yread + 62, "两端低质量部分被剪除，只保留得分最高的中间区段", size=SIZE_NOTE, fill=COLOR_MUTED)

    # 底部结论
    s.line(80, 420, 900, 420, stroke=COLOR_LINE, sw=1)
    s.text(490, 448, "ChIP-seq 数据用默认的 end-to-end 即可；local 适合 reads 质量差或预期存在融合/重排的场景",
           size=SIZE_NOTE, fill=COLOR_TEXT, anchor="middle")
    s.text(490, 470, "（参照 Bowtie 2 手册概念自绘；序列字符为等宽字体逐列对齐）", size=SIZE_NOTE, fill=COLOR_MUTED, anchor="middle")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(s.parts and _svg(s) or "", encoding="utf-8")
    print("written:", OUT.name)


def _svg(s: Svg) -> str:
    from xml.sax.saxutils import escape
    head = (f"<svg xmlns='http://www.w3.org/2000/svg' width='{s.w}' height='{s.h}' "
            f"viewBox='0 0 {s.w} {s.h}'>\n"
            f"<title>{escape(s.title)}</title>\n<desc>{escape(s.desc)}</desc>\n")
    return head + "\n".join(s.parts) + "\n</svg>\n"


if __name__ == "__main__":
    main()
