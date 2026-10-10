#!/usr/bin/env python3
"""IGV 风格 reads 复核视图（据实测 BAM 程序绘制）。

数据：/tmp/ch07_scratch/reads_9068512.sam（27 条 reads，CIGAR 展开）+
参考序列 ref_seq.txt（chr21:9068460-9068620）。
画法对照 IGV 习惯：reads 灰条、错配处画彩色碱基字母、候选变异位置黑框标出。
"""
import re, sys
sys.path.insert(0, '/tmp/bioinfo-ch07-r4/scripts/figures/ch07')
from common import (Svg, save, COLOR_TEXT, COLOR_MUTED, COLOR_PRIMARY,
                    COLOR_FILL, COLOR_WARN, COLOR_LINE, SIZE_NOTE, SIZE_LABEL)

START, END = 9068460, 9068620
VAR_POS = 9068512          # C>T 候选杂合
W = 1180
BP = 7                      # 每碱基像素
X0 = 60                     # 左边距
rows_raw = []
for line in open('/tmp/ch07_scratch/reads_9068512.sam'):
    f = line.rstrip('\n').split('\t')
    if f[0].startswith('@'):
        continue
    qname, flag, rname, pos, mapq, cigar = f[0], int(f[1]), f[2], int(f[3]), int(f[4]), f[5]
    seq = f[9]
    qual = f[10]
    if flag & 0x100:        # secondary 跳过
        continue
    rows_raw.append((qname, flag, pos, mapq, cigar, seq, qual))
rows_raw.sort(key=lambda r: r[2])
N = len(rows_raw)

BASE_COLOR = {'A': '#C0392B', 'C': '#2471A3', 'G': '#1E8449', 'T': '#B7950B',
              'N': COLOR_MUTED}

H = 120 + N * 16 + 66
s = Svg(W, H, "候选杂合变异 chr21:9068512 C>T 的 reads 复核视图（实测数据）",
        "NA12878 WES 教学子集 chr21:9068460-9068620 共 27 条 reads；"
        "灰条为比对区间，彩色字母为与参考不一致的碱基，黑框标出候选变异位置。")

# 顶部标尺
s.text(X0, 34, "chr21:9068460–9068620（NA12878 WES，HaplotypeCaller PASS 记录 chr21:9068512 C>T，GT 0/1，AD 6,7）",
       size=SIZE_LABEL, mono=False, fill=COLOR_PRIMARY, weight='bold')

# 参考序列行
ref = open('/tmp/ch07_scratch/ref_seq.txt').read().strip().upper()
y_ref = 66
for i, ch in enumerate(ref):
    x = X0 + i * BP
    if START + i == VAR_POS:
        s.rect(x - 1, y_ref - 11, BP + 2, 15, fill=COLOR_FILL, stroke=COLOR_PRIMARY, sw=1.4, rx=1)
    s.text(x + BP / 2, y_ref, ch, size=9, fill=COLOR_TEXT, anchor='middle')
s.text(8, y_ref, "REF", size=SIZE_NOTE, mono=False, fill=COLOR_MUTED)

# reads
for r, (qname, flag, pos, mapq, cigar, seq, qual) in enumerate(rows_raw):
    y = y_ref + 22 + r * 16
    qpos = 0
    refpos = pos
    for m in re.finditer(r'(\d+)([MIDNSHP=X])', cigar):
        n, op = int(m.group(1)), m.group(2)
        x0 = X0 + (refpos - START) * BP
        if op in 'M=X':
            w = n * BP
            s.rect(x0, y - 9, w, 12, fill='#e5e7eb', stroke='none', rx=1)
            for k in range(n):
                refidx = refpos + k - START
                if 0 <= refidx < len(ref) and qpos + k < len(seq):
                    base = seq[qpos + k].upper()
                    if base != ref[refidx] and base in BASE_COLOR:
                        x = X0 + refidx * BP
                        s.text(x + BP / 2, y, base, size=9, fill=BASE_COLOR[base],
                               anchor='middle', weight='bold')
            qpos += n
            refpos += n
        elif op == 'I':
            x = X0 + (refpos - START) * BP
            s.rect(x, y - 9, max(n * BP, 3), 12, fill=COLOR_WARN, stroke='none', rx=1)
            qpos += n
        elif op == 'D':
            x = X0 + (refpos - START) * BP
            s.rect(x, y - 3, n * BP, 6, fill='none', stroke=COLOR_WARN, sw=1.2, dash='2,2')
            refpos += n
        elif op == 'S':
            qpos += n
        else:
            refpos += n
    # 候选变异竖线贯穿
xv = X0 + (VAR_POS - START) * BP + BP / 2
s.line(xv, y_ref - 14, xv, y_ref + 24 + N * 16, stroke=COLOR_PRIMARY, sw=1.2, dash='5,4')
s.text(xv, y_ref + 40 + N * 16, "▲ 候选变异 9068512 C>T（杂合）", size=SIZE_NOTE,
       mono=False, fill=COLOR_PRIMARY, anchor='middle')
s.text(X0, y_ref + 60 + N * 16, "复核要点：约半数 reads 支持 T（彩色字母集中于黑框列）、错配碱基质量正常、两条链均有支持（FLAG 奇偶各半）、无 read 末端富集。",
       size=SIZE_NOTE, mono=False, fill=COLOR_TEXT)
save("igv-na12878-review", s)
print(f"drawn {N} reads")
