#!/usr/bin/env python3
"""Figures 5.1/5.2: RNA functions and cell-specific transcriptomes.

Conceptual illustrations, not measured abundances or molecular structures.
RNA roles: NHGRI RNA Fact Sheet and OpenStax Biology 2e, transcription/translation.
Run: python3 scripts/figures/ch05/gen_rna_concepts.py
"""
from common import Svg, save, COLOR_PRIMARY as GREEN, COLOR_FILL as PALE
from common import COLOR_WARN as AMBER, COLOR_WARN_FILL as CREAM, COLOR_TEXT as INK


def path(s, d, color=GREEN, width=2.8, fill="none", extra=""):
    s.add(f'<path d="{d}" fill="{fill}" stroke="{color}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round" {extra}/>')


def circle(s, x, y, r, fill=PALE, stroke=GREEN, width=1.8):
    s.add(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{width}"/>')


def label(s, x, y, txt, size=18, color=INK, weight="normal", anchor="start"):
    s.text(x, y, txt, size=size, mono=False, fill=color, weight=weight, anchor=anchor)


def wave(s, x, y, length=62, color=GREEN, width=3):
    d=f'M {x} {y}'
    for i in range(4):
        t=length/4
        d+=f' q {t/4} -7 {t/2} 0 t {t/2} 0'
    path(s,d,color,width)


def dna(s, x, y, length=220):
    import math
    for phase in [0, math.pi]:
        pts=[(x+i*length/80,y+16*math.sin(i/80*math.pi*5+phase)) for i in range(81)]
        path(s,'M '+' L '.join(f'{a:.2f} {b:.2f}' for a,b in pts),GREEN,3)
    for i in range(2,80,4):
        xx=x+i*length/80; dy=16*math.sin(i/80*math.pi*5)
        s.line(xx,y-dy,xx,y+dy,stroke=GREEN,sw=1.6)


def rna_classes():
    s=Svg(780,800,"RNA 的主要类型与分工", "核内 DNA 转录产生 RNA，snRNA 参与剪接；mRNA 进入细胞质，在含 rRNA 的核糖体上由 tRNA 配合翻译；miRNA、siRNA、lncRNA 与 circRNA 以不同方式参与调控。所画为代表性形态和作用场景。")
    s.rect(16,55,348,463,fill=PALE,stroke=GREEN,sw=1.6,rx=45)
    label(s,40,91,"细胞核",22,GREEN,"bold")
    label(s,414,91,"细胞质",22,GREEN,"bold")
    dna(s,68,143,236)
    label(s,180,126,"DNA",19,GREEN,"bold", "middle")
    s.arrow(190,169,190,213,sw=2)
    label(s,212,194,"转录",18)
    path(s,'M 69 243 L 305 243', GREEN,3)
    for x in [75,162,257]: s.rect(x,234,38,18,fill=GREEN,stroke=GREEN,rx=2)
    label(s,185,279,"前体 mRNA",19,anchor="middle")
    # A snRNA stem-loop at the splice site; it is part of the spliceosome.
    path(s,'M 86 334 L 86 316 C 61 310 66 290 86 292 C 106 290 111 310 94 316 L 94 334',AMBER,3)
    for y in [316,323,330]:s.line(86,y,94,y,stroke=AMBER,sw=1.6)
    label(s,43,364,"snRNA",18,AMBER,"bold")
    s.arrow(190,291,190,355,sw=2)
    label(s,210,329,"剪接",18)
    s.line(122,332,163,332,stroke=AMBER,sw=2)
    for x in [116,155,194]:s.rect(x,376,37,18,fill=GREEN,stroke=GREEN,rx=2)
    wave(s,232,385,40)
    label(s,184,425,"成熟 mRNA",19,anchor="middle")
    s.arrow(280,385,434,385,sw=2.5)
    label(s,387,418,"输出",16,anchor="middle")
    # Nucleus border interrupted by a pore where the mRNA exits.
    s.rect(354,367,18,37,fill="#fcfcf9",stroke="none")
    s.arrow(280,385,434,385,sw=2.5)
    # The ribosome straddles mRNA, with rRNA highlighted inside the subunits.
    path(s,'M 454 369 C 444 290 503 257 565 275 C 614 285 641 323 625 369 Z',GREEN,2,PALE)
    path(s,'M 453 400 C 464 445 613 445 626 400 Z',GREEN,2,PALE)
    path(s,'M 476 340 C 493 311 526 349 543 323 S 590 317 604 345',GREEN,4)
    path(s,'M 480 416 Q 519 404 543 421 T 603 412',GREEN,3)
    wave(s,442,385,252,GREEN,3)
    label(s,668,421,"mRNA",19,GREEN,"bold", "middle")
    label(s,568,474,"核糖体（含 rRNA）",19,GREEN,"bold","middle")
    # A cloverleaf tRNA with anticodon pointing to the mRNA.
    path(s,'M 533 375 L 533 302 L 515 302 C 492 300 491 273 513 272 L 526 272 L 526 255 C 506 234 516 214 535 231 C 554 214 564 234 544 255 L 544 272 L 557 272 C 579 273 578 300 555 302 L 539 302 L 539 375 Q 536 386 533 375',AMBER,3)
    label(s,435,236,"tRNA",20,AMBER,"bold")
    s.line(489,239,516,264,stroke=AMBER,sw=1.5)
    circle(s,535,210,7,CREAM,AMBER)
    label(s,576,207,"携带氨基酸",16)
    s.line(544,210,566,203,stroke=AMBER,sw=1.4)
    for j,(x,y) in enumerate([(605,272),(616,255),(633,249),(648,233),(667,227),(680,210)]):
        if j: s.line(px,py,x,y,stroke=AMBER,sw=3)
        circle(s,x,y,7,CREAM,AMBER);px,py=x,y
    label(s,651,176,"蛋白质",21,AMBER,"bold","middle")
    label(s,656,321,"翻译",19)
    # Regulatory RNA examples are a separate strip, avoiding a false universal pathway.
    label(s,28,559,"非编码 RNA 的调控作用与形态",22,GREEN,"bold")
    s.line(28,575,752,575,stroke=GREEN,sw=1.4)
    # miRNA/siRNA pairing to a target RNA.
    wave(s,32,626,207,GREEN,2.6)
    path(s,'M 102 642 L 174 642',AMBER,4)
    for x in range(106,174,9):s.line(x,631,x,638,stroke=AMBER,sw=1.5)
    label(s,139,682,"miRNA / siRNA",18,AMBER,"bold","middle")
    label(s,139,714,"配对识别靶 RNA",17,anchor="middle")
    label(s,139,740,"影响稳定性或翻译",16,anchor="middle")
    # lncRNA: long folded molecule, no suggestion all lncRNAs share one function.
    path(s,'M 305 646 C 300 604 344 600 348 630 S 376 661 380 627 S 423 600 429 645 C 431 673 390 659 389 641 S 355 629 350 651 S 321 669 305 646',GREEN,3)
    label(s,372,699,"lncRNA",19,GREEN,"bold","middle")
    label(s,372,732,"长链，作用与位置多样",16,anchor="middle")
    # circRNA: a covalently closed RNA, a distinct morphology rather than one fixed mechanism.
    path(s,'M 612 602 C 669 601 683 663 638 678 C 582 697 552 641 587 616 C 595 610 603 605 612 602',GREEN,3)
    s.rect(584,607,35,13,fill=GREEN,stroke=GREEN,rx=3)
    label(s,620,711,"circRNA",19,GREEN,"bold","middle")
    label(s,620,740,"首尾共价相连的环状 RNA",16,anchor="middle")
    label(s,390,783,"形态与作用场景为示意；不同非编码 RNA 的具体功能需要分别验证。",15,anchor="middle")
    save('rna-classes-mechanism',s)


def neuron(s,cx,cy):
    for d in [f'M {cx-14} {cy-8} Q {cx-43} {cy-19} {cx-52} {cy-45} M {cx-36} {cy-16} L {cx-67} {cy-15}',
              f'M {cx} {cy-16} Q {cx-4} {cy-43} {cx+8} {cy-62} M {cx} {cy-37} L {cx-16} {cy-57}',
              f'M {cx+16} {cy-7} Q {cx+44} {cy-24} {cx+61} {cy-46} M {cx+43} {cy-25} L {cx+72} {cy-25}',
              f'M {cx-8} {cy+14} Q {cx-22} {cy+42} {cx-46} {cy+53} M {cx-27} {cy+37} L {cx-26} {cy+60}',
              f'M {cx+12} {cy+10} C {cx+31} {cy+37} {cx+54} {cy+20} {cx+84} {cy+49}']:
        path(s,d,GREEN,3)
    path(s,f'M {cx-20} {cy-6} Q {cx-14} {cy-27} {cx+8} {cy-19} Q {cx+32} {cy-3} {cx+10} {cy+19} Q {cx-22} {cy+27} {cx-20} {cy-6}',GREEN,2,PALE)
    circle(s,cx,cy,9,CREAM,AMBER)


def cells_transcriptomes():
    s=Svg(780,720,'相同基因组，不同转录组','神经、肌肉和上皮细胞具有相同的一组示意基因 A 到 D；RNA A 共有，RNA B、C、D 在不同细胞中丰度不同。波浪线数量和对齐条形图均为示意，不是实测结果。')
    label(s,390,34,'同一生物体：基因组基本相同',23,GREEN,'bold','middle')
    dna(s,245,72,290)
    for x,t in zip([283,344,405,466],['A','B','C','D']):
        s.rect(x,94,32,26,fill=PALE,stroke=GREEN,rx=3);label(s,x+16,114,t,18,GREEN,'bold','middle')
    centers=[144,390,636]
    for x in centers:
        s.arrow(390 if x==390 else (298 if x<390 else 482),129,x,163,stroke=GREEN)
    neuron(s,144,239)
    path(s,'M 308 267 C 358 187 417 194 472 232 C 420 308 353 297 308 267 Z',GREEN,2,PALE)
    for j in range(6):s.line(343+j*16,225,324+j*16,272,stroke=GREEN,sw=1)
    circle(s,390,250,11,CREAM,AMBER)
    for x in [574,616,658]:
        s.rect(x,193,39,97,fill=PALE,stroke=GREEN,rx=8);circle(s,x+20,253,9,CREAM,AMBER)
        for dx in [8,15,22,29]:s.line(x+dx,187,x+dx,178,stroke=GREEN,sw=1.5)
    for x,t in zip(centers,['神经细胞','肌肉细胞','上皮细胞']):
        label(s,x,326,t,22,GREEN,'bold','middle');s.arrow(x,340,x,367)
    levels=[[3,5,1,1],[3,1,5,1],[3,1,1,5]]
    for col,cx in enumerate(centers):
        s.rect(cx-110,383,220,140,fill='#fcfcf9',stroke='#9ca3af',rx=12)
        for row,gene in enumerate('ABCD'):
            y=409+row*30
            label(s,cx-94,y+5,gene,17,GREEN,'bold')
            for j in range(levels[col][row]):wave(s,cx-66+j*31,y,23,GREEN,2.1)
        for row,gene in enumerate('ABCD'):
            y=568+row*25
            label(s,cx-93,y+5,gene,16,GREEN)
            s.rect(cx-65,y-7,levels[col][row]*30,12,fill=GREEN,stroke='none',rx=2)
        label(s,cx,549,'对应 RNA 的相对丰度',15,anchor='middle')
    label(s,390,686,'共有的 RNA 仍然存在，各类 RNA 的丰度组合发生变化。',20,GREEN,'bold','middle')
    label(s,390,711,'A–D 为示意标签；分子数和条形长度不代表实测值。',16,anchor='middle')
    save('cell-transcriptomes',s)


if __name__=='__main__':
    rna_classes()
    cells_transcriptomes()
