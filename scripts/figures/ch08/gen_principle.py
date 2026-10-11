"""第8章原理示意图：亚硫酸盐转化、GLORI 化学、三字母比对、RNA 修饰版图、SNP 混杂。

用法：python3 gen_principle.py  （在 scripts/figures/ch08/ 下运行）
输出：写入 bioinfo_book_publish/assets/09-base-imbalanced-sequencing/
"""

from pathlib import Path
from common import Svg, COLOR_TEXT, COLOR_MUTED, COLOR_PRIMARY, COLOR_FILL, \
    COLOR_WARN, COLOR_WARN_FILL, COLOR_LINE, MONO, SANS, SIZE_LABEL, SIZE_TITLE, SIZE_NOTE

OUT = Path(__file__).resolve().parents[3] / "assets" / "09-base-imbalanced-sequencing"


from gen_bisulfite import gen_bisulfite_chemistry


def gen_glori_chemistry():
    """图：GLORI 化学——乙二醛保护 m6A，亚硝酸盐脱氨其余 A，残留 A 即 m6A。"""
    W, H = 900, 430
    s = Svg(W, H, "GLORI 化学原理",
            "乙二醛保护 m6A 与 G；亚硝酸盐把未修饰 A 脱氨为 I（读作 G）；"
            "m6A 位点在 reads 中残留 A，A/(A+G) 即修饰比例。")
    s.text(30, 34, "mRNA 片段（转录本局部序列）", size=SIZE_TITLE, mono=False, weight="bold")
    seq = "GACUAGACUAA"   # 第 7 个碱基（下标 6）为 m6A，处于 DRACH 基序
    x0, y = 60, 78
    cw = 58
    s.rect(x0 + 6 * cw - 8, y - 22, 34, 30, fill=COLOR_WARN_FILL, stroke=COLOR_WARN, sw=1.2, rx=4)
    for i, ch in enumerate(seq):
        col = COLOR_WARN if i == 6 else COLOR_TEXT
        s.text(x0 + i * cw, y, ch, size=22, fill=col, weight="bold" if i == 6 else "normal")
    s.text(x0 + 6 * cw + 40, y - 20, "m6A（DRACH 基序中的 A）", size=SIZE_NOTE, mono=False, fill=COLOR_WARN)

    s.arrow(430, 108, 430, 148, stroke=COLOR_PRIMARY, sw=1.8)
    s.text(448, 118, "① 乙二醛：保护 m6A 与 G", size=SIZE_NOTE, mono=False, fill=COLOR_PRIMARY)
    s.text(448, 140, "② 亚硝酸盐：未修饰 A 脱氨为 I", size=SIZE_NOTE, mono=False, fill=COLOR_PRIMARY)

    s.text(30, 196, "GLORI 处理 + 逆转录 + 测序后，reads 显示为：", size=SIZE_LABEL, mono=False, fill=COLOR_TEXT)
    y2 = 240
    for i, ch in enumerate(seq):
        if ch == "A" and i != 6:
            out, col, ring = "G", COLOR_PRIMARY, True
        elif i == 6:
            out, col, ring = "A", COLOR_WARN, True
        else:
            out, col, ring = ch, COLOR_TEXT, False
        x = x0 + i * cw
        if ring:
            s.rect(x - 8, y2 - 22, 34, 30,
                   fill=COLOR_FILL if col == COLOR_PRIMARY else COLOR_WARN_FILL,
                   stroke=col, sw=1.2, rx=4)
        s.text(x, y2, out, size=22, fill=col, weight="bold" if ring else "normal")
    s.text(x0 + 4 * cw, y2 + 34, "未修饰 A → 读作 G（~98% 转化）", size=SIZE_NOTE, mono=False, fill=COLOR_PRIMARY)
    s.text(x0 + 6 * cw - 40, y2 + 56, "m6A → 仍读 A", size=SIZE_NOTE, mono=False, fill=COLOR_WARN)

    s.rect(30, 320, 840, 84, fill=COLOR_FILL, stroke=COLOR_PRIMARY, sw=1.2, rx=8)
    s.text(50, 350, "位点修饰比例（化学计量）≈ 该位点 reads 中 A 占 (A + G) 的比例", size=SIZE_LABEL, mono=False, fill=COLOR_PRIMARY, weight="bold")
    s.text(50, 380, "与亚硫酸盐读 5mC 同构：把未修饰碱基化学改写掉，让修饰碱基留下来，从错配里读出比例。",
           size=SIZE_NOTE, mono=False, fill=COLOR_TEXT)
    s.text(50, 398, "代价：脱氨不完全的 ~2% 构成假阳性下限；A/G SNP 会被误读为“被保护的 A”——见 8.5.3。",
           size=SIZE_NOTE, mono=False, fill=COLOR_WARN)
    return s


def gen_three_letter_alignment():
    """图：三字母（双参考）比对原理——把参考转换成 C→T 与 G→A 两套，reads 同步转换后比对。"""
    W, H = 940, 560
    s = Svg(W, H, "三字母比对原理",
            "Bismark 把参考基因组分别转换为 C→T 与 G→A 两套三字母基因组；"
            "reads 同方向转换后进入 bowtie2 比对，再映射回原坐标，避开了成串假错配。")
    s.text(30, 34, "困难：reads 带成串系统性 C→T 错配，四字母直接比对会把它们当真错配",
           size=SIZE_TITLE, mono=False, weight="bold")
    # 参考与reads错配示意（左）
    ref = "CTCAGTC"
    read = "TTTAGTT"
    x0, yref, yread = 60, 74, 108
    for i, ch in enumerate(ref):
        x = x0 + i * 40
        s.text(x, yref, ch, size=18)
        s.line(x + 6, yref + 8, x + 6, yread - 14, stroke=COLOR_LINE, sw=0.8, dash="2,3")
        r = read[i]
        if r != ch:
            s.rect(x - 6, yread - 16, 28, 24, fill=COLOR_WARN_FILL, stroke=COLOR_WARN, sw=1.1, rx=3)
        s.text(x, yread, r, size=18, fill=COLOR_WARN if r != ch else COLOR_TEXT)
    s.text(x0, yread + 30, "wild-type 参考：错配多 → 比对丢失或错位", size=SIZE_NOTE, mono=False, fill=COLOR_WARN)

    s.line(30, 158, W - 30, 158, stroke=COLOR_LINE, sw=1)
    s.text(30, 188, "Bismark 的做法：把问题搬到“三字母世界”", size=SIZE_TITLE, mono=False, weight="bold")

    # 原参考
    s.text(60, 226, "参考基因组", size=SIZE_LABEL, mono=False, fill=COLOR_MUTED)
    s.text(180, 226, "CTCAGTC", size=18)
    # 箭头：参考 -> 两套转换
    s.arrow(150, 236, 150, 262, stroke=COLOR_PRIMARY, sw=1.4)
    # CT 转换组
    s.text(60, 274, "C→T 转换组", size=SIZE_LABEL, mono=False, fill=COLOR_PRIMARY)
    s.text(180, 274, "TTTAGTT", size=18, fill=COLOR_PRIMARY)
    s.text(320, 274, "（OT：reads 原链 C→T 后比对）", size=SIZE_NOTE, mono=False, fill=COLOR_MUTED)
    s.text(60, 306, "G→A 转换组", size=SIZE_LABEL, mono=False, fill=COLOR_PRIMARY)
    s.text(180, 306, "CTCAATC", size=18, fill=COLOR_PRIMARY)
    s.text(320, 306, "（OB：reads 互补 G→A 后比对）", size=SIZE_NOTE, mono=False, fill=COLOR_MUTED)

    # reads 同步转换并比对
    s.text(60, 356, "reads（OT 方向）", size=SIZE_LABEL, mono=False, fill=COLOR_MUTED)
    s.text(180, 356, "TTTAGTT", size=18)
    s.arrow(340, 350, 420, 350, stroke=COLOR_PRIMARY, sw=1.4)
    s.text(440, 356, "与 C→T 组完全匹配（错配消失）", size=SIZE_NOTE, mono=False, fill=COLOR_PRIMARY)

    s.text(60, 396, "reads（OB 方向）", size=SIZE_LABEL, mono=False, fill=COLOR_MUTED)
    s.text(180, 396, "AAATCAA", size=18)
    s.arrow(340, 390, 420, 390, stroke=COLOR_PRIMARY, sw=1.4)
    s.text(440, 396, "G→A 后与 G→A 组比对", size=SIZE_NOTE, mono=False, fill=COLOR_PRIMARY)

    s.rect(30, 430, 880, 108, fill=COLOR_FILL, stroke=COLOR_PRIMARY, sw=1.2, rx=8)
    s.text(50, 460, "比对发生在三字母世界，甲基化判读发生在四碱基世界：", size=SIZE_LABEL, mono=False, fill=COLOR_PRIMARY, weight="bold")
    s.text(50, 486, "比对完成后，Bismark 把 reads 映射回原始参考坐标，逐碱基重新比对 C（或 G）位置，", size=SIZE_NOTE, mono=False, fill=COLOR_TEXT)
    s.text(50, 508, "生成 XM 标签：该位点是 CpG/CHG/CHH 语境、甲基化（Z/X/H）还是未甲基化（z/x/h）。", size=SIZE_NOTE, mono=False, fill=COLOR_TEXT)
    s.text(50, 530, "方向性文库（OT/OB）只需跑两组；非方向性文库才需要 CTOT/CTOB 全部四组比对。", size=SIZE_NOTE, mono=False, fill=COLOR_MUTED)
    return s


def gen_rna_modification_landscape():
    """图：mRNA 上主要内部修饰的分布版图（自绘，依据 Roundtree 2017 等）。"""
    W, H = 920, 430
    s = Svg(W, H, "信使 RNA 上的主要内部修饰",
            "一条 mRNA 的示意：5′ 帽子后有 m6Am；内部以 m6A 最丰富，富集于终止密码子附近与 3′UTR；m5C 稀少。")
    # mRNA 骨架
    x0, x1, y = 90, 830, 120
    s.line(x0, y, x1, y, stroke=COLOR_PRIMARY, sw=3)
    # 5' cap
    s.circle_c(x0 - 16, y, 12, fill=COLOR_FILL, stroke=COLOR_PRIMARY, sw=1.6) if hasattr(s, "circle_c") else None
    s.add(f"<circle cx='{x0-16}' cy='{y}' r='12' fill='{COLOR_FILL}' stroke='{COLOR_PRIMARY}' stroke-width='1.6'/>")
    s.text(x0 - 46, y + 4, "5′", size=SIZE_LABEL, mono=False, fill=COLOR_MUTED)
    s.text(x0 - 16, y + 34, "m7G 帽", size=SIZE_NOTE, mono=False, fill=COLOR_MUTED, anchor="start")
    # 结构区段
    segs = [(90, 260, "5′UTR"), (260, 660, "编码区（CDS）"), (660, 830, "3′UTR")]
    for a, b, name in segs:
        s.text((a + b) / 2, y - 16, name, size=SIZE_LABEL, mono=False, fill=COLOR_MUTED, anchor="middle")
    # 终止密码子
    s.text(668, y + 24, "终止密码子", size=SIZE_NOTE, mono=False, fill=COLOR_WARN)
    s.line(660, y + 6, 660, y + 14, stroke=COLOR_WARN, sw=1.6)

    # m6Am：帽子后第一位
    s.add(f"<circle cx='{x0+18}' cy='{y-12}' r='7' fill='{COLOR_WARN_FILL}' stroke='{COLOR_WARN}' stroke-width='1.4'/>")
    s.text(x0 + 2, y - 30, "m6Am", size=SIZE_NOTE, mono=False, fill=COLOR_WARN, anchor="start")
    # m6A：DRACH，富集终止密码子附近与3'UTR
    m6a_x = [300, 380, 470, 600, 640, 690, 720, 770, 800]
    for i, mx in enumerate(m6a_x):
        s.add(f"<circle cx='{mx}' cy='{y-12}' r='7' fill='{COLOR_FILL}' stroke='{COLOR_PRIMARY}' stroke-width='1.4'/>")
        s.line(mx, y - 5, mx, y - 1, stroke=COLOR_PRIMARY, sw=1.2)
    s.text(560, y - 30, "m6A（最丰富，DRACH 基序，富集于终止密码子附近与 3′UTR）", size=SIZE_NOTE, mono=False, fill=COLOR_PRIMARY, anchor="middle")
    # m5C：稀少
    for mx in (340, 700):
        s.add(f"<circle cx='{mx}' cy='{y+22}' r='6' fill='#ffffff' stroke='{COLOR_MUTED}' stroke-width='1.3'/>")
        s.text(mx, y + 44, "m5C（少量）", size=SIZE_NOTE, mono=False, fill=COLOR_MUTED, anchor="middle")
    # polyA
    s.text(x1 + 8, y + 4, "poly(A)", size=SIZE_LABEL, mono=False, fill=COLOR_MUTED)

    # 底部注释条
    s.rect(30, 210, 860, 190, fill="none", stroke=COLOR_LINE, sw=1, rx=8)
    s.text(50, 240, "三种修饰的数量级对比（约）：", size=SIZE_LABEL, mono=False, weight="bold")
    rows = [
        ("m6A", "占全部腺苷的 0.2%–0.6%；修饰比例普遍低（多数位点 <20%），化学计量可被 GLORI 定量", COLOR_PRIMARY),
        ("m6Am", "只出现在帽子后第一个核苷酸；修饰比例通常远高于内部 m6A", COLOR_WARN),
        ("m5C / m1A", "mRNA 上含量低（m1A 主要存在于 tRNA/rRNA 与线粒体 mRNA）", COLOR_MUTED),
    ]
    for i, (name, desc, col) in enumerate(rows):
        yy = 272 + i * 36
        s.rect(50, yy - 16, 70, 24, fill=COLOR_FILL if col == COLOR_PRIMARY else ("#fdf3e3" if col == COLOR_WARN else "#f3f4f6"),
               stroke=col, sw=1.1, rx=4)
        s.text(85, yy + 1, name, size=SIZE_LABEL, mono=False, fill=col, anchor="middle", weight="bold")
        s.text(140, yy + 1, desc, size=SIZE_NOTE, mono=False, fill=COLOR_TEXT)
    return s


def gen_snp_confounding():
    """图：GLORI 中的 SNP 混杂——A/G SNP 与 m6A 产生同款信号，必须用基因组变异数据排除。"""
    W, H = 900, 520
    s = Svg(W, H, "SNP 混杂：与 m6A 相同的信号",
            "基因组 A/G SNP 的 G 错配与“m6A 被保护”的 A 残留，在单一样本中无法区分；需要 SNP 数据库或对照排除。")

    s.text(30, 34, "情形一：真正的 m6A 位点", size=SIZE_TITLE, mono=False, weight="bold")
    # 基因组 A 位点，reads 混合
    y = 74
    s.text(60, y, "基因组:", size=SIZE_LABEL, mono=False, fill=COLOR_MUTED)
    s.text(140, y, "…GACUAGAACUAA…", size=18)
    s.text(140, y + 26, "↑ 第 7 位为 A（无 SNP）", size=SIZE_NOTE, mono=False, fill=COLOR_MUTED)
    reads = ["…G G G A G G…（带 m6A 的 reads：A 被保护而残留）", "…G G G G G G…（未修饰 reads：A 脱氨读作 G）"]
    for i, r in enumerate(reads):
        yy = y + 58 + i * 26
        s.text(140, yy, r, size=SIZE_NOTE, mono=True, fill=COLOR_TEXT)
    s.text(560, y + 76, "A 残留比例 ≈ m6A 比例", size=SIZE_LABEL, mono=False, fill=COLOR_PRIMARY, weight="bold")

    s.line(30, 220, W - 30, 220, stroke=COLOR_LINE, sw=1)

    s.text(30, 252, "情形二：A/G SNP（基因组变异）伪装成 m6A", size=SIZE_TITLE, mono=False, weight="bold")
    y2 = 292
    s.text(60, y2, "基因组:", size=SIZE_LABEL, mono=False, fill=COLOR_MUTED)
    s.text(140, y2, "…GACUAGAACUAA…", size=18)
    s.text(140, y2 + 26, "↑ 该个体此位点是 A/G 杂合 SNP（一条染色单体为 G）", size=SIZE_NOTE, mono=False, fill=COLOR_WARN)
    reads2 = ["…G G G G G G…（G 等位单体：本来就是 G）",
              "…G G G G G G…（A 等位单体未修饰：脱氨后也读 G）",
              "…G G G A G G…（A 等位单体若带 m6A：读 A，与 m6A 信号混在一起）"]
    for i, r in enumerate(reads2):
        yy = y2 + 58 + i * 26
        s.text(140, yy, r, size=SIZE_NOTE, mono=True, fill=COLOR_TEXT)
    s.rect(30, y2 + 134, 840, 64, fill=COLOR_WARN_FILL, stroke=COLOR_WARN, sw=1.2, rx=8)
    s.text(50, y2 + 158, "关键：A/G SNP 中的 G 等位 reads 与“未修饰 A 脱氨成 G”的 reads 完全同形；", size=SIZE_LABEL, mono=False, fill=COLOR_WARN, weight="bold")
    s.text(50, y2 + 182, "杂合 SNP 若恰有 m6A，比例会被错误合并。必须用 dbSNP/1000G 等已知变异位点排除（GLORI-tools 内置多重过滤）。",
           size=SIZE_NOTE, mono=False, fill=COLOR_TEXT)
    return s


FIGS = {
    "bisulfite-conversion-principle.svg": gen_bisulfite_chemistry,
    "glori-chemistry.svg": gen_glori_chemistry,
    "three-letter-alignment.svg": gen_three_letter_alignment,
    "rna-modification-landscape.svg": gen_rna_modification_landscape,
    "snp-confounding.svg": gen_snp_confounding,
}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for name, fn in FIGS.items():
        svg = fn()
        p = OUT / name
        p.write_text(str(svg), encoding="utf-8")
        print("written", p)


if __name__ == "__main__":
    # Svg 需要 save 方法：补一个通用输出
    def _save(self):
        head = (f"<svg xmlns='http://www.w3.org/2000/svg' width='{self.w}' height='{self.h}' "
                f"viewBox='0 0 {self.w} {self.h}'>\n<title>{self.title}</title>\n<desc>{self.desc}</desc>\n")
        return head + "\n".join(self.parts) + "\n</svg>\n"
    Svg.__str__ = _save
    main()
