"""第6章三张自绘示意图：分析流程总览（重绘 003）、三类信号（重绘 013）、ATAC 原理（新增）。

运行：python3 scripts/figures/ch06/gen_svg.py
输出：assets/07-chip-seq-and-atac-seq/ 下的三个 SVG（编号 015/016/017，旧文件保留）。
"""

from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent))
from common import (Svg, COLOR_TEXT, COLOR_MUTED, COLOR_PRIMARY, COLOR_FILL,
                    COLOR_WARN, COLOR_WARN_FILL, COLOR_LINE, SIZE_LABEL, SIZE_NOTE, SIZE_TITLE)

ROOT = Path(__file__).resolve().parents[3]
ASSETS = ROOT / "assets" / "07-chip-seq-and-atac-seq"


def fig_overview():
    """分析流程总览：共用主干 + ChIP/ATAC 分支 + 共用统计与解释。"""
    s = Svg(980, 700, "ChIP-seq 与 ATAC-seq 分析流程总览",
            "两类区域信号数据共用质控与比对主干，在找峰前各有专属处理，最后汇入统一的计数、差异分析与解释框架。")
    # 标题
    s.text(490, 32, "区域信号分析：从 FASTQ 到结论", size=SIZE_TITLE, anchor="middle", weight="bold")

    cx = 490
    # 共用主干
    s.box(cx, 78, 320, 44, "原始数据 FASTQ", sub="公共数据下载 + md5 校验")
    s.arrow(cx, 100, cx, 128)
    s.box(cx, 150, 320, 44, "质控与修剪", sub="FastQC / fastp")
    s.arrow(cx, 172, cx, 200)
    s.box(cx, 222, 320, 44, "比对到参考基因组", sub="bowtie2（ATAC 加 -X 2000）")

    # 分叉
    lx, rx = 240, 740
    s.line(cx, 244, cx, 268, stroke=COLOR_PRIMARY, sw=1.6)
    s.line(cx, 268, lx, 268, stroke=COLOR_PRIMARY, sw=1.6)
    s.line(cx, 268, rx, 268, stroke=COLOR_PRIMARY, sw=1.6)
    s.arrow(lx, 268, lx, 292)
    s.arrow(rx, 268, rx, 292)
    s.text(lx, 262, "ChIP-seq 主线（NRF1）", size=SIZE_LABEL, anchor="middle", weight="bold", fill=COLOR_PRIMARY)
    s.text(rx, 262, "ATAC-seq 主线（Irf8）", size=SIZE_LABEL, anchor="middle", weight="bold", fill=COLOR_PRIMARY)

    s.box(lx, 316, 300, 52, "比对过滤", sub="samtools MAPQ≥30；峰前无重复去除")
    s.arrow(lx, 342, lx, 366)
    s.box(lx, 388, 300, 52, "peak calling（对 input）", sub="MACS3：NRF1 窄峰 / H3K27ac 宽峰")
    s.arrow(lx, 414, lx, 438)
    s.box(lx, 460, 300, 52, "重复一致性检验", sub="IDR（两个生物学重复）")

    s.box(rx, 316, 300, 52, "比对过滤 + 去 chrM + 去重", sub="samtools markdup")
    s.arrow(rx, 342, rx, 366)
    s.box(rx, 388, 300, 52, "Tn5 偏移校正", sub="alignmentSieve --ATACshift")
    s.arrow(rx, 414, rx, 438)
    s.box(rx, 460, 300, 52, "peak calling（无对照）+ 质控", sub="MACS3 BAMPE；ataqv 指标")

    # 汇合
    s.line(lx, 486, lx, 510, stroke=COLOR_PRIMARY, sw=1.6)
    s.line(rx, 486, rx, 510, stroke=COLOR_PRIMARY, sw=1.6)
    s.line(lx, 510, rx, 510, stroke=COLOR_PRIMARY, sw=1.6)
    s.arrow(cx, 510, cx, 534)
    s.box(cx, 560, 400, 44, "统一峰集合 + reads 计数", sub="bedtools 合并；计数矩阵")
    s.arrow(cx, 582, cx, 606)
    s.box(cx, 628, 400, 44, "差异分析（DiffBind/DESeq2）", sub="差异结合 / 差异可及性")
    s.arrow(cx, 650, cx, 672)
    s.text(cx, 692, "注释 · motif · 可视化 · 联合分析（6.8 节）", size=SIZE_LABEL, anchor="middle", fill=COLOR_PRIMARY, weight="bold")
    return s


def _reads(s, x0, x1, y, ticks, *, color=COLOR_PRIMARY):
    """沿基线画 reads 短竖线：ticks 为 [(x,len)]。"""
    s.line(x0, y, x1, y)
    for x, ln in ticks:
        s.line(x, y, x, y - ln, stroke=color, sw=1.4)


def _density(s, x0, x1, ybase, pts, hmax, *, fill=COLOR_FILL, stroke=COLOR_PRIMARY):
    """密度曲线：pts 为 [(x, 0..1)]，绘制并浅色填充。"""
    d = f"M {x0} {ybase}"
    for x, v in pts:
        d += f" L {x} {ybase - v * hmax}"
    d += f" L {x1} {ybase}"
    s.path(d, fill=fill, stroke=stroke, sw=1.6)


def _panel_signal(s, y0, label, design, plus, minus, dens, peak, peak_note):
    """一个信号面板：设计行 / 正链 / 负链 / 片段密度 / 峰区域。"""
    x0, x1 = 120, 880
    s.text(56, y0 + 14, label, size=SIZE_LABEL, weight="bold", fill=COLOR_PRIMARY)
    # 设计行
    s.text(x0 - 92, y0 + 6, "实验设计", size=SIZE_NOTE, fill=COLOR_MUTED)
    s.line(x0, y0 + 2, x1, y0 + 2, stroke=COLOR_LINE)
    for cx_, w in design:
        s.rect(cx_ - w / 2, y0 - 6, w, 16, fill=COLOR_WARN_FILL, stroke=COLOR_WARN, sw=1, rx=2)
    # reads 行
    yr = y0 + 46
    s.text(x0 - 92, yr - 12, "reads（+/−）", size=SIZE_NOTE, fill=COLOR_MUTED)
    _reads(s, x0, x1, yr, [(x, l) for x, l in plus], color=COLOR_PRIMARY)
    _reads(s, x0, x1, yr + 26, [(x, l) for x, l in minus], color=COLOR_MUTED)
    # 密度
    yd = yr + 92
    s.text(x0 - 92, yd - 8, "片段密度", size=SIZE_NOTE, fill=COLOR_MUTED)
    s.line(x0, yd, x1, yd, stroke=COLOR_LINE)
    _density(s, x0, x1, yd, dens, 52)
    # 峰区域
    yp = yd + 22
    s.text(x0 - 92, yp + 12, "峰区域", size=SIZE_NOTE, fill=COLOR_MUTED)
    for px, pw in peak:
        s.rect(px, yp, pw, 14, fill=COLOR_FILL, stroke=COLOR_PRIMARY, sw=1.2, rx=3)
    s.text(x1, yp + 42, peak_note, size=SIZE_NOTE, fill=COLOR_MUTED, anchor="end")


def fig_signals():
    """三类信号形态：A 窄峰 / B 宽峰 / C 混合。"""
    s = Svg(980, 640, "不同类型蛋白的 ChIP-seq 信号形态",
            "转录因子的窄峰、组蛋白修饰的宽峰与 RNA 聚合酶 II 的混合信号，及其对应的 reads 分布与峰区域。")
    s.text(490, 30, "三类信号形态决定找峰策略", size=SIZE_TITLE, anchor="middle", weight="bold")

    # A：窄峰
    import random
    random.seed(7)
    plusA = [(430 + random.randint(-55, 5), random.randint(10, 22)) for _ in range(16)]
    minusA = [(540 + random.randint(-5, 55), random.randint(10, 22)) for _ in range(16)]
    densA = [(490 + dx, max(0, 1 - abs(dx) / 70)) for dx in range(-150, 151, 10)]
    _panel_signal(s, 66, "A  转录因子（窄峰）",
                  design=[(490, 34)], plus=plusA, minus=minusA,
                  dens=densA, peak=[(458, 64)], peak_note="reads 在结合位点两侧形成双峰，峰区窄而尖")

    # B：宽峰
    plusB = [(250 + dx * 28 + random.randint(-8, 8), random.randint(8, 18)) for dx in range(19)]
    minusB = [(270 + dx * 28 + random.randint(-8, 8), random.randint(8, 18)) for dx in range(19)]
    densB = [(200 + dx * 4, min(1.0, 0.55 + 0.45 * (1 - abs(dx - 45) / 45))) for dx in range(0, 96, 2)]
    _panel_signal(s, 260, "B  组蛋白修饰（宽峰）",
                  design=[(260 + i * 55, 30) for i in range(6)], plus=plusB, minus=minusB,
                  dens=densB, peak=[(215, 510)], peak_note="修饰跨越多个核小体，信号宽而平")

    # C：混合
    plusC = ([(300 + random.randint(-45, 5), random.randint(8, 20)) for _ in range(9)] +
             [(430 + dx * 30 + random.randint(-10, 10), random.randint(6, 14)) for dx in range(13)])
    minusC = ([(345 + random.randint(-5, 45), random.randint(8, 20)) for _ in range(9)] +
              [(450 + dx * 30 + random.randint(-10, 10), random.randint(6, 14)) for dx in range(13)])
    densC = ([(320 + dx, max(0, 1 - abs(dx) / 55)) for dx in range(-120, 121, 8)] +
             [(440 + dx * 4, min(0.55, 0.30 + 0.25 * (1 - abs(dx - 40) / 40))) for dx in range(0, 81, 4)])
    _panel_signal(s, 454, "C  RNA 聚合酶 II（混合）",
                  design=[(320, 30)] + [(450 + i * 38, 26) for i in range(4)],
                  plus=plusC, minus=minusC, dens=densC,
                  peak=[(292, 56), (400, 380)],
                  peak_note="启动子处窄峰（起始/暂停）+ 基因区宽峰（延伸）")
    s.text(490, 624, "简化示意：reads 只测片段两端，正负链分布的峰间距近似片段长度", size=SIZE_NOTE, anchor="middle", fill=COLOR_MUTED)
    return s


def fig_atac_principle():
    """ATAC-seq 原理：开放染色质 + Tn5 建库 + 片段长度含义。"""
    s = Svg(980, 560, "ATAC-seq 原理示意",
            "Tn5 转座酶在开放染色质处切割并连接接头；插入片段长度反映核小体组织：无核小体区、单核小体与多核小体片段。")
    s.text(490, 32, "ATAC-seq：开放染色质被 Tn5 优先切割并连上接头", size=SIZE_TITLE, anchor="middle", weight="bold")

    # 染色质行
    y = 78
    s.text(120, y - 16, "细胞核内的染色质", size=SIZE_NOTE, fill=COLOR_MUTED)
    s.line(120, y, 860, y, stroke=COLOR_TEXT, sw=2)
    nucleosomes = [190, 280, 370, 560, 650, 740, 830]
    for nx in nucleosomes:
        s.circle(nx, y, 26, fill=COLOR_FILL, stroke=COLOR_PRIMARY, sw=1.4)
        s.text(nx, y + 4, "核小体", size=11, anchor="middle", fill=COLOR_MUTED)
    # 开放区
    s.rect(415, y - 30, 105, 60, fill=COLOR_WARN_FILL, stroke=COLOR_WARN, sw=1.2, rx=8, dash="4 3")
    s.text(467, y - 38, "开放染色质（NFR）", size=SIZE_NOTE, anchor="middle", fill=COLOR_WARN)
    # Tn5
    for tx in (440, 492):
        s.rect(tx - 10, y + 26, 20, 20, fill=COLOR_PRIMARY, rx=3)
        s.text(tx, y + 40, "Tn5", size=11, fill="#ffffff", anchor="middle")
    s.arrow(467, y + 50, 467, y + 88)
    s.text(482, y + 74, "切割 + 连接头，一步建库", size=SIZE_NOTE, fill=COLOR_PRIMARY)

    # 片段行
    y2 = 200
    s.text(120, y2 - 16, "得到的测序片段（接头之间为插入 DNA）", size=SIZE_NOTE, fill=COLOR_MUTED)
    frags = [
        (150, 130, "NFR 片段（<100 bp）", COLOR_WARN),
        (360, 260, "单核小体片段（~200 bp）", COLOR_PRIMARY),
        (680, 360, "多核小体片段（~400 bp）", COLOR_PRIMARY),
    ]
    for fx, fw, label, col in frags:
        s.rect(fx, y2, fw, 26, fill=COLOR_FILL, stroke=col, sw=1.4, rx=4)
        s.rect(fx - 14, y2 + 5, 10, 16, fill=col, rx=2)
        s.rect(fx + fw + 4, y2 + 5, 10, 16, fill=col, rx=2)
        s.text(fx + fw / 2, y2 + 46, label, size=SIZE_NOTE, anchor="middle", fill=COLOR_TEXT)
    # 片段中间的核小体示意
    s.circle(490, y2 + 13, 16, stroke=COLOR_MUTED)
    s.circle(860, y2 + 13, 16, stroke=COLOR_MUTED)

    # 分布示意
    y3 = 330
    s.text(120, y3 - 12, "片段长度分布（示意）", size=SIZE_NOTE, fill=COLOR_MUTED)
    s.line(160, 460, 880, 460, stroke=COLOR_TEXT)
    bars = [(200, 34, "NFR"), (330, 78, "单核小体"), (470, 44, "双核小体"), (600, 24, "三核小体")]
    for bx, bh, lab in bars:
        s.rect(bx - 34, 460 - bh, 68, bh, fill=COLOR_FILL, stroke=COLOR_PRIMARY, sw=1.2, rx=3)
        s.text(bx, 460 - bh - 8, lab, size=SIZE_NOTE, anchor="middle", fill=COLOR_TEXT)
    s.path("M 166 460 Q 200 415 236 430 Q 300 470 330 382 Q 360 452 400 456 "
           "Q 470 470 470 440 Q 500 458 536 452 Q 600 468 600 448 Q 640 458 680 455 "
           "Q 780 458 870 458", stroke=COLOR_PRIMARY, sw=1.6)
    for tick, lab in [(200, "100"), (330, "200"), (470, "400"), (600, "600")]:
        s.line(tick, 460, tick, 468)
        s.text(tick, 484, lab, size=SIZE_NOTE, anchor="middle", fill=COLOR_MUTED)
    s.text(880, 484, "片段长度（bp）", size=SIZE_NOTE, anchor="end", fill=COLOR_MUTED)
    s.text(160, 510, "NFR 峰与约 200 bp 周期的核小体峰同时出现，说明文库捕获了真实的染色质组织",
           size=SIZE_NOTE, fill=COLOR_MUTED)
    return s


def main():
    ASSETS.mkdir(parents=True, exist_ok=True)
    fig_overview().save(ASSETS / "015-analysis-overview-dual-case.svg")
    fig_signals().save(ASSETS / "016-signal-types.svg")
    fig_atac_principle().save(ASSETS / "017-atac-principle.svg")
    print("written:", *(p.name for p in sorted(ASSETS.glob("01[567]*.svg"))))


if __name__ == "__main__":
    main()
