#!/usr/bin/env python3
"""10x/BD physical capture compartments (Figure 9.1).

10x Chromium Next GEM 3′ v3.1, CG000204 Rev D, pp15–16;
BD Rhapsody Single Cell Capture and cDNA Synthesis User Guide, pp4–6.
BD beads are retrieved/washed before RT; GEM RT occurs inside droplets.
Run: python3 scripts/figures/ch09/gen_platforms.py
"""
from common import Svg, save, COLOR_PRIMARY as GREEN, COLOR_FILL as PALE
from common import COLOR_WARN as AMBER, COLOR_WARN_FILL as CREAM


def path(s,d,color=GREEN,width=2,fill='none'):
    s.add(f'<path d="{d}" fill="{fill}" stroke="{color}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round"/>')


def circle(s,x,y,r,fill=PALE,color=GREEN,width=1.6):
    s.add(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{color}" stroke-width="{width}"/>')


def text(s,x,y,t,size=18,color='#333333',bold=False,anchor='start'):
    s.text(x,y,t,size=size,mono=False,fill=color,weight='bold' if bold else 'normal',anchor=anchor)


def cell(s,x,y,r=13):
    circle(s,x,y,r);circle(s,x+2,y,r*.33,CREAM,AMBER,1)


def bead(s,x,y,r=11,probes=True):
    import math
    circle(s,x,y,r,CREAM,AMBER)
    if probes:
        for a in range(0,360,45):
            t=math.radians(a);s.line(x+r*math.cos(t),y+r*math.sin(t),x+(r+7)*math.cos(t),y+(r+7)*math.sin(t),stroke=AMBER,sw=1.3)


def rna(s,x,y,length=42):
    path(s,f'M {x} {y} q {length/8} -9 {length/4} 0 t {length/4} 0 t {length/4} 0 t {length/4} 0',GREEN,2.4)


def tube(s,x,y,beads=False):
    path(s,f'M {x} {y} L {x+70} {y} L {x+70} {y+54} L {x+35} {y+86} L {x} {y+54} Z',GREEN,2,PALE)
    s.rect(x-4,y-8,78,10,fill=CREAM,stroke=GREEN,rx=3)
    for j in range(3):
        if beads:bead(s,x+17+j*17,y+20+j*10,5,False)
        else:s.line(x+14,y+18+j*13,x+53,y+18+j*13,stroke=GREEN,sw=2)


def main():
    s=Svg(800,930,'10x Genomics 与 BD Rhapsody 的单细胞捕获流程',
          '10x 通过微流控形成包含细胞与凝胶珠的油包水液滴，液滴内反转录后破乳。BD 用微孔捕获细胞与磁珠，在孔内裂解并捕获 RNA；磁珠回收清洗后在管中反转录。所画为理想捕获单元，未按比例。')
    s.line(400,60,400,857,stroke='#9ca3af',sw=1,dash='4 5')
    text(s,198,35,'10x Genomics',24,GREEN,True,'middle');text(s,602,35,'BD Rhapsody',24,GREEN,True,'middle')
    text(s,198,65,'油包水液滴',18,anchor='middle');text(s,602,65,'固态微孔',18,anchor='middle')
    path(s,'M 31 119 L 144 119 L 202 161 L 215 161 L 215 112 L 242 112 L 242 161 L 263 150 L 376 150 L 376 210 L 263 210 L 242 199 L 242 250 L 215 250 L 215 199 L 202 199 L 144 245 L 31 245 L 31 214 L 134 214 L 179 180 L 134 149 L 31 149 Z',GREEN,1.7,PALE)
    cell(s,66,134,10);cell(s,117,134,10)
    bead(s,67,229,9);bead(s,117,229,9)
    text(s,30,105,'细胞＋试剂',17);text(s,29,277,'带引物的凝胶珠',17,AMBER)
    text(s,269,113,'油相',17,AMBER)
    s.arrow(229,123,229,156,stroke=AMBER);s.arrow(229,239,229,207,stroke=AMBER)
    for x in [278,343]:
        circle(s,x,180,25,'#fcfcf9',GREEN,1.8);cell(s,x-8,180,8);bead(s,x+11,180,6,False)
    text(s,302,227,'GEM 液滴',17,GREEN,True,'middle')
    text(s,429,105,'细胞落孔 → 加载磁珠',17)
    for x in [478,588,698]:
        cell(s,x,126,11);s.arrow(x,142,x,170)
    d='M 427 177 L 444 177 L 444 234 Q 444 243 454 243 L 502 243 Q 512 243 512 234 L 512 177 L 554 177 L 554 234 Q 554 243 564 243 L 612 243 Q 622 243 622 234 L 622 177 L 664 177 L 664 234 Q 664 243 674 243 L 722 243 Q 732 243 732 234 L 732 177 L 776 177 L 776 261 L 427 261 Z'
    path(s,d,GREEN,1.8,PALE)
    for x in [478,588,698]:cell(s,x-11,224,13);bead(s,x+17,230,8)
    text(s,602,284,'侧面剖面：细胞与磁珠同处一孔',17,anchor='middle')
    for x in [198,602]:s.arrow(x,301,x,334,sw=2)
    text(s,198,365,'液滴内：裂解与反转录',20,GREEN,True,'middle')
    text(s,602,365,'微孔内：裂解与 RNA 捕获',20,GREEN,True,'middle')
    circle(s,198,483,106,CREAM,AMBER,1.6);circle(s,198,483,97,'#fcfcf9',GREEN,2)
    path(s,'M 140 467 C 115 449 137 416 158 426 M 164 449 C 169 468 151 481 142 475',GREEN,2)
    rna(s,143,451,47);rna(s,158,476,47)
    for x,y in [(236,428),(246,441),(225,444),(255,456),(236,458)]:circle(s,x,y,3,CREAM,AMBER,1)
    text(s,198,415,'凝胶珠溶解',15,AMBER,False,'middle')
    s.line(232,419,242,428,stroke=AMBER,sw=1)
    for x,y in [(228,478),(216,493),(242,502)]:s.line(x,y,x+23,y,stroke=AMBER,sw=2)
    s.arrow(184,504,184,533,sw=1.5)
    s.line(158,550,248,550,stroke=GREEN,sw=3);s.line(136,550,158,550,stroke=AMBER,sw=3)
    text(s,198,612,'带条形码的 cDNA',16,anchor='middle')
    path(s,'M 452 399 L 478 399 L 478 561 Q 478 584 501 584 L 703 584 Q 727 584 727 561 L 727 399 L 754 399 L 754 609 L 452 609 Z',GREEN,2,PALE)
    path(s,'M 524 458 C 497 442 522 410 541 424 M 548 446 C 551 463 531 472 525 467',GREEN,2)
    rna(s,536,444,48);rna(s,549,469,41);rna(s,599,425,43)
    bead(s,637,531,31)
    for x,y in [(594,513),(645,488),(662,550)]:rna(s,x,y,35)
    s.arrow(567,472,608,501,sw=1.3)
    text(s,525,543,'mRNA',16);text(s,637,580,'捕获磁珠',16,AMBER,False,'middle')
    for x in [198,602]:s.arrow(x,623,x,657,sw=2)
    text(s,198,686,'破乳，回收 cDNA',20,GREEN,True,'middle')
    text(s,602,682,'磁珠回收、清洗',20,GREEN,True,'middle')
    text(s,602,709,'再在管内反转录',19,GREEN,True,'middle')
    tube(s,163,722,False);tube(s,567,739,True)
    text(s,198,843,'扩增与建库',18,anchor='middle');text(s,602,850,'扩增与建库',18,anchor='middle')
    s.line(30,870,770,870,stroke=GREEN,sw=1)
    text(s,400,896,'两条路线都保留细胞来源信息，再按各平台流程完成建库和测序。',18,GREEN,False,'middle')
    text(s,400,922,'图示为理想捕获单元；尺寸、分子数和空位比例均未按实际绘制。',16,anchor='middle')
    save('008-10x-bd-platforms',s)


if __name__=='__main__':main()
