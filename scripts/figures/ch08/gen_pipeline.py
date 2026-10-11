"""第8章流程总览图：BS-seq 链与 GLORI 链（仿第7章 preprocessing-overview 的竖版样式）。

用法：python3 gen_pipeline.py  （在 scripts/figures/ch08/ 下运行）
输出：assets/09-base-imbalanced-sequencing/bs-pipeline-overview.svg、glori-pipeline-overview.svg
"""

from pathlib import Path

from common import Svg, COLOR_TEXT, COLOR_MUTED, COLOR_PRIMARY, COLOR_FILL, \
    COLOR_WARN, COLOR_LINE

OUT = Path(__file__).resolve().parents[3] / "assets" / "09-base-imbalanced-sequencing"

BOX_X, BOX_W = 30, 340
STEP_H, STEP_GAP = 50, 36
AN_X = 386


def add_step(s, idx, y, title, output, action, check, last=False):
    s.add(f"<rect x='{BOX_X}' y='{y}' width='{BOX_W}' height='{STEP_H}' rx='6' "
          f"fill='{COLOR_FILL if last else 'none'}' stroke='{COLOR_PRIMARY}' stroke-width='1.2'/>")
    s.text(BOX_X + BOX_W / 2, y + 29.7, f"{'①②③④⑤⑥⑦⑧'[idx - 1]} {title}",
           size=13, mono=False, weight="bold", anchor="middle")
    s.text(AN_X, y + 16, output, size=12, mono=False, fill=COLOR_PRIMARY, weight="bold")
    s.text(AN_X, y + 32, action, size=12, mono=False, fill=COLOR_MUTED)
    s.text(AN_X, y + 46, check, size=12, mono=False, fill=COLOR_WARN)


def add_arrow(s, y):
    x = BOX_X + BOX_W / 2
    y2 = y + STEP_GAP
    s.line(x, y, x, y2, stroke=COLOR_PRIMARY, sw=2.0)
    s.line(x, y2, x + 3.9, y2 - 8.1, stroke=COLOR_PRIMARY, sw=2.0)
    s.line(x, y2, x - 3.9, y2 - 8.1, stroke=COLOR_PRIMARY, sw=2.0)


def gen_bs_pipeline():
    W, H = 760, 620
    s = Svg(W, H, "BS-seq 分析流程",
            "从 FASTQ 到位点计数表的六个步骤（竖版）：质控、转化参考索引、三字母比对、"
            "去重、甲基化提取，最后进入位点定量与差异甲基化分析。")
    steps = [
        ("原始质控与去接头", "trimmed FASTQ", "reads 带系统性 C→T 错配属预期（trim_galore）",
         "检查：碱基组成 T 高 C 低、接头去除"),
        ("建立转化参考索引", "两套三字母基因组索引", "C→T 与 G→A 各建 bowtie2 索引（bismark_genome_preparation）",
         "检查：CT/GA 两套索引齐全"),
        ("三字母比对", "BAM（XM/XR/XG 标签）", "reads 同步转换后比对，再映射回原坐标（bismark）",
         "检查：方向性文库比对率 50%–75%"),
        ("去重", "去重 BAM", "PCR 重复不算独立证据（deduplicate_bismark）",
         "检查：重复率是否异常"),
        ("甲基化提取", "bismark.cov / cytosine_report", "逐位点清点甲基化/未甲基化 read（bismark_methylation_extractor）",
         "检查：M-bias 平坦、CHH 接近噪声地板"),
        ("位点计数表就绪，进入定量与 DMR", "位点 × 样本计数表", "覆盖率过滤、样本合并后做 DML/DMR 分析（8.3）",
         "检查：覆盖深度、转化率对照"),
    ]
    y = 78
    for i, (t, o, a, c) in enumerate(steps, 1):
        add_step(s, i, y, t, o, a, c, last=(i == len(steps)))
        if i < len(steps):
            add_arrow(s, y + STEP_H)
        y += STEP_H + STEP_GAP
    s.text(30, 40, "每一步都在为“从错配读出甲基化”整理证据：转化错配是信号本体，但它的前提必须被显式管理",
           size=15, mono=False, fill=COLOR_PRIMARY, weight="bold")
    return s


def gen_glori_pipeline():
    W, H = 760, 620
    s = Svg(W, H, "GLORI 分析流程",
            "GLORI 数据从 FASTQ 到位点修饰比例的六个步骤：质控看 A 的坍缩，STAR 剪接比对，"
            "逐位点 A/G 计数，过滤混杂，最后进入定量与差异分析。")
    steps = [
        ("原始质控", "FastQC 报告", "每碱基序列含量：插入序列中 A 坍缩至约 1%",
         "检查：G 升高、A 下降，两端为引物/接头"),
        ("修剪", "trimmed FASTQ", "去除引物与接头、低质量末端（cutadapt）",
         "检查：保留率、读长分布"),
        ("剪接比对与去重", "去重 BAM", "mRNA reads 跨外显子比对（STAR ≥2.7.5c）",
         "检查：比对率、rRNA 残留"),
        ("逐位点 A/G 计数", "位点表（AGcov/Acov）", "每位点统计读作 A 与读作 G 的 reads",
         "检查：覆盖深度分布"),
        ("位点过滤", "过滤后位点表", "覆盖过低剔除；A/G SNP 位点用变异库排除",
         "检查：SNP 来源数据库版本"),
        ("修饰比例表就绪，进入定量", "Ratio = A/(A+G)", "重复一致性、组间逐位点检验（8.5）",
         "检查：重复相关、显著方向一致"),
    ]
    y = 78
    for i, (t, o, a, c) in enumerate(steps, 1):
        add_step(s, i, y, t, o, a, c, last=(i == len(steps)))
        if i < len(steps):
            add_arrow(s, y + STEP_H)
        y += STEP_H + STEP_GAP
    s.text(30, 40, "与 BS-seq 同构：化学转化改写 reads 的碱基组成，分析链把它翻译回逐位点修饰比例",
           size=15, mono=False, fill=COLOR_PRIMARY, weight="bold")
    return s


def main():
    OUT.mkdir(parents=True, exist_ok=True)

    def _save(self):
        head = (f"<svg xmlns='http://www.w3.org/2000/svg' width='{self.w}' height='{self.h}' "
                f"viewBox='0 0 {self.w} {self.h}'>\n<title>{self.title}</title>\n<desc>{self.desc}</desc>\n")
        return head + "\n".join(self.parts) + "\n</svg>\n"

    global Svg
    Svg.__str__ = _save
    for name, fn in (("bs-pipeline-overview.svg", gen_bs_pipeline),
                     ("glori-pipeline-overview.svg", gen_glori_pipeline)):
        svg = fn()
        p = OUT / name
        p.write_text(str(svg), encoding="utf-8")
        print("written", p)


if __name__ == "__main__":
    main()
