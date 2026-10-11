"""图：IGV 甲基化轨迹复核示意（两个样本同一区域对比 + DMR 标注）。自绘示意，非真实截图。

用法：python3 gen_igv_methylation.py
输出：assets/09-base-imbalanced-sequencing/igv-methylation.svg
"""

from pathlib import Path

from common import Svg, COLOR_TEXT, COLOR_MUTED, COLOR_PRIMARY, COLOR_FILL, \
    COLOR_WARN, COLOR_WARN_FILL, COLOR_LINE

OUT = Path(__file__).resolve().parents[3] / "assets" / "09-base-imbalanced-sequencing"


def main():
    W, H = 780, 420
    s = Svg(W, H, "IGV 甲基化复核示意",
            "上：血清样本；下：2i 样本。同一区域逐位点甲基化条形，血清样本普遍高，"
            "2i 样本塌陷；中间阴影为 DMR。")
    # 30 个 CpG 位点，固定伪随机比例
    import random
    random.seed(8)
    serum = [random.uniform(0.62, 0.94) for _ in range(30)]
    two_i = [random.uniform(0.04, 0.38) for _ in range(30)]
    # DMR 区域：位点 10–22
    x0, dx = 70, 22
    track_h = 120
    for ti, (label, vals, y_top) in enumerate((("血清培养（toSerum）", serum, 90),
                                                ("2i 培养（to2i）", two_i, 280))):
        y_base = y_top + track_h
        # 轴线与标签
        s.line(x0 - 20, y_base, W - 40, y_base, stroke=COLOR_LINE, sw=1)
        s.text(x0 - 55, y_top + 20, label, size=13, mono=False, fill=COLOR_TEXT, weight="bold")
        s.text(x0 - 55, y_base - 5, "100%", size=10, mono=False, fill=COLOR_MUTED)
        s.text(x0 - 55, y_base - 60, "50%", size=10, mono=False, fill=COLOR_MUTED)
        s.line(x0 - 20, y_base - 60, W - 40, y_base - 60, stroke=COLOR_LINE, sw=0.5, dash="3,4")
        for i, v in enumerate(vals):
            x = x0 + i * dx
            col = COLOR_PRIMARY if ti == 0 else COLOR_WARN
            hgt = v * track_h * 0.92
            s.line(x, y_base, x, y_base - hgt, stroke=col, sw=7)
        # 覆盖厚度示意：底部小灰点
        for i, v in enumerate(vals):
            x = x0 + i * dx
            s.circle_c(x, y_base + 8, 2.5, fill=COLOR_MUTED, stroke="none") \
                if hasattr(s, "circle_c") else s.add(
                f"<circle cx='{x}' cy='{y_base+8}' r='2.5' fill='{COLOR_MUTED}'/>")
    # DMR 阴影（跨两个轨道）
    dm_x0 = x0 + 10 * dx - 12
    dm_x1 = x0 + 22 * dx + 12
    s.add(f"<rect x='{dm_x0}' y='82' width='{dm_x1-dm_x0}' height='316' fill='{COLOR_WARN_FILL}' "
          f"opacity='0.45' stroke='{COLOR_WARN}' stroke-width='1.2' stroke-dasharray='6,4'/>")
    s.text((dm_x0 + dm_x1) / 2, 76, "DMR（统计检出的差异区域）", size=12, mono=False,
           fill=COLOR_WARN, anchor="middle", weight="bold")
    # 基因组坐标轴
    y_ax = 404
    s.line(x0 - 20, y_ax, W - 40, y_ax, stroke=COLOR_LINE, sw=1)
    for frac, lab in ((0, "48,200"), (0.5, "48,750"), (1.0, "49,300")):
        x = x0 - 20 + frac * (W - 40 - x0 + 20)
        s.line(x, y_ax - 4, x, y_ax + 4, stroke=COLOR_MUTED, sw=1)
        s.text(x, y_ax + 16, lab, size=10, mono=False, fill=COLOR_MUTED, anchor="middle")
    s.text(W - 40, y_ax - 14, "chr12（mm9，示意坐标）", size=10, mono=False,
           fill=COLOR_MUTED, anchor="end")
    s.text(x0 - 55, 40, "每个条形 = 一个 CpG 位点的甲基化比例；条形高度即比例，底部灰点示意覆盖深度。",
           size=11, mono=False, fill=COLOR_MUTED)

    def _save(self):
        head = (f"<svg xmlns='http://www.w3.org/2000/svg' width='{self.w}' height='{self.h}' "
                f"viewBox='0 0 {self.w} {self.h}'>\n<title>{self.title}</title>\n<desc>{self.desc}</desc>\n")
        return head + "\n".join(self.parts) + "\n</svg>\n"

    Svg.__str__ = _save
    p = OUT / "igv-methylation.svg"
    p.write_text(str(s), encoding="utf-8")
    print("written", p)


if __name__ == "__main__":
    main()
