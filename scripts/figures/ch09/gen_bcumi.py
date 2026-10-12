#!/usr/bin/env python3
"""Figure 9.2: a checked molecule-to-matrix example, styled like Figure 9.1.

Reads are paired records: R1 carries barcode/UMI and R2 supplies gene assignment.
Deduplication is within a corrected cell-barcode + gene group, not global by UMI.
The illustrative records assume no UMI collisions, errors or ambiguous mapping.
Sources: 10x CG000416 Rev D, p.22; Cell Ranger gene-expression algorithms.
Run: python3 scripts/figures/ch09/gen_bcumi.py
"""
from collections import defaultdict
from common import Svg, save, COLOR_PRIMARY as GREEN, COLOR_FILL as PALE, COLOR_WARN as AMBER, COLOR_WARN_FILL as CREAM, COLOR_MUTED as MUTED, COLOR_BLUE as BLUE

BCA, BCB = 'AACGTA', 'TTGCAC'
# Five paired records for Gene A in cell A, plus the remaining example molecules.
RECORDS = [(BCA, 'Gene A', 'ATGC')]*3 + [(BCA, 'Gene A', 'GCTA')]*2 + [(BCA, 'Gene B', 'CAGT'), (BCB, 'Gene A', 'ATGC')]


def text(s,x,y,t,size=18,color='#333333',bold=False,anchor='start',mono=False):
    s.text(x,y,t,size=size,fill=color,weight='bold' if bold else 'normal',anchor=anchor,mono=mono)


def path(s,d,color=GREEN,width=2,fill='none'):
    s.add(f'<path d="{d}" fill="{fill}" stroke="{color}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round"/>')


def wave(s,x,y,color=GREEN,length=52):
    path(s,f'M {x} {y} q 6 -9 12 0 t 12 0 t 12 0 t 12 0',color,2.7)


def cell(s,cx,cy,label,molecules):
    path(s,f'M {cx-93} {cy} C {cx-88} {cy-61}, {cx-40} {cy-65}, {cx+11} {cy-55} C {cx+92} {cy-70}, {cx+101} {cy-15}, {cx+88} {cy+26} C {cx+71} {cy+72}, {cx-33} {cy+65}, {cx-77} {cy+39} Z',GREEN,2.1,PALE)
    s.add(f'<ellipse cx="{cx-53}" cy="{cy+2}" rx="22" ry="26" fill="#ffffff" stroke="{GREEN}" stroke-width="1.5"/>')
    for i,gene in enumerate(molecules):wave(s,cx-15,cy-29+i*29,GREEN if gene=='Gene A' else BLUE)
    text(s,cx,cy-82,label,23,GREEN,True,'middle')


def main():
    umi_sets=defaultdict(set)
    for bc,gene,umi in RECORDS:umi_sets[bc,gene].add(umi)
    matrix=[[len(umi_sets[bc,gene]) for bc in [BCA,BCB]] for gene in ['Gene A','Gene B']]
    assert matrix==[[2,1],[1,0]]
    expanded=[r for r in RECORDS if r[0]==BCA and r[1]=='Gene A']
    assert len(expanded)==5 and len({r[2] for r in expanded})==2
    s=Svg(800,1060,'barcode、UMI 与基因×细胞计数矩阵',
          '两个细胞捕获的 RNA 获得细胞 barcode 和 UMI。展开细胞 A 的 Gene A：五条配对测序记录中 ATGC 出现三次、GCTA 出现两次，同细胞同基因按校正后的 UMI 合并为两个分子。矩阵行是 Gene A、Gene B，列是细胞 A、B，数值为 2、1 和 1、0。序列缩短，数量为示意。')
    text(s,28,35,'① 捕获 RNA，加入细胞 barcode 和 UMI',23,GREEN,True)
    cell(s,206,158,'细胞 A',['Gene A','Gene A','Gene B'])
    cell(s,596,158,'细胞 B',['Gene A'])
    text(s,206,239,'barcode：'+BCA,18,GREEN,False,'middle',True)
    text(s,596,239,'barcode：'+BCB,18,GREEN,False,'middle',True)
    text(s,206,270,'Gene A：2 个　Gene B：1 个',17,anchor='middle')
    text(s,596,270,'Gene A：1 个　Gene B：0 个',17,anchor='middle')
    text(s,400,300,'只画本例捕获到的 RNA；不同基因以颜色和名称区分。',16,MUTED,anchor='middle')
    s.line(28,319,772,319,stroke='#a7c9c0',sw=1)

    text(s,28,354,'② 展开细胞 A 的 Gene A：扩增产生多条测序记录',23,GREEN,True)
    text(s,111,388,'R1：细胞 barcode',17,GREEN,True,'middle')
    text(s,294,388,'R1：UMI',17,AMBER,True,'middle')
    text(s,465,388,'R2：cDNA 比对结果',17,GREEN,True,'middle')
    text(s,681,388,'合并 PCR 重复',17,GREEN,True,'middle')
    for i,(_,gene,umi) in enumerate(expanded):
        y=405+i*44
        # These are paired metadata records, deliberately separated R1 / R2.
        s.rect(31,y,159,32,fill=PALE,stroke=GREEN,rx=4)
        s.rect(227,y,130,32,fill=CREAM,stroke=AMBER,rx=4)
        s.rect(395,y,142,32,fill='#f4f6f5',stroke='#9ca3af',rx=4)
        text(s,110,y+23,BCA,20,GREEN,anchor='middle',mono=True)
        text(s,292,y+23,umi,20,AMBER,anchor='middle',mono=True)
        text(s,466,y+23,gene,20,GREEN,anchor='middle',mono=True)
        # A dashed link means metadata from one read pair, not a continuous read.
        s.line(190,y+16,227,y+16,stroke='#9ca3af',dash='3,4')
        s.line(357,y+16,395,y+16,stroke='#9ca3af',dash='3,4')
    for y0,y1,mid,umi,n in [(405,525,465,'ATGC',3),(537,613,575,'GCTA',2)]:
        path(s,f'M 552 {y0+3} H 564 V {y1-3} H 552',AMBER,1.8)
        s.arrow(570,mid,620,mid,stroke=GREEN)
        wave(s,640,mid-10)
        text(s,666,mid+18,umi,18,AMBER,anchor='middle',mono=True)
        text(s,733,mid-2,'1 个',19,GREEN,True,'middle')
        text(s,666,mid+42,str(n)+' 条记录',15,MUTED,anchor='middle')
    text(s,400,657,'5 条记录 → 2 个不同 UMI → 计 2 个分子',23,GREEN,True,'middle')
    text(s,400,688,'去重范围：同一细胞、同一基因；使用校正后的 UMI。',18,anchor='middle')
    s.arrow(400,706,400,736,stroke=GREEN,sw=2)

    text(s,28,772,'③ 填入基因×细胞计数矩阵',23,GREEN,True)
    text(s,243,815,'行：基因',17,MUTED,anchor='end')
    text(s,378,812,'细胞 A',20,GREEN,True,'middle')
    text(s,560,812,'细胞 B',20,GREEN,True,'middle')
    text(s,696,815,'列：细胞',17,MUTED,anchor='middle')
    for i,gene in enumerate(['Gene A','Gene B']):
        y=837+i*59
        text(s,246,y+35,gene,20,GREEN if i==0 else BLUE,True,'end')
        for j,value in enumerate(matrix[i]):
            x=289+j*182
            s.rect(x,y,177,53,fill=CREAM if (i,j)==(0,0) else PALE,stroke=AMBER if (i,j)==(0,0) else GREEN,sw=2 if (i,j)==(0,0) else 1.1,rx=4)
            text(s,x+88.5,y+36,str(value),28,AMBER if (i,j)==(0,0) else GREEN,True,'middle')
    text(s,400,993,'每个数字＝该细胞中、该基因被捕获并计数的 UMI 分子数',18,anchor='middle')
    text(s,400,1028,'0 表示本次未检出；序列长度和分子数量均为教学示意。',16,MUTED,anchor='middle')
    save('002-bc-umi-matrix',s)
    print({'records_in_expanded_group':len(expanded),'unique_UMIs':2,'matrix':matrix})


if __name__=='__main__':main()
